import os 
import sys
import csv
import shutil
import urllib

import requests
from bs4 import BeautifulSoup

from PyQt4.QtCore import *
from PyQt4.QtGui import *

from logger import Logger

try:
    test = QString('Test')
except NameError:
    QString = str

class FG_Parse(object):
	def __init__(self, file_name):
		self.file_name = file_name
		self.log = Logger('FG_Parse')
		self.pitcher_ids = dict()
		self.batter_ids = dict()
		self.pitcher_csv = 'Pitcher_IDs.csv'
		self.batter_csv = 'Batter_IDs.csv'

	def get_pitcher_ids_from_csv(self, file_name):
		self.log('Populating pitcher ID#s from: {}'.format(file_name))
		ids = dict()
		with open(file_name, 'rt') as fg_file:
			for row in fg_file:
				fields = row.replace('"', '').split(',')
				player = fields[0]
				i = fields[-1].replace('\n', '')
				if i.isnumeric():
					ids[player] = int(i)
		return ids

	def get_pitcher_ids(self, clean=False):
		if self.pitcher_csv in os.listdir() and not clean:
			self.log('Pitcher ID#s already found in: {}'.format(self.pitcher_csv))
			self.pitcher_ids = self.get_pitcher_ids_from_csv(self.pitcher_csv)
			return
		self.log('{} not found'.format(self.pitcher_csv))
		self.log('Populating pitcher ID#s from fangraphs')
		ids = dict()
		url = 'http://www.fangraphs.com/leaders.aspx'
		opts = {'pos': 'all', 'stats': 'pit', 'lg': 'all', 'qual': 0, 'type': 8,
			   'season': 2016, 'month': 0, 'season1': 1871, 'ind': 0, 'team': 0, 
			   'rost': 0, 'age': 0, 'filter': '', 'players': 0, 'page':'1_30'}
		res = requests.get(url, params=opts)
		if res.url.find('error') > 0:
			self.log('Problem getting leaderboards')
			self.log(res.url, ex=True)
		soup = BeautifulSoup(res.content, 'lxml')
		self.log('Successful query, finding number of pages in leaderboard')
		num_pages = 1
		for link in soup('a'):
			if link.get('title') == 'Last Page':
				href = link.get('href')
				p = href.find('page')
				equals = href.find('=', href.find('page'))
				uscore = href.find('_', equals)
				num_pages = href[equals+1:uscore]
				if num_pages.isnumeric():
					num_pages = int(num_pages)
				else:
					self.log('Problem finding the number of pages', ex=True)
				break
		self.log('Num pages: {}'.format(num_pages))
		for page in range(1, num_pages+1):
			c_page = '{}_30'.format(page)
			opts['page'] = c_page
			res = requests.get(url, params=opts)
			if res.url.find('error') > 0:
				self.log('Problem getting page: {} from pitching leaderboards'.format(page), ex=True)
			soup = BeautifulSoup(res.content, 'lxml')
			self.log('Parsing page {} of {}'.format(page, num_pages))
			for elem in soup('tbody'):
				for row in elem('tr'):
					for cell in row('td'):
						for child in cell.children:
							if str(child).find('playerid=') > 0:
								child = str(child)
								equals = child.find('=', child.find('playerid'))
								ampers = child.find('&', equals)
								p_id = child[equals+1:ampers]
								close_a = child.find('>')
								open_a = child.find('</', close_a)
								p_name = child[close_a+1:open_a]
								ids[p_name] = int(p_id)
		self.pitcher_ids = ids
		self.log('Done parsing, writing values to: {}'.format(self.pitcher_csv))
		with open(self.pitcher_csv, 'w', newline='\n') as pitcher_csv:
			pitcher_writer = csv.writer(pitcher_csv, delimiter=',')
			pitcher_writer.writerow(['Name', 'ID#'])
			for name, i in self.pitcher_ids.items():
				pitcher_writer.writerow([name, i])
		self.log('Pitcher ID#s populated')

	def get_batter_ids_from_csv(self, file_name):
		self.log('Populating batter ID#s from: {}'.format(file_name))
		ids = dict()
		with open(file_name, 'rt') as fg_file:
			for row in fg_file:
				fields = row.replace('"', '').split(',')
				player = fields[0]
				i = fields[-1].replace('\n', '')
				if i.isnumeric():
					ids[player] = int(i)
		return ids


	def get_batter_ids(self, clean=False):
		if self.batter_csv in os.listdir() and not clean:
			self.log('Batter ID#s already found in: {}'.format(self.batter_csv))
			self.batter_ids = self.get_batter_ids_from_csv(self.batter_csv)
			return

	def get_pitcher_game_logs(self, player):
		if type(player) == str:
			p_id = self.pitcher_ids[player]
			p_name = player
		elif type(player) == int:
			p_id = player 
			for p in self.pitcher_ids:
				if self.pitcher_ids[p] == player:
					p_name = p

		csv_name = '{}_GameLogsAll.csv'.format(p_name)
		# Make sure that the file does not exist
		if csv_name in os.listdir():
		 	print('File already generated')
		 	return
		base_url = 'http://fangraphs.com/'
		options = 'statsd.aspx?playerid={}&position=P&type=0&gds=&gde=&season=all'.format(p_id)
		url = '{}{}'.format(base_url, options)
		res = requests.get(url)
		if res.url.find('error') != -1:
			print('Problem getting game log, may not exist')
			return 
		fg_soup = BeautifulSoup(res.content, 'lxml')
		headers = []
		game_stats = []
		num = 0
		for row in fg_soup('tr'):
			for head in row('th', class_='rgHeader'):
				headers.append(head.text)
			cRow = []
			for cell in row('td'):
				if cell.get('class'):
					for elem in cell.get('class'):
						if elem.find('grid_line_') != -1:
							cRow.append(cell.text)
			if cRow:
				game_stats.append(cRow)
		
		with open(csv_name, 'w', newline='\n') as player_csv:
			player_writer = csv.writer(player_csv, delimiter=',')
			player_writer.writerow(headers)
			for game in game_stats:
				player_writer.writerow(game)

	def get_batter_game_logs(self, player):
		if type(player) == str:
			p_id = self.batter_ids[player]
			p_name = player 
		elif type(player) == int:
			p_id = player 
			for p in self.batter_ids:
				if self.batter_ids[p] == player:
					p_name = p


def main():
	file_name = 'Pitchers_All_1871_2016_MinIP_0.csv'
	parse = FG_Parse(file_name)
	parse.get_pitcher_ids(True)
	for p, i in parse.pitcher_ids.items():
		print(p, i)
if __name__=='__main__':
	main()