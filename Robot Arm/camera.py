import cv2
import os


class Camera:
    def __init__(self):
        self.camera = cv2.VideoCapture(1)
        self.output_folder = "saved_images"
        self.temp_output_folder = "temp_images"
        os.makedirs(self.output_folder, exist_ok=True)
        os.makedirs(self.temp_output_folder, exist_ok=True)

    def take_snapshot(self, states):
        camera_read_success, frame = self.camera.read()
        self.camera.release()
        if camera_read_success:
            print("Successfully read from camera")
            if states:
                full_path = os.path.join(self.output_folder, f"{states}.jpg")
            else:
                full_path = os.path.join("temp_images", "temp.jpg")
            write_success = cv2.imwrite(full_path, frame)
            if write_success:
                print(f"Successfully saved image with {full_path}")
                return full_path
            else:
                print("Could not write image")
        else:
            print("Cannot read from camera")
