import sqlite3

conn = sqlite3.connect('scraped_news.db')

c = conn.cursor()

c.execute("""CREATE TABLE BBC (
            date text,
            title text,
            summary text,
            link text
            )""")

c.execute("""CREATE TABLE Guardian (
            date text,
            title text,
            summary text,
            website text
            )""")

c.execute("""CREATE TABLE NYT (
            date text,
            title text,
            summary text,
            website text
            )""")

conn.commit()

conn.close()