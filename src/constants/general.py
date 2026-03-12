from pathlib import Path

MODEL_DIR = Path(__file__).parent.parent.parent / "model"

MODEL_PATH_EFFICIENT = MODEL_DIR / "model_efficient.keras"
MODEL_PATH_RESNET = MODEL_DIR / "model_resnet.keras"
MODEL_PATH_MOBILEVIT = MODEL_DIR / "model_mobilevit.keras"

JSON_PATH = MODEL_DIR / "metrics.json"

HISTORY_PATH = MODEL_DIR / "history_efficient.png"