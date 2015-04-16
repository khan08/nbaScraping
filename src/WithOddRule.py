__author__ = 'Kang'
from datetime import date, timedelta
from setupData import insertSingleDayGame
import sqlite3
import pandas as pd
import pandas.io.sql as pd_sql

def getAllInfo(): #and db
    db = sqlite3.connect(r'c:\django projects\nbaScraping\data\nba.db')
    team = pd.read_sql(r'select * from team',db)
    return team,db

def getWinPercent(date):
    winsPercent,db = getAllInfo()
    winPercent = []
    for item,row in winsPercent.iterrows():
        team = row['name']
        allGames = pd.read_sql(r'''select * from Games where homeTeam = ?
                                  and date(gameDay) < ?
                                  union
                                  select * from Games
                                  where awayTeam = ?
                                  and date(gameDay) < ?
                                  limit 5
                                  ''',db,params = (team,date,team,date))
        wins = 0
        for item,allGame in allGames.iterrows():
            if allGame['homeTeam'] == team and allGame['result']=='W':
                wins = wins + 1
            elif allGame['awayTeam'] == team and allGame['result']=='L':
                wins = wins + 1
        gameCount =  allGames['gameday'].count()
        percent = float(wins)/gameCount
        winPercent.append(percent)
    winsPercent['winPercent'] = winPercent
    return winsPercent

    #winPercent['winPercent'] = percent
    #return winPercent

def getPowerIndex(date):
    teams, db = getAllInfo()
    teamName = []
    scoreDiff = []
    winPercent = getWinPercent(date)
    for item, row in teams.iterrows():
        team = row['name']
        score_diff = 0
        lastTenGame = pd.read_sql('''select * from Games where homeTeam = ?
                                    and date(gameDay) < ?
                                    union
                                    select * from Games
                                    where awayTeam = ?
                                    and date(gameDay) < ?
                                    limit 10
                                    ''',db, params = (team,date,team,date))
        for item, game in lastTenGame.iterrows():
            if game['scoreDiff']>10:
                    s = 10
            elif game['scoreDiff']<-10:
                    s =-10
            else:
                    s= game['scoreDiff']
            if game['homeTeam'] == team:
                opponentWin = winPercent.loc[winPercent['name']==game['awayTeam']].iloc[0]['winPercent']
                if game['result'] == 'W':
                    score_diff = score_diff + s*opponentWin
                else:
                    score_diff = score_diff + s*(1-opponentWin)
            elif game['awayTeam'] == team:
                opponentWin = winPercent.loc[winPercent['name']==game['homeTeam']].iloc[0]['winPercent']
                if game['result'] == 'L':
                    score_diff = score_diff - s*opponentWin
                else:
                    score_diff = score_diff - s*(1-opponentWin)
        scoreDiff.append(score_diff)
        teamName.append(team)
    powerDict={'Name':teamName,'Power': scoreDiff}
    powerChart = pd.DataFrame(powerDict).sort(['Power'],ascending = 0)
    return powerChart

def predictADay(date):
    db = sqlite3.connect(r'c:\django projects\nbaScraping\data\nba.db')
    prediction = []
    confidence = []
    powerChart = getPowerIndex(date)
    sql = 'SELECT * FROM Games where date(gameDay) = date(\'%s\') ' %date
    if date < date.today():
        aDayGames = pd.read_sql(sql,db)
    elif date == date.today():
        pass
    predictHome = pd.merge(aDayGames, powerChart, left_on = 'homeTeam', right_on = 'Name')
    predictHome = predictHome.rename(columns={'Power':'HTP'})
    predict = pd.merge(predictHome, powerChart, left_on = 'awayTeam', right_on = 'Name')
    predict = predict.rename(columns={'Power':'VTP'})

    for index,row in predict.iterrows():
        if row['HTP']>=row['VTP']:
            prediction.append('W')
            confidence.append(row['HTP']-row['VTP'])
        else:
            prediction.append('L')
            confidence.append(-row['HTP']+row['VTP'])

    predict['6P']=prediction
    predict['7C']=confidence
    predict = predict[['gameday','homeTeam','awayTeam','result','6P','7C']]
    db.close()
    return predict

#Ten Game Score Diff Rule
def predictAll():
    isCorrect = []
    predictAllTable = pd.DataFrame()
    end_date = date.today() - timedelta(days=1)
    start_date = date(2014,11,10)
    day_count = (end_date - start_date).days + 1
    for n in range(day_count):
        onDate = start_date + timedelta(n)
        print onDate
        predictAllTable = predictAllTable.append(predictADay(onDate))
    for item,row in predictAllTable.iterrows():
        if row['result'] == row['6P']:
            isCorrect.append(1)
        else:
            isCorrect.append(0)
    predictAllTable['isCorrect'] = isCorrect
    return predictAllTable.drop_duplicates()

def __main__():
    pass
    #getGame(ondate)

    db = sqlite3.connect(r'c:\django projects\nbaScraping\data\nba.db')
    TenWithWinRule = predictAll()
    print TenWithWinRule
    try:
        TenWithWinRule.to_sql('FlatTenWithWinRule',db,if_exists='append',index=False)
        print 'inserted'
    except Exception as e:
        print 'failed',e.message




if __name__  ==  '__main__':
    __main__()

