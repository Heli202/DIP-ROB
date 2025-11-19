from inference import get_model
import json
import cv2

class NumberModel:
    def __init__(self):
        secrets_file = 'secrets/secrets.json'
        with open(secrets_file) as f:
            api_key = json.load(f).get('api_key')

        self.model = get_model("numbers-xnrog-d6zw6/1", api_key)

    def predict(self, image_path):
        return self.model.infer(cv2.imread(image_path))
