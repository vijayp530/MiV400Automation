import os.path
import time
import sys
import tempfile
from os import path
import pdb, sys;

source = os.path.dirname("C:\Robot_Framework\Desktop-Automation\TestCases\\")
source = os.path.join(source,'log.html')

class MyListner:
    ROBOT_LISTENER_API_VERSION = 2

    def __init__(self, filename='listen.txt'):
        self.ROBOT_LIBRARY_LISTENER = self

    def log_file(self,source):
        if os.path.isfile(source):
            time.sleep(7)
            timestr = time.strftime("%Y%m%d-%H%M%S")
            newname = 'log_' + timestr + '.html'
            #rename the original file as log_YYYYMMDD-HrsMinSec
            os.rename(source, newname)