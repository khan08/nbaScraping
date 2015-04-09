__author__ = 'Kang'
from API.getGame import getGame
from datetime import date,timedelta
import pandas as pd

#default add yesterday games
def setupAllFinishedGames():
    end_date = date.today() - timedelta(days=1)
    print end_date
    start_date = date(2014,10,28)
    day_count = (end_date - start_date).days + 1
    games = pd.read_pickle(r'\django projects\nbaScraping\data\games')
    for n in range(day_count):
        onDate = start_date + timedelta(n)
        #print getGame(onDate)
        games = games.append(getGame(onDate))
    games = games.drop_duplicates()
    games.to_pickle(r'\django projects\nbaScraping\data\games')

def addSingleDayGame(onDate):
    games = pd.read_pickle(r'\django projects\nbaScraping\data\games')
    games = games.append(getGame(onDate))
    games = games.drop_duplicates()
    games.to_pickle(r'\django projects\nbaScraping\data\games')


