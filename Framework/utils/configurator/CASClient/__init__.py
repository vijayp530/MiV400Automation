import requests, base64, json, urlparse
# from abc_client import ABCClient
import configurator.ABCClient
# import slate.config
# from slate.util.log import *
# from slate.resource import Config
import time
import datetime
import gevent
import os
import urllib
import gevent.queue
import ast
#import sys
#sys.setdefaultencoding('iso-8859-1')
# import slate.device
# import slate.util.context
from robot.api import logger

class CASClient(object):
	resource_name = 'cas_client'
 
	ROBOT_LIBRARY_SCOPE = 'GLOBAL'

	def __init__(self):
		# self.config = config
		# user.cas_session_id = None
		self.event_session = None
		self.msg_session = None
		self.event_queue = gevent.queue.Queue()
		self.msgIDs = gevent.queue.Queue()
		self.open_transactions = {}
		self.hasVM = False
		self.done = False
		self.msgid = None
		self.flatRecord = {}
		logger.info( "IN THIS INIT!!!")
		#shuntdown started
		startShutdown = False
 
	def bootOriginal(self):
		abc = ABCClient(self.config.abc_hostname)
		self.ticket = abc.authenticate(self.config.client_username, self.config.vm_password)
		self.url = abc.bootstrap('cas', self.ticket)
		self.full_ticket = abc.full_ticket
		u = urlparse.urlparse(self.url)
		self.host = u.netloc
		if slate.config.get('mode') == 'multi-tenant':
			proxy = slate.config.get_first_host('reverse-proxy')
			self.url = urlparse.urlunparse((u.scheme, proxy.ip_address, u.path, u.params, u.query, u.fragment))
 
		username = self.config.client_username
 
		self.event_session = requests.Session()
		self.msg_session = requests.Session()
 
		result = self.send_raw_message('login', {"app-id":"CASTool", "ticket":self.ticket,
			"username" : username}, session=self.event_session)
		if 'SessionId' in result:
			user.cas_session_id = result['SessionId']
			self.sequence = 1
			slate.util.context.spawn(self.get_events)
			return True
		else:
			return False
 
	def boot(self,user):
		abc_hostname = getattr(user, 'server', None)
		# if not abc_hostname:
			# if slate.config.get('mode') == 'multi-tenant': #defined in cluster conf file
				# abc_hostname = slate.config.get_first_host('reverse-proxy').ip_address
			# else:
				# try:
					# abc_hostname = slate.config.get_first_host('abc-server').ip_address
				# except:
					# abc_hostname = slate.config.get_first_host('headquarters').ip_address
		self.abc = configurator.ABCClient(abc_hostname)
		self.ticket = self.abc.authenticate(user.client_id, user.client_password)
		self.url = self.abc.bootstrap('cas', self.ticket)
		self.full_ticket = self.abc.full_ticket

		u = urlparse.urlparse(self.url)
		self.host = u.netloc
		# if slate.config.get('mode') == 'multi-tenant':
				# proxy = slate.config.get_first_host('reverse-proxy')
		# # # self.url = urlparse.urlunparse((u.scheme, proxy.ip_address, u.path, u.params, u.query, u.fragment))
		username = user.client_id

		# self.event_session = requests.Session((self.config.source_address, 9999), False)#self.config.tunnelport))
		self.event_session = requests.Session()#self.config.tunnelport))
		# self.msg_session = requests.Session((self.config.source_address, 9999), False) #self.config.tunnelport))
		self.msg_session = requests.Session() #self.config.tunnelport))

		result = self.send_raw_message('login', {"app-id":"CASTool", "ticket":self.ticket,
                        "username" : username}, session=self.event_session, bindsource=True)
 
        	if 'SessionId' in result:
            		user.cas_session_id = result['SessionId']
            		self.sequence = 1
			self.request = 1
			#subscribe first, then start event loop
			ret = self.subscribe(user)
			if (ret.get('response') != 0):
				logger.info('Subscribe FAILED')
			
			# logger.info(user.cas_session_id)
			#start event loop that receives events from cas server
			#and put the events into a queue
			# # # slate.util.context.spawn(self.get_events)
			#start event process thread
            # # # slate.util.context.spawn(self.process_events)
 
			'''
			#history downloading
			self.download_history()
			#vm downloading
			self.get_voicemailIDs()
 
			#wait for voice mail ids
			time.sleep(1)
 
			#prepare download vm one by one
			if (self.hasVM):
				while not self.msgIDs.empty():
					msgid = self.msgIDs.get()
					self.prepare_downloadVM(msgid)
 
			while (not self.done):
				time.sleep(1.5)
			'''
            		return True
       	 	else:
            		return False
 
 
	def print_session_id(self,user):
		print(user.cas_session_id)
	
	def get_events(self):
		while True:
			if  self.startShutdown:
				print('exit from get_events thread')
				break
 
			result = self.cas_send_message('GetEvents', type='GET', session=self.event_session)
			if not result: continue
 
			response_id = result.get('response', None)
			if response_id and response_id in self.open_transactions:
				self.open_transactions[response_id].put(result)
 
			self.event_queue.put(result)
 
	def process_events(self):
        	while True:
			if  self.startShutdown:
				print('exit from process_events thread')
                        	break
 
            		result = self.event_queue.get()
			#cracke the event and report it
			#process voice mail id
			#if 'vm-messages' in result:
			if (result.get('message') == "get-msgs"):
				vmmsg = result.get('vm-messages')
				lenth = len(vmmsg)
				logger.info('process_events result length: %s' % lenth)
				if (lenth > 1):
					for index in range(lenth):
						self.msgIDs.put(vmmsg[index][0])
						logger.info('process_events msgID: %s' % self.msgIDs)
					self.hasVM = True
			elif (result.get('message') == "download-location-evt"):
				vmmloc = result.get('location')
				vmmsgid = result.get('msg-id')
				logger.info('process_events download-location-evt loc %s' % vmmloc)
				#download the vm file here
				vmfile = urllib.URLopener()
				os.system("mkdir -p %s"%(os.getcwd()+"/vmfiles/"))
				fname = os.getcwd()+"/vmfiles/"+user.client_id+"-"+vmmsgid+".wav"
				#vmfile.retrieve(vmmloc, fname)
				self.download_voicemail_final(fname, vmmloc)
				self.mark_voicemail_as_read(vmmsgid)
 
			elif (result.get('message') == "msg-added-evt"):
				vmmsgs = result.get('vm-messages')
				vmmsgid = (vmmsgs[1])[0]
				self.delete_voicemail(vmmsgid)
 
			self.done = True
 
	def download_history(self):
		 msg = {"topic":"history", "message":"get-recs", "timelabel-begin":0,"filter-by-call-type":1,"max":10,"forward":True}
	         return self.cas_send_message('Execute', msg)
  
	def delete_all_call_history(self,user):
		msg = {"topic":"history", "message":"delete-all"}
		return self.cas_send_message('Execute', msg,user)
 

	def get_all_vm_ids(self,jsonRecord):
		ids = []
		for i in range(1,len(jsonRecord["vm-messages"])):
			ids.append(jsonRecord['vm-messages'][i][0])
		print(ids)
		return ids

	def clear_cached_vms(self):
		self.flatRecord = {}
		
	# def print_vm_flat_record(self):
		# print(self.flatRecord)
	
	# def set_vm_flat_record(self,jsonRecord):
		# for i in range(1,len(jsonRecord["vm-messages"])):
			# self.flatRecord["msg-id"] = jsonRecord['vm-messages'][i][0]
			# self.flatRecord["dur-msec"] = jsonRecord['vm-messages'][i][1]
			# self.flatRecord["vm-folder"] = jsonRecord['vm-messages'][i][2]
			# self.flatRecord["rcvd-timestamp"] = jsonRecord['vm-messages'][i][3]
			# self.flatRecord["sender-name"] = jsonRecord['vm-messages'][i][4]
			# self.flatRecord["sender-number"] = jsonRecord['vm-messages'][i][5]
			# self.flatRecord["msg-flags"] = jsonRecord['vm-messages'][i][8]
		
		# print(self.flatRecord)
		

	def set_all_vms_heard(self,user):
		records = self.get_vms_from_folder(user)
		ids = self.get_all_vm_ids(records)
		self.set_vms_heard(ids,user)
		
	def set_vms_heard(self,ids,user):
	
		if len(ids) == 0:
			logger.info("No VMs to delete")
			return
		print("Deleting ids")
		idsDQ = ""
		for id in ids:
			idsDQ = "%s\"%s\"," % (idsDQ,id)
		idsDQ = idsDQ.rstrip(',')
		idsQ = "[%s]" % str(idsDQ)
		print(idsQ)
		
		execReq =  {"topic":"subscribe","message":"subscribe-events","subscribe":[["vm"]]}
		execResp = self.cas_send_message('Execute', execReq,user)

		execReq = "{\"topic\":\"vm\",\"message\":\"set-heard\",\"heard\":\"true\",\"mbox-id\":\"%s\",\"msg-ids\":%s, \"timestamp\":123456}"%(user.client_id, idsQ)

		execReq = ast.literal_eval(execReq)
		print(execReq)
		execResp = self.cas_send_message('Execute', execReq,user)
		time.sleep(1)

	def delete_vms_by_id(self,ids,user):
		if len(ids) == 0:
			logger.info("No VMs to delete")
			return
		print("Deleting ids")
		idsDQ = ""
		for id in ids:
			idsDQ = "%s\"%s\"," % (idsDQ,id)
		idsDQ = idsDQ.rstrip(',')
		idsQ = "[%s]" % str(idsDQ)
		print(idsQ)
		
		execReq = "{\"topic\":\"vm\",\"message\":\"move-msgs\",\"vm-folder\":3,\"msg-ids\":%s, \"timestamp\":123456}"%(idsQ)
		execReq = ast.literal_eval(execReq)
		print(execReq)
		execResp = self.cas_send_message('Execute', execReq,user)
		time.sleep(1)

	def delete_all_vms(self,user):
		records = self.get_vms_from_folder(user)
		ids = self.get_all_vm_ids(records)
		self.delete_vms_by_id(ids,user)
		# self.clear_cached_vms()
		
	def purge_deleted_vms(self):
		execReq = {"topic":"vm","message":"purge-deleted-msgs"}
		execResp = self.cas_send_message('Execute', execReq)
		time.sleep(1)

	def get_vms_from_folder(self, user):
		# ClearCachedVMs $phone
		execReq = {"topic":"subscribe","message":"subscribe-events","subscribe":[["vm"]]}
		execResp = self.cas_send_message('Execute', execReq,user)
		time.sleep(1)
		# return execResp
		
		execReq = {"topic":"vm","message":"get-online"}
		execResp = self.cas_send_message('Execute', execReq,user)
		time.sleep(2)
		# return execResp
		
		execReq = {"topic":"vm","message":"get-msgs-summaries","vm-folder":0,"msg-id":"","forward":False}
		execResp = self.cas_send_message('Execute', execReq,user)
		# respdict = json.dumps(execResp)
		# print(respdict['vm-messages'])
		# print(execResp['vm-messages'])
		# vmcount = 0
		return execResp

		## Samples response from get-msgs-summaries
		# {"topic":"vm","message":"get-msgs-summaries","timestamp":1295152664989,"sequence-id":337,"response":0,
		# "vm-messages":[["msg-id","dur-msec","vm-folder","rcvd-timestamp","sender-name","sender-number",
		# "sender-canonical","sender-has-mbox","msg-flags"],["4CMBHPFWY",5240,0,1294958508000,
		# "AbhijitB03 MGCPSIM-01","4202","4202",true,0]]}

		# if {[catch { json::json2dict $execResp } respdict]} {
			# test log "Error in processing JSON: $respdict"
			# return 0
		# }
		# if {! [dict exists $respdict "vm-messages"]} {
			# test log "Error: CAS response does not have any VMs. Response: $execResp"
			# return 0
		# }
		# set vmMessages [dict get $respdict "vm-messages"]
		# set vmcount 0
		
		# for {set i 1} {$i < [llength $vmMessages]} {incr i} {
			# set flatRecord [getVMFlatRecord [lindex $vmMessages $i]]
			# lappend ::CachedVMs $flatRecord
			# incr vmcount
		# }
		# return $vmcount

	def prepare_downloadVM(self, msgid):
		msg = {"topic":"vm", "message":"prepare-download","msg-id":msgid, "mbox-id": user.client_id, "ticket":self.ticket}
        	return self.cas_send_message('Execute', msg)
 
	def get_voicemailIDs(self):
        	msg = {"topic":"vm", "message":"get-msgs","mbox-id": user.client_id}
		return self.cas_send_message('Execute', msg)
 
	def download_voicemail(self):
		msg = {"topic":"vm", "message":"prepare-download","mbox-id": user.client_id}
        	return self.cas_send_message('Execute', msg)
 
	def subscribe(self,user):
		msg = {"topic":"subscribe", "message":"subscribe-events", "subscribe":[["tel","device"],["tel","monitor",[user.client_id]],["system","config.users",[{"UserDN":user.client_id}]],["tel","call.control"], ["vm","accessible-mailboxes",[user.client_id]], ["vm","",[user.client_id]]]}
		logger.info(user.cas_session_id)
		return self.cas_send_message('Execute', msg,user)
 
	def download_history(self):
		 msg = {"topic":"history", "message":"get-recs", "timelabel-begin":0,"filter-by-call-type":1,"max":10,"forward":True}
	         return self.cas_send_message('Execute', msg)
 
 
	def prepare_downloadVM(self, msgid):
		msg = {"topic":"vm", "message":"prepare-download","msg-id":msgid, "mbox-id": user.client_id, "ticket":self.ticket}
        	return self.cas_send_message('Execute', msg)
 
	def get_voicemailIDs(self):
        	msg = {"topic":"vm", "message":"get-msgs","mbox-id": user.client_id}
		return self.cas_send_message('Execute', msg)
 
	def download_voicemail(self):
		msg = {"topic":"vm", "message":"prepare-download","mbox-id": user.client_id}
        	return self.cas_send_message('Execute', msg)
 
	# def subscribe(self):
		  # msg = {"topic":"subscribe", "message":"subscribe-events", "subscribe":[["tel","device"],["tel","monitor",[user.client_id]],["system","config.users",[{"UserDN":user.client_id}]],["tel","call.control"], ["vm","accessible-mailboxes",[user.client_id]], ["vm","",[user.client_id]]]}
		  # return self.cas_send_message('Execute', msg)
 
	def assign_to_user(self, phone_mac_address):
		msg = {"topic":"tel", "message":"assign-to-phone",
#			"ip-address": phone_ip_address}
			"mac-address": phone_mac_address}
 
		return self.cas_send_message('Execute', msg)
 
	def assign_soft_phone(self, soft_phone_type, soft_phone_id):
		msg = {'topic' : 'tel', 'message' : 'assign-soft-phone',
			'soft-phone-type' : soft_phone_type,
			'soft-phone-id' : soft_phone_id,
			'timeout-secs' : 10}
		return self.cas_send_message('Execute', msg)
 
	def execute(self, topic, message, **args):
		msg = {'topic' : topic, 'message' : message}
		for key, value in args.items():
			key = key.replace('_', '-')
			msg[key] = value
		return self.cas_send_message('Execute', msg)
 
	def execute2(self, topic, message, **args):
		pass
		# msg = {'topic' : topic, 'message' : message}
		# for key, value in args.items():
			# key = key.replace('_', '-')
			# msg[key] = value
		# result = self.cas_send_message('Execute', msg)
 
		# response = int(result.get('response', 0))
		# if response:
			# q = gevent.queue.Queue()
			# self.open_transactions[response] = q
			# try:
				# with gevent.Timeout(10):
					# event = q.get()
			# except gevent.Timeout:
				# raise Exception('timeout while waiting for CAS response to %s' % msg)
			# if event['error'] != 0:
				# raise Exception('error 0x%x received for CAS request %s' % (event['error'], msg))
		# else:
			# event = None
		# return (result, event)
 
	def cas_send_message(self, location, msg = None, user = {}, type='POST', session=None, ):
		if msg:
			msg['sequence-id'] = self.sequence
			self.sequence += 1
			msg['request-id'] = self.request
			self.request += 1
		rtn = self.send_raw_message(location, msg, parameters={
			'SessionId':user.cas_session_id}, type=type, session=self.event_session, bindsource=False)
		return rtn
 
	def send_raw_message(self, location, msg=None, parameters={}, headers={}, type='POST', session=None, bindsource=False):
		if msg:
			ts = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')
			msg['timestamp'] = 123456
			msg['version'] = 1
 
		headers.update({
			'Content-Type' : 'application/json',
			'Host' : self.host,
			'User-Agent' : 'SLATE',
			'Expect' : '100-continue',
			'TE' : 'deflate,gzip;q=0.3',
			'Connection' : 'keep-alive',
			'Accept' : 'application/json'})
		full_url = '%s/%s' % (self.url, location)
		if parameters:
			full_url += '?'
			for (key, value) in parameters.items():
				full_url += '%s=%s&' % (key, value)
			full_url = full_url[:-1]
		if msg:
			short_msg = dict(msg)
			if location == 'login': short_msg['ticket'] = '...'
 
		short_msg = self.dict_to_tagvalue(short_msg) if msg else ''
 
		logger.info('$CAS/%s %s' % (location, short_msg))
 
		r = requests.Request(type, full_url, headers=headers,
			data=json.dumps(msg) if msg else None)
		#reqdata = json.dumps(msg, separators=(',',':'))
		#r = requests.Request(type, full_url, headers=headers,
		#	data=reqdata if reqdata else None)
 
		req = r.prepare()
 
			# if 'cas' in slate.config.get('log', []):
		# logger.info('%s\n%s\n%s' % (
			# req.method + ' ' + req.url,
			# '\n'.join('%s: %s' % (k, v) for k, v in req.headers.items()),
			# req.body,
		# ), '->')
 
		if not session: session = self.msg_session
		print(bindsource)
		# r = session.send(req, verify=False,bind_source=bindsource)
		r = session.send(req, verify=False)
 
		if not r.ok:
			logger.info('$CAS/%s ERROR: status_code=%s, reason=%s' % (location, r.status_code, r.reason))
			r.raise_for_status()
		else:
			try:
				json_result = self.dict_to_tagvalue(r.json())
				logger.info('$CAS/%s %s' % (location, json_result))
				return r.json()
			except ValueError:
				logger.info('$CAS/%s %s' % (location, r.content))
				return None
 
	def dict_to_tagvalue(self, d):
		result = ''
 
		ordered_tags = ['topic', 'message']
		for t in ordered_tags:
			if t in d: result += '%s=%s, ' % (t, d[t])
		for t in d:
			if t in ordered_tags: continue
			result += '%s=%s, ' % (t, d[t])
		return result[:-2]
 
	def shutdown(self):
		self.startShutdown = True
		if not user.cas_session_id: return
		return self.send_raw_message('Logout', parameters={'SessionId' : user.cas_session_id,
			'timeout' : 6}, headers={'Content-Type': 'application/x-www-form-urlencoded'})
 
	def check_for_voicemail(self):
		pass
		# self.download_history()
		# #vm downloading
		# result = self.get_voicemailIDs()

		# if (result.get('message') == "get-msgs"):
			# vmmsg = result.get('vm-messages')
			# lenth = len(vmmsg)
			# logger.info('process_events result length: %s' % lenth)
			# if (lenth > 1):
					# for index in range(lenth):
							# self.msgIDs.put(vmmsg[index][0])
							# logger.info('process_events msgID: %s' % self.msgIDs)
					# self.hasVM = True
 
 
                # #prepare download vm one by one
                # if (self.hasVM):
                	# while not self.msgIDs.empty():
                        	# self.msgid = self.msgIDs.get()
                                # self.prepare_downloadVM(self.msgid)
		
		# return (self.msgid)
 
 
	def download_voicemail_final(self, fname, dwnpath):
		pass
		# session = self.event_session
		# type    = 'GET'
		# bindsource = False
 
                # headers = {
                        # 'Host' : self.host,
                        # 'User-Agent' : 'SLATE',
                        # 'Expect' : '100-continue',
			# 'Accept-Encoding': 'identity;q=1, *;q=0',
                        # 'Range': 'bytes=0-',
                        # 'Connection' : 'keep-alive',
			# 'Cookie': 'SessionId=%s'%user.cas_session_id,
                        # 'Accept' : '*/*'}
 
                # full_url = dwnpath
 
                # r = requests.Request(type, full_url, headers=headers,
                        # data= None)
 
                # req = r.prepare()
 
                # if 'cas' in slate.config.get('log', []):
                        # logger.info('%s\n%s\n%s' % (
                                # req.method + ' ' + req.url,
                                # '\n'.join('%s: %s' % (k, v) for k, v in req.headers.items()),
                                # req.body,
                        # ), '->')
 
                # if not session: session = self.msg_session
                # r = session.send(req, verify=False,bind_source=bindsource)
 
                # if not r.ok:
                        # logger.info('$CAS/%s ERROR: status_code=%s, reason=%s' % (location, r.status_code, r.reason))
                        # r.raise_for_status()
                # else:
			# f = open(fname, "wb")
			# f.write(r.content)
                        # f.close()
 
 
 
	def mark_voicemail_as_read(self, vmmgid):
		pass
		# msg = "[{\"topic\":\"vm\",\"message\":\"set-heard\",\"heard\":true,\"mbox-id\":\"%s\",\"msg-ids\":[\"%s\"], \"timestamp\":123456,\"request-id\":%s}]"%(user.client_id, vmmgid, self.request)
		# self.request += 1
 
		# session = self.event_session
                # type    = 'POST'
                # bindsource = False
		# location = 'Execute'
		# parameters = {'SessionId':user.cas_session_id} 
 
                # headers = {
                        # 'Host' : self.host,
                        # 'User-Agent' : 'SLATE',
                        # 'Accept-Encoding': 'gzip, deflate',
			# 'Accept-Language': 'en-US,en-us;q=0.8,en;q=0.6',
                        # 'Connection' : 'keep-alive',
			# 'X-Requested-With': 'XMLHttpRequest',
                        # 'Cookie': 'SessionId=%s'%user.cas_session_id,
                        # 'Accept' : 'application/json, text/javascript, */*; q=0.01',
			# 'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
			# 'Content-Length': len(msg)}
 
                # full_url = '%s/%s'%(self.url, location)
	
		# if parameters:
                        # full_url += '?'
                        # for (key, value) in parameters.items():
                                # full_url += '%s=%s&' % (key, value)
                        # full_url = full_url[:-1]
	
                # r = requests.Request(type, full_url, headers=headers,
                        # data= msg)
 
                # req = r.prepare()
 
                # if 'cas' in slate.config.get('log', []):
                        # logger.info('%s\n%s\n%s' % (
                                # req.method + ' ' + req.url,
                                # '\n'.join('%s: %s' % (k, v) for k, v in req.headers.items()),
                                # req.body,
                        # ), '->')
 
                # if not session: session = self.msg_session
                # r = session.send(req, verify=False,bind_source=bindsource)
 
                # if not r.ok:
                        # logger.info('$CAS/%s ERROR: status_code=%s, reason=%s' % (location, r.status_code, r.reason))
                        # r.raise_for_status()
 
	def delete_voicemail(self, vmmgid):
		pass
		# msg = "[{\"topic\":\"vm\",\"message\":\"move-msgs\",\"vm-folder\":3,\"msg-ids\":[\"%s\"], \"timestamp\":123456,\"request-id\":%s}]"%(vmmgid, self.request)
                # self.request += 1
 
		# session = self.event_session
		# type    = 'POST'
		# bindsource = False
		# location = 'Execute'
		# parameters = {'SessionId':user.cas_session_id}

		# headers = {
				# 'Host' : self.host,
				# 'User-Agent' : 'SLATE',
				# 'Accept-Encoding': 'gzip, deflate',
				# 'Accept-Language': 'en-US,en-us;q=0.8,en;q=0.6',
				# 'Connection' : 'keep-alive',
				# 'X-Requested-With': 'XMLHttpRequest',
				# 'Cookie': 'SessionId=%s'%user.cas_session_id,
				# 'Accept' : 'application/json, text/javascript, */*; q=0.01',
				# 'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
				# 'Content-Length': len(msg)}

		# full_url = '%s/%s'%(self.url, location)

		# if parameters:
			# full_url += '?'
			# for (key, value) in parameters.items():
					# full_url += '%s=%s&' % (key, value)
			# full_url = full_url[:-1]

		# r = requests.Request(type, full_url, headers=headers,
				# data= msg)

		# req = r.prepare()

		# # if 'cas' in slate.config.get('log', []):
				# # logger.info('%s\n%s\n%s' % (
						# # req.method + ' ' + req.url,
						# # '\n'.join('%s: %s' % (k, v) for k, v in req.headers.items()),
						# # req.body,
				# # ), '->')

		# if not session: session = self.msg_session
		# r = session.send(req, verify=False,bind_source=bindsource)

		# if not r.ok:
			# logger.info('$CAS/%s ERROR: status_code=%s, reason=%s' % (location, r.status_code, r.reason))
			# r.raise_for_status()
 