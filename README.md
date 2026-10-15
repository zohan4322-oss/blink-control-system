# Blink Control System

A Python-based computer vision project that detects eye blinks through a webcam and uses an Arduino to control a 12V DC bulb through a relay module.

## Overview

The Blink Control System allows a user to switch a physical bulb ON and OFF by blinking. The Python application processes webcam video, detects eye movements using facial landmarks, and sends serial commands to an Arduino.

This project was developed as a university project to explore computer vision, object-oriented programming, serial communication, and hardware control.

## Features

* Real-time webcam input using OpenCV.
* Facial landmark detection using MediaPipe Face Mesh.
* Eye Aspect Ratio (EAR) calculation for blink detection.
* State-machine-based recognition of completed blinks.
* Serial communication between Python and Arduino.
* Toggle control: each recognized blink switches the bulb's requested state.
* On-screen display of EAR, blink count, and device state.

## Technologies Used

### Software

* Python
* OpenCV
* MediaPipe
* NumPy
* PySerial

### Hardware

* Arduino board
* Webcam
* Relay module compatible with the circuit
* 12V DC bulb
* Suitable 12V DC power supply
* Required wiring and connections

## How It Works

1. OpenCV captures video from the webcam.
2. MediaPipe Face Mesh detects facial landmarks around the eyes.
3. The program calculates the Eye Aspect Ratio (EAR).
4. A blink state machine recognizes a completed blink.
5. Python sends a serial command to the Arduino.
6. The Arduino changes its output pin according to the received command.
7. The relay switches the bulb according to the circuit design.

The Python program sends `1` to request ON and `0` to request OFF.

## Project Files

* `blink_control_system.py` — Python application for blink detection and device control.
* `arduino_code.ino` — Arduino program for receiving serial commands and controlling the output pin.

## Requirements

Python dependencies:

* `opencv-python`
* `mediapipe`
* `numpy`
* `pyserial`

An Arduino development environment is required to upload the Arduino program to the board.

The Python program also requires a compatible webcam and an appropriate serial port configuration.

## Configuration

The Python program currently uses `COM4` as its default Arduino serial port and `9600` baud as its communication speed.

If your Arduino is assigned a different serial port, update the port configuration in the Python code.

The Arduino sketch uses digital pin 7 as its output.

## Running the Project

1. Connect the Arduino and required hardware.
2. Upload `arduino_code.ino` to the Arduino.
3. Install the required Python packages.
4. Check the Arduino's serial port and update the Python configuration if necessary.
5. Run `blink_control_system.py`.
6. Use the webcam to test blink detection and observe the device response.

## Limitations

* Blink detection depends on camera quality, lighting, face position, and detection thresholds.
* The current implementation uses a fixed EAR threshold.
* The displayed device state represents the program's requested state; the software does not independently verify the physical bulb's state.
* The default serial port may need to be changed for another computer.

## Learning Outcomes

This project provided practical experience with computer vision, facial landmarks, blink detection, object-oriented programming, state machines, serial communication, and Arduino-based hardware control.

AI assistance was used during development.
