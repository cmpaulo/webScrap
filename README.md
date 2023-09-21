# webScrap
[![scraper-ads](https://github.com/cmpaulo/webScrap/actions/workflows/scrap_olx_bike.yml/badge.svg?branch=main)](https://github.com/cmpaulo/webScrap/actions/workflows/scrap_olx_bike.yml)

<!-- ingles -->
I developed an application to simplify the search for bicycle ads, enhancing it with statistical analysis using Python and pandas. With this, I was able to calculate average values and price quartiles, while also creating interactive charts to visualize price variations in different cities in São Paulo. This initiative showcases my technical skills in Python, pandas, and statistics, as well as the ability to make GET requests using the requests library and interpret HTML and CSS code. Furthermore, I leveraged my experience with the BeautifulSoup tool for web data scraping and used Pandas for data analysis. This product makes the search for bicycle ads more efficient and assists in fair price evaluation. With this application, I have created a valuable resource for bicycle enthusiasts and potential buyers.

This code is scraping the OLX website for ads that contain the keyword "fixie" in the São Paulo region and collecting information about the ads found. It uses the BeautifulSoup library to navigate the HTML structure of the page and find the desired elements. It saves the collected information in a dictionary "data" that includes the day and time the ad was posted, the ad's code, the bike's name, the price, the city, the neighborhood, the zip code and the ad's URL. It also checks if the ad code has already been collected before to avoid duplicates.


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

The result of ads with a value lower than the average value of ads in the state of são paulo is in the table in markdown [TMD](/busca_bike_dados.md) and to check the complete table only of the items related to the search in this [Complete results](/busca_bike_dados_clean.csv)

![graphnumber](/images/median_price_of_bike.png)


## References
[!Freecodecamp.org - Web scraping python tutorial](https://www.freecodecamp.org/news/web-scraping-python-tutorial-how-to-scrape-data-from-a-website)
