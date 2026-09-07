# FESP Diagnostic App

**Instrumento Consolidado de Diagnóstico Rápido FESP**

Sistema web para la evaluación de las Funciones Esenciales de Salud Pública a nivel Estatal y por Jurisdicción Sanitaria.

## 🚀 Inicio Rápido

### Requisitos Previos
- Python 3.10+
- Node.js 18+
- npm o yarn

### 1. Backend (FastAPI)

```bash
cd backend

# Crear entorno virtual
python -m venv venv

# Activar entorno (Windows)
venv\Scripts\activate

# Activar entorno (Linux/Mac)
source venv/bin/activate

# Instalar dependencias
pip install -r requirements.txt

# Cargar datos de prueba
python seed_data.py

# Iniciar servidor
uvicorn app.main:app --reload
```

El backend estará en: http://localhost:8000
Documentación API: http://localhost:8000/docs

### 2. Frontend (React + Vite)

```bash
cd frontend

# Instalar dependencias
npm install

# Iniciar servidor de desarrollo
npm run dev
```

El frontend estará en: http://localhost:5173

## 👤 Usuarios de Prueba

| Email | Contraseña | Rol |
|-------|------------|-----|
| admin@fesp.gob.mx | admin123 | Admin |
| captura.tam@fesp.gob.mx | captura123 | Writer (Estatal) |
| captura.j1@fesp.gob.mx | captura123 | Writer (Jurisdicción) |
| lector.tam@fesp.gob.mx | lector123 | Reader |

## 📋 Características

### Captura de Diagnóstico
- 4 bloques con 11 ítems FESP
- Escala 0-5 (Inexistente → Óptimo)
- Campos para evidencia y observaciones
- Guardado parcial (borradores)

### Dashboard Ejecutivo
- Filtros por Estado/Jurisdicción/Fecha
- KPIs: Puntaje total, semáforo, brechas
- Gráfica de barras por bloque
- Gráfica radar comparativa
- Tabla detallada por ítem
- Recomendaciones automáticas

### Reportes
- Descarga PDF con portada, gráficas y tablas
- Exportación CSV de datos

### Administración
- Gestión de usuarios (CRUD)
- Control de acceso por rol
- Catálogos de Estados/Jurisdicciones

## 🔐 Roles y Permisos

| Rol | Permisos |
|-----|----------|
| **Admin** | Acceso total, gestión de usuarios/catálogos |
| **Writer** | Captura/edición de evaluaciones asignadas |
| **Reader** | Solo lectura y descarga de reportes |

## 📁 Estructura del Proyecto

```
FESP Dx fast/
├── backend/
│   ├── app/
│   │   ├── main.py           # FastAPI app
│   │   ├── config.py         # Configuración
│   │   ├── database.py       # SQLAlchemy
│   │   ├── models/           # Modelos BD
│   │   ├── schemas/          # Pydantic schemas
│   │   ├── routers/          # API endpoints
│   │   └── utils/            # Auth, cálculos
│   ├── requirements.txt
│   └── seed_data.py
├── frontend/
│   ├── src/
│   │   ├── components/       # Navbar
│   │   ├── context/          # AuthContext
│   │   ├── pages/            # Login, Dashboard, etc.
│   │   ├── services/         # API client
│   │   └── styles/           # CSS
│   ├── package.json
│   └── vite.config.js
└── README.md
```

## 🎯 API Endpoints

### Autenticación
- `POST /api/auth/login` - Login con JWT
- `GET /api/auth/me` - Usuario actual

### Catálogos
- `GET /api/states` - Listar estados
- `GET /api/jurisdictions/by-state/{id}` - Jurisdicciones por estado

### Evaluaciones
- `GET /api/assessments` - Listar con filtros
- `POST /api/assessments` - Crear nueva
- `PUT /api/assessments/{id}` - Actualizar
- `GET /api/assessments/{id}` - Obtener con ítems

### Dashboard
- `GET /api/dashboard/summary/{id}` - Resumen ejecutivo
- `GET /api/dashboard/compare` - Comparar evaluaciones

### Reportes
- `GET /api/reports/pdf/{id}` - Descargar PDF
- `GET /api/reports/csv` - Exportar CSV

## ⚙️ Configuración

Variables de entorno (opcional `.env` en backend/):

```env
SECRET_KEY=tu-clave-secreta
DATABASE_URL=sqlite:///./fesp_diagnostic.db
DEBUG=True
```

## 📊 Semáforo

| Rango | Color | Estado |
|-------|-------|--------|
| 0 - 1.9 | 🔴 Rojo | Crítico |
| 2.0 - 3.4 | 🟡 Amarillo | En desarrollo |
| 3.5 - 5.0 | 🟢 Verde | Óptimo |

## 🛠️ Tecnologías

**Backend:**
- FastAPI
- SQLAlchemy + SQLite
- JWT (python-jose)
- WeasyPrint (PDF)

**Frontend:**
- React 18 + Vite
- React Router
- Chart.js
- Axios

---

Desarrollado para la evaluación de Funciones Esenciales de Salud Pública.
