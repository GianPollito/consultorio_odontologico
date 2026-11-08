@echo off
chcp 65001 > nul
title Sistema de Gestión - Consultorio Odontológico "Sonrisa Perfecta"
echo ======================================================================
echo    CLÍNICA ODONTOLÓGICA "SONRISA PERFECTA" - INICIANDO SISTEMA
echo ======================================================================
echo.
echo Verificando base de datos MariaDB en puerto 3307...
python -c "import socket; s = socket.socket(); res = s.connect_ex(('127.0.0.1', 3307)); s.close(); exit(0 if res == 0 else 1)"
if %errorlevel% neq 0 (
    echo [ADVERTENCIA] MariaDB no responde en el puerto 3307. Asegúrese de que el servicio esté iniciado.
) else (
    echo [OK] Conexión detectada en MariaDB puerto 3307.
)

echo.
echo Verificando puerto HTTP para el servidor Django...
set PORT=8000
python -c "import socket; s = socket.socket(); res = s.connect_ex(('127.0.0.1', 8000)); s.close(); exit(0 if res == 0 else 1)"
if %errorlevel% equ 0 (
    echo [AVISO] El puerto 8000 está ocupado por otro de sus proyectos. Probando puerto 8088...
    set PORT=8088
)

echo Iniciando servidor en: http://127.0.0.1:%PORT%/
echo Usuario administrador inicial: admin
echo Contraseña inicial: admin123
echo.
echo Presione Ctrl+C en cualquier momento para detener el servidor.
echo ======================================================================
python manage.py runserver 127.0.0.1:%PORT%
pause
