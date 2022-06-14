#!/usr/bin/python
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd



def clean_data(name = ""):

    data = pd.read_csv(name, index_col='Unnamed: 0',header=0)

    data = data.drop_duplicates(keep='last').dropna()

    data.reset_index(inplace=True,drop=True)

    return data, name



def related_res(data, name, related_words):

    related_word_upper = [w.upper() for w in related_words]
    related_word_cap   = [w.capitalize() for w in related_words]
    related_words_out  = set(related_words).union(set(related_word_cap).union(set(related_word_upper)) ) 
    related_words_out  = sorted(related_words_out)

    for i in data.index:
        if any(word_i in data['nameBike'][i] for word_i in related_words_out):
            continue
        else:
            data.drop(i, inplace=True)

    data.reset_index(inplace=True,drop=True)
    
    data.to_csv(f'{name.split(".")[0]}_clean.csv')
    
    return data


data, name = clean_data('busca_bike_dados.csv')

# clean data

related_words = ['bike fixa','las magrelas', 'raf','raf bike','sprinter','8bike', 'fixie', 'nexus','tetrapode', 'alleycat','cernunnos','chandan','fixed','aventon','riva','cinelli','single']

data_clean = related_res(data, name, related_words)

data_clean['valueBike'] = pd.to_numeric(data_clean['valueBike'].values)
print(data_clean.loc[:15,['valueBike']])

# # metrics
metrica = plt.boxplot(data_clean['valueBike'])
captop = metrica['caps'][1].get_ydata()[0]
caplow = metrica['caps'][0].get_ydata()[0]

dataK = data[(data['valueBike'] > caplow) & (data['valueBike'] < captop)]


means = dataK.groupby('city').mean().sort_values('valueBike',ascending=False)['valueBike']

Lower_mean_ads = dataK.sort_values('valueBike',ascending=False)
ads = Lower_mean_ads[Lower_mean_ads['valueBike'].values < means.mean()]
ads_mkdw = ads.loc[:,['dayPost', 'nameBike', 'city','valueBike','urlBike']]
ads_mkdw.to_markdown(f'{name.split(".")[0]}.md',index=False)

counts_anuncios = dataK.groupby('city').count().sort_values('valueBike',ascending=False)['valueBike']

# plot

plt.figure(figsize=(10, 7))
ax = plt.axes()

if len(means) > 5:

    ax.barh(means.index, means.values, label='Preço médio')
    ax.axvline(means.mean(), color = 'red',ls = 'dashed', label='Preço médio no Estado de São Paulo')
    ax.set_xlim(0,ax.get_xlim()[1])
    ax.set_ylabel('Cidade')
    ax.set_xlabel('Preço médio [R$]')

else:

    ax.bar(means.index, means.values, label='Preço médio')
    ax.axhline(means.mean(), color = 'red',ls = 'dashed', label='Preço médio no Estado de São Paulo')
    ax.set_ylim(0,ax.get_ylim()[1])
    ax.set_xlabel('Cidade')
    ax.set_ylabel('Preço médio [R$]')

ax.set_title('Valor médio e o número de anúncios para as bicicletas fixa em cidades do Estado de São Paulo')

plt.legend()
plt.tight_layout()
plt.savefig("./images/median_price_of_bike.png")
# plt.show()
# exit()

plt.figure(figsize=(10, 7))
ax = plt.axes()

if len(means) > 5:

    ax.barh(counts_anuncios.index, counts_anuncios.values, label='Número de anúncios por cidade de bike fixa no Estado de São Paulo')
    ax.set_xlim(0,ax.get_xlim()[1])
    ax.set_ylabel('Cidade')
    ax.set_xlabel('Número de anúncios')

else:
    
    ax.bar(counts_anuncios.index, counts_anuncios.values, label='Número de anúncios por cidade de bike fixa no Estado de São Paulo')
    ax.set_ylim(0,ax.get_ylim()[1])
    ax.set_xlabel('Cidade')
    ax.set_ylabel('Número de anúncios')


ax.set_title('Número de anúncios de bicicletas fixa nas cidades do Estado de São Paulo')

plt.tight_layout()
plt.savefig("./images/number_of_ads_bycity.png")
# plt.show()
