# VisionCursor: Vision-based Touchless HCI Interface

> **A real-time, non-contact mouse control system using monocular camera based hand tracking and gesture recognition.**

[![Python](https://img.shields.io/badge/Python-3.10-3776AB?style=flat&logo=python&logoColor=white)](https://www.python.org/)
[![OpenCV](https://img.shields.io/badge/OpenCV-4.x-5C3EE8?style=flat&logo=opencv&logoColor=white)](https://opencv.org/)
[![MediaPipe](https://img.shields.io/badge/MediaPipe-Latest-00C853?style=flat&logo=google&logoColor=white)](https://google.github.io/mediapipe/)
[![PyAutoGUI](https://img.shields.io/badge/PyAutoGUI-Automation-FF6F00?style=flat)](https://pyautogui.readthedocs.io/)

## Overview
**VisionCursor** is a Human-Computer Interaction (HCI) project designed to replace physical input devices with computer vision technology. By leveraging **MediaPipe's ML pipeline** for robust hand tracking and **geometric analysis** for gesture recognition, this system allows users to control the mouse cursor and perform clicks using intuitive hand movements.

This project focuses on **dynamic calibration** and **signal stability** to solve common jitter issues in vision-based control systems, aiming for a seamless user experience in robotics and kiosk environments.

## Key Features & Algorithms

### 1. Robust Gesture Recognition
* **Geometric Heuristics:** Determines finger states (Folded/Extended) by comparing the y-coordinates of finger tips relative to PIP (Proximal Interphalangeal) joints.
* **Euclidean Distance Calculation:** Detects 'Pinch' gestures for clicking by calculating the Euclidean distance between the thumb (Landmark 4) and index finger (Landmark 8).
    * *Threshold:* Triggers a click event when distance < 0.05 (normalized).

### 2. Signal Smoothing & Noise Reduction
* **Gesture Queueing:** Implements a queue-based filtering system (size: 5 frames) to prevent gesture flickering caused by detection noise.
* **Majority Voting:** The current gesture is confirmed only when consistency is maintained across consecutive frames using `collections.Counter`.

### 3. Dynamic Calibration (Offset System)
* **User-Centric Coordinate Mapping:** Recognizing that the camera's center and the user's comfortable "hand center" differ, the system implements a dynamic offset feature.
* **FIST Gesture Trigger:** Making a 'FIST' gesture resets the coordinate origin to the current hand position (`offset_x`, `offset_y`), allowing for personalized calibration.

### 4. Safety & Exception Handling
* **Boundary Clamping:** Prevents `PyAutoGUI` fail-safe errors by clamping cursor coordinates within the screen resolution (`max(5, min(width-5))`).

## 🛠️ System Architecture

The project follows a modular Object-Oriented Programming (OOP) structure:

```text
vision-cursor/
├── main.py                 # Entry point
├── src/
│   ├── __init__.py         # Package initialization
│   ├── vision_cursor.py    # Main controller (Orchestrator)
│   ├── hand_detector.py    # Vision processing & Landmark analysis
│   └── mouse_controller.py # OS-level input simulation
└── requirements.txt        # Dependencies
````

## 🚀 Installation & Usage

### Prerequisites

  * Python 3.10+
  * Webcam

### Installation

1.  **Clone the repository**

    ```bash
    git clone [https://github.com/vbn930/vision-cursor.git](https://github.com/vbn930/vision-cursor.git)
    cd vision-cursor
    ```

2.  **Set up Virtual Environment**

    ```bash
    python -m venv .venv
    # Windows
    .\.venv\Scripts\activate
    # Mac/Linux
    source .venv/bin/activate
    ```

3.  **Install Dependencies**

    ```bash
    pip install -r requirements.txt
    ```

### How to Run

```bash
python main.py
```

## Gesture Guide

| Gesture | Action | Description |
| :--- | :--- | :--- |
| **ONE (Index Up)** | `Cursor Move` | Move the cursor by moving your index finger. |
| **PINCH** | `Click Ready` | Pinch thumb and index finger together. |
| **PINCH (\< 0.05)** | `Click` | Maintains pinch to trigger click/drag actions. |
| **FIST** | `Calibration` | Resets the center point for comfortable mapping. |

## Future Roadmap

  * **Kalman Filter Implementation:** To further smooth cursor trajectory and predict movement for lower latency.
  * **Deep Learning Classification:** Replacing heuristic geometric rules with a lightweight CNN/LSTM model for complex gesture recognition.
  * **3D Depth Integration:** Utilizing depth sensors (RealSense/Kinect) for Z-axis control.

-----

**Author:** Dohun Lee
**Contact:** vbn9302@gmail.com

```