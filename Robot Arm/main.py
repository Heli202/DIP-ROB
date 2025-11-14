import arm
import camera
import arm_model
import number_model
import cv2

numbers = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]

if __name__ == "__main__":
    #my_arm = arm.Arm()
    cam = camera.Camera()
    arm_model = arm_model.ArmModel()
    number_model = number_model.NumberModel()

    # number_prediction = number_model.predict(cam.take_snapshot())
    number_prediction = number_model.predict("../Puzzle Numbers/4.png")
    number_prediction = number_prediction[0].predictions[0].class_name
    print(f"The number I see is: {number_prediction}")

    if number_prediction in numbers:
        # states = my_arm.get_joints()
        # path = cam.take_snapshot(states)
        path = ".././saved_images/[26, 492, 284, 961, 611, 468].jpg"

        img_array = arm_model.load_image(path)
        predicted_servo_pos = arm_model.predict(img_array)
        print(predicted_servo_pos)

        # my_arm.move_servos(predicted_servo_pos)
        # my_arm.turn_off_servos()



