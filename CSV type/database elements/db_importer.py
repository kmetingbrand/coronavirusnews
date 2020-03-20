import sqlite3
import pandas as pd

conn = sqlite3.connect('/Users/kristatingbrand/Desktop/appyapp/corona_scraper/database elements/CSV/scraped_news.db')

read_bbc = pd.read_csv(r'/Users/kristatingbrand/Desktop/appyapp/corona_scraper/database elements/CSV/bbc_scrape.csv')
read_bbc.to_sql('BBC', conn, if_exists='append', index = False)

read_guardian = pd.read_csv(r'/Users/kristatingbrand/Desktop/appyapp/corona_scraper/database elements/CSV/guardian_scrape.csv')
read_guardian.to_sql('Guardian', conn, if_exists='append', index = False)

read_nyt = pd.read_csv(r'/Users/kristatingbrand/Desktop/appyapp/corona_scraper/database elements/CSV/nyt_scrape.csv')
read_nyt.to_sql('NYT', conn, if_exists='replace', index = False)

conn.close()
