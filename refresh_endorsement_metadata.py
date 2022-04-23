import pandas as pd
import requests
from bs4 import BeautifulSoup
import os
import datetime as dt
import smtplib
from email.message import EmailMessage

today = pd.to_datetime("today").strftime("%Y-%m-%d")

trump_url = "https://www.donaldjtrump.com/news/P"

headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) "
    "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36"
}

### Get metadata about the last 10 posts

soups = []

for i in range(0, 2000, 10):
    r = requests.get(trump_url + str(i), headers=headers)
    soups.append(BeautifulSoup(r.text, "html.parser"))

### Extract those elements from the pages

dicts = []

for soup in soups:
    for s in soup.find_all("a", class_="item"):
        url = s["href"]
        date = s.find("p").text
        headline = s.find("h2", class_="title-med-2").text
        data_dict = {
            "date": date,
            "headline": headline,
            "url": str("https://www.donaldjtrump.com") + url,
        }
        dicts.append(data_dict)

### Dataframe with basic metadata 

df = pd.DataFrame(dicts)

df["date"] = pd.to_datetime(df["date"])

### Get release text for each post's page from our metadata

urls = df["url"].to_list()

### Loop over the url list and extract those release pages

release_soup = []

for url in urls:
    release_page = requests.get(url, headers=headers, timeout=15)
    url_text_dict = {
        'url': url,
        'page': BeautifulSoup(release_page.text, "html.parser"),
    }
    release_soup.append(url_text_dict)

### Get elements from the release pages

body_text_dicts = []

for release in release_soup:
    for rl in release['page'].find_all("main", class_="vp-80"):
        try:
            # headline = rl.find("h1", class_="title").text
            # date = rl.find("p", class_="date").text
            body_text = rl.find("div", class_="body").text
            url = release['url']
            text_dict = {
                # "headline": headline,
                # "date": date,
                "body_text": body_text,
                "url": url,
            }
            body_text_dicts.append(text_dict)
        except:
            continue

### Dataframe with posts and clean up text, date

text_df = pd.DataFrame(body_text_dicts)

text_df["body_text"] = text_df["body_text"].str.replace("\n", "")

### Merge the metadata and post text into one dataframe

new_df = pd.merge(df, text_df, on=["url"])

new_df.to_csv('refreshed_releases_metadata.csv', index=False)