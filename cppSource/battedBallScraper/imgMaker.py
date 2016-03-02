import os
import sys
import shutil
import requests
import datetime
from urllib import request
from bs4 import BeautifulSoup, element

import matplotlib as mpl
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import matplotlib.pyplot as plt

from logger import logger

class imgGetter(object):
	def __init__(self):
		self.log = logger(name='main')

		if sys.platform in ('linux', 'cygwin', 'darwin'):
			sep = '/'
		elif sys.platform == 'win32':
			sep = '\\'
		else:
			self.log('Unsupported Platform', True, -1)

		if len(sys.argv) < 4:
			self.log('Need more arguments', True, -1)

		self.urlbase = 'http://gd2.mlb.com/components/game/mlb/'

		self.name = ''
		self.id = None
		self.type = None 
		self.years = []

		getNext = None
		flags = ('-n', '-i', '-s', '-b', '-y')
		# Arguments:
		# 	required:
		#		-n: indicate player name OR -i indicate player id
		# 		-s: make a strike zone heat map
		#		-b: make a batted ball map
		#	optional
		#		-y year: specific year, or all years with data if not set
		#
		# ex ./battedBallHelper -n Yasiel Puig -s -y 2013
		#		get Yasiel Puig's strike zone map from 2013
		for arg in sys.argv:
			if arg is sys.argv[0]:
				continue
			if getNext is not None and arg not in flags:
				if getNext == '-n':
					self.name += arg
				elif getNext == 'i':
					self.id = arg
					getNext = None
				elif getNext == '-y':
					self.years.append(arg)
				continue

			if getNext is None and arg in flags:
				if arg == '-n' and self.name == '':
					getNext = '-n'
				elif arg == '-s' and self.type is None:
					self.type = 'ZoneMap'
				elif arg == '-b' and self.type is None:
					self.type = 'BattedBallMap'

		if not self.years:
			# get all data years
			allYears = True
			pass

		if self.Name is None and self.id is None:
			self.log('Neither name nor id populated', True, -1)
		if self.type is None:
			self.log('Type not populated', True, -1)
		if not self.years:
			self.log('Year(s) not populated', True, -1)

		if len(self.years) == 1:
			self.log('Getting {}\'s {} for {}'.format(self.name, self.type, self.years[0]))
		elif allYears:
			self.log('Getting {}\'s {} for {} to {}'.format(self.name, self.type, self.years[0], self.years[-1]))
		else:
			self.log('Getting {}\'s {} for {}'.format(self.name, self.type, self.years))

		self.basesoup = BeautifulSoup(request.urlopen(self.urlbase), 'lxml')

		if self.id is None: # get name
			pass
		elif self.Name is None: # get id
			pass

		self.cullYears() 

		self.teams = None
		self.getTeams()


	def cullYears(self): # remove years without data
		pass

	def getTeams(self): # make a dict of teams per year
		pass

	def getName(self):
		if self.id is None:
			self.log('')

	def getMonths(self, year):
		pass

	def getData(self):
		for year in self.years:
			self.logMessage('Year: {}'.format(year))
			yearbase = self.urlbase + 'year_{}'.format(year) + '/'
			yearsoup = BeautifulSoup(request.urlopen(yearbase), 'lxml')

	@staticmethod
	def translateTeam(code):
		if 'bos' in code:
			return 'Boston Red Sox'
		elif 'nya' in code:
			return 'New York Yankees'
		elif 'chn' in code:
			return 'Chicago Cubs'
		elif 'col' in code:
			return 'Colorado Rockies'
		elif 'det' in code:
			return 'Detroit Tigers'
		elif 'cle' in code:
			return 'Cleveland Indians'
		elif 'hou' in code:
			return 'Houston Astros'
		elif 'tex' in code:
			return 'Texas Rangers'
		elif 'kca' in code:
			return 'Kansas City Royals'
		#elif ''

def main():
	img = imgGetter()
	img.getData()

if __name__ == '__main__':
	main()