import sqlite3
import csv

conn = sqlite3.connect('champsnew.db')
conn.text_factory = str
c = conn.cursor()

f = open("ChampionSelect-AllItems.csv","rb")
allcsv = csv.DictReader(f)

for eachLine in allcsv:
	a = eachLine['Name']
	b = eachLine['CounteredBy']
	cmd = "INSERT INTO HeroCounters(name, countered_by_name) VALUES (?,?)"
	c.execute(cmd,(a,b))
	
conn.commit()
conn.close()