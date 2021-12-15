#!/usr/bin/python

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# [PR,SC,SP,RS]
data = pd.read_csv('dados_bike_busca_sunburst.csv', index_col='Unnamed: 0')

# print('removendo duplicadas \n e valores nan')
data = data.drop_duplicates(keep='last').dropna()

data.reset_index(inplace=True,drop=True)


# related_word = ['raf','8bike','8Bike', 'nexus', 'tetrapode','cernunnos','fixed','riva','cinelli','single','fixa']
related_word = ['fixed','fixie','single','fixa','sunburst','hotdog', 'simples']

related_word_upper = [w.upper() for w in related_word]
related_word_cap = [w.capitalize() for w in related_word]
related_words = set(related_word).union(set(related_word_cap).union(set(related_word_upper)) ) 
related_words = sorted(related_words)

for i in data.index:
    if any(word_i in data['nomeBike'][i] for word_i in related_words):
        continue
    else:
        data.drop(i, inplace=True)

data.reset_index(inplace=True,drop=True)

# clean data
data.to_csv('dados_bike_BR_clean.csv')

metrica = plt.boxplot(data['precoBike'])
captop = metrica['caps'][1].get_ydata()[0]
dataK = data[(data['precoBike'] > 400) & (data['precoBike'] < captop)]

# print(dataK.loc[:,['diapostagem','nomeBike', 'precoBike', 'cidade', 'urlBike']].sort_values(['diapostagem','precoBike'],ascending=False))
# plot
plt.figure(figsize=(10, 7))
ax = plt.axes()
means = dataK.groupby('cidade').mean().sort_values('precoBike',ascending=False)['precoBike']
ax.barh(means.index, means.values)
ax.axvline(means.mean(), color = 'red',ls = 'dashed', label='Preço médio na Região Sul')
ax.set_title('Valor médio para as bicicletas fixa nas cidades da Região Sul')

# dataK.groupby('cidade').median().sort_values('precoBike',ascending=False).plot(); plt.tight_layout()
# quantidade de anuncios
# dataK.groupby('cidade').count().sort_values('precoBike',ascending=False).plot.bar(y='precoBike', ylim=[0,20],label='Número de anuncios por cidade de bike fixa na Região Sul'); plt.tight_layout(); plt.show()

ax.set_ylabel('Cidade')
ax.set_xlabel('Média de preço [R$]')
ax.set_xlim(0,int(means.values.max())+500)
ax.set_xticklabels(np.arange(0,int(means.values.max())+1000,500))
ax.set_ylim(means.index[0],means.index[-1])
ax.set_yticklabels(means.index)
plt.legend()
plt.tight_layout()
plt.savefig("./images/median_price_of_bike.png")

# plt.show()
# print dos valores
# print(dataK.groupby('cidade').mean().sort_values('precoBike',ascending=False))
# print(dataK.groupby('cidade').mean().mean())

# plot
plt.figure(figsize=(10, 7))
ax = plt.axes()
counts_anuncios = dataK.groupby('cidade').count().sort_values('precoBike',ascending=True)['precoBike']
ax.barh(counts_anuncios.index, counts_anuncios.values, label='Número de anúncios por cidade de bike fixa na Região Sul')
ax.set_title('Número de anúncios de bicicletas fixa nas cidades da Região Sul')

ax.set_ylabel('Cidade')
ax.set_xlabel('Número de anúncios')
ax.set_xlim(0,counts_anuncios.values.max()+4)
ax.set_ylim(counts_anuncios.index[0],counts_anuncios.index[-1])
ax.set_xticklabels(np.arange(0,counts_anuncios.values.max()+6,2))
ax.set_yticklabels(counts_anuncios.index)
plt.tight_layout()
plt.savefig("./images/number_of_ads_bycity.png")
# plt.show()



# print(dataK.sort_values(['diapostagem','precoBike'],ascending=False)[['diapostagem','nomeBike','urlBike']].values)
mm = means[means.values < means.mean()]
for jj in mm.index[::-1]:
    print('cidade: ', jj)
    print(dataK.loc[dataK.cidade == jj,['diapostagem','urlBike']].values)
    print(' ______________________________________________')
