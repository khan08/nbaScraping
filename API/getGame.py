__author__ = 'Kang'
from datetime import date, timedelta
from bs4 import BeautifulSoup
import requests
import pandas as pd

pd.set_option('display.height', 1000)
pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)
pd.set_option('max_rows',200, 'max_column',210)

def getGame(onDate):
    dates = []
    home_team = []
    home_team_score = []
    visit_team = []
    visit_team_score = []
    result = []
    score_diff = []
    #print onDate
    url = "http://www.nba.com/gameline/"+str(onDate).translate(None,'-')
    r = requests.get(url)
    for div_top in BeautifulSoup(r.text).find_all('div',class_ = 'nbaModTopScore'):
        dates.append(onDate)
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
        try:
            score_diff.append(int(_home_score)-int(_visit_score))
        except Exception:
            pass
        if _home_score > _visit_score:
            result.append('W')
        else:
            result.append('L')
    if onDate < date.today():
        dic = {'1D':dates,  '2HT':home_team,
               '3VT':visit_team, '4HS': home_team_score,
               '5VS':visit_team_score,'6SD':score_diff, '7R':result
              }
    elif onDate >= date.today():
        dic = {'1D':dates,  '2HT':home_team,
               '3VT':visit_team}

    return pd.DataFrame(dic).drop_duplicates()
