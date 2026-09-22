import unittest

from config import GPIO_MAPPING
from json_parser import TrafficCommand, parse_command
from signal_controller import SignalController


class FakeDriver:
    def __init__(self) -> None:
        self.states: dict[tuple[str, str], bool] = {}
        self.history: list[tuple[str, str, bool]] = []

    def set_light(self, junction: str, signal: str, is_on: bool) -> None:
        self.states[(junction, signal)] = is_on
        self.history.append((junction, signal, is_on))

    def all_lights_off(self) -> None:
        for key in self.states:
            self.states[key] = False

    def green_junctions(self) -> list[str]:
        return [
            junction
            for junction in GPIO_MAPPING
            if self.states.get((junction, "GREEN"), False)
        ]


class TrafficControllerTests(unittest.TestCase):
    def test_parser_accepts_json_string(self) -> None:
        command = parse_command(
            '{"junction":"Mansarovar","state":"GREEN","duration":35}'
        )
        self.assertEqual(command, TrafficCommand("Mansarovar", "GREEN", 35.0))

    def test_parser_rejects_invalid_commands(self) -> None:
        invalid_commands = (
            "not-json",
            {"junction": "Unknown", "state": "GREEN", "duration": 10},
            {"junction": "Delhi", "state": "BLUE", "duration": 10},
            {"junction": "Delhi", "state": "GREEN", "duration": -5},
            {"junction": "Delhi", "state": "GREEN"},
        )

        for invalid_command in invalid_commands:
            with self.subTest(invalid_command=invalid_command):
                with self.assertRaises(ValueError):
                    parse_command(invalid_command)

    def test_startup_sets_all_junctions_red(self) -> None:
        driver = FakeDriver()
        SignalController(driver, sleep_function=lambda _: None)

        self.assertEqual(driver.green_junctions(), [])
        for junction in GPIO_MAPPING:
            self.assertTrue(driver.states[(junction, "RED")])

    def test_green_command_follows_timed_transition(self) -> None:
        driver = FakeDriver()
        sleeps: list[float] = []
        controller = SignalController(driver, sleep_function=sleeps.append)

        controller.apply_command(TrafficCommand("Nindar", "GREEN", 10))

        self.assertEqual(sleeps, [1.0, 10.0, 3.0])
        self.assertEqual(driver.green_junctions(), [])
        self.assertTrue(driver.states[("Nindar", "RED")])

    def test_new_green_inserts_all_red_safety_delay(self) -> None:
        driver = FakeDriver()
        sleeps: list[float] = []
        controller = SignalController(driver, sleep_function=sleeps.append)

        controller.set_green("Nindar")
        controller.set_green("Delhi")

        self.assertEqual(sleeps, [1.0, 1.0])
        self.assertEqual(driver.green_junctions(), ["Delhi"])

    def test_invalid_command_does_not_change_signal_state(self) -> None:
        driver = FakeDriver()
        controller = SignalController(driver, sleep_function=lambda _: None)
        before = dict(driver.states)

        with self.assertRaises(ValueError):
            parse_command('{"junction":"Unknown","state":"GREEN","duration":10}')

        self.assertEqual(driver.states, before)


if __name__ == "__main__":
    unittest.main()
