"""
FESP Diagnostic App - Main Application
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from app.config import settings
from app.database import init_db
from app.routers import (
    auth_router, states_router, jurisdictions_router,
    assessments_router, dashboard_router, reports_router, users_router
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan - initialize database on startup"""
    init_db()
    yield


app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="""
    API para el Instrumento Consolidado de Diagnóstico Rápido FESP.
    
    ## Funcionalidades
    
    * **Autenticación**: Login con JWT
    * **Catálogos**: Estados y Jurisdicciones
    * **Evaluaciones**: CRUD de diagnósticos FESP
    * **Dashboard**: Resumen ejecutivo, KPIs, brechas
    * **Reportes**: Exportación PDF y CSV
    * **Administración**: Gestión de usuarios
    
    ## Roles
    
    * **Admin**: Acceso total
    * **Writer**: Captura y edición de evaluaciones
    * **Reader**: Solo lectura y descarga de reportes
    """,
    lifespan=lifespan
)

# CORS middleware - allow all Vercel preview URLs and localhost
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "https://fesp-dx.vercel.app",
    ],
    allow_origin_regex=r"https://.*\.vercel\.app",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth_router)
app.include_router(states_router)
app.include_router(jurisdictions_router)
app.include_router(assessments_router)
app.include_router(dashboard_router)
app.include_router(reports_router)
app.include_router(users_router)


@app.get("/", tags=["Root"])
def root():
    """API Root - Health check"""
    return {
        "app": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "status": "running",
        "docs": "/docs"
    }


@app.get("/health", tags=["Root"])
def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}
