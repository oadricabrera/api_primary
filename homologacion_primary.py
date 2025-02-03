from pyRofex import *
import schedule

def job():
    detalle_de_posicion = get_detailed_position(
    account="REM20096", environment=Environment.REMARKET
    )
    print(f"\n\Detalle de Cuenta: {detalle_de_posicion}")
    reporte_de_cuenta = get_account_report()
    print("#####\n\ Reporte de Cuenta ",reporte_de_cuenta)    

# Inicialización de la sesión
initialize(
    user="oadricabrera20096",
    password="nvdevU6$",
    account="REM20096",
    environment=Environment.REMARKET,
)
accion = "DLR/ENE25/FEB25" 
# Definición de los manejadores
def market_data_handler(message):
    simbolo= message.get("instrumentId").get("symbol")
    # Extraer precios y tamaños de OF y BI
    if message.get("marketData").get("BI") and (message.get("marketData").get("BI")[0].get("price") != message.get("marketData").get("OF")[0].get("price")):    
        _size_BI= message.get("marketData").get("BI")[0].get("size")
        _price_BI = message.get("marketData").get("BI")[0].get("price")
        _price_OF= message.get("marketData").get("OF")[0].get("price")
        _size_OF = message.get("marketData").get("OF")[0].get("size")
        SOJ.append({"simbolo":symbol,"precio_compra":_price_BI,"cantidad_compra":_size_BI,"precio_venta":_price_OF,"cantidad_venta":_size_OF})
        print(f"simbolo: {simbolo}'       '_size_BI:{_size_BI}'       '_price_BI: {_price_BI}'       '_price_OF: {_price_OF}'       '_size_OF:{_size_OF}")
        """
        # Buscar el símbolo en la lista SOJ y actualizar los valores
        for item in SOJ:
            if item["simbolo"] == simbolo:
                item["precio_compra"] = _size_BI  # Reemplazar el primer cero
                item["cantidad_compra"] = _price_BI  # Reemplazar el segundo cero
                item["precio_venta"] = _price_OF  # Reemplazar el tercer cero
                item["cantidad_venta"] = _size_OF  # Reemplazar el cuarto cero
                break
        """  
    # Imprimir para verificar
    print(f"\nActualizado: {simbolo}")
    for i in SOJ:
        if i.get("precio_compra") != i.get("precio_venta"):
            print(i.get("simbolo"), "   ", i.get("precio_compra"), "   ", i.get("cantidad_compra"), "   ", i.get("precio_venta"), "   ", i.get("cantidad_venta"))

    for symbol in SOJ[1:]:
        # Extraer los valores específicos de SOJ[0] y symbol
        valores_SOJ0 = list(SOJ[0].values())
        valores_symbol = list(symbol.values())
        
        # Crear la combinación con los valores deseados
        _lanzamiento_cubierto = [
            valores_SOJ0[0],  # Primer valor de SOJ[0] ('SOJ.ROS/NOV25 300 P')
            valores_SOJ0[2],  # Tercer valor de SOJ[0] (tercer cero)
            valores_SOJ0[3],  # Cuarto valor de SOJ[0] (cuarto cero)
            valores_symbol[0],  # Primer valor de symbol ('SOJ.ROS/NOV25 300 C')
            valores_symbol[1],  # Primer cero de symbol
            valores_symbol[2],  # Segundo cero de symbol
        ]

        print (f"_lanzamiento_cubierto: {_lanzamiento_cubierto}") if (valores_symbol[1] != valores_symbol[2]) else None

    print("\nMarket Data Message Received: {0}".format(message))

def order_report_handler(message):
    print("\nOrder Report Message Received: {0}".format(message))
    # 6-Handler will validate if the order is in the correct state (pending_new)
    print(f"\norder report handler {message}")
    if message["orderReport"]["status"] == "NEW":
        propietary = message["orderReport"]["proprietary"]
        # 6.1-We cancel the order using the websocket connection
        print("\nSend to Cancel Order with clOrdID: {0}".format(message["orderReport"]["clOrdId"]))
        cancel_order_via_websocket(message["orderReport"]["clOrdId"],propietary,environment=Environment.REMARKET,)
    # 7-Handler will receive an Order Report indicating that the order is cancelled (will print it)
    elif message["orderReport"]["status"] == "CANCELLED":
        print("\nOrder with ClOrdID '{0}' is Cancelled.".format(message["orderReport"]["clOrdId"]))

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

SOJ = list()
SOJA = list()
TRI = list()
lanzamientoCubierto = list()
mariposa=list()

#Quiero saber qué papeles están cotizando

almacenamiento_de_detalles = get_detailed_instruments()
almacenamiento_de_detalles = almacenamiento_de_detalles.get("instruments")

for i in almacenamiento_de_detalles:
    symbol = i['instrumentId']['symbol']
    if symbol.startswith('SOJ.ROS'):
        SOJA.append(symbol)
        #SOJ.append({"simbolo":symbol,"precio_compra":0,"cantidad_compra":0,"precio_venta":0,"cantidad_venta":0})
        
    elif symbol.startswith('TRI.ROS'):
        TRI.append(symbol)
"""
for symbol in SOJ[1:]:
    # Extraer los valores específicos de SOJ[0] y symbol
    valores_SOJ0 = list(SOJ[0].values())
    valores_symbol = list(symbol.values())
    
    # Crear la combinación con los valores deseados
    _lanzamiento_cubierto = [
        valores_SOJ0[0],  # Primer valor de SOJ[0] ('SOJ.ROS/NOV25 300 P')
        valores_SOJ0[2],  # Tercer valor de SOJ[0] (tercer cero)
        valores_SOJ0[3],  # Cuarto valor de SOJ[0] (cuarto cero)
        valores_symbol[0],  # Primer valor de symbol ('SOJ.ROS/NOV25 300 C')
        valores_symbol[1],  # Primer cero de symbol
        valores_symbol[2],  # Segundo cero de symbol
    ]
    
    lanzamientoCubierto.append(_lanzamiento_cubierto)

for i in SOJ:
    print(i.get("simbolo"),"   ",i.get("precio_compra"),"   ",i.get("cantidad_compra"),"   ",i.get("precio_venta"),"   ",i.get("cantidad_venta"))

print("\n")

for i in TRI:
    print(i)

# Imprimir las combinaciones
print("\nLanzamiento Cubierto")
for combo in lanzamientoCubierto:
    print(*combo)        #print("\t".join(combo))

# Crear combinaciones de tres elementos consecutivos
for i in range(len(TRI) - 2):
    _mariposa = [TRI[i], TRI[i + 1], TRI[i + 2]]
    mariposa.append(_mariposa)

# Imprimir las combinaciones
print("\nMariposa")
for group in mariposa:
    print("\t".join(group))
"""
# Suscripción a datos del mercado

_tickers = SOJA + TRI

market_data_subscription(
    tickers=_tickers,
    entries=[MarketDataEntry.BIDS, MarketDataEntry.OFFERS],
    depth=4
)

# Obtener reporte de cuenta
reporte_de_cuenta = get_account_report()

detalle_de_posicion = get_detailed_position(
    account="REM20096", environment=Environment.REMARKET
)
print(f"\n\nReporte de Cuenta: {reporte_de_cuenta}, \n\ndetalle de cuenta: {detalle_de_posicion}")
"""
# Enviar una orden
send_order_via_websocket(       
        ticker=accion,
        side=Side.BUY,
        size=10,
        price=1093,
        order_type=OrderType.LIMIT,
    )
"""
order_report_subscription(account="REM20096", environment=Environment.REMARKET) #¿Sirve?

schedule.every(10000).seconds.do(job)                    #schedule.every(10).seconds.do(job)
while True:
    schedule.run_pending()


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
