#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed Jan 29 21:43:04 2020

@author: jonpetter
"""

#%%
import pandas as pd

#%%
df = pd.read_csv('/Users/jonpetter/Downloads/transactions_export_2020-04-29T22_30_34.csv',
            sep='\t',
            encoding='utf-16',
            header=0,
            decimal=',',
            thousands=' ',
            keep_default_na=False,
            na_values=[])

print(df)
print([c for c in df.columns])

#%%
newDfColumns = [u"Dato", 
                u"Type", 
                u"Beskrivelse1", 
                u"Beskrivelse2",
                u"Inn på konto", 
                u"Ut fra konto",
                u"Resultat", 
                u"Bokføring",
                u"Valuta"]
                
extractDataFnList = [lambda row: row[u"Bokføringsdag"],
                     lambda row: row[u"Transaksjonstype"] + u" " + row[u"Verdipapir"] + u" " + str(row[u"Antall"]) + u", " + str(row[u"Kurs"]) + u", " + str(row[u"Avgifter"]) ,
                     lambda row: row[u"Transaksjonstype"],
                     lambda row: row[u"Verdipapir"],
                     lambda row: row[u"Beløb"] if row[u"Beløb"] > 0 else "",
                     lambda row: row[u"Beløb"] if row[u"Beløb"] < 0 else "",
                     lambda row: "",
                     lambda row: "",
                     lambda row: row[u"Valuta"]
                     ]

def createNewLine(row):
    newRow = []
    for j in range(len(newDfColumns)):
        newRow.append(extractDataFnList[j](row))
    return newRow
                
newData = []
for i, row in df.iterrows():
    if row[u"Beløb"] == 0.0:
        print('Skipping row %s'%(row[u"Bokføringsdag"] + u" " + row[u"Transaksjonstype"] + u" " + row[u"Verdipapir"]))
        continue
    newData.insert(0, createNewLine(row))
    
newDf = pd.DataFrame(newData, columns=newDfColumns)
print(newDf)

newDf.to_csv('/Users/jonpetter/Downloads/nordnet_transactions.cvs')
                
#newDf = df[[u'Bokføringsdag',
#            u'Transaksjonstype',
#            u'Transaksjonstype',
#            u'Verdipapir']].copy()