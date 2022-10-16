import MetaTrader5 as mt5

mt5.initialize()
ativo = "AUDUSD"
simb_selecionado = mt5.symbol_select(ativo,True)
info_simbolo = mt5.symbol_info(ativo)
print(info_simbolo)
info_simbolo_dic = info_simbolo._asdict()
for ch in info_simbolo_dic:
    print(f'{ch} <-> {info_simbolo_dic[ch]}')
print('-----------')

print(f'{ativo}: spread',info_simbolo.spread)

print('-----------')

info_simbolo_dict = mt5.symbol_info(ativo)._asdict()
print(info_simbolo_dict)
for prop in info_simbolo_dict:
    print(f'{prop} <-> {info_simbolo_dict[prop]}')


mt5.shutdown()