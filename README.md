# AURIX — Autonomous Urban Robotics & Intelligent eXploration

<p align="center">
  <strong>Building autonomous intelligence. Simulating decisions. Bringing robotics to life.</strong>
</p>

<p align="center">
  <em>An experimental autonomous vehicle platform starting with a 1:24 BMW M4 RC drift car.</em>
</p>

---

## Overview

**AURIX** is an experimental autonomous robotics project focused on developing a modular self-driving vehicle system by combining autonomous navigation, environmental perception, intelligent decision-making, and embedded control.

The project follows a **software-first development approach**: vehicle intelligence is developed and tested in simulation before being deployed to physical hardware.

Starting with a 1:24 BMW M4 RC drift car, AURIX aims to evolve into a modular autonomous vehicle platform capable of understanding its environment, planning movements, avoiding obstacles, and executing driving commands independently.

Rather than building a simple remote-controlled car, the goal is to engineer an autonomous system where perception, planning, and control work together.

## Core Objectives

- **Autonomous Navigation:** Develop waypoint-based navigation, path planning, and movement strategies.
- **Environmental Perception:** Process sensor data and camera input to understand the surrounding environment.
- **Obstacle Avoidance:** Detect obstacles and make safe driving decisions dynamically.
- **Intelligent Decision-Making:** Develop a modular autonomy engine for interpreting environmental information and selecting actions.
- **Vehicle Control:** Implement steering, throttle, braking, and motion control.
- **Simulation:** Build a virtual testing environment to validate vehicle behavior before hardware deployment.
- **Embedded Integration:** Connect the autonomous software to physical hardware using ESP32 and compatible motor-control electronics.

## System Architecture

AURIX is designed around independent modules that communicate through well-defined interfaces.

```text
             AUTONOMOUS VEHICLE SYSTEM
                       |
              +--------v--------+
              |   Perception    |
              | Sensors / Vision|
              +--------+--------+
                       |
              +--------v--------+
              |  Decision Engine|
              |  Autonomy Logic |
              +--------+--------+
                       |
              +--------v--------+
              | Navigation &    |
              | Path Planning   |
              +--------+--------+
                       |
              +--------v--------+
              | Vehicle Control |
              | Steering/Throttle|
              +--------+--------+
                       |
              +--------v--------+
              | Vehicle Interface|
              +--------+--------+
                       |
             +---------+---------+
             |                   |
       +-----v------+      +-----v------+
       | Simulation |      |  Physical  |
       |   Engine   |      |  Hardware  |
       +------------+      +------------+
```

The simulation and physical hardware implementations will share the same vehicle-control interface, allowing the autonomy system to transition between simulated and real-world environments.

## Technology Stack

| Technology | Purpose |
|---|---|
| Python | Core application and autonomy logic |
| FastAPI | Vehicle control API and backend services |
| Pydantic | Data validation and structured communication |
| NumPy | Numerical computations and sensor processing |
| OpenCV | Computer vision and image processing |
| WebSockets | Real-time telemetry communication |
| Pytest | Automated testing |
| ESP32 | Embedded vehicle control |
| C++ | Microcontroller firmware |

## Project Structure

```text
aurix-autonomous-vehicle/
│
├── app/
│   ├── api/
│   │   ├── routes/
│   │   └── websocket.py
│   │
│   ├── autonomy/
│   │   ├── decision_engine.py
│   │   ├── obstacle_avoidance.py
│   │   └── path_planning.py
│   │
│   ├── perception/
│   │   ├── sensors.py
│   │   └── vision.py
│   │
│   ├── vehicle/
│   │   ├── controller.py
│   │   ├── simulator.py
│   │   └── hardware_interface.py
│   │
│   ├── schemas/
│   ├── core/
│   └── main.py
│
├── simulation/
├── firmware/
│   └── esp32/
│
├── tests/
├── docs/
├── scripts/
│
├── requirements.txt
├── pyproject.toml
├── README.md
└── LICENSE
```

*The repository structure represents the intended architecture and will evolve as development progresses.*

## Development Roadmap

AURIX is being developed incrementally, with each phase building upon the previous one.

- [ ] **Phase 1 — Software Foundation**
  - FastAPI application and API architecture.
  - Vehicle control interfaces.
  - Pydantic schemas and configuration.
  - Initial automated tests.

- [ ] **Phase 2 — Vehicle Simulation**
  - Simulated vehicle dynamics.
  - Steering and throttle behavior.
  - Position and velocity tracking.
  - Virtual sensor readings.

- [ ] **Phase 3 — Autonomous Navigation**
  - Waypoint navigation.
  - Path planning.
  - Obstacle detection and avoidance.
  - Autonomous decision-making.

- [ ] **Phase 4 — Computer Vision**
  - Camera integration.
  - Image processing with OpenCV.
  - Track and object detection.
  - Visual navigation.

- [ ] **Phase 5 — Embedded Hardware Integration**
  - ESP32 firmware.
  - Motor-driver integration.
  - Steering and throttle control.
  - Sensor integration and telemetry.

- [ ] **Phase 6 — Real-World Autonomous Testing**
  - Physical vehicle deployment.
  - Simulation-to-reality validation.
  - Control-system tuning.
  - Autonomous indoor track testing.

## Development Philosophy

AURIX follows three fundamental principles:

**1. Software Before Hardware**

Develop and validate the autonomous driving logic before investing in the complete hardware setup.

**2. Modular Engineering**

Keep perception, navigation, decision-making, and vehicle control independent so individual components can be improved without redesigning the entire system.

**3. Simulation Before Deployment**

Test vehicle behavior in controlled virtual environments before allowing the physical vehicle to execute autonomous commands.

## Current Development Status

**Project stage:** Initial software architecture and simulation development.

The project is currently focused on establishing the Python backend, vehicle-control interfaces, and simulation foundation. Physical hardware integration and autonomous navigation will follow in subsequent development phases.

## Hardware Platform

The initial physical platform is a **1:24 BMW M4 Style RC Drift Car**.

Planned hardware components include:

- ESP32 microcontroller.
- Existing RC drive motor and steering mechanism, subject to compatibility.
- Distance and proximity sensors.
- Camera module for visual perception.
- Suitable motor drivers and power regulation.

Hardware specifications and component selection will be finalized after evaluating the original vehicle electronics.

## Future Vision

The long-term goal of AURIX is to develop an autonomous vehicle capable of:

- Understanding its surrounding environment.
- Navigating predefined and dynamically selected routes.
- Detecting and responding to obstacles.
- Making independent movement decisions.
- Executing controlled driving actions.
- Operating through a modular software and embedded hardware architecture.

AURIX is an evolving robotics engineering project, and its capabilities will expand as development and experimentation progress.

---

## Author

**Arjun Bhattarai**

AI & Backend Systems Enthusiast | Robotics & Autonomous Systems

- GitHub: [@Arjun-Bhattarai](https://github.com/Arjun-Bhattarai)
- Portfolio: [arjunbhattarai8.com.np](https://arjunbhattarai8.com.np)

---

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

<p align="center">
  <strong>AURIX</strong><br>
  <em>From remote control to autonomous intelligence.</em>
</p>
