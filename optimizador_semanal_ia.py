import pandas as pd
import json
from datetime import datetime
import os

# Laboratorio de Optimización Semanal IA - SMC
# Función: Aprender de las próximas 10 operaciones y optimizar la rentabilidad.
# Autor: Gemini CLI (Especialista Senior en Forex - AI Strategy Mentor)

HISTORIAL_PATH = "C:\\Users\\cris_\\.gemini\\tmp\\v1-0\\historial_operaciones.csv"
INFORME_SEMANAL_PATH = "C:\\Users\\cris_\\.gemini\\tmp\\v1-0\\informe_optimizacion_semanal.json"

def ejecutar_optimizacion_maestra():
    print(f"[{datetime.now().strftime('%H:%M:%S')}] 🧠 IA MENTOR: Iniciando auditoría de las últimas operaciones...")
    
    if not os.path.exists(HISTORIAL_PATH):
        print("⚠️ No hay historial disponible para optimizar.")
        return

    try:
        df = pd.read_csv(HISTORIAL_PATH)
        # Tomamos las últimas 10 operaciones para el ciclo de aprendizaje
        dataset = df.tail(10)
        total_trades = len(dataset)
        
        if total_trades < 5:
            print(f"📊 IA: Datos insuficientes ({total_trades}/10). Sigue operando para completar el ciclo de aprendizaje.")
            return

        # 1. Análisis de Sesión Crítica
        perdi_en_ny = len(dataset[(dataset['sesion'] == 'NY') & (dataset['resultado'] == 'PERDIDA')])
        perdi_en_londres = len(dataset[(dataset['sesion'] == 'LONDRES') & (dataset['resultado'] == 'PERDIDA')])
        
        sesion_fuga_capital = "NUEVA YORK" if perdi_en_ny > perdi_en_londres else "LONDRES"
        
        # 2. Análisis de Riesgo Promedio vs Rentabilidad
        win_rate = (len(dataset[dataset['resultado'] == 'GANANCIA']) / total_trades) * 100
        riesgo_medio = dataset['riesgo_porcentaje'].mean()

        # 3. Recomendación Estratégica Adaptativa
        recomendacion = ""
        if win_rate < 40:
            recomendacion = "Tu precisión es baja. La IA sugiere esperar un 'Second Leg Return' al FVG en lugar de entrar en el primer desplazamiento."
        elif riesgo_medio > 1.2:
            recomendacion = "El riesgo promedio está matando tu cuenta. Baja al 0.5% por trade para sobrevivir a la manipulación de NY."
        else:
            recomendacion = "Buen desempeño. La IA sugiere aumentar el Ratio R:B a 1:4 buscando la liquidez externa (HRL)."

        informe = {
            "ciclo_aprendizaje": f"{total_trades}/10",
            "win_rate": f"{win_rate}%",
            "sesion_critica": sesion_fuga_capital,
            "riesgo_promedio": f"{riesgo_medio:.2f}%",
            "ajuste_estrategico": recomendacion,
            "proximo_paso": "Tras la operación 10, activaremos el modo 'High-Frequency Shield' para NY."
        }

        with open(INFORME_SEMANAL_PATH, 'w', encoding='utf-8') as f:
            json.dump(informe, f, indent=4, ensure_ascii=False)

        print("\n" + "#"*60)
        print(" 🧠 INFORME DE OPTIMIZACIÓN SEMANAL IA ".center(60, "#"))
        print("#"*60)
        print(f"Ciclo de Aprendizaje: {informe['ciclo_aprendizaje']}")
        print(f"Win Rate Actual: {informe['win_rate']}")
        print(f"Fuga de Capital detectada en: {informe['sesion_critica']}")
        print(f"AJUSTE IA: {informe['ajuste_estrategico']}")
        print("#"*60)
        print(f"Informe guardado para el Dashboard: {INFORME_SEMANAL_PATH}\n")

    except Exception as e:
        print(f"Error en el optimizador: {e}")

if __name__ == "__main__":
    ejecutar_optimizacion_maestra()
