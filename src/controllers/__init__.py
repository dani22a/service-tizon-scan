from fastapi import APIRouter
from src.controllers.auth import router as auth_router
from src.controllers.cultivo import router as cultivo_router
from src.controllers.evaluation import router as evaluation_router
from src.controllers.train import router as train_router
from src.controllers.metrics import router as metrics_router
from src.controllers.periodo import router as periodo_router

router = APIRouter()

router.include_router(auth_router, tags=["auth"])
router.include_router(cultivo_router,prefix="/modulos", tags=["cultivo"])
router.include_router(evaluation_router,prefix="/evaluation", tags=["evaluation"])
router.include_router(train_router,prefix="/train", tags=["train"])
router.include_router(metrics_router,prefix="/metrics", tags=["metrics"])
router.include_router(periodo_router, tags=["periodos"])