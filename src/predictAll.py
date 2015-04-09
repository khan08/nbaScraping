__author__ = 'Kang'
import predictADay as pad
from datetime import date, timedelta
import pandas as pd

#Ten Game Score Diff Rule
def predictAll():
    predictAllTable = pd.DataFrame()
    end_date = date(2014,11,20)#date.today() - timedelta(days=1)
    start_date = date(2014,11,15)
    day_count = (end_date - start_date).days + 1
    for n in range(day_count):
        onDate = start_date + timedelta(n)
        print onDate
        predictAllTable = predictAllTable.append(pad.predictADay(onDate))
    print predictAllTable

predictAll()