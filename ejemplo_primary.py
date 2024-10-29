from pyRofex import *

initialize(
    user="oadricabrera20096",
    password="nvdevU6$",
    account="REM20096",
    environment=Environment.REMARKET,
)

print(get_market_data("GGAL/OCT24"))

# _set_environment_parameter("proprietary",) minuto 28:45

print(get_market_data.__doc__)

todos_los_instrumentos= get_all_instruments()

print(f"primer instrumento: {todos_los_instrumentos.get('instruments')[0]}")

print(f"\nDetalle de un instrumento: {get_instrument_details('GGAL/OCT24')}")

for ins in todos_los_instrumentos.get('instruments'):
    print(ins)

print(f"\nhistórico de GGAL/JUN24: {get_trade_history('GGAL/JUN24','2023-05-01','2023-06-01')}")

#print(f"\n{get_market_data('PAMP/AGO24'),[MarketDataEntry.LAST],Environment.REMARKET}")

orden = send_order('GGAL/OCT24',side=Side.BUY,size=10,price=2555,order_type=OrderType.LIMIT)
print(f"\nenviar orden: {orden}")

print(f"\nenviar orden clientId: {orden}")

print(f"\nestado de la oden: {get_order_status(orden)}")