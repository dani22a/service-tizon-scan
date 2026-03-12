from types import SimpleNamespace

import pytest
from fastapi import HTTPException

from src.services import roboflow_service


VALID_IMAGE_URL = "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRstfdrZEb9SnHazGH5CMQRZxygnOiM5YbnpQ&s"


class _FakeRoboflowClient:
    def __init__(self, result: dict | None = None, error: Exception | None = None):
        self.result = result or {"predictions": []}
        self.error = error

    def infer_image_url(self, image_url: str) -> dict:
        if self.error:
            raise self.error
        return self.result

    def infer_image_path(self, image_path: str) -> dict:
        if self.error:
            raise self.error
        return self.result


@pytest.fixture
def fake_config(monkeypatch: pytest.MonkeyPatch) -> SimpleNamespace:
    config = SimpleNamespace(
        MAX_IMAGE_SIZE_MB=1,
        ROBOFLOW_TIMEOUT_SEC=2,
        ROBOFLOW_MODEL_ID="potato_late_blight_yolov8n/10",
        ROBOFLOW_API_KEY="test-key",
        ROBOFLOW_API_URL="https://serverless.roboflow.com",
    )
    monkeypatch.setattr(roboflow_service, "get_config", lambda: config)
    return config


def test_validate_image_content_type_ok() -> None:
    roboflow_service.validate_image_content_type("image/png")


def test_validate_image_content_type_invalid() -> None:
    with pytest.raises(HTTPException) as exc:
        roboflow_service.validate_image_content_type("text/plain")
    assert exc.value.status_code == 400


def test_validate_image_url_invalid() -> None:
    with pytest.raises(HTTPException) as exc:
        roboflow_service.validate_image_url("ftp://example.com/img.jpg")
    assert exc.value.status_code == 400


def test_validate_image_size_empty(fake_config: SimpleNamespace) -> None:
    _ = fake_config
    with pytest.raises(HTTPException) as exc:
        roboflow_service.validate_image_size(b"")
    assert exc.value.status_code == 400


def test_validate_image_size_too_large(fake_config: SimpleNamespace) -> None:
    _ = fake_config
    with pytest.raises(HTTPException) as exc:
        roboflow_service.validate_image_size(b"a" * (2 * 1024 * 1024))
    assert exc.value.status_code == 413


@pytest.mark.asyncio
async def test_service_requires_file_or_url() -> None:
    with pytest.raises(HTTPException) as exc:
        await roboflow_service.roboflow_inference_service()
    assert exc.value.status_code == 400


@pytest.mark.asyncio
async def test_service_url_success(fake_config: SimpleNamespace, monkeypatch: pytest.MonkeyPatch) -> None:
    _ = fake_config
    payload = {
        "predictions": [
            {
                "x": 174.5,
                "y": 46.5,
                "width": 123,
                "height": 97,
                "confidence": 0.707,
                "class": "blight",
                "class_id": 0,
                "detection_id": "81f1cf32-d08e-4922-bd21-e26b19de03ac",
            }
        ]
    }
    monkeypatch.setattr(roboflow_service, "_build_client", lambda: _FakeRoboflowClient(result=payload))

    result = await roboflow_service.roboflow_inference_service(
        image_url=VALID_IMAGE_URL
    )

    assert result["source"] == "url"
    assert result["model_id"] == "potato_late_blight_yolov8n/10"
    assert result["has_matches"] is True
    assert len(result["predictions"]) == 1
    assert result["predictions"][0]["class"] == "blight"


@pytest.mark.asyncio
async def test_service_no_matches_success(
    fake_config: SimpleNamespace, monkeypatch: pytest.MonkeyPatch
) -> None:
    _ = fake_config
    monkeypatch.setattr(
        roboflow_service,
        "_build_client",
        lambda: _FakeRoboflowClient(result={"predictions": []}),
    )

    result = await roboflow_service.roboflow_inference_service(
        image_url=VALID_IMAGE_URL
    )

    assert result["source"] == "url"
    assert result["predictions"] == []
    assert result["has_matches"] is False


@pytest.mark.asyncio
async def test_service_file_success(fake_config: SimpleNamespace, monkeypatch: pytest.MonkeyPatch) -> None:
    _ = fake_config
    payload = {
        "predictions": [
            {
                "x": 10,
                "y": 10,
                "width": 20,
                "height": 20,
                "confidence": 0.9,
                "class": "leaf",
                "class_id": 1,
                "detection_id": "det-1",
            }
        ]
    }
    monkeypatch.setattr(roboflow_service, "_build_client", lambda: _FakeRoboflowClient(result=payload))

    result = await roboflow_service.roboflow_inference_service(image_bytes=b"fake-image-bytes")

    assert result["source"] == "file"
    assert result["has_matches"] is True
    assert result["predictions"][0]["class"] == "leaf"


@pytest.mark.asyncio
async def test_service_timeout_maps_to_504(
    fake_config: SimpleNamespace, monkeypatch: pytest.MonkeyPatch
) -> None:
    _ = fake_config
    monkeypatch.setattr(
        roboflow_service,
        "_build_client",
        lambda: _FakeRoboflowClient(error=TimeoutError("timeout")),
    )

    with pytest.raises(HTTPException) as exc:
        await roboflow_service.roboflow_inference_service(
            image_url=VALID_IMAGE_URL
        )

    assert exc.value.status_code == 504
