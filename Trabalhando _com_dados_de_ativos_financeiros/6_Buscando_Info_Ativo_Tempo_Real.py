import MetaTrader5 as mt5
import time
#Quando for coletar informações de algum ativo, é necessário
# que ele esteja na janela de observação de mercado
mt5.initialize()
ativo = "AUDUSD"
while(True):
    time.sleep(2)
    mt5.symbol_select(ativo)
    print(mt5.symbol_info_tick(ativo).last)
mt5.shutdown()