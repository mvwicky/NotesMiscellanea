from bs4 import BeautifulSoup, element
from urllib import request
import requests
import multiprocessing as mp 
import os, sys, random, math, shutil

from PyQt4.QtCore import *
from PyQt4.QtGui import *

def removeNotAllowedChars(inp):
	for c in ('<','>',':','"','/','\\','|','?','*'):
		inp = inp.replace(c, '')
	return inp

def getFile(arg):
	with open(arg[1], 'wb') as f:
		print("Downloading {}".format(arg[0]))
		res = requests.get(arg[0], stream=True)
		totalLength = res.headers.get('content-length')
		if totalLength is None:
			f.write(res.content)
		else:
			dl = 0
			totalLength = int(totalLength)
			for data in res.iter_content():
				dl += len(data)
				f.write(data)


def usage(scriptName):
	print("{} OPTION".format(scriptName))
	print("if OPTION is blank: get 2010 - 2015")
	print("if OPTION is in 2010-2015, get that year")
	sys.exit(-1)

class Window(QWidget):
	def __init__(self, parent=None):
		QWidget.__init__(self, parent)

		self.audio = dict(base = 'http://www.supremecourt.gov/oral_arguments/argument_audio/',
			 	 media = 'http://www.supremecourt.gov/media/audio/mp3files/')
		self.slipBase = 'http://supremecourt.gov/opinions/slipopinion/'

		self.initUI()
	def initUI(self):
		self.setWindowTitle('Scotus Scraper')
		self.setWindowIcon(QIcon('Seal.png'))

		grid = QGridLayout()
		grid.setSpacing(10)
		pos = 0
		savedir = os.getcwd() + '\\SCOTUS\\'
		if os.path.exists(savedir):
			yDir = os.listdir(savedir)
			print(yDir)
			for year in yDir:
				yearButton = QPushButton(year, self)
				

				grid.addWidget(yearButton, pos, 1, 1, 1)
				pos += 1

		cleanButton = QPushButton('Clean', self)
		cleanButton.connect(cleanButton, SIGNAL('clicked()'), self.clean)

		pos += 1
		grid.addWidget(cleanButton, pos, 1, 1, 1)

		self.con = [QLabel(str(i), self) for i in range(5)]
		for c in self.con:
			pos += 1
			grid.addWidget(c, pos, 1, 1, 1)
			c.setText('')

		self.setLayout(grid)
		self.resize(500, 750)
		self.center()
		self.show()
	def center(self):
		qr = self.frameGeometry()
		cp = QDesktopWidget().availableGeometry().center()
		qr.moveCenter(cp)
		self.move(qr.topLeft())
	def clean(self):
		savedir = os.getcwd() + '\\SCOTUS\\'
		if os.path.exists(savedir):
			shutil.rmtree('SCOTUS', ignore_errors=True)
			if os.path.exists(savedir):
				self.sendMessage('Problem removing save directory')
			else:
				self.sendMessage('Save directory removed')
				#self.updateConsole('Save directory removed')
		else:
			self.sendMessage('Save directory not found, nothing to clean')
	def sendMessage(self, msg):
		self.updateConsole(msg)
		sys.stdout.write(msg + '\n')
		sys.stdout.flush()
	def updateConsole(self, msg):
		for i in range(len(self.con) - 1):
			self.con[i].setText(self.con[i + 1].text())
		self.con[-1].setText(msg)
	def getArgumentAudio(self, year):
		pass
	def getSlipOpinions(self, year):
		pass
	def getAll(self, year):
		pass



def main():
	scriptName = sys.argv[0] # get name
	if len(sys.argv) < 2:
		years = list(range(2010, 2016)) # no argument: all years
	elif sys.argv[1] in ('--help', '-h'): # display help
		usage(scriptName)
	elif int(sys.argv[1]) not in range(2010, 2016): 
		print("Year in Incorrect Range")
		usage(scriptName)
	else:
		year = int(sys.argv[1])
		years = [year]

	savedir = os.getcwd() + '\\SCOTUS\\'
	if not os.path.exists(savedir):
		try:
			os.makedirs(savedir)
		except: 
			print("Problem Making Save Directory")
			sys.exit(-1)

	audio = dict(base = 'http://www.supremecourt.gov/oral_arguments/argument_audio/',
			 	 media = 'http://www.supremecourt.gov/media/audio/mp3files/')
	slipBase = 'http://supremecourt.gov/opinions/slipopinion/'

	cases = dict()

	for year in years: 
		year = str(year)

		print("Making Directories for {}".format(year))
		yearDir = savedir + year + '\\'
		if not os.path.exists(yearDir):
			try:
				os.makedirs(yearDir)
			except:
				print("Problem Making: {}".format(yearDir))
				sys.exit(-1)
		else:
			print("Year Already Fetched")
			continue
		audioDir = yearDir + 'Argument Audio\\'
		if not os.path.exists(audioDir):
			try:
				os.makedirs(audioDir)
			except:
				print("Problem Making {}".format(audioDir))
				sys.exit(-1)
		slipDir = yearDir + 'Slip Opinions\\'
		if not os.path.exists(slipDir):
			try:
				os.makedirs(slipDir)
			except:
				print("Problem Making {}".format(slipDir))
				sys.exit(-1)

		print("Retrieving Documents for {}".format(year))

		print("Argument Audio")
		audioURL = audio['base'] + year # current base url
		audioSoup = BeautifulSoup(request.urlopen(audioURL), 'lxml')
		
		audioLinks = []
		audioDockets = []
		audioNames = []
		for row in audioSoup.find_all('tr'):
			for a in row.find_all('a', class_=None):
				if '../audio/' in a.get('href'):
					audioLinks.append(a.get('href')) # link is the href in the <a> tag
					audioDockets.append(a.string) # docket is the text inside the <a></a> block
					audioNames.append(row.find('span').string) # case name is stored inside a span next to the <a>

		print("Slip Opinions")		
		slipURL = slipBase + str(int(year) - 2000)
		slipSoup = BeautifulSoup(request.urlopen(slipURL), 'lxml')

		slipLinks = []
		slipDockets = []
		slipNames = []
		for row in slipSoup.find_all('tr'):
			for a in row.find_all('a'):
				if '/opinions/' + str(int(year) - 2000) + 'pdf/' in a.get('href'): 
					if ' v. ' in a.string:
						slipLinks.append(a.get('href'))
						slipNames.append(a.string)
						for cell in row.find_all('td')[2::10]:
							docket = cell.string.replace(', ', '-').replace('.', '')
							slipDockets.append(docket)
						

							

		audioURLs = [audio['media'] + i + '.mp3' for i in audioDockets]
		slipURLs = ['http://supremecourt.gov' + i for i in slipLinks]

	
		
		audioFilenames = []
		for d, n in zip(audioDockets, audioNames):
			name = audioDir + removeNotAllowedChars(d + '-' + n) + '.mp3'
			audioFilenames.append(name)
		
		slipFilenames = []
		for d, n in zip(slipDockets, slipNames):
			name = slipDir + removeNotAllowedChars(d + '-' + n) + '.pdf'
			slipFilenames.append(name)
		

		audioPair = [(i, j) for i, j in zip(audioURLs, audioFilenames)]
		slipPair = [(i, j) for i, j in zip(slipURLs, slipFilenames)]
		


		#with mp.Pool(processes=4) as pool:
		#	pool.map(getFile, audioPair)
		#	pool.map(getFile, slipPair)


	app = QApplication(sys.argv)
	w = Window()
	sys.exit(app.exec_())

if __name__ == '__main__':
	main() 