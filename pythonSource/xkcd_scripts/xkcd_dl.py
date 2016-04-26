import os
import sys

import multiprocessing as mp

from argparse import ArgumentParser

import requests

from PIL import Image
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

        self.queue = mp.Queue()

        if not os.path.exists(self.save_path):
            try:
                os.makedirs(os.path.abspath(self.save_path))
            except:
                self.log('Could not create save folder')
                return -1
            else:
                self.log('Folder Created: {}'
                         .format(os.path.abspath(self.save_path)))

    @staticmethod
    def fmt_name(inp):
        not_allowed_chars = '<>:"/\\|?*'  # Explicity not allowed characters
        for char in not_allowed_chars:
            inp = inp.replace(char, '')
        for char in ', ':  # I personally don't want these
            inp = inp.replace(char, '')
        return inp

    @staticmethod
    def size_msg(size_bytes):
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

    def mp_parse_and_download(self, nprocs=2):
        self.mp_parse()
        [self.queue.put(None) for _ in range(nprocs)]

        self.log('Done parsing, starting downloads')

        procs = [mp.Process(target=self.mp_download) for _ in range(nprocs)]

        for proc in procs:
            proc.start()

        [proc.join() for proc in procs]
        return 0

    def mp_parse(self):
        num = 1
        while True:
            url = ''.join([self.base_url, str(num), '/'])
            res = requests.get(url)
            if res.status_code == 404 and num != 404:
                self.log('Status Code: 404, breaking loop')
                break
            soup = BeautifulSoup(res.content, 'lxml',
                                 parse_only=SoupStrainer('div', id='comic'))
            for elem in soup('img'):
                if 'comics' in elem.get('src'):
                    comic_url = ''.join(['http:', elem.get('src')])
                    file_name = 'xkcd_{}.png'.format(num)
                    file_path = os.path.join(self.save_path, file_name)
                    pair = (comic_url, file_path)
                    self.queue.put(pair)
                    self.log('{} put into queue'.format(pair))
            num += 1
        self.queue.put(None)

    def mp_download(self):
        while True:
            arg = self.queue.get()
            if arg is None:
                break
            self.log('Getting {}'.format(arg[0]))
            with open(arg[1], 'wb') as comic:
                res = requests.get(arg[0], stream=True)
                if res.headers.get('content-length') is None:
                    comic.write(res.content)
                else:
                    for data in res.iter_content():
                        comic.write(data)
            self.log('{} written'.format(arg[1]))
        self.log('Downloads Complete')

    def download_comic(self, comic):
        self.log('Getting comic: {}'.format(comic))
        url = ''.join([self.base_url, str(comic), '/'])
        res = requests.get(url)
        if res.status_code != 404:
            soup = BeautifulSoup(res.content, 'lxml',
                                 parse_only=SoupStrainer('div', id='comic'))
            for elem in soup('img'):
                img_url = ''.join(['http:', elem.get('src')])
                file_name = 'xkcd_{}.png'.format(num)
                file_path = os.path.join(self.save_path, file_name)
                self.log('{}, {}'.format(img_url, file_path))
        else:
            self.log('Could not find comic {}'.format(comic), ex=True)
        msg_tup = (img_url.replace('http://', ''), file_name)
        msg = ' -> '.join(msg_tup)
        self.log(msg)
        with open(file_path, 'wb') as file:
                res = requests.get(img_url, stream=True)
                if not res.headers.get('content-length'):
                    file.write(res.content)
                else:
                    total_size += float(res.headers.get('content-length'))
                    for data in res.iter_content():
                        file.write(data)
                    ts_msg = self.size_msg(total_size)
                    self.log('Total Data Downloaded: {}'.format(ts_msg))

    def get_title_text(self, comic):
        url = ''.join([self.base_url, str(comic), '/'])
        res = requests.get(url)
        if res.status_code != 404:
            soup = BeautifulSoup(res.content, 'lxml',
                                 parse_only=SoupStrainer('div', id='comic'))
            for elem in soup('img'):
                title_text = elem.get('title')
            return self.fmt_name(title_text)
        else:
            self.log('Could not find comic {}'.format(comic), ex=True)

    def get_title(self, comic):
        url = ''.join([self.base_url, str(comic), '/'])
        res = requests.get(url)
        if res.status_code != 404:
            soup = BeautifulSoup(res.content, 'lxml',
                                 parse_only=SoupStrainer('div', id='comic'))
            for elem in soup('img'):
                title = elem.get('alt')
            return self.fmt_name(title)
        else:
            self.log('Could not find comic {}'.format(comic), ex=True)

    def make_image(self, comic):
        file_path = 'xkcd_{}.png'.format(comic)
        if not os.path.exists(file_path):
            self.download_comic(comic)

    def clean(self):
        pass


def main():
    dl = xkcd_dl()
    dl.mp_parse_and_download(4)


if __name__ == '__main__':
    main()
