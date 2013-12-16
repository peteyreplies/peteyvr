##scrapes listings from VRBO & exports data to spreadsheet 
##by petey@mit.edu

##import some libraries which will probably be useful
from bs4 import BeautifulSoup
from collections import Counter
from pprint import pprint
import os
import csv
import string
import urllib
import urllib2
import sys
import ast
import re
import time

##fetch ALL THE LISTINGS and load into a huge soup 
#set some baseline parameters
baseURL = "http://vrbo.com"
resultsURL = "/vacation-rentals/usa/florida/south-west/cape-coral?page="
i = 1
html = ""

#loop through & download the first 10 pages of listings 
while i <= 10:
	doc = urllib2.urlopen(baseURL + resultsURL + str(i))
	html = html + doc.read()
	i = i + 1

#load to soup 
soup = BeautifulSoup(html)

##walk the tree & store 
#create a list of properties 
properties = []

#search the soup for each list item by some class text which appears in each 
for listing in soup.find_all("li","altlisting"): 
	#ok, so this gets weird, but we're going to pull all of the things we need by trial and error
	#first, from out of the <li> itself 
	listingID = str(listing['id']) #this is the id of the listing, which seems random? 
	listingURL = str(listing['data-listingurl']) #this is the URL of the listing, v. important!
	
	#find the rate & duration info 
	rate = soup.find("div", "rate-summary")
	listingDuration = str(rate['data-duration'])
	listingMinStay = str(rate['data-minstay'])
	listingRate = str(rate['data-rate'])

	#find the accommodations info 
	room = soup.find("span","altlisting-center")
	bedsRaw = str((room['data-beds']))
	listingBeds = int(re.findall(r'[0-9]+', bedsRaw)[0])
	bathsRaw = str((room['data-baths']))
	listingBaths = int(re.findall(r'[0-9]+', bathsRaw)[0])
	sleepsRaw = str((room['data-sleeps']))
	listingSleeps = int(re.findall(r'[0-9]+', sleepsRaw)[0])
	listingTitle = str(room.a.text)
	
	#find the region listing info 
	region = soup.find("span","altlisting-region")
	listingRegion = str(region.a.text)
	
	#walk into the icons div and assess as booleans
	handicappedAccessible = False
	petFriendly = False
	bookOnline = False
	onMap = False 
	ownerOperated = False
	icons in soup.find("div","altlisting-icons")
	if 'book online' in str(icons.find("span","altlisting-icon-bookable")['title']):
		bookOnline = True
	if 'not' in str(icons.find("span","altlisting-icon-handicap")['title']):
		handicappedAccessible = False
	if 'friendly' in str(icons.find("span","altlisting-icon-pet")['title']):
		petFriendly = True
	if 'has' in str(icons.find("span","altlisting-icon-marker")['title']):
		onMap = True
	if 'owner' in str(icons.find('span','altlisting-icon-owner')['class']):
		ownerOperated = True
	starsRaw = str(icons.find('span','altlisting-icon-reviews')['class'][1]) 
	starsString = re.findall(r'[0-9]+', starsRaw)[0]
	if len(starsString) > 1:
		listingStars = float(starsString[0] + '.' + starsString[-1])
	else:
		listingStars = int(starsString)
	listingReviews = int(str(icons.find('span','altlisting-icon-reviews').text))

	thisListing = {
				'ID': listingID,
				'Title': listingTitle,
				'URL': listingURL,
				'Booking Duration': listingDuration,
				'Minimum Stay': listingMinStay,
				'Rate Range': listingRate,
				'Beds': listingBeds,
				'Baths': listingBaths,
				'Sleeps': listingSleeps,
				'Region': listingRegion,
				'Accessible?': handicappedAccessible,
				'Pets?': petFriendly,
				'Book Online?': bookOnline,
				'Map Marker?': onMap,
				'Owner Operated?': ownerOperated,
				'# of Stars': listingStars,
				'# of Reviews': listingReviews,
				}
	properties.append(thisListing)

print 'CHECK OUT SPORTS'
pprint(properties)



