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
    df_data = pd.read_csv(filename, sep=',', header=0)
    df_data['Date'] = pd.to_datetime(df_data['Date'])
    df_data = df_data.set_index('Date')
    # print df_data
    df_data = df_data[~df_data['Close'].isin(['null'])]
    closing_data[indx_name] = pd.to_numeric(df_data['Close'])

closing_data = closing_data.dropna(how='any')
closing_data.sort_index(ascending=True, inplace=True)

# for i in closing_data['snp_close']:
#    if (isinstance(i, str)):
#        print(i)

log_return_data = pd.DataFrame()

log_return_data['nifty_log_return'] = np.log(closing_data['nifty_close']/closing_data['nifty_close'].shift())
log_return_data['snp_log_return']=np.log(closing_data['snp_close'] / closing_data['snp_close'].shift())
log_return_data['nyse_log_return']=np.log(closing_data['nyse_close'] / closing_data['nyse_close'].shift())
log_return_data['djia_log_return']=np.log(closing_data['djia_close'] / closing_data['djia_close'].shift())
log_return_data['nikkei_log_return']=np.log(closing_data['nikkei_close'] / closing_data['nikkei_close'].shift())
log_return_data['hangseng_log_return']=np.log(closing_data['hangseng_close'] / closing_data['hangseng_close'].shift())
log_return_data['dax_log_return']=np.log(closing_data['dax_close'] / closing_data['dax_close'].shift())
log_return_data['aord_log_return']=np.log(closing_data['aord_close'] / closing_data['aord_close'].shift())

log_return_data['nifty_log_return_positive']=0
log_return_data.ix[log_return_data['nifty_log_return'] >= 0, 'nifty_log_return_positive']=1
log_return_data['nifty_log_return_negative']=0
log_return_data.ix[log_return_data['nifty_log_return'] < 0, 'nifty_log_return_negative']=1
log_return_data['Date']=closing_data.index.values

training_test_data=pd.DataFrame(
    columns=[
        'Date', 'nifty_log_return_positive', 'nifty_log_return_negative',
        'nifty_log_return_1', 'nifty_log_return_2', 'nifty_log_return_3',
        'snp_log_return_1', 'snp_log_return_2', 'snp_log_return_3',
        'nyse_log_return_1', 'nyse_log_return_2', 'nyse_log_return_3',
        'djia_log_return_1', 'djia_log_return_2', 'djia_log_return_3',
        'nikkei_log_return_0', 'nikkei_log_return_1', 'nikkei_log_return_2',
        'hangseng_log_return_0', 'hangseng_log_return_1', 'hangseng_log_return_2',
        #'ftse_log_return_0', 'ftse_log_return_1', 'ftse_log_return_2',
        'dax_log_return_0', 'dax_log_return_1', 'dax_log_return_2',
        'aord_log_return_0', 'aord_log_return_1', 'aord_log_return_2'])

for i in range(7, len(log_return_data)):
    nifty_log_return_positive=log_return_data['nifty_log_return_positive'].ix[i]
    nifty_log_return_negative=log_return_data['nifty_log_return_negative'].ix[i]
    nifty_log_return_1 = log_return_data['nifty_log_return'].ix[i-1]
    nifty_log_return_2 = log_return_data['nifty_log_return'].ix[i-2]
    nifty_log_return_3 = log_return_data['nifty_log_return'].ix[i-3]
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
         'nifty_log_return_positive': nifty_log_return_positive,
         'nifty_log_return_negative': nifty_log_return_negative,
         'nifty_log_return_1':nifty_log_return_1,
         'nifty_log_return_2':nifty_log_return_2,
         'nifty_log_return_3':nifty_log_return_3,
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

closing_data['nifty_close'] = closing_data['nifty_close'].shift()
closing_data['nyse_close'] = closing_data['nyse_close'].shift()
closing_data['snp_close'] = closing_data['snp_close'].shift()
closing_data['aord_close'] = closing_data['aord_close'].shift()
closing_data['hangseng_close'] = closing_data['hangseng_close'].shift()
closing_data['nikkei_close'] = closing_data['nikkei_close'].shift()
closing_data['djia_close'] = closing_data['djia_close'].shift()
closing_data['dax_close'] = closing_data['dax_close'].shift()

training_test_data=training_test_data.set_index('Date')
closing_data=pd.merge(training_test_data, closing_data, left_index=True, right_index=True, how='outer')
closing_data=closing_data.dropna(how='any')

# print(closing_data)

for index, row in closing_data.iterrows():

    db.finance.insert({'date': index.strftime('%Y-%m-%d'), 'close': [{'stock': 'nifty', 'value': row['nifty_close']},
                                                {'stock': 'nyse', 'value': row['nyse_close']},
                                                {'stock': 'snp', 'value': row['snp_close']},
                                                {'stock': 'aord', 'value': row['aord_close']},
                                                {'stock': 'hangseng', 'value': row['hangseng_close']},
                                                {'stock': 'nikkei', 'value': row['nikkei_close']},
                                                {'stock': 'djia', 'value': row['djia_close']},
                                                {'stock': 'dax', 'value': row['dax_close']}],
                                        'parameters': {'nifty_log_return_positive': row['nifty_log_return_positive'],
									         'nifty_log_return_negative': row['nifty_log_return_negative'],
									         'nifty_log_return_1': row['nifty_log_return_1'],
									         'nifty_log_return_2': row['nifty_log_return_2'],
									         'nifty_log_return_3': row['nifty_log_return_3'],
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


