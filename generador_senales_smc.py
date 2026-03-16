import json
from datetime import datetime
import os

# Generador de Señales SCALPING NY (Controlado por IA)
# Función: Crear señales adaptativas basadas en el aprendizaje de la IA.

SIGNALS_PATH = "C:\\Users\\cris_\\.gemini\\tmp\\v1-0\\senales_activas.json"
CONFIG_IA_PATH = "C:\\Users\\cris_\\.gemini\\tmp\\v1-0\\ia_config_dinamica.json"

def generar_senal_ia(par, operacion, entrada_base, sl_base, tp_base, razon_tecnica):
    print(f"\n[{datetime.now().strftime('%H:%M:%S')}] 🤖 GENERANDO SEÑAL DE SCALPING NY CON IA...")
    
    # 1. Cargar el Cerebro de la IA
    config_ia = {"buffer_manipulacion_oro": 1.5, "filtro_fomo_activo": False}
    if os.path.exists(CONFIG_IA_PATH):
        with open(CONFIG_IA_PATH, 'r') as f:
            config_ia = json.load(f)
            
    # 2. Aplicar Adaptaciones de la IA (Tolerancia a Manipulación)
    entrada_final = entrada_base
    sl_final = sl_base
    
    if par == "XAU/USD":
        buffer = config_ia.get("buffer_manipulacion_oro", 1.5)
        if operacion == "COMPRA":
            sl_final = sl_base - buffer # Aleja el SL para evitar que una mecha institucional lo toque
            if config_ia.get("filtro_fomo_activo"):
                entrada_final = entrada_base - 1.0 # Exige un descuento extra para entrar
        else:
            sl_final = sl_base + buffer
            if config_ia.get("filtro_fomo_activo"):
                entrada_final = entrada_base + 1.0

    # 3. Cálculo de Ratio
    riesgo = abs(entrada_final - sl_final)
    beneficio = abs(tp_base - entrada_final)
    ratio = round(beneficio / riesgo, 2)
    
    razon_ia = razon_tecnica + f" | 🧠 [IA Ajuste: SL expandido ${buffer} para absorber volatilidad]"

    senal = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "par": par.upper(),
        "operacion": f"SCALP {operacion.upper()}",
        "entrada": f"${entrada_final:.2f}",
        "sl": f"${sl_final:.2f}",
        "tp": f"${tp_base:.2f}",
        "razon_smc": razon_ia,
        "riesgo_beneficio": f"1:{ratio}"
    }

    # 4. Guardar Señal
    try:
        senales = []
        if os.path.exists(SIGNALS_PATH):
            with open(SIGNALS_PATH, 'r', encoding='utf-8') as f:
                senales = json.load(f)
        
        senales.insert(0, senal)
        senales = senales[:5]
        
        with open(SIGNALS_PATH, 'w', encoding='utf-8') as f:
            json.dump(senales, f, indent=4, ensure_ascii=False)
            
        print(f"✅ Señal Optimizada por IA Guardada. Ratio: 1:{ratio}")
        print(f"🛡️ Tolerancia a Manipulación Aplicada: SL ajustado a {senal['sl']}")

    except Exception as e:
        print(f"Error al guardar señal: {e}")

if __name__ == "__main__":
    # Generar señal de prueba con IA
    generar_senal_ia("XAU/USD", "COMPRA", 4995.00, 4985.00, 5020.00, "Sweep M15 + BOS")
