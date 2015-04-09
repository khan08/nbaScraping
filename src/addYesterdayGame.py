__author__ = 'Kang'
from setupData import addSingleDayGame
from datetime import date,timedelta

def addYesterday():
    yesterday = date.today()-timedelta(days=1)
    addSingleDayGame(yesterday)

addYesterday()