@echo off
title FESP Diagnostic App - Iniciando...
color 0A

echo =============================================
echo    FESP DIAGNOSTIC APP - INICIO AUTOMATICO
echo =============================================
echo.

cd /d "%~dp0"

echo [1/4] Verificando entorno virtual...
if not exist "backend\venv" (
    echo      Creando entorno virtual...
    cd backend
    python -m venv venv
    cd ..
)

echo [2/4] Iniciando Backend (FastAPI)...
start "FESP Backend" cmd /k "cd /d %~dp0backend && venv\Scripts\activate && uvicorn app.main:app --reload"

echo      Esperando que el backend inicie...
timeout /t 5 /nobreak > nul

echo [3/4] Iniciando Frontend (React)...
start "FESP Frontend" cmd /k "cd /d %~dp0frontend && npm run dev"

echo      Esperando que el frontend inicie...
timeout /t 5 /nobreak > nul

echo [4/4] Abriendo navegador...
timeout /t 3 /nobreak > nul
start http://localhost:5173

echo.
echo =============================================
echo    APP INICIADA CORRECTAMENTE
echo =============================================
echo.
echo    Frontend: http://localhost:5173
echo    Backend:  http://localhost:8000/docs
echo.
echo    Usuario: admin@fesp.gob.mx
echo    Clave:   admin123
echo.
echo    Para cerrar, cierra las ventanas de terminal.
echo =============================================
echo.
pause
