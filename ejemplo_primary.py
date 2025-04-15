from pyRofex import *

initialize(
    user="oadricabrera20096",
    password="nvdevU6$",
    account="REM20096",
    environment=Environment.REMARKET,
)

print(get_market_data("DLR/JUL25"))

# _set_environment_parameter("proprietary",) minuto 28:45

print(get_market_data.__doc__)

todos_los_instrumentos= get_all_instruments()

print(f"primer instrumento: {todos_los_instrumentos.get('instruments')[0]}")

print(f"\nDetalle de un instrumento: {get_instrument_details('DLR/JUL25')}")

for ins in todos_los_instrumentos.get('instruments'):
    print(ins)

#print(f"\nhistórico de DLR/JUL25: {get_trade_history('DLR/JUL25','2025-04-01','2025-04-11')}") *** Funciona bien ***

#print(f"\n{get_market_data('PAMP/AGO24'),[MarketDataEntry.LAST],Environment.REMARKET}")

orden = send_order('DLR/JUL25',side=Side.BUY,size=2,price=1310,order_type=OrderType.LIMIT)
print(f"\nenviar orden: {orden}")

print(f"\nenviar orden clientId: {orden}")

print(f"\nestado de la orden: {get_order_status(orden)}")