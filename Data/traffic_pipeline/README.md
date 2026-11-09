# D1 traffic preprocessing

This package creates a reproducible, movement-level, 15-minute table from the classified-count workbook already stored at `Data/test_data/TMC-14 Number (D1).xlsx`. It preserves the supplied workbook in place and writes derived files under `Data/traffic_pipeline/output/`.

## Run

From the repository root:

```powershell
python -m pip install -r Data/traffic_pipeline/requirements.txt
python Data/traffic_pipeline/preprocess.py
```

Use `--workbook` and `--output-dir` to select another input or output location. `--test-fraction` controls a chronological holdout (default 0.2). The split is by timestamp so movements from the same 15-minute interval cannot fall on opposite sides.

## Outputs

- `processed/d1_movement_15min.csv` and `.jsonl`: normalized rows with workbook and sheet provenance, approach (`origin`, `destination`), interval boundaries, vehicle-class counts, reported totals, and independently computed totals/mismatch flags.
- `processed/train_chronological.csv` and `test_chronological.csv`: time-ordered holdout partitions.
- `reports/workbook_sheet_audit.csv`: all sheet names and whether each was included as a `V_<number>` movement sheet.
- `reports/data_quality_report.json`: source SHA-256, row counts, duplicate/missing checks, total inconsistencies, and split boundary.

The observation date comes from `Summary!I1`; intervals that cross midnight advance to the following day. Direction labels come from the movement sheet's `B4` and `E4`. Count fields retain the workbook's values; derived totals are separate and never overwrite reported totals. Feature engineering is limited to transparent sums and mismatch indicators; no congestion labels or thresholds are inferred.

## Scope and limitations

This milestone processes D1 only. D2/D3 are present in the repository but have not been combined pending confirmation that they should be included. No video or image data is present in this pipeline, so image/video deduplication is out of scope. The workbook has no ground-truth congestion labels; the chronological test set is not a basis for supervised congestion accuracy claims. This pipeline does not change signal timings, thresholds, hardware specifications, or controller code.
