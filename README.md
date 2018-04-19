# Craigslist Car Scraper
A simple python script that extracts information from Craigslist car ads and exports it into a google sheet. The Craigslist Car Scraper extracts the price, brand, model, year, location, and number of miles. 

## Instalation
The Craigslist Car Scraper uses python2 and the following packages:
* Gspread
* Oauthclient2
* BeautifulSoup4

You will also need an OAuth token from Google named "craigslist.json", and a google sheet named "Cars" that is shared with your service account.

## Usage
To use the Craigslist Car Scraper, simply add the URLs of the Craigslist listings you would like to organize to the "listings" array. Additionally you can sort these listings by adding a tag. 

Sorting Options| Action
-------------- | ------
priceAccending|Sorts the list by price from least to greatest
priceDecending|Sorts the list by price from greatest to least
milesAccending|Sorts the list by miles from least to greatest
milesDecending|Sorts the list by miles from greatest to least
yearAccending|Sorts the list by year from least to greatest
yearDecending|Sorts the list by year from greatest to least
brand|Sorts the list by brand
location|Sorts the list by location

For example: "python CraigslistCarScraper.py priceAccending" sorts the list from least to greatest price

### Exceptions
Sometimes a Craigslist posting will be in an unusual format or not have all the information listed. In this case the script will print " *insert url here* needs more information"
