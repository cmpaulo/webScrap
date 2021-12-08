#!/usr/bin/python

import numpy as np
import pandas as pd
import requests
from bs4 import BeautifulSoup
from datetime import date

# https://sp.olx.com.br/ciclismo?q=bike%20fixa
# https://sp.olx.com.br/sao-paulo-e-regiao/ciclismo?q=bike%20fixa
# https://sp.olx.com.br/sao-paulo-e-regiao/ciclismo?o=2&q=bike%20fixa

# Obtém a URL
# palavras para buscar [Airwalk, RAF, 8Bike, Nexus, Vicinitech, Tetrapode]
def buscarDadosOLX(pages = 2,estado= "SP", regiao = "11", palavra = "fixa"):
    regiaoBuscar = {"0":"","11":"sao-paulo-e-regiao"}
    listaAnuncios = []
    estado = estado.lower()
    if regiao == "0":
        url = f"https://{estado}.olx.com.br/ciclismo?q={palavra}&sf=1"

    else:
        url = f"https://{uf[estado]}.olx.com.br/{regiaoBuscar[regiao]}/ciclismo?q={palavra}&sf=1"
        
    PARAMS = {
        "authority" : "pr.olx.com.br",
        "method": "GET",
        "path": "sao-paulo-e-regiao/ciclismo",
        "scheme" : "https",
        "referer" : "https://sp.olx.com.br/sao-paulo-e-regiao/ciclismo",
        "sec-fetch-mode" : "navigate",
        "sec-fetch-site" : "same-origin",
        "sec-fetch-user" : "?1",
        "upgrade-insecure-requests":"1",
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36"
    }
    page = requests.get(url=url, headers=PARAMS)
    soup = BeautifulSoup(page.content, 'lxml')
    # dicanuncios = {'diapostagem':[], 'hora':[],'nomedoVeiculo':[],'precoVeiculo':[],'kmrodado':[],'Cambio':[],'combustivel':[],'cidade':[],'bairro':[],'url':[]}
    nResultadosBusca = soup.find_all("span", class_="sc-1mi5vq6-0 eDXljX sc-ifAKCX fhJlIo")[0].contents[0]
    print(nResultadosBusca)
    if len(nResultadosBusca) > 20:
        try:
            if 'resultados' in nResultadosBusca:
                tpages = int( int( nResultadosBusca.split(" ")[-2].replace(".","") ) / 50 )
        except:
            print("erro paginas")
            tpages = 0
        
    if int(tpages) > 10:
        tpages = 3


    # for das paginas
    for ipages in range(tpages+1):
        page = requests.get(url=url.replace('?',f'?o={ipages}&'), headers=PARAMS)
        soup = BeautifulSoup(page.content, 'lxml')
        # for dos itens
        for itens in soup.find_all("ul", {"class": "sc-1fcmfeb-1 kntIvV"}):
            for item in itens.find_all("li"):
                try:
                    nomeBike = item.find_all('h2')[0].contents[0]
                    precoBike = item.find_all("span", class_="sc-ifAKCX eoKYee")[0].contents[0].split("R$")[1].replace('.','')
                    precoBike = float(precoBike)
                    diaPostagem = item.find_all("span", class_="wlwg1t-1 fsgKJO sc-ifAKCX eLPYJb")[0].contents[0]
                    horaPostagem = item.find_all("span", class_="wlwg1t-1 fsgKJO sc-ifAKCX eLPYJb")[1].contents[0]
                    urlBike = item.find('a')['href']
                    localiza = item.find_all("span", class_="sc-7l84qu-1 ciykCV sc-ifAKCX dpURtf")[0].contents[0]
                    
                    try:
                        locais = localiza.split(',')
                        cidade = locais[0]
                        bairro = locais[1]
                    except:
                        cidade = localiza
                        bairro = ' '
                
                    listaAnuncios.append([diaPostagem,horaPostagem,nomeBike,precoBike,cidade,bairro,urlBike])
                except:
                    print(["ERRO"])
                    listaAnuncios.append(np.ones(7)*np.nan )
        
    name = ['diapostagem', 'hora','nomeBike','precoBike','cidade','bairro','urlBike']
    data = pd.DataFrame(listaAnuncios, columns=name)
        # data.to_csv(f'dados_bike_{estado}_{regiao}.csv')
    return data

datai = pd.DataFrame()
for i in ['SP','PR',"SC","RS"]:
    for j in ['raf','8bike','8Bike', 'nexus','tetrapode' ,'cernunnos','fixed','riva', 'gear','cinelli','single','bike%20fixa']:
        reg = "0"
        datai = datai.append(buscarDadosOLX(2, estado = i, regiao = reg, palavra = j))
    
datai.to_csv(f'dados_bike_regiaoSUL.csv')
print(datai)

print("Fim!")