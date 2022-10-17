import MetaTrader5 as mt5

mt5.initialize()

simbolos = mt5.symbols_get()

contador = 0
for simbolo in simbolos:
    contador +=1
    print(f'{contador}. {simbolo.name}')
    if contador == 10:
        break
print('Qtd de simbolos:', len(simbolos))
print('-------------------------------------')
usd_simbolos = mt5.symbols_get("*USD*")
print('(',len(usd_simbolos), 'simbolos','com "USD")')


mt5.shutdown()