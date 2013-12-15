import ast
import re
import sys
import time
import urllib
import urllib2

from datetime import datetime
from bs4 import BeautifulSoup

# url = "http://www.indiegogo.com/projects?utf8=%E2%9C%93&filter_location=on&filter_country=CTRY_US&location_filter_submit=Search&filter_your=&filter_quick=&filter_category=Community"
# dataFile = "indiegogo_data.csv"

# Other helper functions, in alphabetical order
def cleanIndieGoGoURL(url):
    return url.split("&pg_num=")[0]

def cleanMoney(money):
    money = ''.join(money.split('.'))
    return ''.join(money.split(',')).strip('$').strip('USD').strip(' ').strip('EUR').strip('C$').strip('CA').strip('GBP')

def cleanPercentage(percentageString):
    return float(''.join(percentageString.split(',')).strip('%').strip(' '))

def calcTotal(percentageRaised, raisedSoFar):
    if percentageRaised == 0.0:
        total = "too big to calculate"
    else:
        total = int(float(raisedSoFar) / float(percentageRaised * 0.01))
    return total

def cleanFunders(fundersString):
    return fundersString.strip(" funders")

def cleanTimeLeft(timeLeftString):
    if timeLeftString == "?":
        timeLeftString = 0;
    return timeLeftString

def removeWhiteSpace(string):
    clean =  string.lstrip("\n\t\r ").rstrip("\n\t\r ")
    while "\n" in clean or "\t" in clean or "\r" in clean:
        clean = ''.join(clean.split("\n"))
        clean = ''.join(clean.split("\t"))
        clean = ''.join(clean.split("\r"))
    return clean 

def encodeUTFtoStr(text):
    return str(text.encode('ascii','ignore'))
    
def getRequestToSoup(url):
    opener = urllib2.build_opener()
    opener.addheaders = [('User-Agent', 'civic media ftw by rodrigodavies')]
    try:
        response = urllib2.urlopen(url)
        return BeautifulSoup(response.read())
    except AttributeError:
        raise Exception("Invalid URL: %s"%url)

def writeDataWithHeaders(dataString, file):
    f = open(file, 'a')
    f.write(dataString)
    f.close()

def getRequestToSoupIndiegogo(url):
    response = urllib2.urlopen(url)
    responseLines = response.readlines()
    responseString = ''
    for line in responseLines:
        if ("<!--" in line and not ("-->" in line)) or ("[endif]-->" in line):
            continue
        else:
            responseString += line
    return BeautifulSoup(responseString)

def scrapeIndieGoGo(url, dataFile, run):
    opener = urllib2.build_opener()
    opener.addheaders = [('User-Agent', 'civic media by rodrigodavies')]
    pageSoup = getRequestToSoupIndiegogo(url)
#    print pageSoup.prettify()
    lastPageNum = int(pageSoup.find(text="Next").parent.previous_element.previous_element)
    #print lastPageNum
    cleanURL = cleanIndieGoGoURL(url)
    dataString = ""
    for pageNum in range(1,lastPageNum+1):
        #print pageNum
        if pageNum > 10:
            continue
        nextPageString = "&pg_num=%s"%pageNum
        nextURL = "%s%s"%(cleanURL,nextPageString)
        #print nextURL
        thisSoup = getRequestToSoupIndiegogo(nextURL)
        # time.sleep(20)
        content = thisSoup.find(class_="badges clearfix")
        projects = content.find_all("li")
        for project in projects:
            # Project Name
            projectName = removeWhiteSpace(encodeUTFtoStr(project.find(class_="name").text))
            #print projectName
            # Summary
            projectDescription = removeWhiteSpace(encodeUTFtoStr(project.find(class_="description").text))
            # Project Location
            projectLocation = removeWhiteSpace(encodeUTFtoStr(project.find(id="project_location").text))
            raisedSoFarString = removeWhiteSpace(encodeUTFtoStr(project.find(id="project-stats-funding-amt").text))
            # Raised So Far
            raisedSoFar = int(cleanMoney(raisedSoFarString))
            # Percentage Raised
            percentageString = removeWhiteSpace(encodeUTFtoStr(project.find(id="project-stats-funding-pct").text))
            percentageRaised = float(cleanPercentage(percentageString))
            # Total Goal
            projectTotal = calcTotal(percentageRaised, raisedSoFar)
            # Funding Complete?
            timeLeftString = project.find(id="time_left_number").text
            timeLeft = int(cleanTimeLeft(timeLeftString))
            if timeLeft == 0:
                fundingComplete = True
            else:
                fundingComplete = False
            projectURLStub = project.find("a")["href"]
            loadURL = "%s%s"%("http://www.indiegogo.com", projectURLStub)
            projectSoup = getRequestToSoupIndiegogo(loadURL)
            # NEVER USE PROJECTSOUP?
            # Avg Pledge
            fundersString = project.find(id="funders").text
            numFunders = int(cleanFunders(removeWhiteSpace(fundersString)))
            if numFunders == 0:
                avgPledge = 0
            else: 
                avgPledge = float(raisedSoFar)/numFunders
            # Time (UTC)
            time = str(datetime.utcnow())
            #print time
            projectString = "%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n"%(projectName,
                                                            projectLocation,
                                                            projectTotal,
                                                            raisedSoFar,
                                                            percentageRaised,
                                                            numFunders,
                                                            avgPledge,
                                                            fundingComplete,
                                                            projectDescription,
                                                            time)
                                                            
            dataString = "%s%s"%(dataString, projectString)
    if run == 0:
        headerString = "Project Name\tProject Location\tTotal Goal\tRaised So Far\tPercentage Raised\t# Funders\tAvg Pledge\tFunding Complete?\tSummary\tTime (UTC)\n"
        dataString = "%s%s"%(headerString, dataString)
    writeDataWithHeaders(dataString, dataFile)

    
if __name__ == "__main__":
    time = str(datetime.utcnow())
    dataFile = "/mit/rodrigod/crowdfunding/indiegogo/indiegogo_data_%s.csv"%time        
    for i in range(2):
        if i == 0:
            url = "http://www.indiegogo.com/projects?utf8=%E2%9C%93&filter_location=on&filter_country=CTRY_US&location_filter_submit=Search&filter_your=&filter_quick=&filter_category=Community"
        else:
            url = "http://www.indiegogo.com/projects?utf8=%E2%9C%93&filter_location=on&filter_country=CTRY_GB&location_filter_submit=Search&filter_your=&filter_quick=&filter_category=Community"
        scrapeIndieGoGo(url, dataFile, i)

