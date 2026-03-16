import time
import os
from http.server import HTTPServer, BaseHTTPRequestHandler
import threading
import json
import random
from datetime import datetime
import urllib.request

# =================================================================
# SMC QUANT HUB v11.2 - TELEGRAM SENTINEL EDITION
# Architect: Gemini CLI (Senior Specialist)
# =================================================================

PORT = int(os.environ.get("PORT", 8000))
TELEGRAM_TOKEN = "8257347014:AAH18BpiTCBgdfvKegF54iAlWwNpCQzVE_k"
TELEGRAM_CHAT_ID = "8502418291"

def enviar_telegram(mensaje):
    """Envía una notificación institucional al móvil del usuario"""
    try:
        url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
        data = json.dumps({"chat_id": TELEGRAM_CHAT_ID, "text": mensaje, "parse_mode": "Markdown"}).encode('utf-8')
        req = urllib.request.Request(url, data=data, headers={'Content-Type': 'application/json'})
        with urllib.request.urlopen(req) as response:
            return response.read()
    except Exception as e:
        print(f"[!] Error enviando Telegram: {e}")

class MarketSimulator:
    def __init__(self):
        self.prices = {"oro": 5017.29, "eur": 1.1410, "dxy": 100.36}
        self.fixed_signals = []
        self.lock = threading.Lock()
        self.alerta_ote_enviada = False
        self.generate_new_signals(enviar_alerta=True) 

    def update_prices(self):
        while True:
            with self.lock:
                self.prices["oro"] += random.uniform(-0.15, 0.20)
                self.prices["eur"] += random.uniform(-0.0001, 0.0001)
                self.prices["dxy"] += random.uniform(-0.02, 0.02)
                
                # Alerta OTE XAU/USD ($5,012.00)
                if self.prices["oro"] <= 5012.05 and not self.alerta_ote_enviada:
                    enviar_telegram("🚀 *ALERTA SMC: XAU/USD EN ZONA OTE ($5,012.00)*\nBuscando barrido de liquidez SSL. Prepara ejecución institucional.")
                    self.alerta_ote_enviada = True
                elif self.prices["oro"] > 5015.00:
                    self.alerta_ote_enviada = False # Reset para la próxima entrada
            time.sleep(2)

    def calculate_potential(self, entry, tp, asset_id, lot):
        diff = abs(tp - entry)
        if asset_id == "oro":
            return round(diff * 100 * lot, 2)
        else:
            return round(diff * 100000 * lot, 2)

    def generate_new_signals(self, enviar_alerta=False):
        with self.lock:
            p = self.prices
            new_signals = []
            config = [
                {"id": "oro", "nombre": "XAU/USD (ORO)", "precio": p["oro"], "step": 1.0},
                {"id": "eur", "nombre": "EUR/USD (EURO)", "precio": p["eur"], "step": 0.0010}
            ]
            reporte = "📊 *REPORTE DE MATRIZ SMC v11.2*\n\n"
            for asset in config:
                base = asset["precio"]
                reporte += f"*{asset['nombre']}*:\n"
                for tipo, mult_e, mult_sl, mult_tp in [("SCALP", 0.15, 0.8, 3.0), ("INTRADAY", 0.40, 1.5, 7.0), ("SWING", 0.80, 2.0, 10.0)]:
                    entry = round(base - (asset["step"] * mult_e), 4 if asset["id"] == "eur" else 2)
                    sig = {
                        "asset_name": asset["nombre"], "tipo": tipo, "entrada": entry,
                        "sl": round(entry - (asset["step"] * mult_sl), 4 if asset["id"] == "eur" else 2),
                        "tp": round(entry + (asset["step"] * mult_tp), 4 if asset["id"] == "eur" else 2),
                        "tendencia": f"BULLISH {tipo}", "asset_id": asset["id"]
                    }
                    new_signals.append(sig)
                    reporte += f"🔹 {tipo}: Entry ${entry} | TP ${sig['tp']}\n"
                reporte += "\n"
            
            self.fixed_signals = new_signals
            if enviar_alerta:
                enviar_telegram(reporte + "🌐 *Dashboard Online:* https://smc-quant-hub-v11.onrender.com")

    def get_full_data(self):
        with self.lock:
            data = {"timestamp": datetime.now().strftime("%H:%M:%S"), "activos": []}
            for sig in self.fixed_signals:
                cp = self.prices[sig["asset_id"]]
                pnl_l = (cp - sig["entrada"]) * (1 if sig["asset_id"] == "oro" else 10000)
                data["activos"].append({
                    **sig,
                    "precio_actual": round(cp, 4 if sig["asset_id"] == "eur" else 2),
                    "pnl_latente": f"{'+' if pnl_l >= 0 else ''}{round(pnl_l, 2)}",
                    "ganancia_100": f"${self.calculate_potential(sig['entrada'], sig['tp'], sig['asset_id'], 1.00)}",
                    "ganancia_050": f"${self.calculate_potential(sig['entrada'], sig['tp'], sig['asset_id'], 0.50)}",
                    "ganancia_010": f"${self.calculate_potential(sig['entrada'], sig['tp'], sig['asset_id'], 0.10)}"
                })
            return data

simulator = MarketSimulator()

class DashboardHandler(BaseHTTPRequestHandler):
    def log_message(self, format, *args): pass
    def do_GET(self):
        if self.path == '/api/data':
            self.send_response(200); self.send_header('Content-type', 'application/json'); self.end_headers()
            self.wfile.write(json.dumps(simulator.get_full_data()).encode())
        elif self.path == '/api/generate':
            simulator.generate_new_signals(enviar_alerta=True); self.send_response(200); self.send_header('Content-type', 'application/json'); self.end_headers()
            self.wfile.write(json.dumps({"success": True}).encode())
        elif self.path == '/':
            self.send_response(200); self.send_header('Content-type', 'text/html; charset=utf-8'); self.end_headers()
            html = """
            <!DOCTYPE html>
            <html lang="es">
            <head>
                <meta charset="UTF-8">
                <title>SMC HUB v11.2 - TELEGRAM ACTIVE</title>
                <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800&family=JetBrains+Mono:wght@400;700&display=swap" rel="stylesheet">
                <style>
                    :root { --bg: #050608; --card: #11141a; --border: #1e222d; --green: #089981; --red: #f23645; --gold: #ffd700; --blue: #2962ff; }
                    body { font-family: 'Inter', sans-serif; background-color: var(--bg); color: #d1d4dc; margin: 0; padding: 20px; }
                    .container { max-width: 1750px; margin: auto; }
                    header { display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid var(--border); padding-bottom: 15px; margin-bottom: 20px; }
                    .btn-generate { background: var(--gold); color: #000; border: none; padding: 12px 25px; border-radius: 8px; font-weight: 800; cursor: pointer; text-transform: uppercase; }
                    .matrix-card { background: var(--card); border: 1px solid var(--border); border-radius: 12px; padding: 20px; margin-bottom: 30px; }
                    table { width: 100%; border-collapse: collapse; border: 1px solid #333; }
                    th { text-align: center; color: #848e9c; font-size: 10px; text-transform: uppercase; padding: 15px; background: #1a1e26; border: 1px solid #333; }
                    td { padding: 15px; border: 1px solid #222; font-size: 13px; text-align: center; }
                    .asset-cell { font-size: 18px; font-weight: 800; color: var(--gold); background: #0c0e12; border-right: 2px solid #333 !important; }
                    .price-real { font-size: 20px; font-weight: 800; color: #fff; background: #0c0e12; border-right: 2px solid #333 !important; }
                    .strategy-cell { font-weight: 800; color: #00ff41; background: rgba(0,255,65,0.02); }
                    .charts-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 20px; }
                    .tv-container { background: var(--card); border: 1px solid var(--border); border-radius: 12px; height: 450px; overflow: hidden; }
                </style>
                <script type="text/javascript" src="https://s3.tradingview.com/tv.js"></script>
            </head>
            <body>
                <div class="container">
                    <header>
                        <div>
                            <div style="font-weight:800; color:var(--gold); font-size:24px;">SMC QUANT HUB v11.2</div>
                            <div style="color:var(--green); font-size:12px;">TELEGRAM SENTINEL ACTIVADO: NOTIFICACIONES AL MÓVIL</div>
                        </div>
                        <button class="btn-generate" onclick="generateSignals()">Generar Señales y Enviar Reporte</button>
                        <div id="terminal-clock" style="font-family:'JetBrains Mono'; font-size:14px; color:var(--green);">--:--:--</div>
                    </header>
                    <div class="matrix-card">
                        <table>
                            <thead>
                                <tr>
                                    <th>Activo Principal</th><th>Precio Mercado</th><th>Estrategia</th><th>Status</th><th>Entrada</th><th>SL</th><th>TP</th>
                                    <th>PnL Latente</th><th>G-1.00</th><th>G-0.50</th><th>G-0.10</th>
                                </tr>
                            </thead>
                            <tbody id="data-table-body"></tbody>
                        </table>
                    </div>
                    <div class="charts-grid">
                        <div class="tv-container"><div id="tv_oro" style="height:100%;"></div></div>
                        <div class="tv-container"><div id="tv_eur" style="height:100%;"></div></div>
                    </div>
                </div>
                <script>
                    new TradingView.widget({"autosize": true, "symbol": "FX_IDC:XAUUSD", "interval": "15", "theme": "dark", "container_id": "tv_oro"});
                    new TradingView.widget({"autosize": true, "symbol": "FX:EURUSD", "interval": "15", "theme": "dark", "container_id": "tv_eur"});

                    async function generateSignals() {
                        if(confirm("¿Recalcular matriz y enviar reporte a Telegram?")) { await fetch('/api/generate'); update(); }
                    }
                    async function update() {
                        try {
                            const res = await fetch('/api/data'); const data = await res.json();
                            document.getElementById('terminal-clock').innerText = 'SMC GLOBAL CLOCK: ' + data.timestamp;
                            let html = '';
                            for(let i=0; i<data.activos.length; i++) {
                                let a = data.activos[i];
                                html += `<tr>`;
                                if(i % 3 === 0) {
                                    html += `<td rowspan="3" class="asset-cell">${a.asset_name}</td>`;
                                    html += `<td rowspan="3" class="price-real">$${a.precio_actual}</td>`;
                                }
                                html += `<td class="strategy-cell">${a.tipo}</td>
                                    <td><span style="background:rgba(8,153,129,0.1); color:var(--green); padding:4px 8px; border-radius:4px; font-size:10px; font-weight:bold;">${a.tendencia}</span></td>
                                    <td style="color:var(--blue); font-weight:bold;">$${a.entrada}</td>
                                    <td style="color:var(--red); font-weight:bold;">$${a.sl}</td>
                                    <td style="color:var(--green); font-weight:bold;">$${a.tp}</td>
                                    <td style="color:var(--gold); font-weight:800;">${a.pnl_latente}</td>
                                    <td style="color:var(--gold); font-weight:bold;">${a.ganancia_100}</td>
                                    <td style="color:var(--gold); font-weight:bold;">${a.ganancia_050}</td>
                                    <td style="color:var(--gold); font-weight:bold;">${a.ganancia_010}</td>
                                </tr>`;
                            }
                            document.getElementById('data-table-body').innerHTML = html;
                        } catch (e) {}
                    }
                    setInterval(update, 2000); update();
                </script>
            </body>
            </html>
            """
            self.wfile.write(html.encode('utf-8'))

def run_server():
    server = HTTPServer(('0.0.0.0', PORT), DashboardHandler)
    print(f"[*] SMC Hub v11.2 Sentinel - Puerto: {PORT}")
    server.serve_forever()

if __name__ == "__main__":
    threading.Thread(target=simulator.update_prices, daemon=True).start()
    run_server()
