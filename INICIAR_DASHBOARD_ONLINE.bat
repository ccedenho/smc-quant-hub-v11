@echo off
title SMC QUANT HUB v11.2 - ACTIVACION PRO
echo ==========================================
echo    SMC QUANT HUB v11.2 - ONLINE MODE
echo ==========================================
cd /d "%~dp0"
echo Iniciando Cerebro Quant...
start http://localhost:8000
python cerebro_segundo_plano.py
if %ERRORLEVEL% NEQ 0 (
    echo Error detectado. Intentando ruta alternativa...
    C:\Users\cris_\AppData\Local\Microsoft\WindowsApps\python.exe cerebro_segundo_plano.py
)
pause
