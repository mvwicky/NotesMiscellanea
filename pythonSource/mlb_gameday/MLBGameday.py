import os
import sys
import datetime

from typing import Union

import requests
import records
import tablib
from bs4 import BeautifulSoup, SoupStrainer

from logger import Logger

teams = {
    'ana': 'Los Angeles Angels of Anaheim',
    'ari': 'Arizona Diamondbacks',
    'atl': 'Atlanta Braves',
    'bal': 'Baltimore Orioles',
    'bos': 'Boston Red Sox',
    'cha': 'Chicago White Sox',
    'chn': 'Chicago Cubs',
    'cin': 'Cincinnati Reds',
    'cle': 'Cleveland Indians',
    'col': 'Colorado Rockies',
    'det': 'Detroit Tigers',
    'hou': 'Houston Astros',
    'kca': 'Kansas City Royals',
    'lan': 'Los Angeles Dodgers',
    'mia': 'Miami Marlins',
    'mil': 'Milwaukee Brewers',
    'min': 'Minnesota Twins',
    'nya': 'New York Yankees',
    'nyn': 'New York Mets',
    'oak': 'Oakland Athletics',
    'phi': 'Philadelphi Phillies',
    'pit': 'Pittsburgh Pirates',
    'sdn': 'San Diego Padres',
    'sea': 'Seattle Mariners',
    'sfn': 'San Francisco Giants',
    'sln': 'St. Louis Cardinals',
    'tba': 'Tampa Bay Rays',
    'tex': 'Texas Rangers',
    'tor': 'Toronto Blue Jays',
    'was': 'Washington Nationals'
}


class MLBGameday(object):
    base_url = 'http://gd2.mlb.com/components/game/mlb'

    def __init__(self):
        self.log = Logger('MLBGameday')

    @classmethod
    def years_with_data(cls):
        years = []
        res = requests.get(cls.base_url)
        if res.status_code == 404:
            print('Got a 404 from {}'.format(cls.base_url))
            return years
        soup = BeautifulSoup(res.content, 'lxml')
        for a in soup('a'):
            link = a.get('href')
            if link and link.startswith('year_'):
                link = link.replace('/', '').replace('year_', '')
                if link.isnumeric():
                    year = int(link)
                    print(year)

    @classmethod
    def url_day(cls, year: int, month: int, day: int):
        if month < 10:
            month = ''.join(['month_', '0', str(month)])
        else:
            month = ''.join(['month_', str(month)])
        if day < 10:
            day = ''.join(['day_', '0', str(day)])
        else:
            day = ''.join(['day_', str(day)])
        year = 'year_{}'.format(year)
        return '/'.join([cls.base_url, year, month, day])

    @classmethod
    def num_games_played_on_date(cls, year: int, month: int, day: int):
        url = cls.url_day(year, month, day)
        res = requests.get(url)
        if res.status_code == 404:
            print('Got a 404 from {}'.format(url))
            return -1
        soup = BeautifulSoup(res.content, 'lxml')
        num_games = 0
        for a in soup('a'):
            link = a.get('href')
            if link and link.startswith('gid'):
                num_games += 1
        return num_games

    @classmethod
    def urls_on_date(cls, year: int, month: int, day: int):
        folders = []
        url = cls.url_day(year, month, day)
        res = requests.get(url)
        if res.status_code == 404:
            print('Got a 404 from {}'.format(url))
            return folders
        soup = BeautifulSoup(res.content, 'lxml')
        for a in soup('a'):
            link = a.get('href')
            if link and link.startswith('gid'):
                folders.append(link)
        return ['/'.join([cls.base_url, game]) for game in folders]

if __name__ == '__main__':
    mlb = MLBGameday()
    mlb.years_with_data()
    print(mlb.urls_on_date(2016, 5, 11))
