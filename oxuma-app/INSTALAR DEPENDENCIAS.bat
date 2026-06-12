@echo off
echo  Instalando dependencias de Oxuma...
echo.
py -m pip install flask openpyxl
if errorlevel 1 (
    python -m pip install flask openpyxl
)
echo.
echo  Listo. Ya podés usar "INICIAR APP.bat"
pause
