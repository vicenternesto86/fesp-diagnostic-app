"""Routers package"""
from app.routers.auth import router as auth_router
from app.routers.states import router as states_router
from app.routers.jurisdictions import router as jurisdictions_router
from app.routers.assessments import router as assessments_router
from app.routers.dashboard import router as dashboard_router
from app.routers.reports import router as reports_router
from app.routers.users import router as users_router

__all__ = [
    "auth_router", "states_router", "jurisdictions_router",
    "assessments_router", "dashboard_router", "reports_router", "users_router"
]
