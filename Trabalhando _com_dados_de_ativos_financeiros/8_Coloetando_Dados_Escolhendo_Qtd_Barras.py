from datetime import datetime
import MetaTrader5 as mt5
import pytz
import pandas as pd
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1500)
timezone = pytz.timezone("ETC/UTC")
data_hoje = datetime.today().strftime('%Y-%m-%d')
data_hoje_pregao = data_hoje + "-10:00:00"
print(data_hoje)
print(data_hoje_pregao)
print('------------------------------')
diff_inicio_pregao = datetime.today() - pd.Timestamp(data_hoje_pregao)
print(diff_inicio_pregao)
minutos = 5
quant_barras = int(diff_inicio_pregao.total_seconds()/(minutos*60))
print(diff_inicio_pregao)
print(quant_barras)
mt5.initialize()
ativo = "AUDUSD"
barras = mt5.copy_rates_from(ativo, mt5.TIMEFRAME_M5, datetime.today(),quant_barras)
barras_frame = pd.DataFrame(barras)
barras_frame['time']=pd.to_datetime(barras_frame['time'],unit='s')
print('xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx')
print(barras_frame)
barras_hoje = barras_frame[barras_frame['time'] >= data_hoje_pregao].reset_index(drop = True)
print('yyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyy')
print(barras_hoje)
#%%
