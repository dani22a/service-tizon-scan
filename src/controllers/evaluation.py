from fastapi import APIRouter, UploadFile, File, Form, HTTPException, Request, Body
from src.models.classifier import classifier
from src.helpers.response import success_response
from src.services.roboflow_service import (
  roboflow_inference_service,
  validate_image_content_type,
)
from src.services.evaluation_service import (
  save_image_locally,
  create_prediccion_fase1,
  update_prediccion_fase2,
  list_predicciones_by_user,
  list_all_surcos_for_user,
  create_diagnosis_report_with_recommendations,
  list_recommendations_by_user,
  prediccion_to_dict,
)
from src.services import prediction_recommendation_service

router = APIRouter()


def _get_user_id(request: Request, default: int = 1) -> int:
  user_id = getattr(request.state, "user_id", None)
  return user_id if user_id else default


@router.post("/roboflow", status_code=200)
async def evaluate_roboflow(
  request: Request,
  file: UploadFile | None = File(None),
  image_url: str | None = Form(None),
  surco_id: int | None = Form(None),
  periodo_id: int | None = Form(None),
):
  user_id = _get_user_id(request)
  
  if file and image_url:
    raise HTTPException(status_code=400, detail="Provide only one input: file or image_url")
  if not file and not image_url:
    raise HTTPException(status_code=400, detail="Provide either an image file or image_url")

  image_bytes: bytes | None = None
  saved_image_url: str | None = None

  if file:
    validate_image_content_type(file.content_type)
    image_bytes = await file.read()
    saved_image_url = save_image_locally(image_bytes, file.content_type, request)

  result = await roboflow_inference_service(image_bytes=image_bytes, image_url=image_url)

  await create_prediccion_fase1(
    user_id=user_id,
    imagen_url=saved_image_url or image_url or "",
    fase1_payload=result,
    surco_id=surco_id,
    periodo_id=periodo_id,
  )

  message = "inference successful"
  if not result.get("predictions"):
    message = "No hubo coincidencias"

  return success_response(
    result,
    message,
    status_code=200,
  )


@router.post("/evaluate", status_code=200)
async def evaluate(
  request: Request,
  file: UploadFile = File(...),
  periodo_id: int | None = Form(None),
):
  if not file.content_type or not file.content_type.startswith("image/"):
    raise HTTPException(status_code=400, detail="Invalid image format")

  user_id = _get_user_id(request)

  img_bytes = await file.read()
  result = classifier.predict_all_models_bytes(img_bytes)

  prediccion = await update_prediccion_fase2(user_id=user_id, fase2_payload=result)
  if prediccion and periodo_id is not None:
      # in case we want to update periodo on phase2, set and save
      prediccion.periodo_id = periodo_id
      await prediccion.save()

  response_data = {
    "clasificacion": result,
  }
  if prediccion:
    response_data["prediccion"] = await prediccion_to_dict(prediccion)

  return success_response(response_data, "Evaluation successful", status_code=200)


@router.get("/surcos", status_code=200)
async def get_user_surcos(request: Request):
  user_id = _get_user_id(request)
  surcos = await list_all_surcos_for_user(user_id)
  return success_response(surcos, "Surcos obtenidos", status_code=200)


@router.get("/history", status_code=200)
async def get_evaluation_history(request: Request):
  user_id = _get_user_id(request)
  predicciones = await list_predicciones_by_user(user_id)
  return success_response(predicciones, "Historial de predicciones", status_code=200)


@router.post("/diagnosis", status_code=201)
async def create_diagnosis(
  request: Request,
  payload: dict = Body(...),
):
  """
  Guarda un snapshot de diagnóstico agregado + recomendaciones.
  El payload debe seguir la estructura documentada en create_diagnosis_report_with_recommendations.
  """
  user_id = _get_user_id(request)
  report = await create_diagnosis_report_with_recommendations(user_id=user_id, payload=payload)
  return success_response(report, "Diagnosis report creado", status_code=201)


@router.get("/diagnosis/recommendations", status_code=200)
async def get_diagnosis_recommendations(request: Request):
  """
  Retorna todas las recomendaciones de diagnóstico del usuario actual.
  """
  user_id = _get_user_id(request)
  recomendaciones = await list_recommendations_by_user(user_id)
  return success_response(recomendaciones, "Recomendaciones de diagnóstico", status_code=200)


# ── Recomendaciones por predicción individual ──────────────────────

@router.post("/predicciones/{prediccion_id}/recommendation", status_code=201)
async def create_prediccion_recommendation(
  request: Request,
  prediccion_id: int,
  payload: dict = Body(...),
):
  """
  Guarda una recomendación para una predicción específica.
  El frontend envía el snapshot de métricas junto con el texto de la recomendación.

  Payload esperado:
  {
    "categoria": "fungicida|monitoreo|riego|general|alerta",
    "prioridad": "urgente|alta|media|baja",
    "titulo": str,
    "contenido": str,
    "etiquetas": list[str] | null,
    "metricas_snapshot": {
      "fase1_resumen": {...} | null,
      "fase2_resumen": {...} | null,
      "surco_id": int | null,
      "surco_numero": int | null,
      "lote_identificador": str | null,
      "modulo_nombre": str | null
    } | null
  }
  """
  user_id = _get_user_id(request)
  from src.models.prediccion import Prediccion
  prediccion = await Prediccion.filter(id=prediccion_id, usuario_id=user_id).first()
  if not prediccion:
    raise HTTPException(status_code=404, detail="Predicción no encontrada")
  rec = await prediction_recommendation_service.create_prediccion_recommendation(
    user_id=user_id,
    prediccion_id=prediccion_id,
    payload=payload,
  )
  return success_response(rec, "Recomendación de predicción guardada", status_code=201)


@router.get("/predicciones/{prediccion_id}/recommendation", status_code=200)
async def list_prediccion_recommendations(
  request: Request,
  prediccion_id: int,
):
  """
  Retorna el historial de recomendaciones de una predicción específica.
  """
  user_id = _get_user_id(request)
  from src.models.prediccion import Prediccion
  prediccion = await Prediccion.filter(id=prediccion_id, usuario_id=user_id).first()
  if not prediccion:
    raise HTTPException(status_code=404, detail="Predicción no encontrada")
  recs = await prediction_recommendation_service.list_prediccion_recommendations(prediccion_id)
  return success_response(recs, "Historial de recomendaciones de la predicción", status_code=200)
