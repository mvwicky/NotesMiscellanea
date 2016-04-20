import os
import json
import socket
import argparse

import multiprocessing as mp
import threading as th


request_types = ('PATH_REQ', 'FILE_REQ', 'QUIT_REQ')


class query_server(object):
    def __init__(self, host, port, size=1024, backlog=5):
        assert isinstance(host, str)
        assert isinstance(port, int)
        self.host = host
        self.port = port
        self.size = size
        self.backlog = backlog

        self.path = None
        self.path_contents = []
        self.client = None
        self.address = None

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind((self.host, self.port))
        self.sock.listen(self.backlog)

    def loop(self):
        while True:
            self.client, self.address = self.sock.accept()
            req = self.client.recv(self.size).decode()

            if 'PATH_REQ' in req:
                print('PATH CONTENTS REQUEST RECEIVED')
                self.get_path_contents()
            elif 'FILE_REQ' in req:
                print('FILE REQUEST RECEIVED')
                self.get_file()
            elif 'QUIT_REQ' in req:
                print('QUIT REQUEST RECEIVED')
                self.client.send('ACK'.encode())
                self.client.close()
                break
            else:
                print('Request not recognized...')
            self.client.close()

    def get_path_contents(self):
        self.client.send('ACK'.encode())
        path = self.client.recv(self.size).decode()
        if os.path.exists(path):
            self.path = path
            self.client.send('RTS'.encode())

            ack_rts = self.client.recv(self.size)

            len_msg = str(len(os.listdir(self.path))).encode()
            self.client.send(len_msg)

            len_ack = self.client.recv(self.size)

            cts_msg = ','.join(os.listdir(self.path)).encode()
            self.client.send(cts_msg)
            print('Sent contents of: {}'.format(os.path.normpath(self.path)))

            ack = self.client.recv(self.size)
            self.path_contents = os.listdir(self.path)
            return 0
        else:
            self.client.send('NAK'.encode())
            print('Path not found')
            return -1

    def get_file(self):
        if not self.path_contents:
            self.client.send('NAK'.encode())
            return -1
        self.client.send('ACK'.encode())
        file = self.client.recv(self.size).decode()
        file_path = os.path.join(self.path, file)
        if os.path.exists(file_path) and file in os.listdir(self.path):
            self.client.send('RTS'.encode())

            ack_rts = self.client.recv(self.size)

            len_msg = str(os.path.getsize(file_path)).encode()
            self.client.send(len_msg)

            len_ack = self.client.recv(self.size).decode()
            if 'LEN_ACK' not in len_ack:
                print('Length not acked')
                return -1

            print('Sending File')
            with open(file_path, 'rb') as file:
                f_cts = file.read(self.size)
                while f_cts:
                    self.client.send(f_cts)
                    f_cts = file.read(self.size)
            ack_msg = self.client.recv(self.size)
            return 0
        else:
            self.client.send('NAK'.encode())
            return -1


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--config',
                        help='Path to config file',
                        type=str)

    args = parser.parse_args()

    if args.config:
        if not os.path.exists(args.config):
            print('File not found')
            return -1
        if not args.config.endswith('.json'):
            print('Config file must be json')
            return -1
        config_json = args.config
    else:
        config_json = 'server_config.json'
        print('Using default config file')
        print('Using {}'.format(config_json))

    with open(config_json) as cfg:
        config = json.load(cfg)

    host = config['hostname']
    port = int(config['port'])
    print('({host}, {port})'.format(host=host, port=port))

    query = query_server(host, port)
    query.loop()

if __name__ == '__main__':
    main()
