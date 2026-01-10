import pyRofex
import asyncio
import os
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

class RofexHomologadoBot:
    def __init__(self):
        self.user = os.getenv("ROFEX_USER")
        self.password = os.getenv("ROFEX_PASSWORD")
        self.account = os.getenv("ROFEX_ACCOUNT")
        
        self.balance = 0.0
        self.positions = {}
        self.market_data = {}
        self.order_history = []
        self.instruments = []
        self.logs = []

    def log(self, message):
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.logs.append(f"[{timestamp}] {message}")
        self.logs = self.logs[-8:]
        self.render_table()

    # --- HANDLERS ---
    def market_data_handler(self, message):
        symbol = message['instrumentId']['symbol']
        md = message['marketData']
        
        # Extraemos precios y cantidades (lotes)
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
        msg = f"ORDEN {report['clOrdId']}: {report['status']} - {report.get('text', '')}"
        self.log(msg)

    def error_handler(self, message):
        self.log(f"API ERROR: {message}")

    def exception_handler(self, e):
        self.log(f"WS EXCEPTION: {str(e)}")

    # --- INTERFAZ ESTÁTICA ---
    def render_table(self):
        print("\033c", end="") 
        print(f"=== HOMOLOGACIÓN PRIMARY - CUENTA: {self.account} ===")
        print(f"SALDO DISPONIBLE: ${self.balance:,.2f} | POSICIONES: {len(self.positions)}")
        print("-" * 85)
        # Columnas fijas: Símbolo, Cant. Compra, Compra, Venta, Cant. Venta, Último
        print(f"{'Símbolo':<18} | {'Q.Bid':<8} | {'Bid':<10} | {'Offer':<10} | {'Q.Off':<8} | {'Last':<10}")
        print("-" * 85)
        
        for sym in self.instruments:
            d = self.market_data.get(sym, {"bid": 0, "bid_qty": 0, "offer": 0, "offer_qty": 0, "last": 0})
            print(f"{sym:<18} | {d['bid_qty']:<8} | {d['bid']:<10.2f} | {d['offer']:<10.2f} | {d['offer_qty']:<8} | {d['last']:<10.2f}")
        
        print("\n" + "="*40 + "\n LOGS DE AUDITORÍA\n" + "="*40)
        for line in self.logs: print(line)
        if not self.logs: print("Esperando eventos de mercado...")

    # --- LOGICA REST (Heartbeat 5s) ---
    async def heartbeat_control(self):
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
                self.log(f"Error Heartbeat: {e}")
            await asyncio.sleep(5)

    # --- OPERATIVA ---
    async def send_order_safe(self, symbol, side, size, price):
        # Validación de Seguridad Pre-Trade
        if side == pyRofex.Side.BUY and self.balance <= 0:
            self.log("BLOQUEO: Saldo insuficiente")
            return

        cl_id = f"bot_{int(datetime.now().timestamp())}"
        pyRofex.send_order_via_websocket(
            ticker=symbol, side=side, size=size, price=price,
            order_type=pyRofex.OrderType.LIMIT, ws_client_order_id=cl_id,
            all_or_none=True
        )
        self.order_history.append(cl_id)

    async def start(self):
        try:
            pyRofex.initialize(user=self.user, password=self.password, account=self.account, environment=pyRofex.Environment.REMARKET)
            
            all_inst = pyRofex.get_detailed_instruments()
            self.instruments = sorted([
                i['instrumentId']['symbol'] for i in all_inst['instruments'] 
                if "DLR/" in i['instrumentId']['symbol'] and i['instrumentId']['symbol'].count('/') == 1
                and " " not in i['instrumentId']['symbol']
            ])

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

            asyncio.create_task(self.heartbeat_control())
            while True: await asyncio.sleep(1)
        except Exception as e:
            print(f"Error inicial: {e}")

if __name__ == "__main__":
    bot = RofexHomologadoBot()
    asyncio.run(bot.start())