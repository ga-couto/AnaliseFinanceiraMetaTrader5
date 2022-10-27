import time
import random
import MetaTrader5 as mt5
import pandas as pd
from datetime import datetime
import time
import numpy as np

#Configurar parâmetros (opções) da biblioteca pandas
import talib

pd.set_option('display.max_columns',500)
pd.set_option('display.width',1500)
pd.set_option('mode.chained_assignment',None)

ATIVO = 'WINJ21'
mt5.initialize()
mt5.symbol_select(ATIVO)

stop_loss = 500
take_profit = 500

def ordem_compra():
    print('Ordem de compra Enviada')
    #A documentação pede para fazer isso logo abaixo "Nessa função"
    lot = float(1)
    symbol = ATIVO #--
    point = mt5.symbol_info(symbol).point
    price = mt5.symbol_info_tick(symbol).ask
    deviation = 20

    #Comprar mercado é a mesma coisa que comprar útimo valor negociado.
    #Criando dicionário com as informação da requisção de compra
    request = {
        "action":       mt5.TRADE_ACTION_DEAL,
        "symbol":       symbol,
        "volume":       lot,
        "type":         mt5.ORDER_TYPE_BUY, #Estou comprando...
        "price":        price, #Último preço é o último valor negciado...
        "sl":           price - stop_loss * point,#"sl" Stop Los
        "tp":           price + take_profit * point,# "tp" Take Profit
        "deviation":    deviation,
        "magic":        10032021,
        "comment":      "Ordem de compra enviada",
        "type_time":    mt5.ORDER_TIME_GTC,
        "type_filling": mt5.ORDER_FILLING_RETURN #Tipo de preenchimento da ordem
        #Finalizado o dicionário com a requisição completa
    }
    #Preciso mandar essa requisição. Vou chamala de "resultado"
    resultado = mt5.order_send(request)
    return resultado #Aqui estou enviando a compra.

def ordem_venda():
    print('Ordem de venda Enviada')
    #A documentação pede para fazer isso logo abaixo "Nessa função"
    lot = float(1)
    symbol = ATIVO #--
    point = mt5.symbol_info(symbol).point
    price = mt5.symbol_info_tick(symbol).bid
    deviation = 20

    #Criando dicionário com as informação da requisção de venda
    request = {
        "action":       mt5.TRADE_ACTION_DEAL,
        "symbol":       symbol,
        "volume":       lot,
        "type":         mt5.ORDER_TYPE_SELL, #Estou vendendo...
        "price":        price, #Último preço é o último valor negciado...
        "sl":           price - stop_loss * point,#"sl" Stop Los
        "tp":           price + take_profit * point,# "tp" Take Profit
        "deviation":    deviation,
        "magic":        10032021,
        "comment":      "Ordem de venda enviada",
        "type_time":    mt5.ORDER_TIME_GTC,
        "type_filling": mt5.ORDER_FILLING_RETURN #Tipo de preenchimento da ordem
        #Finalizado o dicionário com a requisição completa
    }
    #Preciso mandar essa requisição. Vou chamala de "resultado"
    resultado = mt5.order_send(request)
    return resultado

def ordem_fechamento(ativo,quantidade,ticket,type_order,magic,deviatio):
    #O "type_order" vai ser "0" ou "1". "0"=compra, "1"=venda.
    #Vamos fazer assim... Se eu tiver uma ordem de compra, abro uma ordem de venda.
    #Se eu tiveruma ordem de venda, abro uma ordem de compra.
    if(type_order==0):
        print('Ordem de Venda - Fechamento')
        request_fechamento = {
            "action": mt5.TRADE_ACTION_DEAL,
            "position": ticket,
            "symbol": ativo,
            "volume": quantidade,
            "deviation": deviatio,
            "magic": magic,
            "type": mt5.ORDER_TYPE_SELL, #"SELL" Porque estou vendendo...
            "price": mt5.symbol_info_tick(ativo).bid, #Vou vender no "bid"
            "type_time": mt5.ORDER_TIME_GTC,
            "type_filling": mt5.ORDER_FILLING_RETURN
        }
        resultado = mt5.order_send(request_fechamento)
        print(resultado)
    else:
        print('Ordem de Compra - Fechamento')
        request_fechamento = {
            "action": mt5.TRADE_ACTION_DEAL,
            "position": ticket,
            "symbol": ativo,
            "volume": quantidade,
            "deviation": deviatio,
            "magic": magic,
            "type": mt5.ORDER_TYPE_BUY,  # "BUY" Porque estou vendendo...
            "price": mt5.symbol_info_tick(ativo).ask, #Vou comprar no "ask"
            "type_time": mt5.ORDER_TIME_GTC,
            "type_filling": mt5.ORDER_FILLING_RETURN
        }
        resultado = mt5.order_send(request_fechamento)
        print(resultado)

#Coletar dados do ATIVO
df = pd.DataFrame()
df = mt5.copy_rates_from_pos(ATIVO,mt5.TIMEFRAME_M1,1,5000)
df = pd.DataFrame(df)
df['time'] = pd.to_datetime(df['time'], unit='s')
df = df.set_index('time') #Transformando "time" em index

print(df)

#Criar as médias
df['sma9'] = talib.EMA(df['close'].values,timeperiod=9)
df['sma21'] = talib.EMA(df['close'].values,timeperiod=21)
print(df)

while True:
    total_ordens = mt5.positions_total()
    dr = pd.DataFrame()
    dr = mt5.copy_rates_from_pos(ATIVO, mt5.TIMEFRAME_M1, 0, 1)#Pegar a útima barra. Uma só...
    dr = pd.DataFrame(dr)
    dr['time'] = pd.to_datetime(dr['time'], unit='s')
    dr = dr.set_index('time')  # Transformando "time" em index
    df = df.append(dr)
    df['sma9'] = talib.EMA(df['close'].values, timeperiod=9)
    df['sma21'] = talib.EMA(df['close'].values, timeperiod=21)
    df['signal'] = np.sign(df['ema9'] - df['ema21']) #Quero comprar quando a média menor estiver sobre a média maior.
    print(df)
    time.sleep(4)

    if (total_ordens == 0):
        if(df['signal'].iloc[-1] == 1):
            print(ordem_compra())#Tive que printar p poder funcionar
            total_ordens = mt5.positions_total()
        else:
            print(ordem_venda())
            total_ordens = mt5.positions_total()
    elif (total_ordens == 1):
        info_posicoes = mt5.positions_get(symbol=ATIVO)
        data_posicoes = pd.DataFrame(list(info_posicoes),columns=info_posicoes[0]._asdict().keys())
        if (data_posicoes['type'][0]==[0] and df['signal'].iloc[-1] == [-1]):
            print(ordem_fechamento(
                str(data_posicoes['symbol'][0]),
                float(data_posicoes['volume'][0]),
                int(data_posicoes['ticket'][0]),
                data_posicoes['type'][0],
                int(data_posicoes['magic'][0]),
                0))
            print(ordem_venda())
        if(data_posicoes['type'][0] == 1 and df['sigal'].iloc[-1] == 1):
            print(ordem_fechamento(
                str(data_posicoes['symbol'][0]),
                float(data_posicoes['volume'][0]),
                int(data_posicoes['ticket'][0]),
                data_posicoes['type'][0],
                int(data_posicoes['magic'][0]),
                0))
            print(ordem_compra())
    time.sleep(60)