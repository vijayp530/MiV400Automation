###############################################################################
## Module: log
## File name: log.py
## Description: Setting log handler is achieved in this class
##
##
##  -----------------------------------------------------------------------
##  Modification log:
##
##  Date        Engineer              Description
##  ---------   ---------      -----------------------
##  14-Aug-2014  VHA              Initial Version
###############################################################################

import os

from datetime import datetime
import LoggerModule
from utils.confMgr import confMgr

# Constants for the framework begin ----
#LOG_FILE = os.path.join('../reports', 'staf_server_' + datetime.now().strftime('%y%m%d%H%M%S') + '.log')
# Create reports folder if not exist
if not os.path.exists('../../reports'):
    os.makedirs('../../reports')

with open(os.path.join('../../reports', 'reports.log'), 'w') and open(os.path.join('../../reports', 'TestReport.out'), 'w'):
    pass
LOG_FILE = os.path.join('../../reports', 'staf_server.log')
REPORT_FILE = "../../reports/TestReport.out"
# Constants for the framework end ----


class log(object):
    mjLog = LoggerModule.LoggerModule()
    consHandlr = None
    fileHandlr = None
    rprtHandlr = None

    @staticmethod
    def setLogHandlers():
        log.consHandlr = log.mjLog.ConsoleLogWriter(confMgr.getConfigMap()['UI_lOG_LEVEL'], "", False) # param1: Log level, param2: Filter, param3: TimeOn?
        log.fileHandlr = log.mjLog.RotatingLogFileHandler(LOG_FILE, "a", confMgr.getConfigMap()['FILE_LOG_LEVEL'], "", False) # param1: logfile, param2: level, param3: filter
        log.rprtHandlr = log.mjLog.RotatingLogFileHandler(REPORT_FILE, "a", "debug", "TReport", False) # param1: logfile, param2: level, param3: filter        

    @classmethod
    def changeConsoleLogLevel(self, newLevel):
        log.mjLog.HandlerClose(log.consHandlr)
        log.consHandlr = log.mjLog.ConsoleLogWriter(newLevel, "", False)

    @classmethod
    def changeFileLogLevel(self, newLevel):
        log.mjLog.HandlerClose(log.fileHandlr)
        log.fileHandlr = log.mjLog.RotatingLogFileHandler(LOG_FILE, "w", newLevel, "", False)
        
if __name__ == "__main__":
    log.setLogHandlers()
