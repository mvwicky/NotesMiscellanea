import os
import json


class FolderContents(object):
    def __init__(self, to_root):
        if to_root.endswith('/'):
            to_root = to_root[:len(to_root)-1]
        self.to_root = to_root

        files = []
        folders = []
        submodules = []
        for elem in os.listdir(self.to_root):
            path_to_elem = '{}/{}'.format(self.to_root, elem)
            if not elem.startswith('.'):
                if os.path.isfile(path_to_elem):
                    files.append(elem)
                if os.path.isdir(path_to_elem):
                    folders.append(elem)
        for folder in folders:
            path_to_folder = '{}/{}'.format(self.to_root, folder)
            elems = os.listdir(path_to_folder)
            if '.git' in elems:
                submodules.append(folder)
        self.contents = {'folders': folders,
                         'filesinroot': files,
                         'submodules': submodules}

if __name__ == '__main__':
    pass
