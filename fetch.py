import googlefinance.client as gf
from datetime import datetime
from pymongo import MongoClient
import pandas as pd
import numpy as np
import os
import sys

# client = MongoClient("mongodb://localhost:27017/")
client = MongoClient("mongodb://finseriesmongo:27017/")

db = client.joetest
rowCount = db.finance.count()
print("rowCount is {}".format(rowCount))

if (rowCount > 0):
    recentEntries = db.finance.find({}).sort([('date', -1)])[:4]
else:
    print("DB is empty. Can't proceed.")
    sys.exit(1)

ldate = datetime.strptime(recentEntries[0]['date'], '%Y-%m-%d')
print(ldate)
closing_data = pd.DataFrame()
index_array = []
date_array = []
nifty_array = []
nyse_array = []
snp_array = []
aord_array = []
hangseng_array = []
nikkei_array = []
djia_array = []
dax_array = []


# for entry in recentEntries[0]['close']:
#     index_array.append(entry['stock'])

for row in recentEntries:
    date_array.append(str(row['date']))
    for entry in row['close']:

        if (entry['stock'] == "nifty"):
            nifty_array.append(entry['value'])
        elif (entry['stock'] == "nyse"):
            nyse_array.append(entry['value'])
        elif (entry['stock'] == "snp"):
            snp_array.append(entry['value'])
        elif (entry['stock'] == "aord"):
            aord_array.append(entry['value'])
        elif (entry['stock'] == "hangseng"):
            hangseng_array.append(entry['value'])
        elif (entry['stock'] == "nikkei"):
            nikkei_array.append(entry['value'])
        elif (entry['stock'] == "djia"):
            djia_array.append(entry['value'])
        elif (entry['stock'] == "dax"):
            dax_array.append(entry['value'])


now = datetime.now()
diff = now - ldate

months = int(diff.days / 30) + (diff.days % 30 > 0)
print("DB is not updated for nearly", diff.days, "days")

# sys.exit(0)
# date = datetime(2018, 4, 11)  # Get date from db and insert here
# NIFTY 50 : NSE: NIFTY
# Dow Jones Industrial Average : INDEXDJX: .DJI
# S&P 500 Index : INDEXCBOE: .INX
# All Ordinaries AORD : INDEXASX: XAO
# NYSE Composite Index : INDEXNYSEGIS: NYA
# DAX PERFORMANCE-INDEX : INDEXDB: DAX
# Hang Seng Index: INDEXHANGSENG: HSI
# Nikkei 225: INDEXNIKKEI: NI225
param = [{'q': 'NIFTY', 'i': "86400", 'x': "NSE"},
         {'q': '.DJI', 'i': "86400", 'x': "INDEXDJX"},
         {'q': '.INX', 'i': "86400", 'x': "INDEXSP"},
         {'q': 'XAO', 'i': "86400", 'x': "INDEXASX"},
         {'q': 'NYA', 'i': "86400", 'x': "INDEXNYSEGIS"},
         {'q': 'DAX', 'i': "86400", 'x': "INDEXDB"},
         {'q': 'HSI', 'i': "86400", 'x': "INDEXHANGSENG"},
         {'q': 'NI225', 'i': "86400", 'x': "INDEXNIKKEI"}]

dg = gf.get_prices_data(param, str(months) + "M")

print("Date\t\tNIFTY\t\tDJX\t\tSP500\t\tAORD\t\tNYSE\t\tDAX\t\tHANGSENG\t\tNIKKEI")

dg['NYA_Close'] = dg['NYA_Close'].shift(-1)
dg['.INX_Close'] = dg['.INX_Close'].shift(-1)
dg['.DJI_Close'] = dg['.DJI_Close'].shift(-1)

# dg['NIFTY_Close'] = dg['NIFTY_Close'].shift()
# dg['XAO_Close'] = dg['XAO_Close'].shift()
# dg['DAX_Close'] = dg['DAX_Close'].shift()
# dg['HSI_Close'] = dg['HSI_Close'].shift()
# dg['NI225_Close'] = dg['NI225_Close'].shift()

for index, row in dg.iterrows():
    if index > datetime.date(ldate):
        date_array.append(str(index))
        row1 = dg.ix[index]
        nifty_array.append(row1['NIFTY_Close'])
        nyse_array.append(row1['NYA_Close'])
        snp_array.append(row1['.INX_Close'])
        aord_array.append(row1['XAO_Close'])
        hangseng_array.append(row1['HSI_Close'])
        nikkei_array.append(row1['NI225_Close'])
        djia_array.append(row1['.DJI_Close'])
        dax_array.append(row1['DAX_Close'])

        print(index.strftime('%m/%d/%Y'), "\t", row1['NIFTY_Close'], "\t",  row1['.DJI_Close'], "\t",
              row1['.INX_Close'], "\t",  row1['XAO_Close'], "\t", row1['NYA_Close'], "\t",
              row1['DAX_Close'], "\t", row1['HSI_Close'], "\t",  row1['NI225_Close'])

closing_data['date'] = date_array
closing_data['nifty_close'] = nifty_array
closing_data['nyse_close'] = nyse_array
closing_data['snp_close'] = snp_array
closing_data['aord_close'] = aord_array
closing_data['hangseng_close'] = hangseng_array
closing_data['nikkei_close'] = nikkei_array
closing_data['djia_close'] = djia_array
closing_data['dax_close'] = dax_array
closing_data = closing_data.set_index('date')

closing_data = closing_data.dropna(how='any')
closing_data.sort_index(ascending=True, inplace=True)

# print(closing_data)

log_return_data = pd.DataFrame()

log_return_data['nifty_log_return'] = np.log(
    closing_data['nifty_close'] / closing_data['nifty_close'].shift())
log_return_data['snp_log_return'] = np.log(
    closing_data['snp_close'] / closing_data['snp_close'].shift())
log_return_data['nyse_log_return'] = np.log(
    closing_data['nyse_close'] / closing_data['nyse_close'].shift())
log_return_data['djia_log_return'] = np.log(
    closing_data['djia_close'] / closing_data['djia_close'].shift())
log_return_data['nikkei_log_return'] = np.log(
    closing_data['nikkei_close'] / closing_data['nikkei_close'].shift())
log_return_data['hangseng_log_return'] = np.log(
    closing_data['hangseng_close'] / closing_data['hangseng_close'].shift())
log_return_data['dax_log_return'] = np.log(
    closing_data['dax_close'] / closing_data['dax_close'].shift())
log_return_data['aord_log_return'] = np.log(
    closing_data['aord_close'] / closing_data['aord_close'].shift())

log_return_data['nifty_log_return_positive'] = 0
log_return_data.ix[log_return_data['nifty_log_return'] >= 0, 'nifty_log_return_positive'] = 1
log_return_data['nifty_log_return_negative'] = 0
log_return_data.ix[log_return_data['nifty_log_return'] < 0, 'nifty_log_return_negative'] = 1
log_return_data['Date'] = closing_data.index.values

training_test_data = pd.DataFrame(
    columns=[
        'Date', 'nifty_log_return_positive', 'nifty_log_return_negative',
        'nifty_log_return_1', 'nifty_log_return_2', 'nifty_log_return_3',
        'snp_log_return_1', 'snp_log_return_2', 'snp_log_return_3',
        'nyse_log_return_1', 'nyse_log_return_2', 'nyse_log_return_3',
        'djia_log_return_1', 'djia_log_return_2', 'djia_log_return_3',
        'nikkei_log_return_0', 'nikkei_log_return_1', 'nikkei_log_return_2',
        'hangseng_log_return_0', 'hangseng_log_return_1', 'hangseng_log_return_2',
        'dax_log_return_0', 'dax_log_return_1', 'dax_log_return_2',
        'aord_log_return_0', 'aord_log_return_1', 'aord_log_return_2'])

for i in range(3, len(log_return_data)):
    nifty_log_return_positive = log_return_data['nifty_log_return_positive'].ix[i]
    nifty_log_return_negative = log_return_data['nifty_log_return_negative'].ix[i]
    nifty_log_return_1 = log_return_data['nifty_log_return'].ix[i - 1]
    nifty_log_return_2 = log_return_data['nifty_log_return'].ix[i - 2]
    nifty_log_return_3 = log_return_data['nifty_log_return'].ix[i - 3]
    snp_log_return_1 = log_return_data['snp_log_return'].ix[i - 1]
    snp_log_return_2 = log_return_data['snp_log_return'].ix[i - 2]
    snp_log_return_3 = log_return_data['snp_log_return'].ix[i - 3]
    nyse_log_return_1 = log_return_data['nyse_log_return'].ix[i - 1]
    nyse_log_return_2 = log_return_data['nyse_log_return'].ix[i - 2]
    nyse_log_return_3 = log_return_data['nyse_log_return'].ix[i - 3]
    djia_log_return_1 = log_return_data['djia_log_return'].ix[i - 1]
    djia_log_return_2 = log_return_data['djia_log_return'].ix[i - 2]
    djia_log_return_3 = log_return_data['djia_log_return'].ix[i - 3]
    nikkei_log_return_0 = log_return_data['nikkei_log_return'].ix[i]
    nikkei_log_return_1 = log_return_data['nikkei_log_return'].ix[i - 1]
    nikkei_log_return_2 = log_return_data['nikkei_log_return'].ix[i - 2]
    hangseng_log_return_0 = log_return_data['hangseng_log_return'].ix[i]
    hangseng_log_return_1 = log_return_data['hangseng_log_return'].ix[i - 1]
    hangseng_log_return_2 = log_return_data['hangseng_log_return'].ix[i - 2]
    dax_log_return_0 = log_return_data['dax_log_return'].ix[i]
    dax_log_return_1 = log_return_data['dax_log_return'].ix[i - 1]
    dax_log_return_2 = log_return_data['dax_log_return'].ix[i - 2]
    aord_log_return_0 = log_return_data['aord_log_return'].ix[i]
    aord_log_return_1 = log_return_data['aord_log_return'].ix[i - 1]
    aord_log_return_2 = log_return_data['aord_log_return'].ix[i - 2]
    training_test_data = training_test_data.append(
        {'Date': log_return_data['Date'].ix[i],
         'nifty_log_return_positive': nifty_log_return_positive,
         'nifty_log_return_negative': nifty_log_return_negative,
         'nifty_log_return_1': nifty_log_return_1,
         'nifty_log_return_2': nifty_log_return_2,
         'nifty_log_return_3': nifty_log_return_3,
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

training_test_data = training_test_data.set_index('Date')
closing_data = pd.merge(training_test_data, closing_data,
                        left_index=True, right_index=True, how='outer')
closing_data = closing_data.dropna(how='any')

# print(closing_data)

for index, row in closing_data.iterrows():
    db.finance.insert({'date': index, 'close': [{'stock': 'nifty', 'value': row['nifty_close']},
                                                {'stock': 'nyse',
                                                 'value': row['nyse_close']},
                                                {'stock': 'snp',
                                                 'value': row['snp_close']},
                                                {'stock': 'aord',
                                                 'value': row['aord_close']},
                                                {'stock': 'hangseng',
                                                 'value': row['hangseng_close']},
                                                {'stock': 'nikkei',
                                                 'value': row['nikkei_close']},
                                                {'stock': 'djia',
                                                 'value': row['djia_close']},
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


sys.exit(0)
