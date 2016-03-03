import os
import sys
import shutil
import requests
import datetime
from urllib import request
from bs4 import BeautifulSoup, element

from logger import logger

class downloader(object):
	'''class that downloads a single year of xml for a player
	   i.e., gets xml for every game a player played in'''
	def __init__(self, name, id, year):
		'''constructor
		   name: name of player 
		   id: player id 
		   year: year to get 
		'''
		self.name = str(name).replace(' ', '')
		self.id = str(id).replace(' ', '')
		self.year = str(year)
		folderName = '{}_{}'.format(self.name, self.year)
		logName = 'Downloader_{}.log'.format(folderName)

		self.log = logger(logName, ovrw=True)

		if folderName not in os.listdir():
			try:
				os.path.makedirs(self.folderName)
			except:
				self.log('Problem creating {}'.format(folderName), True, -1)
			else:
				self.log('Folder created {}'.format(folderName))

		self.saveDir = os.path.join(os.getcwd(), self.folderName)

		self.urlBase = 'http://gd2.mlb.com/components/game/mlb/year_{}/'.format(year)

		yearSoup = BeautifulSoup(request.urlopen(self.urlBase), 'lxml')
		months = []
		for a in yearSoup.find_all('a'):
			if 'month_' in a.get('href'):
				link = '{}/{}'.format(self.urlBase, a.get('href'))
				months.append(link)

		print(months)


		#gids = []
		#for a in yearSoup.find_all('a'):
		#	if 'gid_' in a.get('href'):
		#		a.append(a.get('href'))


def main():
	argNum = 7
	if len(sys.argv) < argNum:
		log = logger('Downloader Error')
		log('Expected format: -n First Last -i ID -y year')
		log('Got {} argument(s), expected {}'.format(len(sys.argv), argNum), True, -1)

	flags = ('-n', '-i', '-y')
	name = ''
	for i, arg in enumerate(sys.argv):
		print(arg)
		if arg is sys.argv[0]:
			continue
		if arg == '-n':
			j = i + 1 
			while sys.argv[j] not in flags:
				name += sys.argv[j]
				j += 1
		elif arg == '-i':
			idNum = sys.argv[i + 1]
		elif arg == '-y':
			year = sys.argv[i + 1]

	inp = (name, idNum, year)
	down = downloader(*inp)

	
	
if __name__ == '__main__':
	main()
