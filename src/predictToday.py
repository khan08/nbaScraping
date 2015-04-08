__author__ = 'Kang'
from datetime import date, timedelta
from API.addYesterdayGames import addYesterdayGame, yesterday
from checkData import games, futureGames
from API.getScores import getTeam
import pandas as pd

pd.set_option('display.height', 1000)
pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)
pd.set_option('max_rows',200, 'max_column',210)

f=open('output.txt','w')
games = addYesterdayGame(games)
f.write('check yesterday games correctly loaded\n')
f.write('-'*100+'\n')
f.write(str(games.loc[games['Date']==yesterday])+'\n')
f.write('-'*100+'\n')

def getTodayGame():
    global todayGames
    todayGames = futureGames.loc[futureGames['Date']== date.today()]
    todayGames = todayGames.drop_duplicates()


def getPowerIndex():
    teamName = []
    teamPower = []
    for index,team in getTeam().iterrows():
        teamName.append(team['Teams'])
        powerTableHome = games.loc[(games['home_team']==team['Teams'])]
        powerTableHome = powerTableHome.sort(['Date'],ascending = 1).drop_duplicates()[-20:]
        powerTableAway = games.loc[(games['visit_team']==team['Teams'])]
        powerTableAway = powerTableAway.sort(['Date'],ascending = 1).drop_duplicates()[-20:]
        powerTableAway['score diff'] = -powerTableAway['score diff']
        powerTable = powerTableHome.append(powerTableAway)
        powerTable = powerTable.sort(['Date'],ascending = 1)[-10:]
        f.write('\n'+str(team['Teams'])+'\n')
        f.write('-'*100+'\n')
        f.write(str(powerTable)+'\n')
        f.write('-'*100+'\n')
        #print team['Teams']
        #print powerTableHome[['Date','home_team','visit_team','score diff']]
        #print powerTableAway[['Date','home_team','visit_team','score diff']]
        #print powerTable[['Date','home_team','visit_team','score diff']]
        powerIndex = powerTable.sum(axis=0)['score diff']
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
    predictHome = pd.merge(todayGames, powerChart, left_on = 'Home Team', right_on = 'Name')
    predictHome = predictHome.rename(columns={'Power':'Home Team Power'})
    predict = pd.merge(predictHome, powerChart, left_on = 'Visit Team', right_on = 'Name')
    predict = predict.rename(columns={'Power':'Visit Team Power'})[['Date','Home Team','Home Team Power',
                                                                    'Visit Team','Visit Team Power']]
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
    f.write(str(predict[['Home Team','Visit Team','PREDICTION','CONFIDENCE']]))


def __main__():
    getPowerIndex()
    getTodayGame()
    predictToday()

if __name__  ==  '__main__':
    __main__()

