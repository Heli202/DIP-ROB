import arm
import camera
import arm_model
import number_model
import cv2


if __name__ == "__main__":
    #my_arm = arm.Arm()
    cam = camera.Camera()
    arm_model = arm_model.ArmModel()
    number_model = number_model.NumberModel()

    # states = my_arm.get_joints()
    # path = cam.take_snapshot(states) # change back for test
    path = ".././saved_images/[26, 492, 284, 961, 611, 468].jpg"
    img_array = arm_model.load_image(path)
    predicted_servo_pos = arm_model.predict(img_array)
    print(predicted_servo_pos)
    # my_arm.move_servos(predicted_servo_pos)
    # my_arm.turn_off_servos()
    predicted_number = number_model.predict(cv2.imread("../Puzzle Numbers/0 normal.png"))
    print(predicted_number)

