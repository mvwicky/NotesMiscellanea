import json

from FolderContents import FolderContents 

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

	def gen_tag(self, tag, text=None, _id=None, _class=None, new_line=True,
				indent=False, close=False, as_string=False):
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

	def open_div(self, text=None, _id=None, _class=None, new_line=True, 
				 indent=False, close=False, as_string=False):
		ret = self.gen_tag('div', text, _id, _class, new_line, indent, 
						   close, as_string)
		if ret is not None and as_string:
			return ret

	def close_div(self, new_line=True):
		self.close_tag('div', new_line)

	def close_all_tags(self):
		with open(self.file_name, 'a') as html:
			for tag in self.open_tags:
				html.write('{}</{}>\r\n'.format(self.decrease_indent(), tag))
		self.open_tags = []

	def link(self, href, text, _id=None, _class=None, new_line=True, 
			 indent=False, as_string=False):
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

	def list_open(self, ordered=False, _id=None, _class=None, new_line=True, 
				  indent=False, as_string=False):
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

	def list_element(self, text=None, _id=None, _class=None, new_line=True, 
					 indent=False, as_string=False):
		ret = self.gen_tag('li', text, _id, _class, new_line, indent, True, as_string)
		if ret is not None and as_string:
			return ret

	def header(self, level, text=None, _id=None, _class=None, new_line=True, 
			   indent=False, close=False, as_string=False):
		tag = 'h{}'.format(level)
		ret = self.gen_tag(tag, text, _id, _class, new_line, indent, close, as_string)
		if ret is not None and as_string:
			return ret

	def close_header(self, level):
		self.close_tag('h{}'.format(level))

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

if __name__ == '__main__':
	pass