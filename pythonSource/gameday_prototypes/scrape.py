import re
import os
import sys

from datetime import date

import requests
from bs4 import BeautifulSoup


class gameday_scraper(object):
    def __init__(self, year, team):
        self.base_url = ('http://gd2.mlb.com/components/game/mlb/year_{}'
                         .format(year))
        self.year = year
        self.team = team
        self.game_dates = dict()
        self.game_paths = dict()
        save_folder_name = '_'.join([team.upper(), str(year)])
        self.save_path = os.path.abspath(save_folder_name)
        if not os.path.exists(self.save_path):
            try:
                os.makedirs(self.save_path)
            except:
                print('Problem making save path')
        print('Save Folder: {}'.format(self.save_path))

    def get_game_dates(self):
        months = dict()
        res = requests.get(self.base_url)
        if res.status_code == 404:
            print('Got 404')
            return months
        soup = BeautifulSoup(res.content, 'lxml')
        for a in soup('a'):
            link = a.get('href')
            if link and link.startswith('month'):
                months[link] = []
        for link, days in months.items():
            url = '/'.join([self.base_url, link])
            res = requests.get(url)
            if res.status_code == 404:
                print('Got 404')
                return days
            soup = BeautifulSoup(res.content, 'lxml')
            for a in soup('a'):
                link = a.get('href')
                if link and link.startswith('day'):
                    days.append(link)
        for month, days in months.items():
            for day in days:
                month_str, day_str = month[-3:-1], day[-3:-1]
                url = '/'.join([self.base_url, month, day])
                res = requests.get(url)
                if res.status_code == 200:
                    soup = BeautifulSoup(res.content, 'lxml')
                    for a in soup('a'):
                        link = a.get('href')
                        if link and link.startswith('gid'):
                            if link.find(self.team) != -1:
                                m, d = int(month_str), int(day_str)
                                game_date = date(int(self.year), m, d)
                                self.game_dates[game_date] = '/'.join([url,
                                                                       link])
                else:
                    continue

    def get_game_files(self):
        for date, link in self.game_dates.items():
            url = '/'.join([link, 'inning/inning_all.xml'])
            file_name = '{}.xml'.format(date)
            file_path = os.path.join(self.save_path, file_name)
            print('Getting game played on: {}'.format(date))
            res = requests.get(url)
            if res.status_code == 404:
                continue
            with open(file_path, 'wb') as file:
                res = requests.get(url, stream=True)
                if not res.headers.get('content-length'):
                    file.write(res.content)
                else:
                    for data in res.iter_content():
                        file.write(data)

if __name__ == '__main__':
    scraper = gameday_scraper(2016, 'lan')
    scraper.get_game_dates()
    scraper.get_game_files()
