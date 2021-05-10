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
#from Class import softphone
import gevent
import csv

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

params = Util.getCallParams("ConfigParam.txt")
pphoneList = Util.getUserData()

def addUser(index, count):
        
	counter = index-1
	c_threads = []
	boss = BOSS.BOSS(s_log)
	
	for i in range(0,count) :
		boss.addNewUser(pphoneList[counter], params)
		counter = counter +1

def runPhoneUnReg(index, count):
        
	counter = index-1
	c_threads = []
	for i in range(0,count) :
		id = gevent.spawn(phoneUnReg,pphoneList[counter])
		counter = counter +1
		c_threads.append(id)
	gevent.joinall(c_threads)

def phoneUnReg (Phone) :

	p1 = pphone.PPhone(Phone, params, s_log)

	p1.connect()
	p1.register()
	gevent.sleep(10)
	p1.unRegister()
	gevent.sleep(5)
	p1.shutdown()
	gevent.sleep(5)

def runPhoneReg(index, count):
        
	counter = index-1
	c_threads = []
	for i in range(0,count) :
		id = gevent.spawn(phoneReg,pphoneList[counter])
		counter = counter +1
		c_threads.append(id)
	gevent.joinall(c_threads)

def phoneReg (Phone) :

	p1 = pphone.PPhone(Phone, params, s_log)

	p1.connect()
	p1.register()
	#gevent.sleep(10)
	p1.boot_cas()
	gevent.sleep(2)
	p1.shutdown()
	gevent.sleep(5)
	
def runSoftphoneReg(index, count):
        
	counter = index-1
	c_threads = []
	for i in range(0,count) :
		id = gevent.spawn(softphoneReg,pphoneList[counter])
		counter = counter +1
		c_threads.append(id)
	gevent.joinall(c_threads)

def softphoneReg (Shone) :

	p1 = softphone.Softphone(Phone, params, s_log)

	p1.connect()
	p1.register()
	#gevent.sleep(10)
	p1.boot_cas()
	gevent.sleep(2)
	p1.shutdown()
	gevent.sleep(5)
	
def runBasicCallScenario(index, count):
        
	counter = index-1
	c_threads = []
	for i in range(0,count) :
		id = gevent.spawn(singlecall,pphoneList[counter],pphoneList[counter+1])
		counter = counter +2
		c_threads.append(id)
	gevent.joinall(c_threads)

    
def singlecall(phone1,phone2):

	s_log.debug("Basic call is starting\n")
	p1 = pphone.PPhone(phone1, params, s_log)
	p2 = pphone.PPhone(phone2, params, s_log)

	p1.connect()
	p2.connect()
	p1.register()
	p2.register()

	#c1 = p1.call(p2.extension)   
	c1 = p1.call('9%s' % str(p2.did)[-10:])	
	c2 = p2.receive_invite()
	p2.send_ringing()
	#p1.receive_invite_response(c1, '180') 
	gevent.sleep(3)
	p2.answer(c2)
	p1.receive_answer(c1)                 
	p1.send_ack(c1)                       
	p2.receive_ack(c2)

	gevent.sleep(30)

	p1.send_bye(c1)
	p2.receive_bye(c2)

	p1.shutdown()
	p2.shutdown()
	gevent.sleep(5)
	
def runTrunkoutboundCall(index, count):

	counter = index-1
	c_threads = []
	for i in range(0,count) :
		id  = gevent.spawn(trunk_outboundcall,pphoneList[counter])
		counter = counter +1
		c_threads.append(id)
	gevent.joinall(c_threads)

def trunk_outboundcall(phone1):

	p1 = pphone.PPhone(phone1, params, s_log)
	t1 = trunk.Trunk(params,phone1['Cluster'],s_log)
	
	p1.connect()
	p1.register()
	c1 = p1.call('9%s' % t1.did)           # -> INVITE
	c2 = t1.receive_invite()              # <- INVITE
	t1.send_ringing(c2)                   # -> 180 Ringing
	p1.receive_invite_response(c1, '180') # <- 180 Ringing
	t1.answer(c2)                         # -> OK
	p1.receive_answer(c1)                 # <- OK
	p1.send_ack(c1)                       # -> ACK
	t1.receive_ack(c2)                    # <- ACK

	gevent.sleep(20)

	p1.send_bye(c1)                       # -> BYE
	t1.receive_bye(c2)                    # <- BYE
	
	p1.shutdown()
	t1.shutdown()
	gevent.sleep(5)
	
def runTrunkinboundCall(index, count):

 	counter = index-1
	c_threads = []
	for i in range(0,count) :
		id  = gevent.spawn(trunk_inboundcall,pphoneList[counter])
		counter = counter +1
		c_threads.append(id)
	gevent.joinall(c_threads)
	
def trunk_inboundcall(phone1):

	#p2 = pphone.PPhone(phone1, params, s_log)
	t1 = trunk.Trunk(params, phone1['Cluster'], s_log)
	#p2.connect()
	#p2.register()
	#c1 = t1.call(str(p2.did))           # -> INVITE
	c1 = t1.call(phone1['did'])           # -> INVITE
	#c2 = p2.receive_invite()              # <- INVITE
	#p2.send_ringing(c2)                   # -> 180 Ringing
	t1.receive_invite_response(c1, '180') # <- 180 Ringing
	#p2.answer(c2)                         # -> OK
	t1.receive_answer(c1)                 # <- OK
	t1.send_ack(c1)                       # -> ACK
	#p2.receive_ack(c2)                    # <- ACK

	gevent.sleep(10)

	t1.send_bye(c1)
	#p2.receive_bye(c2)	
	
	#p2.shutdown()
	t1.shutdown()
	gevent.sleep(5)
	
#addUser(15,1)
#runPhoneUnReg(1,1)
#runPhoneReg(2,1)
#runBasicCallScenario(11, 1)
#runBasicCallScenario(13, 1)
#runTrunkoutboundCall(1,1)
runTrunkinboundCall(1,1)
#runSoftphoneReg(1,1)
#gevent.sleep(200)

