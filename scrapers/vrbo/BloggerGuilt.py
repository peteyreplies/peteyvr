#scrapes the last 100 blog posts from mitadmissions & computes blogger stats 

from bs4 import BeautifulSoup
from collections import Counter
from pprint import pprint
import os
import csv
import string
import urllib
import urllib2

# Open the last 100 blog entries. gross but works. 
doc = urllib2.urlopen('http://mitadmissions.org/blogs')
doc2 = urllib2.urlopen('http://mitadmissions.org/blogs/P20')
doc3 = urllib2.urlopen('http://mitadmissions.org/blogs/P40')
doc4 = urllib2.urlopen('http://mitadmissions.org/blogs/P60')
doc5 = urllib2.urlopen('http://mitadmissions.org/blogs/P80')

html = doc.read() + doc2.read() + doc3.read() + doc4.read() + doc5.read()
soup = BeautifulSoup(html)

#get blogger names 
names = []
nameSoup = soup.find_all("p", "byline")
for name in nameSoup: 
	thisName = name.string
	fixedName = thisName.encode('ascii', 'ignore')
	names.append(str(fixedName))

#get blog title
titles = []
titleSoup = soup.find_all("h3")
for title in titleSoup:
	thisTitle = title.string
	fixedTitle = thisTitle.encode('ascii', 'ignore')
	titles.append(str(fixedTitle))

#get blog link 
links = []
linkSoup = soup.find_all("h3")
for link in linkSoup:
	thisLink = link.a['href']
	fixedLink = str(thisLink)
	links.append(fixedLink)

#get blog dates
dates = []
dateSoup = soup.find_all("p", "meta")
for date in dateSoup:
	thisDate = str(date.contents[0])
	fixedDate = thisDate[:-3]
	dates.append(fixedDate)

#create a list of dicts containing blog info 
entries = [] 
e = 0 
for d in dates:
	entry = {
	'date': dates[e],
	'author': names[e],
	'title': titles[e],
	'url': links[e],
	}
	entries.append(entry)
	e = e + 1 

#count blogs by blogger and print to terminal
print "DISTRIBUTION BY TOTAL"
pprint(Counter(names).most_common())

#count blog by most recent blog date and print to terminal
print "DISTRIBUTION BY TIME"
mostRecent = []
for i in entries:
	if i["author"] not in mostRecent:
		print i["author"] + "\t \t" + i["date"]
		mostRecent.append(i["author"])

print "THE LAST 100 BLOGS"
print "(ordered by recency, then number)"

#write to csv and save to directory 
keys = ['date', 'author', 'title', 'url']
f = open ('BloggerGuilt.csv','wb')
DW = csv.DictWriter(f,keys)
DW.writer.writerow(keys)
DW.writerows(entries)













