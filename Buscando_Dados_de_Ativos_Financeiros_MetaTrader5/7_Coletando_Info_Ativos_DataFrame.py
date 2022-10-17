from datetime import datetime
import MetaTrader5 as mt5
import pandas as pd
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1500)

mt5.initialize()
ativo = "AUDUSD"
barras = mt5.copy_rates_from(ativo, mt5.TIMEFRAME_H1,datetime.today(),10)#Selecionando 10 barras de 1 hora

print(barras)
print('-----------------------------------------------------------------------------------------------')
barras_frame = pd.DataFrame(barras)
print(barras_frame)

barras_frame['time'] = pd.to_datetime(barras_frame['time'], unit='s')
print('xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx')
print(barras_frame)
mt5.shutdown()