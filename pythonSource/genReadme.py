import os
import sys
import shutil
import urllib
import typing
import datetime

debug = True

class HTMLGen(object):
	def __init__(self, file_name, title):
		self.open_tags = []
		self.indent = ''
		self.file_name = file_name
		self.title = title

	def increase_indent(self):
		return ''
		self.indent = '{}\t'.format(self.indent)
		return self.indent

	def decrease_indent(self):
		return ''
		ret = self.indent
		self.indent = self.indent[:-2]
		return ret

	def gen_tag(self, tag, text=None, _id=None, _class=None, new_line=True, indent=False, close=False, as_string=False):
		ret = []
		if indent:
			self.increase_indent()
		ret.append('{}<{}'.format(self.indent, tag))
		if _id is not None:
			ret.append(' id=\"{}\"'.format(_id))
		if _class is not None:
			ret.append(' class=\"{}\"'.format(_class))
		ret.append('>')
		if text is not None:
			ret.append(text)
		if close:
			ret.append('</{}>'.format(tag))
		if not close:
			self.open_tags.append(tag)
		if new_line and debug:
			ret.append('\r\n')
		ret = ''.join(ret)	
		if as_string:
			return ret
		with open(self.file_name, 'a') as html:
			html.write(ret)

	def close_tag(self, tag, new_line=True):
		with open(self.file_name, 'a') as html:
			html.write('{}</{}>'.format(self.decrease_indent(), tag))
			if new_line and debug:
				html.write('\r\n')
		self.open_tags.remove(tag)

	def close_all_tags(self):
		with open(self.file_name, 'a') as html:
			for tag in self.open_tags:
				html.write('{}</{}>\r\n'.format(self.decrease_indent(), tag))
		self.open_tags = []

	def link(self, href, text, _id=None, _class=None, new_line=True, indent=False, as_string=False):
		ret = []
		if indent:
			self.increase_indent()
		ret.append('{}<a href=\"{}\"'.format(self.indent, href))
		if _id is not None:
			ret.append(' id=\"{}\"'.format(_id))
		if _class is not None:
			ret.append(' class=\"{}\"'.format(_class))
		ret.append('>{}</a>'.format(text))
		if new_line and debug:
			ret.append('\r\n')
		ret = ''.join(ret)	
		if as_string:
			return ret
		with open(self.file_name, 'a') as html:
			html.write(ret)

	def br(self, num=1):
		with open(self.file_name, 'a') as html:
			for i in range(num):
				html.write('{}<br />\r\n'.format(self.indent))

	def list_open(self, ordered=False, _id=None, _class=None, new_line=True, indent=False, as_string=False):
		if ordered:
			tag = 'ol'
		else:
			tag = 'ul'
		ret = self.gen_tag(tag, None, _id, _class, new_line, indent, False, as_string)
		if ret is not None and as_string:
			return ret

	def list_close(self, ordered=False, new_line=True):
		if ordered:
			tag = 'ol'
		else:
			tag = 'ul'
		self.close_tag(tag, new_line)

	def list_element(self, text=None, _id=None, _class=None, new_line=True, indent=False, as_string=False):
		ret = self.gen_tag('li', text, _id, _class, new_line, indent, True, as_string)
		if ret is not None and as_string:
			return ret

	def header(self, level, text=None, _id=None, _class=None, new_line=True, indent=False, close=False, as_string=False):
		tag = 'h{}'.format(level)
		ret = self.gen_tag(tag, text, _id, _class, new_line, indent, close, as_string)
		if ret is not None and as_string:
			return ret

	def opening(self, file_paths=None):
		with open(self.file_name, 'w') as html:
			html.write('<!DOCTYPE html>\r\n')
			html.write('{}<head>\r\n'.format(self.increase_indent()))
			html.write('{}<title>{}</title>\r\n'.format(self.increase_indent(), self.title))
			if file_paths is not None:
				for path in file_paths:
					if path.find('.js') != -1:
						html.write('{}<script type=\"text/javascript\" src=\"{}\"></script>\r\n'.format(self.indent, path))
					elif path.find('.css') != -1:
						html.write('{}<link rel=\"stylesheet\" type=\"text/css\" href=\"{}\">\r\n'.format(self.indent, path))
			html.write('{}</head>\r\n'.format(self.decrease_indent()))
			html.write('{}<body>\r\n'.format(self.increase_indent()))

	def close(self):
		with open(self.file_name, 'a') as html:
			html.write('{}</body>\r\n'.format(self.decrease_indent()))
			html.write('{}</html>\r\n'.format(self.decrease_indent()))

def get_files():
	files = []
	for elem in os.listdir('..'):
		dot = elem.find('.')
		if dot != -1 and not elem.startswith('.'):
			files.append(elem)
	for i, file in enumerate(files):
		dot = file.find('.')
		if dot != -1:
			ext = file[dot+1:]
			files[i] = (file[:dot], ext)

	return files

def get_folders():
	folders = []
	for elem in os.listdir('..'):
		dot = elem.find('.')
		if dot == -1:
			folders.append(elem)
	return folders

def get_submodules():
	folders = get_folders()
	submodules = []
	for folder in folders:
		elems = os.listdir('../{}'.format(folder))
		if '.git' in elems:
			submodules.append(folder)
	return submodules

def main():
	root = get_files()
	folders = get_folders()
	submodules = get_submodules()

	readme_file = 'README_v3.html'
	files = ['../ReadmeRes/style.css',
			 '../ReadmeRes/jquery.min.js',
			 '../ReadmeRes/readme_v2.js']

	readme = HTMLGen(file_name=readme_file, title='Notes Miscellanea - Readme')
	readme.opening(file_paths=files)

	readme.gen_tag('div', _id='container')
	readme.gen_tag('div', _id='maindiv')
	readme.header(1, text=readme.link(href='#notesmiscellanea', text='Notes Miscellanea',new_line=False, as_string=True), close=True)
	readme.gen_tag('span', text='A repo of interesting (to me) documents', close=True)
	readme.br(num=2)

	readme.gen_tag('div', _id='contents', _class='subzero')
	readme.header(2, text=readme.link(href='#contents', text='Contents', _class='gen_link', new_line=False, as_string=True), close=True)

	readme.gen_tag('div', _class='subone', _id='folders')
	readme.header(4, text=readme.link(href='#folders', text='Folders', _class='top_link', new_line=False, as_string=True), close=True)
	readme.list_open(_class='toplist')
	for folder in folders:
		sub_folder = os.listdir('../{}'.format(folder))
		readme.list_element(text=readme.gen_tag(tag='span', text=folder, _id=folder.replace(' ',''), _class='sub_link', close=True, new_line=False, as_string=True))
		readme.list_open(_class='sublist', _id=folder.replace(' ', ''))
		for elem in sub_folder:
			readme.list_element(text=readme.gen_tag(tag='span', text=elem, close=True, new_line=False, as_string=True))
		readme.list_close()

	readme.list_close()
	readme.close_tag('div')

	readme.gen_tag('div', _class='subone', _id='filesinroot')
	readme.header(4, text=readme.link(href='#filesinroot', text='Files in Root', _class='top_link', new_line=False, as_string=True), close=True)
	readme.list_open(_class='toplist')
	for file in root:
		readme.list_element(text=readme.gen_tag(tag='span', text='{} ({})'.format(*file),  close=True , new_line=False, as_string=True))

	readme.list_close()
	readme.close_tag('div')

	readme.gen_tag('div', _class='subone', _id='submodules')
	readme.header(4, text=readme.link(href='#submodules', text='Submodules',_class='top_link', new_line=False, as_string=True), close=True)
	readme.list_open(_class='toplist')
	for module in submodules:
		module_name = module.replace(' ', '')
		readme.list_element(text=readme.gen_tag(tag='span', text=module, _id=module_name, _class='sub_link', close=True , new_line=False, as_string=True))
	readme.list_close()
	readme.close_tag('div')

	readme.close_all_tags()
	readme.close()

if __name__ == '__main__':
	main()