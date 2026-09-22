"""Traffic-light state logic and green-signal safety interlock."""

import time
from collections.abc import Callable, Mapping

from config import ALL_RED_SAFETY_DELAY, GPIO_MAPPING, YELLOW_DURATION
from gpio_driver import GPIODriver
from json_parser import TrafficCommand


class SignalController:
    """Apply validated commands while maintaining a safe signal sequence."""

    def __init__(
        self,
        gpio_driver: GPIODriver,
        gpio_mapping: Mapping[str, Mapping[str, int]] = GPIO_MAPPING,
        sleep_function: Callable[[float], None] = time.sleep,
    ) -> None:
        self._gpio_driver = gpio_driver
        self._junctions = tuple(gpio_mapping)
        self._sleep = sleep_function
        self._active_green: str | None = None
        self.set_all_red()

    def _set_junction_state(self, junction: str, active_signal: str) -> None:
        for signal in ("RED", "YELLOW", "GREEN"):
            self._gpio_driver.set_light(
                junction,
                signal,
                signal == active_signal,
            )

    def set_red(self, junction: str) -> None:
        """Set one junction to red."""
        self._set_junction_state(junction, "RED")
        if self._active_green == junction:
            self._active_green = None

    def set_yellow(self, junction: str) -> None:
        """Set one junction to yellow without leaving another green active."""
        if self._active_green is not None and self._active_green != junction:
            self.set_all_red()
        self._set_junction_state(junction, "YELLOW")
        if self._active_green == junction:
            self._active_green = None

    def set_green(self, junction: str) -> None:
        """Set one junction to green after applying the safety interlock."""
        if self._active_green != junction:
            self.set_all_red()
            self._sleep(ALL_RED_SAFETY_DELAY)

        self._set_junction_state(junction, "GREEN")
        self._active_green = junction

    def set_all_red(self) -> None:
        """Set every junction to red and clear the active-green record."""
        for junction in self._junctions:
            self._set_junction_state(junction, "RED")
        self._active_green = None

    def all_signals_off(self) -> None:
        """Turn every output off, for shutdown or maintenance."""
        self._gpio_driver.all_lights_off()
        self._active_green = None

    def apply_command(self, command: TrafficCommand) -> None:
        """Apply a validated command, including timing for a green command."""
        if command.state == "RED":
            self.set_red(command.junction)
        elif command.state == "YELLOW":
            self.set_yellow(command.junction)
        else:
            self.set_green(command.junction)
            self._sleep(command.duration)
            self.set_yellow(command.junction)
            self._sleep(YELLOW_DURATION)
            self.set_red(command.junction)
