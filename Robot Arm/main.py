import xarm
import serial as ser
import states

if __name__ == "__main__":
    arm = xarm.Controller("USB")
    states.set_state("home")
    #states.set_state("ready_to_grab")
    #states.set_state("ready_to_move")
    #states.set_state("lift")
    print(states.get_joints())
