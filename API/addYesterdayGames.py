__author__ = 'Kang'
from datetime import date, timedelta
from bs4 import BeautifulSoup
import requests
import pandas as pd
import src.checkData

yesterday = date.today() - timedelta(days=1)

def getYesterdayGame(games):
    dates = []
    home_team = []
    home_team_score = []
    visit_team = []
    visit_team_score = []
    score_diff = []

    url = "http://www.nba.com/gameline/"+str(yesterday).translate(None,'-')
    r = requests.get(url)
    for div_top in BeautifulSoup(r.text).find_all('div',class_ = 'nbaModTopScore'):
        dates.append(yesterday)
        divHomeTeam = div_top.find('div', class_='nbaModTopTeamHm')
        divAwayTeam = div_top.find('div',class_='nbaModTopTeamAw')
        visit_team.append(str(divAwayTeam.img['title']).lower())
        try:
            _visit_score = divAwayTeam.find('div',class_='nbaModTopTeamNum win').text
            visit_team_score.append(_visit_score)
        except Exception:
            _visit_score = divAwayTeam.find('div',class_='nbaModTopTeamNum').text
            visit_team_score.append(_visit_score)
        home_team.append(str(divHomeTeam.img['title']).lower())
        try:
            _home_score = divHomeTeam.find('div',class_='nbaModTopTeamNum win').text
            home_team_score.append(_home_score)
        except Exception:
            _home_score = divHomeTeam.find('div',class_='nbaModTopTeamNum').text
            home_team_score.append(_home_score)
        score_diff.append(int(_home_score)-int(_visit_score))
    dic = {'Date':dates,  'home_team':home_team,
           'visit_team':visit_team, 'home_score': home_team_score,
           'visit_score':visit_team_score,'score diff':score_diff
            }
    games = games.append(pd.DataFrame(dic)).drop_duplicates()
    games.to_pickle(r"c:/django projects/nbaScraping/data/games")
    print 'Yesterday Games Added'
    return games


