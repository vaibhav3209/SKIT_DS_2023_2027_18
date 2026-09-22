"""Parse and validate commands for the traffic-light controller."""

import json
from collections.abc import Mapping
from dataclasses import dataclass
from typing import Any

from config import VALID_JUNCTIONS, VALID_STATES


@dataclass(frozen=True)
class TrafficCommand:
    """A validated traffic-light command."""

    junction: str
    state: str
    duration: float


def parse_command(json_command: str | bytes | bytearray | Mapping[str, Any]) -> TrafficCommand:
    """Parse JSON or a mapping and return a validated traffic command."""
    try:
        command: Any
        if isinstance(json_command, (str, bytes, bytearray)):
            command = json.loads(json_command)
        elif isinstance(json_command, Mapping):
            command = json_command
        else:
            raise ValueError("command must be a JSON string or object")

        if not isinstance(command, Mapping):
            raise ValueError("JSON command must be an object")

        missing_fields = {"junction", "state", "duration"} - command.keys()
        if missing_fields:
            missing = ", ".join(sorted(missing_fields))
            raise ValueError(f"missing required field(s): {missing}")

        junction = command["junction"]
        state = command["state"]
        duration = command["duration"]

        if not isinstance(junction, str) or junction not in VALID_JUNCTIONS:
            raise ValueError(f"unknown junction: {junction!r}")

        if not isinstance(state, str) or state not in VALID_STATES:
            raise ValueError(f"invalid state: {state!r}")

        if isinstance(duration, bool) or not isinstance(duration, (int, float)):
            raise ValueError("duration must be a number")
        if duration <= 0:
            raise ValueError("duration must be greater than zero")

        return TrafficCommand(junction, state, float(duration))
    except json.JSONDecodeError as error:
        raise ValueError(f"invalid JSON: {error.msg}") from error
