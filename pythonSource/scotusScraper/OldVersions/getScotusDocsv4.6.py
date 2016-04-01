from bs4 import BeautifulSoup, element
from urllib import request
import requests
import multiprocessing as mp 
import os, sys, random, math, shutil, threading, queue

from PyQt4.QtCore import *
from PyQt4.QtGui import *

QString = str

def removeNotAllowedChars(inp):
	for c in ('<','>',':','"','/','\\','|','?','*'):
		inp = inp.replace(c, '')
	return inp

class docDialog(QDialog):
	def __init__(self, parent=None):
		QDialog.__init__(self, parent)
		self.initUI()
	def initUI(self):
		self.setWindowTitle(' ')
		self.setWindowIcon(QIcon('Seal.png'))
		layout = QHBoxLayout(self)

		audioButton = QPushButton('Argument Audio', self)
		slipButton = QPushButton('Slip Opinions', self)
		bothButton = QPushButton('Both', self)
		
		layout.addWidget(audioButton)
		layout.addWidget(slipButton)
		layout.addWidget(bothButton)

		audioButton.connect(audioButton, SIGNAL('clicked()'), self.accept)
		slipButton.connect(slipButton, SIGNAL('clicked()'), self.accept)
		bothButton.connect(bothButton, SIGNAL('clicked()'), self.accept)

		self.ret = 'Cancel'
	def accept(self):
		self.ret = self.sender().text()
		super(docDialog, self).accept()
	@staticmethod
	def decRet(parent=None):
		dialog = docDialog(parent)
		result = dialog.exec_()
		return dialog.ret

class worker(QThread):
	def __init__(self, parent=None):
		QThread.__init__(self, parent)
		self.exiting = False 
		self.arg = None
	def __del__(self):
		self.exiting = True
		self.wait()
	def download(self, arg):
		self.arg = arg
		self.exiting = False
		self.start()
	def run(self):
		for arg in self.arg:
			if self.exiting:
				break
			with open(arg[1], 'wb') as f:
				self.emit(SIGNAL('output(QString)'), QString(arg[0]))
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


class window(QWidget):
	def __init__(self, parent=None):
		QWidget.__init__(self, parent)

		self.dim = (800, 500)
		self.audio = dict(base = 'http://www.supremecourt.gov/oral_arguments/argument_audio/',
			 	 		  media = 'http://www.supremecourt.gov/media/audio/mp3files/')
		self.slipBase = 'http://supremecourt.gov/opinions/slipopinion/'
		self.saveDir = os.getcwd() + '\\SCOTUS\\'
		self.queue = queue.Queue()

		self.thread = worker()

		self.connect(self.thread, SIGNAL('output(QString)'), self.sendMessage)

		self.initUI()
	def initUI(self):
		self.setWindowTitle('Scotus Scraper')
		self.setWindowIcon(QIcon('Seal.png'))

		grid = QGridLayout()
		self.con = [QLabel(' ', self) for i in range(15)]

		if not os.path.exists(self.saveDir):
			self.sendMessage('No save directory')
			try:
				os.makedirs(self.savedir)
			except:
				self.sendMessage('Problem making save directory')
				sys.exit(-1)
			else:
				self.sendMessage('Save directory created: {}'.format(self.saveDir))
		else:
			self.sendMessage('Save directory: {}'.format(self.saveDir))
		years = [str(i) for i in range(2010, 2016)]
		for year in years:
			yearButton = QPushButton(year, self)
			yearButton.connect(yearButton, SIGNAL('clicked()'), self.yearButtonPress)
			grid.addWidget(yearButton, years.index(year), 0, 1, 1)

		pos = 0
		for c in self.con:
			grid.addWidget(c, pos, 1, 1, 1)
			pos += 1

		clearCon = QPushButton('Clear Console', self)

		cancelButton = QPushButton('Cancel Download', self)
		cancelButton.connect(cancelButton, SIGNAL('clicked()'), self.cancel)
		grid.addWidget(cancelButton, grid.rowCount(), 0, 1, 1)

		cleanButton = QPushButton('Clean', self)
		cleanButton.connect(cleanButton, SIGNAL('clicked()'), self.clean)
		grid.addWidget(cleanButton, grid.rowCount(), 0, 1, 1)


		grid.setColumnStretch(0, 1)
		grid.setColumnStretch(1, 2)
		self.setLayout(grid)
		self.resize(*self.dim)
		self.center()
		self.show()
	def center(self):
		qr = self.frameGeometry()
		cp = QDesktopWidget().availableGeometry().center()
		qr.moveCenter(cp)
		self.move(qr.topLeft())
	def clean(self):
		if os.path.exists(self.saveDir):
			shutil.rmtree('SCOTUS', ignore_errors=True)
			if os.path.exists(self.saveDir):
				self.sendMessage('Problem removing save directory')
			else:
				self.sendMessage('Save directory removed')
		else:
			self.sendMessage('Save directory not found, nothing to clean')
	def cancel(self):
		self.sendMessage('Stopping Download')
		self.thread.exiting = True
	def sendMessage(self, msg):
		msg = str(msg)
		self.updateConsole(msg)
		sys.stdout.write(msg + '\n')
		sys.stdout.flush()
	def updateConsole(self, msg):
		for i in range(len(self.con) - 1):
			self.con[i].setText(self.con[i + 1].text())
		self.con[-1].setText(msg)
	def yearButtonPress(self):
		year = self.sender().text()
		yearDir = self.saveDir + year + '\\'
		res = docDialog.decRet()
		if 'Cancel' in res:
			return
		if not os.path.exists(yearDir):
			self.sendMessage('No directory for: {}'.format(year))
			try:
				os.makedirs(yearDir)
			except:
				self.sendMessage('Problem creating: {}'.format(yearDir))
				return 0
			else:
				self.sendMessage('Directory created: {}'.format(yearDir))
		if 'Audio' in res:
			self.getArgumentAudio(year)
		elif 'Slip' in res:
			self.getSlipOpinions(year)
		elif 'Both' in res:
			self.getArgumentAudio(year)
			self.getSlipOpinions(year)
	def getArgumentAudio(self, year):
		self.sendMessage('Getting argument audio')
		yearDir = self.saveDir + year + '\\'
		audioDir = yearDir + 'Argument Audio\\' 
		if not os.path.exists(audioDir):
			self.sendMessage('No directory for: {}'.format(audioDir))
			try: 
				os.makedirs(audioDir)
			except:
				self.sendMessage('Problem creating: {}'.format(audioDir))
				return 0
			else:
				self.sendMessage('Created: {}'.format(audioDir))
		audioURL = self.audio['base'] + year 
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
		audioURLs = [audio['media'] + i + '.mp3' for i in audioDockets]
		audioFilenames = []
		for d, n in zip(audioDockets, audioNames):
			name = audioDir + removeNotAllowedChars(d + '-' + n) + '.mp3'
			audioFilenames.append(name)
		audioPair = [(i, j) for i, j in zip(audioURLs, audioFilenames)]
		self.thread.download(audioPair)
	def getSlipOpinions(self, year):
		self.sendMessage('Getting slip opinions')
		yearDir = self.saveDir + year + '\\'
		slipDir = yearDir + 'Slip Opinions\\'
		if not os.path.exists(slipDir):
			self.sendMessage('No directory for: {}'.format(slipDir))
			try:
				os.makedirs(slipDir)
			except:
				self.sendMessage('Problem creating: {}'.format(slipDir))
				return 0
			else:
				self.sendMessage('Created: {}'.format(slipDir))
		slipURL = self.slipBase + str(int(year) - 2000)
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
		slipURLs = ['http://supremecourt.gov' + i for i in slipLinks]
		slipFilenames = []
		for d, n in zip(slipDockets, slipNames):
			name = slipDir + removeNotAllowedChars(d + '-' + n) + '.pdf'
			slipFilenames.append(name)
		slipPair = [(i, j) for i, j in zip(slipURLs, slipFilenames)]
		self.thread.download(slipPair)

def main():
	app = QApplication(sys.argv)
	w = window()
	sys.exit(app.exec_())

if __name__ == '__main__':
	main() 