import requests
from bs4 import BeautifulSoup
import time
import pandas as pd
import os

# fixed part of the URL
url1 = "https://books.toscrape.com/catalogue/"

# list to hold the final URLs
urls = []

# creating the final URLs and adding them to the list
for i in range(50):
    a = i + 1
    url2 = f"page-{a}.html"
    urlLast = url1 + url2
    urls.append(urlLast)

# browser identity, to avoid issues with requests
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

# data dictionary to hold book names and URLs
data = {}

# iterating over the URLs we prepared earlier
for i, url in enumerate(urls, start = 1):
    # sending request for each URL
    response = requests.get(url, headers = headers)

    # printing status information
    if response.status_code == 200:
        print(f"Successfully accessed the page {i} !")
    else:
        print(f"Error: {response.status_code}")
        exit()

    time.sleep(1)

    # defining the received HTML as a BeautifulSoup object
    soup = BeautifulSoup(response.content, "html.parser")


    # creating a list that holds the addresses of our data
    links = soup.select("article.product_pod h3 a")


    # retrieving the data at each address and adding it to the "data" dictionary ("title": "url")
    for a in links:
        title = a.get("title")
        href = a.get("href")
        data[title] = href

# creating a dataframe from the keys and values in the "data" dictionary
df = pd.DataFrame(list(data.items()), columns = ["bookName", "link"])

# setting the directory of the file as the default directory
cur_dir = os.path.dirname(os.path.abspath(__file__))

# creating the path where the CSV file will be saved
csv_path = os.path.join(cur_dir, "books.csv")

# saving our dataframe as a CSV file to the desired path
df.to_csv(csv_path, index = False, encoding = "utf-8")

# informational message
print(f"Saved the CSV file: {csv_path}")
