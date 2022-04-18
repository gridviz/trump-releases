# Archiving former Presidents Trump's news feed

This repo contains a Github action that finds and archives any new posts on the ["news" section](https://www.donaldjtrump.com/news) of the former president's website. These posts typically consist of four categories: 

- [New candidate endorsements](https://www.donaldjtrump.com/news/news-6hxhjdufq21851)
- [Official statements](https://www.donaldjtrump.com/news/news-mvrzrvg5d61849) 
- ["ICYMI" posts](https://www.donaldjtrump.com/news/news-gzvsvbqznh1868) highlighting links to reports or conservative media
- [Announcements](https://www.donaldjtrump.com/news/news-k9mq7bc4pw1869) for events, such as rallies


### The action runs hourly and produces two CSV files: 

| TABLE   |      DESCRIPTION  |    
|----------|-------------|
| [all_press_releases_archive.csv](https://github.com/gridviz/trump-releases/blob/main/data/processed/all_press_releases_archive.csv) |  All of Trump's 1,500+ statements since Jan. 17, 2021 |
[all_press_releases_latest.csv](https://github.com/gridviz/trump-releases/blob/main/data/processed/all_press_releases_latest.csv) |  Trump's most recent 10 statements|


### The resulting tables contain four variables: 

| COLUMN   |      DESCRIPTION      |
|----------|-------------|
| `date` |  Date of release in `%Y-%m-%d` format. 
| `headline` |  Unedited headline from the release|
| `url` |  URL address of the release|
| `body_text` | Full text of the release without capturing any inline links (yet)|

The [archive](https://github.com/gridviz/trump-releases/blob/main/data/processed/all_press_releases_archive.csv) also has the dates parsed into `year`,`month`,`weekday` and `month_year` columns.

Please [let us know](mailto:mstiles@grid.news) if you have any questions or comments. 
