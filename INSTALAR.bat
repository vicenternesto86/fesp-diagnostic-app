@echo off
echo Instalando dependencias de FESP Diagnostic App...
echo.

cd /d "%~dp0"

echo [1/3] Creando entorno virtual Python...
cd backend
python -m venv venv
call venv\Scripts\activate

echo [2/3] Instalando dependencias del backend...
pip install -r requirements.txt

echo [3/3] Cargando datos de prueba...
python seed_data.py

cd ..

echo.
echo [4/4] Instalando dependencias del frontend...
cd frontend
call npm install

echo.
echo =============================================
echo    INSTALACION COMPLETADA
echo =============================================
echo.
echo    Ahora puedes ejecutar INICIAR_APP.bat
echo    para iniciar la aplicacion.
echo.
pause
