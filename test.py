from re import search
import sqlite3

conn = sqlite3.connect("bot.db")
c = conn.cursor()
reminder = {"reminder": "god is dog"}
r = "lake"
print(r, type(r))
c.execute("DELETE FROM reminder WHERE reminder = ?", (r, ))
conn.commit()
    
