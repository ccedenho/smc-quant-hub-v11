import time
import winsound
from datetime import datetime
import random

# Automatización de Alerta Institucional SMC - ENFOQUE MULTI-ACTIVO (DXY + ORO)
# Niveles de Alerta: DXY @ 100.42 (Resistencia) | XAU/USD @ $5,000.00 (Soporte)
# Autor: Gemini CLI (Especialista Senior en Forex - NY Focus)

# Niveles Institucionales
DXY_RESISTENCIA = 100.42
ORO_SOPORTE = 5000.00

# Killzones de Nueva York (EST)
NY_AM_INICIO = 8
NY_AM_FIN = 11

def alerta_oro():
    """Alerta grave para el barrido de liquidez del Oro"""
    for _ in range(3):
        winsound.Beep(1000, 500)
        winsound.Beep(1500, 300)

def alerta_dxy():
    """Alerta aguda para la resistencia crítica del Dólar (DXY)"""
    for _ in range(5):
        winsound.Beep(3000, 150)
        winsound.Beep(2500, 150)

def es_killzone_ny():
    ahora = datetime.now().hour
    return NY_AM_INICIO <= ahora < NY_AM_FIN

def monitorear_maestro():
    print(f"[{datetime.now().strftime('%H:%M:%S')}] CENTINELA INSTITUCIONAL SMC ACTIVADO...")
    print(f"Monitoreando DXY en {DXY_RESISTENCIA} | XAU/USD en ${ORO_SOPORTE}")
    print(f"Especialización: Divergencia SMT (DXY vs EUR/XAU)")
    print("-" * 65)

    try:
        while True:
            # Simulación de volatilidad correlacionada
            dxy_simulado = round(100.36 + random.uniform(-0.15, 0.15), 2)
            oro_simulado = round(5015.00 + random.uniform(-30, 15), 2)
            
            # Lógica de Alerta DXY
            if dxy_simulado >= DXY_RESISTENCIA:
                print(f"\033[93m[{datetime.now().strftime('%H:%M:%S')}] ¡ALERTA DXY! RESISTENCIA TOCADA: {dxy_simulado}\033[0m")
                if es_killzone_ny():
                    print("\033[92m[SMT] DXY EN TECHO. BUSCA RECHAZO PARA LARGOS EN ORO/EURO.\033[0m")
                    alerta_dxy()
                time.sleep(10)

            # Lógica de Alerta Oro
            if oro_simulado <= ORO_SOPORTE + 1.5:
                print(f"\033[91m[{datetime.now().strftime('%H:%M:%S')}] ¡ALERTA ORO! ZONA DE BARRIDO: ${oro_simulado}\033[0m")
                if es_killzone_ny():
                    print("\033[92m[NY OPEN] BARRIDO DE LIQUIDEZ SSL. PREPARA EJECUCIÓN.\033[0m")
                    alerta_oro()
                time.sleep(10)
            
            time.sleep(1.5)

    except KeyboardInterrupt:
        print("\n[INFO] Centinela desactivado.")

if __name__ == "__main__":
    monitorear_maestro()
