@echo off
cd /d "%~dp0"
echo.
echo  ╔══════════════════════════════════════════════╗
echo  ║   Oxuma — Subiendo cambios a GitHub...       ║
echo  ╚══════════════════════════════════════════════╝
echo.
git add -A
git status
git commit -m "v1.4: Login/roles, mapa clientes, asistente IA mejorado, precio_costo admin"
git push origin main
echo.
echo  Listo! Ahora en PythonAnywhere:
echo.
echo  1. Abrí: https://www.pythonanywhere.com/user/kollmann/consoles/
echo  2. Consola Bash ^> pega:
echo     cd ~/oxuma-app/oxuma-app ^&^& git pull origin main
echo  3. Volvé a Webapps y hacé Reload
echo.
pause
