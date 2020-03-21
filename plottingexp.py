from matplotlib import pyplot as plt
import sqlite3

conn = sqlite3.connect("db/data.db")
c = conn.cursor()

region = input("Region: ")

query = f"SELECT total_deaths, date FROM regiondata WHERE region='{region}'"
result = c.execute(query)

x = data = []
y = dates = []


for row in c.fetchall():
    data.append(str(row[1]))
    dates.append(int(row[0]))


plt.plot(x, y)
plt.title(f"{region} death toll changes")
plt.ylabel("Death toll")
plt.xlabel("Date")
plt.xticks(rotation=90)
plt.legend(f"{region}")
plt.show()