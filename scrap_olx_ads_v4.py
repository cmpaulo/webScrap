#!/usr/bin/python
# try to work in streamlit cloud.


from bs4 import BeautifulSoup
import numpy as np
import pandas as pd
import requests
import streamlit as st


# @st.cache()
def download_page(url1):

    PARAMS = {
        "authority" : "olx.com.br",
        "method": "GET",
        "scheme" : "https",
        "referer" : "https://olx.com.br",
        "sec-fetch-mode" : "navigate",
        "sec-fetch-site" : "same-origin",
        "sec-fetch-user" : "?1",
        "upgrade-insecure-requests":"1",
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36"
    }
    page1 = requests.get(url=url1, headers=PARAMS)

    return page1



def remove_accents(wwrd):

    accents_words = ["á","é","í","ó","ú","â","ê","ô","ã","ẽ","õ","ç"]
    accents_spell = ["a","e","i","o","u","a","e","o","a","e","o","c"]
    for ik,i in enumerate(accents_words):
        normalword = wwrd.replace(i,accents_spell[ik])
        if wwrd != normalword:
            break

    return normalword

# @st.cache()
def olxAdress(key_words = "fixa", category = "ciclismo", state = "São Paulo :: SP", locate="DDD"):

    statelow = state.split('::')[1].strip().lower()
    target_key = key_words.lower().replace(" ","%20")
    categor = remove_accents(category.lower().replace(' ','-'))
        
    region = locate
    url = ''


    if categor == "todas-as-categorias":
        url = f"https://{statelow}.olx.com.br/?q={target_key}&sf=1"    
    else:
        url = f"https://{statelow}.olx.com.br/{categor}?q={target_key}&sf=1"    

    return url


def npages(page):
    
    soup = BeautifulSoup(page.content, 'lxml')

    try:
        nResults = soup.find_all("span", class_="sc-1mi5vq6-0 eDXljX sc-ifAKCX fhJlIo")[0].contents[0]

        if 'resultados' in nResults:

            results = nResults.split(" ")
            tpages = int( int( results[-2].replace(".","") ) / int(results[-4]) )

    except:
            print("erro paginas")
            tpages = 0
    
    
    if int(tpages) > 10:

        print(f'Number of results is {tpages} pages')

        tpages = 3
    
    print(tpages, 'pages')

    return tpages


# @st.cache()
def ads_list(page, url1):

    listaAnuncios=[]

    tpage = npages(page)
    
    data = pd.DataFrame()
    
    for ipages in range(1,tpage+1):
        
        print('\\\\\\\\\\\ \\\\\\\\\\\\\\\\\\ ',url1)

        res_page = download_page(url=url1.replace('?',f'?o={ipages}&'))
        soup = BeautifulSoup(res_page.content, 'lxml')

        for itens in soup.find_all("ul", {"class": "sc-1fcmfeb-1 kntIvV"}):

            for item in itens.find_all("li"):

                try:
                    
                    nomeAds = item.find_all('h2')[0].contents[0]

                    try:

                        precoAds = item.find_all("span", class_="sc-ifAKCX eoKYee")[0].contents[0].split("R$")[1].replace('.','')
                        precoAds = np.float64(precoAds.replace(',','.'))
                        print(precoAds)

                    except:

                        precoAds = np.nan

                    try:

                        diaPostagem = item.find_all("span", class_="wlwg1t-1 fsgKJO sc-ifAKCX eLPYJb")[0].contents[0]

                    except:

                        diaPostagem = np.nan

                    try:

                        horaPostagem = item.find_all("span", class_="wlwg1t-1 fsgKJO sc-ifAKCX eLPYJb")[1].contents[0]

                    except:

                        horaPostagem = np.nan

                    try:

                        urlAds = item.find('a')['href']
                        codAnuncio = urlAds.split('-')[-1]

                    except:

                        codAnuncio = np.nan

                    try:

                        localiza = item.find_all("span", class_="sc-7l84qu-1 ciykCV sc-ifAKCX dpURtf")[0].contents[0]
                        locais = localiza.split(',')
                        cidade = locais[0]
                        bairro = locais[1]

                    except:

                        cidade = np.nan
                        bairro = np.nan
                
                    try:
                        
                        page2 = download_page(url=urlAds)
                        soupsp = BeautifulSoup(page2.content, 'lxml')
                        cep = soupsp.find_all("dd", class_="sc-1f2ug0x-1 ljYeKO sc-ifAKCX kaNiaQ")[0].contents[0]

                    except:

                        cep = np.nan
                    
                    
                    objct_list = [diaPostagem, horaPostagem, codAnuncio, nomeAds, precoAds, cidade, bairro, cep, urlAds]
                    listaAnuncios.append(objct_list)

                except:

                    print("Not found ads.")
                    listaAnuncios.append(np.ones(len(objct_list))*np.nan )

    
            name = ['diaPostagem', 'hora','codigo','nomeAds','precoAds','cidade','bairro','cep','urlAds']
            
            data = data.append(pd.DataFrame(listaAnuncios, columns=name))
            data.to_csv('dados_Ads_sp.csv')

    
    return data


st.title('Buscar anúncios no OLX Brasil.')
st.header("Buscar por palavra chave, selecione a categoria principal e depois escolha o estado. \n Click no botão Buscar anuncios")

text_input = st.text_input("Buscar por palavras chaves" )


@st.cache()
def categorias_lista():
    pth = "cat_sub.txt"
    
    return pd.read_csv(pth)

@st.cache()
def estado_lista():
    pth = "estados.txt"
    
    return pd.read_csv(pth)
    
cat_df = categorias_lista()
estado_df = estado_lista()

sel_catgorias = st.selectbox('Escolha uma categoria', cat_df )

sel_estados =  st.selectbox('Escolha o estado', estado_df)


sigbtt = st.button("Buscar anuncios")

st.write("Os resultados serão apresentados em um tabela logo abaixo.")

if sigbtt:
    st.write(f'Buscando anuncios com as palavras {text_input} em {sel_estados} ...')
    
    url = olxAdress(key_words=text_input,state=sel_estados,category=sel_catgorias)

    page = download_page(url)
    
    print(url)
    
    resultados = ads_list(page, url)

    if len(resultados) == 0:
        st.write('refazer busca.')
    else:
        st.write("valor médio de {:.2f} reais".format(resultados['precoAds'].mean()))
        st.markdown( resultados.loc[resultados['precoAds'] < resultados['precoAds'].mean() ,['nomeAds','cidade','precoAds','urlAds']].drop_duplicates(keep='last').dropna().to_markdown() )
        st.write("Fim!")
