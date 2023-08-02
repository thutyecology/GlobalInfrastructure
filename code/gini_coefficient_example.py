# -*- coding: utf-8 -*-
import os
import inequalipy as ineq 
import tifffile as tiff
import pandas as pd

parent = os.path.dirname(os.getcwd())
fdir = parent+'\\data\\gini_example\\'

uid = 237
imgPop = tiff.imread(fdir+'population-ADM0_CODE_'+str(uid)+'.tif')
imgEco = tiff.imread(fdir+'economic-infrastructure-ADM0_CODE_'+str(uid)+'.tif')
imgSoc = tiff.imread(fdir+'social-infrastructure-ADM0_CODE_'+str(uid)+'.tif')
imgEnv = tiff.imread(fdir+'environment-infrastructure-ADM0_CODE_'+str(uid)+'.tif')

arPop = imgPop.flatten()
df = pd.DataFrame(arPop,columns=['Population'])
df['Economic'] = imgEco.flatten()
df['Social'] = imgSoc.flatten()
df['Environmental'] = imgEnv.flatten()
df = df.dropna()
df = df.loc[df['Population']>0]
    
giniEco = ineq.gini(df.Economic.values,df.Population.values)
giniSoc = ineq.gini(df.Social.values,df.Population.values)
giniEnv = ineq.gini(df.Environmental.values,df.Population.values)

print ('Gini coefficient:')
print ('Economic infrastructure inequality = %.2f'%(giniEco))
print ('Social infrastructure inequality = %.2f'%(giniSoc))
print ('Environmental infrastructure inequality = %.2f'%(giniEnv))
