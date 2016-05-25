import os
import sys
import socket
import hashlib
import argparse

import logger


def md5_file(file_path):
    m = hashlib.md5()
    with open(file_path, 'rb') as file:
        cts = file.read(1024)
        while cts:
            m.update(cts)
            cts = file.read(1024)
    return str(m.hexdigest())


def main():
    logger_file_name = ''.join([logger.__name__, '.py'])
    if not os.path.exists(logger_file_name):
        print('Master logger module not found')
        return -1
    master_logger_path = os.path.realpath(logger_file_name)
    print(master_logger_path)
    dirs = list(filter(os.path.isdir, os.listdir('.')))
    while dirs:
        elem = dirs.pop()
        if 'logger.py' in os.listdir(elem):
            elem_path = os.path.realpath(elem)
            child_logger_path = os.path.join(elem_path, logger_file_name)
            if md5_file(master_logger_path) != md5_file(child_logger_path):
                try:
                    os.unlink(child_logger_path)
                except:
                    print('Logger in {} delete failed'.format(elem_path))
                    continue
                else:
                    print('Logger in {} deleted, replacing'.format(elem_path))
                    with open(master_logger_path, 'r') as master:
                        try:
                            child = open(child_logger_path, 'w')
                        except PermissionError as e:
                            print(e)
                            continue
                        else:
                            with child:
                                child.write(master.read())
                    print('Logger in {} replaced'.format(elem_path))
            else:
                print('Logger in {} matches the master'
                      .format(child_logger_path))

if __name__ == '__main__':
    main()
