__author__ = 'Kang'
import twentyDay
import sqlite3
import matplotlib.pyplot as plt
db =  sqlite3.connect(r'c:\python data science\nbaScraping\data\nba.db')
ax = twentyDay.plotPowerChartTime('houston rockets','2015-04-12',db)
ax = twentyDay.plotPowerChartTime('utah jazz','2015-04-12',db,ax = ax)
plt.legend( ['NY','GSW'],loc = 'best')
plt.show()