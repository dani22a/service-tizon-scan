from inference_sdk import InferenceHTTPClient


class RoboflowClient:
    def __init__(self, api_url: str, api_key: str, model_id: str):
        self.model_id = model_id
        self.client = InferenceHTTPClient(api_url=api_url, api_key=api_key)

    def infer_image_path(self, image_path: str) -> dict:
        return self.client.infer(image_path, model_id=self.model_id)

    def infer_image_url(self, image_url: str) -> dict:
        return self.client.infer(image_url, model_id=self.model_id)
