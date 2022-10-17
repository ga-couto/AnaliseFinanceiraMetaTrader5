from datetime import datetime
import pandas as pd
import MetaTrader5 as mt5
from pylab import mpl, plt
import numpy as np
#import matplotlib.pyplot as plt
print('Backtesting utilizando a estratégia de cruzamento de médias "Média curta" e "Média Longa".\n'
      'Para resumir, a ideia é pegar a média de várias linhas.\nMédia curta, pega poucas linhas.\n'
      'Média longa, pega mais linhas que a média curta.')
print()
print()
#Configurar parâmetros para plotagem nográfico
plt.style.use('seaborn-v0_8')
mpl.rcParams['savefig.dpi'] = 300
mpl.rcParams['font.family'] = 'serif'

#Configurar parâmetros da biblioteca pandas
pd.set_option('display.max_columns',500)
pd.set_option('display.width',1500)
pd.set_option('mode.chained_assignment', None)

mt5.initialize()
ativo = 'AUDUSD'
barras = mt5.copy_rates_from(ativo, mt5.TIMEFRAME_D1,datetime.today(),5000)

#print(barras)

print('Tranformando os dados num dataframe e ajusatndo visualização do "time"')
data = pd.DataFrame(barras)
data['time'] = pd.to_datetime(data['time'], unit='s')
print(data)

print('Criando colunas "SMA"')
data['SMACURTA'] = data['close'].rolling(43).mean()
data['SMALONGA'] = data['close'].rolling(252).mean()
data.dropna(inplace=True)
print(data)

print('Selecionando as colunas que preciso')
data = data[['time','close','SMACURTA','SMALONGA']]
print(data)

print('Transformar "time" em index do dataframe')
data = data.set_index('time')
print(data)

print('---')
data.plot(title = "Média de 43 e 252 do Ativo: "+ ativo,figsize=(20,12))
#plt.show()#Para mostrar o gráfico, descomentar 'plt.show'
print(data)

#Vamos ver qual o resultado dessa estratégia logo abaixo.
"""Toda vez que a SMA curta corta a SMA loga para cima, eu compro (Entro comprando).
    Toda vez que a SMA curta corta a SMA loga para baixo, eu entro vendido (Vendo).
    A ideia é estar comprando todas as vezes que o retorno estiver
        acima da média e vendendo quando estiver abaixo."""
print('Defirnir em qual posição estarei para poder entrar com a comra/venda."1"=compra  /  "-1"=vende')
#'1'=compra  /  '-1'=vende
data['Posicao'] = np.where(data['SMACURTA'] > data['SMALONGA'], 1, -1)
print(data)

data['Posicao'] = data['Posicao'].shift(1)
data.dropna(inplace=True)
print(data)

print('Mostrando a posição no gráfico plotado (1 compra, -1 vende).')
data.plot(figsize=(20,12),secondary_y='Posicao')
print(data)
#plt.show()#Para mostrar o gráfico, descomentar 'plt.show'

#Vamos verificar se essa estratégia é lucrativa ou não. Iremos calcular os retornos logo abaixo.
print('Calculando retorno sem a estratégia, ainda...')
data['Retornos'] = np.log(data['close']/data['close'].shift(1))
data.dropna(inplace=True)
print(data)

#Quando eu tiver uma posição vendida"-1" e o "Retorno" negativo, multiplico o Retorno por "-1" para que eu tenha um ganho.
print('Quando eu tiver uma posição vendida"-1" e o "Retorno" negativo, multiplico o Retorno por "-1" para que eu tenha um ganho.')
print('Calcular o retorno de uma posição vendida')
data['Retorno Estratégia'] = data['Posicao'] * data['Retornos']
print(data)

print('Calcular retornos simples. Ainda não estou calculando o retorno de forma logarítimica...')
print('"Ex: Retornos -0.20 <=> Retornos 20% ')
retorno_simples = data[['Retornos','Retorno Estratégia']].sum()
print(retorno_simples)

print('Calcular retornos de forma logarítimica')
retorno_log = data[['Retornos','Retorno Estratégia']].sum().apply(np.exp) -1
print(retorno_log)
print('Finalizei o backtesting utilizando a estratégia de cruzamento de médias "Média curta" e "Média Longa".')
print('-----------------------------------')

print('Plotar o gráfico com o retorno dessa estratégia')
data[['Retornos','Retorno Estratégia']].cumsum().apply(np.exp).plot(figsize=(20,12))
print(data)
plt.show()