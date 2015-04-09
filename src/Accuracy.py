__author__ = 'Kang'
import pandas as pd

pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)
pd.set_option('max_rows',200, 'max_column',210)

def getScore(ruleNameFile):
    Rule = pd.read_pickle('/django projects/nbaScraping/data/'+ruleNameFile)
    print Rule
    score = 0.0
    rows = 0.0
    for item,rule in Rule.iterrows():
        rows = rows + 1
        if rule['7R']== rule['6P']:
            score = score+1
    print score/rows


getScore('TenDayRule')