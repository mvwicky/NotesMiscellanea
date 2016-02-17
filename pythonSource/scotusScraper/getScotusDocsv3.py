from bs4 import BeautifulSoup, element
from urllib import request
import requests
import multiprocessing as mp 
import os
import sys 

def removeNotAllowedChars(inp):
	for c in ('<','>',':','"','/','\\','|','?','*'):
		inp = inp.replace(c, '')
	return inp

def fmtName(name, docket, ext, maxLen=80):
	pass 

class case:
	def __init__(self, audioFilename, audioURL, slipFilename, slipURL, 
				       year, docket, name):
		self.audioFilename = audioFilename 
		self.audioURL = audioURL
		self.slipFilename = slipFilename
		self.slipURL = slipURL
		self.year = int(year)
		self.docket = str(docket)
		self.name = str(name)
	def getAudio(self):
		with open(self.audioFilename, 'wb') as f:
			print("Downloading {}".format(self.audioFilename))
			res = requests.get(self.audioURL, stream=True)
			totalLength = res.headers.get('content-length')
			if totalLength is None:
				f.write(res.content)
			else:
				dl = 0
				totalLength = int(totalLength)
				for data in res.iter_content():
					dl += len(data)
					f.write(data)
					done = int(50 * dl / totalLength)
					sys.stdout.write("\r[%s%s]" % ('=' * done, ' ' * (50 - done)))
					sys.stdout.flush()
	def getSlip(self):
		with open(self.slipFilename, 'wb') as f:
			print("Downloading {}".format(self.slipFilename))
			res = requests.get(self.slipURL, stream=True)
			totalLength = res.headers.get('content-length')
			if totalLength is None:
				f.write(res.content)
			else:
				dl = 0
				totalLength = int(totalLength)
				for data in res.iter_content():
					dl += len(data)
					f.write(data)
					done = int(50 * dl / totalLength)
					sys.stdout.write("\r[%s%s]" % ('=' * done, ' ' * (50 - done)))
					sys.stdout.flush()	

def numFromDocket(docket):
	pass

def usage(scriptName):
	print("{} OPTION".format(scriptName))
	print("if OPTION is blank: get 2010 - 2015")
	print("if OPTION is in 2010-2015, get that year")
	sys.exit(-1)

def main():
	scriptName = sys.argv[0]
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
		yearDir = savedir + year + '\\'
		if not os.path.exists(yearDir):
			try:
				os.makedirs(yearDir)
			except:
				print("Problem Making: {}".format(yearDir))
				sys.exit(-1)

		print("Retrieving Documents for {}".format(year))

		print("Argument Audio")
		baseURL = audio['base'] + year # current base url

		baseSoup = BeautifulSoup(request.urlopen(baseURL), 'lxml')

		

		#audioLinks = []
		#for l in baseSoup.find_all('a'):
		#	link = str(l.get('href'))
		#	if '../audio/' in link:
		#		audioLinks.append(link)

		#audioNames = [] # names based on audio page HTML
		#for n in baseSoup.find_all('span'):
		#	n.string = str(n.string)
		#	if ' v. ' in n.string:
		#		audioNames.append(n.string.title().replace(' ', '')) # get case names


		audioDockets = []
		for row in baseSoup.find_all('tr'):
			for a in row.find_all('a', class_=None):
				link = a.get('href')
				if '../audio/' in link:
					print(link)


		prefixLength = len('../audio/' + year + '/') # length of ../audio/year/
		#audioDockets = [i[prefixLength:] for i in audioLinks] # form dockets by stripping ../audio/year/ from link

		print("Slip Opinions")
		baseURL = slipBase + str(int(year) - 2000)
		baseSoup = BeautifulSoup(request.urlopen(baseURL), 'lxml')
		
		slipLinks = []
		slipNames = [] # names based on slip page HTML
		for l in baseSoup.find_all('a'):
			link = str(l.get('href'))
			if '/opinions' in link and ' v. ' in l.string:
				slipLinks.append(link)
				slipNames.append(l.string.title().replace(' ', ''))

		slipLinks = []
		slipNames = []
		slipDockets = []
		for row in baseSoup.find_all('tr'):
			for cell in row.find_all('td', style="text-align: center;")[2::10]:
				docket = cell.string.replace(', ', '-').replace('.', '')
				if docket in audioDockets:
					slipDockets.append(docket)
		


					#for link in row.find_all('a'):
					#	print(link.get('href'))

		print(len(audioDockets))
		print(audioDockets)
		print(len(slipDockets))

		audioURLs = [audio['media'] + i + '.mp3' for i in audioDockets]
		#slipURLs_temp = ['http://supremecourt.gov' + i for i in slipLinks]
		

		slipURLs = []

if __name__ == '__main__':
	main() 