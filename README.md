# Archiving former Presidents Trump's news feed

This repo contains a Github action that finds and archives any new endorsements or statements released on the ["news" section](https://www.donaldjtrump.com/news) of the former president's website. It runs hourly.


### The action produces two CSV files: 

| TABLE   |      DESCRIPTION  |    
|----------|-------------|
| [all_press_releases_archive.csv](https://github.com/gridviz/trump-releases/blob/main/data/processed/all_press_releases_archive.csv) |  All of Trump's statements since Jan. 17, 2021 |
[all_press_releases_latest.csv](https://github.com/gridviz/trump-releases/blob/main/data/processed/all_press_releases_latest.csv) |  Trump's most recent 10 statements|


### The tables contain four key variables: 

| COLUMN   |      DESCRIPTION      |
|----------|-------------|
| `date` |  Date of release in `%Y-%m-%d` format. 
| `headline` |  Unedited headline from the release|
| `url` |  URL address of the release|
| `body_text` | Full text of the release without capturing any inline links (yet)|

The [archive](https://github.com/gridviz/trump-releases/blob/main/data/processed/all_press_releases_archive.csv) also has the dates parsed into `year`,`month`,`weekday` and `month_year` columns.

Please [let us know](mailto:mstiles@grid.news) if you have any questions or comments. 
