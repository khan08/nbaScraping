__author__ = 'Kang'
from datetime import date, timedelta
from checkData import loadGame
from API.getGame import getGame
import pandas as pd

pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)
pd.set_option('max_rows',200, 'max_column',210)

games = loadGame()

def getPowerIndex(date):
    teamName = []
    teamPower = []
    teams = games['2HT'].unique()
    for team in teams:
        teamName.append(team)
        powerTableHome = games.loc[(games['2HT']==team) & (games['1D']<date)]
        powerTableHome = powerTableHome.sort(['1D'],ascending = 1).drop_duplicates()[-20:]
        powerTableAway = games.loc[(games['3VT']==team) & (games['1D']<date)]
        powerTableAway = powerTableAway.sort(['1D'],ascending = 1).drop_duplicates()[-20:]
        powerTableAway['6SD'] = -powerTableAway['6SD']
        powerTable = powerTableHome.append(powerTableAway)
        powerTable = powerTable.sort(['1D'],ascending = 1)[-10:]
        #print team['Teams']
        #print powerTableHome[['Date','home_team','visit_team','score diff']]
        #print powerTableAway[['Date','home_team','visit_team','score diff']]
        #print powerTable[['Date','home_team','visit_team','score diff']]
        powerIndex = powerTable.sum(axis=0)['6SD']
        #print '_'*15
        teamPower.append(powerIndex)

    powerDict={'Name':teamName,'Power': teamPower}
    return pd.DataFrame(powerDict).sort(['Power'],ascending = 0)

def predictADay(date):
    prediction = []
    confidence = []
    powerChart = getPowerIndex(date)
    if date < date.today():
        aDayGames = games.loc[(games['1D']==date)]
    elif date == date.today():
        aDayGames = getGame(date.today())
    predictHome = pd.merge(aDayGames, powerChart, left_on = '2HT', right_on = 'Name')
    predictHome = predictHome.rename(columns={'Power':'4HTP'})
    predict = pd.merge(predictHome, powerChart, left_on = '3VT', right_on = 'Name')
    if date<date.today():
        predict = predict.rename(columns={'Power':'5VTP'})[['1D','2HT','3VT','4HTP','5VTP','7R']]
    else:
        predict = predict.rename(columns={'Power':'5VTP'})[['1D','2HT','3VT','4HTP','5VTP']]
    for index,row in predict.iterrows():
        if row['4HTP']>=row['5VTP']:
            prediction.append('W')
            confidence.append(row['4HTP']-row['5VTP'])
        else:
            prediction.append('L')
            confidence.append(-row['4HTP']+row['5VTP'])
    predict['6P']=prediction
    predict['7C']=confidence
    return predict

#Ten Game Score Diff Rule
def predictAll():
    predictAllTable = pd.read_pickle(r'/django projects/nbaScraping/data/TenDayRule')
    end_date = date.today() - timedelta(days=1)
    start_date = date.today() - timedelta(days=1)
    day_count = (end_date - start_date).days + 1
    for n in range(day_count):
        onDate = start_date + timedelta(n)
        print onDate
        predictAllTable = predictAllTable.append(predictADay(onDate))
    return predictAllTable.drop_duplicates()

def __main__():
    #getGame(ondate)
    #predictAll().to_pickle(r'/django projects/nbaScraping/data/TenDayRule')
    print predictADay(date.today())



if __name__  ==  '__main__':
    __main__()

