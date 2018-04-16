import googlefinance.client as gf
from datetime import datetime
import pandas as pd
import os
import sys
import glob

path = "./data/"

last_date = []
for filename in glob.glob(os.path.join(path, '*.csv')):
    indx_name = filename.split('_')[1].split('.')[0].lower()
    indx_name += '_close'
    df_data = pd.read_csv(filename, sep=',', header=0)
    df_data['Date'] = pd.to_datetime(df_data['Date'])
    df_data = df_data.set_index('Date')
    df_data = df_data.dropna(how='any')
    df_data.sort_index(ascending=False, inplace=True)
    last_date.append(df_data.index[0])
    print(filename, df_data.index[0])


def checkEqual(iterator):
    return len(set(iterator)) <= 1


if (checkEqual(last_date)):
    print("Last Date matches")
else:
    print("Last Date doesn't match")
    sys.exit(1)

ldate = last_date[0]
print(ldate)

now = datetime.now()
diff = now - ldate

months = int(diff.days / 30) + (diff.days % 30 > 0)
print("DB is not updated for nearly", diff.days, "days")

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

dg['NYA_Close'] = dg['NYA_Close'].shift(-1)
dg['.INX_Close'] = dg['.INX_Close'].shift(-1)
dg['.DJI_Close'] = dg['.DJI_Close'].shift(-1)

aord_f = open("./data/YAHOO-INDEX_AORD.csv", "a+")
dax_f = open("./data/YAHOO-INDEX_DAX.csv", "a+")
djia_f = open("./data/YAHOO-INDEX_DJIA.csv", "a+")
hs_f = open("./data/YAHOO-INDEX_HANGSENG.csv", "a+")
nifty_f = open("./data/YAHOO-INDEX_NIFTY.csv", "a+")
nikkei_f = open("./data/YAHOO-INDEX_NIKKEI.csv", "a+")
nyse_f = open("./data/YAHOO-INDEX_NYSE.csv", "a+")
snp_f = open("./data/YAHOO-INDEX_SNP.csv", "a+")

dg = dg.dropna(how='any')

for index, row in dg.iterrows():
    if index > datetime.date(ldate):
        row1 = dg.ix[index]
        nifty_f.write("%s,%d,%d,%d,%f,%d,%d\n" %
                      (index.strftime('%m/%d/%Y'), 0, 0, 0, row1['NIFTY_Close'], 0, 0))
        djia_f.write("%s,%d,%d,%d,%f,%d,%d\n" % (index.strftime('%m/%d/%Y'),
                                                 0, 0, 0, row1['.DJI_Close'], 0, 0))
        snp_f.write("%s,%d,%d,%d,%f,%d,%d\n" % (index.strftime('%m/%d/%Y'),
                                                0, 0, 0, row1['.INX_Close'], 0, 0))
        aord_f.write("%s,%d,%d,%d,%f,%d,%d\n" % (index.strftime('%m/%d/%Y'),
                                                 0, 0, 0, row1['XAO_Close'], 0, 0))
        nyse_f.write("%s,%d,%d,%d,%f,%d,%d\n" % (index.strftime('%m/%d/%Y'),
                                                 0, 0, 0, row1['NYA_Close'], 0, 0))
        dax_f.write("%s,%d,%d,%d,%f,%d,%d\n" % (index.strftime('%m/%d/%Y'),
                                                0, 0, 0, row1['DAX_Close'], 0, 0))
        hs_f.write("%s,%d,%d,%d,%f,%d,%d\n" % (index.strftime('%m/%d/%Y'),
                                               0, 0, 0, row1['HSI_Close'], 0, 0))
        nikkei_f.write("%s,%d,%d,%d,%f,%d,%d\n" % (index.strftime('%m/%d/%Y'),
                                                   0, 0, 0, row1['NI225_Close'], 0, 0))
