__author__ = 'Kang'
import sqlite3
from datetime import date
import pandas as pd

db =  sqlite3.connect(r'c:\python data science\nbaScraping\data\nba.db')

def getTeam(db):
    cursor = db.cursor()
    cursor.execute('''SELECT name FROM Team''')
    all_rows = cursor.fetchall()
    teamName = []
    for row in all_rows:
        teamName.append(str(row[0]))
    return teamName

def getTeamGamesBeforeDate(db,team,date):
    cursor = db.cursor()
    cursor.execute('''select * from Games where homeTeam = ?
                            and date(gameDay) < ?
                            union
                            select * from Games
                            where awayTeam = ?
                            and date(gameDay) < ?
                            order by gameDay desc
                            limit 20
                            ''',(team,date,team,date))
    games = cursor.fetchall()
    print games
    return games

def getPower(db,table,team,date,ax = None):
    sql = 'SELECT * FROM %s' \
          ' where date(gameDay) < date(%r) and name = %r' %(table,date,team)
    print sql
    powerChart = pd.read_sql(sql,db)
    powerChart['gameday']=pd.to_datetime(powerChart['gameday'])
    print powerChart
    return powerChart

def getGameScoreDiff(db,team,date):
    sql = '''select * from Games where homeTeam = %r
                            and date(gameDay) < %r
                            union
                            select * from Games
                            where awayTeam = %r
                            and date(gameDay) < date(%r)
                            order by gameDay desc
                            '''%(team,date,team,date)
    games = pd.read_sql(sql,db)
    score_diffs = []
    score_diff = 0
    for item,game in games.iterrows():
                s = game['scoreDiff']
                if game['homeTeam'] == team:
                    score_diff =  s
                else:
                    score_diff = - s
                score_diffs.append(score_diff)
    return score_diffs