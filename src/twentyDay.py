__author__ = 'Kang'
__author__ = 'Kang'
from datetime import date, timedelta
from setupData import insertSingleDayGame
import sqlite3
import pandas as pd
import pandas.io.sql as pd_sql
import matplotlib.pyplot as plt

def getPowerIndex(date, db):
    cursor = db.cursor()
    cursor.execute('''SELECT name FROM Team''')
    all_rows = cursor.fetchall()
    teamName = []
    scoreDiff = []
    dates = []
    for row in all_rows:
        for team in row:
            score_diff = 0
            cursor.execute('''select * from Games where homeTeam = ?
                            and date(gameDay) < ?
                            union
                            select * from Games
                            where awayTeam = ?
                            and date(gameDay) < ?
                            order by gameDay desc
                            ''',(team,date,team,date))
            games = cursor.fetchall()
            for game in games:
                s = game[5]
                if game[1] == team:
                    score_diff = score_diff + s
                else:
                    score_diff = score_diff - s
            teamName.append(team)
            dates.append(date)
            scoreDiff.append(score_diff)
    powerDict={'gameday':dates, 'Name':teamName,'Power': scoreDiff}
    return pd.DataFrame(powerDict).sort(['Power'],ascending = 0)

def plotPowerChartTime(db,table,team,date,ax = None):
    sql = 'SELECT * FROM %s' \
          ' where date(gameDay) < date(\'%s\') and name = %r' %(table,date,team)
    print sql
    powerChart = pd.read_sql(sql,db)
    print powerChart
    powerChart['gameday']=pd.to_datetime(powerChart['gameday'])
    return powerChart.plot(x='gameday',y='Power',title='Power Chart', ax = ax)
    #print powerChart

def predictADay(date,db):
    prediction = []
    confidence = []
    powerChart = getPowerIndex(date,db)
    try:
        powerChart.to_sql('PowerChartAll',db,if_exists='append',index=False)
        print 'inserted powerChart',date
    except Exception as e:
        print e.message
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
    isCorrect = []
    for item,row in predict.iterrows():
        if row['result'] == row['6P']:
            isCorrect.append(1)
        else:
            isCorrect.append(0)
    predict['isCorrect'] = isCorrect
    try:
        predict.to_sql('AllGame',db,if_exists='append',index=False)
        print 'inserted prediction',date
    except Exception as e:
        print e.message

#Ten Game Score Diff Rule
def predictAll(db):
    end_date = date.today() - timedelta(days=1)
    start_date = date(2014,11,10)
    day_count = (end_date - start_date).days + 1
    for n in range(day_count):
        onDate = start_date + timedelta(n)
        print onDate
        predictADay(onDate,db)

def __main__():
    db =  sqlite3.connect(r'c:\python data science\nbaScraping\data\nba.db')
    predictAll(db)






if __name__  ==  '__main__':
    __main__()

