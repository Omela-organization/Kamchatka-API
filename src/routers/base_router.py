from fastapi import APIRouter

from src.routers.v1.auth import router_auth
from src.routers.v1.user import router_user
from src.routers.v1.role import router_role
from src.routers.v1.status import router_status
from src.routers.v1.type_incident import router_type_incident
from src.routers.v1.territory import router_territory
from src.routers.v1.track import router_track
from src.routers.v1.feedback import router_feedback
from src.routers.v1.applications import router_application
from src.routers.v1.eco_problem import router_eco_problem
from src.routers.v1.photo import router_photo
from src.routers.v1.document import router_document
from src.routers.v1.eco_monitoring import router_eco_monitoring

base_router = APIRouter(prefix="/api/v1")

base_router.include_router(router_auth)
base_router.include_router(router_user)
base_router.include_router(router_role)
base_router.include_router(router_status)
base_router.include_router(router_type_incident)
base_router.include_router(router_territory)
base_router.include_router(router_track)
base_router.include_router(router_feedback)
base_router.include_router(router_application)
base_router.include_router(router_eco_problem)
base_router.include_router(router_photo)
base_router.include_router(router_document)
base_router.include_router(router_eco_monitoring)



