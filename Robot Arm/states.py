# In your xArm serial module (adapt from docs)
import time

import xarm
import serial as ser

# arm is the first xArm detected which is connected to USB
arm = xarm.Controller('USB')
print('Battery voltage in volts:', arm.getBatteryVoltage())

# 0 - gripper
# 1 - gripper
# 2
# 3
# 4 - forearm
# 5

servo1 = xarm.Servo(1)
servo2 = xarm.Servo(2)
servo3 = xarm.Servo(3)
servo4 = xarm.Servo(4)
servo5 = xarm.Servo(5)
servo6 = xarm.Servo(6)
servos = [servo1, servo2, servo3, servo4, servo5, servo6]

def set_state(state_name):
    states = {
        'home': [180, 500, 300, 90, 90, 500],  # Central safe pos (calibrate once)
        'ready_to_grab': [180, 500, 90, 350, 90, 500],  # Above fixed piece spot, gripper open/down
        'ready_to_move': [400, 500, 90, 350, 90, 500],   # Lifted 5-10cm, gripper closed
        'lift': [400, 500, 300, 350, 90, 500]
    }
    if state_name in states:
        for servo in servos:
            arm.setPosition(servo.servo_id, states[state_name][servo.servo_id - 1])
        print(f"Set to {state_name}")
        time.sleep(1.5)
        if state_name == 'ready_to_move':
            check_grip_success()
    else:
        print("Invalid state")

def get_joints():
    joints = []
    for servo in servos:  # Returns list of 6 floats + voltages
        joints.append(arm.getPosition(servo))
    return joints

def check_grip_success():
    if arm.getPosition(servo1.servo_id) > 400:
        print("Gripped")
        return True
    else:
        print("Not gripped")
        return False

def turn_off_servos():
    for servo in servos:
        arm.servoOff(servo.servo_id)