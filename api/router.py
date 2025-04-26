from fastapi import APIRouter

from api.endpoints import todo

v1_router = APIRouter(prefix="/api/v1")

v1_router.include_router(todo.router)