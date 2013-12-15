import sys
import ast
import re
import time
import urllib
import urllib2

from datetime import datetime
from bs4 import BeautifulSoup

#url = "http://ioby.org/projects?phrase=&city=&province=&status=1&vols=All&sort_by=title&sort_order=ASC&items_per_page=All"
#dataFile = "ioby_data.csv"

HEADER_STRING = "Project Name\tProject Location\tTotal Goal\tRaised So Far\tPercentage Raised\t# Funders\tAvg Pledge\tFunding Complete?\tSummary\tTime (UTC)\tURL"
INACTIVE_TIMEOUT = 50
LATEST_OFFSET_HOURS = 5
MISSING_TIMEOUT = 5

# Beautiful Soup and output methods

def getRequestToSoup(url):
    opener = urllib2.build_opener()
    opener.addheaders = [('User-Agent', 'civic media by rodrigodavies')]
    try:
        response = urllib2.urlopen(url)
        return BeautifulSoup(response.read())
    except AttributeError:
        raise Exception("Invalid URL: %s"%url)

def encodeUTFtoStr(text):
    return str(text.encode('ascii','ignore'))

def writeData(dataString, dataFile):
    f = open(dataFile,'w')
    f.write(dataString)
    f.close()

# Finding and cleaning project data

def findProjects (tag):
    return tag.name == "article" and tag.has_key("id") and not ("block-block" in tag["id"])

def removeWhiteSpace(string):
    clean =  string.lstrip("\n\t\r ").rstrip("\n\t\r ")
    while "\n" in clean or "\t" in clean or "\r" in clean:
        clean = ''.join(clean.split("\n"))
        clean = ''.join(clean.split("\t"))
        clean = ''.join(clean.split("\r"))
    return clean 
    
def cleanMoney(money):
    money = ''.join(money.split('.'))
    return ''.join(money.split(',')).strip('$').strip('USD').strip(' ').strip('EUR').strip('C$').strip('CA').strip('GBP')

def getLocation(soup):
    locationSoup = soup.find(text="Location").parent.next_element.next_element.next_element
    nbrhood = locationSoup.find("span")
    if nbrhood is None:
        nbrhood = ""
    else:
        nbrhood = encodeUTFtoStr(nbrhood.text)
    zipLine = encodeUTFtoStr(locationSoup.text).split('(')
    if len(zipLine) > 1:
        zip = zipLine[1].rstrip("\n\t\r) ")
    else:
        zip = zipLine[0].rstrip("\n\t\r) ")
    return nbrhood, zip
        
def getLocationString(street, nbrhood, zip):
    street = removeWhiteSpace(encodeUTFtoStr(street))
    nbrhood = removeWhiteSpace(encodeUTFtoStr(nbrhood))
    zip = removeWhiteSpace(encodeUTFtoStr(zip))
    nyCheckStr = encodeUTFtoStr(zip[0:2])
    if nyCheckStr == "10" or nyCheckStr == "11":
        city = "New York, NY, "
    else:
        city = ""
    if len(encodeUTFtoStr(zip)) > 0:
        if encodeUTFtoStr(zip[0]) not in "0123456789":
            zip = ""
    if street != "":
        street += ", "
    if nbrhood != "" and zip != "":
        nbrhood += ", "
    return "%s%s%s%s"%(street, nbrhood, city, zip)

def getStreet(project_page):
    project_street = project_page.find(class_="street-only")
    if project_street == None: 
        project_street = project_page.find(class_="field field-name-field-project-neighborhood field-type-text field-label-hidden")
        if project_street == None:
            project_street = ""
        else:
            project_street = encodeUTFtoStr(project_street.text).lstrip("( ").rstrip(") ")
    else:
        project_street = encodeUTFtoStr(project_street.text)
    return project_street

def calcFunders(project_page):
    funders = project_page.find(id="contributors")
    names = funders.find_all('li')
    numFunders = len(str(names).split('</li>')) - 1
    return numFunders

def getSummary(project):
    project_summary = project.find(class_="field field-name-field-project-inbrief field-type-text-long field-label-hidden")
    if project_summary == None:
        project_summary = project.find(class_ = "field field-name-body field-type-text-with-summary field-label-hidden")
        if project_summary == None: 
            project_summary = ""
        else:
            project_summary = encodeUTFtoStr(project_summary.text)
    else:
        project_summary = encodeUTFtoStr(project_summary.text)
    print removeWhiteSpace(project_summary)
    return removeWhiteSpace(project_summary)

def getProjects(url):
    opener = urllib2.build_opener()
    opener.addheaders = [('User-Agent', 'civic media by rodrigodavies')]
    nextURL = url
    dataString = HEADER_STRING + "\n"


    try: 
        pageSoup = getRequestToSoup(nextURL)
#        time.sleep(35)
        projects = pageSoup.find_all(findProjects)
        for project in projects:
            project_data = [] # initialize list of project data
            url = project.find("a")["href"] # search for first link, index in to href and return relative URL
            # URL
            project_url = "http://ioby.org" + url # insert base url
            # Project Name
            project_title = removeWhiteSpace(encodeUTFtoStr(project.find("h3").text)) # find plain text assoc. with h3 tags
            print project_title
            # Summary
            project_summary = getSummary(project) # the only p tags used are for summaries (double-check this)
            # Total Goal
            project_total_string = project.find(text="Total Needed").parent.next_element.next_element.next_element.text
            project_total = float(cleanMoney(project_total_string))
            # Raised So Far
            project_raised_string = project.find(text="Raised").parent.next_element.next_element.next_element.text
            project_raised = float(cleanMoney(project_raised_string))   
            # Project Location
            project_nbrhood, project_zip = getLocation(project)
            response = urllib2.urlopen(project_url) # open the individual project page
            project_page = BeautifulSoup(response.read())
            project_street = getStreet(project_page) # check the street address
            project_location = getLocationString(project_street, project_nbrhood, project_zip)
            num_funders = calcFunders(project_page)
            if num_funders == 0:
                avgPledge = 0
            else:
                avgPledge = float(project_raised)/num_funders
            percentage_raised = float(project_raised)/project_total
            fundingComplete = False
            latestTime = str(datetime.utcnow())
            projectString = "%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n"%(
                                                    project_title,
                                                    project_location,
                                                    project_total,
                                                    project_raised,
                                                    percentage_raised,
                                                    num_funders,
                                                    avgPledge,
                                                    fundingComplete,
                                                    project_summary,
                                                    latestTime,
                                                    project_url)
            projectString = encodeUTFtoStr(projectString)
            dataString = "%s%s"%(dataString, projectString)
        dataFile = "/mit/rodrigod/crowdfunding/ioby/ioby_data_%s.csv"%latestTime
        writeData(dataString, dataFile)

    except urllib2.HTTPError:
        pass
    

if __name__ == '__main__':
    url = "http://ioby.org/projects?phrase=&city=&province=&status=1&vols=All&sort_by=title&sort_order=ASC&items_per_page=All"
    # url = sys.argv[1]
    getProjects(url)
