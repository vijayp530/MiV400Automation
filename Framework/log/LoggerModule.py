## Module: LoggerModule
## File name: LoggerModule.py
## Description: Creating Console Log and Rotating Log files for STAF tool.
##
##  -----------------------------------------------------------------------
##  Modification log:
##
##  Date        Engineer              Description
##  ---------   ---------      -----------------------
## 14 AUG 2014  VHA               Initial Version
###############################################################################


import logging.handlers
import os

class  LoggerModule():
   def __init__(self):
      pass
   
   def TimeFormatter(self):
       return logging.Formatter('%(asctime)-5s | %(name)-5s | %(levelname)-5s | %(message)s')    

   def ConsoleLogWriter(self,Loglevel="debug",Filt = "",DisplayTimeFormat = True):
       '''
        ConsoleLogWriter () will create handler to write log into console
       '''
       #print(("ConsoleLogWriter: ", Loglevel))
       #print(("ConsoleLogWriter", Loglevel, Filt, DisplayTimeFormat))
       LEVELS = {'debug': logging.DEBUG,
                 'info': logging.INFO,
                 'warning': logging.WARNING,
                 'error': logging.ERROR,
                 'critical': logging.CRITICAL
                 }

       self.Loglevel = Loglevel
       self.DisplayTimeFormat = DisplayTimeFormat
       self.Filt = Filt
       streamHandler = logging.getLogger(self.Filt)
       ch = logging.StreamHandler()
       logfil = logging.Filter(Filt)
       ch.addFilter(logfil)
       streamHandler.setLevel(LEVELS.get(self.Loglevel,logging.NOTSET))
       ch.setLevel(LEVELS.get(self.Loglevel,logging.NOTSET))
       if self.DisplayTimeFormat == True :
           formatter = self.TimeFormatter()
           ch.setFormatter(formatter)
       else:        
           formatter = logging.Formatter("%(name)s - %(levelname)s - %(message)s")
           ch.setFormatter(formatter)
       streamHandler.addHandler(ch)
       return [ch,streamHandler]
       
   def RotatingLogFileHandler(self,logfile="checker1.out",fileMode = "a",Loglevel="debug",LogFilter = "",
                               DisplayTimeFormat = True,maxbytesinfile = 10000000,filecount = 1000):
        '''
        RotatingLogFileHandler() will create handler for rotating log files
        '''
        #print(("RotatingLogFileHandler", Loglevel, Filt, DisplayTimeFormat))
        LEVELS = {'debug': logging.DEBUG,
                  'info': logging.INFO,
                  'warning': logging.WARNING,
                  'error': logging.ERROR,
                  'critical': logging.CRITICAL
                  }
        
        self.logfile = logfile
        self.Loglevel = Loglevel
        self.DisplayTimeFormat = DisplayTimeFormat
        self.maxbytesinfile = maxbytesinfile
        self.filecount = filecount
        self.fileMode = fileMode
        self.LogFilter = LogFilter
        loggerName= logging.getLogger(self.LogFilter)
        logfile = os.path.abspath(logfile)
        rotlogfilter = logging.Filter(self.LogFilter)
        #if LogFilter == "TReport":
        loggerName.setLevel(LEVELS.get(self.Loglevel,logging.DEBUG))
        
        if fileMode == "w" or fileMode == "W":
           newLogfile = open(logfile,"w")
           newLogfile.close()
        Filehandler = logging.handlers.RotatingFileHandler(self.logfile,self.fileMode,self.maxbytesinfile,self.filecount)
        Filehandler.setLevel(LEVELS.get(self.Loglevel,logging.DEBUG))
        Filehandler.addFilter(rotlogfilter)
        if self.DisplayTimeFormat == True :
            formatter = self.TimeFormatter()
            Filehandler.setFormatter(formatter)
        else:
            FileOutFormater = logging.Formatter('%(name)-5s | %(levelname)-5s | %(message)s')
            Filehandler.setFormatter(FileOutFormater)
        loggerName.addHandler(Filehandler)
        return [Filehandler,loggerName]
       
   def HandlerClose(self,HandlerName):
        '''
        HandlerClose() method can be used to close handlers like stream handler or rotating file handler at runtime
        '''
       #print(("HandlerClose: ", HandlerName))
        self.LoggerName = HandlerName[1]
        self.HandlerName = HandlerName[0]
        self.LoggerName.removeHandler(self.HandlerName)
        self.HandlerName.close()
        
   def LoggerShutdown(self):
        '''
        LoggerShutdown() method is used to stop logger module
        '''
        logging.shutdown()
      
   def LogReporter(self,loggername ="STAF",Loglevel="debug",Message = None,MessageLen = 0):
        '''
        LogReporter() method is used to write into console or log file
        '''
        self.loggername = loggername
        self.Loglevel = Loglevel
        self.Message = Message
        if MessageLen == 0:
           getattr(logging.getLogger(self.loggername),self.Loglevel)(self.Message)
        if MessageLen != 0:
           if(len(self.Message) < MessageLen):
              getattr(logging.getLogger(self.loggername),self.Loglevel)(self.Message)
           else:
              getattr(logging.getLogger(self.loggername),self.Loglevel)(self.Message[:MessageLen])
      
        
#####Messenger###############

   
if __name__ == "__main__":
   #lm = LoggerModule()
   km = LoggerModule()
   k = km.ConsoleLogWriter("info","Exec",False)
   l = km.RotatingLogFileHandler("KK.out","w","debug","",False)
   
   for n in range(5):
      km.LogReporter("Exec","debug",n)
   for n in range(5):
      km.LogReporter("Exec","info",n)
   print((k))
   km.HandlerClose(k)
   
   k = km.ConsoleLogWriter("info","Exec",False)
   print((k))

   for n in range(5):
      km.LogReporter("Exec","debug",n)
   for n in range(5):
      km.LogReporter("Exec","info",n)
   print((k))
   km.HandlerClose(k)
   
   k = km.ConsoleLogWriter("info","Exec",False)
   print((k))

   for n in range(5):
      km.LogReporter("Exec","debug",n)
   for n in range(5):
      km.LogReporter("Exec","info",n)
   print((k))
   km.HandlerClose(k)
   print((k))
   
   



   
            

