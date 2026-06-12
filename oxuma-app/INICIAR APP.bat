@echo off
cd /d "%~dp0"
echo.
echo  ==========================================
echo   OXUMA DISTRIBUIDORA - Sistema de Gestion
echo  ==========================================
echo.

echo  Verificando dependencias...
py -m pip install flask openpyxl --quiet --disable-pip-version-check 2>nul
if errorlevel 1 (
    echo  [!] Error instalando dependencias. Intentando con pip...
    pip install flask openpyxl --quiet 2>nul
)
echo  Dependencias OK
echo.
echo  Iniciando el sistema en http://localhost:5000
echo  (Cerrá esta ventana para detener el servidor)
echo.
start "" "http://localhost:5000"
py app.py
if errorlevel 1 (
    echo.
    echo  [ERROR] No se pudo iniciar. Intentando con python...
    python app.py
)
pause
