import pyRofex
import asyncio
import os
from datetime import datetime
from dotenv import load_dotenv

# Cargar credenciales desde el archivo .env
load_dotenv()

class RofexBot:
    def __init__(self):
        self.user = os.getenv("ROFEX_USER")
        self.password = os.getenv("ROFEX_PASSWORD")
        self.account = os.getenv("ROFEX_ACCOUNT")
        
        # Estado del sistema
        self.balance = 0.0
        self.positions = {}
        self.market_data = {}  
        self.order_history = [] 
        self.instruments = []   
        self.logs = []

    def log(self, message):
        """Guarda un mensaje con hora y refresca la pantalla."""
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.logs.append(f"[{timestamp}] {message}")
        self.logs = self.logs[-8:] # Mantenemos los últimos 8 mensajes
        self.render_table()

    # --- HANDLERS ---
    def market_data_handler(self, message):
        symbol = message['instrumentId']['symbol']
        md = message['marketData']
        
        self.market_data[symbol] = {
            "bid": md.get('bi', [{}])[0].get('price', 0),
            "bid_qty": md.get('bi', [{}])[0].get('size', 0),
            "offer": md.get('of', [{}])[0].get('price', 0),
            "offer_qty": md.get('of', [{}])[0].get('size', 0),
            "last": md.get('la', {}).get('price', 0)
        }
        self.render_table()

    def order_report_handler(self, message):
        report = message["orderReport"]
        status = report['status']
        texto = report.get('text', 'Sin info')
        self.log(f"ORDEN {report['clOrdId']}: {status} ({texto})")

    def error_handler(self, message):
        self.log(f"ERROR API: {message}")

    def exception_handler(self, e):
        self.log(f"EXCEPCIÓN WS: {str(e)}")

    # --- INTERFAZ ---
    def render_table(self):
        """Dibuja la tabla y los logs debajo."""
        print("\033c", end="") 
        print(f"=== MONITOR ROFEX - CUENTA: {self.account} ===")
        print(f"Disponible: ${self.balance:.2f} | Posiciones: {len(self.positions)}")
        print("-" * 78)
        print(f"{'Símbolo':<18} | {'Bid':<10} | {'Offer':<10} | {'Last':<10} | {'Vol. Bid':<8}")
        print("-" * 78)
        
        for sym in self.instruments:
            d = self.market_data.get(sym, {"bid": 0, "offer": 0, "last": 0, "bid_qty": 0})
            print(f"{sym:<18} | {d['bid']:<10.2f} | {d['offer']:<10.2f} | {d['last']:<10.2f} | {d['bid_qty']:<8}")
        
        print("\n" + "="*40)
        print(" RECIENTES / ESTADO ")
        print("="*40)
        if not self.logs:
            print("Esperando eventos...")
        else:
            for line in self.logs:
                print(line)
        print("\n[Ctrl+C para salir]")

    # --- LÓGICA REST (Heartbeat) ---
    async def rest_heartbeat(self):
        while True:
            try:
                acc = pyRofex.get_account_report(account=self.account)
                if acc and acc.get("status") == "OK":
                    data = acc.get("accountData", {})
                    self.balance = data.get("availableToOperate") or data.get("cash", 0.0)

                pos = pyRofex.get_detailed_position(account=self.account)
                if pos and pos.get("status") == "OK":
                    details = pos.get("positionDetails", [])
                    self.positions = {p["symbol"]: (p.get("buySize", 0) - p.get("sellSize", 0)) for p in details}
                
                self.render_table()
            except Exception as e:
                self.log(f"Error en Heartbeat: {e}")
            await asyncio.sleep(5)

    # --- OPERATIVA ---
    async def send_order(self, symbol, side, size, price):
        try:
            cl_id = f"bot_{int(datetime.now().timestamp())}"
            self.log(f"Enviando {side} {symbol} a ${price}...")
            
            pyRofex.send_order_via_websocket(
                ticker=symbol, side=side, size=size, price=price,
                order_type=pyRofex.OrderType.LIMIT, ws_client_order_id=cl_id, all_or_none=True
            )
            self.order_history.append(cl_id)
            return cl_id
        except Exception as e:
            self.log(f"Error al enviar orden: {e}")

    # --- MAIN ---
    async def start(self):
        while True:
            try:
                self.log("Conectando con Primary...")
                pyRofex.initialize(user=self.user, password=self.password, account=self.account, environment=pyRofex.Environment.REMARKET)
                
                # 1. Filtro optimizado: Solo contratos directos de Dólar
                all_inst = pyRofex.get_detailed_instruments()
                self.instruments = sorted([
                    i['instrumentId']['symbol'] 
                    for i in all_inst['instruments'] 
                    if "DLR/" in i['instrumentId']['symbol'] 
                    and i['instrumentId']['symbol'].count('/') == 1 
                    and " " not in i['instrumentId']['symbol']
                ])
                
                # 2. Conexión WebSocket
                pyRofex.init_websocket_connection(
                    market_data_handler=self.market_data_handler,
                    order_report_handler=self.order_report_handler,
                    error_handler=self.error_handler,
                    exception_handler=self.exception_handler
                )

                pyRofex.order_report_subscription()
                pyRofex.market_data_subscription(
                    tickers=self.instruments,
                    entries=[pyRofex.MarketDataEntry.BIDS, pyRofex.MarketDataEntry.OFFERS, pyRofex.MarketDataEntry.LAST]
                )

                # 3. Lanzamos el Heartbeat (Consulta de Saldo)
                asyncio.create_task(self.rest_heartbeat())

                # 4. PRUEBA DE ORDEN (Mañana a las 10am esto debería entrar al mercado)
                await asyncio.sleep(3)
                await self.send_order("DLR/FEB26A", pyRofex.Side.BUY, 1000, 1400.00)
                
                while True:
                    await asyncio.sleep(1)

            except Exception as e:
                self.log(f"Reconectando: {e}")
                await asyncio.sleep(10)

if __name__ == "__main__":
    bot = RofexBot()
    asyncio.run(bot.start())