<div align="center">


# 🏎️ AURIX
### **A**utonomous **U**rban **R**obotics & **I**ntelligent e**X**ploration

<p>
  <strong>Building autonomous intelligence. Simulating decisions. Bringing robotics to life.</strong>
</p>

<p>
  <em>An experimental autonomous vehicle platform starting with a 1:24 BMW M4 RC drift car.</em>
</p>

<!-- Status & Tech Badges -->
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
> **Software-First Philosophy:** Rather than starting with hardware trial-and-error, AURIX validates vehicle intelligence inside a virtual simulation environment before deploying a single command to physical motors.

Starting with a **1:24 BMW M4 RC drift car**, AURIX is designed to evolve into a scalable autonomous platform capable of understanding its surroundings, planning trajectories, avoiding obstacles, and executing real-time driving commands independently.

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
      <p>Detect static and dynamic obstacles in real time and compute safe, collision-free maneuvers.</p>
    </td>
    <td width="50%" valign="top">
      <h3>🧠 Intelligent Decision-Making</h3>
      <p>Build a modular autonomy engine to interpret telemetry and select optimal driving states.</p>
    </td>
  </tr>
  <tr>
    <td width="50%" valign="top">
      <h3>🎮 Vehicle Control</h3>
      <p>Implement precision steering, throttle, braking, and closed-loop motion control.</p>
    </td>
    <td width="50%" valign="top">
      <h3>🖥️ Simulation & Embedded</h3>
      <p>Validate behavior in a virtual physics sandbox before deploying via ESP32 and motor-control electronics.</p>
    </td>
  </tr>
</table>

---

## 🏗️ System Architecture

AURIX is built around decoupled modules that communicate through strict, well-defined interfaces. Both the **Simulation Engine** and **Physical Hardware** share the exact same control interface, enabling seamless *Sim-to-Real* transitions.

```text
                    ┌───────────────────────────────────┐
                    │     AUTONOMOUS VEHICLE SYSTEM     │
                    └─────────────────┬─────────────────┘
                                      │
                                      ▼
                    ┌───────────────────────────────────┐
                    │         Perception Layer          │
                    │     Sensors & Computer Vision     │
                    └─────────────────┬─────────────────┘
                                      │
                                      ▼
                    ┌───────────────────────────────────┐
                    │          Decision Engine          │
                    │    State Machine & Autonomy Logic │
                    └─────────────────┬─────────────────┘
                                      │
                                      ▼
                    ┌───────────────────────────────────┐
                    │    Navigation & Path Planning     │
                    │   Waypoints & Obstacle Avoidance  │
                    └─────────────────┬─────────────────┘
                                      │
                                      ▼
                    ┌───────────────────────────────────┐
                    │          Vehicle Control          │
                    │     Steering, Throttle & Braking  │
                    └─────────────────┬─────────────────┘
                                      │
                                      ▼
                    ┌───────────────────────────────────┐
                    │     Unified Vehicle Interface     │
                    └─────────────────┬─────────────────┘
                                      │
                        ┌─────────────┴─────────────┐
                        ▼                           ▼
          ┌───────────────────────────┐ ┌───────────────────────────┐
          │     Simulation Engine     │ │     Physical Hardware     │
          │  (Virtual Test Sandbox)   │ │  (1:24 BMW M4 + ESP32)    │
          └───────────────────────────┘ └───────────────────────────┘
```

---

## 🛠️ Technology Stack

| Layer | Technology | Purpose |
| :--- | :--- | :--- |
| **Core & Autonomy** | ![Python](https://img.shields.io/badge/-Python-3776AB?style=flat-square&logo=python&logoColor=white) | Core application logic, state machines, and autonomy algorithms |
| **Backend & API** | ![FastAPI](https://img.shields.io/badge/-FastAPI-009688?style=flat-square&logo=fastapi&logoColor=white) | High-performance vehicle control API and backend services |
| **Data Validation** | ![Pydantic](https://img.shields.io/badge/-Pydantic-E92063?style=flat-square&logo=pydantic&logoColor=white) | Strict schema enforcement and structured inter-module telemetry |
| **Math & Telemetry** | ![NumPy](https://img.shields.io/badge/-NumPy-013243?style=flat-square&logo=numpy&logoColor=white) | Vectorized kinematics, numerical computations, and sensor filtering |
| **Computer Vision** | ![OpenCV](https://img.shields.io/badge/-OpenCV-5C3EE8?style=flat-square&logo=opencv&logoColor=white) | Real-time image processing, lane tracking, and object detection |
| **Real-Time Comms** | ![WebSockets](https://img.shields.io/badge/-WebSockets-010101?style=flat-square&logo=socket.io&logoColor=white) | Low-latency bidirectional telemetry and remote command streaming |
| **Testing** | ![Pytest](https://img.shields.io/badge/-Pytest-0A9EDC?style=flat-square&logo=pytest&logoColor=white) | Automated unit and integration testing for autonomy modules |
| **Embedded & Firmware** | ![ESP32](https://img.shields.io/badge/-ESP32_%2F_C++-E7352C?style=flat-square&logo=espressif&logoColor=white) | Microcontroller firmware, PWM actuation, and hardware interfacing |

---

## 📂 Project Structure

```text
aurix-autonomous-vehicle/
│
├── 📁 app/
│   ├── 📁 api/                 # REST endpoints & real-time telemetry streams
│   │   ├── 📁 routes/
│   │   └── 📄 websocket.py
│   │
│   ├── 📁 autonomy/            # Core intelligence & navigation algorithms
│   │   ├── 📄 decision_engine.py
│   │   ├── 📄 obstacle_avoidance.py
│   │   └── 📄 path_planning.py
│   │
│   ├── 📁 perception/          # Sensor fusion & computer vision pipelines
│   │   ├── 📄 sensors.py
│   │   └── 📄 vision.py
│   │
│   ├── 📁 vehicle/             # Unified vehicle abstraction & drivers
│   │   ├── 📄 controller.py
│   │   ├── 📄 simulator.py
│   │   └── 📄 hardware_interface.py
│   │
│   ├── 📁 schemas/             # Pydantic data models
│   ├── 📁 core/                # App configuration & logging
│   └── 📄 main.py              # FastAPI entry point
│
├── 📁 simulation/              # Virtual environment & physics models
├── 📁 firmware/
│   └── 📁 esp32/               # C++ microcontroller source code
│
├── 📁 tests/                   # Automated test suite
├── 📁 docs/                    # Architecture diagrams & technical notes
├── 📁 scripts/                 # Utility & calibration scripts
│
├── 📄 requirements.txt
├── 📄 pyproject.toml
├── 📄 README.md
└── 📄 LICENSE
```

> *Note: The repository structure reflects the intended modular architecture and will evolve as development progresses.*

---

## 🗺️ Development Roadmap

AURIX is developed incrementally, with each phase validating core capabilities before moving up the stack.

| Phase | Milestone | Key Deliverables | Status |
| :---: | :--- | :--- | :---: |
| **01** | **Software Foundation** | FastAPI backend, unified vehicle interfaces, Pydantic schemas, initial Pytest suite | 🟡 *In Progress* |
| **02** | **Vehicle Simulation** | 2D vehicle dynamics, steering/throttle physics, odometry tracking, virtual sensors | ⚪ *Planned* |
| **03** | **Autonomous Navigation** | Waypoint following, path planning, dynamic obstacle avoidance, decision engine | ⚪ *Planned* |
| **04** | **Computer Vision** | Camera feed ingestion, OpenCV processing pipelines, track & object detection | ⚪ *Planned* |
| **05** | **Embedded Integration** | ESP32 C++ firmware, motor-driver PWM control, hardware sensor telemetry | ⚪ *Planned* |
| **06** | **Real-World Testing** | Hardware deployment, Sim-to-Real calibration, PID tuning, indoor track runs | ⚪ *Planned* |

<details>
<summary><b>📋 Click to expand detailed phase checklists</b></summary>
<br>

- **Phase 1 — Software Foundation**
  - [ ] FastAPI application and API architecture
  - [ ] Abstract vehicle control interfaces
  - [ ] Pydantic schemas and environment configuration
  - [ ] Initial automated unit tests

- **Phase 2 — Vehicle Simulation**
  - [ ] Simulated vehicle kinematics & dynamics
  - [ ] Steering and throttle response curves
  - [ ] Position, heading, and velocity tracking
  - [ ] Virtual proximity & distance sensor readings

- **Phase 3 — Autonomous Navigation**
  - [ ] Waypoint navigation controller
  - [ ] Local & global path planning
  - [ ] Obstacle detection and avoidance logic
  - [ ] State-machine autonomous decision-making

- **Phase 4 — Computer Vision**
  - [ ] Camera streaming integration
  - [ ] Image preprocessing with OpenCV
  - [ ] Track boundary and obstacle detection
  - [ ] Vision-assisted navigation

- **Phase 5 — Embedded Hardware Integration**
  - [ ] ESP32 firmware architecture
  - [ ] Motor-driver (H-Bridge/ESC) integration
  - [ ] Servo steering and throttle actuation
  - [ ] Real-time sensor integration and telemetry uplink

- **Phase 6 — Real-World Autonomous Testing**
  - [ ] Full physical vehicle assembly & deployment
  - [ ] Simulation-to-reality behavioral validation
  - [ ] Control-system and PID tuning
  - [ ] Autonomous indoor track testing

</details>

---

## 💡 Engineering Philosophy

1. **💻 Software Before Hardware** — Develop, benchmark, and debug the autonomous driving stack in software before committing to physical hardware constraints.
2. **🧩 Modular Engineering** — Keep perception, planning, decision-making, and actuation strictly decoupled so individual subsystems can be upgraded independently.
3. **🧪 Simulation Before Deployment** — Validate edge cases and obstacle avoidance behavior in controlled virtual environments before executing commands on physical motors.

---

## 🏎️ Hardware Platform

The initial physical testbed is a **1:24 Scale BMW M4 Style RC Drift Car**, chosen for its compact footprint and agile steering geometry—ideal for indoor autonomous navigation experiments.

### Planned Bill of Materials (BOM)
* **Compute & Comms:** ESP32 Microcontroller (Wi-Fi / Serial telemetry & PWM control)
* **Actuation:** Stock RC drive motor & steering servo/mechanism *(subject to electrical characterization)*
* **Perception:** Ultrasonic / Time-of-Flight (ToF) distance sensors + lightweight camera module
* **Power & Drive:** Dual H-Bridge motor driver & regulated LiPo battery distribution

> [!IMPORTANT]
> **Current Status:** AURIX is currently in **Phase 1 & 2** (establishing the Python backend, control interfaces, and simulation foundation). Final hardware component selection will be locked in once initial chassis electronics characterization is complete.

---

## 👨‍💻 Author

**Arjun Bhattarai**  
*AI & Backend Systems Enthusiast | Robotics & Autonomous Systems*

[![GitHub](https://img.shields.io/badge/GitHub-@Arjun--Bhattarai-181717?style=for-the-badge&logo=github)](https://github.com/Arjun-Bhattarai)
[![Portfolio](https://img.shields.io/badge/Portfolio-arjunbhattarai8.com.np-0A66C2?style=for-the-badge&logo=google-chrome&logoColor=white)](https://arjunbhattarai8.com.np)

---

<div align="center">
  <strong>AURIX</strong><br>
  <em>From remote control to autonomous intelligence.</em>
</div>
