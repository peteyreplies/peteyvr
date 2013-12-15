import sys
import urllib
import urllib2

from bs4 import BeautifulSoup
from datetime import datetime

# Custom BeautifulSoup methods for find_all
def get_num_backers(tag):
    return tag.name == "data" and tag.has_key("itemprop") and tag["itemprop"] == "Project[backers_count]"

def get_page_numbers(tag):
    return tag.name == "a" and not tag.has_key("class")

def get_project_name(tag):
    return tag.name == "a" and tag["target"] == "" and len(tag.text) > 0

def get_total_goal(tag):
    return tag.name == "h5" and "pledged of" in tag.text

# Other helper functions, in alphabetical order
def cleanDescription(text):
    return ''.join(text.strip("\n").split("\n"))

def cleanKickstarterURL(url):
    return url.split('#',1)[0]

def cleanMoneyComma(money):
    return ''.join(money.split(','))

def cleanMoneyDecimal(money):
    return money.split('.')[0]

def cleanMoneyEnds(money):
    return money.strip('\n').strip('$')

def cleanMoneyNewlines(money):
    return money.split('\n')[0]

def cleanMoney(money):
    return cleanMoneyDecimal(cleanMoneyComma(cleanMoneyNewlines(cleanMoneyEnds(money))))

def cleanNumber(number):
    return ''.join(number.split(','))

def encodeUTFtoStr(text):
    return str(text.encode('ascii','ignore'))

def getLastPageNum(soup):
    relevantHTML = soup.find("div","pagination")
    countTags = relevantHTML.find_all(get_page_numbers)
    return int(encodeUTFtoStr(countTags[len(countTags)-1].text))
    
def getRequestToSoup(url):
    opener = urllib2.build_opener()
    opener.addheaders = [('User-Agent', 'civic media ftw by /u/rileybmit')]
    try:
        response = urllib2.urlopen(url)
        return BeautifulSoup(response.read())
    except AttributeError:
        raise Exception("Invalid URL: %s"%url)

def writeDataWithHeaders(dataString, file):
    headerString = "Project Name\tProject Location\tTotal Goal\tRaised So Far\tPercentage Raised\t# Funders\tAvg Pledge\tFunding Complete?\tSummary\tTime (UTC)\n"
    totalString = "%s%s"%(headerString, dataString)
    f = open(file, 'w')
    f.write(totalString)
    f.close()

def scrapeKickstarter(url):
    cleanURL = cleanKickstarterURL(url)
    soup = getRequestToSoup(cleanURL)
    lastPageNum = getLastPageNum(soup)
    dataString = ""
    for pageNdx in range(1,lastPageNum+1):
        #print pageNdx
        nextPageString = "?page=%s"%pageNdx
        nextURL = "%s%s"%(cleanURL,nextPageString)
        thisSoup = getRequestToSoup(nextURL)
        projectsList = thisSoup.find_all(class_ = "project-card")
        for ndx, project in enumerate(projectsList):
            # Project Name
            projectName = encodeUTFtoStr(project.find(get_project_name).text)
            #print projectName
            # Project Description
            summary = encodeUTFtoStr(cleanDescription(project.find("p", class_ = "bbcard_blurb").text))
            # Project Location
            projectLocation = encodeUTFtoStr(project.find("span", class_ = "location-name").text)
            # Raised So Far
            raisedSoFarString = encodeUTFtoStr(project.find("li", class_ = "pledged").text)
            raisedSoFar = int(cleanMoney(raisedSoFarString))
            projectString =  encodeUTFtoStr(project.find("li", class_ = "first funded").text)
            fundingCompleteHTML = project.find("div", class_ = "project-pledged-successful")
            # Funding Complete?
            if fundingCompleteHTML.has_key("style") and fundingCompleteHTML["style"] == "display: none;":
                fundingComplete = False
            else:
                fundingComplete = True
            projectURLStub = project.find("a")["href"]
            loadURL = "%s%s"%("http://www.kickstarter.com", projectURLStub)
            projectSoup = getRequestToSoup(loadURL)
            # Total Goal
            totalGoalString = encodeUTFtoStr(projectSoup.find_all(get_total_goal)[0].text)
            strList = totalGoalString.split(" ")
            totalGoal = int(cleanMoneyEnds(cleanMoneyComma(strList[len(strList)-2])))
#            print totalGoal
            # Percentage Raised
            percentageRaised = float(raisedSoFar)/float(totalGoal)
            # # Funders
            numFunders = int(cleanNumber(encodeUTFtoStr(projectSoup.find(get_num_backers).text)))
            #print numFunders
            # Avg Pledge
            if numFunders == 0:
                avgPledge = 0
            else:
                avgPledge = float(raisedSoFar)/numFunders
            time = str(datetime.utcnow())
            projectString = "%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n"%(projectName,
                                                            projectLocation,
                                                            totalGoal,
                                                            raisedSoFar,
                                                            percentageRaised,
                                                            numFunders,
                                                            avgPledge,
                                                            fundingComplete,
                                                            summary,
                                                            time)
                                                            
            dataString = "%s%s"%(dataString, projectString)
    data_file = "/mit/rodrigod/crowdfunding/kickstarter/kickstarter_data_%s.csv"%time        
    writeDataWithHeaders(dataString, data_file)


# URL should be "http://www.kickstarter.com/discover/tags/civic"
if __name__ == "__main__":
#    url = sys.argv[1]
    url = "http://www.kickstarter.com/discover/tags/civic"
    scrapeKickstarter(url)

