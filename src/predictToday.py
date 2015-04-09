__author__ = 'Kang'
from datetime import date, timedelta
from API.getGame import getGame
from src.setupData import addSingleDayGame
yesterday = date.today()-timedelta(days=1)
addSingleDayGame(yesterday)
from checkData import games
import pandas as pd

todayFile = [r'c:\django projects\nbaScraping\bin/'+str(date.today())+'.txt',r'\django projects\nbaScraping\data/'
             +str(date.today())]

f=open(todayFile[0], 'w+')
f.write('check yesterday games correctly loaded\n')
f.write('-'*100+'\n')
f.write(str(games.loc[games['1D']==yesterday])+'\n')
f.write('-'*100+'\n')

def getTodayGame():
    global todayGames
    todayGames = getGame(date.today())

def getPowerIndex():
    teamName = []
    teamPower = []
    teams = games['2HT'].unique()
    for team in teams:
        teamName.append(team)
        powerTableHome = games.loc[(games['2HT']==team)]
        powerTableHome = powerTableHome.sort(['1D'],ascending = 1).drop_duplicates()[-20:]
        powerTableAway = games.loc[(games['3VT']==team)]
        powerTableAway = powerTableAway.sort(['1D'],ascending = 1).drop_duplicates()[-20:]
        powerTableAway['6SD'] = -powerTableAway['6SD']
        powerTable = powerTableHome.append(powerTableAway)
        powerTable = powerTable.sort(['1D'],ascending = 1)[-10:]
        f.write('\n'+str(team)+'\n')
        f.write('-'*100+'\n')
        f.write(str(powerTable)+'\n')
        f.write('-'*100+'\n')
        #print team['Teams']
        #print powerTableHome[['Date','home_team','visit_team','score diff']]
        #print powerTableAway[['Date','home_team','visit_team','score diff']]
        #print powerTable[['Date','home_team','visit_team','score diff']]
        powerIndex = powerTable.sum(axis=0)['6SD']
        #print '_'*15
        teamPower.append(powerIndex)
    powerDict={'Name':teamName,'Power': teamPower}
    global powerChart
    powerChart = pd.DataFrame(powerDict).sort(['Power'],ascending = 0)
    f.write('Power Chart'+'\n')
    f.write('-'*100+'\n')
    f.write('\n'+str(powerChart)+'\n')
    f.write('*'*100+'\n')

def predictToday():
    prediction = []
    confidence = []
    predictHome = pd.merge(todayGames, powerChart, left_on = '2HT', right_on = 'Name')
    predictHome = predictHome.rename(columns={'Power':'Home Team Power'})
    predict = pd.merge(predictHome, powerChart, left_on = '3VT', right_on = 'Name')
    predict = predict.rename(columns={'Power':'Visit Team Power'})[['1D','2HT','Home Team Power',
                                                                    '3VT','Visit Team Power']]
    for index,row in predict.iterrows():
        if row['Home Team Power']>=row['Visit Team Power']:
            prediction.append('W')
            confidence.append(row['Home Team Power']-row['Visit Team Power'])
        else:
            prediction.append('L')
            confidence.append(-row['Home Team Power']+row['Visit Team Power'])
    predict['PREDICTION']=prediction
    predict['CONFIDENCE']=confidence
    f.write(str(date.today())+'\n')
    f.write('*'*100+'\n')
    f.write(str(predict[['2HT','3VT','PREDICTION','CONFIDENCE']]))
    predict.to_pickle(todayFile[1])


def __main__():
    getPowerIndex()
    getTodayGame()
    predictToday()


if __name__  ==  '__main__':
    __main__()

f.close()