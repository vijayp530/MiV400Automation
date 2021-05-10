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
	
def runTrunkinboundCall(index, count):
 	counter = index-1
	c_threads = []
	for i in range(0,count) :
		id  = gevent.spawn(trunk_inboundcall,pphoneList[counter])
		counter = counter +1
		c_threads.append(id)
	gevent.joinall(c_threads)
	
def trunk_inboundcall(index):
	# import rpdb2; rpdb2.start_embedded_debugger('admin1') 
	p = pphoneList[index-1]
	#p2 = pphone.PPhone(phone1, params, s_log)
	t1 = trunk.Trunk(params, p['Cluster'], s_log)
	#p2.connect()
	#p2.register()
	#c1 = t1.call(str(p2.did))           # -> INVITE
	print("Young: Talk time is ==> " + params['MT']['talkTime'] + " \n")
	c1 = t1.call("14082223001")           # -> INVITE
	#c1 = t1.call(p['did'])           # -> INVITE
	#c2 = p2.receive_invite()              # <- INVITE
	#p2.send_ringing(c2)                   # -> 180 Ringing
	t1.receive_invite_response(c1, '180') # <- 180 Ringing
	#p2.answer(c2)                         # -> OK
	t1.receive_answer(c1)                 # <- OK
	t1.send_ack(c1)                       # -> ACK
	#p2.receive_ack(c2)                    # <- ACK

	gevent.sleep(int(params['MT']['talkTime']))

	t1.send_bye(c1)
	#p2.receive_bye(c2)	
	
	#p2.shutdown()
	t1.shutdown()
	gevent.sleep(5)
	
def runTrunkoutboundCall(index, count):

	counter = index-1
	c_threads = []
	for i in range(0,count) :
		id  = gevent.spawn(trunk_outboundcall,pphoneList[counter])
		counter = counter +1
		c_threads.append(id)
	gevent.joinall(c_threads)

def trunk_outboundcall(index):

	#p1 = pphone.PPhone(phone1, params, s_log)
	t1 = trunk.Trunk(params,pphoneList[index-1]['Cluster'],s_log)
	
	#p1.connect()
	#p1.register()
	#c1 = p1.call('9%s' % t1.did)           # -> INVITE
	c2 = t1.receive_invite()              # <- INVITE
	t1.send_ringing(c2)                   # -> 180 Ringing
	#p1.receive_invite_response(c1, '180') # <- 180 Ringing
	t1.answer(c2)                         # -> OK
	#p1.receive_answer(c1)                 # <- OK
	#p1.send_ack(c1)                       # -> ACK
	t1.receive_ack(c2)                    # <- ACK

	gevent.sleep(20)

	#p1.send_bye(c1)                       # -> BYE
	t1.receive_bye(c2)                    # <- BYE
	
	#p1.shutdown()
	t1.shutdown()
	gevent.sleep(5)
	
trunk_inboundcall(1)
#runTrunkinboundCall(1,1)
#runTrunkoutboundCall(1,1)


