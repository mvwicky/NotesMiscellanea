import os
import sys
import datetime

from typing import Union

import tablib
import records
import requests
from bs4 import BeautifulSoup, SoupStrainer

from logger import Logger


class RetrosheetParser(object):
    def __init__(self, path_to_events, dbname='retrosheet'):
        self.path_to_events = os.path.normpath(path_to_events)
        self.db = records.Database('sqlite:///{}.db'.format(dbname))
        self.folders, self.files = [], dict()
        for folder in os.listdir(self.path_to_events):
            if folder[:4].isnumeric() and folder.endswith('eve'):
                self.folders.append(os.path.join(self.path_to_events, folder))
                year = int(folder[:4])
                self.files[year] = []
                events = os.path.join(self.path_to_events, folder)
                for eve in os.listdir(events):
                    file_path = os.path.join(self.path_to_events, folder, eve)
                    self.files[year].append(file_path)

    def init_team_table(self):
        self.db.query('DROP TABLE IF EXISTS teams')
        fields = ('year', 'abbreviation', 'league', 'city', 'name')
        table_struct = ('year int',
                        'abbreviation text',
                        'league text',
                        'city text',
                        'name text')
        self.db.query('CREATE TABLE teams ({}, {}, {}, {}, {})'
                      .format(*table_struct))
        for year in self.files.keys():
            file_name = 'TEAM{}'.format(year)
            year_path = os.path.join(self.path_to_events, '{}eve'.format(year))
            file_path = os.path.join(year_path, file_name)
            with open(file_path, 'rt') as file:
                for row in file:
                    row = row.replace('\n', '').split(',')
                    ins = ('INSERT INTO teams ({}, {}, {}, {}, {})'
                           .format(*fields))
                    val = ('VALUES({year}, {abbr}, {league}, {city}, {name})'
                           .format(year=int(year),
                                   abbr=str(row[0]),
                                   league=str(row[1]),
                                   city=str(row[2]),
                                   name=str(row[3])))
                    query = ' '.join([ins, val])
                    print(query)
                    self.db.query(query)


if __name__ == '__main__':
    parser = RetrosheetParser('E:\\retrosheet\\events')
    parser.init_team_table()
