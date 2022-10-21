import yfinance as yf
import datetime
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from prophet import Prophet

#Importando dados do "Ativo"
data = yf.download('PETR4.SA',start='2018-01-01', end=datetime.datetime.today())
print(data)

#Criando dataframe vazio
df = pd.DataFrame()
df['y'] = data['Close']
df['ds'] = data.index
df['ds'] = df['ds'].dt.tz_localize(None)

print(df)

modelo = Prophet(daily_seasonality=True)
modelo.fit(df)

futuro = modelo.make_future_dataframe(periods=35)
predictions = modelo.predict(futuro)
modelo.plot(predictions)
print(predictions.tail(n=50))