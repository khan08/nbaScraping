__author__ = 'Kang'
from getScores import table
import pandas as pd
from datetime import datetime, date

def getFutureGames():
    dates = []
    home_team = []
    visit_team = []
    _team = 'Boston'

    for row in table.find_all('tr'):
        try:
            columns = row.find_all('td')
            _home = True if columns[1].li.text == 'vs' else False
            _other_team = columns[1].find_all('a')[1].text
            d = datetime.strptime(columns[0].text,'%a, %b %d')
            if d.month<8:
                d = d.replace(2015)
            else:
                d = d.replace(2014)
            now = datetime.now()
            if d > now:
                print d
                dates.append(d)
                home_team.append(_team if _home else _other_team)
                visit_team.append(_team if not _home else _other_team)
                print _other_team
                print _team
        except (ValueError, IndexError, AttributeError):
            pass
    print len(dates), len(home_team),len(visit_team)
    dict = {'Date': dates, 'Home Team': home_team, 'Visit Team':visit_team}
    global futureGames
    futureGames = pd.DataFrame(dict)

def save_output():
    print 'Saving future game to file'
    print futureGames.dtypes
    futureGames.to_pickle("c:/django projects/nbaScraping/data/futureGames")

def __main__():
    getFutureGames()
    save_output()

if __name__ == '__main__':
    __main__()

