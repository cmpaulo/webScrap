# webScrap
[![scraper-ads](https://github.com/cmpaulo/webScrap/actions/workflows/scrap_olx_bike.yml/badge.svg)](https://github.com/cmpaulo/webScrap/actions/workflows/scrap_olx_bike.yml)

<!-- ingles -->

# WebScraping first step.

## Authors: Paulo, Claudio M. 

First steps in Web Scraping. Project carried out for training in Web Scrapping.
The export of information to a structured database (Pandas DataFrame) where the information was obtained by making a request() call from pages with known addresses. Find the information in the 'lxml' code formatted by BeautfullSoup, and finally exported in csv format.

- How to automate the search for related words in OLX ads.

- Can I use quartile analysis to find the best product at the best price?


## Our Plan

1. Select the list of related words.
 
2. Use requests to download the page.

3. Use BSsoup to format the downloaded page in lxml.

4. Create a structured database with date and time of posting, ad title, product value, city and neighborhood where it is being advertised.

5. Filter the database by removing ads whose ad title does not contain the desired words.

6. Use the percentile and average value metric to find the average price of advertisements by cities (of Brazilian states).

## Current progress

Data scraping was carried out and the database was created to analyze the average value by city. 

Database formed by information in OLX Brasil website advertisements.

The code is with variables and comments in Portuguese, and the search for advertisements is carried out with words in the Portuguese language.

The images are updated every 12 hours, and show the result of the search for keywords in each Brazilian state, only on the OLX advertising website (Brazil).

## Conclusions

The data obtained allows answers to questions with a graphic presentation of the average value of bicycles per city.


![graphnumber](/images/median_price_of_bike.png)


![graph1](/images/number_of_ads_bycity.png)

## References
[!Freecodecamp.org - Web scraping python tutorial](https://www.freecodecamp.org/news/web-scraping-python-tutorial-how-to-scrape-data-from-a-website)
