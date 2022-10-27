import time
import random
import MetaTrader5 as mt5
import pandas as pd

#Configurar parâmetros (opções) da biblioteca pandas
pd.set_option('display.max_columns',500)
pd.set_option('display.width',1500)
pd.set_option('mode.chained_assignment',None)

mt5.initialize()
ATIVO = 'WINJ21'
info_posicoes = mt5.positions_get(symbol=ATIVO)
total_ordens = mt5.positions_total()

# #Coletar dados do ATIVO
# df = mt5.copy_rates_from_pos(ATIVO,mt5.TIMEFRAME_M15,0,5000)
# df = pd.DataFrame(df)
# df['time'] = pd.to_datetime(df['time'], unit='s')
# df = df.set_index('time') #Transformando "time" em index
# df['diff_hl'] = df['high'] - df['low']
#print(df['diff_hl'].describe())

stop_loss = 500
take_profit = 500

tipo_de_ordem = [0,1]

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

while True:
    if total_ordens <= 5:
        print(f'Total de ordens: ', total_ordens)
        escolha = random.choice(tipo_de_ordem)
        if escolha == 0:
            print(ordem_compra()) #Tive que printar p poder funcionar
        else:
            print(ordem_venda()) #Tive que printar p poder funcionar
    else:
        print('Não fez nada')
    total_ordens = mt5.positions_total()
    time.sleep(15*60)
mt5.shutdown()