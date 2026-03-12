from pydantic import BaseModel, Field, ConfigDict


class RoboflowPrediction(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    x: float
    y: float
    width: float
    height: float
    confidence: float
    class_name: str = Field(alias="class")
    class_id: int | None = None
    detection_id: str | None = None

    def to_provider_shape(self) -> dict:
        return {
            "x": self.x,
            "y": self.y,
            "width": self.width,
            "height": self.height,
            "confidence": self.confidence,
            "class": self.class_name,
            "class_id": self.class_id,
            "detection_id": self.detection_id,
        }


class RoboflowInferenceResponse(BaseModel):
    source: str
    model_id: str
    predictions: list[RoboflowPrediction]

    @property
    def has_matches(self) -> bool:
        return len(self.predictions) > 0
