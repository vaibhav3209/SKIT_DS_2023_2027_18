"""Configuration for the Raspberry Pi traffic-light controller."""

from typing import Final


# BCM GPIO numbers for each junction's red, yellow, and green outputs.
GPIO_MAPPING: Final[dict[str, dict[str, int]]] = {
    "Nindar": {
        "RED": 4,
        "YELLOW": 5,
        "GREEN": 6,
    },
    "Delhi": {
        "RED": 17,
        "YELLOW": 18,
        "GREEN": 22,
    },
    "Chomu Pulia": {
        "RED": 23,
        "YELLOW": 24,
        "GREEN": 25,
    },
    "Mansarovar": {
        "RED": 12,
        "YELLOW": 13,
        "GREEN": 16,
    },
}

VALID_JUNCTIONS: Final[frozenset[str]] = frozenset(GPIO_MAPPING)
VALID_STATES: Final[frozenset[str]] = frozenset({"RED", "YELLOW", "GREEN"})

# Timing values are in seconds.
ALL_RED_SAFETY_DELAY: Final[float] = 1.0
YELLOW_DURATION: Final[float] = 3.0
