import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime, date

teamURL = "http://espn.go.com/nba/teams"
teamHTML = requests.get(teamURL)
teamSoup = BeautifulSoup(teamHTML.text)
teamTable = teamSoup.find_all('ul', class_ = 'medium-logos')

def getTeam():
    team = []
    teamPre = []
    for table in teamTable:
        lis = table.find_all('li')
        for li in lis:
            info = li.h5.a
            team.append(info.text)
            teamPre.append(info['href'].split('/')[-2])
    allTeams = {'Teams': team, 'Prefix': teamPre}
    global teams
    teams = pd.DataFrame(allTeams)
    return teams




def getScores():
    match_id = []
    dates = []
    home_team = []
    home_team_score = []
    visit_team = []
    visit_team_score = []
    score_diff = []

    for index,team in teams.iterrows():
        baseURL = 'http://espn.go.com/nba/team/schedule/_/name/{0}'
        print str(baseURL.format(team['Prefix']))
        scoreHTML = requests.get(baseURL.format(team['Prefix']))
        scoreTable = BeautifulSoup(scoreHTML.text).table
        _team = team['Teams']

        for row in scoreTable.find_all('tr'):
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
                #scores
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
                d = datetime.strptime(columns[0].text,'%a, %b %d')
                #dates.append(d)
                dates.append(date(1415, d.month, d.day))
            except (AttributeError, IndexError, ValueError) as e:
                pass

    dic = {'id': match_id,'Date':dates,  'home_team':home_team,
               'visit_team':visit_team, 'home_score': home_team_score,
            'visit_score':visit_team_score,'score diff':score_diff
            }
    global games
    games = pd.DataFrame(dic)
    print games

def saveScores():
    print 'Saving games to file'
    print games.dtypes
    games.to_pickle(r"c:/django projects/nbaScraping/data/games")

def __main__():
    getTeam()
    getScores()
    saveScores()

if __name__ == '__main__':
    __main__()



