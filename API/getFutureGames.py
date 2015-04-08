__author__ = 'Kang'
from getScores import getTeam
import pandas as pd
import requests
import string
from bs4 import BeautifulSoup
from datetime import datetime, date

def getFutureGames():
    teams = getTeam()
    print teams
    dates = []
    home_team = []
    visit_team = []

    for index,team in teams.iterrows():
        baseURL = 'http://espn.go.com/nba/team/schedule/_/name/{0}'
        print str(baseURL.format(team['Prefix']))
        scoreHTML = requests.get(baseURL.format(team['Prefix']))
        scoreTable = BeautifulSoup(scoreHTML.text).table
        _team = team['Teams']

        for row in scoreTable.find_all('tr'):
            try:
                columns = row.find_all('td')
                _home = True if columns[1].li.text == 'vs' else False
                _other_team = columns[1].find_all('a')[1]['href'].split('/')[-1]
                _other_team = string.replace(str(_other_team),'-',' ').lower()
                d = datetime.strptime(columns[0].text,'%a, %b %d')
                d = d.date()
                if d.month<8:
                    d = d.replace(2015)
                else:
                    d = d.replace(2014)
                if d >= date.today():
                    dates.append(d)
                    home_team.append(_team if _home else _other_team)
                    visit_team.append(_team if not _home else _other_team)
            except (ValueError, IndexError, AttributeError):
                pass
    dict = {'Date': dates, 'Home Team': home_team, 'Visit Team':visit_team}
    global futureGames
    futureGames = pd.DataFrame(dict)
    print futureGames

def save_output():
    print 'Saving future game to file'
    print futureGames.dtypes
    futureGames.to_pickle("c:/django projects/nbaScraping/data/futureGames")

def __main__():
    getFutureGames()
    save_output()

if __name__ == '__main__':
    __main__()

