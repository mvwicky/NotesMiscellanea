from bs4 import BeautifulSoup
from urllib import request 
import os
import sys

def fmtName(name, num, maxLen=80, ext='.mp3'):
	name = str(name)
	num = str(num)
	ext = str(ext)
	extLen = len(ext) # number of characters in extension

	for c in ('<', '>', ':', '"', '/', '\\', '|', '?', '*'):
		name = name.replace(c, '')

	name = name.title().replace(' V. ', '_v_', 1)

	name = num + '-' + name 

	name = name[0  :maxLen - extLen] # clamp name to maxLen - extension length
	name = name + ext # add extension (len(eName) <= )
	name = name.replace(' ', '')

	return name

def main():
	#years = [i for i in range(2010, 2016)]
	years = [i for i in range(2010, 2011)]
	username = 'michael.vanwickle'
	execdir = 'c:\\Users\\' + username + '\\Documents\\SCOTUS\\'
	audiobase = 'http://www.supremecourt.gov/oral_arguments/argument_audio/'
	slipbase = 'http://supremecourt.gov/opinions/slipopinion/'

	if not os.path.exists(execdir):
		os.makedirs(execdir)

	for year in years:
		# argument audio
		print("Retrieving Documents for " + str(year))
		
		print("Argument Audio")
		baseurl = audiobase + str(year)
		base = BeautifulSoup(request.urlopen(baseurl), 'lxml')

		d = execdir + str(year) + '\\'
		if not os.path.exists(d):
			os.makedirs(d)

		aLinks = []
		for l in base.find_all('a'):
			link = str(l.get('href'))
			if '../audio/' in link:
				aLinks.append(link) # get links

		aNames = []
		for s in base.find_all('span'):
			name = str(s.string)
			if 'v.' in name:
				aNames.append(name)
			
		pre = len('../audio/' + str(year) + '/') # ../audio/year/ prefix length
		caseNum = [i[pre:] for i in aLinks] # get case numbers


		for num, name in zip(caseNum, aNames):
			url = 'http://www.supremecourt.gov/media/audio/mp3files/' + num + '.mp3'
			filename = d + fmtName(name, num, maxLen=80, ext='.mp3')
			#try: 
			#	request.urlretrieve(url, filename)
			#except:
			#	print("Problem Getting File")



		# get slip opinions
		print("Slip Opinions")
		baseurl = slipbase + str(year - 2000)
		base = BeautifulSoup(request.urlopen(baseurl), 'lxml')

		aLinks = []
		aNames = []
		for l in base.find_all('a'):
			link = str(l.get('href'))
			if '/opinions/' in link:
				if ' v. ' in l.string:
					aLinks.append(link)
					aNames.append(l.string)

		caseNum = []
		for t in base.find_all('td'):
			if len(str(t.string)) > 2 and len(str(t.string)) <= 12 and '/' not in str(t.string) and 'v.' not in str(t.string) and 'style' in t.attrs:
				caseNum.append(str(t.string))

		for num, name, link in zip(caseNum, aNames, aLinks):
			url = 'http://supremecourt.gov' + link
			filename = d + fmtName(name, num, maxLen=80, ext='.pdf')
			print(num, name)
			try: 
				request.urlretrieve(url, filename)
			except:
				print("Problem Getting File")

		


if __name__ == '__main__':
	main()
