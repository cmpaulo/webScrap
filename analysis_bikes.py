#!/usr/bin/python
import datetime as dtime
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


def map_date(data):

    today = dtime.datetime.today().date()
    
    day_data = data['diaPostagem']
    
    for i in range(len(day_data)):
        if day_data[i] == 'Ontem':
            data.loc[i,'diaPostagem'] = (today - dtime.timedelta(days=1)).strftime("%d %b")
        elif day_data[i] == 'Hoje':
            data.loc[i,'diaPostagem'] = today.strftime("%d %b")
    
    return data


def clean_data(name = ""):

    data = pd.read_csv(name, index_col='Unnamed: 0')

    data = data.drop_duplicates(keep='last').dropna()

    data.reset_index(inplace=True,drop=True)

    data = map_date(data)

    return data, name



def related_res(data, name, related_words):

    related_word_upper = [w.upper() for w in related_words]
    related_word_cap   = [w.capitalize() for w in related_words]
    related_words_out  = set(related_words).union(set(related_word_cap).union(set(related_word_upper)) ) 
    related_words_out  = sorted(related_words_out)

    for i in data.index:
        if any(word_i in data['nomeBike'][i] for word_i in related_words_out):
            continue
        else:
            data.drop(i, inplace=True)

    data.reset_index(inplace=True,drop=True)
    
    data.to_csv(f'{name.split(".")[0]}_clean.csv')
    
    return data


data, name = clean_data('dados_bike_busca.csv')

# clean data
related_words = ['fixa', 'sunburst', 'hotdog', '8bike', '8','oito','rosa','urbana','single','night', 'riders', 'night riders']

data_clean = related_res(data, name, related_words)

# metricas
metrica = plt.boxplot(data['precoBike'])
captop = metrica['caps'][1].get_ydata()[0]
caplow = metrica['caps'][0].get_ydata()[0]

dataK = data[(data['precoBike'] > caplow) & (data['precoBike'] < captop)]


means = dataK.groupby('cidade').mean().sort_values('precoBike',ascending=False)['precoBike']

Lower_mean_ads = dataK.sort_values('precoBike',ascending=False)
ads = Lower_mean_ads[Lower_mean_ads['precoBike'].values < means.mean()]
ads_mkdw = ads.loc[:,['diaPostagem','nomeBike','cidade','precoBike','urlBike']]
ads_mkdw.to_markdown(f'{name.split(".")[0]}.md',index=False)

counts_anuncios = dataK.groupby('cidade').count().sort_values('precoBike',ascending=True)['precoBike']

# plot

plt.figure(figsize=(10, 7))
ax = plt.axes()
ax.barh(means.index, means.values,label='Preço médio')
ax.axvline(means.mean(), color = 'red',ls = 'dashed', label='Preço médio no Estado de São Paulo')
# ax.set_title('Valor médio para as bicicletas fixa nas cidades da Região Sul')
ax.set_title('Valor médio para as bicicletas fixa nas cidades do Estado de São Paulo')

ax.set_ylabel('Cidade')
ax.set_xlabel('Preço médio [R$]')
ax.set_xlim(0,int(means.values.max())+500)
ax.set_xticklabels(np.arange(0,int(means.values.max())+1000,500))
ax.set_ylim(means.index[0],means.index[-1])
ax.set_yticklabels(means.index)
plt.legend()
plt.tight_layout()
plt.savefig("./images/median_price_of_bike.png")

plt.figure(figsize=(10, 7))
ax = plt.axes()
ax.barh(counts_anuncios.index, counts_anuncios.values, label='Número de anúncios por cidade de bike fixa no Estado de São Paulo')
ax.set_title('Número de anúncios de bicicletas fixa nas cidades do Estado de São Paulo')

ax.set_ylabel('Cidade')
ax.set_xlabel('Número de anúncios')
ax.set_xlim(0,counts_anuncios.values.max()+4)
ax.set_ylim(counts_anuncios.index[0],counts_anuncios.index[-1])
ax.set_xticklabels(np.arange(0,counts_anuncios.values.max()+6,2))
ax.set_yticklabels(counts_anuncios.index)
plt.tight_layout()
plt.savefig("./images/number_of_ads_bycity.png")
# plt.show()