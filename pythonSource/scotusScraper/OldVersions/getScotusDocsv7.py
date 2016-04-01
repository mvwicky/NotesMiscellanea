import os
import sys
import shutil
import urllib
import datetime

import requests
from bs4 import BeautifulSoup

from PyQt4.QtCore import *
from PyQt4.QtGui import *

try:
	test = QString('Test')
except NameError:
	print('QString Import Failed')
	QString = str

class docDialog(QDialog):
	'''shows a dialog allowing the user to choose which documents to fetch'''
	def __init__(self, parent=None):
		QDialog.__init__(self, parent)
		self.initUI()
	def initUI(self):
		self.setWindowTitle(' ')
		self.setWindowIcon(QIcon('Seal.png'))
		layout = QHBoxLayout(self)

		audioButton = QPushButton('Argument Audio', self)
		slipButton = QPushButton('Slip Opinions', self)
		transButton = QPushButton('Argument Transcript', self)
		allButton = QPushButton('All', self)

		audioButton.connect(audioButton, SIGNAL('clicked()'), self.accept)
		slipButton.connect(slipButton, SIGNAL('clicked()'), self.accept)
		transButton.connect(transButton, SIGNAL('clicked()'), self.accept)
		allButton.connect(allButton, SIGNAL('clicked()'), self.accept)

		layout.addWidget(audioButton)
		layout.addWidget(slipButton)
		layout.addWidget(transButton)
		layout.addWidget(allButton)

		self.ret = 'Cancel'
	def accept(self):
		self.ret = self.sender().text()
		super(docDialog, self).accept()
	@staticmethod
	def decRet(parent=None):
		dialog = docDialog(parent)
		result = dialog.exec_()
		return dialog.ret

class downloader(QThread):
	'''downloads the requested documents'''
	def __init__(self, parent=None):
		QThread.__init__(self, parent)
		self.exiting = False 
		self.arg = None
	def __del__(self):
		self.exiting = True
		self.wait()
	def __call__(self, arg):
		'''arg: a list of tuples consisting of a url and a filename'''
		self.arg = arg 
		self.exiting = False 
		self.start()
	def run(self):
		self.emit(SIGNAL('output(QString)'), QString('Starting download of {} files'.format(len(self.arg))))
		for arg in self.arg:
			if self.exiting:
				self.emit(SIGNAL('output(QString)'), 'Cancelling download')
				return 0;
			with open(arg[1], 'wb') as f:
				res = requests.get(arg[0], stream=True)
				self.emit(SIGNAL('output(QString)'), QString('Downloading: {}'.format(arg[0])))
				if res.headers.get('content-length') is None:
					f.write(res.content)
				else:
					fmtLen = '{}K'.format(float(res.headers.get('content-length')) / 1000)
					self.emit(SIGNAL('output(QString)'), QString('Total Length: {}').format(fmtLen))
					for data in res.iter_content():
						f.write(data)
				self.emit(SIGNAL('output(QString)'), QString('Saved to: {}'.format(arg[1])))
		self.emit(SIGNAL('output(QString)'), QString('Download of {} files completed'.format(len(self.arg))))

class window(QMainWindow):
	def __init__(self, parent=None):
		QMainWindow.__init__(self, parent)
		self.dim = (850, 500)

		self.baseURL = 'http://supremecourt.gov/' 
		self.transBase = '{}oral_arguments/'.format(self.baseURL)
		self.saveDir = '{}\\SCOTUS\\'.format(os.getcwd())

		self.downloader = downloader() 
		self.connect(self.downloader, SIGNAL('output(QString)'), self.sendMessage)

		scriptName = (sys.argv[0].split('\\')[-1]).replace('.py', '.log')
		logDir = '{}\\logs\\'.format(os.getcwd())
		self.logName = '{}{}'.format(logDir,scriptName)
		if not os.path.exists(logDir):
			try:
				os.makedirs(logDir)
			except:
				errLog = logger('ErrorLog')
				errLog('Problem making log directory', ex=True, exitCode=-1)

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
		cancelButton = QPushButton('Cancel Download', self)
		cleanButton = QPushButton('Clean', self)
		clearLogButton = QPushButton('Clear Log File', self)

		clearConButton.connect(clearConButton, SIGNAL('clicked()'), self.clearConsole)
		cancelButton.connect(cancelButton, SIGNAL('clicked()'), self.cancelDownload)
		cleanButton.connect(cleanButton, SIGNAL('clicked()'), self.clean)
		clearLogButton.connect(clearLogButton, SIGNAL('clicked()'), self.clearLog)

		buttons = [ clearConButton, cancelButton,
				    cleanButton, clearLogButton ]

		for i, button in enumerate(buttons):
			grid.addWidget(button, r + (40 + i), 0)

		
		grid.addWidget(self.con, 1, 1, grid.rowCount(), 1)

		grid.setColumnStretch(0, 1)
		grid.setColumnStretch(1, 2)

		self.mainWidget = QWidget(self)
		self.mainWidget.setLayout(grid)
		self.setCentralWidget(self.mainWidget)
		self.resize(*self.dim)
		self.center()
		self.sendMessage('Opening')
		self.show()
	def closeEvent(self, event):
		self.sendMessage('Closing')
		self.downloader.quit()
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
		self.downloader.exiting = True
	def clearLog(self):
		with open(self.logName, 'w') as log:
			pass
		self.sendMessage('Log Cleared')
	def sendMessage(self, msg):
		msg = str(msg)
		self.statusBar().showMessage(msg)
		self.con.append('-> {}'.format(msg))
		sys.stdout.write('{}\n'.format(msg))
		sys.stdout.flush()
		now = datetime.datetime.now().strftime('%c')
		with open(self.logName, 'a') as log:
			log.write('{} -> {}\n'.format(now, msg))
			log.flush()
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
		yearDir = '{}{}\\'.format(self.saveDir, year)
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
		elif 'Transcript' in res:
			self.getArgumentTranscripts(year)
		elif 'All' in res:
			self.getArgumentAudio(year)
			self.getSlipOpinions(year)
			self.getArgumentTranscripts(year)
	def getArgumentAudio(self, year):
		self.sendMessage('Getting argument audio')
		audio = { 'media'     : '{}media/audio/mp3files/'.format(self.baseURL), # url where media files are stored
				  'dir'       : '{}{}\\Argument Audio\\'.format(self.saveDir, year),  # local directory to save the files
				  'url'       : '{}oral_arguments/argument_audio/{}'.format(self.baseURL, year), # specific url for this year
				  'soup'      : '',
				  'links'     : [], 'dockets' : [], 'names' : [],
				  'filenames' : [], 'urls'    : [], 'pairs' : [] }	
		if not os.path.exists(audio['dir']):
			self.sendMessage('No directory for: {}'.format(audio['dir']))
			try: 
				os.makedirs(audio['dir'])
			except:
				self.sendMessage('Problem creating: {}'.format(audio['dir']))
				return 0
			else:
				self.sendMessage('Created: {}'.format(audio['dir']))
		audio['soup'] = BeautifulSoup(urllib.request.urlopen(audio['url']), 'lxml')
		for row in audio['soup'].find_all('tr'):
			for a in row.find_all('a', class_=None):
				if '../audio/' in a.get('href'):
					audio['links'].append(a.get('href')) # link is the href in the <a> tag
					audio['dockets'].append(a.string) # docket is the text inside the <a></a> block
					audio['names'].append(row.find('span').string) # case name is stored inside a span next to the <a>
		audio['urls'] = ['{}{}.mp3'.format(audio['media'], i) for i in audio['dockets']]
		for d, n in zip(audio['dockets'], audio['names']):
			name = '{}{}.mp3'.format(audio['dir'], self.removeNotAllowedChars('{}-{}'.format(d, n)))
			audio['filenames'].append(name)
		audio['pairs'] = [(i, j) for i, j in zip(audio['urls'], audio['filenames'])]
		self.downloader(audio['pairs'])
	def getSlipOpinions(self, year):
		self.sendMessage('Getting slip opinions')
		yearDir = '{}{}\\'.format(self.saveDir, year)
		slip = { 'dir'       : '{}Slip Opinions\\'.format(yearDir), 
				 'url'       : '{}opinions/slipopinion/{}'.format(self.baseURL, str(int(year) - 2000)), 
				 'soup'      : '',
				 'links'     : [],  'dockets' : [], 'names' : [],
				 'filenames' : [],  'urls'    : [], 'pairs' : [] }		
		if not os.path.exists(slip['dir']):
			self.sendMessage('No directory for: {}'.format(slip['dir']))
			try:
				os.makedirs(slip['dir'])
			except:
				self.sendMessage('Problem creating: {}'.format(slip['dir']))
				return 0
			else:
				self.sendMessage('Created: {}'.format(slip['dir']))
		slip['soup'] = BeautifulSoup(urllib.request.urlopen(slip['url']), 'lxml')
		for row in slip['soup'].find_all('tr'):
			for a in row.find_all('a'):
				if '/opinions/{}pdf/'.format(str(int(year) - 2000)) in a.get('href'):
					if ' v. ' in a.string:
						slip['links'].append(a.get('href'))
						slip['names'].append(a.string)
						for cell in row.find_all('td')[2::10]:
							docket = cell.string.replace(', ', '-').replace('.', '')
							slip['dockets'].append(docket)
		slip['urls'] = ['http://supremecourt.gov{}'.format(i) for i in slip['links']]
		for d, n in zip(slip['dockets'], slip['names']):
			name = '{}{}.pdf'.format(slip['dir'], self.removeNotAllowedChars('{}-{}'.format(d, n)))
			slip['filenames'].append(name)
		slip['pairs'] = [(i, j) for i, j in zip(slip['urls'], slip['filenames'])]
		self.downloader(slip['pairs'])
	def getArgumentTranscripts(self, year):
		self.sendMessage('Getting argument transcripts for {}'.format(year))
		trans = { 'dir'       : '{}{}\\Argument Transcripts\\'.format(self.saveDir, year),
				  'url'       : '{}oral_arguments/argument_transcript/{}'.format(self.baseURL, year),
				  'soup'      : '',
				  'links'     : [], 'dockets' : [],'names': [], 'filenames' : [], 'pairs' : [] }
		if not os.path.exists(trans['dir']):
			self.sendMessage('No directory for: {}'.format(trans['dir']))
			try:
				os.makedirs(trans['dir'])
			except:
				self.sendMessage('Problem creating: {}'.format(trans['dir']))
				return 0 
			else:
				self.sendMessage('Created: {}'.format(trans['dir']))
		transURL = '{}argument_transcript/{}'.format(self.transBase, year)
		trans['soup'] = BeautifulSoup(urllib.request.urlopen(transURL), 'lxml')
		for cell in trans['soup'].find_all('td'):
			for a in cell.find_all('a'):
				if 'argument_transcripts' in a.get('href'):
					link = a.get('href').replace('../', '')
					docket = (link.replace('argument_transcripts/', '')).replace('.pdf', '')
					trans['dockets'].append(docket)
					link = '{}{}'.format(self.transBase, link)
					trans['links'].append(link)
					name = cell.find('span').string
					trans['names'].append(name)
					fileName = '{}{}{}'.format(trans['dir'], self.removeNotAllowedChars('{}-{}'.format(docket, name)), '.pdf')
					trans['filenames'].append(fileName)
					trans['pairs'].append((link, fileName))
		self.downloader(trans['pairs'])


def main():
	app = QApplication(sys.argv)
	w = window()
	sys.exit(app.exec_())

if __name__ == '__main__':
	main() 