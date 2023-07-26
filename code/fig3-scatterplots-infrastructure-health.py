# -*- coding: utf-8 -*-

import os
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import math
import matplotlib.lines as mlines
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.feature_selection import f_regression

def linear_regression(x,y):
    model = LinearRegression()   
    model.fit(x, y)
    predictions = model.predict(x)
    r2 = r2_score(y, predictions)
    rmse = mean_squared_error(y, predictions, squared=False)
    freg=f_regression(x,y)
    p=float(freg[1])
    coef = model.coef_
    inter = model.intercept_

    return r2,rmse,p,coef,inter

parent = os.path.dirname(os.getcwd())

file = parent+'\\file\\regression_data.xlsx'
df = pd.read_excel(file,sheet_name=0)
dfexp = df.rename(columns={'ExpEconomic':'Economic','ExpSocial':'Social','ExpEnvironmental':'Environmental'})
dfinq = df.rename(columns={'GiniEconomic':'Economic','GiniSocial':'Social','GiniEnvironmental':'Environmental'})

catlist = ['exposure','exposure inequality']
vars1 = ['Economic','Social','Environmental']
var2 = 'HALE'

for cat in catlist:
    if cat == 'exposure':
        dfn = dfexp.loc[dfexp['SN']=='North']
        dfs = dfexp.loc[dfexp['SN']=='South']
    else:
        dfn = dfinq.loc[dfinq['SN']=='North']
        dfs = dfinq.loc[dfinq['SN']=='South']

    for var1 in vars1:
        x1 = dfn[var1].values.reshape(-1, 1)
        y1 = dfn[var2].values.reshape(-1, 1)  
        r2,rmse,pn,coef,inter = linear_regression(x1,y1)
        rn = math.sqrt(r2)

        x2 = dfs[var1].values.reshape(-1, 1)
        y2 = dfs[var2].values.reshape(-1, 1)  
        r2,rmse,ps,coef,inter = linear_regression(x2,y2)
        rs = math.sqrt(r2)
        
        sns.set(font_scale=1.5, style="ticks", palette="bright", color_codes=True)
        fig, ax = plt.subplots(1, 1,figsize=(5,5),dpi=300)
        
        sns.regplot(
                    x=var1,
                    y=var2,
                    data=dfs,
                    ax=ax,
                    ci=95, 
                    scatter_kws={'color':'b','s':75,'alpha':0.7}, 
                    line_kws={"color": "b",'linewidth':3,'alpha':0.9}
                    )  
        
        sns.regplot(
                    x=var1,
                    y=var2,
                    data=dfn,
                    ax=ax,
                    ci=95, 
                    scatter_kws={'color':'r','s':75,'alpha':0.5}, 
                    line_kws={"color": "r",'linewidth':3,'alpha':0.9}
                    )
    
        ymin, ymax = ax.get_ylim()
        xmin, xmax = ax.get_xlim()
        
        plt.ylabel(var2)
        plt.xlabel(var1+' '+cat)  
        
        marker1 = mlines.Line2D([], [], color='r', marker='o', linestyle='None',
                              markersize=10, label='Global North')
        marker2 = mlines.Line2D([], [], color='b', marker='o', linestyle='None',
                              markersize=10, label='Global South')  
        
        if cat == 'exposure' and var1 == 'Economic':
            plt.legend(handles=[marker1, marker2],fontsize=16,facecolor="white",framealpha=1)
        
        if cat == 'exposure' and var2 == 'HALE':
            ax.text(xmax-(xmax-xmin)/2,(ymax-ymin)/1.08+ymin,"r=%.2f"%(rn)+", p=%.2f"%(pn),size=18,color='r',backgroundcolor='white')    
            ax.text(xmax-(xmax-xmin)/2,(ymax-ymin)/3.3+ymin,"r=%.2f"%(rs)+", p=%.2f"%(ps),size=18,color='b',backgroundcolor='white') 
        else:
            ax.text(xmax-(xmax-xmin)/2.25,(ymax-ymin)/1.09+ymin,"r=%.2f"%(rn)+", p=%.2f"%(pn),size=18,color='r',backgroundcolor='white')    
            ax.text(xmax-(xmax-xmin)/1.1,(ymax-ymin)/5+ymin,"r=%.2f"%(rs)+", p=%.2f"%(ps),size=18,color='b',backgroundcolor='white') 
            
        outdir = parent+"\\result\\health\\"+var2+"\\"
        #plt.savefig(outdir +"scatterplot-"+cat+"-"+var1.lower(), dpi=600, bbox_inches = 'tight')
        plt.show() 
