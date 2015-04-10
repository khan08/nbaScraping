__author__ = 'Kang'
from datetime import date, timedelta
from bs4 import BeautifulSoup
import requests
import pandas as pd
import sqlite3

pd.set_option('display.height', 1000)
pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)
pd.set_option('max_rows',200, 'max_column',210)

def getGame(onDate):
    record = []
    print onDate
    url = "http://www.nba.com/gameline/"+str(onDate).translate(None,'-')
    r = requests.get(url)
    for div_top in BeautifulSoup(r.text).find_all('div',class_ = 'nbaModTopScore'):
        divHomeTeam = div_top.find('div', class_='nbaModTopTeamHm')
        divAwayTeam = div_top.find('div',class_='nbaModTopTeamAw')
        _visit_team=str(divAwayTeam.img['title']).lower()
        try:
            _visit_score = divAwayTeam.find('div',class_='nbaModTopTeamNum win').text
        except Exception:
            _visit_score = divAwayTeam.find('div',class_='nbaModTopTeamNum').text
        _home_team = str(divHomeTeam.img['title']).lower()
        try:
            _home_score = divHomeTeam.find('div',class_='nbaModTopTeamNum win').text
        except Exception:
            _home_score = divHomeTeam.find('div',class_='nbaModTopTeamNum').text
        try:
            _score_diff = int(_home_score)-int(_visit_score)
        except Exception:
            pass
        try:
            if int(_home_score) - int(_visit_score)>0:
                result = ('W')
            else:
                result = ('L')
        except Exception:
            pass
        if onDate < date.today():
            record.append((str(onDate),str(_home_team),str(_visit_team),int(_home_score),int(_visit_score),_score_diff,result))
        elif onDate >= date.today():
            record.append(())
    return record
