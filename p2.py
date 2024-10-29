from pyRofex import *

# Set the the parameter for the REMARKET environment
# item 2-Llamado al método get token
initialize(
    user="oadricabrera20096",
    password="nvdevU6$",
    account="REM20096",
    environment=Environment.REMARKET,
)


def market_data_handler(message):
    print("Market Data Message Received: {0}".format(message))


def order_report_handler(message):
    print("Order Report Message Received: {0}".format(message))
    if message["orderReport"]["status"] == "NEW":
        print(
            "Send to Cancel Order with clOrdID: {0}".format(
                message["orderReport"]["clOrdId"]
            )
        )
        cancel_order_via_websocket(message["orderReport"]["clOrdId"])

    elif message["orderReport"]["status"] == "CANCELLED":
        print(
            "Order with ClOrdID '{0}' is Cancelled.".format(
                message["orderReport"]["clOrdId"]
            )
        )


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
lista_simbolo = list()

# item 3-Solicitar lista de instrumentos
# almacenar el listado de instrumentos con su detalles en almacenamiento_de_detalles
almacenamiento_de_detalles = get_detailed_instruments()
almacenamiento_de_detalles = almacenamiento_de_detalles.get("instruments")

# # item 4- validamos los intrumentos de interes: vamos a trabajar con acciones y opciones de merval
for i in almacenamiento_de_detalles:
    simbolo = i.get("instrumentId").get("symbol")
    if simbolo.startswith("MERV") and simbolo.endswith("48hs"):
        lista_simbolo.append(simbolo)
        # print(simbolo)

entries = [MarketDataEntry.BIDS, MarketDataEntry.OFFERS, MarketDataEntry.LAST]
# order_report_subscription(account="REM9893", environment=Environment.REMARKET)

for simbolo in lista_simbolo:
    print(f"Envio de orden para el ticker {simbolo}")
    send_order_via_websocket(
        ticker=simbolo,
        side=Side.BUY,
        size=10,
        order_type=OrderType.LIMIT,
        price=55.8,
    )
    break
order_report_subscription()
