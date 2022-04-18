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

for i in range(0, 10, 10):
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

### Dates

new_df["year"] = new_df["date"].dt.year
new_df["month"] = new_df["date"].dt.month_name()
new_df["weekday"] = new_df["date"].dt.day_name()
new_df["month_year"] = pd.to_datetime(new_df["date"]).dt.to_period("M")

### Export the most recent 10 posts

new_df.to_csv(f"data/processed/all_press_releases_latest.csv", index=False)

### Read the archive 

archive_df = pd.read_csv('data/processed/all_press_releases_archive.csv').drop_duplicates(subset='url')

### Merge 'em together

new_archive_df = pd.concat([archive_df, new_df]).reset_index(drop='True').drop_duplicates(subset='url')

new_archive_df['date'] = pd.to_datetime(new_archive_df['date'])

new_archive_df = new_archive_df.sort_values('date', ascending=False).reset_index(drop='True')

### Export and archive
new_archive_df.to_csv("data/processed/archives_timeseries/all_press_releases_archive.csv", index=False)
new_archive_df.to_csv(f"data/processed/archives_timeseries/all_press_releases_archive_{today}.csv", index=False)
new_archive_df.to_csv(f"data/processed/all_press_releases_archive.csv", index=False)

### Send an email with tailored messages based on whether there's new stuff

diff = (len(new_archive_df) - len(archive_df)) - len(new_df)

if diff >= 1:
    if diff > 1:
        email = f"We've scraped {diff} new items from the former president's news site. See the latest here: https://github.com/gridviz/trump-releases/blob/main/data/processed/all_press_releases_latest.csv"
        subject = f'New Trump scraper result: {diff} new items!'
    else: 
        email = f"We've scraped a new item from the former president's news site. See the latest here: https://github.com/gridviz/trump-releases/blob/main/data/processed/all_press_releases_latest.csv"
        subject = f'New Trump scraper result: one new item!'
else: 
    email = 'The scrape turned up nothing new.'
    subject = 'New scraper result: Nothing to see here.'

# get email and password from environment variables
EMAIL_ADDRESS = os.environ.get('EMAIL_ADDRESS')
EMAIL_PASSWORD = os.environ.get('EMAIL_PASSWORD')
EMAIL_RECIPIENT = os.environ.get('EMAIL_RECIPIENT')
    
# set up email content
msg = EmailMessage()
msg['Subject'] = subject
msg['From'] = EMAIL_ADDRESS
msg['To'] = EMAIL_RECIPIENT
msg.set_content(f'{email}')
    
# send email
with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
    smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
    smtp.send_message(msg)