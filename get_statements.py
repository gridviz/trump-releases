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

soups = []

for i in range(0, 10, 10):
    r = requests.get(trump_url + str(i), headers=headers)
    soups.append(BeautifulSoup(r.text, "html.parser"))
    

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
        
df = pd.DataFrame(dicts).drop_duplicates()
df["date"] = pd.to_datetime(df["date"])

urls = df["url"].to_list()

release_soup = []

for url in urls:
    release_page = requests.get(url, headers=headers, timeout=15)
    release_soup.append(BeautifulSoup(release_page.text, "html.parser"))
    
body_text_dicts = []

for release in release_soup:
    for rl in release.find_all("main", class_="vp-80"):
        try:
            headline = rl.find("h1", class_="title").text
            date = rl.find("p", class_="date").text
            body_text = rl.find("div", class_="body").text
            text_dict = {
                "headline": headline,
                "date": date,
                "body_text": body_text,
            }
            body_text_dicts.append(text_dict)
        except:
            continue
            
text_df = pd.DataFrame(body_text_dicts).drop_duplicates()

text_df["body_text"] = text_df["body_text"].str.replace("\n", "")
text_df["date"] = pd.to_datetime(text_df["date"])

merged_df = pd.merge(df, text_df, on=["headline", "date"])

merged_df["year"] = merged_df["date"].dt.year
merged_df["month"] = merged_df["date"].dt.month_name()
merged_df["weekday"] = merged_df["date"].dt.day_name()
merged_df["month_year"] = pd.to_datetime(merged_df["date"]).dt.to_period("M")

archive_df = pd.read_csv('data/processed/all_press_releases_archive.csv')
latest_df = pd.concat([archive_df, merged_df]).reset_index(drop='True').drop_duplicates()
latest_df.to_csv(f"data/processed/archives_timeseries/all_press_releases_archive_{today}.csv", index=False)

merged_df.to_csv(f"data/processed/all_press_releases_latest.csv", index=False)

record_count = len(merged_df) + len(archive_df)

if record_count < len(latest_df):
    diff = len(latest_df) - len(archive_df)
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
