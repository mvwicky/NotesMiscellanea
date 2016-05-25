import os

import multiprocessing as mp

import requests

from logger import Logger


class Downloader(object):
    def __init__(self, name='Downloader', nprocs=2):
        self.name = name
        self.nprocs = nprocs
        self.log = Logger(name)
        self.exiting = False
        self.arg = None
        self.in_queue = mp.Queue(1)
        self.out_queue = mp.Queue()

    def __del__(self):
        self.exiting = True

    def __call__(self, arg):
        """ arg: list of tuples (url, filename) """
        self.arg = arg
        self.exiting = False
        self.download_par()

    def download_par(self):
        if not self.arg:
            self.log('No arguments received')
            return 0
        self.log('Starting download of {} files in {} threads'
                 .format(len(self.arg), self.nprocs))

        procs = [mp.Process(target=self.download_func)
                 for _ in range(self.nprocs)]

        for proc in procs:
            proc.start()

        sent = [self.in_queue.put((i, x)) for i, x in enumerate(self.arg)]
        [self.in_queue.put((None, None)) for _ in range(self.nprocs)]
        ret = [self.out_queue.get() for _ in range(len(sent))]

        [proc.join() for proc in procs]

        return [x for i, x in ret]

    def download_func(self):
        while True:
            arg = self.in_queue.get()
            tup = arg[1]
            if tup is None:
                break
            self.log('Getting: {}'.format(tup[0]))
            with open(tup[1], 'wb') as file:
                res = requests.get(tup[0])
                if res.headers.get('content-length') is None:
                    file.write(res.content)
                else:
                    for data in res.iter_content():
                        file.write(data)
            self.log('{} written'.format(tup[1]))
            self.out_queue.put((arg[0], True))
        self.log('Downloads Complete')
        return 0


if __name__ == '__main__':
    pa = os.path.realpath('patch.png')
    pa2 = os.path.realpath('bun.png')
    args = [('http://imgs.xkcd.com/comics/patch.png', pa),
            ('http://imgs.xkcd.com/comics/bun.png', pa2)]
    dl = Downloader()
    dl(args)
