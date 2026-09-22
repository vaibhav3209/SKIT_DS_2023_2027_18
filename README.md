# Urban Traffic Congestion Control

This project contains the Raspberry Pi traffic-light hardware control module.
It accepts an already-received JSON command, validates it, and drives the
traffic-light control outputs through `gpiozero` using BCM numbering.

## Files

- `config.py`: BCM mapping and timing constants.
- `gpio_driver.py`: `gpiozero` output initialization, switching, and cleanup.
- `json_parser.py`: JSON parsing and command validation.
- `signal_controller.py`: signal states, timing, and the all-red interlock.
- `main.py`: hardcoded test command and safe shutdown handling.
- `test_traffic_controller.py`: hardware-independent unit tests.

## Install and run on Raspberry Pi

Install the GPIO library:

```bash
python3 -m pip install gpiozero
```

Run the hardcoded Nindar test command:

```bash
python3 main.py
```

Expected output after the ten-second green and three-second yellow sequence:

```text
Applying GREEN at Nindar for 10 seconds
Command completed
```

The program initializes all approaches red. Before a new junction becomes
green, it sets all approaches red and waits one second. A green command then
uses this sequence:

```text
GREEN -> YELLOW -> RED
```

Invalid commands are rejected before the controller changes any signal state.
Pressing Ctrl+C turns outputs off and closes the GPIO resources.

## Hardware architecture

Raspberry Pi GPIO pins must not directly power high-current traffic-light
modules. GPIO pins provide control signals only:

```text
Raspberry Pi GPIO
	|
	v
Transistor / logic-level MOSFET
	|
	v
Traffic-light LED
	|
	v
External power supply
```

For an individual low-current LED, use a suitable current-limiting resistor.
The resistor value depends on the LED forward voltage, supply voltage, and
desired current. For a larger traffic-light module, determine the driver
transistor or MOSFET, resistor requirements, supply voltage, and current from
that module's actual specifications. Do not assume every module has the same
pinout.

The Raspberry Pi ground, driver-circuit ground, and external-supply ground
must share a common reference when the circuit design requires it. Follow the
driver and module datasheets, and disconnect power before changing wiring.

## Incremental hardware test plan

Do not connect all 12 outputs initially.

1. **One LED:** connect the test output on BCM GPIO 6 through the appropriate
   resistor and verify on/off behavior with `gpiozero`.
2. **One signal:** connect BCM GPIO 4 for red, GPIO 5 for yellow, and GPIO 6
   for green through the driver circuit. Verify red, yellow, and green in
   sequence.
3. **JSON:** test `{"junction":"Nindar","state":"GREEN","duration":10}`.
4. **Second approach:** add Delhi and verify that only one green output can be
   active.
5. **Third approach:** add Chomu Pulia and repeat the interlock test.
6. **Complete system:** add Mansarovar and verify all 12 outputs.

The configured test commands are:

```json
{"junction":"Nindar","state":"GREEN","duration":10}
{"junction":"Delhi","state":"GREEN","duration":10}
{"junction":"Chomu Pulia","state":"GREEN","duration":10}
{"junction":"Mansarovar","state":"GREEN","duration":10}
```

Invalid-command examples:

```json
{"junction":"Unknown","state":"GREEN","duration":10}
{"junction":"Delhi","state":"BLUE","duration":10}
{"junction":"Delhi","state":"GREEN","duration":-5}
```

Run the hardware-independent checks from the project directory:

```bash
python3 -m unittest -v
```