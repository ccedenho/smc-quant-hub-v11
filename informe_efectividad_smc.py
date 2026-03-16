import json
from datetime import datetime
import os

# Analista Post-Simulación de Noticias SMC
# Función: Evaluar la efectividad del movimiento institucional (XAU/USD)
# Autor: Gemini CLI (Especialista Senior en Forex - NY Data Analyst)

INFORME_PATH = "C:\\Users\\cris_\\.gemini\\tmp\\v1-0\\informe_post_noticia.json"

def generar_informe_post_noticia(datos_simulacion):
    """
    Analiza los datos de la simulación y genera un informe estructurado en JSON y Texto.
    """
    precio_apertura = datos_simulacion.get('apertura', 5020.00)
    minimo_alcanzado = datos_simulacion.get('minimo', 4992.40)
    maximo_final = datos_simulacion.get('maximo', 5140.00)
    nivel_liquidez = datos_simulacion.get('nivel_liquidez', 5000.00)
    
    # 1. Cálculo de Barrido (Liquidity Sweep Depth)
    profundidad_barrido = round(nivel_liquidez - minimo_alcanzado, 2)
    es_barrido_valido = profundidad_barrido > 0
    
    # 2. Cálculo de Expansión (Expansion Strength)
    expansion_total = round(maximo_final - minimo_alcanzado, 2)
    displacement_ratio = round(expansion_total / (precio_apertura - minimo_alcanzado), 2)
    
    # 3. Puntuación de Calidad Institucional (0-100)
    score_institucional = 0
    if es_barrido_valido: score_institucional += 40
    if displacement_ratio >= 2.0: score_institucional += 30
    if expansion_total > 100: score_institucional += 30
    
    informe = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "evento": "Simulación Post-Noticia CPI/NFP",
        "activo": "XAU/USD (Oro)",
        "metricas": {
            "profundidad_barrido": f"${profundidad_barrido}",
            "expansion_total": f"${expansion_total}",
            "displacement_ratio": displacement_ratio,
            "calidad_institucional_score": f"{score_institucional}%"
        },
        "analisis_especialista": (
            "Movimiento institucional clásico (Judas Swing) detectado. "
            "El barrido de liquidez bajo $5,000 activó las órdenes de compra de los bancos. "
            "La expansión posterior confirma un desplazamiento (displacement) de alta calidad."
        ) if score_institucional > 80 else "Movimiento de baja confluencia. Posible manipulación extendida."
    }

    # Guardar en JSON para integración con el Dashboard
    with open(INFORME_PATH, 'w', encoding='utf-8') as f:
        json.dump(informe, f, indent=4, ensure_ascii=False)

    # Imprimir resumen profesional en consola
    print("\n" + "="*60)
    print(" INFORME DE EFECTIVIDAD INSTITUCIONAL (SMC) ".center(60, "#"))
    print("="*60)
    print(f"Evento: {informe['evento']}")
    print(f"Activo: {informe['activo']}")
    print("-" * 60)
    print(f"Barrido bajo Liquidez ($5,000): ${profundidad_barrido}")
    print(f"Fuerza de Expansión: ${expansion_total}")
    print(f"Ratio de Desplazamiento: {displacement_ratio}x")
    print(f"CALIDAD INSTITUCIONAL: {informe['metricas']['calidad_institucional_score']}")
    print("-" * 60)
    print(f"NOTAS: {informe['analisis_especialista']}")
    print("="*60)
    print(f"Informe guardado en: {INFORME_PATH}\n")

if __name__ == "__main__":
    # Datos de ejemplo de la última simulación exitosa
    datos_ejemplo = {
        'apertura': 5020.00,
        'minimo': 4992.40,
        'maximo': 5140.00,
        'nivel_liquidez': 5000.00
    }
    generar_informe_post_noticia(datos_ejemplo)
