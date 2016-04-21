import os
import sys

from argparse import ArgumentParser

import requests

from bs4 import BeautifulSoup, SoupStrainer
from logger import Logger


class xkcd_dl(object):
    def __init__(self):
        self.log = Logger('xkcd_dl')
        parser = ArgumentParser()
        parser.add_argument('-n', '--number',
                            help='Comic number to get',
                            type=int)
        args = parser.parse_args()
        if args.number:
            self.num = args.number
        else:
            self.num = None
        self.pairs = []
        self.base_url = 'http://xkcd.com/'
        self.save_folder = 'xkcd'
        self.save_path = os.path.abspath(self.save_folder)

        if not os.path.exists(self.save_path):
            try:
                os.makedirs(os.path.abspath(self.save_path))
            except:
                self.log('Could not create save folder')
                return -1
            else:
                self.log('Folder Created: {}'
                         .format(os.path.abspath(self.save_path)))

    def fmt_name(self, inp):
        not_allowed_chars = '<>:"/\\|?*'  # Explicity not allowed characters
        for char in not_allowed_chars:
            inp = inp.replace(char, '')
        for char in ', ':  # I personally don't want these
            inp = inp.replace(char, '')
        return inp

    def size_msg(self, size_bytes):
        int_bytes = int(size_bytes)
        if int_bytes in range(0, 1000):
            return '{} bytes'.format(size_bytes)
        elif int_bytes in range(1001, int(1e6)):
            kb = size_bytes / 1000
            return '{}kB'.format(kb)
        elif int_bytes in range(int(1e6)+1, int(1e9)):
            mb = size_bytes / 1e6
            return '{}MB'.format(mb)
        elif int_bytes in range(int(1e9)+1, int(1e12)):
            gb = size_bytes / 1e9
            return '{}GB'.format(gb)
        else:
            return '{} bytes'.format(size_bytes)

    def parse(self):
        if self.num:
            self.log('Getting comic {}'.format(self.num))
        else:
            self.log('Getting all comics')
        self.pairs = []
        img = SoupStrainer('div', id='comic')
        num = self.num if self.num else 1
        url = ''.join([self.base_url, str(num), '/'])
        res = requests.get(url)
        while res.status_code != 404:
            soup = BeautifulSoup(res.content, 'lxml',
                                 parse_only=SoupStrainer('div', id='comic'))
            for elem in soup('img'):
                if 'comics' in elem.get('src'):
                    img_url = ''.join(['http:', elem.get('src')])
                    comic_name = self.fmt_name(elem.get('alt'))
                    file_name = 'xkcd_{}_{}.png'.format(num, comic_name)
                    file_path = os.path.join(self.save_path, file_name)
                    self.pairs.append((img_url, file_path))
                    self.log('{}, {}'.format(img_url, file_path))
            if self.num:
                break
            num += 1
            url = ''.join([self.base_url, str(num), '/'])
            res = requests.get(url)

    def download(self):
        assert self.pairs
        if self.num:
            print('Getting comic {}'.format(self.num))
        else:
            print('Getting {} comics'.format((len(pairs))))
        total_size = 0
        for pair in self.pairs:
            msg_tup = (pair[0].replace('http:', ''), os.path.split(pair[1])[1])
            msg = ' -> '.join(msg_tup)
            self.log(msg)
            with open(pair[1], 'wb') as comic:
                res = requests.get(pair[0], stream=True)
                if not res.headers.get('content-length'):
                    comic.write(res.content)
                else:
                    total_size += float(res.headers.get('content-length'))
                    for data in res.iter_content():
                        comic.write(data)
                    ts_msg = self.size_msg(total_size)
                    self.log('Total Data Downloaded: {}'.format(ts_msg))


def main():
    dl = xkcd_dl()
    dl.parse()
    dl.download()


if __name__ == '__main__':
    main()
