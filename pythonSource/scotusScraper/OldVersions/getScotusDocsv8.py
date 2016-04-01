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

class DocDialog(QDialog):
	'''shows a dialog allowing the user to choose which documents to fetch'''
	def __init__(self, parent=None):
		QDialog.__init__(self, parent)
		self.init_ui()
	def init_ui(self):
		self.setWindowTitle(' ')
		self.setWindowIcon(QIcon('Seal.png'))
		layout = QHBoxLayout(self)

		audio_button = QPushButton('Argument Audio', self)
		slip_button = QPushButton('Slip Opinions', self)
		trans_button = QPushButton('Argument Transcript', self)
		all_button = QPushButton('All', self)

		audio_button.connect(audio_button, SIGNAL('clicked()'), self.accept)
		slip_button.connect(slip_button, SIGNAL('clicked()'), self.accept)
		trans_button.connect(trans_button, SIGNAL('clicked()'), self.accept)
		all_button.connect(all_button, SIGNAL('clicked()'), self.accept)

		layout.addWidget(audio_button)
		layout.addWidget(slip_button)
		layout.addWidget(trans_button)
		layout.addWidget(all_button)

		self.ret = 'Cancel'
	def accept(self):
		self.ret = self.sender().text()
		super(DocDialog, self).accept()
	@staticmethod
	def dec_ret(parent=None):
		dialog = DocDialog(parent)
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
					fmt_len = '{}K'.format(float(res.headers.get('content-length')) / 1000)
					self.emit(SIGNAL('output(QString)'), QString('Total Length: {}').format(fmt_len))
					for data in res.iter_content():
						f.write(data)
				self.emit(SIGNAL('output(QString)'), QString('Saved to: {}'.format(arg[1])))
		self.emit(SIGNAL('output(QString)'), QString('Download of {} files completed'.format(len(self.arg))))

class window(QMainWindow):
	def __init__(self, parent=None):
		QMainWindow.__init__(self, parent)
		self.dim = (850, 500)

		self.base_url = 'http://supremecourt.gov/' # The url of the supreme court site
		self.trans_base = '{}oral_arguments/'.format(self.base_url) # url to find transcripts
		self.save_dir = '{}\\SCOTUS\\'.format(os.getcwd()) # the base directory where files are saved

		self.downloader = downloader() 
		self.connect(self.downloader, SIGNAL('output(QString)'), self.send_message)

		script_name = (sys.argv[0].split('\\')[-1]).replace('.py', '.log')
		log_dir = '{}\\logs\\'.format(os.getcwd())
		self.log_name = '{}{}'.format(log_dir,script_name)
		if not os.path.exists(log_dir):
			try:
				os.makedirs(log_dir)
			except:
				err_log = logger('ErrorLog')
				err_log('Problem making log directory', ex=True, exitCode=-1)

		self.init_ui()
	def init_ui(self):
		self.setWindowTitle('Scotus Scraper')
		self.setWindowIcon(QIcon('Seal.png'))
		grid = QGridLayout()

		self.con = QTextEdit(self)
		self.con.setReadOnly(True) 
		self.con.setAcceptRichText(False)

		if not os.path.exists(self.save_dir):
			self.send_message('No save directory')
			try:
				os.makedirs(self.save_dir)
			except :
				self.send_message('Problem making save directory')
				sys.exit(-1)
			else:
				self.send_message('Save directory created: {}'.format(self.save_dir))

		for year in range(2010, 2016):
			year_button = QPushButton(str(year), self)
			year_button.connect(year_button, SIGNAL('clicked()'), self.year_button_press)
			grid.addWidget(year_button, grid.rowCount(), 0)

		r = grid.rowCount()

		clear_con_button = QPushButton('Clear Console', self)
		cancel_button = QPushButton('Cancel Download', self)
		clean_button = QPushButton('Clean', self)
		clear_log_button = QPushButton('Clear Log File', self)

		clear_con_button.connect(clear_con_button, SIGNAL('clicked()'), self.clear_console)
		cancel_button.connect(cancel_button, SIGNAL('clicked()'), self.cancel_download)
		clean_button.connect(clean_button, SIGNAL('clicked()'), self.clean)
		clear_log_button.connect(clear_log_button, SIGNAL('clicked()'), self.clear_log)

		buttons = [ clear_con_button, cancel_button,
				    clean_button, clear_log_button ]

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
		self.send_message('Opening')
		self.show()
	def closeEvent(self, event):
		self.send_message('Closing')
		self.downloader.quit()
		event.accept()
	def center(self):
		qr = self.frameGeometry()
		cp = QDesktopWidget().availableGeometry().center()
		qr.moveCenter(cp)
		self.move(qr.topLeft())
	def clean(self):
		if os.path.exists(self.save_dir):
			if not os.listdir(self.save_dir):
				self.send_message('Nothing to clean')
				return 0
			for file in os.listdir(self.save_dir):
				file_path = os.path.join(self.save_dir, file)
				try:
					if os.path.isfile(file_path):
						os.unlink(file_path)
						self.send_message('Deleted file: {}'.format(file_path))
					elif os.path.isdir(file_path):
						shutil.rmtree(file_path)
						self.send_message('Deleted folder: {}'.format(file_path))
				except Exception as e:
					print(e)			
			if os.listdir(self.save_dir):
				self.send_message('Problem cleaning {}'.format(self.save_dir))
		else:
			self.send_message('Directory not found: {}'.format(self.save_dir))
	def cancel_download(self):
		self.send_message('Stopping Download')
		self.downloader.exiting = True
	def clear_log(self):
		with open(self.log_name, 'w') as log:
			pass
		self.send_message('Log Cleared')
	def send_message(self, msg):
		msg = str(msg)
		self.statusBar().showMessage(msg)
		self.con.append('-> {}'.format(msg))
		sys.stdout.write('{}\n'.format(msg))
		sys.stdout.flush()
		now = datetime.datetime.now().strftime('%c')
		with open(self.log_name, 'a') as log:
			log.write('{} -> {}\n'.format(now, msg))
			log.flush()
	def clear_console(self):
		self.send_message('Console Cleared')
		self.con.clear()
	def update_download_progress(self, val):
		msg = '[{}{}]'.format(('=' * val), ('  ' * (50 - val)))
		self.statusBar().showMessage(msg)
	def remove_not_allowed_chars(self, inp):
		for c in ('<','>',':','"','/','\\','|','?','*'):
			inp = inp.replace(c, '')
		return inp
	def year_button_press(self):
		year = self.sender().text()
		year_dir = '{}{}\\'.format(self.save_dir, year)
		res = DocDialog.dec_ret()
		if 'Cancel' in res:
			return
		if not os.path.exists(year_dir):
			self.send_message('No directory for: {}'.format(year))
			try:
				os.makedirs(year_dir)
			except:
				self.send_message('Problem creating: {}'.format(year_dir))
				return 0
			else:
				self.send_message('Directory created: {}'.format(year_dir))
		if 'Audio' in res:
			self.get_argument_audio(year)
		elif 'Slip' in res:
			self.get_slip_opinions(year)
		elif 'Transcript' in res:
			self.get_argument_transcripts(year)
		elif 'All' in res:
			self.get_argument_audio(year)
			self.get_slip_opinions(year)
			self.get_argument_transcripts(year)
	def get_argument_audio(self, year):
		self.send_message('Getting argument audio')
		audio = { 'media'     : '{}media/audio/mp3files/'.format(self.base_url), # url where media files are stored
				  'dir'       : '{}{}\\Argument Audio\\'.format(self.save_dir, year),  # local directory to save the files
				  'url'       : '{}oral_arguments/argument_audio/{}'.format(self.base_url, year), # specific url for this year
				  'soup'      : '',
				  'links'     : [], 'dockets' : [], 'names' : [],
				  'filenames' : [], 'urls'    : [], 'pairs' : [] }	
		if not os.path.exists(audio['dir']):
			self.send_message('No directory for: {}'.format(audio['dir']))
			try: 
				os.makedirs(audio['dir'])
			except:
				self.send_message('Problem creating: {}'.format(audio['dir']))
				return 0
			else:
				self.send_message('Created: {}'.format(audio['dir']))
		audio['soup'] = BeautifulSoup(urllib.request.urlopen(audio['url']), 'lxml')
		for row in audio['soup'].find_all('tr'):
			for a in row.find_all('a', class_=None):
				if '../audio/' in a.get('href'):
					audio['links'].append(a.get('href')) # link is the href in the <a> tag
					audio['dockets'].append(a.string) # docket is the text inside the <a></a> block
					audio['names'].append(row.find('span').string) # case name is stored inside a span next to the <a>
		audio['urls'] = ['{}{}.mp3'.format(audio['media'], i) for i in audio['dockets']]
		for d, n in zip(audio['dockets'], audio['names']):
			name = '{}{}.mp3'.format(audio['dir'], self.remove_not_allowed_chars('{}-{}'.format(d, n)))
			audio['filenames'].append(name)
		audio['pairs'] = [(i, j) for i, j in zip(audio['urls'], audio['filenames'])]
		self.downloader(audio['pairs'])
	def get_slip_opinions(self, year):
		self.send_message('Getting slip opinions')
		year_dir = '{}{}\\'.format(self.save_dir, year)
		slip = { 'dir'       : '{}Slip Opinions\\'.format(yearDir), 
				 'url'       : '{}opinions/slipopinion/{}'.format(self.base_url, str(int(year) - 2000)), 
				 'soup'      : '',
				 'links'     : [],  'dockets' : [], 'names' : [],
				 'filenames' : [],  'urls'    : [], 'pairs' : [] }		
		if not os.path.exists(slip['dir']):
			self.send_message('No directory for: {}'.format(slip['dir']))
			try:
				os.makedirs(slip['dir'])
			except:
				self.send_message('Problem creating: {}'.format(slip['dir']))
				return 0
			else:
				self.send_message('Created: {}'.format(slip['dir']))
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
			name = '{}{}.pdf'.format(slip['dir'], self.remove_not_allowed_chars('{}-{}'.format(d, n)))
			slip['filenames'].append(name)
		slip['pairs'] = [(i, j) for i, j in zip(slip['urls'], slip['filenames'])]
		self.downloader(slip['pairs'])
	def get_argument_transcripts(self, year):
		self.send_message('Getting argument transcripts for {}'.format(year))
		trans = { 'dir'       : '{}{}\\Argument Transcripts\\'.format(self.save_dir, year),
				  'url'       : '{}oral_arguments/argument_transcript/{}'.format(self.base_url, year),
				  'soup'      : '',
				  'links'     : [], 'dockets' : [],'names': [], 'filenames' : [], 'pairs' : [] }
		if not os.path.exists(trans['dir']):
			self.send_message('No directory for: {}'.format(trans['dir']))
			try:
				os.makedirs(trans['dir'])
			except:
				self.send_message('Problem creating: {}'.format(trans['dir']))
				return 0 
			else:
				self.send_message('Created: {}'.format(trans['dir']))
		trans_url = '{}argument_transcript/{}'.format(self.trans_base, year)
		trans['soup'] = BeautifulSoup(urllib.request.urlopen(trans_url), 'lxml')
		for cell in trans['soup'].find_all('td'):
			for a in cell.find_all('a'):
				if 'argument_transcripts' in a.get('href'):
					link = a.get('href').replace('../', '')
					docket = (link.replace('argument_transcripts/', '')).replace('.pdf', '')
					trans['dockets'].append(docket)
					link = '{}{}'.format(self.trans_base, link)
					trans['links'].append(link)
					name = cell.find('span').string
					trans['names'].append(name)
					file_name = '{}{}{}'.format(trans['dir'], self.remove_not_allowed_chars('{}-{}'.format(docket, name)), '.pdf')
					trans['filenames'].append(file_name)
					trans['pairs'].append((link, file_name))
		self.downloader(trans['pairs'])


def main():
	app = QApplication(sys.argv)
	w = window()
	sys.exit(app.exec_())

if __name__ == '__main__':
	main() 