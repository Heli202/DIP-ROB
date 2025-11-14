import arm
import camera
import tensorflow as tf
from tensorflow.keras.preprocessing.image import load_img, img_to_array
import numpy as np
# import time



if __name__ == "__main__":
    model = tf.keras.models.load_model("servo_model.keras")
    my_arm = arm.Arm()
    cam = camera.Camera()
    # my_arm.set_state("home")
    # arm.set_state("ready_to_grab")
    # arm.set_state("ready_to_move")
    # arm.set_state("lift")
    # time.sleep(0.5)
    states = my_arm.get_joints()
    path = cam.take_snapshot(states)
    my_arm.turn_off_servos()

