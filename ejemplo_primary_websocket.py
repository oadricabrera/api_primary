from pyRofex import *
import ssl
import certifi
ssl_context = ssl.create_default_context(cafile=certifi.where())

# Desactivar verificación de certificados (solo para desarrollo)
#ssl._create_default_https_context = ssl._create_unverified_context

try:
    # Inicialización de la sesión
    initialize(
        user="oadricabrera20096",
        password="nvdevU6$",
        account="REM20096",
        environment=Environment.REMARKET,
    )
except Exception as e:
    print(f"Error al inicializar la sesión: {e}")
    exit(1)

accion = "DLR/JUL25"

# Definición de los manejadores
def market_data_handler(message):
    print("Market Data Message Received: {0}".format(message))

def order_report_handler(message):
    print("Order Report Message Received: {0}".format(message))

def error_handler(message):
    print("Error Message Received: {0}".format(message))

def exception_handler(e):
    print("Exception Occurred: {0}".format(e))

try:
    # Iniciar conexión WebSocket
    init_websocket_connection(
        market_data_handler=market_data_handler,
        order_report_handler=order_report_handler,
        error_handler=error_handler,
        exception_handler=exception_handler,
    )
except Exception as e:
    print(f"Error al iniciar la conexión WebSocket: {e}")
    exit(1)

try:
    # Suscripción a datos del mercado
    market_data_subscription(
        tickers=[accion],
        entries=[MarketDataEntry.BIDS, MarketDataEntry.OFFERS],
        depth=4
    )
except Exception as e:
    print(f"Error al suscribirse a los datos del mercado: {e}")
    exit(1)

try:
    # Obtener reporte de cuenta
    reporte_de_cuenta = get_account_report()
    print(f"\nReporte de cuenta: {reporte_de_cuenta}")
except Exception as e:
    print(f"Error al obtener el reporte de cuenta: {e}")

try:
    # Enviar una orden
    orden_enviada = send_order(
        ticker=accion,
        side=Side.BUY,
        size=1,
        price=1310,
        order_type=OrderType.LIMIT
    )
    print(f"\nOrden Enviada: {orden_enviada}")
except Exception as e:
    print(f"Error al enviar la orden: {e}")

# Cerrar la conexión WebSocket al finalizar
close_websocket_connection()