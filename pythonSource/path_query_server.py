import os
import json
import socket
import argparse

import multiprocessing as mp
import threading as th


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

    backlog = 5
    size = 1024

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind((host, port))
    sock.listen(backlog)

    while True:
        client, address = sock.accept()
        msg = client.recv(size).decode()

        if 'PATH_REQ' in msg:
            print('PATH REQUEST RECEIVED')
            client.send('ACK'.encode())
            path = client.recv(size).decode()
            if os.path.exists(path):
                client.send('RTS'.encode())
                ack_msg = client.recv(size)

                len_msg = str(len(os.listdir(path))).encode()
                client.send(len_msg)

                len_ack = client.recv(size)

                msg = ','.join(os.listdir(path)).encode()
                client.send(msg)
                print('Sent contents of: {}'.format(os.path.normpath(path)))

                ack = client.recv(size).decode()
            else:
                client.send('Path not found'.encode())
                print('Path not found')
        elif 'QUIT_REQ' in msg:
            print('QUIT REQUEST RECEIVED')
            client.send('ACK'.encode())
            client.close()
            break
        client.close()

if __name__ == '__main__':
    main()
