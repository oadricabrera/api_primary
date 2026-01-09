import pyRofex
import asyncio
import os
from dotenv import load_dotenv

# Cargar credenciales desde el archivo .env
load_dotenv()

USER = os.getenv("ROFEX_USER")
PASSWORD = os.getenv("ROFEX_PASSWORD")
ACCOUNT = os.getenv("ROFEX_ACCOUNT")

# Estado del sistema
state = {"balance": 0.0, "positions": {}, "active_orders": []}

# --- HANDLERS ---
def market_data_handler(message):
    print(f"Tick: {message['instrumentId']['symbol']} - Bid: {message['marketData']['bi']}")

def order_report_handler(message):
    report = message["orderReport"]
    print(f"Orden ID {report['clOrdId']} - Estado: {report['status']}")

def error_handler(message):
    print(f"Error de Rofex: {message}")

def exception_handler(e):
    """Atrapa excepciones graves del WebSocket para que el bot no crashee"""
    print(f"Excepción de WebSocket detectada: {e}")
    # Aquí podrías agregar un sistema de notificaciones (Telegram/Mail) en el futuro

# --- BUCLE DE CONTROL (REST) ---
async def rest_heartbeat():
    """
    Consulta REST cada 5 segundos para actualizar saldo y posiciones.
    Esta función cumple con los requisitos de seguridad Pre-Trade de Primary.
    """
    while True:
        try:
            # 1. Consultar Reporte de Cuenta (Saldo)
            acc = pyRofex.get_account_report(account=ACCOUNT)
            
            if acc and acc.get("status") == "OK":
                account_data = acc.get("accountData", {})
                
                # Intentamos obtener el disponible de varios campos posibles
                # reMarkets a veces usa 'availableToOperate' y otras 'cash'
                available = account_data.get("availableToOperate")
                if available is None:
                    available = account_data.get("cash", 0.0)
                
                state["balance"] = available
            else:
                print(f"[!] Warning: No se pudo obtener reporte de cuenta: {acc}")

            # 2. Consultar Posiciones Detalladas (Stock)
            pos = pyRofex.get_detailed_position(account=ACCOUNT)
            
            if pos and pos.get("status") == "OK":
                details = pos.get("positionDetails", [])
                # Mapeamos símbolo -> cantidad neta (compras - ventas)
                state["positions"] = {
                    p["symbol"]: (p.get("buySize", 0) - p.get("sellSize", 0)) 
                    for p in details
                }
            
            # 3. Imprimir estado actual
            print(f">>> [HEARTBEAT] Disponible: ${state['balance']:.2f} | Activos en cartera: {len(state['positions'])}")

        except Exception as e:
            print(f"Error crítico en Heartbeat REST: {e}")
            
        # Esperar 5 segundos antes de la próxima consulta
        await asyncio.sleep(5)

# --- INICIO ---
async def main():
    while True:
        try:
            print("Iniciando conexión con Matba Rofex...")
            
            # Inicializar entorno
            pyRofex.initialize(
                user=USER, 
                password=PASSWORD, 
                account=ACCOUNT, 
                environment=pyRofex.Environment.REMARKET
            )
            
            # Configurar el WebSocket con manejadores
            pyRofex.init_websocket_connection(
                market_data_handler=market_data_handler,
                order_report_handler=order_report_handler,
                error_handler=error_handler,
                exception_handler=exception_handler # Este es clave para la resiliencia
            )

            # Suscripciones
            pyRofex.order_report_subscription()
            pyRofex.market_data_subscription(
                tickers=["GGAL", "AL30"], 
                entries=[pyRofex.MarketDataEntry.BIDS, pyRofex.MarketDataEntry.OFFERS]
            )

            print("Conexión establecida. Iniciando Heartbeat...")
            
            # Ejecutar el Heartbeat. Si falla o se desconecta, el 'await' terminará
            # y el bucle 'while True' volverá a intentar la conexión.
            await rest_heartbeat()

        except Exception as e:
            print(f"Conexión perdida o fallida: {e}. Reintentando en 10 segundos...")
            await asyncio.sleep(10)

if __name__ == "__main__":
    asyncio.run(main())