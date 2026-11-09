"""Normalize classified traffic counts from the D1 workbook.

Run from the repository root:
    python Data/traffic_pipeline/preprocess.py
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[2]
DEFAULT_WORKBOOK = ROOT / "Data/test_data/TMC-14 Number (D1).xlsx"
DEFAULT_OUTPUT = ROOT / "Data/traffic_pipeline/output"
VALUE_COLUMNS = {
    "B": "car_taxi_tempo_auto_pickup",
    "C": "motorcycle_scooter",
    "D": "tractor_lcv_minibus",
    "E": "three_wheeler_axle_truck_bus",
    "F": "tractor_trailer_truck_mav",
    "G": "reported_total_fast_vehicles",
    "H": "cycle",
    "I": "cycle_rickshaw",
    "J": "hand_cart",
    "K": "horse_drawn",
    "L": "bullock_cart",
    "M": "reported_total_slow_vehicles",
    "N": "reported_grand_total_vehicles",
    "O": "reported_grand_total_pcu",
}
FAST = list(VALUE_COLUMNS.values())[:5]
SLOW = list(VALUE_COLUMNS.values())[6:11]


def interval_minutes(value: object) -> tuple[int, str]:
    raw = str(value).strip()
    match = re.fullmatch(r"(\d{2})(\d{2})-(\d{2})(\d{2})", raw)
    if not match:
        raise ValueError(f"Unexpected interval label: {value!r}")
    h1, m1, h2, m2 = map(int, match.groups())
    start = h1 * 60 + m1
    end = h2 * 60 + m2
    if end <= start:
        end += 24 * 60
    if end - start != 15:
        raise ValueError(f"Interval is not 15 minutes: {raw}")
    return start, raw


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--workbook", type=Path, default=DEFAULT_WORKBOOK)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--test-fraction", type=float, default=0.2)
    args = parser.parse_args()
    from openpyxl import load_workbook

    workbook_path = args.workbook.resolve()
    output = args.output_dir.resolve()
    processed, reports = output / "processed", output / "reports"
    processed.mkdir(parents=True, exist_ok=True)
    reports.mkdir(parents=True, exist_ok=True)
    digest = hashlib.sha256(workbook_path.read_bytes()).hexdigest()
    # Normal mode avoids repeated XML scans when looking up a row and its columns.
    wb = load_workbook(workbook_path, data_only=True, read_only=False)

    summary = wb["Summary"] if "Summary" in wb.sheetnames else None
    observation_date = pd.to_datetime(summary["I1"].value).normalize() if summary else pd.NaT
    records, audits, skipped_non_interval_rows = [], [], []
    for ws in wb.worksheets:
        is_movement = bool(re.fullmatch(r"V_\d+", ws.title))
        audits.append({"sheet": ws.title, "max_row": ws.max_row, "max_column": ws.max_column,
                       "included_as_movement": is_movement, "header_row": 6 if is_movement else None})
        if not is_movement:
            continue
        origin, destination = ws["B4"].value, ws["E4"].value
        for row in range(8, ws.max_row + 1):
            raw_time = ws.cell(row, 1).value
            if raw_time is None or not str(raw_time).strip():
                continue
            try:
                start_minute, raw_label = interval_minutes(raw_time)
            except ValueError:
                skipped_non_interval_rows.append({"sheet": ws.title, "excel_row": row, "value": str(raw_time)})
                continue
            day_offset, clock_minute = divmod(start_minute, 24 * 60)
            # The survey runs from 08:00 through 07:45 the following morning.
            if clock_minute < 8 * 60:
                day_offset += 1
            start = observation_date + pd.Timedelta(days=day_offset, minutes=clock_minute) if pd.notna(observation_date) else pd.NaT
            vals = {name: pd.to_numeric(ws[f"{col}{row}"].value, errors="coerce")
                    for col, name in VALUE_COLUMNS.items()}
            row_data = {
                "source_file": workbook_path.name, "source_sha256": digest,
                "source_sheet": ws.title, "source_excel_row": row,
                "origin": origin, "destination": destination,
                "raw_interval": raw_label, "interval_start": start,
                "interval_end": start + pd.Timedelta(minutes=15) if pd.notna(start) else pd.NaT,
                "interval_minutes": 15, **vals,
            }
            row_data["computed_fast_vehicle_total"] = sum(row_data[c] for c in FAST if pd.notna(row_data[c]))
            row_data["computed_slow_vehicle_total"] = sum(row_data[c] for c in SLOW if pd.notna(row_data[c]))
            row_data["computed_vehicle_total"] = row_data["computed_fast_vehicle_total"] + row_data["computed_slow_vehicle_total"]
            row_data["fast_total_mismatch"] = row_data["computed_fast_vehicle_total"] != row_data["reported_total_fast_vehicles"]
            row_data["slow_total_mismatch"] = row_data["computed_slow_vehicle_total"] != row_data["reported_total_slow_vehicles"]
            row_data["grand_total_mismatch"] = row_data["computed_vehicle_total"] != row_data["reported_grand_total_vehicles"]
            records.append(row_data)
    wb.close()

    df = pd.DataFrame(records).sort_values(["source_sheet", "interval_start", "source_excel_row"], na_position="last")
    df.to_csv(processed / "d1_movement_15min.csv", index=False)
    df.to_json(processed / "d1_movement_15min.jsonl", orient="records", lines=True, date_format="iso")
    pd.DataFrame(audits).to_csv(reports / "workbook_sheet_audit.csv", index=False)
    ordered = df.dropna(subset=["interval_start"]).sort_values(["interval_start", "source_sheet"])
    unique_times = ordered["interval_start"].drop_duplicates().sort_values().reset_index(drop=True)
    cutoff_index = int(len(unique_times) * (1 - args.test_fraction))
    cutoff = unique_times.iloc[cutoff_index] if cutoff_index < len(unique_times) else pd.NaT
    train, test = ordered[ordered["interval_start"] < cutoff], ordered[ordered["interval_start"] >= cutoff]
    train.to_csv(processed / "train_chronological.csv", index=False)
    test.to_csv(processed / "test_chronological.csv", index=False)
    report = {
        "source_file": workbook_path.name, "source_sha256": digest,
        "observation_date_from_summary": str(observation_date.date()) if pd.notna(observation_date) else None,
        "workbook_sheets": len(audits), "movement_sheets_included": sorted(df.source_sheet.unique().tolist()),
        "record_count": len(df), "unique_intervals": int(df.raw_interval.nunique()),
        "duplicate_sheet_interval_keys": int(df.duplicated(["source_sheet", "raw_interval"]).sum()),
        "missing_interval_start": int(df.interval_start.isna().sum()),
        "reported_fast_total_mismatches": int(df.fast_total_mismatch.sum()),
        "reported_slow_total_mismatches": int(df.slow_total_mismatch.sum()),
        "reported_grand_total_mismatches": int(df.grand_total_mismatch.sum()),
        "skipped_non_interval_rows": skipped_non_interval_rows,
        "train_rows": len(train), "test_rows": len(test),
        "chronological_split_cutoff": cutoff.isoformat() if pd.notna(cutoff) else None,
        "test_fraction_requested": args.test_fraction,
        "limitations": ["D1 workbook only", "No ground-truth congestion labels", "No image/video observations"],
    }
    (reports / "data_quality_report.json").write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(json.dumps({k: report[k] for k in ("workbook_sheets", "record_count", "unique_intervals", "train_rows", "test_rows", "chronological_split_cutoff")}, indent=2))


if __name__ == "__main__":
    main()
