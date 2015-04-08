__author__ = 'Kang'
from datetime import date, timedelta
from checkData import games, futureGames
from API.getScores import getTeam
import pandas as pd

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
    print
    print date.today()
    print predict[['Home Team','Visit Team','PREDICTION','CONFIDENCE']]


def __main__():
    getPowerIndex()
    getTodayGame()
    predictToday()

if __name__  ==  '__main__':
    __main__()

