# Object Detection and Policy Model Robot Arm Number Puzzle

This project contains the use of both an object detection model to detect numbers of a childrens' puzzle game, and a
policy model to predict the servo positions of a robot arm to be able to pick up the puzzle piece and place it in 
the correct position.

This however is the end goal, and not what the models are currently able to do.

## Table of Contents
- [Features](#features)
- [Required Hardware](#required-hardware)
- [Required Software](#required-software)
- [Instructions](#instructions)
- [License](#license)
- [Libraries](#libraries)

## Features
- Detecting a puzzle piece with the number 0-9 (sometimes inaccurate).
- Policy model attempting to move a robot arm to the puzzle piece (very likely to miss).
- Tries another two times with the new states.

## Required Hardware
- **xArm 1s**
- **USB Webcam**

Both connected to the same PC.

## Required Software
- An IDE capable of interpretting Python (this project used Python 3.12)

## Instructions
1. Clone the repo:
```git clone https://github.com/Heli202/DIP-ROB.git```
2. After creating a virtual environment, pip install the requirements:
```pip install -r requirements.txt```
3. Place a puzzle piece in view underneath the camera, ensuring the robot arm can reach it.
4. Run ```main.py``` inside ```/Robot Arm``` and observe the robot trying to pick up a number.

### Demo Video
A video demonstrating the project in its current state can be found here: [Demo Video](https://youtu.be/YhuzUlPbKec)

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Libraries
The [requirements.txt](requirements.txt) file in the root directory contains all libraries used in this project.
