__author__ = 'Kang'
import pandas as pd
games = pd.read_pickle('c:/django projects/nbaScraping/data/games')
print('games loaded')
print games
futureGames = pd.read_pickle('c:/django projects/nbaScraping/data/futureGames')
print('\n\nfutureGames loaded')
print futureGames