#!/usr/bin/python

from bs4 import BeautifulSoup
import numpy as np
import pandas as pd
import requests

# https://sp.olx.com.br/ciclismo?q=bike%20fixa
# https://sp.olx.com.br/sao-paulo-e-regiao/ciclismo?q=bike%20fixa
# https://sp.olx.com.br/sao-paulo-e-regiao/ciclismo?o=2&q=bike%20fixa
# melhora o try para obter mais resultados.
# Obtém a URL
# palavras para buscar [Airwalk, RAF, 8Bike, Nexus, Vicinitech, Tetrapode]

def buscarDadosOLX(estado= "SP", regiao = "11", palavra = "fixa"):
    regiaoBuscar = {"0":"","11":"sao-paulo-e-regiao"}
    listaAnuncios = []
    estado = estado.lower()
    palavra = palavra.lower()
    if regiao == "0":
        url = f"https://{estado}.olx.com.br/ciclismo?q={palavra}&sf=1"

    else:
        url = f"https://{estado}.olx.com.br/{regiaoBuscar[regiao]}/ciclismo?q={palavra}&sf=1"
        
    PARAMS = {
        "authority" : "sp.olx.com.br",
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
    
    if (page.status_code != 200):
        print('problema no servidor', 'code status ', page.status_code)
        exit()
    else:
        print('OK')
    
    soup = BeautifulSoup(page.content, 'lxml')

    nResultadosBusca = soup.find_all("span", class_="sc-1mi5vq6-0 eDXljX sc-ifAKCX fhJlIo")[0].contents[0]

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
                    try:
                        precoBike = item.find_all("span", class_="sc-ifAKCX eoKYee")[0].contents[0].split("R$")[1].replace('.','')
                        precoBike = float(precoBike)
                    except:
                        precoBike = np.nan
                    try:
                        diaPostagem = item.find_all("span", class_="wlwg1t-1 fsgKJO sc-ifAKCX eLPYJb")[0].contents[0]
                    except:
                        diaPostagem = np.nan
                    try:
                        horaPostagem = item.find_all("span", class_="wlwg1t-1 fsgKJO sc-ifAKCX eLPYJb")[1].contents[0]
                    except:
                        horaPostagem = np.nan
                    try:
                        urlBike = item.find('a')['href']
                        codAnuncio = urlBike.split('-')[-1]
                    except:
                        codAnuncio = np.nan
                    try:
                        localiza = item.find_all("span", class_="sc-7l84qu-1 ciykCV sc-ifAKCX dpURtf")[0].contents[0]
                        locais = localiza.split(',')
                        cidade = locais[0]
                        bairro = locais[1]
                    except:
                        cidade = localiza
                        bairro = ' '
                
                    try:
                        # get distance form initialcep of street to cep of ad.
                        page2 = requests.get(url=urlBike, headers=PARAMS)
                        soupsp = BeautifulSoup(page2.content, 'lxml')
                        cep = soupsp.find_all("dd", class_="sc-1f2ug0x-1 ljYeKO sc-ifAKCX kaNiaQ")[0].contents[0]
                    except:
                        cep = np.nan

                    listaAnuncios.append([diaPostagem,horaPostagem,codAnuncio,nomeBike,precoBike,cidade,bairro,cep,urlBike])
                except:
                    print("Item não identificado como anuncio.")
                    listaAnuncios.append(np.ones(9)*np.nan )
        
    name = ['diaPostagem', 'hora','codigo','nomeBike','precoBike','cidade','bairro','cep','urlBike']
    data = pd.DataFrame(listaAnuncios, columns=name)
        # data.to_csv(f'dados_bike_{estado}_{regiao}.csv')
    return data


# Referência de busca: fixie, barra forte,bike urbana, urban bike, single speed, bike speed, colossi, 8bike, fuji, trek, cannondale, specialized, Night Riders, 
# Specialized Langster, Caloi, Aço Hi-ten, aro 700. #Caloi City Tour
#['sense','sense%20urban','sense%20move'
# btwin, focus, pinarello, Soul, sundown, vicinitech, gancheira horizontal, gancheira pista, aventon, miyamura, sugino, dura Ace, shimano, chandan, Raf bikes, caloi 10, caloi 12, monark 10, peugeot 10, giant, audax, tsw, groove, oggi, riva, cernnunos, república, Ferroveló, caixinha, caixa, sunburst, airwalk, black flea, ColorBikes, eight bikes, nirve belmont, Eagle bikes, foffa, cubos rolamentados, flip flop, contra pedal, quadro fixa, bicicleta.
    # for j in ['raf','sprinter','8bike', 'fixie', 'nexus','tetrapode', 'alleycat','cernunnos','chandan','fixed','aventon','riva','cinelli','single','bike%20fixa']:

datai = pd.DataFrame()

# for i in ["SP","PR","SC","RS"]:
# buscar bicicleta que foram roubadas pelo nome do anuncio, selecionar as bicicletas que estão com o valor abaixo da média onde poderia estar anunciada a bicicleta que foi roubada.
#1/ sunburst, hotdog
#2/ 8bike, rosa

for i in ["SP"]:
    for j in ['8bike', 'sunburst', 'hotdog', 'caixinha', 'caixa', 'bike%20fixa', 'bicicleta%20fixa', 'barra%20fixa', 'night%20riders']:
        print(j)
        reg = "0"
        datai = datai.append(buscarDadosOLX(estado = i, regiao = reg, palavra = j))
    
datai.to_csv(f'dados_bike_busca.csv')
print(f'tamanho do dataframe {len(datai)}')

print("Fim!")
