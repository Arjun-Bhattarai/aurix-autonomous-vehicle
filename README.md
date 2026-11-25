# 🏎️ AURIX
### **A**utonomous **U**rban **R**obotics & **I**ntelligent e**X**ploration

<div align="center">

<p>
  <strong>Building autonomous intelligence. Simulating decisions. Bringing robotics to life.</strong>
</p>

<p>
  <em>An experimental autonomous vehicle platform starting with a 1:24 BMW M4 RC drift car.</em>
</p>

<p>
  <img src="https://img.shields.io/badge/Status-In_Development-blue?style=for-the-badge" alt="Status" />
  <img src="https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python" />
  <img src="https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white" alt="FastAPI" />
  <img src="https://img.shields.io/badge/OpenCV-5C3EE8?style=for-the-badge&logo=opencv&logoColor=white" alt="OpenCV" />
  <img src="https://img.shields.io/badge/ESP32-E7352C?style=for-the-badge&logo=espressif&logoColor=white" alt="ESP32" />
  <img src="https://img.shields.io/badge/C++-00599C?style=for-the-badge&logo=cplusplus&logoColor=white" alt="C++" />
</p>

<p>
  <a href="#-overview">Overview</a> •
  <a href="#-system-architecture">Architecture</a> •
  <a href="#-technology-stack">Tech Stack</a> •
  <a href="#-project-structure">Structure</a> •
  <a href="#-development-roadmap">Roadmap</a> •
  <a href="#-hardware-platform">Hardware</a>
</p>

</div>

---

## 📖 Overview

**AURIX** is an experimental autonomous robotics project focused on engineering a modular self-driving vehicle system by combining environmental perception, intelligent decision-making, autonomous navigation, and embedded control.

> [!NOTE]
> **Software-First Philosophy:** Rather than starting with hardware trial-and-error, AURIX validates vehicle intelligence inside a virtual simulation environment before deploying commands to physical motors.

Starting with a **1:24 BMW M4 RC drift car**, AURIX is designed to evolve into a scalable autonomous platform capable of understanding its surroundings, planning trajectories, avoiding obstacles, and executing driving commands independently.

## 🚧 Current Development Status

AURIX is currently focused on establishing a reliable software foundation and developing its vehicle simulation before moving to physical hardware.

### Implemented foundations

- Abstract vehicle interface for consistent vehicle control.
- Simulated vehicle supporting forward and reverse movement.
- Time-based acceleration, braking, and coasting.
- Steering-based heading dynamics using a kinematic bicycle model.
- Communication timeout watchdog.
- Emergency-stop behavior.
- Pydantic command and telemetry validation.
- Automated test suite with **49 passing tests**.

### Current development focus

- Improving vehicle simulation accuracy.
- Expanding vehicle motion and telemetry capabilities.
- Strengthening simulator reliability through automated testing.
- Preparing the foundation for autonomous navigation.

Computer vision, advanced autonomous obstacle avoidance, and physical hardware integration remain future development goals.

---

## 🎯 Core Objectives

<table>
  <tr>
    <td width="50%" valign="top">
      <h3>🧭 Autonomous Navigation</h3>
      <p>Develop waypoint-based navigation, path planning algorithms, and dynamic movement strategies.</p>
    </td>
    <td width="50%" valign="top">
      <h3>👁️ Environmental Perception</h3>
      <p>Process proximity sensor data and live camera feeds to map and understand the surrounding environment.</p>
    </td>
  </tr>
  <tr>
    <td width="50%" valign="top">
      <h3>🛡️ Obstacle Avoidance</h3>
      <p>Detect static and dynamic obstacles and compute safe, collision-aware maneuvers.</p>
    </td>
    <td width="50%" valign="top">
      <h3>🧠 Intelligent Decision-Making</h3>
      <p>Build a modular autonomy engine to interpret telemetry and select appropriate driving states.</p>
    </td>
  </tr>
  <tr>
    <td width="50%" valign="top">
      <h3>🎮 Vehicle Control</h3>
      <p>Implement precision steering, throttle, braking, and closed-loop motion control.</p>
    </td>
    <td width="50%" valign="top">
      <h3>🖥️ Simulation & Embedded Systems</h3>
      <p>Validate vehicle behavior in a virtual environment before deploying through ESP32 and motor-control electronics.</p>
    </td>
  </tr>
</table>

---

## 🏗️ System Architecture

AURIX is organized around modular components with clearly defined responsibilities and interfaces.

The simulation and future physical vehicle implementations are designed to share a unified vehicle interface, supporting a gradual transition from simulation to real-world operation.

```text
                    ┌───────────────────────────────────┐
                    │     AUTONOMOUS VEHICLE SYSTEM      │
                    └─────────────────┬─────────────────┘
                                      │
                                      ▼
                    ┌───────────────────────────────────┐
                    │          Perception Layer          │
                    │     Sensors & Computer Vision      │
                    └─────────────────┬─────────────────┘
                                      │
                                      ▼
                    ┌───────────────────────────────────┐
                    │          Decision Engine           │
                    │    State Machine & Autonomy Logic  │
                    └─────────────────┬─────────────────┘
                                      │
                                      ▼
                    ┌───────────────────────────────────┐
                    │      Navigation & Path Planning    │
                    │    Waypoints & Obstacle Avoidance  │
                    └─────────────────┬─────────────────┘
                                      │
                                      ▼
                    ┌───────────────────────────────────┐
                    │          Vehicle Control           │
                    │     Steering, Throttle & Braking   │
                    └─────────────────┬─────────────────┘
                                      │
                                      ▼
                    ┌───────────────────────────────────┐
                    │      Unified Vehicle Interface     │
                    └─────────────────┬─────────────────┘
                                      │
                        ┌─────────────┴─────────────┐
                        ▼                           ▼
          ┌───────────────────────────┐ ┌───────────────────────────┐
          │     Simulation Engine     │ │     Physical Hardware     │
          │   (Virtual Test Sandbox)  │ │  (1:24 BMW M4 + ESP32)    │
          └───────────────────────────┘ └───────────────────────────┘
```

*Note: This diagram represents the intended overall architecture. Not every layer is fully implemented yet.*

---

## 🛠️ Technology Stack

| Layer | Technology | Purpose |
| :--- | :--- | :--- |
| **Core & Autonomy** | ![Python](https://img.shields.io/badge/-Python-3776AB?style=flat-square&logo=python&logoColor=white) | Core application logic, state machines, and autonomy algorithms |
| **Backend & API** | ![FastAPI](https://img.shields.io/badge/-FastAPI-009688?style=flat-square&logo=fastapi&logoColor=white) | Vehicle control API and backend application |
| **Data Validation** | ![Pydantic](https://img.shields.io/badge/-Pydantic-E92063?style=flat-square&logo=pydantic&logoColor=white) | Schema enforcement and structured telemetry |
| **Math & Telemetry** | ![NumPy](https://img.shields.io/badge/-NumPy-013243?style=flat-square&logo=numpy&logoColor=white) | Planned numerical computations and sensor processing |
| **Computer Vision** | ![OpenCV](https://img.shields.io/badge/-OpenCV-5C3EE8?style=flat-square&logo=opencv&logoColor=white) | Planned image processing, lane tracking, and object detection |
| **Real-Time Communication** | ![WebSockets](https://img.shields.io/badge/-WebSockets-010101?style=flat-square&logo=socket.io&logoColor=white) | Planned bidirectional telemetry and remote command streaming |
| **Testing** | ![Pytest](https://img.shields.io/badge/-Pytest-0A9EDC?style=flat-square&logo=pytest&logoColor=white) | Automated unit and integration testing |
| **Embedded & Firmware** | ![ESP32](https://img.shields.io/badge/-ESP32%20%2F%20C++-E7352C?style=flat-square&logo=espressif&logoColor=white) | Planned microcontroller firmware and hardware interfacing |

---

## 📂 Project Structure

```text
aurix-autonomous-vehicle/
│
├── app/
│   ├── api/                    # FastAPI routing and endpoints
│   │   ├── routes/
│   │   │   ├── autonomy.py
│   │   │   ├── telemetry.py
│   │   │   └── vehicle.py
│   │   └── router.py
│   │
│   ├── autonomy/               # Autonomous decision-making
│   │   ├── decision_engine.py
│   │   └── obstacle_avoidance.py
│   │
│   ├── control/                # Vehicle control logic
│   │   └── controller.py
│   │
│   ├── core/                   # Configuration and safety
│   │   ├── config.py
│   │   └── safety.py
│   │
│   ├── navigation/             # Path planning and waypoints
│   │   ├── path_planner.py
│   │   └── waypoint.py
│   │
│   ├── perception/             # Sensor and vision modules
│   │   ├── sensors.py
│   │   └── vision.py
│   │
│   ├── schemas/                # Pydantic data models
│   │   ├── commands.py
│   │   └── telemetry.py
│   │
│   ├── vehicle/                # Vehicle abstraction and implementations
│   │   ├── interface.py
│   │   ├── simulator.py
│   │   └── hardware.py
│   │
│   └── main.py                 # FastAPI application entry point
│
├── scripts/
│   ├── test_commands.py
│   ├── test_config.py
│   ├── test_interface.py
│   ├── test_simulator.py
│   ├── test_telemetry.py
│   └── README.md
│
├── requirements.txt
├── pyproject.toml
├── README.md
└── LICENSE
```

*Note: The repository structure reflects the current codebase. Module capabilities will expand as development progresses.*

---

## 🗺️ Development Roadmap

AURIX is developed incrementally, with each phase validating core capabilities before moving to the next stage.

| Phase | Milestone | Key Deliverables | Status |
| :---: | :--- | :--- | :---: |
| **01** | **Software Foundation** | FastAPI backend, unified vehicle interfaces, Pydantic schemas, configuration, and initial automated tests | 🟢 Foundation Established |
| **02** | **Vehicle Simulation** | Vehicle dynamics, steering/throttle physics, heading and velocity tracking, virtual sensors | 🟡 In Progress |
| **03** | **Autonomous Navigation** | Waypoint following, path planning, obstacle avoidance, and decision engine | ⚪ Planned |
| **04** | **Computer Vision** | Camera feed ingestion, OpenCV processing pipelines, track and object detection | ⚪ Planned |
| **05** | **Embedded Integration** | ESP32 firmware, motor-driver PWM control, and hardware sensor telemetry | ⚪ Planned |
| **06** | **Real-World Testing** | Hardware deployment, Sim-to-Real calibration, PID tuning, and indoor track testing | ⚪ Planned |

<details>
<summary><strong>📋 Click to expand detailed phase checklists</strong></summary>

### Phase 1 — Software Foundation

- [x] FastAPI application foundation
- [x] Abstract vehicle control interface
- [x] Pydantic command and telemetry schemas
- [x] Application configuration foundation
- [x] Initial automated unit tests

### Phase 2 — Vehicle Simulation

- [x] Forward and reverse vehicle movement
- [x] Time-based acceleration and braking
- [x] Coasting behavior
- [x] Steering-based heading calculations
- [x] Initial heading and steering tests
- [ ] Refine simulated vehicle dynamics
- [ ] Position and odometry tracking
- [ ] Virtual proximity and distance sensor readings

### Phase 3 — Autonomous Navigation

- [ ] Waypoint navigation controller
- [ ] Local and global path planning
- [ ] Obstacle detection and avoidance logic
- [ ] State-machine autonomous decision-making

### Phase 4 — Computer Vision

- [ ] Camera streaming integration
- [ ] Image preprocessing with OpenCV
- [ ] Track boundary and obstacle detection
- [ ] Vision-assisted navigation

### Phase 5 — Embedded Hardware Integration

- [ ] ESP32 firmware architecture
- [ ] Motor-driver (H-Bridge/ESC) integration
- [ ] Servo steering and throttle actuation
- [ ] Real-time sensor integration and telemetry uplink

### Phase 6 — Real-World Autonomous Testing

- [ ] Full physical vehicle assembly and deployment
- [ ] Simulation-to-reality behavioral validation
- [ ] Control-system and PID tuning
- [ ] Autonomous indoor track testing

</details>

---

## 💡 Engineering Philosophy

1. **💻 Software Before Hardware** — Develop, benchmark, and debug the autonomous driving stack in software before committing to physical hardware constraints.

2. **🧩 Modular Engineering** — Keep perception, planning, decision-making, and actuation separated so individual subsystems can evolve independently.

3. **🧪 Simulation Before Deployment** — Validate vehicle behavior and edge cases in a controlled virtual environment before executing commands on physical motors.

4. **🛡️ Safety by Design** — Build safety mechanisms such as emergency stops, communication watchdogs, and command validation into the vehicle system.

5. **📈 Incremental Development** — Build, test, and validate each subsystem before expanding the overall autonomy stack.

---

## 🏎️ Hardware Platform

The initial physical testbed is a **1:24 Scale BMW M4 Style RC Drift Car**, selected for its compact footprint and steering characteristics, making it a useful platform for indoor autonomous navigation experiments.

### Planned Bill of Materials (BOM)

- **Compute & Communication:** ESP32 microcontroller with Wi-Fi or serial communication.
- **Actuation:** Stock RC drive motor and steering servo/mechanism, subject to electrical characterization.
- **Perception:** Ultrasonic or Time-of-Flight (ToF) distance sensors and a lightweight camera module.
- **Power & Drive:** Compatible motor driver and regulated battery distribution.

> [!IMPORTANT]
> **Current Status:** AURIX is currently developing its Python backend and vehicle simulation. Physical hardware integration has not started. Final hardware component selection will be determined after the initial simulation and chassis electronics characterization.

---

## 👨‍💻 Author

**Arjun Bhattarai**  
*AI & Backend Systems Enthusiast | Robotics & Autonomous Systems*

[![GitHub](https://img.shields.io/badge/GitHub-@Arjun--Bhattarai-181717?style=for-the-badge&logo=github)](https://github.com/Arjun-Bhattarai)

[![Portfolio](https://img.shields.io/badge/Portfolio-arjunbhattarai8.com.np-0A66C2?style=for-the-badge&logo=google-chrome&logoColor=white)](https://arjunbhattarai8.com.np)

---

<div align="center">
  <strong>AURIX</strong>

  <em>From remote control to autonomous intelligence.</em>
</div>