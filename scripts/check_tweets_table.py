import sqlite3

con = sqlite3.connect("../twitter_bot.db")
cur = con.cursor()
res = cur.execute("SELECT * FROM tweets")
print(res.fetchall())
con.close()