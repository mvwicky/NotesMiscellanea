import os
import sys
import shutil
import requests
import datetime
from urllib import request
from bs4 import BeautifulSoup, element

from PyQt4.QtCore import *
from PyQt4.QtGui import *

try:
    test = QString('Test')
except NameError:
    print('QString Import Failed')
    QString = str

class genScraper(QMainWindow):
    def __init__(self, parent=None):
        QMainWindow.__init__(self, parent)

        self.dim = (850, 500)

        self.setWindowTitle('Web Scraper')

        self.url, ok = QInputDialog.getText(self, 'Input Target URL','Target URL:')
        self.confirmURL()

        grid = QGridLayout()
        

        self.domainName, self.directory = self.confirmURL()

        


        self.show()
    def confirmURL(self):
        if 'http:' not in self.url:
            pass
        if 'www' not in self.url:
            pass
        if self.url[0:2] == 'www':
            self.url = 'http://' + self.url
    def parseURL(self):
        w = self.url.find('www.')
        while w == -1:
            self.confirmURL()
            w = self.url.find('www')
        tlds = ('.co', '.ru', '.net', '.org', '.gov', '.edu')
        for tld in tlds:
            c = self.url.find(tld, w)
            if c != -1:
                break
        domainName = self.url[w, c]
        lSlash = self.url.rfind('/')
        if lSlash == len(self.url) - 1:
            pass
        return 'domainName', 'directory'
def main():
    app = QApplication(sys.argv)
    scraper = genScraper()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()