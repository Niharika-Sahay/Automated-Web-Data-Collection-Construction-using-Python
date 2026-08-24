#Importing required libraries
import requests
from bs4 import BeautifulSoup
import pandas as pd

#Implementing pagination style web-scrapping
data_items=[]
for i in range(1,18):
  url = f"https://webscraper.io/test-sites/pagination?page={i}"
  page= requests.get(url)
  #print(page) -->checking response status [200]

  soup = BeautifulSoup(page.content, 'html.parser')
  #print(soup)

  card_container = soup.find('div', class_= 'row test-items-container g-4 mb-3')
  cards = card_container.find_all('div', class_='card sitemap-card test-sites-card' )

  for card in cards:
    availability = card.find_all('div', class_='badge')
    for avail in availability:
      avail_text= avail.get_text().strip()
      #print(avail_text)

    titles = card.find_all('h3', class_='card-title mt-3 mb-0')
    for title in titles:
      title_text = title.get_text().strip()
      #print(title_text)

    description = card.find_all('p', class_='description text-muted')
    for desc in description:
      desc_text = desc.get_text().strip()
      #print(desc_text)

    years = card.find_all('p', class_='card-text')[0::3]
    for year in years:
      year_text = year.get_text().strip()
      year_text = year_text.replace('Year:  ', '')
      #print(year_text)

    countries = card.find_all('p', class_='card-text')[1::3]
    for country in countries:
      country_text = country.get_text().strip()
      country_text = country_text.replace('Country of origin:  ', '')
      #print(country_text)

    mileages = card.find_all('p', class_='card-text')[2::3]
    for mil in mileages:
      mil_text = mil.get_text().strip()
      mil_text = mil_text.replace('Mileage:  ', '')
      mil_text = mil_text.replace(' km', '')
      #print(mil_text)

    ratings = card.find_all('div', class_='col-6 rarity-rating d-flex flex-row justify-content-start p-0')
    for rating in ratings:
      rating_value = rating.get('data-rating')
      #print(rating_value)

    prices = card.find_all(attrs={"itemprop": "price"})
    for price in prices:
      price_text = price.get_text().strip()
      price_text = price_text.replace('USD ', '')
      #print(price_text)

    #Adding the scrapped data into a list to order them
    data_items.append([title_text,avail_text,desc_text, year_text, country_text, mil_text,rating_value, price_text])
    #print(data_items)

#Creating a DataFrame with the columns to add the scrapped data
df = pd.DataFrame(data_items, columns=['Title', 'Availability_Status', 'Description', 'Year', 'Country of Origin', 'Mileage', 'Rating', 'Price'])

#For Availability_Status values like Available:1, splitting the status and number of available into two columns
df[['Availability', 'Number of Available']] = df['Availability_Status'].str.split(':', n=1, expand=True)

#Saving into a CSV File
df.to_csv('Car Dataset')
