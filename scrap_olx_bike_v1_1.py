#!/usr/bin/python
"""This code is scraping the OLX website for ads that contain the keyword "fixie" in the São Paulo region and collecting information about the ads found. It uses the BeautifulSoup library to navigate the HTML structure of 
the page and find the desired elements. It saves the collected information in a dictionary "data" that includes the day and time the ad was posted, the ad's code, the bike's name, the price, the city, 
the neighborhood, the zip code and the ad's URL. It also checks if the ad code has already been collected before to avoid duplicates.
"""
"september, 13, 2023"
"This code has been discontinued because the website changed the way it presents advertisements, necessitating an update in the technique for retrieving ads and values for this site."
from bs4 import BeautifulSoup
import numpy as np
import pandas as pd
import requests


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
            "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36",
            "X-NewRelic-ID":"VQYGVF5SCBAJVlFaAQIH",
            "X-Requested-With":"XMLHttpRequest"
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

        try:

            # nRes = soup.find_all("span", class_="sc-1mi5vq6-0 dQbOE sc-ifAKCX lgjPoE")[0].contents[0]
            nRes = soup.find_all("p", class_="sc-bqiRlB dZqfhU")[0].contents[0]
            
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
            
            maindiv = soup.find_all("div", {"class": "sc-bb3a36b6-0 bPPSiI renderIfVisible"})
            
            for itens in maindiv:

                nBike = itens.find("h2")
                if nBike != None:
                    nameBike = nBike.text
                else:
                    nameBike = " "

                for item in itens.find_all("a"):

                    try:

                        urlBike = item['href']
                        codeAd = urlBike.split('-')[-1]
                        

                    except:

                        codeAd = ' '
                    
                    # remove duplicates during the scrapping ads.
                    if codeAd is self.base_codes or codeAd == ' ':
                        continue
                    
                    try: #open ads and get informations enter on ads and get price
                        
                        page2 = requests.get(url=urlBike, headers=self.PARAMS)
                        soupsp = BeautifulSoup(page2.content, 'lxml')

                        try:
                            # converting from BR presentation of numbers
                            # valueBike = soupsp.find_all("h2", class_="ad__sc-12l420o-1 dnbBJL sc-jTzLTM iyLIyP")[0].contents[0]
                            valueBike = soupsp.find("span", class_="ad__sc-1wimjbb-1 hoHpcC sc-jTzLTM kNahTW").text.split("R$ ")[1].replace('.','')
                            valueBike = float(valueBike)

                        except:

                            valueBike = 0.0
                            
                        try:

                            daytimePost = soupsp.find("span", class_="ad__sc-1oq8jzc-0 dWayMW sc-jTzLTM iGzcjb").text.split(' às ')
                            dayPost = daytimePost[0][-5:]
                            timePost = daytimePost[1]
                            
                        except:

                            dayPost = ' '
                            timePost = ' '
                        try:

                            objectLocat = soupsp.find_all("span", class_="ad__sc-1f2ug0x-1 cpGpXB sc-jTzLTM ieZUgc")
                            vararr = []
                            ij=0
                            while ij < len(objectLocat):
                                ao = objectLocat[ij].text
                                vararr.append(ao)
                                ij=ij+1
                                 
                            cep , city , neighborhood = vararr
                            
                            if cep == '': cep = '00000000'
                            if city == '': cep = 'undef'
                            if neighborhood == '': cep = 'undef'
                            
                                                            
                        except:

                            cep = '00000000'
                            city = 'undef'
                            neighborhood = 'undef'

                        objct_list = [dayPost,timePost,codeAd,nameBike,valueBike,city,neighborhood,cep,urlBike]
                        
                        for ki,kd in enumerate(self.dic_temp.keys()):
                            
                            self.dic_temp[kd].append(objct_list[ki])
                    
                    except:
                        print("Not link of found ads.")

                        for ki,kd in enumerate(self.dic_temp.keys()):

                            self.dic_temp[kd].append(np.nan)


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

    for j in ['bike%20fixa' ,'las%20magrelas', 'raf','raf%20bike','sprinter','8bike', 'fixie', 'nexus','tetrapode', 'alleycat','cernunnos','chandan','fixed','aventon','riva','cinelli']:

        print(j)
        res_page = busca.initial_configs(state = i, region = "0", target_word = j)
        dados_busca = busca.search_ads(res_page=res_page)
        
        if len(dados_busca) > 0:

            dados_busca = pd.DataFrame(dados_busca)
            datai =  pd.concat([datai, dados_busca], ignore_index=True)

        else:

            continue


if len(datai) > 0:

    datai.to_csv(f'busca_bike_dados.csv')
    print(f'tamanho do dataframe {len(datai)}')

else:

    print('Search empty')


print("The end!")