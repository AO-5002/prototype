
from fastapi import APIRouter
from routes.websocket import router as websocket_router


router = APIRouter()
router.include_router(websocket_router)
