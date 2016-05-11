import os
import sys

from multiprocessing import Queue, Process

import requests
from bs4 import BeautifulSoup, SoupStrainer

from logger import Logger


def download_func(func, q_in, q_out):
    while True:
        i, x = q_in.get()
        if i is None:
            break
        q_out.put((i, func(x)))


def download(arg):
    with open(arg[1], 'wb') as file:
        res = requests.get(arg[0], stream=True)
        if res.headers.get('content-length') is None:
            file.write(res.content)
        else:
            for data in res.iter_content():
                file.write(data)
    return 0


class Downloader(object):
    def __init__(self, in_file, out_path, nprocs=2):
        self.log = Logger('RetroSheet Downloader')
        self.nprocs = nprocs
        self.in_file = in_file
        self.out_path = os.path.normpath(out_path)
        self.queue = Queue()

    def parse_and_download(self):
        self.parse()
        [self.queue.put(None) for _ in range(self.nprocs)]

        procs = [Process(target=self.download) for _ in range(self.nprocs)]

        for proc in procs:
            proc.start()

        [proc.join() for proc in procs]
        return 0

    def parse(self):
        with open(self.in_file) as file:
            for row in file:
                link = row.replace('\n', '')
                file_path = os.path.join(self.out_path, link.split('/')[-1])
                pair = (link, file_path)
                self.queue.put(pair)
                self.log('{} put into queue'.format(pair))

    def download(self):
        while True:
            arg = self.queue.get()
            if arg is None:
                break
            self.log('Getting: {}'.format(arg[0]))
            with open(arg[1], 'wb') as file:
                res = requests.get(arg[0], stream=True)
                if res.headers.get('content-length') is None:
                    file.write(res.content)
                else:
                    for data in res.iter_content():
                        file.write(data)
            self.log('{} written'.format(arg[1]))
        self.log('Downloads Complete')


class RetroSheet(object):
    def __init__(self, out_file):
        self.log = Logger('RetroSheet')
        self.out_file = out_file
        self.out_path = os.path.abspath(out_file)

    def get_play_by_play(self):
        self.log('File Name: {}'.format(self.out_file))
        url = 'http://www.retrosheet.org/game.htm'
        self.log('URL: {}'.format(url))
        res = requests.get(url)
        self.log('Status Code: {}'.format(res.status_code))
        if res.status_code == 404:
            self.log('Got 404!', ex=True, exit_code=404)
        soup = BeautifulSoup(res.content, 'lxml')
        with open(self.out_path, 'w') as out:
            for a in soup('a'):
                if a.get('href'):
                    link = a.get('href')
                    if link.endswith('eve.zip'):
                        if not link.endswith('seve.zip'):
                            out.write(link)
                            out.write('\n')
                            self.log('Link: {}'.format(link))


def main():
    retro = RetroSheet('retrosheet.txt`')
    retro.get_play_by_play()
    dl = Downloader(retro.out_path, 'E:\\retrosheet')
    dl.parse_and_download()

if __name__ == '__main__':
    main()
