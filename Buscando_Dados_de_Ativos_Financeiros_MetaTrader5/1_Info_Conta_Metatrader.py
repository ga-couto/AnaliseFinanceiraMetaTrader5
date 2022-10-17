import MetaTrader5 as mt5
import pandas as pd
mt5.initialize()
info_conta = mt5.account_info()
info_conta_dic = info_conta._asdict()
for prop in info_conta_dic:
    print(f"{prop} = {info_conta_dic[prop]}")
print(info_conta_dic)

data_frame = pd.DataFrame(list(info_conta_dic.items()),columns=['property','value'])
print(data_frame)
mt5.shutdown()