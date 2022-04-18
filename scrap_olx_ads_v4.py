#!/usr/bin/python
# try to work in streamlit cloud.


from bs4 import BeautifulSoup
import numpy as np
import pandas as pd
import requests
import streamlit as st
import os


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

    base_codes = []
    dic_temp = {'dayPost':[], 'timePost':[], 'codeAd':[], 'nameAds':[], 'valueAds':[], 'city':[], 'neighborhood':[], 'cep':[], 'urlAds':[]}

    tpage = npages(page)
    
    soup = BeautifulSoup(page.content, 'lxml')

    for itens in soup.find_all("ul", {"class": "sc-1fcmfeb-1 kntIvV"}):

        for item in itens.find_all("li"):

            try:
                
                nameAds = item.find_all('h2')[0].contents[0]
                
                try:

                    urlAds = item.find('a')['href']
                    codeAd = urlAds.split('-')[-1]

                except:

                    codeAd = ' '
                
                # remove duplicates during the scrapping ads.
                if (codeAd is base_codes) or codeAd == ' ':
                    continue

                try: #open ads and get informations
                    
                    page2 = download_page(urlAds)
                    soupsp = BeautifulSoup(page2.content, 'lxml')

                    try:
                        # converting from BR presentation of numbers
                        valueAds = soupsp.find_all("h2", class_="sc-1wimjbb-2 iUSogS sc-ifAKCX cmFKIN")[0].contents[0].split("R$ ")[1].replace('.','')
                        valueAds = float(valueAds)

                    except:

                        valueAds = np.nan

                    try:

                        daytimePost = soupsp.find_all("span", class_="sc-1oq8jzc-0 jvuXUB sc-ifAKCX fizSrB")[0].contents[2].split(' às ')
                        dayPost = daytimePost[0]
                        timePost = daytimePost[1]

                    except:

                        dayPost = ' '
                        timePost = ' '

                    try:

                        cep = soupsp.find_all("dd", class_="sc-1f2ug0x-1 ljYeKO sc-ifAKCX kaNiaQ")[0].contents[0]
                        city = soupsp.find_all("dd", class_="sc-1f2ug0x-1 ljYeKO sc-ifAKCX kaNiaQ")[1].contents[0]
                                                        
                    except:

                        cep = ' '
                        city = ' '

                    try:

                        neighborhood = soupsp.find_all("dd", class_="sc-1f2ug0x-1 ljYeKO sc-ifAKCX kaNiaQ")[2].contents[0]

                    except:

                        neighborhood = ' '


                    objct_list = [dayPost,timePost,codeAd,nameAds,valueAds,city,neighborhood,cep,urlAds]
                    
                    for ki,kd in enumerate(dic_temp.keys()):
                        
                        dic_temp[kd].append(objct_list[ki])
                
                except:
                    print("Not link of found ads.")

                    for ki,kd in enumerate(dic_temp.keys()):

                        dic_temp[kd].append(np.nan)


            except:

                print("Not found ads.")

                for ki,kd in enumerate(dic_temp.keys()):

                    dic_temp[kd].append(np.nan)
        
        dic_temp_df = pd.DataFrame(dic_temp)
        dic_temp_df.to_csv('temp_ads_search.csv')
        return dic_temp_df

    

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
    
    rslt_data = ads_list(page, url)

    
    if os.path.exists('temp_ads_search.csv'):
        rslt_data = pd.read_csv('temp_ads_search.csv',header=0,index_col=0, na_filter=True, na_values=' ')


    rslt_data['valueAds'] = pd.to_numeric(rslt_data['valueAds'].values)
    

    if len(rslt_data) == 0:
        st.write('refazer busca.')
    else:
        st.write("valor médio de {:.2f} reais".format(rslt_data['valueAds'].mean()))
        st.markdown( rslt_data.loc[rslt_data['valueAds'] < rslt_data['valueAds'].mean() ,['nameAds','city','valueAds','urlAds']].drop_duplicates(keep='last').sort_values('valueAds',ascending=False).to_markdown() )
        st.write("Fim!")
