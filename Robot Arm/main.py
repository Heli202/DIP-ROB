import arm
import camera
import arm_model
import number_model
import cv2
import time
import sys

numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']

if __name__ == "__main__":
    my_arm = arm.Arm()
    cam = camera.Camera()
    arm_model = arm_model.ArmModel()
    number_model = number_model.NumberModel()

    time.sleep(1)

    attempts = []

    for i in range(3):
        states = my_arm.get_joints()
        path = cam.take_snapshot(states)
        if path is None:
            break

        number_prediction = number_model.predict(path)
        count = 0
        while len(number_prediction[0].predictions) == 0:
            path = cam.take_snapshot(states)
            number_prediction = number_model.predict(path)
            if count == 4:
                sys.exit("Exiting script after 5 attempts to find number.")
            print("Couldn't find a number. Retrying in 5 seconds...")
            time.sleep(5)
            count += 1

        number_prediction = number_prediction[0].predictions[0].class_name
        print(f"The number I see is: {number_prediction}")

        time.sleep(3)

        if number_prediction in numbers:
            print("Number was in the list")
            img_array = arm_model.load_image(path)
            predicted_servo_pos = arm_model.predict(img_array)
            print(f"BEFORE Predicted servo pos: {predicted_servo_pos}")
            predicted_servo_pos = [x * 1000 for x in predicted_servo_pos]
            predicted_servo_pos = [int(x) for x in predicted_servo_pos]
            print(f"AFTER Predicted servo pos: {predicted_servo_pos}")

            time.sleep(2)

            print(predicted_servo_pos)
            attempts.append(f"Attempt {i + 1}: {predicted_servo_pos}")
            my_arm.move_arm(predicted_servo_pos)
            time.sleep(3)
            my_arm.turn_off_servos()
            time.sleep(5)

    cam.camera.release()
    for attempt in attempts:
        print(attempt)