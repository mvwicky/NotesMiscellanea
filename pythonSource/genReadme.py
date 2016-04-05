import os
import sys
import shutil
import urllib
import typing
import datetime

class HTMLGen(object):
	def __init__(self):
		self.open_tags = []

def write_gen_tag(filename, tag, text=None, _id=None, _class=None):
	with open(filename, 'a') as f:
		f.write('<{}'.format(tag))
		if (_id is not None):
			f.write(' id=\"{}\"'.format(id))
		if (_class is not None):
			f.write(' class=\"{}\"'.format(_class))
		f.write('>')
		if (text is not None):
			f.write(text)
		f.write('</{}>'.format(tag))

def main():
	print(os.listdir('..'))
	readme = 'README_v3.html'
	with open(readme, 'w') as r:
		r.write('<!DOCTYPE html>\r\n<html>\r\n')
		r.write('\t<head>\r\n') # start head tag
		r.write('\t\t<title>Notes Miscellanea - Readme</title>\r\n')
		r.write('\t\t<link rel=\"stylesheet\" type=\"text/css\" href=\"../ReadmeRes/style.css\">\r\n')
		r.write('\t\t<script type=\"text/javascript\" src=\"../ReadmeRes/jquery.min.js\"></script>\r\n')
		r.write('\t\t<script type=\"text/javascript\" src=\"../ReadmeRes/readme_v2.js\"></script>\r\n')
		r.write('\t</head>\r\n') # end head tag
		r.write('\t<body>\r\n') # start body tag

		r.write('\t\t<div id=\"container\">\r\n')
		r.write('\t\t\t<div id=\"maindiv\">\r\n')
		r.write('<br /><br />\r\n')
		r.write('\t\t\t\t<div class=\"subzero\" id=\"contents\">\r\n')

		r.write('\t\t\t\t</div>\r\n')

		r.write('\t\t\t</div>\r\n')
		r.write('\t\t</div>\r\n')

		r.write('\t</body>\r\n')
		r.write('</html>')

if __name__ == '__main__':
	main()