from fastapi import APIRouter

from src.controller.http.v1 import v1_router

router = APIRouter()

router.include_router(v1_router)
