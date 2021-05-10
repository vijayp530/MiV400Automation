__author__ = 'mkr'

import logging
import sys
import os
from datetime import datetime


class MyFormatter(logging.Formatter):

    info_fmt = err_fmt = "%(asctime)s - %(levelname)s - %(message)s"
    dbg_fmt = "%(asctime)s - %(filename)s:%(lineno)s - %(funcName)s() - %(levelname)s - %(message)s"



    def __init__(self, fmt="%(levelno)s: %(msg)s"):
        logging.Formatter.__init__(self, fmt)


    def format(self, record):

        # Save the original format configured by the user
        # when the logger formatter was instantiated
        format_orig = self._fmt

        # Replace the original format with one customized by logging level
        if record.levelno == logging.DEBUG:
            self._fmt = MyFormatter.dbg_fmt

        elif record.levelno == logging.INFO:
            self._fmt = MyFormatter.info_fmt

        elif record.levelno == logging.ERROR:
            self._fmt = MyFormatter.err_fmt

        # Call the original formatter class to do the grunt work
        result = logging.Formatter.format(self, record)

        # Restore the original format configured by the user
        self._fmt = format_orig

        return result

def get_logger(logFile=None, level='INFO'):
    level = getattr(logging, level)
    if not logFile:
        logFile = os.path.join(os.path.curdir, datetime.now().strftime('%y%m%d%H%M%S')+'.log')
    rootLogger = logging.getLogger('root')
    rootLogger.setLevel(level)
    logFormatter = MyFormatter()
    fileHandler = logging.FileHandler(logFile)
    fileHandler.setFormatter(logFormatter)
    rootLogger.addHandler(fileHandler)
    consoleHandler = logging.StreamHandler(sys.stdout)
    consoleHandler.setFormatter(logFormatter)
    rootLogger.addHandler(consoleHandler)
    return rootLogger