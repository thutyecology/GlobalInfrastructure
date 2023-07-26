# -*- coding: utf-8 -*-

import os
import pandas as pd
import statsmodels.api as sm
from sklearn.metrics import r2_score

parent = os.path.dirname(os.getcwd())

file = parent+'\\file\\regression_data.xlsx'
df = pd.read_excel(file,sheet_name=0)

models = {'Model I': ['ExpEconomic','ExpSocial','LnPop','LnGDP'],
          'Model II': ['GiniEconomic','GiniSocial','LnPop','LnGDP'],
          'Model III': ['ExpEconomic','ExpSocial',
                        'GiniEconomic','GiniSocial',
                        'LnPop','LnGDP'],
        }

model = 'Model III'

varx = models[model]
vary = 'HALE'
#vary = 'Ln(DALYs)'

endog1 = df[vary]
exog1 = sm.tools.tools.add_constant(df[varx])
md = sm.MixedLM(endog1, exog1, groups=df["SN"])
mdf = md.fit()
#print(mdf.summary())

nobs = mdf.nobs
params = mdf.params.reset_index()
pvalues = mdf.pvalues.reset_index()

std = mdf.bse.reset_index()
predictions = mdf.predict(exog1)
r2 = r2_score(endog1, predictions)
    
dfre = pd.merge(params,pvalues,on='index')
dfre = pd.merge(dfre,std,on='index')
a = dfre.values
relist = []

for i in range(len(pvalues)):
    coef = a[i][1]
    p = a[i][2]
    std = a[i][3]
    if p<0.01:
        s = str("%.2f"%(coef))+'*** ('+str("%.2f"%(std))+')'
    elif p<0.05:
        s = str("%.2f"%(coef))+'** ('+str("%.2f"%(std))+')'
    elif p<0.1:
        s = str("%.2f"%(coef))+'* ('+str("%.2f"%(std))+')'
    else:
        s = str("%.2f"%(coef))+' ('+str("%.2f"%(std))+')'
    relist.append(s)
    
dfre['Coefficient'] = relist
dfre = dfre.rename(columns={'index':'Variable'})
dfre2 = dfre[['Variable','Coefficient']]

print (model)
print (dfre2)
print ()
print ("Dependent variable:",vary)
print ("R-square:","%.2f"%(r2)) 



