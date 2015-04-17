__author__ = 'Kang'
import twentyDay
import sqlite3
import matplotlib.pyplot as plt
import pandas as pd
from DbAPI import getPower,getTeam, getGameScoreDiff
from math import sqrt
ax = plt.subplot()
db =  sqlite3.connect(r'c:\python data science\nbaScraping\data\nba.db')
def plotAll():
    teams = getTeam(db)
    for team in teams:
        powerChart = getPower(db,'PowerChartAll',team,'2015-04-15')
        powerChart.plot(x='gameday',y='Power')
        plt.savefig(r'\python data science\nbaScraping\out/'+team+r'.png')





def getMeanStd(a):
    n = len(a)
    mean = float(sum(a)) / n
    sd = sqrt(sum((x-mean)**2 for x in a) / n)
    return mean,sd
'''
powerChart = getPower(db,'PowerChart20','golden state warriors','2015-04-15')
pd.DataFrame.hist(powerChart,ax=ax, bins = 20)
plt.show()
'''

gameScore = getGameScoreDiff(db,'toronto raptors','2015-04-15')
mean,std = getMeanStd(gameScore)
plt.hist(gameScore,bins = (-30,-25,-20,-15,-10,-5,0,5,10,15,20,25,30))
plt.savefig(r'\python data science\nbaScraping\out/TOR_hist.png')
print mean,std


