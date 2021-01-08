import string
import csv
from ckonlpy.tag import Twitter
twitter = Twitter()
f = open("Han.txt", mode = "r", encoding = "utf-8")
c = csv.writer(open("HanKeoRyeKonlPy.csv","w",encoding = "utf-8"))
for t in f:
    c.writerow(twitter.morphs(t))
    