# -*- coding: utf-8 -*-

import os
import pandas as pd
from decimal import Decimal

def Decimal2(a):
    return Decimal(a).quantize(Decimal("0.00"))

def computeStatitics(df):
    valist = []
    dfsta = df[['SN','Economic', 'Social', 'Environmental']].groupby('SN').describe().reset_index()
    array = dfsta.values
    for row in array:
        val = str(Decimal2(row[2]))+'±'+str(Decimal2(row[3]))
        val2 = str(Decimal2(row[10]))+'±'+str(Decimal2(row[11]))
        val3 = str(Decimal2(row[18]))+'±'+str(Decimal2(row[19]))
        valist.append([row[0],row[1],val,val2,val3])
        
    dfsta = df[['CONTINENT','Economic', 'Social', 'Environmental']].groupby('CONTINENT').describe().reset_index()
    array = dfsta.values
    for row in array:
        val = str(Decimal2(row[2]))+'±'+str(Decimal2(row[3]))
        val2 = str(Decimal2(row[10]))+'±'+str(Decimal2(row[11]))
        val3 = str(Decimal2(row[18]))+'±'+str(Decimal2(row[19]))
        valist.append([row[0],row[1],val,val2,val3])
        
    mean = df[['Economic', 'Social', 'Environmental']].mean()
    std = df[['Economic', 'Social', 'Environmental']].std()
    val = str(Decimal2(mean[0]))+'±'+str(Decimal2(std[0]))
    val2 = str(Decimal2(mean[1]))+'±'+str(Decimal2(std[1]))
    val3 = str(Decimal2(mean[2]))+'±'+str(Decimal2(std[2]))
    m,n=df.shape
    valist.append(['Global',m,val,val2,val3])
        
    dfval = pd.DataFrame(valist,columns=['Region','Count','Economic', 'Social', 'Environmental'])
    dfval['Count'] = dfval['Count'].astype(int)
    
    order = [1,2,8,4,3,5,7,6,9]
    dfval['Order'] = order 
    dfval = dfval.sort_values('Order')
    return dfval

parent = os.path.dirname(os.getcwd())

file = parent+'\\file\\infrastructure_exposure_inequality_country.xlsx'
dfexp = pd.read_excel(file,sheet_name='exposure')
dfinq = pd.read_excel(file,sheet_name='inequality')

dfexpSta = computeStatitics(dfexp)
print ('Infrastructure exposure:')
print (dfexpSta.drop(columns=['Order']))
print ()

dfinqSta = computeStatitics(dfinq)
print ('Infrastructure exposure inequality (Gini):')
print (dfinqSta.drop(columns=['Order']))

