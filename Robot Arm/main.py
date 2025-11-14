import arm
import camera
import model


if __name__ == "__main__":
    #my_arm = arm.Arm()
    cam = camera.Camera()
    model = model.Model()

    # states = my_arm.get_joints()
    # path = cam.take_snapshot(states) # change back for test
    path = ".././saved_images/[26, 492, 284, 961, 611, 468].jpg"
    img_array = model.load_image(path)
    predicted_servo_pos = model.predict(img_array)
    print(predicted_servo_pos)
    # my_arm.move_servos(predicted_servo_pos)
    # my_arm.turn_off_servos()
