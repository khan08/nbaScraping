__author__ = 'Kang'
from datetime import date, timedelta
from checkData import games, futureGames

def getTodayGame():
    return futureGames.loc[futureGames['Date']== date.today()+ timedelta(1)]


def getPowerIndex():
    powerTable = games[['Date','score diff']][-11:]
    powerIndex = powerTable.sum(axis=0)['score diff']
    print "powerIndex: ", powerIndex

print ''
print getTodayGame()