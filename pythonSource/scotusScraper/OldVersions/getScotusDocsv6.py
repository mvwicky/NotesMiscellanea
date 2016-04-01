import os
import sys
import shutil
import requests
import datetime
from urllib import request
from bs4 import BeautifulSoup, element

from PyQt4.QtCore import *
from PyQt4.QtGui import *

try:
	test = QString('Test')
except NameError:
	print('QString Import Failed')
	QString = str


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
					for data in res.iter_content():
						dl += len(data)
						f.write(data)

class window(QMainWindow):
	def __init__(self, parent=None):
		QMainWindow.__init__(self, parent)

		self.dim = (850, 500)
		self.audio = dict(base = 'http://www.supremecourt.gov/oral_arguments/argument_audio/',
			 	 		  media = 'http://www.supremecourt.gov/media/audio/mp3files/')
		self.slipBase = 'http://supremecourt.gov/opinions/slipopinion/'
		self.saveDir = os.getcwd() + '\\SCOTUS\\'

		self.thread = worker()
		self.connect(self.thread, SIGNAL('output(QString)'), self.sendMessage)

		self.logName = sys.argv[0][2:-3] + '.log'
		if self.logName in os.listdir():
			self.log = open(self.logName, 'a')
		else:
			self.log = open(self.logName, 'w')

		self.initUI()
	def initUI(self):
		self.setWindowTitle('Scotus Scraper')
		self.setWindowIcon(QIcon('Seal.png'))

		grid = QGridLayout()

		self.con = QTextEdit(self)
		self.con.setReadOnly(True) 
		self.con.setAcceptRichText(False)

		if not os.path.exists(self.saveDir):
			self.sendMessage('No save directory')
			try:
				os.makedirs(self.saveDir)
			except :
				self.sendMessage('Problem making save directory')
				sys.exit(-1)
			else:
				self.sendMessage('Save directory created: {}'.format(self.saveDir))

		for year in range(2010, 2016):
			yearButton = QPushButton(str(year), self)
			yearButton.connect(yearButton, SIGNAL('clicked()'), self.yearButtonPress)
			grid.addWidget(yearButton, grid.rowCount(), 0)

		r = grid.rowCount()

		clearConButton = QPushButton('Clear Console', self)
		clearConButton.connect(clearConButton, SIGNAL('clicked()'), self.clearConsole)
		grid.addWidget(clearConButton, r + 40, 0)

		cancelButton = QPushButton('Cancel Download', self)
		cancelButton.connect(cancelButton, SIGNAL('clicked()'), self.cancelDownload)
		grid.addWidget(cancelButton, r + 41, 0)

		cleanButton = QPushButton('Clean', self)
		cleanButton.connect(cleanButton, SIGNAL('clicked()'), self.clean)
		grid.addWidget(cleanButton, r + 42, 0)

		clearLogButton = QPushButton('Clear Log File', self)
		clearLogButton.connect(clearLogButton, SIGNAL('clicked()'), self.clearLog)
		grid.addWidget(clearLogButton, r + 43, 0)
		
		grid.addWidget(self.con, 1, 1, grid.rowCount(), 1)

		grid.setColumnStretch(0, 1)
		grid.setColumnStretch(1, 2)

		self.mainWidget = QWidget(self)
		self.mainWidget.setLayout(grid)
		self.setCentralWidget(self.mainWidget)

		self.statusBar().showMessage('Ready')

		self.sendMessage('Opening')

		self.resize(*self.dim)
		self.center()
		self.show()
	def closeEvent(self, event):
		self.sendMessage('Closing')
		self.log.close()
		event.accept()
	def center(self):
		qr = self.frameGeometry()
		cp = QDesktopWidget().availableGeometry().center()
		qr.moveCenter(cp)
		self.move(qr.topLeft())
	def clean(self):
		if os.path.exists(self.saveDir):
			if not os.listdir(self.saveDir):
				self.sendMessage('Nothing to clean')
				return 0
			for file in os.listdir(self.saveDir):
				filePath = os.path.join(self.saveDir, file)
				try:
					if os.path.isfile(filePath):
						os.unlink(filePath)
						self.sendMessage('Deleted file: {}'.format(filePath))
					elif os.path.isdir(filePath):
						shutil.rmtree(filePath)
						self.sendMessage('Deleted folder: {}'.format(filePath))
				except Exception as e:
					print(e)			
			if os.listdir(self.saveDir):
				self.sendMessage('Problem cleaning {}'.format(self.saveDir))
		else:
			self.sendMessage('Directory not found: {}'.format(self.saveDir))
	def cancelDownload(self):
		self.sendMessage('Stopping Download')
		self.thread.exiting = True
	def clearLog(self):
		self.log.close()
		self.log = open(self.logName, 'w')
		self.sendMessage('Log Cleared')
	def sendMessage(self, msg):
		msg = str(msg)
		self.con.append('-> {}'.format(msg))
		sys.stdout.write('{}\n'.format(msg))
		sys.stdout.flush()
		now = datetime.datetime.now().strftime('%c')
		self.log.write('{} {}\n'.format(now, msg))
		self.log.flush()
	def clearConsole(self):
		self.sendMessage('Console Cleared')
		self.con.clear()
	def updateDownloadProgress(self, val):
		msg = '[{}{}]'.format(('=' * val), ('  ' * (50 - val)))
		self.statusBar().showMessage(msg)
	def removeNotAllowedChars(self, inp):
		for c in ('<','>',':','"','/','\\','|','?','*'):
			inp = inp.replace(c, '')
		return inp
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
			self.getArguemntAudio(year)
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
			name = audioDir + self.removeNotAllowedChars(d + '-' + n) + '.mp3'
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
			name = slipDir + self.removeNotAllowedChars(d + '-' + n) + '.pdf'
			slipFilenames.append(name)
		slipPair = [(i, j) for i, j in zip(slipURLs, slipFilenames)]
		self.thread.download(slipPair)

def main():
	app = QApplication(sys.argv)
	w = window()
	sys.exit(app.exec_())

if __name__ == '__main__':
	main() 