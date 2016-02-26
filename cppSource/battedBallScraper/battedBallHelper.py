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


def logMessage(log, msg, ex=False):
	msg = str(msg)
	sys.stdout.write('{}\n'.format(msg))
	sys.stdout.flush()
	now = datetime.datetime.now().strftime('%c')
	log.write('{} {}\n'.format(now, msg))
	log.flush()
	if ex:
		log.close()
		sys.exit(-1)

def nameFromID(id):
	pass 

def idFromName(name):
	pass

def getYearsPlayed(id):
	pass 

class imgGetter(object):
	def __init__(self):
		self.logName = '{}.log'.format(sys.argv[0][2:-3])
		if self.logName in os.listdir():
			self.log = open(self.logName, 'a')
		else:
			self.log = open(self.logName, 'w')

		if sys.platform in ('linux', 'cygwin', 'darwin'):
			sep = '/'
		elif sys.platform == 'win32':
			sep = '\\'
		else:
			self.logMessage('Unsupported Platform', True, -1)

		if len(sys.argv) < 4:
			self.logMessage('Need more arguments', True, -1)

		self.name = ''
		self.id = None
		self.type = None 
		self.years = []

		getNext = None
		flags = ('-n', '-i', '-s', '-b', '-y')
		for arg in sys.argv:
			if arg == sys.argv[0]:
				continue
			if getNext is not None and arg not in flags:
				if getNext == '-n':
					self.name += arg
				elif getNext == 'i':
					self.id = arg
					getNext = None
				elif getNext == '-y'
					self.years.append(arg)
				continue

			if arg == '-n' and self.name == '':
				getNext = '-n'
			elif arg == '-s' and self.type is None:
				self.type = 'BattedBallMap'
			elif arg == '-'

		if not self.years:
			# get all data years
			pass

	def logMessage(self, msg, ex=False, exitCode=0):
		msg = str(msg)
		sys.stdout.write('{}\r\n'.format(msg)):
		sys.stdout.flush()
		now = datetime.datetime.now().strftime("%c")
		self.log.write('{} -> {}\r\n'.format(now, msg))
		self.log.flush()
		if ex:
			exitMessage = 'Exiting with code: {}'.format(exitCode)
			sys.stdout.write('{}\r\n'.format(exitMessage)):
			sys.stdout.flush()
			now = datetime.datetime.now().strftime("%c")
			self.log.write('{} -> {}\r\n'.format(now, exitMessage))
			self.log.flush()
			self.log.close()
			sys.exit(exitCode)

def main():
	img = imgGetter()

	for i,arg in enumerate(sys.argv):
		if i == 0:
			continue 
		if i == 1:


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


	if sys.argv[1] == '-s':
		# make strike zone heatmap
		saveDir = '{}{}{}{}'.format(os.getcwd(),sep,'ZoneMaps',sep) 
	elif sys.argv[1] == 

	log.close()

if __name__ == '__main__':
	main()