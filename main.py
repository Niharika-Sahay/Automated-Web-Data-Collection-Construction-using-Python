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


#Exploring the Dataset

#Creating another DataFrame
df1 = pd.read_csv("Car Dataset")

#High-level information about the Dataset
print(df1.info())

#Number of Records Collected
number_of_records = len(df1)
print("Total records collected:", number_of_records)

#Unique Records
unique_vehicles = df1["Title"].nunique()
print("Number of unique vehicles:", unique_vehicles)

#Duplicate Records
duplicates = df1["Title"].duplicated().sum()
print("Duplicate vehicle records:", duplicates)


#Coverting price from str to float and replacing spaces between them into commas
df1["Price"] = (
    df1["Price"]
    .astype(str)
    .str.replace(" ", "", regex=False)
)

df1["Price"] = pd.to_numeric(df1["Price"], errors="coerce")

df1["Mileage"] = (
    df1["Mileage"]
    .astype(str)
    .str.replace(" ", "", regex=False)
    .str.replace("km", "", regex=False)
)

df1["Mileage"] = pd.to_numeric(df1["Mileage"], errors="coerce")

#Average Price
average_price = df1["Price"].mean()
print(f"Average price: ₹{average_price:,.2f}")

#Min-Max Price
minimum_price = df1["Price"].min()
maximum_price = df1["Price"].max()
print(f"Minimum price: ₹{minimum_price:,.2f}")
print(f"Maximum price: ₹{maximum_price:,.2f}")
print(f"Price range: ₹{minimum_price:,.2f} - ₹{maximum_price:,.2f}")

#Average Rating
average_rating = df1["Rating"].mean()
print(f"Average rating: {average_rating:.2f}")

print("========== DATASET SUMMARY ==========")

print(f"Total records collected : {len(df1)}")
print(f"Unique vehicles         : {df1['Title'].nunique()}")
print(f"Average price           : ₹{df1['Price'].mean():,.2f}")
print(f"Minimum price           : ₹{df1['Price'].min():,.2f}")
print(f"Maximum price           : ₹{df1['Price'].max():,.2f}")
print(f"Average rating          : {df1['Rating'].mean():.2f}")

print("======================================")
