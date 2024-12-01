from fastapi import APIRouter
from .google import router as google_router

router = APIRouter(prefix="/auth", tags=["auth"])

router.include_router(google_router)
