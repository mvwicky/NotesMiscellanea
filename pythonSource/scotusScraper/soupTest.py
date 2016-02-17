from bs4 import BeautifulSoup
from urllib import request 
import os
import sys

years = [i for i in range(2010, 2016)]
username = 'michael.vanwickle'
execdir = 'c:\\Users\\' + username + '\\Documents\\SCOTUS\\'
if not os.path.exists(execdir):
	os.makedirs(execdir)

for year in years:
	baseurl = 'http://www.supremecourt.gov/oral_arguments/argument_audio/' + str(year)
	base = BeautifulSoup(request.urlopen(baseurl), 'lxml')

	d = execdir + str(year) + '\\'
	if not os.path.exists(d):
		os.makedirs(d)

	aLinks = []
	for l in base.find_all('a'):
		link = str(l.get('href'))
		if '../audio/' in link:
			aLinks.append(link) # get links
			

	pre = len('../audio/' + str(year) + '/') # ../audio/year/ prefix length
	caseNum = [i[pre:] for i in aLinks] # get case numbers


	for c in caseNum:
		filename = d + c + '.mp3'
		url = 'http://www.supremecourt.gov/media/audio/mp3files/' + filename
		print(filename)
		#request.urlretrieve(url, filename)
