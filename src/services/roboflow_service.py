import asyncio
import os
import tempfile
from fastapi import HTTPException
from urllib.parse import urlparse

from src.config import get_config
from src.lib.roboflow_client import RoboflowClient
from src.schemas.evaluation import RoboflowInferenceResponse, RoboflowPrediction


_ALLOWED_IMAGE_TYPES = {
    "image/jpeg",
    "image/jpg",
    "image/png",
    "image/webp",
}


def validate_image_content_type(content_type: str | None) -> None:
    if not content_type or content_type.lower() not in _ALLOWED_IMAGE_TYPES:
        raise HTTPException(status_code=400, detail="Invalid image format")


def validate_image_url(image_url: str) -> None:
    parsed = urlparse(image_url)
    if parsed.scheme not in {"http", "https"} or not parsed.netloc:
        raise HTTPException(status_code=400, detail="Invalid image URL")


def validate_image_size(img_bytes: bytes) -> None:
    if not img_bytes:
        raise HTTPException(status_code=400, detail="Empty image file")

    config = get_config()
    max_size_bytes = config.MAX_IMAGE_SIZE_MB * 1024 * 1024
    if len(img_bytes) > max_size_bytes:
        raise HTTPException(status_code=413, detail="Image exceeds maximum allowed size")


def _build_client() -> RoboflowClient:
    config = get_config()

    if not config.ROBOFLOW_API_KEY:
        raise HTTPException(status_code=500, detail="ROBOFLOW_API_KEY is not configured")
    if not config.ROBOFLOW_MODEL_ID:
        raise HTTPException(status_code=500, detail="ROBOFLOW_MODEL_ID is not configured")

    return RoboflowClient(
        api_url=config.ROBOFLOW_API_URL,
        api_key=config.ROBOFLOW_API_KEY,
        model_id=config.ROBOFLOW_MODEL_ID,
    )


def _normalize_response(raw_result: dict, source: str) -> dict:
    config = get_config()
    raw_predictions = raw_result.get("predictions", [])

    parsed_predictions: list[RoboflowPrediction] = []
    for raw_prediction in raw_predictions:
        parsed_predictions.append(RoboflowPrediction.model_validate(raw_prediction))

    response = RoboflowInferenceResponse(
        source=source,
        model_id=config.ROBOFLOW_MODEL_ID or "",
        predictions=parsed_predictions,
    )

    return {
        "source": response.source,
        "model_id": response.model_id,
        "predictions": [prediction.to_provider_shape() for prediction in response.predictions],
        "has_matches": response.has_matches,
    }


async def roboflow_inference_service(
    image_bytes: bytes | None = None,
    image_url: str | None = None,
) -> dict:
    if not image_bytes and not image_url:
        raise HTTPException(status_code=400, detail="Provide either an image file or image_url")

    client = _build_client()

    config = get_config()

    try:
        if image_url:
            validate_image_url(image_url)
            raw_result = await asyncio.wait_for(
                asyncio.to_thread(client.infer_image_url, image_url),
                timeout=config.ROBOFLOW_TIMEOUT_SEC,
            )
            return _normalize_response(raw_result, source="url")

        validate_image_size(image_bytes or b"")

        with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as temp_file:
            temp_file.write(image_bytes or b"")
            temp_path = temp_file.name

        try:
            raw_result = await asyncio.wait_for(
                asyncio.to_thread(client.infer_image_path, temp_path),
                timeout=config.ROBOFLOW_TIMEOUT_SEC,
            )
            return _normalize_response(raw_result, source="file")
        finally:
            if os.path.exists(temp_path):
                os.remove(temp_path)

    except HTTPException:
        raise
    except TimeoutError:
        raise HTTPException(status_code=504, detail="Roboflow inference timeout")
    except Exception as exc:
        raise HTTPException(status_code=502, detail=f"Roboflow inference failed: {str(exc)}")
