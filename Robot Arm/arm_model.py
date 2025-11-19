import tensorflow as tf
from tensorflow.keras.preprocessing.image import load_img, img_to_array
import numpy as np


class ArmModel:
    def __init__(self):
        self.model = tf.keras.models.load_model("servo_model.keras")

    def predict(self, img_array: np.array) -> list[int]:
        predicted_positions = self.model.predict(img_array)[0]
        return predicted_positions.tolist()

    def load_image(self, path: str) -> np.array:
        img = load_img(path, target_size=(224, 224))
        return self.__make_image_array(img)

    @staticmethod
    def __make_image_array(img) -> np.array:
        img_array = img_to_array(img).astype("float32") / 255
        return np.expand_dims(img_array, 0)