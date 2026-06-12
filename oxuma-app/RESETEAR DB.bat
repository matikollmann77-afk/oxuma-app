@echo off
echo.
echo  ==========================================
echo   OXUMA - Resetear base de datos
echo  ==========================================
echo.
echo  Esto borra la base de datos actual y la
echo  vuelve a crear con todos los precios
echo  individuales de cada producto.
echo.
echo  Presiona cualquier tecla para continuar...
echo  (o cierra esta ventana para cancelar)
pause > nul

cd /d "%~dp0"

if exist oxuma.db (
    del oxuma.db
    echo  Base de datos borrada.
)

echo.
echo  Iniciando la app (va a recrear la base)...
echo.
start "" "http://localhost:5000"
py app.py
pause
