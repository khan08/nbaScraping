__author__ = 'Kang'
from API.getGame import getGame
from datetime import date,timedelta
import sqlite3



#default add yesterday games
def setupAllFinishedGames():
    db = sqlite3.connect(r'c:\python data science\nbaScraping\data\nba.db')
    cursor = db.cursor()
    end_date = date.today() - timedelta(days=2)
    start_date = date(2014,10,28)
    day_count = (end_date - start_date).days + 1
    for n in range(day_count):
        onDate = start_date + timedelta(n)
        record = getGame(onDate)
        print record
        cursor.executemany('''INSERT INTO Games values(?,?,?,?,?,?,?)''',record)
    db.commit()
    db.close()

def insertSingleDayGame(onDate = date.today()-timedelta(days=1)):
    db = sqlite3.connect(r'c:\django projects\nbaScraping\data\nba.db')
    cursor = db.cursor()
    record = getGame(onDate)
    try:
        cursor.executemany('''INSERT INTO Games values(?,?,?,?,?,?,?)''',record)
        print 'inserted'
    except Exception as e:
        print 'insert failed:',e.message
        pass
    db.commit()
    db.close()

def __main__():
    setupAllFinishedGames()

if __name__ == '__main__':
    __main__()
