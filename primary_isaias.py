from pyRofex import *

# Set the the parameter for the REMARKET environment
# item 2-Llamado al método get token
initialize(
    user="oadricabrera20096",
    password="nvdevU6$",
    account="REM20096",
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
    print("Order Report Message Received: {0}".format(message))
    # 6-Handler will validate if the order is in the correct state (pending_new)
    print(f"\norder report handler {message}")
    if message["orderReport"]["status"] == "NEW":
        # 6.1-We cancel the order using the websocket connection
        print("\nSend to Cancel Order with clOrdID: {0}".format(message["orderReport"]["clOrdId"]))
        cancel_order_via_websocket(message["orderReport"]["clOrdId"])
    # 7-Handler will receive an Order Report indicating that the order is cancelled (will print it)
    if message["orderReport"]["status"] == "CANCELLED":
        print("\nOrder with ClOrdID '{0}' is Cancelled.".format(message["orderReport"]["clOrdId"]))


def error_handler(message):
    print("Error Message Received: {0}".format(message))


def exception_handler(e):
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
#<<<<<<< HEAD
#market_data_subscription(tickers=lista_simbolo, entries=entries)

# Subscribes to receive order report messages (default account will be used) **

#order_report_subscription(account="REM20096", environment=Environment.REMARKET)

#send_order(lista_simbolo)

reporte_de_cuenta = get_account_report(
    account="REM20096", environment=Environment.REMARKET
)
""" lo cambiamos por get_detailed_position
posicion_de_cuenta = get_account_position(
    account="REM20096", environment=Environment.REMARKET
)
"""
# print(reporte_de_cuenta,posicion_de_cuenta)
# ['MERV - XMEV - AGRO - 48hs', 'MERV - XMEV - CVH - 48hs', 'MERV - XMEV - MIRG - 48hs', 'MERV - XMEV - GOOGL - 48hs', 'MERV - XMEV - VALE - 48hs', 'MERV - XMEV - HMY - 48hs', 'MERV - XMEV - PBRC - 48hs', 'MERV - XMEV - APBRA - 48hs', 'MERV - XMEV - DICAC - 48hs', 'MERV - XMEV - TLC5O - 48hs', 'MERV - XMEV - BBD - 48hs', 'MERV - XMEV - YPCUD - 48hs', 'MERV - XMEV - VIST - 48hs', 'MERV - XMEV - YPFD - 48hs', 'MERV - XMEV - TGNO4 - 48hs', 'MERV - XMEV - BMA - 48hs', 'MERV - XMEV - LOMA - 48hs', 'MERV - XMEV - DICA - 48hs', 'MERV - XMEV - SAMI - 48hs', 'MERV - XMEV - ARC1O - 48hs', 'MERV - XMEV - IRCFO - 48hs', 'MERV - XMEV - CP17O - 48hs', 'MERV - XMEV - CS38O - 48hs', 'MERV - XMEV - AA37 - 48hs', 'MERV - XMEV - TSLA - 48hs', 'MERV - XMEV - GD30D - 48hs', 'MERV - XMEV - YMCQO - 48hs', 'MERV - XMEV - GD35 - 48hs', 'MERV - XMEV - COME - 48hs', 'MERV - XMEV - MGCHO - 48hs', 'MERV - XMEV - AY24 - 48hs', 'MERV - XMEV - AY24C - 48hs', 'MERV - XMEV - AMZND - 48hs', 'MERV - XMEV - AAPL - 48hs', 'MERV - XMEV - GD41D - 48hs', 'MERV - XMEV - AAPLD - 48hs', 'MERV - XMEV - AMZNC - 48hs', 'MERV - XMEV - MTCGO - 48hs', 'MERV - XMEV - YPCUO - 48hs', 'MERV - XMEV - PBRD - 48hs', 'MERV - XMEV - BBAR - 48hs', 'MERV - XMEV - CRES - 48hs', 'MERV - XMEV - GD30C - 48hs', 'MERV - XMEV - TXAR - 48hs', 'MERV - XMEV - AY24D - 48hs', 'MERV - XMEV - PBR - 48hs', 'MERV - XMEV - IRCGO - 48hs', 'MERV - XMEV - PAMP - 48hs', 'MERV - XMEV - AMZN - 48hs', 'MERV - XMEV - MELI - 48hs', 'MERV - XMEV - AER1D - 48hs', 'MERV - XMEV - ALUA - 48hs', 'MERV - XMEV - CP30O - 48hs', 'MERV - XMEV - AAPLC - 48hs', 'MERV - XMEV - TECO2 - 48hs', 'MERV - XMEV - CEPU - 48hs', 'MERV - XMEV - AL29C - 48hs', 'MERV - XMEV - SUPV - 48hs', 'MERV - XMEV - VALO - 48hs', 'MERV - XMEV - GGAL - 48hs', 'MERV - XMEV - CP30D - 48hs', 'MERV - XMEV - BYMA - 48hs', 'MERV - XMEV - DIA - 48hs', 'MERV - XMEV - EWZ - 48hs', 'MERV - XMEV - GD30 - 48hs', 'MERV - XMEV - SPY - 48hs', 'MERV - XMEV - GD41 - 48hs', 'MERV - XMEV - TGSU2 - 48hs', 'MERV - XMEV - KO - 48hs', 'MERV - XMEV - AL41 - 48hs', 'MERV - XMEV - TRAN - 48hs', 'MERV - XMEV - AL30C - 48hs', 'MERV - XMEV - AL30 - 48hs', 'MERV - XMEV - YMCIO - 48hs', 'MERV - XMEV - GOLD - 48hs', 'MERV - XMEV - AL29 - 48hs', 'MERV - XMEV - MSFT - 48hs', 'MERV - XMEV - DICAD - 48hs', 'MERV - XMEV - AL35 - 48hs', 'MERV - XMEV - MGC9O - 48hs', 'MERV - XMEV - AL29D - 48hs', 'MERV - XMEV - AL30D - 48hs']

detalle_de_posicion = get_detailed_position(
    account="REM20096", environment=Environment.REMARKET
)

print(f"\n\nReporte de Cuenta: {reporte_de_cuenta}, \n\ndetalle de cuenta: {detalle_de_posicion}")
"""
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
"""
#send_order_via_websocket(tickers='MERV - XMEV - AY24C - 48hs')

order = send_order_via_websocket(
        ticker='MERV - XMEV - AGRO - 48hs',
        side=Side.BUY,
        size=10,
        price=55.8,
        order_type=OrderType.LIMIT,
    )
order_report_subscription()

"""
cancelar_orden = cancel_order_via_websocket(order["order"]["clientId"])

orden_cancelada = cancel_order_via_websocket(
        ticker='MERV - XMEV - AY24C - 48hs',
        side=Side.BUY,
        size=10,
        price=55.8,
        order_type=OrderType.LIMIT,
    )
"""
#Order Report Message Received: {'type': 'or', 'timestamp': 1714005193796, 'orderReport': {'orderId': None, 'clOrdId': '452565193309279', 'proprietary': 'PBCP', 'accountId': {'id': 'REM20096'}, 'instrumentId': {'marketId': 'ROFX', 'symbol': 'MERV - XMEV - AY24C - 48hs'}, 'price': 55.8, 'orderQty': 10, 'ordType': 'LIMIT', 'side': 'BUY', 'timeInForce': 'DAY', 'transactTime': '20240424-21:33:13.796-0300', 'status': 'PENDING_NEW', 'text': 'Enviada'}}
#>>>>>>>> afd2b7cf25567332d6bcda4d30ea4f9f7fc0931e:primary.py
#=======
# market_data_subscription(tickers=lista_simbolo, entries=entries)

# Subscribes to receive order report messages (default account will be used) **

order_report_subscription(account="REM20096", environment=Environment.REMARKET)

# send_order(lista_simbolo)

# reporte_de_cuenta = get_account_report(
#     account="REM20096", environment=Environment.REMARKET
# )

# posicion_de_cuenta = get_account_position(
#     account="REM20096", environment=Environment.REMARKET
# )

# order = send_order()
# print(reporte_de_cuenta,posicion_de_cuenta)
# ['MERV - XMEV - AGRO - 48hs', 'MERV - XMEV - CVH - 48hs', 'MERV - XMEV - MIRG - 48hs', 'MERV - XMEV - GOOGL - 48hs', 'MERV - XMEV - VALE - 48hs', 'MERV - XMEV - HMY - 48hs', 'MERV - XMEV - PBRC - 48hs', 'MERV - XMEV - APBRA - 48hs', 'MERV - XMEV - DICAC - 48hs', 'MERV - XMEV - TLC5O - 48hs', 'MERV - XMEV - BBD - 48hs', 'MERV - XMEV - YPCUD - 48hs', 'MERV - XMEV - VIST - 48hs', 'MERV - XMEV - YPFD - 48hs', 'MERV - XMEV - TGNO4 - 48hs', 'MERV - XMEV - BMA - 48hs', 'MERV - XMEV - LOMA - 48hs', 'MERV - XMEV - DICA - 48hs', 'MERV - XMEV - SAMI - 48hs', 'MERV - XMEV - ARC1O - 48hs', 'MERV - XMEV - IRCFO - 48hs', 'MERV - XMEV - CP17O - 48hs', 'MERV - XMEV - CS38O - 48hs', 'MERV - XMEV - AA37 - 48hs', 'MERV - XMEV - TSLA - 48hs', 'MERV - XMEV - GD30D - 48hs', 'MERV - XMEV - YMCQO - 48hs', 'MERV - XMEV - GD35 - 48hs', 'MERV - XMEV - COME - 48hs', 'MERV - XMEV - MGCHO - 48hs', 'MERV - XMEV - AY24 - 48hs', 'MERV - XMEV - AY24C - 48hs', 'MERV - XMEV - AMZND - 48hs', 'MERV - XMEV - AAPL - 48hs', 'MERV - XMEV - GD41D - 48hs', 'MERV - XMEV - AAPLD - 48hs', 'MERV - XMEV - AMZNC - 48hs', 'MERV - XMEV - MTCGO - 48hs', 'MERV - XMEV - YPCUO - 48hs', 'MERV - XMEV - PBRD - 48hs', 'MERV - XMEV - BBAR - 48hs', 'MERV - XMEV - CRES - 48hs', 'MERV - XMEV - GD30C - 48hs', 'MERV - XMEV - TXAR - 48hs', 'MERV - XMEV - AY24D - 48hs', 'MERV - XMEV - PBR - 48hs', 'MERV - XMEV - IRCGO - 48hs', 'MERV - XMEV - PAMP - 48hs', 'MERV - XMEV - AMZN - 48hs', 'MERV - XMEV - MELI - 48hs', 'MERV - XMEV - AER1D - 48hs', 'MERV - XMEV - ALUA - 48hs', 'MERV - XMEV - CP30O - 48hs', 'MERV - XMEV - AAPLC - 48hs', 'MERV - XMEV - TECO2 - 48hs', 'MERV - XMEV - CEPU - 48hs', 'MERV - XMEV - AL29C - 48hs', 'MERV - XMEV - SUPV - 48hs', 'MERV - XMEV - VALO - 48hs', 'MERV - XMEV - GGAL - 48hs', 'MERV - XMEV - CP30D - 48hs', 'MERV - XMEV - BYMA - 48hs', 'MERV - XMEV - DIA - 48hs', 'MERV - XMEV - EWZ - 48hs', 'MERV - XMEV - GD30 - 48hs', 'MERV - XMEV - SPY - 48hs', 'MERV - XMEV - GD41 - 48hs', 'MERV - XMEV - TGSU2 - 48hs', 'MERV - XMEV - KO - 48hs', 'MERV - XMEV - AL41 - 48hs', 'MERV - XMEV - TRAN - 48hs', 'MERV - XMEV - AL30C - 48hs', 'MERV - XMEV - AL30 - 48hs', 'MERV - XMEV - YMCIO - 48hs', 'MERV - XMEV - GOLD - 48hs', 'MERV - XMEV - AL29 - 48hs', 'MERV - XMEV - MSFT - 48hs', 'MERV - XMEV - DICAD - 48hs', 'MERV - XMEV - AL35 - 48hs', 'MERV - XMEV - MGC9O - 48hs', 'MERV - XMEV - AL29D - 48hs', 'MERV - XMEV - AL30D - 48hs']
for simbolo in lista_simbolo:
    print(f"Envio de orden para el ticker {simbolo}")
    order = send_order_via_websocket(
        ticker=simbolo,
        side=Side.BUY,
        size=10,
        order_type=OrderType.LIMIT,
        price=55.8,
    )
    break
# {'status': 'OK', 'order': {'clientId': '450835497387610', 'proprietary': 'PBCP'}}

# cancel_order = cancel_order(order["order"]["clientId"])

# Order Report Message Received: {'type': 'or', 'timestamp': 1714006211871, 'orderReport': {'orderId': '1714005765766846', 'clOrdId': '452565764314230', 'proprietary': 'PBCP', 'execId': '1713866408332482', 'accountId': {'id': 'REM20096'}, 'instrumentId': {'marketId': 'ROFX', 'symbol': 'MERV - XMEV - CEPU - 48hs'}, 'price': 55.8, 'orderQty': 10, 'ordType': 'LIMIT', 'side': 'BUY', 'timeInForce': 'DAY', 'transactTime': '20240424-21:42:45.766-0300', 'avgPx': 0, 'lastPx': 0, 'lastQty': 0, 'cumQty': 0, 'leavesQty': 10, 'status': 'NEW', 'text': 'ME_ACCEPTED', 'originatingUsername': 'PBCP'}}

# Order Report Message Received: {'type': 'or', 'timestamp': 1714006211868, 'orderReport': {'orderId': '1714005765064736', 'clOrdId': '452565764313704', 'proprietary': 'PBCP', 'execId': '1713866408332463', 'accountId': {'id': 'REM20096'}, 'instrumentId': {'marketId': 'ROFX', 'symbol': 'MERV - XMEV - YPFD - 48hs'}, 'price': 55.8, 'orderQty': 10, 'ordType': 'LIMIT', 'side': 'BUY', 'timeInForce': 'DAY', 'transactTime': '20240424-21:42:45.064-0300', 'avgPx': 0, 'lastPx': 0, 'lastQty': 0, 'cumQty': 0, 'leavesQty': 10, 'status': 'NEW', 'text': 'ME_ACCEPTED', 'originatingUsername': 'PBCP'}}

# print("------- estatus order ", get_order_status("452565764314230"))
#>>>>>>> afd2b7cf25567332d6bcda4d30ea4f9f7fc0931e
