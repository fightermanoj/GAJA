# Team SEA-KERS Submission Hack Vortex

- Video link : 
- PPT Link :


# GAJA: AI-Powered Autonomous UAVs for Enhanced Border Security
![GAJA Project DEMO](https://drive.google.com/uc?export=view&id=1tqBEIKV9O0bEftjSX_e4UdFclymeUuAY "GAJA Project File Structure Overview")

## Table of Contents

1. [Introduction](#introduction)  
2. [Problem Statement](#problem-statement)  
3. [Proposed Solution](#proposed-solution)  
4. [Key Features](#key-features)  
5. [Core Technologies](#core-technologies)  
6. [Project Structure](#project-structure)  
7. [Development Phases](#development-phases)  
8. [Scalability & Applications](#scalability--applications)  
9. [Impact & Safety](#impact--safety)  
10. [Challenges](#challenges)  
11. [Getting Started](#getting-started)  
12. [Usage](#usage)  
13. [Contributing](#contributing)  
14. [License](#license)

## 1. Introduction

GAJA is a modular AI upgrade for UAVs focused on autonomous border surveillance and patrolling. It transforms basic drones into AI-powered sentinels with "see-through" detection, real-time 3D mapping, and intelligent, GPS-independent pathfinding.

## 2. Problem Statement

Conventional patrolling techniques expose security forces to lethal threats. Incidents such as Pahalgam, Uri, and Nagrota highlight the need for intelligent systems that reduce human involvement in hostile terrains.

## 3. Proposed Solution

GAJA enables autonomous UAV patrols by integrating:

- AI-powered modular hardware for existing drones
- A BSF dashboard for drone control and monitoring
- Real-time obstacle-aware human detection via radar
- Offline-capable pathfinding and mapping

## 4. Key Features

- **"See-Through" Human Detection** using 24GHz radar
- **Modular AI Attachment** (plug-and-play on most UAVs)
- **GPS-Independent Pathfinding** with onboard AI agents
- **Live 3D Mapping** for continuous situational awareness

## 5. Core Technologies

### Software
- Depth Estimation: Depth Anything V2
- Scene Understanding: Qwen Omni 2.5
- Object Detection: RF-DTR
- 3D Reconstruction: Neuralangelo
- Languages: Python, JavaScript, C++
- Frameworks: FastAPI, Django, Keras, React
- Containerization: Docker

### Hardware
- Compute: Raspberry Pi 5, ESP32 WROOM
- Camera: XIAO ESP32S (multi-client video streaming)
- Sensors: 24GHz Radar, INMP441, MPU6050, HMC5883L
- Dev Tools: Arduino IDE

## 6. Project Structure

GAJA/
├── Hardware/
│ ├── esp32_camera_multiclient/
│ │ ├── src/
│ │ │ ├── LICENSE.txt
│ │ │ ├── camera_pins.h
│ │ │ ├── code.txt.txt
│ │ │ └── home_wifi_multi.h
│ │ └── esp32_camera_multiclient.ino
│ └── human_radar/
│ ├── radar_serial/
│ └── radar_targets/
├── Software/
│ ├── 3d_model/
│ │ ├── examples/
│ │ ├── vggt/
│ │ ├── CODE_OF_CONDUCT.md
│ │ ├── demo_colmap.py
│ │ ├── demo_gradio.py
│ │ ├── demo_viser.py
│ │ ├── pyproject.toml
│ │ ├── requirements_demo.txt
│ │ └── visual_util.py
│ ├── autonomous_navigation/
│ │ ├── static/
│ │ ├── templates/
│ │ ├── app.py
│ │ ├── location_data.csv
│ │ ├── req.txt
│ │ ├── ser.py
│ │ └── view.jpg
│ └── depth_estimation/
└── README.md



## 7. Development Phases

### Phase 1: R&D & Prototyping
- Radar detection + sensor fusion
- Offline navigation module
- AI hardware prototype with RPi5

### Phase 2: Alpha Integration
- Drone integration
- Alpha BSF dashboard
- Initial field tests

### Phase 3: Pilot Deployment
- Real-environment testing
- Feedback from BSF units
- Mass deployment preparation

## 8. Scalability & Applications

- Modular upgrade for legacy drones
- Extendable to search & rescue, agriculture, logistics
- Robust for extreme terrains and conditions

## 9. Impact & Safety

- Reduced exposure of personnel in hostile zones
- 24/7 autonomous monitoring
- Proactive threat mitigation and anomaly alerts

## 10. Challenges

- Edge inference on limited hardware
- False positive mitigation in "see-through" models
- Payload and flight dynamics with AI module

## 11. Getting Started

### Prerequisites

- Python 3.8+
- Node.js + npm
- Docker
- Arduino IDE
- Raspberry Pi 5 + sensors

### Installation


git clone https://github.com/your-username/GAJA.git
cd GAJA
Hardware
Setup ESP32 using esp32_camera_multiclient/

Connect and configure 24GHz radar via human_radar/

Software

12. Usage
Power up and deploy drone with AI attachment

Run backend and open the dashboard (http://localhost:3000)

Monitor 3D maps, alerts, and patrol status

