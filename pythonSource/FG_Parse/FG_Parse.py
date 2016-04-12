import os 
import sys
import csv
import shutil
import urllib
import datetime

import requests
from bs4 import BeautifulSoup, SoupStrainer

from PyQt4.QtCore import *
from PyQt4.QtGui import *

import matplotlib as mpl
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import matplotlib.pyplot as plt

from logger import Logger

try:
    test = QString('Test')
except NameError:
    QString = str

class FG_Parser(object):
	def __init__(self):
		self.log = Logger('FG_Parser')
		self.pitcher_ids = dict()
		self.batter_ids = dict()
		self.pitcher_csv = 'Pitcher_IDs.csv'
		self.batter_csv = 'Batter_IDs.csv'

	def get_id_name_tup(self, player):
		if type(player) == str:
			try:
				p_id = self.batter_ids[player]
			except KeyError:
				p_id = self.pitcher_ids[player]
			finally:
				p_name = player
		elif type(player) == int:
			p_id = player
			p_name = None
			for p in self.batter_ids:
				if self.batter_ids[p] == player:
					p_name = p 
					break
			if p_name is None:
				for p in self.pitcher_ids:
					if self.pitcher_ids[p] == player:
						p_name = p 
						break
		return (p_id, p_name)

	def get_ids_csv(self, pit=True, bat=True):
		if not pit and not bat:
			self.log('Populating no ids')
			return 
		if pit and self.pitcher_csv not in os.listdir():
			self.log('{} not found'.format(self.pitcher_csv), ex=True)
		if bat and self.batter_csv not in os.listdir():
			self.log('{} not found'.format(self.batter_csv), ex=True)
		if not (bat and pit):
			file_name = self.pitcher_csv if pit else self.batter_csv 
			ids = dict()
			self.log('Populating {} ID#s from: {}'.format('pitcher' if pit else 'batter', file_name))
			with open(file_name, 'rt') as fg_file:
				for row in fg_file:
					fields = row.replace('"', '').split(',')
					player = fields[0]
					i = fields[-1].replace('\n', '')
					if i.isnumeric():
						ids[player] = int(i)
			if pit:
				self.pitcher_ids = ids 
			if bat: 
				self.batter_ids = ids
			return ids
		if pit and bat:
			self.get_ids_csv(True, False)
			self.get_ids_csv(False, True)

	def get_ids_web(self, pit=True, bat=True, clean=False):
		if not pit and not bat:
			self.log('Getting no ids')
			return
		if pit and self.pitcher_csv in os.listdir() and not clean:
			self.log('Pitcher ID#s already found in: {}'.format(self.pitcher_csv))
			self.get_ids_csv(True, False)
			return
		if bat and self.batter_csv in os.listdir() and not clean:
			self.log('Batter ID#s already found in: {}'.format(self.batter_csv))
			self.get_ids_csv(False, True)
			return
		opts = {'pos': 'all', 'lg': 'all', 'qual': 0, 'type': 8,
			   'season': 2016, 'month': 0, 'season1': 1871, 'ind': 0, 'team': 0, 
			   'rost': 0, 'age': 0, 'filter': '', 'players': 0, 'page':'1_30'}
		if not (bat and pit):
			opts['stats'] = 'pit' if pit else 'bat'
			self.log('Populating {} ID#s'.format('pitcher' if pit else 'batter'))
			url = 'http://fangraphs.com/leaders.aspx'
			res = requests.get(url, params=opts)
			if res.url.find('error') != -1:
				self.log('Problem getting {} leaderboards'.format('pitching' if pit else 'batting'))
				self.log(res.url, ex=True)
			soup = BeautifulSoup(res.content, 'lxml')
			self.log('Successful query, finding number of pages in {} leaderboard'.format('pitching' if pit else 'batting'))
			num_pages = 1 
			for link in soup('a'):
				if link.get('title') == 'Last Page':
					href = link.get('href')
					equals = href.find('=', href.find('page'))
					uscore = href.find('_', equals)
					num_pages = href[equals+1:uscore]
					if num_pages.isnumeric():
						num_pages = int(num_pages)
					else:
						self.log('Problem finding number of pages')
						self.log('Value found: {}'.format(num_pages), ex=True)
					break
			self.log('Num pages in {} leaderboard: {} '.format('pitching' if pit else 'batting', num_pages))
			ids = dict()
			for page in range(1, num_pages + 1):
				c_page = '{}_30'.format(page)
				opts['page'] = c_page
				res = requests.get(url, params=opts)
				if res.url.find('error') != -1:
					self.log('Problem getting page {} from {} leaderboards'.format(
						page, 'pitching' if pit else 'batting'))
				tbody = SoupStrainer('tbody')
				soup = BeautifulSoup(res.content, 'lxml', parse_only=tbody)
				self.log('Parsing page {} of {} ({} leaderboard)'.format(
					page, num_pages, 'Pitchers' if pit else 'Batters'))
				for row in soup('tr'):
					for cell in row('td'):
						for child in cell.children:
							if str(child).find('playerid=') > 0:
								child = str(child)
								equals = child.find('=', 
									child.find('playerid'))
								ampers = child.find('&', equals)
								p_id = child[equals+1:ampers]
								close_a = child.find('>')
								open_a = child.find('</', close_a)
								p_name = child[close_a+1:open_a]
								ids[p_name] = p_id
		
			p_csv = self.pitcher_csv if pit else self.batter_csv	
			self.log('Done parsing, writing values to: {}'.format(p_csv))
			with open(p_csv, 'w', newline='\n') as csv_file:
				player_writer = csv.writer(csv_file, delimiter=',')
				player_writer.writerow(['Name', 'ID#'])
				for name, i in ids.items():
					player_writer.writerow([name, i])
			if pit:
				self.pitcher_ids = ids 
			if bat: 
				self.batter_ids = ids
			self.log('{} ID#s populated'.format('Pitcher' if pit else 'Batter'))
		if bat and pit:
			self.get_ids_web(True, False, clean)
			self.get_ids_web(False, True, clean)

	def get_game_logs(self, player, clean=False):
		p_tup = self.get_id_name_tup(player)
		
		csv_name = '{}_GameLogs_All.csv'.format(p_tup[1].replace(' ', ''))
		# Make sure that the file does not exist
		if csv_name in os.listdir() and not clean:
		 	self.log('File already generated: {}'.format(csv_name))
		 	return csv_name
		url = 'http://fangraphs.com/statsd.aspx'
		opts = {'playerid': p_tup[0], 'season':'all'}
		res = requests.get(url, params=opts)
		if res.url.find('error') != -1:
			self.log('Problem getting game logs for: {}, may not exist'.format(p_tup[1]))
			return csv_name
		self.log('Getting game logs for: {}'.format(p_tup[1]))
		soup = BeautifulSoup(res.content, 'lxml')
		headers = []
		game_stats = []
		for row in soup('tr'):
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
		self.log('Game logs found, writing to csv')
		with open(csv_name, 'w', newline='\n') as player_csv:
			player_writer = csv.writer(player_csv, delimiter=',')
			player_writer.writerow(headers)
			for game in game_stats:
				player_writer.writerow(game)
		self.log('Game logs for {} written to: {}'.format(p_tup[1], csv_name))
		return csv_name

	def get_play_logs(self, player, clean=False):
		p_tup = self.get_id_name_tup(player)
		csv_name = '{}_PlayLogsAll.csv'.format(p_tup[1].replace(' ', ''))
		# Make sure that the file does not exist
		if csv_name in os.listdir() and not clean:
		 	self.log('File already generated: {}'.format(csv_name))
		 	return csv_name
		url = 'http://fangraphs.com/statsp.aspx'
		opts = {'playerid': p_tup[0]}
		res = requests.get(url, params=opts)
		if res.url.find('error') != -1:
			self.log('Problem getting play logs for: {}, may not exist'.format(p_tup[1]))
			return csv_name
		self.log('Getting play logs for: {}'.format(p_tup[1]))
		soup = BeautifulSoup(res.content, 'lxml')
		years = []
		headers = []
		for div in soup('div', id='PlayStats1_tsLog', class_='RadTabStrip'):
			for span in div('span', class_='rtsTxt'):
				if span.text.isnumeric():
					years.append(int(span.text))
		for head in soup('thead'):
			for col in head('th', class_='rgHeader'):
				headers.append(col.get_text())

		with open(csv_name, 'w', newline='\n') as file:
			player_writer = csv.writer(file, delimiter=',')
			player_writer.writerow(headers)

		for year in years:
			opts['season'] = year
			res = requests.get(url, params=opts)
			if res.url.find('error') != -1:
				self.log('Problem getting play logs for: {}, year: {}'.format(p_tup[1], year))
				return csv_name
			tbody = SoupStrainer('tbody')
			soup = BeautifulSoup(res.content, 'lxml', parse_only=tbody)
			plays = []	
			for row in soup('tr'):
				c_play = []
				for cell in row('td'):
					if cell.get('class'):
						for cl in cell.get('class'):
							if cl.find('grid_line_') != -1:
								c_play.append(cell.text)
				d = ('{}/{}'.format(c_play[0], year)).split('/')
				c_play[0] = datetime.date(int(d[2]), int(d[0]), int(d[1]))
				plays.append(c_play)
			with open(csv_name, 'a', newline='\n') as file:
				player_writer = csv.writer(file, delimiter=',')
				dates = []
				for play in plays:
					player_writer.writerow(play)
		self.log('Play logs for {} written to: {}'.format(p_tup[1], csv_name))
		return csv_name

	def wOBA_game(self, player, year=None):
		p_tup = self.get_id_name_tup(player)
		if p_tup[1] not in self.batter_ids:
			self.log('{} is not a batter'.format(p_tup[1]))
			return
		csv_name = self.get_game_logs(p_tup[0])
		dates = []
		wOBAs = []
		with open(csv_name, 'rt') as game_logs:
			for row in game_logs:
				fields = row.replace('"', '').split(',')
				if row.startswith('Date'):
					woba_ind = fields.index('wOBA')
					continue
				if row.startswith('Total'):
					continue
				d = fields[0].split('-')
				if year and int(d[0]) == year:
					dates.insert(0, datetime.date(int(d[0]), int(d[1]), int(d[2])))
					wOBAs.insert(0, fields[woba_ind])
				elif not year:
					dates.insert(0, datetime.date(int(d[0]), int(d[1]), int(d[2])))
					wOBAs.insert(0, fields[woba_ind])
		
		plt.close()
		plt.plot(dates, wOBAs, 'r.')
		plt.title('{} per game wOBA'.format(p_tup[1]))
		plt.grid()
		plt.savefig('{}PerGame_wOBA.png'.format(p_tup[1].replace(' ', '')), bbox_inches='tight')

	def cum_avg_wOBA(self, player):
		p_tup = self.get_id_name_tup(player)
		if p_tup[1] not in self.batter_ids:
			self.log('{} is not a batter'.format(p_tup[1]))
			return 
		csv_name = self.get_game_logs(p_tup[0])
		dates = []
		wOBAs = []
		with open(csv_name, 'rt') as game_logs:
			for row in game_logs:
				fields = row.replace('"', '').split(',')
				if row.startswith('Date'):
					woba_ind = fields.index('wOBA')
					continue
				if row.startswith('Total'):
					continue
				d = fields[0].split('-')
				dates.insert(0, datetime.date(int(d[0]), int(d[1]), int(d[2])))
				wOBAs.insert(0, float(fields[woba_ind]))
		cma = []
		for n, woba in enumerate(wOBAs):
			if n == 0:
				cma.insert(0, woba)
				continue
			cma_n1 = cma[n-1] + (woba - cma[n-1]) / n
			cma.append(cma_n1)

		plt.close()
		plt.plot(dates, cma, 'r.')
		plt.title('{} cumulative average wOBA'.format(p_tup[1]))
		plt.grid()
		plt.savefig('{}CumulativeAverage_wOBA.png'.format(p_tup[1].replace(' ', '')), bbox_inches='tight')

	def cum_avg(self, player, stat):
		p_tup = self.get_id_name_tup(player)
		csv_name = self.get_game_logs(p_tup[0])

	def per_game(self, player, stat):
		p_tup = self.get_id_name_tup(player)
		csv_name = self.get_game_logs(p_tup[0])


def main():
	pass
	
if __name__=='__main__':
	main()