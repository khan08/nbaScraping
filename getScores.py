#import pandas as pd
import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime, date

url = 'http://espn.go.com/nba/team/schedule/_/name/bos/boston-celtics'

match_id = []
dates = []
home_team = []
home_team_score = []
visit_team = []
visit_team_score = []
score_diff = []
ultimatePredictor = []

r = requests.get(url)
table = BeautifulSoup(r.text).table
with open("rawScore.html","w") as f:
    f.write(BeautifulSoup(r.text).table.prettify())

#loop through team
_team = 'Boston'

for row in table.find_all('tr'):
    columns = row.find_all('td')
    try:
        _home = True if columns[1].li.text == 'vs' else False
        _other_team = columns[1].find_all('a')[1].text
        _score = columns[2].a.text.split(' ')[0].split('-')
        _score_diff = int(_score[0])- int(_score[1]) if _home else \
                        int(_score[1])-int(_score[0])
        _won = True if columns[2].span.text == 'W' else False

        match_id.append(columns[2].a['href'].split('?id=')[1])
        home_team.append(_team if _home else _other_team)
        visit_team.append(_team if not _home else _other_team)
        score_diff.append(_score_diff)
        #score
        if _home:
            if _won:
                home_team_score.append(_score[0])
                visit_team_score.append(_score[1])
            else:
                home_team_score.append(_score[1])
                visit_team_score.append(_score[0])
        else:
            if _won:
                home_team_score.append(_score[1])
                visit_team_score.append(_score[0])
            else:
                home_team_score.append(_score[0])
                visit_team_score.append(_score[1])

        #score differential

        d = datetime.strptime(columns[0].text,'%a, %b %d')
        #dates.append(d)
        dates.append(date(1415, d.month, d.day))

    except (AttributeError, IndexError) as e:
        pass

dic = {'id': match_id,'Date':dates,  'home_team':home_team,
       'visit_team':visit_team, 'home_score': home_team_score,
       'visit_score':visit_team_score,'score diff':score_diff
       }

games = pd.DataFrame(dic)
print(games[['home_team','visit_team','home_score',
             'visit_score','score diff']])



