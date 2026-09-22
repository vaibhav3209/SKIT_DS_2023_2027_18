"""Entry point for the Raspberry Pi traffic-light controller."""

from config import GPIO_MAPPING
from gpio_driver import GPIODriver
from json_parser import parse_command
from signal_controller import SignalController


TEST_JSON_COMMAND = '{"junction":"Nindar","state":"GREEN","duration":1}'


def main() -> None:
    gpio_driver: GPIODriver | None = None
    controller: SignalController | None = None

    try:
        gpio_driver = GPIODriver(GPIO_MAPPING)
        controller = SignalController(gpio_driver)

        try:
            command = parse_command(TEST_JSON_COMMAND)
        except ValueError as error:
            print(f"Command rejected: {error}")
            return

        print(
            f"Applying {command.state} at {command.junction} "
            f"for {command.duration:g} seconds"
        )
        controller.apply_command(command)
        print("Command completed")
    except KeyboardInterrupt:
        print("Interrupted; shutting down safely")
    finally:
        if controller is not None:
            controller.all_signals_off()
        if gpio_driver is not None:
            gpio_driver.close()


if __name__ == "__main__":
    main()
