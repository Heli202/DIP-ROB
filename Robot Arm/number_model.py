from inference import InferencePipeline
import supervision as sv
import cv2

class NumberModel:
    def __init__(self):
        self.pipeline = InferencePipeline.init_with_workflow(
            api_key=
        )

    def predict(self, image):
        results = self.model.infer(image)[0]
        return results