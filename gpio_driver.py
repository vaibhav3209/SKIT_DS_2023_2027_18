"""GPIO hardware abstraction for the traffic-light controller."""

from collections.abc import Callable, Mapping
from typing import Any


class GPIODriver:
    """Control traffic-light outputs without exposing GPIO details elsewhere."""

    def __init__(
        self,
        gpio_mapping: Mapping[str, Mapping[str, int]],
        device_factory: Callable[[int], Any] | None = None,
    ) -> None:
        if device_factory is None:
            try:
                from gpiozero import DigitalOutputDevice
            except ImportError as error:
                raise RuntimeError(
                    "gpiozero is required to use GPIODriver on the Raspberry Pi."
                ) from error

            device_factory = DigitalOutputDevice

        self._devices: dict[tuple[str, str], Any] = {}
        for junction, signals in gpio_mapping.items():
            for signal, gpio_pin in signals.items():
                self._devices[(junction, signal)] = device_factory(
                    gpio_pin,
                    initial_value=False,
                )

    def set_light(self, junction: str, signal: str, is_on: bool) -> None:
        """Set one light output to either on or off."""
        try:
            device = self._devices[(junction, signal)]
        except KeyError as error:
            raise ValueError(f"Unknown light: {junction} {signal}") from error

        if is_on:
            device.on()
        else:
            device.off()

    def all_lights_off(self) -> None:
        """Turn every configured output off."""
        for device in self._devices.values():
            device.off()

    def close(self) -> None:
        """Turn outputs off and release GPIO resources."""
        for device in self._devices.values():
            device.off()
            device.close()
