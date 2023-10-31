#!/usr/bin/python
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import datetime
import glob
import os

"""
This code is performing several data cleaning and manipulation tasks on a CSV file. It starts by reading in a file with the given name and dropping any duplicate or empty rows.
Then, it filters the data to only include rows where the "nameBike" column contains any of the specified related words. The cleaned data is then saved to a new CSV file. 
Additionally, it converts the "valueBike" column to a numeric data type and creates boxplots and bar charts to show statistics and information about the cleaned data. Finally, it exports the data to a markdown file.
"""


def clean_data(names = ""):
    
    list_files = glob.glob(names)
    
    list_files = sorted(list_files)
    list_dfs = []
    for i in list_files:
        data = pd.read_csv(i, index_col='Unnamed: 0',header=0)
        os.remove(i)
        names = i        
        data = data.dropna()
        
        list_dfs.append(data)
        
        
    scrp_files = pd.concat(list_dfs)

    scrp_files.reset_index(inplace=True,drop=True)
        # print(data)
    tagtime = datetime.datetime.now().strftime("%Y%m%d_%H%M")
        
    scrp_files.to_csv(f"busca_bike_dados_{tagtime}.csv")
        
    return scrp_files, names



def related_res(data, name, related_words):

    related_word_upper = [w.upper() for w in related_words]
    related_word_cap   = [w.capitalize() for w in related_words]
    related_words_out  = set(related_words).union(set(related_word_cap).union(set(related_word_upper)) ) 
    related_words_out  = sorted(related_words_out)

    data = data[data['nameBike'].apply(lambda x: any(word_i in x for word_i in related_words_out))]

    data.reset_index(inplace=True,drop=True)
    
    data.to_csv(name.replace('*.csv','_clean.csv'))
        
    return data


data, name = clean_data('busca_bike_dados_*.csv')

# clean data
# if len(data) > 500:

#     related_words = ['bike fixa','las magrelas', 'raf','raf bike','sprinter','8bike', 'fixie', 'nexus','tetrapode', 'alleycat','cernunnos','chandan','fixed','aventon','riva','cinelli','single']

#     data_clean = related_res(data, name, related_words)

# else:

data_clean = data.copy()


if len (data_clean) > 0:
    data_clean['valueBike'] = pd.to_numeric(data_clean['valueBike'].values)
    data_clean['update'] = pd.to_datetime(data_clean['update'],format="%Y%m%d_%H%M")
    # # metrics
    metrica = plt.boxplot(data_clean['valueBike'])
    captop = metrica['caps'][1].get_ydata()[0]
    caplow = metrica['caps'][0].get_ydata()[0]

    dataK = data_clean[(data_clean['valueBike'] > caplow) & (data_clean['valueBike'] < captop)]

    means = dataK.loc[:,["city","valueBike"]].groupby('city').mean().sort_values('valueBike',ascending=False)

    if len(dataK) > 10:
        Lower_mean_ads = dataK.sort_values('valueBike',ascending=False)
        bollowmean_last15days = ((Lower_mean_ads['valueBike'].values < means['valueBike'].mean()) & (Lower_mean_ads.loc[:,'update'] > (datetime.datetime.now()-datetime.timedelta(days=15.0))))
        ads = dataK.loc[bollowmean_last15days,:]
        ads_mkdw = ads.loc[:,['dayPost', 'nameBike', 'city','valueBike','urlBike']]
        ads_mkdw = ads_mkdw.drop_duplicates(keep='last')
   
        filename = ''.join(x for x in name if x.isalpha() or x == "_")
        ads_mkdw.to_markdown('{}'.format(filename.replace("__csv",'.md')),index=False)
        
    else:
        
        ads_mkdw = dataK.loc[:,['dayPost', 'nameBike', 'city','valueBike','urlBike']]
        
        filename = ''.join(x for x in name if x.isalpha() or x == "_")
        ads_mkdw.to_markdown('{}'.format(filename.replace("__csv",'.md')),index=False)
        
    counts_anuncios = dataK.groupby('city').count().sort_values('valueBike',ascending=False)['valueBike']

    # plot

    plt.figure(figsize=(10, 7))
    ax = plt.axes()

    if len(means) > 5:

        ax.barh(means.index, means['valueBike'].values, label='Preço médio')
        
        for i, city in enumerate(means.index):
            ax.text(means.loc[city,:] + 1, i, "n = "+str(counts_anuncios[city]))

        ax.set_xlim(0,ax.get_xlim()[1])
        ax.text(means['valueBike'].mean()+50,ax.get_ylim()[0], f"Atualizado em {pd.Timestamp.today().date()}")
        ax.axvline(means['valueBike'].mean(), color = 'red',ls = 'dashed', label=f'R$ {means["valueBike"].mean():.2f}, Preço médio no Estado de São Paulo')
        
        ax.set_ylabel('Cidade')
        ax.set_xlabel('Preço médio [R$]')

    else:

        ax.bar(means.index, means["valueBike"].values, label='Preço médio')
        # ax.set_ylim(0,ax.get_ylim()[1])
        ax.set_xlabel('Cidade')
        ax.set_ylabel('Preço médio [R$]')
        # ax.text(ax.get_ylim()[0],means['valueBike'].mean()+50, f"Atualizado em {pd.Timestamp.today().date()}")
    
    # ax.axhline(means['valueBike'].mean(), color = 'red',ls = 'dashed', label=f'R$ {means["valueBike"].mean():.2f}, Preço médio no Estado de São Paulo')
    ax.set_title('Valor médio e o número de anúncios para as bicicletas fixa em cidades do Estado de São Paulo')

    plt.legend()
    plt.tight_layout()
    plt.savefig("./images/median_price_of_bike.png")
    # plt.show()
else:
    print("no related results or dataframe to small")
    