#!/usr/bin/python

from re import L
from bs4 import BeautifulSoup
import numpy as np
import pandas as pd
import requests

# https://sp.olx.com.br/ciclismo?q=bike%20fixa
# https://sp.olx.com.br/sao-paulo-e-region/ciclismo?q=bike%20fixa
# https://sp.olx.com.br/sao-paulo-e-region/ciclismo?o=2&q=bike%20fixa
# meltime o try para obter mais resultados.
# Obtém a URL
# target_words para buscar [Airwalk, RAF, 8Bike, Nexus, Vicinitech, Tetrapode]


class scrap_olx_ads():

    
    def __init__(self):
        self.base_codes = []
        self.dic_temp = {'dayPost':[], 'timePost':[], 'codeAd':[], 'nameBike':[], 'valueBike':[], 'city':[], 'neighborhood':[], 'cep':[], 'urlBike':[]}


        
    def initial_configs(self, state= "SP", region = "11", target_word = "fixa"):

        regionBuscar = {"0":"","11":"sao-paulo-e-regiao"}
        state = state.lower()
        target_word = target_word.lower()

        if region == "0":
            self.url = f"https://{state}.olx.com.br/ciclismo?q={target_word}&sf=1"

        else:
            self.url = f"https://{state}.olx.com.br/{regionBuscar[region]}/ciclismo?q={target_word}&sf=1"
            

        self.PARAMS = {
            "authority" : "sp.olx.com.br",
            "method": "GET",
            "path": "sao-paulo-e-region/ciclismo",
            "scheme" : "https",
            "referer" : "https://sp.olx.com.br/sao-paulo-e-region/ciclismo",
            "sec-fetch-mode" : "navigate",
            "sec-fetch-site" : "same-origin",
            "sec-fetch-user" : "?1",
            "upgrade-insecure-requests":"1",
            "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36"
        }

        page = requests.get(url=self.url, headers=self.PARAMS)
    
        if (page.status_code != 200):

            print('Remote problem', 'code status ', page.status_code)
            exit()

        else:

            print('OK')

        
        return page

    
    def search_ads(self, res_page):

        
        soup = BeautifulSoup(res_page.content, 'lxml')

        nRes = soup.find_all("span", class_="sc-1mi5vq6-0 eDXljX sc-ifAKCX fhJlIo")[0].contents[0]


        if len(nRes) > 20:

            try:

                if 'resultados' in nRes:

                    tpages = int( int( nRes.split(" ")[-2].replace(".","") ) / 50 )

            except:

                print("erro paginas")
                tpages = 0
        
        if int(tpages) > 10:

            tpages = 3
        
        print(tpages)


        for ipages in range(1,tpages+1):

            res_page = requests.get(url=self.url.replace('?',f'?o={ipages}&'), headers=self.PARAMS)
            soup = BeautifulSoup(res_page.content, 'lxml')

            for itens in soup.find_all("ul", {"class": "sc-1fcmfeb-1 kntIvV"}):

                for item in itens.find_all("li"):

                    try:
                        
                        nameBike = item.find_all('h2')[0].contents[0]
                        
                        try:

                            urlBike = item.find('a')['href']
                            codeAd = urlBike.split('-')[-1]

                        except:

                            codeAd = ' '
                        
                        # remove duplicates during the scrapping ads.
                        if codeAd is self.base_codes or codeAd == ' ':
                            continue

                        try: #open ads and get informations
                            
                            page2 = requests.get(url=urlBike, headers=self.PARAMS)
                            soupsp = BeautifulSoup(page2.content, 'lxml')

                            try:
                                # converting from BR presentation of numbers
                                valueBike = soupsp.find_all("h2", class_="sc-1wimjbb-2 iUSogS sc-ifAKCX cmFKIN")[0].contents[0].split("R$ ")[1].replace('.','')
                                valueBike = float(valueBike)

                            except:

                                valueBike = ' '

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


                            objct_list = [dayPost,timePost,codeAd,nameBike,valueBike,city,neighborhood,cep,urlBike]
                            
                            for ki,kd in enumerate(self.dic_temp.keys()):
                                
                                self.dic_temp[kd].append(objct_list[ki])
                       
                        except:
                            print("Not link of found ads.")

                            for ki,kd in enumerate(self.dic_temp.keys()):

                                self.dic_temp[kd].append(np.nan)
        

                    except:

                        print("Not found ads.")

                        for ki,kd in enumerate(self.dic_temp.keys()):

                            self.dic_temp[kd].append(np.nan)
        

        return self.dic_temp

# Referência de busca: fixie, barra forte,bike urbana, urban bike, single speed, bike speed, colossi, 8bike, fuji, trek, cannondale, specialized, Night Riders, 
# Specialized Langster, Caloi, Aço Hi-ten, aro 700. #Caloi City Tour
#['sense','sense%20urban','sense%20move'
# btwin, focus, pinarello, Soul, sundown, vicinitech, gancheira horizontal, gancheira pista, aventon, miyamura, sugino, dura Ace, shimano, chandan, Raf bikes, caloi 10, caloi 12, monark 10, peugeot 10, giant, audax, tsw, groove, oggi, riva, cernnunos, república, Ferroveló, caixinha, caixa, sunburst, airwalk, black flea, ColorBikes, eight bikes, nirve belmont, Eagle bikes, foffa, cubos rolamentados, flip flop, contra pedal, quadro fixa, bicicleta.
    # for j in ['bike%20fixa', 'raf','raf bike','sprinter','8bike', 'fixie', 'nexus','tetrapode', 'alleycat','cernunnos','chandan','fixed','aventon','riva','cinelli','single','bike%20fixa']:

datai = pd.DataFrame()

busca = scrap_olx_ads()


for i in ["SP"]:

    for j in ['bike%20fixa','las%20magrelas', 'raf','raf%20bike','sprinter','8bike', 'fixie', 'nexus','tetrapode', 'alleycat','cernunnos','chandan','fixed','aventon','riva','cinelli','single']:

        print(j)
        reg = "0"
        res_page = busca.initial_configs(state = i, region = reg, target_word = j)
        dados_busca = busca.search_ads(res_page=res_page)
        
        if len(dados_busca) > 0:

            dados_busca = pd.DataFrame(dados_busca)
            datai = datai.append(dados_busca)

        else:

            continue


if len(datai) > 0:

    datai.to_csv(f'busca_bike_dados.csv')
    print(f'tamanho do dataframe {len(datai)}')

else:

    print('Search empty')


print("The end!")
