import time
import xarm


class Arm:
    def __init__(self):
        self.arm = xarm.Controller('USB')
        print('Battery voltage in volts:', self.arm.getBatteryVoltage())
        self.servo1 = xarm.Servo(1)
        self.servo2 = xarm.Servo(2)
        self.servo3 = xarm.Servo(3)
        self.servo4 = xarm.Servo(4)
        self.servo5 = xarm.Servo(5)
        self.servo6 = xarm.Servo(6)
        self.servos = [self.servo1, self.servo2, self.servo3, self.servo4, self.servo5, self.servo6]

    def set_state(self, state_name):
        states = {
            'home': [180, 500, 300, 90, 90, 500],  # Central safe pos (calibrate once)
            'ready_to_grab': [180, 500, 90, 350, 90, 500],  # Above fixed piece spot, gripper open/down
            'ready_to_move': [400, 500, 90, 350, 90, 500],   # Lifted 5-10cm, gripper closed
            'lift': [400, 500, 300, 350, 90, 500]
        }
        if state_name in states:
            for servo in self.servos:
                self.arm.setPosition(servo.servo_id, states[state_name][servo.servo_id - 1])
            print(f"Set to {state_name}")
            time.sleep(1.5)
            if state_name == 'ready_to_move':
                self.check_grip_success()
        else:
            print("Invalid state")

    def move_arm(self, positions: list[int]):
        if len(positions) != 6:
            print("Must have 6 positions in the array")
            return
        for servo in self.servos:
            self.arm.setPosition(servo.servo_id, positions[servo.servo_id - 1])

    def get_joints(self):
        joints = []
        for servo in self.servos:  # Returns list of 6 floats + voltages
            joints.append(self.arm.getPosition(servo))
        return joints

    def check_grip_success(self):
        if self.arm.getPosition(self.servo1.servo_id) > 400:
            print("Gripped")
            return True
        else:
            print("Not gripped")
            return False

    def turn_off_servos(self):
        for servo in self.servos:
            self.arm.servoOff(servo.servo_id)
