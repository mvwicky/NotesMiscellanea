import os
import sys
import socket
import argparse

import logger


def main():
    logger_file_name = ''.join([logger.__name__, '.py'])
    if not os.path.exists(logger_file_name):
        print('Master logger module not found')
        return -1
    master_logger_path = os.path.abspath(logger_file_name)
    print(master_logger_path)
    for elem in filter(os.path.isdir, os.listdir('.')):
        if 'logger.py' in os.listdir(elem):
            elem_path = os.path.abspath(elem)
            child_logger_path = os.path.join(elem_path, logger_file_name)
            try:
                os.unlink(child_logger_path)
            except:
                print('Logger in {} delete failed'.format(elem_path))
                continue
            else:
                print('Logger in {} deleted, replacing'.format(elem_path))
                with open(master_logger_path, 'r') as master, \
                        open(child_logger_path, 'w') as child:
                    child.write(master.read())
                print('Logger in {} replaced'.format(elem_path))

if __name__ == '__main__':
    main()
