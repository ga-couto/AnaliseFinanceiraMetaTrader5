import yfinance as yf
import datetime
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
#Compra na baixa, vende na alta
data = yf.download('PETR4.SA',start='2022-10-01', end= datetime.datetime.today(),progress = False)
print(data)

data_signal = pd.DataFrame(index = data.index)
print(data_signal)

data_signal['Preço Fechamento']  = data['Close']
print(data_signal)

data_signal['Diferença Diária'] = data_signal['Preço Fechamento'].diff()
print(data_signal)

data_signal['Sinal'] = np.where(data_signal['Diferença Diária'] > 0, 1.0, 0.0)
print(data_signal)

data_signal['Posições']= data_signal['Sinal'].diff()
print(data_signal)
print('- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -')
capital_inicial = 1000.0
posicoes  = pd.DataFrame(index=data_signal.index).fillna(0.0)
portifolio = pd.DataFrame(index=data_signal.index).fillna(0.0)
posicoes['PETR4'] = data_signal['Sinal']
portifolio['Posicoes'] = (posicoes.multiply(data_signal['Preço Fechamento'], axis=0)).cumsum()
portifolio['Dinheiro Investido'] = capital_inicial - (posicoes.diff().multiply(data_signal['Preço Fechamento'],axis=0)).cumsum()
portifolio['Total'] = portifolio['Posicoes'] + portifolio['Dinheiro Investido']
print(portifolio)


