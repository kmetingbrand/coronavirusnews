from bs4 import BeautifulSoup as bs
from datetime import datetime
from matplotlib import pyplot as plt
import requests
import sqlite3
import json

class CoronaNewsScrape():
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
            title1 = article.title.text.replace("'","\\")
            summary1 = article.description.text.replace("'","\\")
            website1 = article.guid.text.replace("'","\\")
            date1 = article.pubDate.text.replace("'","\\")
            if "corona" in summary1 or "corona" in title1 or "virus" in summary1 or "virus" in title1:
                self.news_appender_bbc(title1, summary1, website1, date1)

    def guardian_scrape(self):
        self.source2 = requests.get("https://www.theguardian.com/world/rss").text

        self.soup2 = bs(self.source2, 'xml')

        for article2 in self.soup2.find_all('item'):
            title2 = article2.title.text.replace("'","\\")
            summary2 = article2.description.text.replace("'","\\")
            website2 = article2.link.text.replace("'","\\")
            date2 = article2.pubDate.text.replace("'","\\")
            if "corona" in summary2 or "corona" in title2 or "virus" in summary2 or "virus" in title2:
                self.news_appender_guardian(title2, summary2, website2, date2)

    def nyt_scrape(self):
        self.source3 = requests.get("https://rss.nytimes.com/services/xml/rss/nyt/Europe.xml").text

        self.soup3 = bs(self.source3, 'xml')
        
        for article3 in self.soup3.find_all('item'):
            title3 = article3.title.text.replace("'","\\")
            summary3 = article3.description.text.replace("'","\\")
            website3 = article3.link.text.replace("'","\\")
            date3 = article3.pubDate.text.replace("'","\\")
            
            if "corona" in summary3 or "corona" in title3 or "virus" in summary3 or "virus" in title3:
                self.news_appender_nyt(title3, summary3, website3, date3)
    
    def news_appender_bbc(self, title1, summary1, website1, date1):
        query = f"SELECT * FROM bbc WHERE title = '{title1}'"
        self.c.execute(query)
        result = self.c.fetchone()
        if not result:
            query = f"INSERT INTO bbc VALUES(?, ?, ?, ?)"
            values = (title1, summary1, website1, date1)
            self.c.execute(query, values)
            self.conn.commit()

    def news_appender_guardian(self, title2, summary2, website2, date2):
        query = f"SELECT * FROM guardian WHERE title = '{title2}'"
        self.c.execute(query)
        result = self.c.fetchone()
        if not result:
            query = f"INSERT INTO guardian VALUES(?, ?, ?, ?)"
            values = (title2, summary2, website2, date2)
            self.c.execute(query, values)
            self.conn.commit()

    def news_appender_nyt(self, title3, summary3, website3, date3):
        query = f"SELECT * FROM nyt WHERE title = '{title3}'"
        self.c.execute(query)
        result = self.c.fetchone()
        if not result:
            query = f"INSERT INTO nyt VALUES(?, ?, ?, ?)"
            values = (title3, summary3, website3, date3)
            self.c.execute(query, values)
            self.conn.commit()

class CoronaDataScrape():
    def __init__(self):
        self.conn = sqlite3.connect("db/data.db")
        self.c = self.conn.cursor()

        query = "SELECT count(name) FROM sqlite_master WHERE type='table' AND name='countrydata'"
        self.c.execute(query)
        if not self.c.fetchone()[0] == 1:
            self.__createtables()
    
    def __createtables(self):
        self.c.execute("""CREATE TABLE countrydata (
                        country text,
                        total_deaths integer,
                        total_cases integer,
                        date text
                        )""")

        self.c.execute("""CREATE TABLE regiondata (
                        region text,
                        total_deaths integer,
                        total_cases integer,
                        date text
                        )""")
        
        self.c.execute("""CREATE TABLE changetrack (
                        region text,
                        total_deaths integer,
                        total_cases integer,
                        date text
                        )""")
        
        self.conn.commit()
    
    def country_data_scrape(self):
        data_url = "https://mattblackworld.com/api/totals"
        
        req = requests.get(data_url)
        result = json.loads(req.text)
    
        for r in result:
            country = r['country']
            total_deaths = r['total_deaths']
            total_cases = r['total_cases']
            date = datetime.date(datetime.now())
        
            self.country_data_appender(country, total_deaths, total_cases, date)
    
    def country_data_appender(self, country, total_deaths, total_cases, date):
        query = f"SELECT * FROM countrydata WHERE country = '{country}' AND date = '{date}'"
        self.c.execute(query)
        result = self.c.fetchone()
        if not result:
            query = f"INSERT INTO countrydata VALUES(?, ?, ?, ?)"
            values = (country, total_deaths, total_cases, date)
            self.c.execute(query, values)
            self.conn.commit()

    def region_data_scrape(self):
        data_url = "https://mattblackworld.com/api/regions"

        req = requests.get(data_url)
        result = json.loads(req.text)

        for r in result:
            region = r['region']
            total_deaths = r['total_deaths']
            total_cases = r['total_cases']
            date = r['date']

            self.region_data_appender(region, total_deaths, total_cases, date)

    def region_data_appender(self, region, total_deaths, total_cases, date):
        query = f"SELECT * FROM regiondata WHERE region = '{region}' AND date = '{date}'"
        self.c.execute(query)
        result = self.c.fetchone()
        if not result:
            query = f"INSERT INTO regiondata VALUES (?, ?, ?, ?)"
            values = (region, total_deaths, total_cases, date)
            self.c.execute(query, values)
            self.conn.commit()

    def totalr_data_scrape(self):
        data_url = "https://mattblackworld.com/api/regions/totals"

        req = requests.get(data_url)
        result = json.loads(req.text)

        for r in result:
            region = r['region']
            total_deaths = r['total_deaths']
            total_cases = r['total_cases']
            date = datetime.date(datetime.now())

            self.totalr_data_appender(region, total_deaths, total_cases, date)
        
    def totalr_data_appender(self, region, total_deaths, total_cases, date):
        query = f"SELECT * FROM changetrack WHERE region = '{region}'AND date = '{date}'"
        self.c.execute(query)
        result = self.c.fetchone()
        if not result:
            query = f"INSERT INTO changetrack VALUES(?, ?, ?, ?)"
            values = (region, total_deaths, total_cases, date)
            self.c.execute(query, values)
            self.conn.commit()

class StatisticalPlotting:
    def __init__(self):
        self.conn = sqlite3.connect("db/data.db")
        self.c = self.conn.cursor()
    
    def total_death(self):
        query = f"SELECT total_deaths, date FROM changetrack"
        self.c.execute(query)

        data = []
        xTickMarks = []

        for row in self.c.fetchall():
            data.append(int(row[1]))
            xTickMarks.append(str(row[0]))

            self.total_death_plot(data)

CoronaDataScrape().region_data_scrape()
CoronaDataScrape().country_data_scrape()
CoronaDataScrape().totalr_data_scrape()
CoronaNewsScrape().bbc_scrape()
CoronaNewsScrape().guardian_scrape()
CoronaNewsScrape().nyt_scrape()