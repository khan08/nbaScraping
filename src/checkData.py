__author__ = 'Kang'
import pandas as pd
games = pd.read_pickle('c:/django projects/nbaScraping/data/games')
print('games loaded')
futureGames = pd.read_pickle('c:/django projects/nbaScraping/data/futureGames')
print('futureGames loaded')
