import MetaTrader5 as mt5

mt5.initialize()

simbolos = mt5.symbols_total()

if simbolos > 0:
    print(f'Total de simbolos encontrados: {simbolos}\n'
          f'Significa que podemos operar com {simbolos} ativos aqui no Meta Trader 5.\n'
          f'{simbolos} é a quantidade de ativos que existe vinculada à corretora em questão.')
else:
    print("Nenhum simbolo encontrado")

mt5.shutdown()