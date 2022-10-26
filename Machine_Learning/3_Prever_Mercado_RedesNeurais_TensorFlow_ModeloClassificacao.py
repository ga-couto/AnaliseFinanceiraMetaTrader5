import MetaTrader5 as mt5
from datetime import datetime
import time
import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
import talib
import seaborn as sns
import statsmodels.api as sm
from sklearn.neural_network import MLPClassifier
import tensorflow as tf
from keras.models import Sequential
from keras.layers import Dense
from keras.optimizers import Adam, RMSprop
import random


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
df = df.set_index('time') #Transformando "time" em index

#Vamos trabalhar com modelo de classificação do machine Learn. Prevendo o futuro...
#A ideia é saber se o mercado futuro estará positivo ou negativo.

#Primeiro, irei calcular os retornos.   "df['close'].shift(1)" => próximo retorno...
df['return'] = np.log(df['close']/df['close'].shift(1)) #"pct_change" calcula os retornos percentuais. Aqui, iremos calcular retornos logaritmicos.
df.dropna(inplace=True)#Utilizei o "inplace=True" para deletar a primeira linha "A primeira linha vai ficar com NaN, por isso irei deletar".
print(df)

#Num outro modelo de regressão, empacotei 5 dias para prever os próximos 5 dias.
#Nesse modelo, irei pegar alguns dias passados para prever um único dia futuro(amanhã).

#Buscando dias passados
cols = []
lags = 5 #Quantidade de dias
for lag in range(1,lags+1):
    col = f'lag_{lag}'
    df[col] = df['return'].shift(lags) #Estou pegando o retorno e puxando para a distância de dias do pacote. O pacote é o pacote de dias passados.
    cols.append(col)
df.dropna(inplace=True)#Utilizei o "inplace=True" para deletar a primeira linha "A primeira linha vai ficar com NaN, por isso irei deletar".
print(df)

variaveis_uteis = ['close','return'] + cols
df_new = df[variaveis_uteis]
df_new['direction'] = np.where(df_new['return']>0,1,0)
print(df_new)
#O DataFrame que irei utilizar para prever está pronto. Eu posso adicionar diversas colunas para melhorar essa estratégia.

#Iniciar a criação da rede neural.
#O "Adam" é um otimizador. Ele aprende um baseado num "RATE". Ele vai mudar as variaveis para achar um ponto ótimo.
optimizer = Adam(learning_rate=0.0001)
def set_seeds(seed = 100):
    random.seed(seed)
    np.random.seed(seed)
    tf.random.set_seed(seed)
set_seeds()

#Criar meu modelo
#O modelo sequÊncial abaixo pode ser alterado(adicionar mais camadas) para esperimentar outras opções com essa estratégia.
model = Sequential()
#Adicionar as camadas de neurônios.
#Os numeros abaixo podem ser alterados. Faz parte da estratégia de mmodelo neural
#"relu" é uma força de ativação
#"input_shape é o tamanho das variáveis
model.add(Dense(64,
                 activation='relu',
                 input_shape=(lags,)))

#Adicionar mais uma camada
model.add(Dense(64,
           activation='relu'))

#Adicionar uma útima camada, que é de output. Quero saber um valor entre 0 e 1.
model.add(Dense(1,
                activation='sigmoid'))

#Vou compilar agora. Estou usando "accuracy" por ser um modelo de classificação
model.compile(optimizer = optimizer,
              loss='binary_crossentropy',
              metrics=['accuracy']) #optimizer q estou usando é o Adam.
#Aqui ja tenho o modelo de aprendizagem de rede neural

#Vou definir agora os dados de teste e os dados de treino.
cutoff = '2022-01-01' #Limite até onde pego meus dados de treino e teste
training_data = df_new[df.index < cutoff].copy()#"copy para copiar esse valor

#Para normalizar os valores, irei definir a média e o desvio padrão
media = training_data.mean()
desvio = training_data.std()

#Criar outro dataframe de treinamento "normalizado"
training = (training_data - media) / desvio
print(training)
teste_data = df_new[df_new.index >= cutoff].copy()
teste = teste_data - media /desvio
print(teste)

#Treinar meu modelo.
#"epochs"=quantas vezes meu modelo vai aprender...
#"validation_split=0.2" = estou usando 20% dos meus dados de treino
#"shuffle=False" = não fortear os dados.
print(time)#Só p ver...
model.fit(training_data[cols],
          training_data['direction'],
          epochs = 50,
          verbose=True,
          validation_split=0.2,
          shuffle=False
          )
#Após treinamento. Resultado abaixo.
res = pd.DataFrame(model.history.history)
print(res)
res[['accuracy','val_accuracy']].plot(figsize=(10,6),style= '--')


model.evaluation(training[cols],training_data['direction'])

#Agora precisamo verificar como ficou essa estratégia.
#Criar as predições
pred = np.where(model.predict(training[cols])>0.5,1,0)#Se for mais que 0.5, atribuo "1".

#Definir quais as posições que compra e venda. Basicamente o que foi feito num outro código "BackTestin". Estou fazendo um BackTesting abaixo.
training_data['prediction'] = np.where(pred > 0,1,0)
training_data['strategy'] = (training_data['prediction'] * training_data['return'])
training_data[['return','strategy']].sum().apply(np.exp)
training_data[['return','strategy']].cumsum().apply(np.exp).plot(figsize=(10,6))

#Vamos ver agora os testes
model.evaluate(teste[cols],teste_data['direction'])
pred = np.where(model.predict(teste[cols]) > 0.5 ,1,0)
teste_data['prediction'] = np.where(pred>0,1,-1)
teste_data['strategy'] = (teste_data['prediction'] * teste_data['return'])
teste_data[['return','strategy']].sum().apply(np.exp)
teste_data[['return','strategy']].cumsum().apply(np.exp).plot(figsize=(10,6))
