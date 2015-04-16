import bs4
from pandas import DataFrame
import requests

def getDOM(url, parser):
    resp = requests.get(url)
    return bs4.BeautifulSoup(resp.text, parser)
def getInningsSummary():
    pass
def getBattingScore(matchDOM, innings, matchNum):
    battingTables = matchDOM.select('table.batting-table')
    battingLine = []
    country = battingTables[innings - 1].select('th.th-innings-heading')[0].text.split('innings')[0].strip()
    for element in battingTables[innings - 1].select('tr td.batsman-name'):
        row = [matchNum, country, element.get_text().strip()]
        for i in range(7):
            element = element.next_sibling.next_sibling
            if element == None:
                row += [element]
            else:
                row += [element.get_text().strip()]
        battingLine.append(row)
    return battingLine
def getBowlingScore(matchDOM, innings, country, matchNum):
    bowlingTables = matchDOM.select('table.bowling-table')
    bowlingLine = []
    for element in bowlingTables[innings - 1].select('tr td.bowler-name'):
        row = [matchNum, country, element.get_text().strip()]
        for i in range(9):
            element = element.next_sibling.next_sibling
            if element == None:
                row += [element]
            else:
                row += [element.get_text()]
        bowlingLine.append(row)        
    return bowlingLine

espnHomeURL = 'http://www.espncricinfo.com'
wcResultsURL = '/icc-cricket-world-cup-2015/engine/series/509587.html'
wcResultsDOM = getDOM(espnHomeURL + wcResultsURL, "html.parser")
#inningsSummary = matchResultsDOM.select('div.brief-summary div')
#matchResult = inningsSummary[3].get_text()
#matchDate = inningsSummary[7].get_text().strip().split('(')[0]
matchLinks = [link['href'] for link in wcResultsDOM.select('div[class~="news-list"] div[class~="content_data"] a[class~="potMatchLink"]')]
batting = []
bowling = []
for index, matchLink in enumerate(matchLinks):
    if index != 10:
        print index
        matchResultsDOM = getDOM(espnHomeURL + matchLink, "lxml")
        battingScore1 = getBattingScore(matchResultsDOM, 1, index + 1)
        battingScore2 = getBattingScore(matchResultsDOM, 2, index + 1)
        bowlingScore1 = getBowlingScore(matchResultsDOM, 1, battingScore2[0][1], index + 1)
        bowlingScore2 = getBowlingScore(matchResultsDOM, 2, battingScore1[0][1], index + 1)
        batting += battingScore1 + battingScore2
        bowling += bowlingScore1 + bowlingScore2

battingDF = DataFrame(batting, columns = ['MatchNum', 'Country', 'Batsman','Dismissal-Info','R','M','B','4s','6s', 'SR'])
bowlingDF = DataFrame(bowling, columns = ['MatchNum', 'Country','Bowler','O','M','R','W','Econ','0s','4s','6s','Extra'])
battingDF.to_csv('I:\\WebScraping\\CricketWorldCup2015\\batting.csv', encoding = 'utf-8')
bowlingDF.to_csv('I:\\WebScraping\\CricketWorldCup2015\\bowling.csv', encoding = 'utf-8')
    
