from pyRofex import *

# Inicialización de la sesión
initialize(
    user="oadricabrera20096",
    password="nvdevU6$",
    account="REM20096",
    environment=Environment.REMARKET,
)
accion = "ORO/MAY25"
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
print(f"\nReporte de cuenta: {reporte_de_cuenta}")

# Enviar una orden
orden_enviada = send_order(
    ticker=accion,
    side=Side.BUY,
    size=1,
    price=6670,
    order_type=OrderType.LIMIT
)
print(f"\nOrden Enviada: {orden_enviada}")

"""
from pyRofex import *

initialize(
    user="oadricabrera9893",
    password="dkjtoG2@",
    account="REM9893",
    environment=Environment.REMARKET,
)

def market_data_handler(message):
    print("Market Data Message Received: {0}".format(message))


def order_report_handler(message):
    print("Order Report Message Received: {0}".format(message))


def error_handler(message):
    print("Error Message Received: {0}".format(message))


def exception_handler(e):
    print("Exception Occurred: {0}".format(e.message))

init_websocket_connection(
    market_data_handler=market_data_handler,
    order_report_handler=order_report_handler,
    error_handler=error_handler,
    exception_handler=exception_handler,
)


reporte_de_cuenta = get_account_report(account="REM9893", environment=Environment.REMARKET) 

print(f"\nReporte de cuenta: {reporte_de_cuenta}")

market_data_subscription(["GGAL/DIC24"],[MarketDataEntry.BIDS,MarketDataEntry.OFFERS],depth=4)

"""
print(f"\n{MarketDataEntry.__doc__}")


