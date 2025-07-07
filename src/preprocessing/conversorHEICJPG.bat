@echo off
setlocal enabledelayedexpansion

REM 🗂 Cambia estas rutas según tus carpetas
set ORIGEN=C:\Users\Administrador\Downloads\Imagenes
set DESTINO=C:\Users\Administrador\Downloads\Imagenes_jpg

REM 🔧 Crea carpeta destino si no existe
if not exist "%DESTINO%" (
    mkdir "%DESTINO%"
)

echo Convirtiendo archivos .HEIC de %ORIGEN% a .JPG en %DESTINO%...

for %%F in ("%ORIGEN%\*.heic") do (
    set "archivo=%%~nF"
    echo Procesando: !archivo!.heic
    magick "%%F" "%DESTINO%\!archivo!.jpg"
)

echo.
echo DONE ¡Conversión completada sin perder metadatos!
pause
