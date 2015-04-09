__author__ = 'Kang'
import pandas as pd

def loadGame():
    return pd.read_pickle('c:/django projects/nbaScraping/data/games').drop_duplicates()
    print('games loaded')
