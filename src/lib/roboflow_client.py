import httpx


class RoboflowClient:
    def __init__(self, api_url: str, api_key: str, model_id: str):
        self.api_url = api_url.rstrip("/")
        self.api_key = api_key
        self.model_id = model_id

    def _infer(self, **request_kwargs: object) -> dict:
        url = f"{self.api_url}/{self.model_id}"
        with httpx.Client(timeout=60.0) as client:
            response = client.post(
                url,
                params={"api_key": self.api_key},
                **request_kwargs,
            )
            response.raise_for_status()
            return response.json()

    def infer_image_path(self, image_path: str) -> dict:
        with open(image_path, "rb") as image_file:
            return self._infer(files={"file": image_file})

    def infer_image_url(self, image_url: str) -> dict:
        return self._infer(data={"image": image_url})
