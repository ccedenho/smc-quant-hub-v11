import time
import os
from http.server import HTTPServer, BaseHTTPRequestHandler
import threading
import json
import random
from datetime import datetime

# =================================================================
# SMC QUANTITATIVE HUB - CORE ENGINE v6.5 (INTERACTIVE CHART MODE)
# Architect: Gemini CLI (Senior Specialist)
# =================================================================

PORT = 8080

class MarketSimulator:
    def __init__(self):
        # Estado inicial base
        self.state = {
            "oro": {"precio": 5132.80, "entrada": 5012.00, "sl": 5120.00, "tp": 5150.00, "tendencia": "BULLISH EXPANSION", "color": "#00ff41", "symbol": "FX_IDC:XAUUSD"},
            "dxy": {"precio": 99.32, "entrada": 100.42, "sl": 99.60, "tp": 99.00, "tendencia": "BEARISH BREAKOUT", "color": "#ff3131", "symbol": "CAPITALCOM:DXY"},
            "eur": {"precio": 1.1492, "entrada": 1.1405, "sl": 1.1440, "tp": 1.1550, "tendencia": "BULLISH CORRELATION", "color": "#00ff41", "symbol": "FX:EURUSD"}
        }
        self.lock = threading.Lock()

    def update_prices(self):
        """Simula la volatilidad del mercado SMC (Smart Money Concepts)"""
        while True:
            with self.lock:
                # Volatilidad direccional SMC (Oro empujando a TP, DXY cayendo)
                self.state["oro"]["precio"] += random.uniform(-0.3, 0.8)  # Sesgo alcista NY Session
                self.state["dxy"]["precio"] += random.uniform(-0.015, 0.005) # Sesgo bajista
                self.state["eur"]["precio"] += random.uniform(-0.0001, 0.0003)

                # Evitar que los precios crucen TPs o SLs de manera abrupta en la simulación
                self.state["oro"]["precio"] = min(self.state["oro"]["precio"], 5150.00) 
                self.state["dxy"]["precio"] = max(self.state["dxy"]["precio"], 99.00)
                
            time.sleep(2) # Actualización interna cada 2 segundos

    def get_data(self):
        with self.lock:
            data = {"timestamp": datetime.now().strftime("%H:%M:%S"), "activos": []}
            for key, val in self.state.items():
                rango = val["tp"] - val["sl"]
                if val["nombre_display"] == "DXY (DÓLAR INDEX)": # Invertir para DXY
                   rango = val["sl"] - val["tp"]
                   progreso = ((val["sl"] - val["precio"]) / (rango if rango != 0 else 1)) * 100
                else:
                   progreso = ((val["precio"] - val["sl"]) / (rango if rango != 0 else 1)) * 100
                
                # Diferenciar PNL por activo
                mult = 1 if key == "oro" else (10 if key == "dxy" else 10000)
                pnl = abs(val["precio"] - val["entrada"]) * mult if (val["precio"] > val["entrada"] if key != "dxy" else val["precio"] < val["entrada"]) else -abs(val["precio"] - val["entrada"]) * mult
                
                data["activos"].append({
                    "nombre": val["nombre_display"], "precio": round(val["precio"], 4 if key == "eur" else 2),
                    "tendencia": val["tendencia"], "entrada": val["entrada"],
                    "sl": val["sl"], "tp": val["tp"], "symbol": val["symbol"],
                    "pnl": f"{'+' if pnl >= 0 else ''}{round(pnl, 2)}", "color": val["color"], "progreso": max(0, min(100, progreso))
                })
            return data

# Nombres legibles para el simulador
simulator = MarketSimulator()
simulator.state["oro"]["nombre_display"] = "XAU/USD (ORO)"
simulator.state["dxy"]["nombre_display"] = "DXY (DÓLAR INDEX)"
simulator.state["eur"]["nombre_display"] = "EUR/USD (EURO)"

class DashboardHandler(BaseHTTPRequestHandler):
    def log_message(self, format, *args): pass
        
    def do_GET(self):
        if self.path == '/':
            self.send_response(200)
            self.send_header('Content-type', 'text/html; charset=utf-8')
            self.end_headers()
            data = simulator.get_data()
            
            rows, charts = "", ""
            for a in data['activos']:
                rows += f"""
                <tr class="hover-row">
                    <td style="color:{a['color']}; font-weight:800;">{a['nombre']}</td>
                    <td style="font-size:20px; font-weight:bold; color:#fff;">${a['precio']}</td>
                    <td><span class="trend-badge">{a['tendencia']}</span></td>
                    <td style="color:#2962ff;">${a['entrada']}</td>
                    <td style="color:#f23645;">${a['sl']}</td>
                    <td style="color:#089981;">${a['tp']}</td>
                    <td style="color:#ffd700; font-weight:bold;">{a['pnl']}</td>
                </tr>
                """
                
                charts += f"""
                <div class="chart-card">
                    <div class="chart-header">
                        <span>MAPA INTERACTIVO {a['nombre']}</span>
                        <span class="status-live">● LIVE</span>
                    </div>
                    <!-- TradingView Widget BEGIN -->
                    <div class="tradingview-widget-container" style="height:400px; width:100%;">
                        <div id="tradingview_{a['symbol'].replace(':','_')}" style="height:100%;"></div>
                        <script type="text/javascript" src="https://s3.tradingview.com/tv.js"></script>
                        <script type="text/javascript">
                        new TradingView.widget({{
                          "autosize": true,
                          "symbol": "{a['symbol']}",
                          "interval": "15",
                          "timezone": "Etc/UTC",
                          "theme": "dark",
                          "style": "1",
                          "locale": "es",
                          "toolbar_bg": "#f1f3f6",
                          "enable_publishing": false,
                          "hide_side_toolbar": false,
                          "allow_symbol_change": true,
                          "container_id": "tradingview_{a['symbol'].replace(':','_')}"
                        }});
                        </script>
                    </div>
                    <!-- TradingView Widget END -->
                    <div class="progress-container">
                        <div class="map-label">PROGRESO SMC: {round(a['progreso'], 1)}%</div>
                        <div class="progress-bar-bg">
                            <div class="progress-fill" style="width:{a['progreso']}%"></div>
                        </div>
                    </div>
                </div>
                """

            html = f"""
            <!DOCTYPE html>
            <html lang="es">
            <head>
                <meta charset="UTF-8">
                <title>SMC QUANT HUB v6.5 - CHART MODE</title>
                <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800&family=JetBrains+Mono:wght@400;700&display=swap" rel="stylesheet">
                <style>
                    :root {{ --bg: #050608; --card: #11141a; --border: #1e222d; --green: #089981; --red: #f23645; --gold: #ffd700; }}
                    body {{ font-family: 'Inter', sans-serif; background-color: var(--bg); color: #d1d4dc; margin: 0; padding: 20px; }}
                    .container {{ max-width: 1600px; margin: auto; }}
                    header {{ display: flex; justify-content: space-between; border-bottom: 1px solid var(--border); padding: 10px 0; margin-bottom: 20px; }}
                    .title {{ font-weight: 800; font-size: 20px; color: var(--gold); }}
                    .matrix-card {{ background: var(--card); border: 1px solid var(--border); border-radius: 12px; padding: 20px; margin-bottom: 30px; }}
                    table {{ width: 100%; border-collapse: collapse; }}
                    th {{ text-align: left; color: #848e9c; font-size: 11px; text-transform: uppercase; padding: 10px; border-bottom: 1px solid var(--border); }}
                    td {{ padding: 15px 10px; border-bottom: 1px solid #1e222d; }}
                    .trend-badge {{ background: rgba(8,153,129,0.1); color: var(--green); padding: 4px 8px; border-radius: 4px; font-size: 11px; font-weight: bold; }}
                    
                    /* Charts Layout */
                    .charts-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(500px, 1fr)); gap: 20px; }}
                    .chart-card {{ background: var(--card); border: 1px solid var(--border); border-radius: 12px; overflow: hidden; }}
                    .chart-header {{ padding: 15px; background: #1a1e26; display: flex; justify-content: space-between; font-weight: bold; font-size: 12px; border-bottom: 1px solid var(--border); }}
                    .status-live {{ color: var(--green); animation: pulse 2s infinite; }}
                    @keyframes pulse {{ 0% {{ opacity: 1; }} 50% {{ opacity: 0.4; }} 100% {{ opacity: 1; }} }}
                    
                    /* Progress Styles */
                    .progress-container {{ padding: 15px; background: #0c0e12; }}
                    .map-label {{ font-size: 10px; color: #848e9c; margin-bottom: 8px; text-transform: uppercase; }}
                    .progress-bar-bg {{ height: 8px; background: #2a2e39; border-radius: 4px; overflow: hidden; }}
                    .progress-fill {{ height: 100%; background: linear-gradient(90deg, var(--red), var(--green)); transition: width 1s; }}
                </style>
            </head>
            <body>
                <div class="container">
                    <header>
                        <div class="title">SMC QUANTITATIVE HUB v6.5</div>
                        <div style="font-family:'JetBrains Mono'; font-size:12px; color:var(--green);">TERMINAL NYC: {data['timestamp']}</div>
                    </header>
                    
                    <div class="matrix-card">
                        <table id="price-table">
                            <thead>
                                <tr><th>Activo</th><th>Precio</th><th>Estado SMC</th><th>Entry</th><th>Stop Loss</th><th>Take Profit</th><th>PnL Total</th></tr>
                            </thead>
                            <tbody>{rows}</tbody>
                        </table>
                    </div>

                    <div class="charts-grid">{charts}</div>

                    <footer style="text-align:center; padding:40px; color:#50535e; font-size:11px;">
                        PLATAFORMA AUTÓNOMA SMC | INTERFACE PRO v6.5 | GEMINI CLI SENIOR QUANT
                    </footer>
                </div>
                <script>
                    // Auto-refresh data every 5 seconds without full page reload for widgets
                    setInterval(() => {{
                        location.reload(); 
                    }}, 10000); // Recarga completa cada 10s para actualizar widgets y precios
                </script>
            </body>
            </html>
            """
            self.wfile.write(html.encode('utf-8'))

def run_server():
    server = HTTPServer(('localhost', PORT), DashboardHandler)
    print(f"[*] SMC Hub v6.5 Interactive Charts Online en {PORT}")
    server.serve_forever()

if __name__ == "__main__":
    print("Sincronizando con los mercados globales...")
    threading.Thread(target=simulator.update_prices, daemon=True).start()
    run_server()
