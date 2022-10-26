import MetaTrader5 as mt5
from datetime import datetime
import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
import talib
import seaborn as sns
import statsmodels.api as sm

#Configurar parâmetros da biblioteca pandas
pd.set_option('display.max_columns',500)
pd.set_option('display.width',1500)
pd.set_option('mode.chained_assignment',None)

#Importar dados do "Ativo"
ATIVO = "PETR4"
mt5.initialize()
mt5.symbol_select(ATIVO)

df = mt5.copy_rates_from_pos(ATIVO,mt5.TIMEFRAME_D1,0,5000)
df = pd.DataFrame(df)
df['time'] = pd.to_datetime(df['time'], unit='s')


print(df)

df['close'].plot(label="PETR4", legend=True)
plt.show()
plt.clf()

#Plotar retornos em forma de histograma
df['close'].pct_change().plot.hist(bins=50)
plt.show()
plt.clf()

# O objetivo do código abaixo é buscar retornos da póxima semana.
pacote_de_dias = 5

df['dias_no_futuro'].shift(-pacote_de_dias)
df['dias_no_futuro_retorno'] = df['dias_no_futuro'].pct_change(pacote_de_dias)
df['dias_atuais_retorno'] = df['close'].pct_change(pacote_de_dias)
df = df.dropna()
correlacao = df[['dias_atuais_retorno','dias_no_futuro_retorno']].corr()
print("Correlação: ", str(correlacao))
print(df.tail(10))

#Criar Indicadores. Irei utilizar a biblioteca Tailb
df['obv'] = talib.OBV(df['close'],df['real_volume'])

#Criar uma lista com algumas variáveis para analisar
feature_names = ['dias_atuais_retorno','obv'] #Estou buscando algumas variáveis para estudar e tentar encontrar padrões.
for n in [2,7,9,21,50,20]:
    #Criar média móvel exponencial
    df['mme'+str(n)] = talib.EMA(df['close'].valores,timeperiod = n)

    #Criar rsi
    df['rsi'+str(n)] = talib.RSI(df['close'].values,timeperiod= n)

    feature_names = feature_names +['mme'+str(n),'rsi'+str(n)]
df = df.dropna()#Retira os NaN

#Definir quais variáveis que estou buscando para prever. Basicamente irei copiar somente as variáveis que me interessam para não perder o "df"
features = df[feature_names] #Essa variável estou buscando para me ajudar a prever
target = df['dias_no_futuro_retorno']
features_e_target = ['dias_no_futuro_retorno'] + feature_names
features_e_target_df = df[features_e_target]

#Correlação entre essas variáveis que estou buscando do "df"
corr = features_e_target_df.corr()
print(corr)

#Plotar a correlação
sns.heatmap(corr,annot=True,annot_kwx={"size": 5})
plt.yticks(rotation=0,size = 8)
plt.xticks(rotation=90,size = 8)
plt.tight_layout()
plt.show()
plt.clf()

#Após analisar as correlações, irei colocar abaixo os rsi "mais forte"
plt.scatter(df['dias_no_futuro_retorno',df['rsi9']])
plt.show()
plt.clf()
#Observar que pode ser que não tenha nenhuma correlação significativa...


linear_features = sm.add_constant(features)
tamanho_treinamento = int(0.85*features.shape[0])
variaveis_treinamento = linear_features[:tamanho_treinamento]
alvo_treinamento = target[:tamanho_treinamento]

variaveis_teste = linear_features[tamanho_treinamento:]
alvo_teste = target[tamanho_treinamento:]


#Criar meu modelo
modelo = sm.OLS(alvo_treinamento,variaveis_treinamento)
resultado = modelo.fit()
print(resultado.pvalues)

#Tentar prever os resultados
previsoes_treinamento = resultado.predict(variaveis_treinamento)
previsoes_teste = resultado.predict(variaveis_teste)

plt.scatter(previsoes_treinamento,alvo_treinamento,alpha=0.2,color='b',label = 'Treinamento')
plt.scatter(previsoes_teste,alvo_teste,alpha=0.2,color='r',label='Teste')
xmin,xmax = plt.xlim()
plt.plot(np.arange(xmin,xmax,0.01),np.arange(xmin,xmax,0.01),c='k')

plt.xlabel('Previsoes')
plt.ylabel('Reais')
plt.legend()

plt.show()