#! /usr/bin/python3.7
import xarm
import serial as ser
import arm

if __name__ == "__main__":
    arm = xarm.Controller("USB")
    arm.set_state("home")
    #states.set_state("ready_to_grab")
    #states.set_state("ready_to_move")
    #states.set_state("lift")
    print(arm.get_joints())
