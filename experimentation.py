from bs4 import BeautifulSoup as bs
import requests
import csv

def nyt_scrape():
    source3 = requests.get("https://rss.nytimes.com/services/xml/rss/nyt/Europe.xml").text

    soup3 = bs(source3, 'xml')
    with open(r'/Users/kristatingbrand/Desktop/appyapp/corona_scraper/database elements/CSV/nyt_scrape.csv', "a") as csv_file_nyt:
        csv_reader_nyt = csv.reader(csv_file_nyt)
        for row in csv_reader_nyt:
            print(row)

        for article3 in soup3.find_all('item'):
            title = article3.title.text
            summary = article3.description.text
            website = article3.link.text
            date = article3.pubDate.text

            if "corona" in summary or "corona" in title or "virus" in summary or "virus" in title:
                print(summary)
                print(title)
                print(website)
                print(date)

                print()

    csv_file_nyt.close()

nyt_scrape()