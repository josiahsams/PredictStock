from pymongo import MongoClient
# pprint library is used to make the output look more pretty
from pprint import pprint

import pandas as pd
import numpy as np
import os
import sys
import glob
import datetime

# connect to MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client.joetest

closing_data = pd.DataFrame()
path = "./data/"

for filename in glob.glob(os.path.join(path, '*.csv')):
    # print filename
    indx_name = filename.split('_')[1].split('.')[0].lower()
    indx_name += '_close'
    # print indx_name
    df_data = pd.read_csv(filename, sep=',', header=0).set_index('Date')
    # print df_data
    closing_data[indx_name] = df_data['Close']

closing_data = closing_data.dropna(how='any')
closing_data.sort_index(ascending=True, inplace=True)

# sys.exit(0)

log_return_data = pd.DataFrame()

# tmp = pd.DataFrame()
# tmp[0] = closing_data['snp_close']
# tmp[1] = closing_data['snp_close'].shift(1)
# tmp[2] = closing_data['snp_close'].shift(2)

# tmp1 = pd.DataFrame()
# for i in range(2, len(tmp)):
# 	da = [tmp[0].ix[i], tmp[1].ix[i], tmp[2].ix[i]]
# 	# tmp1 = tmp1.append('past', pd.DataFrame(np.array[tmp[0].ix[i], tmp[1].ix[i], tmp[2].ix[i]]))
# 	tmp1 = tmp1.append({'past', pd.DataFrame(da)})

# print(tmp1)
# sys.exit(0)

# log_return_data['past']=[closing_data['snp_close'], closing_data['snp_close'].shift(), closing_data['snp_close'].shift(2)]
log_return_data['snp_log_return']=np.log(closing_data['snp_close'] / closing_data['snp_close'].shift())
log_return_data['nyse_log_return']=np.log(closing_data['nyse_close'] / closing_data['nyse_close'].shift())
log_return_data['djia_log_return']=np.log(closing_data['djia_close'] / closing_data['djia_close'].shift())
log_return_data['nikkei_log_return']=np.log(closing_data['nikkei_close'] / closing_data['nikkei_close'].shift())
log_return_data['hangseng_log_return']=np.log(closing_data['hangseng_close'] / closing_data['hangseng_close'].shift())
# log_return_data['ftse_log_return'] = np.log(closing_data['ftse_close']/closing_data['ftse_close'].shift())
log_return_data['dax_log_return']=np.log(closing_data['dax_close'] / closing_data['dax_close'].shift())
log_return_data['aord_log_return']=np.log(closing_data['aord_close'] / closing_data['aord_close'].shift())

log_return_data['snp_log_return_positive']=0
log_return_data.ix[log_return_data['snp_log_return'] >= 0, 'snp_log_return_positive']=1
log_return_data['snp_log_return_negative']=0
log_return_data.ix[log_return_data['snp_log_return'] < 0, 'snp_log_return_negative']=1
log_return_data['Date']=closing_data.index.values

training_test_data=pd.DataFrame(
    columns=[
        'Date', 'snp_log_return_positive', 'snp_log_return_negative',
        'snp_log_return_1', 'snp_log_return_2', 'snp_log_return_3',
        'nyse_log_return_1', 'nyse_log_return_2', 'nyse_log_return_3',
        'djia_log_return_1', 'djia_log_return_2', 'djia_log_return_3',
        'nikkei_log_return_0', 'nikkei_log_return_1', 'nikkei_log_return_2',
        'hangseng_log_return_0', 'hangseng_log_return_1', 'hangseng_log_return_2',
        #'ftse_log_return_0', 'ftse_log_return_1', 'ftse_log_return_2',
        'dax_log_return_0', 'dax_log_return_1', 'dax_log_return_2',
        'aord_log_return_0', 'aord_log_return_1', 'aord_log_return_2'])

for i in range(7, len(log_return_data)):
    snp_log_return_positive=log_return_data['snp_log_return_positive'].ix[i]
    snp_log_return_negative=log_return_data['snp_log_return_negative'].ix[i]
    snp_log_return_1=log_return_data['snp_log_return'].ix[i - 1]
    snp_log_return_2=log_return_data['snp_log_return'].ix[i - 2]
    snp_log_return_3=log_return_data['snp_log_return'].ix[i - 3]
    nyse_log_return_1=log_return_data['nyse_log_return'].ix[i - 1]
    nyse_log_return_2=log_return_data['nyse_log_return'].ix[i - 2]
    nyse_log_return_3=log_return_data['nyse_log_return'].ix[i - 3]
    djia_log_return_1=log_return_data['djia_log_return'].ix[i - 1]
    djia_log_return_2=log_return_data['djia_log_return'].ix[i - 2]
    djia_log_return_3=log_return_data['djia_log_return'].ix[i - 3]
    nikkei_log_return_0=log_return_data['nikkei_log_return'].ix[i]
    nikkei_log_return_1=log_return_data['nikkei_log_return'].ix[i - 1]
    nikkei_log_return_2=log_return_data['nikkei_log_return'].ix[i - 2]
    hangseng_log_return_0=log_return_data['hangseng_log_return'].ix[i]
    hangseng_log_return_1=log_return_data['hangseng_log_return'].ix[i - 1]
    hangseng_log_return_2=log_return_data['hangseng_log_return'].ix[i - 2]
    dax_log_return_0=log_return_data['dax_log_return'].ix[i]
    dax_log_return_1=log_return_data['dax_log_return'].ix[i - 1]
    dax_log_return_2=log_return_data['dax_log_return'].ix[i - 2]
    aord_log_return_0=log_return_data['aord_log_return'].ix[i]
    aord_log_return_1=log_return_data['aord_log_return'].ix[i - 1]
    aord_log_return_2=log_return_data['aord_log_return'].ix[i - 2]
    training_test_data=training_test_data.append(
        {'Date': log_return_data['Date'].ix[i],
         'snp_log_return_positive': snp_log_return_positive,
         'snp_log_return_negative': snp_log_return_negative,
         'snp_log_return_1': snp_log_return_1,
         'snp_log_return_2': snp_log_return_2,
         'snp_log_return_3': snp_log_return_3,
         'nyse_log_return_1': nyse_log_return_1,
         'nyse_log_return_2': nyse_log_return_2,
         'nyse_log_return_3': nyse_log_return_3,
         'djia_log_return_1': djia_log_return_1,
         'djia_log_return_2': djia_log_return_2,
         'djia_log_return_3': djia_log_return_3,
         'nikkei_log_return_0': nikkei_log_return_0,
         'nikkei_log_return_1': nikkei_log_return_1,
         'nikkei_log_return_2': nikkei_log_return_2,
         'hangseng_log_return_0': hangseng_log_return_0,
         'hangseng_log_return_1': hangseng_log_return_1,
         'hangseng_log_return_2': hangseng_log_return_2,
         'dax_log_return_0': dax_log_return_0,
         'dax_log_return_1': dax_log_return_1,
         'dax_log_return_2': dax_log_return_2,
         'aord_log_return_0': aord_log_return_0,
         'aord_log_return_1': aord_log_return_1,
         'aord_log_return_2': aord_log_return_2},
        ignore_index=True)


# print(training_test_data)

training_test_data=training_test_data.set_index('Date')
closing_data=pd.merge(training_test_data, closing_data, left_index=True, right_index=True, how='outer')
closing_data=closing_data.dropna(how='any')

print(closing_data)

for index, row in closing_data.iterrows():

    db.finance.insert({'date': index, 'close': [{'stock': 'nyse', 'value': row['nyse_close']},
                                                {'stock': 'snp', 'value': row['snp_close']},
                                                {'stock': 'aord', 'value': row['aord_close']},
                                                {'stock': 'hangseng', 'value': row['hangseng_close']},
                                                {'stock': 'nikkei', 'value': row['nikkei_close']},
                                                {'stock': 'djia', 'value': row['djia_close']},
                                                {'stock': 'dax', 'value': row['dax_close']}],
                                        'parameters': {'snp_log_return_positive': row['snp_log_return_positive'],
									         'snp_log_return_negative': row['snp_log_return_negative'],
									         'snp_log_return_1': row['snp_log_return_1'],
									         'snp_log_return_2': row['snp_log_return_2'],
									         'snp_log_return_3': row['snp_log_return_3'],
									         'nyse_log_return_1': row['nyse_log_return_1'],
									         'nyse_log_return_2': row['nyse_log_return_2'],
									         'nyse_log_return_3': row['nyse_log_return_3'],
									         'djia_log_return_1': row['djia_log_return_1'],
									         'djia_log_return_2': row['djia_log_return_2'],
									         'djia_log_return_3': row['djia_log_return_3'],
									         'nikkei_log_return_0': row['nikkei_log_return_0'],
									         'nikkei_log_return_1': row['nikkei_log_return_1'],
									         'nikkei_log_return_2': row['nikkei_log_return_2'],
									         'hangseng_log_return_0': row['hangseng_log_return_0'],
									         'hangseng_log_return_1': row['hangseng_log_return_1'],
									         'hangseng_log_return_2': row['hangseng_log_return_2'],
									         'dax_log_return_0': row['dax_log_return_0'],
									         'dax_log_return_1': row['dax_log_return_1'],
									         'dax_log_return_2': row['dax_log_return_2'],
									         'aord_log_return_0': row['aord_log_return_0'],
									         'aord_log_return_1': row['aord_log_return_1'],
									         'aord_log_return_2': row['aord_log_return_2']}})

docs=db.finance.find({'date': '1990-12-21'})
for entry in docs:
    pprint(entry)


# closing_data = pd.DataFrame()
# path = "./data/"
# print(path + 'YAHOO-INDEX_SNP.csv')
# snp = pd.read_csv(path + 'YAHOO-INDEX_SNP.csv')
# snp = snp.set_index(pd.to_datetime(snp['Date']))[['Date', 'Close']]

# nyse = pd.read_csv(path + 'YAHOO-INDEX_NYSE.csv')
# nyse = nyse.set_index(pd.to_datetime(nyse['Date']))[['Date', 'Close']]

# # Merge the data
# data = pd.merge(snp, nyse, left_index=True, right_index=True, how='outer')
# data.drop('Date_x', axis=1, inplace=True)
# data.drop('Date_y', axis=1, inplace=True)

# data = data.rename(columns={'Close_x': 'snp'})
# data = data.rename(columns={'Close_y': 'nyse'})

# nikkei = pd.read_csv(path + 'YAHOO-INDEX_NIKKEI.csv')
# nikkei = nikkei.set_index(pd.to_datetime(nikkei['Date']))[['Date', 'Close']]

# # Merge the data
# data = pd.merge(data, nikkei, left_index=True, right_index=True, how='outer')

# hangseng = pd.read_csv(path + 'YAHOO-INDEX_HANGSENG.csv')
# hangseng = hangseng.set_index(pd.to_datetime(hangseng['Date']))[['Date', 'Close']]

# # Merge the data
# data = pd.merge(data, hangseng, left_index=True, right_index=True, how='outer')

# data.drop('Date_x', axis=1, inplace=True)
# data.drop('Date_y', axis=1, inplace=True)

# data = data.rename(columns={'Close_x': 'nikkei'})
# data = data.rename(columns={'Close_y': 'hangseng'})


# djia = pd.read_csv(path + 'YAHOO-INDEX_DJIA.csv')
# djia = djia.set_index(pd.to_datetime(djia['Date']))[['Date', 'Close']]

# # Merge the data
# data = pd.merge(data, djia, left_index=True, right_index=True, how='outer')

# dax = pd.read_csv(path + 'YAHOO-INDEX_DAX.csv')
# dax = dax.set_index(pd.to_datetime(dax['Date']))[['Date', 'Close']]

# # Merge the data
# data = pd.merge(data, dax, left_index=True, right_index=True, how='outer')

# data.drop('Date_x', axis=1, inplace=True)
# data.drop('Date_y', axis=1, inplace=True)

# data = data.rename(columns={'Close_x': 'djia'})
# data = data.rename(columns={'Close_y': 'dax'})


# aord = pd.read_csv(path + 'YAHOO-INDEX_AORD.csv')
# aord = aord.set_index(pd.to_datetime(aord['Date']))[['Date', 'Close']]

# # Merge the data
# data = pd.merge(data, aord, left_index=True, right_index=True, how='outer')

# data.drop('Date', axis=1, inplace=True)
# data = data.rename(columns={'Close': 'aord'})

# data.dropna(how='any', inplace=True)


# # Issue the serverStatus command and print the results
# serverStatusResult = db.command("serverStatus")
# pprint(serverStatusResult)
