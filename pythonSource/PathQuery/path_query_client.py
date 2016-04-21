import os
import json
import socket
import argparse


class query_client(object):
    def __init__(self, host, port, path, size=1024):
        assert isinstance(host, str)
        assert isinstance(port, int)
        self.host = host
        self.port = port
        self.path = path
        self.size = size
        self.path_contents = []

    def get_path_contents(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((self.host, self.port))

        sock.send('PATH_REQ'.encode())
        init_ack = sock.recv(self.size).decode()
        if 'NAK' in init_ack:
            print('NAK received: Path does not exist...')
            sock.close()
            return -1

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

    def get_file(self, file_name):
        assert isinstance(file_name, str)
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((self.host, self.port))

        sock.send('FILE_REQ'.encode())
        req_ack = sock.recv(self.size).decode()
        if 'NAK' in req_ack:
            print('NAK received: Path not populated')
            sock.close()
            return -1

        sock.send(file_name.encode())

        rts_msg = sock.recv(self.size).decode()
        if 'RTS' in rts_msg:
            sock.send('ACK'.encode())

            len_msg = sock.recv(self.size)
            sock.send('LEN_ACK'.encode())

            print('Receiving File')
            with open(file_name, 'wb') as file:
                while True:
                    f_cts = sock.recv(self.size)
                    print('Received:', repr(f_cts.decode()))
                    if not f_cts:
                        break
                    file.write(f_cts)
                print('Done Writing')
                file.close()
            sock.send('ACK'.encode())
            sock.close()
            return 0
        elif 'NAK' in rts_msg:
            print('Not a valid file path')
            sock.close()
            return -1

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
    parser.add_argument('-f', '--file',
                        help='File to get from the server',
                        type=str)
    parser.add_argument('-q', '--quit',
                        help='Server quits after sending contents',
                        action='store_true')

    args = parser.parse_args()

    host = 'localhost'
    port = 50000
    print('({host}, {port})'.format(host=host, port=port))
    print(' ')

    query = query_client(host, port, args.path)
    query.get_path_contents()
    for elem in query.path_contents:
        print(elem)
    if args.file:
        query.get_file(args.file)
    if args.quit:
        query.close_server()


if __name__ == '__main__':
    main()
