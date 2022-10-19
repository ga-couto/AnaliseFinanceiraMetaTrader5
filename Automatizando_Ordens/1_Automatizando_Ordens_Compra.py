from datetime import datetime
import pandas as pd
import MetaTrader5 as mt5
import time
import numpy as np

#Configurar parâmetros da biblioteca pandas
pd.set_option('display.max_columns',500)
pd.set_option('display.width',1500)
pd.set_option('mode.chained_assignment', None)

horario_inicio_mercado = pd.Timestamp(datetime.today().strftime("%Y-%m-%d-") + "-10:00:00")
horario_fechamento_mercado = pd.Timestamp(datetime.today().strftime("%Y-%m-%d-")+ "-17:50:00")

ativo = "WINJ21"

mt5.initialize()
#Colocar o Ativo na observação de mercado para poder operar.
selecionado = mt5.symbol_select(ativo)

#Buscar
ultimo_preco = mt5.symbol_info_tick(ativo)
print(ultimo_preco)

def ordem_compra(ativo,quantidade):
    print('Ordem Enviada')
    #A documentação pede para faer isso logo abaixo "Nessafunção"
    lot = float(quantidade)
    symbol = ativo
    price = mt5.symbol_info_tick(symbol).last
    point = mt5.symbol_info(symbol).point
    deviation = 0

    #Comprar mercado é a mesma coisa que comprar útimo valor negociado.
    #Criando dicionário com as informação da requisção de compra
    request = {
        "action":       mt5.TRADE_ACTION_DEAL,
        "symbol":       symbol,
        "volume":       lot,
        "type":         mt5.ORDER_TYPE_BUY, #Estou comprando...
        "price":        price, #Último preço é o último valor negciado...
        "sl":           price - 200 * point,#"sl" Stop Los
        "tp":           price + 200 * point,# "tp" Take Proft
        "deviation":    deviation,
        "comment":      "Ordem de compra enviada",
        "type_time":    mt5.ORDER_TIME_GTC,
        "type_filling": mt5.ORDER_FILLING_RETURN #Tipo de preenchimento da ordem
        #Finalizado o dicionário com a requisição completa
    }
    #Preciso mandar essa requisição. Vou chamala de "resultado"
    resultado = mt5.order_send(request)
    return resultado #Aqui estou enviando a compra.

#Criar máquina de estados para verificar condições
while True:
    #Pegando horário atual
    hora_agora = datetime.now()
    #Verificando se estou dentro do horário válido
    to_dentro_horario = hora_agora >= horario_inicio_mercado and hora_agora<=horario_fechamento_mercado
    #Buscar total de ordens abertas
    ordens_abertas = mt5.symbols_total()
    #Buscando posicoes abertas
    posicoes_abertas = mt5.positions_total()
    print('Ordens abertas ', str(ordens_abertas), ' Testeeeee')
    print('Posições abertas ', str(posicoes_abertas), ' Testeeeee')

    #Para operar, só quero uma posição e uma ordem aberta.
    if (ordens_abertas == 0 and posicoes_abertas == 0):
        ordem_compra(ativo,1)
    else:
        print("Não foi possível comprar. As ordens e as posições não estão zeradas. :/")

    #Buscando as minhas posições
    info_posicoes = mt5.positions_get(symbol=ativo)
    print(info_posicoes)

    #Transformar as posições num dataframe "Excel do Python"
    df = pd.DataFrame(list(info_posicoes), columns=info_posicoes[0]._asdict().keys()) #Estou pegando as chaves "key" para transformar em colunas.
    print(df)
    df['time'] = pd.to_datetime(df['time'], unit='s')

    print(to_dentro_horario)
    time.sleep(2)