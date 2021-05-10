__author__ = "milton.villeda@mitel.com"

import sys,socket,thread,logging,time
from datetime import timedelta, datetime
from time import sleep
from struct import *
import struct
import os, signal
import glob
import random, string
from Class import pphone
from Class import trunk
from Class import Util
from Class import BOSS
import gevent
import csv

import subprocess 
import psutil 

# from robot.api.logger import console
from robot.api import logger

dirfmt = "\\Logs\\%4d%02d%02d-%02d%02d%02d"
dirname = dirfmt % time.localtime()[0:6]
logDir = os.getcwd()+dirname
os.makedirs(logDir)

mainLog = logDir+"\\Main.log"

handler = logging.FileHandler(mainLog)
formatter = logging.Formatter('%(asctime)s %(message)s')
handler.setFormatter(formatter)
s_log = logging.getLogger("Global")
s_log.addHandler(handler)
s_log.setLevel(logging.DEBUG)

wintrunksim_dir = os.path.dirname(__file__)

class cd:
    """Context manager for changing the current working directory"""
    def __init__(self, newPath):
        self.newPath = os.path.expanduser(newPath)

    def __enter__(self):
        self.savedPath = os.getcwd()
        os.chdir(self.newPath)

    def __exit__(self, etype, value, traceback):
        os.chdir(self.savedPath)

class wintrunksim():
    """windows trunk siumulator"""

    _DEFAULT_TIMEOUT = 10
    ROBOT_LIBRARY_SCOPE = 'GLOBAL'
    
    def __init__(self):
        # with cd("C://ATF_ROBOT//Framework//winslatedevices"):
        with cd(os.path.dirname(__file__)):
           # self.r_queue = {'trunk'  : gevent.queue.Queue()}
        
           self.t_params = Util.getCallParams("ConfigParam.txt")
           self.params = self.t_params

           # t_nooftrunks = int(self.t_params["NoOfTrunks"])
           # for i in range(0,t_nooftrunks):
           self.build_resources('trunk')

    def build_resources(self,resource):
        self.t_resource = trunk.Trunk(self.params,"MT",s_log)
        # self.r_queue['trunk'].put(t_resource)
                    
    def get_resource(self,type):
        # return self.r_queue[type].get_nowait()
        return self.t_resource
        
    def start_rtp_bridge(self):
        """ Method still in progress """
        rtp_bridge_cmd = rtp_bridge_exe + " -s socket"
        # self.rtp_bridge_pid = subprocess.Popen([rtp_bridge_exe,"-s","socket"], shell=True).pid
        # self.rtp_bridge_pid = subprocess.Popen([rtp_bridge_exe,"-s","socket"], creationflags=subprocess.CREATE_NEW_CONSOLE).pid
        self.rtp_bridge_pid = subprocess.Popen(rtp_bridge_cmd, creationflags=subprocess.CREATE_NEW_CONSOLE).pid
        # self.rtp_bridge_pid = subprocess.Popen([rtp_bridge_exe," -s socket"],creationflags=subprocess.CREATE_NEW_CONSOLE).pid
   
                    
    def stop_rtp_bridge(self):
        p = psutil.Process(self.rtp_bridge_pid)
        p.terminate()

    # def runBasicCallScenario(self):
        # c_count = self.r_queue['pphone'].qsize()/2
        # #c_count = 1
        # c_threads = [gevent.spawn(singlecall,get_resource('pphone'),get_resource('pphone')) for i in range(0,c_count)]
        # gevent.joinall(c_threads)
    
    # def trunk_outboundcall(self,t1,p1):
        # p1.connect()
        # p1.register()
        # c1 = p1.call('9%s' % t1.did)           # -> INVITE
        # c2 = t1.receive_invite()              # <- INVITE
        # t1.send_ringing(c2)                   # -> 180 Ringing
        # p1.receive_invite_response(c1, '180') # <- 180 Ringing
        # gevent.sleep(int(self.params["RingDuration"]))
        # t1.answer(c2)                         # -> OK
        # p1.receive_answer(c1)                 # <- OK
        # p1.send_ack(c1)                       # -> ACK
        # t1.receive_ack(c2)                    # <- ACK

        # gevent.sleep(int(self.params["CallDuration"]))

        # p1.send_bye(c1)                       # -> BYE
        # t1.receive_bye(c2)                    # <- BYE
        # print(p1.get_call_stats(c1))
        # print(t1.get_call_stats(c2))
 
    # def singlecall(self,p1,p2):

        # s_log.debug("Basic call is starting\n")
    
        # p1.connect()
        # p2.connect()
        # p1.register()
        # p2.register()
    
        # c1 = p1.call(p2.extension)     
        # c2 = p2.receive_invite()
        # p2.send_ringing()
        # p1.receive_invite_response(c1, '180')
        # gevent.sleep(int(self.params["RingDuration"]))
        # p2.answer(c2)
        # p1.receive_answer(c1)                 
        # p1.send_ack(c1)                       
        # p2.receive_ack(c2)

        # gevent.sleep(int(self.params["CallDuration"]))
    
        # p1.send_bye(c1)
        # p2.receive_bye(c2)
        # print(p1.get_call_stats(c1))
        # print(p2.get_call_stats(c2))


    def trunksim_inboundcall(self, did):
        t1 = self.get_resource('trunk')
        # import rpdb2; rpdb2.start_embedded_debugger('admin1') 
        # t1 = trunk.Trunk(self.params,"MT",s_log)  # old way
        c1 = t1.call(did)           # -> INVITE
        self.t1 = t1
        self.c1 = c1

        t1.receive_invite_response(c1, '180') # <- 180 Ringing
        t1.sleep_ring_duration()

    def trunksim_complete_inboundcall(self):
        t1 = self.t1
        c1 = self.c1
        
        t1.receive_answer(c1)                 # <- OK
        t1.send_ack(c1)                       # -> ACK

        t1.sleep_call_duration()

    def trunksim_complete_outboundcall(self):
        t1 = self.get_resource('trunk') 
        c1 = t1.receive_invite()              # <- INVITE
        
        self.t1 = t1
        self.c1 = c1
        t1.send_ringing(c1)                   # -> 180 Ringing
	    # import rpdb2; rpdb2.start_embedded_debugger('admin1') 
        t1.sleep_ring_duration()
        
        t1.answer(c1)                         # -> OK
        
        # p1.receive_answer(c1)                 # <- OK
        # p1.send_ack(c1)                       # -> ACK
        
        t1.receive_ack(c1)                    # <- ACK
        t1.sleep_call_duration()

    def trunksim_hangup(self):
        t1 = self.t1
        c1 = self.c1
        # t1.receive_bye(NULL)
        t1.send_bye(c1)    

    def trunksim_farend_hangup(self):
        t1 = self.t1
        c1 = self.c1
        t1.receive_bye(None)

            
    def trunksim_shutdown(self):
        t1 = self.t1
        t1.shutdown()