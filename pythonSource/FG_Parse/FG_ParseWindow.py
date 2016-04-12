import os
import sys
import shutil
import urllib
import typing
import datetime

import requests
from bs4 import BeautifulSoup

from PyQt4.QtCore import *
from PyQt4.QtGui import *

from FG_Parse import FG_Parser
from logger import Logger

try:
    test = QString('Test')
except NameError:
    QString = str