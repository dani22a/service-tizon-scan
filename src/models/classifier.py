import numpy as np
from keras.preprocessing import image
import json
from src.constants.general import (
    MODEL_PATH_EFFICIENT,
    MODEL_PATH_RESNET,
    MODEL_PATH_MOBILEVIT,
    JSON_PATH,
)
from keras.models import load_model
from keras.applications.efficientnet import preprocess_input as efficientnet_preprocess
from keras.applications.resnet import preprocess_input as resnet_preprocess
from PIL import Image
import io


def mobilevit_preprocess(x):
    return x / 255.0


MODEL_REGISTRY = {
    "efficient": {
        "path": MODEL_PATH_EFFICIENT,
        "preprocess": efficientnet_preprocess,
    },
    "resnet": {
        "path": MODEL_PATH_RESNET,
        "preprocess": resnet_preprocess,
    },
    "mobilevit": {
        "path": MODEL_PATH_MOBILEVIT,
        "preprocess": mobilevit_preprocess,
    },
}


class PotatoDiseaseClassifier:
    def __init__(self):
        with open(JSON_PATH, "r") as f:
            self.info = json.load(f)

        self.class_names = self.info["class_names"]
        self.img_size = self.info["img_size"]
        self.best_model = self.info.get("best_model", "efficient")
        self.training_metrics = self.info.get("metrics_classifier", {})

        self.models = {}
        for name, config in MODEL_REGISTRY.items():
            self.models[name] = {
                "model": load_model(config["path"]),
                "preprocess": config["preprocess"],
            }

    def _predict_single(self, model_name: str, pil_img: Image.Image) -> dict:
        config = self.models[model_name]
        img_resized = pil_img.resize((self.img_size, self.img_size))
        img_array = image.img_to_array(img_resized)
        img_array = np.expand_dims(img_array, axis=0)
        img_array = config["preprocess"](img_array)

        predictions = config["model"].predict(img_array, verbose=0)
        predicted_class = np.argmax(predictions[0])
        confidence = float(predictions[0][predicted_class])

        return {
            "modelo": model_name,
            "clase_predicha": self.class_names[predicted_class],
            "confianza": confidence,
            "todas_predicciones": {
                self.class_names[i]: float(predictions[0][i])
                for i in range(len(self.class_names))
            },
            "metricas_entrenamiento": self.training_metrics.get(model_name, {}),
        }

    def predict_all_models_bytes(self, img_bytes: bytes) -> dict:
        pil_img = Image.open(io.BytesIO(img_bytes)).convert("RGB")

        resultados = {}
        for model_name in self.models:
            resultados[model_name] = self._predict_single(model_name, pil_img)

        clases = [r["clase_predicha"] for r in resultados.values()]
        confianzas = {name: r["confianza"] for name, r in resultados.items()}
        modelo_mas_confiado = max(confianzas, key=confianzas.get)
        consenso = len(set(clases)) == 1

        return {
            "mejor_modelo_global": self.best_model,
            "resultados": resultados,
            "resumen_comparativo": {
                "consenso": consenso,
                "clase_consenso": clases[0] if consenso else None,
                "modelo_mas_confiado": modelo_mas_confiado,
                "confianza_maxima": confianzas[modelo_mas_confiado],
            },
        }

    def predict_bytes(self, img_bytes: bytes) -> dict:
        """Predicción con el mejor modelo (backward-compatible)."""
        pil_img = Image.open(io.BytesIO(img_bytes)).convert("RGB")
        return self._predict_single(self.best_model, pil_img)

    def predict(self, img_path: str) -> dict:
        """Predicción a partir de un path en disco."""
        pil_img = Image.open(img_path).convert("RGB")
        return self._predict_single(self.best_model, pil_img)

    def predict_batch(self, img_paths) -> list:
        """Predice múltiples imágenes a partir de paths en disco."""
        results = []
        for img_path in img_paths:
            result = self.predict(img_path)
            result["imagen"] = img_path
            results.append(result)
        return results


classifier = PotatoDiseaseClassifier()
