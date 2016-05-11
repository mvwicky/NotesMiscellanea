import os
import sys
import shutil
import urllib
import datetime
import json

from HTMLGen import HTMLGen
from FolderContents import FolderContents

debug = True

div, span = ('div', 'span')


class GenReadme(object):
    def __init__(self, config):
        with open(config) as cfg:
            self.config = json.load(cfg)
        file_name = self.config['file_name']
        title = self.config['title']

        self.contents = FolderContents(self.config['to_root']).contents
        self.html = HTMLGen(file_name, title)
        self.write()

    def write(self):
        self.open_html()
        self.open_page()

        self.content()

        self.close_page()
        self.close_html()

    def open_html(self):
        res_names = self.config['resource_names']
        self.html.opening(res_names)

    def close_html(self):
        self.html.close_all_tags()
        self.html.close()

    def open_page(self):
        self.html.open_div(_id='container')
        self.html.open_div(_id='maindiv')

        page_header = self.config['page_header']
        ref = page_header.lower()
        ref = '#{}'.format(ref.replace(' ', ''))
        head_link = self.html.link(ref, text=page_header,
                                   new_line=False, as_string=True)
        self.html.header(1, text=head_link, close=True)
        desc = self.config['page_description']
        self.html.gen_tag(span, text=desc, close=True)
        self.html.br(2)

    def close_page(self):
        self.html.close_div()
        self.html.close_div()

    def content(self):
        headings = self.config['sub_headings']
        for heading in headings.keys():
            heading_id = heading.lower().replace(' ', '')
            self.html.open_div(_id=heading_id, _class='subzero')
            l = '#{}'.format(heading_id)
            heading_link = self.html.link(l, text=heading, _class='gen_link',
                                          new_line=False, as_string=True)
            self.html.header(2, text=heading_link, close=True)
            for sub in headings[heading]:
                sub_id = sub.lower().replace(' ', '')
                self.html.open_div(_class='subone', _id=sub_id)
                a_right = self.html.gen_tag(span, _class='arrow arrow_right',
                                            new_line=False, close=True,
                                            as_string=True)
                self.html.header(4, text=a_right)
                l = '#{}'.format(sub_id)
                self.html.link(l, text=sub, _class='top_link', new_line=False)
                self.html.close_header(4)

                self.html.list_open(_class='toplist')
                for elem in self.contents[sub_id]:
                    elem_id = elem.replace(' ', '')
                    li = self.html.gen_tag(span, text=elem, _id=elem_id,
                                           _class='sub_link', close=True,
                                           new_line=False, as_string=True)
                    self.html.list_element(text=li)

                    path_to_elem = '{}/{}'.format(self.config['to_root'], elem)
                    if os.path.isdir(path_to_elem):
                        elem_cts = [i for i in os.listdir(path_to_elem)
                                    if not i.startswith('.')]
                        self.html.list_open(_class='sublist', _id=elem_id)
                        for e in elem_cts:
                            li = self.html.gen_tag(span, text=e,
                                                   close=True, new_line=False,
                                                   as_string=True)
                            self.html.list_element(text=li)
                        self.html.list_close()
                self.html.list_close()
                self.html.close_div()
            self.html.close_div()


def main():
    readme = GenReadme('config.json')

if __name__ == '__main__':
    main()
