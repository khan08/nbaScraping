__author__ = 'Kang'
from checkData import games, futureGames

def getPowerIndex():
    powerTable = games[['Date','score diff']][-11:]
    powerIndex = powerTable.sum(axis=0)['score diff']
    print "powerIndex: ", powerIndex

