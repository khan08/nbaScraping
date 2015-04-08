__author__ = 'Kang'
from datetime import date, datetime, timedelta
from bs4 import BeautifulSoup
import requests
def getYesterdayGame():
    yesterday = date.today() - timedelta(days=1)
    url = "http://www.nba.com/gameline/"+str(yesterday).translate(None,'-')
    r = requests.get(url)
    for div_top in BeautifulSoup(r.text).find_all('div',class_ = 'nbaModTopScore'):
        divHomeTeam = div_top.find('div', class_='nbaModTopTeamHm')
        divAwayTeam = div_top.find('div',class_='nbaModTopTeamAw')
        print divAwayTeam.img['title']
        try:
            print divAwayTeam.find('div',class_='nbaModTopTeamNum win').text
        except Exception:
            print divAwayTeam.find('div',class_='nbaModTopTeamNum').text
        print divHomeTeam.img['title']
        try:
            print divHomeTeam.find('div',class_='nbaModTopTeamNum win').text
        except Exception:
            print divHomeTeam.find('div',class_='nbaModTopTeamNum').text

        #print divAwayTeam.img['alt'],divHomeTeam.img('alt')



getYesterdayGame()