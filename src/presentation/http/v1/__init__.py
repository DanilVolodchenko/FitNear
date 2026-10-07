from fastapi import APIRouter

from src.presentation.http.v1.auth.endpoint import router as auth_router

v1_router = APIRouter(prefix='/api/v1')
v1_router.include_router(auth_router)
