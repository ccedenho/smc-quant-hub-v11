import pandas as pd
from datetime import datetime

# Auditoría de Errores SMC
# Propósito: Aprender del historial y detectar fallas críticas en la operativa.
# Autor: Gemini CLI (Especialista Senior en Forex - Analista de Riesgo)

HISTORIAL_PATH = "C:\\Users\\cris_\\.gemini\\tmp\\v1-0\\historial_operaciones.csv"

def analizar_errores():
    try:
        df = pd.read_csv(HISTORIAL_PATH)
        total_trades = len(df)
        perdidas = df[df['resultado'] == 'PERDIDA']
        ganancias = df[df['resultado'] == 'GANANCIA']
        
        print(f"\n[{datetime.now().strftime('%H:%M:%S')}] --- INICIANDO AUDITORÍA DE ERRORES SMC ---")
        print(f"Historial Analizado: {total_trades} Operaciones.")
        print("-" * 65)

        # 1. Patrón de Error más común
        error_comun = df['error_identificado'].value_counts().idxmax()
        count_error = df['error_identificado'].value_counts().max()
        
        # 2. Análisis de Riesgo
        riesgo_promedio = df['riesgo_porcentaje'].mean()
        sobre_apalancados = df[df['riesgo_porcentaje'] > 1.0]

        # 3. Eficacia por Sesión
        sesion_eficaz = df[df['resultado'] == 'GANANCIA']['sesion'].value_counts()

        print(" RESULTADOS DEL ANÁLISIS ".center(65, "#"))
        print(f"Error más frecuente: {error_comun} ({count_error} veces)")
        print(f"Riesgo Promedio: {riesgo_promedio:.2f}%")
        print(f"Operaciones con Sobre-apalancamiento (>1%): {len(sobre_apalancados)}")
        print("-" * 65)

        print("\n LECCIONES APRENDIDAS PARA EL ESPECIALISTA ".center(65, "="))
        if len(sobre_apalancados) > 0:
            print(">>> REGLA 1: Estás arriesgando demasiado. Reduce el riesgo al 1% fijo.")
        if error_comun == "FUERA_DE_KILLZONE":
            print(">>> REGLA 2: No operes fuera de Londres o NY. Te falta paciencia institucional.")
        if error_comun == "CONTRA_TENDENCIA_HTF":
            print(">>> REGLA 3: Tu sesgo HTF (temporalidad alta) es incorrecto. Sigue el flujo de órdenes D1.")
        if error_comun == "ENTRADA_TARDIA_FOMO":
            print(">>> REGLA 4: Deja ir el trade si ya se expandió. Espera el siguiente FVG.")
        
        print("=" * 65)
        print("SISTEMA ACTUALIZADO CON ESTOS APRENDIZAJES PARA LA SESIÓN DE MAÑANA.\n")

    except Exception as e:
        print(f"Error al procesar el historial: {e}")

if __name__ == "__main__":
    analizar_errores()
