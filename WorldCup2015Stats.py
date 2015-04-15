from bs4 import BeautifulSoup
from pandas import DataFrame
import requests

def getDOM(url):
    resp = requests.get(url)
    return BeautifulSoup(resp.text)

def getDOMParser(url):
    resp = requests.get(url)
    return BeautifulSoup(resp.text,"html.parser")
    
def getBatsmenInfo(battingTable):
    batsmenList = []
    batsmenList.append([batsman.get_text() for batsman in battingTable.select('tr td[class="batsman-name"]')])
    info = [info.get_text() for info in battingTable.select('tr td + td + td + td')]
    batsmenList.append(info[0::6][:-2])
    batsmenList.append(info[2::6][:-1])
    batsmenList.append(info[3::6][:-1])
    batsmenList.append(info[4::6][:-1])
    return batsmenList

def getMatchBattingStats(matchDOM):
    result = matchDOM.select('.innings-requirement')[0].get_text()
    date = " ".join(matchDOM.select('.match-information div:nth-of-type(3)')[0].get_text().split()[:3])
    battingTables = matchDOM.select('table[class~="batting-table"]')
    team1 = battingTables[0].select('.tr-heading .th-innings-heading')[0].get_text().split('innings')[0]
    team2 = battingTables[1].select('.tr-heading .th-innings-heading')[0].get_text().split('innings')[0]
    matchDict = {"team1" : team1, "team2" : team2, "batting1" : getBatsmenInfo(battingTables[0]), "batting2" : getBatsmenInfo(battingTables[1]), 'Result' : result, 'Date' : date}
    return matchDict

def renderBatting(batting):
    for i in range(len(batting[0])):
        print "%s Runs : %s Balls : %s Fours : %s Sixes : %s"%(batting[0][i],batting[1][i],batting[2][i],batting[3][i],batting[4][i])
def getLine():
    return "-----------------------------------"    
        
def getBowlerInfo(bowlingTable):
    bowlerList = []
    bowlerList.append([bowler.get_text() for bowler in bowlingTable.select('tr td[class="bowler-name"]')])
    bowlerList.append([info.get_text() for info in bowlingTable.select('tr td[class="bowler-name"] + td')])
    bowlerList.append([info.get_text() for info in bowlingTable.select('tr td[class="bowler-name"] + td + td + td')])
    bowlerList.append([info.get_text() for info in bowlingTable.select('tr td[class="bowler-name"] + td + td + td + td')])
    return bowlerList

def renderBowling(bowling):
    for i in range(len(bowling[0])):
        print "%s Overs : %s Runs Given : %s Wickets Taken : %s"%(bowling[0][i],bowling[1][i],bowling[2][i],bowling[3][i])

def getMatchBowlingStats(matchDOM, matchDict):
    bowlingTables = matchDOM.select("table.bowling-table")  
    matchDict["bowling1"] = (getBowlerInfo(bowlingTables[0]))
    matchDict["bowling2"] = (getBowlerInfo(bowlingTables[1]))
    return matchDict

def render(matchInfo):
    print getLine()
    print "Date : %s" %matchInfo["Date"]
    print getLine()
    print "Result : %s" %matchInfo["Result"]
    print matchInfo["team1"]
    print "Batting STATS"
    print getLine()
    renderBatting(matchInfo["batting1"])
    print getLine()
    print "Bowling STATS"
    renderBowling(matchInfo["bowling2"])
    print getLine()
    print matchInfo["team2"] 
    print getLine() 
    print "Batting Stats"
    renderBatting(matchInfo["batting2"])
    print getLine()
    print "Bowling STATS"
    renderBowling(matchInfo["bowling1"])
    
      

espnHomeURL = 'http://www.espncricinfo.com'
wcResultsURL = '/icc-cricket-world-cup-2015/engine/series/509587.html'
wcResultsDOM = getDOMParser(espnHomeURL + wcResultsURL)

matchLinks = [link['href'] for link in wcResultsDOM.select('div[class~="news-list"] div[class~="content_data"] a[class~="potMatchLink"]')]

matchesInfo = {}

for index, matchLink in enumerate(matchLinks):
    if index != 10:
        matchURL = espnHomeURL + matchLink
        print "loading match %d ........."%(index + 1)
        matchDOM= getDOM(matchURL)
        matchesInfo[index + 1] = getMatchBowlingStats(matchDOM,getMatchBattingStats(matchDOM))
    else:
        matchesInfo[index + 1] = "Australia V Bangladesh Match Cancelled Due to Rain!!!"

df = DataFrame(matchesInfo)
print df    
matchNum = int(raw_input("Enter Match Number to see the stats : "))

while matchNum != 0:
    if matchNum != 11:
        render(matchesInfo[matchNum])
    else:
        print matchesInfo[11]
    matchNum = int(raw_input("Enter Match Number to see the stats press 0 to exit : "))



