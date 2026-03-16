import json
import pandas as pd
import os
from datetime import datetime

# Motor de Inteligencia Artificial SMC (Aprendizaje de Errores)
# Propósito: Ajustar dinámicamente los parámetros de las señales de Scalping en NY
# para tolerar manipulación (Stop Hunts) y reducir el margen de pérdida.

HISTORIAL_PATH = "C:\\Users\\cris_\\.gemini\\tmp\\v1-0\\historial_operaciones.csv"
CONFIG_IA_PATH = "C:\\Users\\cris_\\.gemini\\tmp\\v1-0\\ia_config_dinamica.json"

def analizar_y_aprender():
    print(f"[{datetime.now().strftime('%H:%M:%S')}] 🧠 IA MOTOR: Analizando historial y patrones de manipulación...")
    
    # Parámetros base por defecto
    config_ia = {
        "buffer_manipulacion_oro": 1.5, # $1.5 extra al SL para evitar Stop Hunts
        "buffer_manipulacion_euro": 0.0005,
        "filtro_fomo_activo": False,
        "riesgo_maximo_permitido": 1.0,
        "ratio_rb_minimo": 3.0,
        "estado_mercado": "NORMAL"
    }

    try:
        if os.path.exists(HISTORIAL_PATH):
            df = pd.read_csv(HISTORIAL_PATH)
            
            # Análisis de los últimos 5 trades para adaptación a corto plazo
            ultimos_trades = df.tail(5)
            perdidas = ultimos_trades[ultimos_trades['resultado'] == 'PERDIDA']
            
            # 1. Tolerancia a Manipulación (Si hay muchas pérdidas seguidas, el mercado está errático)
            if len(perdidas) >= 2:
                print("🧠 IA: Volatilidad alta detectada. Aumentando Buffer de Manipulación (Stop Loss más holgado).")
                config_ia["buffer_manipulacion_oro"] = 3.5 # Ampliamos SL para tolerar mechas de manipulación
                config_ia["estado_mercado"] = "ALTA_MANIPULACION"
                config_ia["ratio_rb_minimo"] = 2.0 # Ajustamos el RR mínimo por el SL más amplio
                
            # 2. Corrección de FOMO (Entradas tempranas)
            errores_fomo = len(ultimos_trades[ultimos_trades['error_identificado'] == 'ENTRADA_TARDIA_FOMO'])
            if errores_fomo > 0:
                print("🧠 IA: Patrón FOMO detectado. Activando Filtro OTE (Optimal Trade Entry) obligatorio.")
                config_ia["filtro_fomo_activo"] = True
                
            # 3. Castigo por Sobre-Apalancamiento
            if ultimos_trades['riesgo_porcentaje'].mean() > 1.0:
                print("🧠 IA: Violación de riesgo detectada. Forzando reducción de tamaño de lote.")
                config_ia["riesgo_maximo_permitido"] = 0.5 # Corta el riesgo a la mitad para proteger capital

        # Guardar el "Cerebro" actualizado
        with open(CONFIG_IA_PATH, 'w', encoding='utf-8') as f:
            json.dump(config_ia, f, indent=4)
            
        print("🧠 IA: Aprendizaje completado. Parámetros de Scalping NY calibrados y guardados.")
        
    except Exception as e:
        print(f"Error en el motor de IA: {e}")

if __name__ == "__main__":
    analizar_y_aprender()
