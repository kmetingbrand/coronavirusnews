from bs4 import BeautifulSoup as bs
import requests
import sqlite3

class CoronaScrape():
    def __init__(self):
        self.conn = sqlite3.connect("db/news.db")
        self.c = self.conn.cursor()

        query = "SELECT count(name) FROM sqlite_master WHERE type='table' AND name='bbc'"
        self.c.execute(query)
        if not self.c.fetchone()[0] == 1:
            self.__createttables()
    
    def __createttables(self):
        self.c.execute("""CREATE TABLE bbc (
                    title text,
                    summary text,
                    website text,
                    date text
                    )""")
        
        self.c.execute("""CREATE TABLE guardian (
                    title text,
                    summary text,
                    website text,
                    date text
                    )""")
        
        self.c.execute("""CREATE TABLE nyt (
                    title text,
                    summary text,
                    website text,
                    date text
                    )""")

        self.conn.commit()
    
    def bbc_scrape(self):
        self.source = requests.get("http://feeds.bbci.co.uk/news/health/rss.xml").text

        self.soup = bs(self.source, 'xml')

        for article in self.soup.find_all('item'):
            title1 = article.title.text
            summary1 = article.description.text
            website1 = article.guid.text
            date1 = article.pubDate.text
            if "corona" in summary1 or "corona" in title1 or "virus" in summary1 or "virus" in title1:
                self.news_appender_bbc(title1, summary1, website1, date1)

    def guardian_scrape(self):
        self.source2 = requests.get("https://www.theguardian.com/world/rss").text

        self.soup2 = bs(self.source2, 'xml')

        for article2 in self.soup2.find_all('item'):
            title2 = article2.title.text
            summary2 = article2.description.text
            website2 = article2.link.text
            date2 = article2.pubDate.text
            if "corona" in summary2 or "corona" in title2 or "virus" in summary2 or "virus" in title2:
                self.news_appender_guardian(title2, summary2, website2, date2)

    def nyt_scrape(self):
        self.source3 = requests.get("https://rss.nytimes.com/services/xml/rss/nyt/Europe.xml").text

        self.soup3 = bs(self.source3, 'xml')
        
        for article3 in self.soup3.find_all('item'):
            title3 = article3.title.text
            summary3 = article3.description.text
            website3 = article3.link.text
            date3 = article3.pubDate.text
            if "corona" in summary3 or "corona" in title3 or "virus" in summary3 or "virus" in title3:
                self.news_appender_nyt(title3, summary3, website3, date3)
    
    def news_appender_bbc(self, title1, summary1, website1, date1):
        is_in_table = False
        information = f"SELECT * FROM bbc"
        self.c.execute(information)
        title = title1
        summary = summary1
        website = website1
        date = date1
        for row in self.c.fetchall():
            if row[1] == website:
                is_in_table = True
        if is_in_table == False:
            query = f"INSERT INTO bbc VALUES(?, ?, ?, ?)"
            values = (title, summary, website, date)
            self.c.execute(query, values)
            self.conn.commit()

    def news_appender_guardian(self, title2, summary2, website2, date2):
        is_in_table = False
        information = f"SELECT * FROM guardian"
        self.c.execute(information)
        title = title2
        summary = summary2
        website = website2
        date = date2
        for row in self.c.fetchall():
            if row[1] == website:
                is_in_table = True
        if is_in_table == False:
            query = f"INSERT INTO guardian VALUES(?, ?, ?, ?)"
            values = (title, summary, website, date)
            self.c.execute(query, values)
            self.conn.commit()

    def news_appender_nyt(self, title3, summary3, website3, date3):
        is_in_table = False
        information = f"SELECT * FROM nyt"
        self.c.execute(information)
        title = title3
        summary = summary3
        website = website3
        date = date3
        for row in self.c.fetchall():
            if row[1] == website:
                is_in_table = True
        if is_in_table == False:
            query = f"INSERT INTO nyt VALUES(?, ?, ?, ?)"
            values = (title, summary, website, date)
            self.c.execute(query, values)
            self.conn.commit()

CoronaScrape().bbc_scrape()
CoronaScrape().guardian_scrape()
CoronaScrape().nyt_scrape()