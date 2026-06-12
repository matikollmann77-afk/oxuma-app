@echo off
echo.
echo  ==========================================
echo   OXUMA - Copiando assets de marca
echo  ==========================================
echo.

set SRC=C:\Users\usuario\Downloads\OXUMA
set DEST=C:\Users\usuario\OneDrive\oxuma-app\brand
set STATIC=C:\Users\usuario\OneDrive\oxuma-app\static

:: Crear carpeta brand
if not exist "%DEST%" mkdir "%DEST%"
if not exist "%STATIC%\img" mkdir "%STATIC%\img"

:: Copiar PDFs de marca
echo  Copiando documentos de marca...
xcopy /Y "%SRC%\Estrategia y dirección creativa - Oxuma.pdf" "%DEST%\" 2>nul
xcopy /Y "%SRC%\Manual de marca - Oxuma.pdf" "%DEST%\" 2>nul
xcopy /Y "%SRC%\Presentación de marca - Oxuma.pdf" "%DEST%\" 2>nul

:: Copiar ZIPs con gráficos y logos
echo  Copiando elementos gráficos...
for %%f in ("%SRC%\Elementos gráficos*.zip") do xcopy /Y "%%f" "%DEST%\" 2>nul
for %%f in ("%SRC%\Signo de identidad*.zip") do xcopy /Y "%%f" "%DEST%\" 2>nul

:: Copiar logos PNG desde Downloads directamente
echo  Copiando logos...
xcopy /Y "C:\Users\usuario\Downloads\Logotipo con bajada - Blanco.png" "%STATIC%\img\" 2>nul
xcopy /Y "C:\Users\usuario\Downloads\Logotipo con bajada - Negro.png" "%STATIC%\img\" 2>nul

:: Extraer ZIPs si existen
echo  Extrayendo archivos ZIP...
for %%f in ("%DEST%\*.zip") do (
    powershell -Command "Expand-Archive -Path '%%f' -DestinationPath '%STATIC%\img' -Force" 2>nul
)

echo.
echo  ==========================================
echo   Listo! Assets copiados a:
echo   - %DEST%
echo   - %STATIC%\img
echo  ==========================================
echo.
pause
