from pyRofex import *

# Inicialización de la sesión
initialize(
    user="oadricabrera20096",
    password="nvdevU6$",
    account="REM20096",
    environment=Environment.REMARKET,
)
accion = "SOY.CME/DIC24"
# Definición de los manejadores
def market_data_handler(message):
    print("Market Data Message Received: {0}".format(message))

def order_report_handler(message):
    print("Order Report Message Received: {0}".format(message))

def error_handler(message):
    print("Error Message Received: {0}".format(message))

def exception_handler(e):
    print("Exception Occurred: {0}".format(e.message))

# Iniciar conexión WebSocket
init_websocket_connection(
    market_data_handler=market_data_handler,
    order_report_handler=order_report_handler,
    error_handler=error_handler,
    exception_handler=exception_handler,
)

# Suscripción a datos del mercado

market_data_subscription(
    tickers=[accion],
    entries=[MarketDataEntry.BIDS, MarketDataEntry.OFFERS],
    depth=4
)

# Obtener reporte de cuenta
reporte_de_cuenta = get_account_report()

detalle_de_posicion = get_detailed_position(
    account="REM20096", environment=Environment.REMARKET
)
print(f"\n\nReporte de Cuenta: {reporte_de_cuenta}, \n\ndetalle de cuenta: {detalle_de_posicion}")

# Enviar una orden
order = send_order_via_websocket(       #¿Hace falta hacer print para ver order?
        ticker=accion,
        side=Side.BUY,
        size=10,
        price=359.9,
        order_type=OrderType.LIMIT,
    )

print(f"\norder: {order}")  #veo None

# Obtener reporte de cuenta
reporte_de_cuenta = get_account_report()

detalle_de_posicion = get_detailed_position(
    account="REM20096", environment=Environment.REMARKET
)
print(f"\n\nReporte de Cuenta: {reporte_de_cuenta}, \n\ndetalle de cuenta: {detalle_de_posicion}")

print("\norder_report_subscription()")

order_report_subscription() #¿Sirve?

print("\norder_report_subscription(account=´REM20096´, environment=Environment.REMARKET)")

order_report_subscription(account="REM20096", environment=Environment.REMARKET) #¿Sirve?

"""
métodos

get_detailed_instruments al iniciar el script
get_detailed_position cada 5 segundos
get_account_report cada 5 segundos

wS

init_websocket_connection listo
send_order_via_websocket
cancel_order_via_websocket
order_report_subscription probar
market_data_subscription listo
"""
"""
from pyRofex import initialize, Environment, MarketDataEntry, Side, OrderType

# Inicialización de la sesión
initialize(
    user="oadricabrera20096",
    password="nvdevU6$",
    account="REM20096",
    environment=Environment.REMARKET,
)

accion = "SOY.CME/DIC24"

# Definición de los manejadores
def market_data_handler(message):
    print(f"Market Data Message Received: {message}")

def order_report_handler(message):
    print(f"Order Report Message Received: {message}")

def error_handler(message):
    print(f"Error Message Received: {message}")

def exception_handler(e):
    print(f"Exception Occurred: {str(e)}")

# Iniciar conexión WebSocket
init_websocket_connection(
    market_data_handler=market_data_handler,
    order_report_handler=order_report_handler,
    error_handler=error_handler,
    exception_handler=exception_handler,
)

# Suscripción a datos del mercado
try:
    market_data_subscription(
        tickers=[accion],
        entries=[MarketDataEntry.BIDS, MarketDataEntry.OFFERS],
        depth=4
    )
except Exception as e:
    print(f"Error al suscribirse a datos de mercado: {str(e)}")

# Enviar una orden
order = send_order_via_websocket(
    ticker=accion,
    side=Side.BUY,
    size=10,
    price=359.9,
    order_type=OrderType.LIMIT,
)

if order is None:
    print("Error: No se pudo enviar la orden.")
else:
    print(f"Orden enviada: {order}")

# Obtener reporte de cuenta y posiciones
try:
    reporte_de_cuenta = get_account_report()
    detalle_de_posicion = get_detailed_position(
        account="REM20096", environment=Environment.REMARKET
    )
    print(f"\n\nReporte de Cuenta: {reporte_de_cuenta}")
    print(f"\nDetalle de cuenta: {detalle_de_posicion}")
except Exception as e:
    print(f"Error al obtener reporte: {str(e)}")

# Suscripción a reportes de órdenes
order_report_subscription()
"""