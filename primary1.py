from pyRofex import *

# Set the the parameter for the REMARKET environment
# item 2-Llamado al método get token
initialize(
    user="oadricabrera9893",
    password="dkjtoG2@",
    account="REM9893",
    environment=Environment.REMARKET,
)


lista_simbolo = list()

# item 3-Solicitar lista de instrumentos
# almacenar el listado de instrumentos con su detalles en almacenamiento_de_detalles
almacenamiento_de_detalles = get_detailed_instruments()
almacenamiento_de_detalles = almacenamiento_de_detalles.get("instruments")
"""
for i in almacenamiento_de_detalles:
    print(i.instruments)
"""
# item 4- validamos los intrumentos de interes: vamos a trabajar con acciones y opciones de merval
for i in almacenamiento_de_detalles:
    simbolo = i.get("instrumentId").get("symbol")
    if simbolo.startswith("MERV") and simbolo.endswith("48hs"):
        lista_simbolo.append(simbolo)
        # print(simbolo)

# print(lista_simbolo)


# First we define the handlers that will process the messages and exceptions.
# item 5 y 6: suscripción a la marketdata y manejo de los datos
def market_data_handler(message):
    print("Market Data Message Received: {0}".format(message))


def order_report_handler(message):
    id_order = message["orderReport"]["clOrdId"]

    print(f"estatus orden {id_order}", get_order_status(id_order))
    # print(f"******* {type(message)}")
    # print("Order Report Message Received: {0}".format(message))


def error_handler(message):
    print("Error Message Received: {0}".format(message))


def exception_handler(e):
    print(f"--<< {e} >>--")
    print("Exception Occurred: {0}".format(e.message))


# Initiate Websocket Connection
init_websocket_connection(
    market_data_handler=market_data_handler,
    order_report_handler=order_report_handler,
    error_handler=error_handler,
    exception_handler=exception_handler,
)

# Instruments list to subscribe
# instruments = ["DLR/DIC23", "DLR/ENE24"]
# Uses the MarketDataEntry enum to define the entries we want to subscribe to
entries = [MarketDataEntry.BIDS, MarketDataEntry.OFFERS, MarketDataEntry.LAST]

# Subscribes to receive market data messages **
# market_data_subscription(tickers=lista_simbolo, entries=entries)

# Subscribes to receive order report messages (default account will be used) **

order_report_subscription(account="REM9893", environment=Environment.REMARKET)

# send_order(lista_simbolo)

# reporte_de_cuenta = get_account_report(
#     account="REM9893", environment=Environment.REMARKET
# )

# posicion_de_cuenta = get_account_position(
#     account="REM9893", environment=Environment.REMARKET
# )

# order = send_order()
# print(reporte_de_cuenta,posicion_de_cuenta)
# ['MERV - XMEV - AGRO - 48hs', 'MERV - XMEV - CVH - 48hs', 'MERV - XMEV - MIRG - 48hs', 'MERV - XMEV - GOOGL - 48hs', 'MERV - XMEV - VALE - 48hs', 'MERV - XMEV - HMY - 48hs', 'MERV - XMEV - PBRC - 48hs', 'MERV - XMEV - APBRA - 48hs', 'MERV - XMEV - DICAC - 48hs', 'MERV - XMEV - TLC5O - 48hs', 'MERV - XMEV - BBD - 48hs', 'MERV - XMEV - YPCUD - 48hs', 'MERV - XMEV - VIST - 48hs', 'MERV - XMEV - YPFD - 48hs', 'MERV - XMEV - TGNO4 - 48hs', 'MERV - XMEV - BMA - 48hs', 'MERV - XMEV - LOMA - 48hs', 'MERV - XMEV - DICA - 48hs', 'MERV - XMEV - SAMI - 48hs', 'MERV - XMEV - ARC1O - 48hs', 'MERV - XMEV - IRCFO - 48hs', 'MERV - XMEV - CP17O - 48hs', 'MERV - XMEV - CS38O - 48hs', 'MERV - XMEV - AA37 - 48hs', 'MERV - XMEV - TSLA - 48hs', 'MERV - XMEV - GD30D - 48hs', 'MERV - XMEV - YMCQO - 48hs', 'MERV - XMEV - GD35 - 48hs', 'MERV - XMEV - COME - 48hs', 'MERV - XMEV - MGCHO - 48hs', 'MERV - XMEV - AY24 - 48hs', 'MERV - XMEV - AY24C - 48hs', 'MERV - XMEV - AMZND - 48hs', 'MERV - XMEV - AAPL - 48hs', 'MERV - XMEV - GD41D - 48hs', 'MERV - XMEV - AAPLD - 48hs', 'MERV - XMEV - AMZNC - 48hs', 'MERV - XMEV - MTCGO - 48hs', 'MERV - XMEV - YPCUO - 48hs', 'MERV - XMEV - PBRD - 48hs', 'MERV - XMEV - BBAR - 48hs', 'MERV - XMEV - CRES - 48hs', 'MERV - XMEV - GD30C - 48hs', 'MERV - XMEV - TXAR - 48hs', 'MERV - XMEV - AY24D - 48hs', 'MERV - XMEV - PBR - 48hs', 'MERV - XMEV - IRCGO - 48hs', 'MERV - XMEV - PAMP - 48hs', 'MERV - XMEV - AMZN - 48hs', 'MERV - XMEV - MELI - 48hs', 'MERV - XMEV - AER1D - 48hs', 'MERV - XMEV - ALUA - 48hs', 'MERV - XMEV - CP30O - 48hs', 'MERV - XMEV - AAPLC - 48hs', 'MERV - XMEV - TECO2 - 48hs', 'MERV - XMEV - CEPU - 48hs', 'MERV - XMEV - AL29C - 48hs', 'MERV - XMEV - SUPV - 48hs', 'MERV - XMEV - VALO - 48hs', 'MERV - XMEV - GGAL - 48hs', 'MERV - XMEV - CP30D - 48hs', 'MERV - XMEV - BYMA - 48hs', 'MERV - XMEV - DIA - 48hs', 'MERV - XMEV - EWZ - 48hs', 'MERV - XMEV - GD30 - 48hs', 'MERV - XMEV - SPY - 48hs', 'MERV - XMEV - GD41 - 48hs', 'MERV - XMEV - TGSU2 - 48hs', 'MERV - XMEV - KO - 48hs', 'MERV - XMEV - AL41 - 48hs', 'MERV - XMEV - TRAN - 48hs', 'MERV - XMEV - AL30C - 48hs', 'MERV - XMEV - AL30 - 48hs', 'MERV - XMEV - YMCIO - 48hs', 'MERV - XMEV - GOLD - 48hs', 'MERV - XMEV - AL29 - 48hs', 'MERV - XMEV - MSFT - 48hs', 'MERV - XMEV - DICAD - 48hs', 'MERV - XMEV - AL35 - 48hs', 'MERV - XMEV - MGC9O - 48hs', 'MERV - XMEV - AL29D - 48hs', 'MERV - XMEV - AL30D - 48hs']
order = send_order(
    ticker="MERV - XMEV - AGRO - 48hs",
    side=Side.BUY,
    size=10,
    price=55.8,
    order_type=OrderType.LIMIT,
)  # {'status': 'OK', 'order': {'clientId': '450835497387610', 'proprietary': 'PBCP'}}
print("\ncreamos una orden--> ", order)

estado_de_orden = get_order_status(order["order"]["clientId"])

print(f'\nestado de orden: {estado_de_orden}')

cancelar_orden = cancel_order(order["order"]["clientId"])

print(f"\ncancelamos una orden: {cancelar_orden}")

estado_de_orden_cancelada = get_order_status(cancelar_orden)

print(f"\nestado de Orden Cancelada: {estado_de_orden_cancelada}")
