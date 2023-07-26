# -*- coding: utf-8 -*-

import os
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

parent = os.path.dirname(os.getcwd())

file = parent+'\\file\\infrastructure_exposure_inequality_country.xlsx'
df = pd.read_excel(file,sheet_name='exposure')

typlist = ['Economic','Social','Environmental']
for typ in typlist:
    dfgsub = df[[typ,'ADM0_CODE']]
    dfgsub = dfgsub.rename(columns={typ:'Exposure'})
    dfgsub['Category'] = typ

    sns.set(font_scale=1.75, style="ticks", palette="bright", color_codes=True)
    fig, ax = plt.subplots(1,1,figsize=(1.5,5),dpi=300)
    my_pal = {"Global South": "b", "Global North": "red"}
    sns.boxplot(
                x='SN',
                y=typ,
                data=df.sort_values('SN'),
                ax=ax,
                showfliers = False,
                palette = my_pal,
                width= 0.5
                )
    plt.xlabel('')
    plt.ylabel('')
    plt.ylim(-0.05,1.05)
    labels = ['N','S']
    ax.set_xticklabels(labels)
    
    outdir = parent+"\\result\\exposure\\"
    #plt.savefig(outdir +"boxplot-"+subcat.lower()+"-exposure-"+version, dpi=600, bbox_inches = 'tight')
    plt.show() 


 
