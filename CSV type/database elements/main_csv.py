from bs4 import BeautifulSoup as bs
import requests
import csv

def bbc_scrape():
    source = requests.get("http://feeds.bbci.co.uk/news/health/rss.xml").text

    soup = bs(source, 'xml')

    csv_file_bbc = open('bbc_scrape.csv', 'w')
    csv_writer = csv.writer(csv_file_bbc)
    csv_writer.writerow(["Date", "Link", "Title", "Summary"])

    for article in soup.find_all('item'):
        title = article.title.text
        summary = article.description.text
        website = article.guid.text
        date = article.pubDate.text
        if "corona" in summary or "corona" in title or "virus" in summary or "virus" in title:
            print(summary)
            print(title)
            print(website)
            print(date)

            print()
            csv_writer.writerow([date, website, title, summary])

    csv_file_bbc.close()

def guardian_scrape():
    source2 = requests.get("https://www.theguardian.com/world/rss").text

    soup2 = bs(source2, 'xml')

    csv_file_guardian = open('guardian_scrape.csv', 'w')
    csv_writer_guardian = csv.writer(csv_file_guardian)
    csv_writer_guardian.writerow(["Date", "Website", "Title", "Summary"])

    for article2 in soup2.find_all('item'):
        title = article2.title.text
        summary = article2.description.text
        website = article2.link.text
        date = article2.pubDate.text
        if "corona" in summary or "corona" in title or "virus" in summary or "virus" in title:
            print(summary)
            print(title)
            print(website)
            print(date)

            print()
            csv_writer_guardian.writerow([date, website, title, summary])

    csv_file_guardian.close()

def nyt_scrape():
    source3 = requests.get("https://rss.nytimes.com/services/xml/rss/nyt/Europe.xml").text

    soup3 = bs(source3, 'xml')

    csv_file_nyt = open('nyt_scrape.csv', 'w')
    csv_writer_nyt = csv.writer(csv_file_nyt)
    csv_writer_nyt.writerow(["Date", "Website", "Title", "Summary"])

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
            csv_writer_nyt.writerow([date, website, title, summary])

    csv_file_nyt.close()

bbc_scrape()
guardian_scrape()
nyt_scrape()


