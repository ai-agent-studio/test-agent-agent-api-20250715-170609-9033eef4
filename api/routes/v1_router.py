from fastapi import APIRouter

from api.routes.agents import agents_router

v1_router = APIRouter(prefix="/v1")
v1_router.include_router(agents_router)
