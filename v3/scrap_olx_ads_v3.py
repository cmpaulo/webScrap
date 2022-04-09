#!/usr/bin/python

from bs4 import BeautifulSoup
import numpy as np
import pandas as pd
import requests

import streamlit as st

# https://sp.olx.com.br/ciclismo?q=bike%20fixa
# https://sp.olx.com.br/sao-paulo-e-regiao/ciclismo?q=bike%20fixa
# https://sp.olx.com.br/sao-paulo-e-regiao/ciclismo?o=2&q=bike%20fixa
# melhora o try para obter mais resultados.
# Obtém a URL
# palavras para buscar [Airwalk, RAF, 8Bike, Nexus, Vicinitech, Tetrapode]

class scrap_olx_ads():
    

    def __init__(self, key_words = "fixa", category = "ciclismo", state = "São Paulo :: SP", locate="DDD"):

        self.estado = state.split('::')[1].lower()
        self.palavra = key_words.lower().replace(" ","%20")
        self.categor = self.remove_accents(category.lower()).replace(' ','-')
        
        self.region = locate
        self.url = ''

            # "path": "sao-paulo-e-regiao/ciclismo",
            # "referer" : "https://sp.olx.com.br/sao-paulo-e-regiao/ciclismo",
        self.PARAMS = {
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


    def remove_accents(self, wwrd):

        accents_words = ["á","é","í","ó","ú","â","ê","ô","ã","ẽ","õ","ç"]
        accents_spell = ["a","e","i","o","u","a","e","o","a","e","o","c"]
        for ik,i in enumerate(accents_words):
            normalword = wwrd.replace(i,accents_spell[ik])
            if wwrd != normalword:
                break

        return normalword


    def olxAdress(self):
        
        estado = self.estado.strip()
        palavra = self.palavra
        regiao = self.region
        categor = self.categor


        if categor == "todas-as-categorias":
            self.url = f"https://{estado}.olx.com.br/?q={palavra}&sf=1"    
        else:
            self.url = f"https://{estado}.olx.com.br/{categor}?q={palavra}&sf=1"    

    

    def npages(self):

        self.olxAdress()
        
        url1 = self.url
        print(url1)

        self.page = requests.get(url=url1, headers=self.PARAMS)
    
        if (self.page.status_code != 200):

            print('problema no servidor', 'code status ', self.page.status_code)
            exit()

        else:

            print('OK')
        
        soup = BeautifulSoup(self.page.content, 'lxml')

        try:
            nResultadosBusca = soup.find_all("span", class_="sc-1mi5vq6-0 eDXljX sc-ifAKCX fhJlIo")[0].contents[0]

            if 'resultados' in nResultadosBusca:

                resultados = nResultadosBusca.split(" ")
                tpages = int( int( resultados[-2].replace(".","") ) / int(resultados[-4]) )

        except:
                print("erro paginas")
                tpages = 0
        
        
        if int(tpages) > 10:

            tpages = 3
        
        print(tpages, 'páginas')

        return tpages



    def ads_list(self):

        listaAnuncios=[]

        tpage = self.npages()

        for ipages in range(tpage+1):
            # if ipages > 0: break

            res_page = requests.get(url=self.url.replace('?',f'?o={ipages}&'), headers=self.PARAMS)
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
                            
                            page2 = requests.get(url=urlAds, headers=self.PARAMS)
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
                data = pd.DataFrame(listaAnuncios, columns=name)
                data.to_csv('dados_Ads_sp.csv')
        
        return data


st.title('Buscar anuncios no OLX brasil.')
st.header("Buscar por palabra chave, selecione a categoria principal e depois escolha o estado. \n Click no botão Buscar anuncios")

text_input = st.text_input("Buscar por palavras chaves" )

def categorias_lista():
    pth = "/home/claudio/Documents/profissao_DS/projetos/Raspagem_web/webScrap/v2/cat_sub.txt"
    
    return pd.read_csv(pth)

def estado_lista():
    pth = "/home/claudio/Documents/profissao_DS/projetos/Raspagem_web/webScrap/v2/estados.txt"
    
    return pd.read_csv(pth)

cat_df = categorias_lista()
estado_df = estado_lista()

sel_catgorias = st.selectbox('Escolha uma categoria', cat_df )

sel_estados =  st.selectbox('Escolha o estado', estado_df)


sigbtt = st.button("Buscar anuncios")

st.write("Os resultados serão apresentados em um tabela logo abaixo.")

if sigbtt:
    st.write(f'Buscando anuncios com as palavras {text_input} em {sel_estados} ...')
    
    busca = scrap_olx_ads(key_words=text_input,state=sel_estados,category=sel_catgorias)
    
    resultados = busca.ads_list()
    st.write(f"valor médio de {resultados['precoAds'].mean()} reais")
    st.table(resultados.loc[resultados['precoAds'] < resultados['precoAds'].mean() ,['nomeAds','cidade','precoAds','urlAds']].drop_duplicates(keep='last').dropna() )
    st.write("Fim!")    