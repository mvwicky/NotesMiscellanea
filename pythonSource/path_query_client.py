import os
import json
import socket
import argparse


class path_query(object):
    def __init__(self, host, port, path, size=1024):
        assert isinstance(host, str)
        assert isinstance(port, int)
        self.host = host
        self.port = port
        self.size = size
        self.path = path
        self.path_contents = []

    def get_path_contents(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((self.host, self.port))

        sock.send('PATH_REQ'.encode())
        init_ack = sock.recv(self.size)

        sock.send(self.path.encode())

        rts_msg = sock.recv(self.size).decode()
        if 'RTS' in rts_msg:
            sock.send('ACK'.encode())

            len_msg = sock.recv(self.size).decode()
            if not len_msg.isnumeric():
                print('Problem getting length')
                sock.close()
                return -1
            sock.send('LEN_ACK'.encode())

            cts_str = sock.recv(self.size).decode()
            self.path_contents = cts_str.split(',')
            sock.send('ACK'.encode())
        else:
            print('Did not get a ready to send...')
            sock.close()
            return -1
        return 0

    def close_server(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((self.host, self.port))
        sock.send('QUIT_REQ'.encode())
        quit_ack = sock.recv(self.size).decode()
        if 'ACK' in quit_ack:
            print('Server quit successfully')
        elif 'NAK' in quit_ack:
            print('Problem quitting server')
        sock.close()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('path',
                        help='Path for the server to look at',
                        type=str)
    parser.add_argument('-c', '--config',
                        help='Path to config file',
                        type=str)
    parser.add_argument('-q', '--quit',
                        help='Server quits after sending contents',
                        action='store_true')

    args = parser.parse_args()

    if args.config:
        config_path = os.path.abspath(args.config)
        config_name = os.path.split(config_path)[1]
        if not os.path.exists(config_path):
            print('File not found')
            return -1
        if not config_name.endswith('.json'):
            print('Config file must be json')
            return -1
        config_json = config_path
    else:
        config_json = 'client_config.json'
        print('Using default config file')
    print('Config File: {}'.format(os.path.abspath(config_json)))

    with open(config_json) as cfg:
        config = json.load(cfg)

    host = config['hostname']
    port = int(config['port'])
    print('({host}, {port})'.format(host=host, port=port))
    print(' ')

    pq = path_query(host, port, args.path)
    pq.get_path_contents()
    for elem in pq.path_contents:
        print(elem)
    pq.close_server()


if __name__ == '__main__':
    main()
