# Urban Traffic Congestion Control

## Raspberry Pi Traffic-Light Hardware Control Module

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
## Project Overview

### Smarter Signals. Smoother Traffic. Better Cities.

An intelligent traffic management system designed to simulate urban traffic conditions and optimize traffic signal timing based on real-time vehicle density. The project aims to reduce congestion, minimize unnecessary waiting time, and improve traffic flow through a data-driven decision algorithm.

---

## 🌟 About the Project

Traditional traffic signals often operate on fixed timers, regardless of how many vehicles are waiting at an intersection. This can lead to unnecessary delays, uneven traffic distribution, and increased congestion.

**Urban Traffic Congestion Control** aims to make traffic signal management more adaptive by analyzing traffic conditions, monitoring vehicle density, and determining more efficient signal timings.

Our goal is to develop a system that can make intelligent traffic signal decisions based on simulated or generated traffic data, with the potential to integrate real-world traffic information in future iterations.

## 👥 Meet the Team

We believe great systems are built through collaboration. Meet the people working to make urban traffic smarter.

<!-- Replace the placeholders with your actual team members and GitHub usernames. -->

<table>
  <tr>
    <td align="center" width="33%">
      <a href="https://github.com/GITHUB_USERNAME_1">
        <img src="https://github.com/GITHUB_USERNAME_1.png" width="120" height="120" alt="Team Member 1" style="border-radius:50%;" />
        <br />
        <strong>Team Member 1</strong>
      </a>
      <br />
      <sub>Project Lead / Developer</sub>
      <br />
      <a href="https://github.com/GITHUB_USERNAME_1">@GITHUB_USERNAME_1</a>
    </td>
    <td align="center" width="33%">
      <a href="https://github.com/GITHUB_USERNAME_2">
        <img src="https://github.com/GITHUB_USERNAME_2.png" width="120" height="120" alt="Team Member 2" style="border-radius:50%;" />
        <br />
        <strong>Team Member 2</strong>
      </a>
      <br />
      <sub>Dataset & Simulation</sub>
      <br />
      <a href="https://github.com/GITHUB_USERNAME_2">@GITHUB_USERNAME_2</a>
    </td>
    <td align="center" width="33%">
      <a href="https://github.com/GITHUB_USERNAME_3">
        <img src="https://github.com/GITHUB_USERNAME_3.png" width="120" height="120" alt="Team Member 3" style="border-radius:50%;" />
        <br />
        <strong>Team Member 3</strong>
      </a>
      <br />
      <sub>Algorithm & Optimization</sub>
      <br />
      <a href="https://github.com/GITHUB_USERNAME_3">@GITHUB_USERNAME_3</a>
    </td>
  </tr>
</table>

> 💡 Add or remove cards depending on the size of your team. GitHub profile pictures load automatically from the usernames in the image URLs.

---

## 🛠️ What We're Working On

We are currently focusing on two major components that form the foundation of the project.

### 1. 📊 Dataset Generation & Traffic Simulation

We are developing a simulated traffic environment to represent how vehicles arrive at and leave an intersection throughout the day.

Current focus:

* Simulating traffic conditions beginning at **8:00 AM**.
* Generating vehicle arrivals dynamically instead of relying on pre-existing CSV datasets.
* Modeling different vehicle categories, including cars, buses, and bikes.
* Tracking vehicle arrivals, departures, and waiting queues.
* Maintaining traffic density measurements for signal decision-making.
* Creating realistic traffic patterns that can later support algorithm development and evaluation.

### 2. 🧠 Intelligent Traffic Signal Decision Algorithm

We are developing a decision-making algorithm that uses traffic density and vehicle queue information to determine when a traffic signal should change.

Current focus:

* Monitoring traffic density continuously.
* Managing the green, yellow, and red signal phases.
* Evaluating traffic conditions near the end of a signal cycle.
* Determining whether a signal should switch based on congestion and queue conditions.
* Balancing waiting times across traffic lanes.
* Exploring adaptive signal timing instead of relying entirely on fixed-duration cycles.

**Our current priority:** Build a reliable traffic simulation and develop a decision algorithm that can be evaluated against conventional fixed-time signals.

---

## 🗺️ Project Roadmap

* [x] Define the project objective and core approach.
* [ ] Develop dynamic vehicle arrival simulation.
* [ ] Track vehicle density and waiting queues.
* [ ] Implement the traffic signal decision algorithm.
* [ ] Evaluate adaptive signals against fixed-time signals.
* [ ] Measure waiting time, queue length, and traffic throughput.
* [ ] Explore real-world traffic data integration.
* [ ] Develop a more complete traffic management interface.

---

## 🔮 Future Scope

Potential future improvements include:

* Integrating computer vision for vehicle detection.
* Exploring real-world traffic data from mapping or traffic information services.
* Extending the simulation to multiple connected intersections.
* Comparing rule-based control with machine-learning-based approaches.
* Developing a dashboard for monitoring traffic conditions and signal decisions.

These are planned possibilities, not claims about features already implemented.

---

## 🤝 Contributing

We welcome collaboration and ideas that can help improve urban traffic management.

1. Fork the repository.
2. Create a feature branch.
3. Make your changes and test them.
4. Submit a pull request describing your contribution.

---

## 📄 License

A license has not yet been specified. Add a `LICENSE` file when the project license is decided.

---

<p align="center">
  <strong>🚦 Building smarter traffic systems, one intersection at a time.</strong>
</p>
