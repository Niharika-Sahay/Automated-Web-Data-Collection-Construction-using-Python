### Pagination Web Scraper & Car Dataset Analyzer

A robust data extraction and analytics pipeline built in Python. The project uses **BeautifulSoup** and **Requests** to programmatically scrape tabular, multi-page data from a live paginated testing environment (webscraper.io), handles key string manipulation tasks via **Pandas**, and executes primary Exploratory Data Analysis (EDA) metrics. 

### Project Pipeline Overview

1. **Dynamic Ingestion (Pagination)**: Iterates sequentially through 17 dynamic pages (page=1 to page=17) leveraging the requests library to fetch structural HTML blocks.
2. **DOM Parsing & Scraping (BeautifulSoup)**: Targets nested card objects within specific container columns (div.card) to isolate unstructured text streams for vehicle attributes.
3. **Data Transformation & Structural Splitting**: Cleans textual suffixes and splits composite properties (such as string keys like Available:1 into independent features).
4. **Data Aggregation & EDA (Pandas)**: Stores compiled matrices to a local flat CSV file before parsing structural datatypes to calculate statistical summary metrics.

### Web Scraping Execution (Python & BeautifulSoup)

The scraper traverses the site DOM using careful index mapping patterns to collect structural tags across multiple pages: 

* **Target Selection**: Pulls target wrapper classes row test-items-container and drills down into individual .sitemap-card nodes.
* **Property Slicing**: Handles repeating child paragraphs <p class="card-text"> using step-slicing rules ([0::3], [1::3], [2::3]) to map unstructured elements accurately to **Year**, **Country of Origin**, and **Mileage**.
* **Attribute Parsing**: Extracts specific operational tags directly (such as retrieving data-rating values directly from inline style tags).

### Scraped Features Captured:

* Title (Vehicle model name)
* Availability_Status (Composite tag layout e.g. Available:1, Reserved, Sold)
* Description (Contextual tag string)
* Year (Extracted integer)
* Country of Origin
* Mileage (Cleaned numerical kilometer values)
* Rating (Rarity metric value score)
* Price (Cleaned numeric value)

### Data Formatting & Transformation Steps

To transition data from arbitrary raw string captures into high-value relational variables, the script performs the following data-cleaning operations via Pandas: 

### 1. Feature Engineering (String Splitting)

The composite column Availability_Status containing strings like "Available:1" is parsed dynamically to split its categorical values from operational count flags: 
```
df[['Availability', 'Number of Available']] = df['Availability_Status'].str.split(':', n=1, expand=True)
```

### 2. Numerical Normalization

Cleans out non-numeric structures (like space separators and km text tags), applying explicit coercion protocols (errors='coerce') to safely convert elements to clean float data tracking structures: 
```
df1["Price"] = pd.to_numeric(df1["Price"].str.replace(" ", ""), errors="coerce")
df1["Mileage"] = pd.to_numeric(df1["Mileage"].str.replace(" ", "").str.replace("km", ""), errors="coerce")
```

### Exploratory Data Analysis & Aggregation Insights

The script automatically executes a terminal reporting suite that tracks absolute collection statistics and pricing margins: 

* **Duplication & Uniqueness Profiling**: Calculates explicit distinct row sums using .nunique() and checks for duplicate data logs with .duplicated().sum().
* **Value Distribution Averages**: Evaluates core mathematical statistics (.mean(), .min(), .max()) on continuous variables to build a high-level dataset summary profile.

### Generated Console Output Format Example:
```
========== DATASET SUMMARY ==========
Total records collected : [Count]
Unique vehicles         : [Count]
Average price           : ₹[Formatted Value]
Minimum price           : ₹[Formatted Value]
Maximum price           : ₹[Formatted Value]
Average rating          : [Value]
======================================
```

### Requirements & Environment Setup

To run this pipeline locally, install the necessary Python external libraries: 
```

pip install requests beautifulsoup4 pandas
```

### Project File Tree Structure:

* main.py - Core execution script containing retrieval algorithms and EDA code blocks.
* Car Dataset - Raw generated flat CSV output holding parsed vehicle entries.

![Car Dataset Screenshot]()

>[!NOTE]
>This script connects to a designated [web scraping demo platform sandbox](webscraper.io/test-sites/pagination). All data objects, pricing numbers, and luxury model metrics are fictional, synthesized strictly for analytics testing and software simulation validation purposes.
