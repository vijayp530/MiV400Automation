import requests, base64, json, urlparse, logging
from abc_client import ABCClient
#import slate.config
#from slate.util.log import *
#from slate.resource import Config
import time
import datetime
import gevent
import os
import urllib
import gevent.queue
import sys
import Util
#sys.setdefaultencoding('iso-8859-1')
#import slate.device
#import slate.util.context
requests.packages.urllib3.disable_warnings()



class CASClient():
	resource_name = 'cas_client'

	def __init__(self, phone_info,config, logFile):
		#self.config = config
		self.abc_hostname = config['serverURL']
		self.client_username = phone_info['UserID']
		self.vm_password = phone_info['Pin']
		self.client_extension = phone_info['Extn']
		self.mac_address = phone_info['MacAddr']
		self.did = phone_info['did']
		self.pin = phone_info['Pin']
		self.cluster = phone_info['Cluster']
		self.log = logFile
		self.session_id = None
		self.event_session = None
		self.msg_session = None
		self.event_queue = gevent.queue.Queue()
		self.msgIDs = gevent.queue.Queue()
		self.open_transactions = {}
		self.hasVM = False
		self.done = False
		self.msgid = None
	#shuntdown started
	startShutdown = False

	@classmethod
	def build(cls, c, resource):
		if slate.config.get('mode') == 'multi-tenant':
			abc = slate.config.get_first_host('reverse-proxy')
		else:
			try:
				abc = slate.config.get_first_host('abc-server')
			except:
				abc = slate.config.get_first_host('headquarters')

		resources = []
		password_change = resource.get('password_change', "no")
		new_password = str(resource.get('new_password','changeme'))
		count = int(resource.get('count', 1))
		if resource.get('csv_db'):
			filename = resource.get('csv_db', None)
			start_row = int(resource.get('start_row',1))
			import csv
                        with open(filename, 'rb') as csvfile :
                                reader = csv.DictReader(csvfile, delimiter=' ', quotechar='"')
                                for row in reader:
                                        start_row = start_row - 1
                                        if start_row > 0: continue
                                        client_password = row['Password']
                                        client_username = row['UserID']
					source_address = row['PhoneIPAddr']
					client_extension = row['Extn']
					config = Config(abc_hostname=abc.ip_address,client_extension = client_extension,password_change = password_change,
				client_username = client_username, old_password = client_password, new_password = new_password, source_address = source_address, vm_password = client_password)
					resources.append(CASClient(config))
                                        if count and len(resources) >= count: break
				return resources

	@classmethod
        def buildNew(cls, c, resource):
            if slate.config.get('mode') == 'multi-tenant': #defined in cluster conf file
                abc = slate.config.get_first_host('reverse-proxy')
            else:
                try:
                    abc = slate.config.get_first_host('abc-server')
		except:
                    abc = slate.config.get_first_host('headquarters')

            resources = []

            client_username_prefix = resource.get('client_username_prefix') or 'User'
	    client_vmbox_id_start = resource.get('client_vmbox_id_start') or '3998'
	    client_extension_start = resource.get('client_extension_start') or '3998'
	    client_vmbox_id_start_int = int(client_vmbox_id_start)

	    for i in range(0, int(resource.get('count', 2))):
                config = Config(abc_hostname=abc.ip_address,
                                client_username = '%s%s' % (client_username_prefix, i+3998),
                                client_password = resource.client_password)
				#client_extension = i + client_extension_start,
				#client_vmbox_id = i + client_vmbox_id_start_int)

                if 'vm_password' in resource:
			config.vm_password = resource.vm_password
                else:
			config.vm_password = resource.client_password

                resources.append(CASClient(config))

            return resources

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
			self.session_id = result['SessionId']
			self.sequence = 1
			slate.util.context.spawn(self.get_events)
			return True
		else:
			return False

	def boot(self):
		# abc_hostname = getattr(self.config, 'abc_hostname', None)
		# if not abc_hostname:
			# if slate.config.get('mode') == 'multi-tenant': #defined in cluster conf file
				# abc_hostname = slate.config.get_first_host('reverse-proxy').ip_address
			# else:
				# try:
					# abc_hostname = slate.config.get_first_host('abc-server').ip_address
				# except:
					# abc_hostname = slate.config.get_first_host('headquarters').ip_address
		# if hasattr(self.config, 'password_change'):
			# if self.config.password_change == "yes":
				# time.sleep(1)
				# self.passwdchange()
				# return
		self.abc = ABCClient(self.abc_hostname, self.mac_address, self.did, self.pin, self.cluster, self.log)
		self.ticket = self.abc.authenticate(self.client_username, self.vm_password)
		self.url = self.abc.bootstrap('cas', self.ticket)
		self.full_ticket = self.abc.full_ticket
		u = urlparse.urlparse(self.url)
		self.host = u.netloc
		#if slate.config.get('mode') == 'multi-tenant':
				#proxy = slate.config.get_first_host('reverse-proxy')
		self.url = urlparse.urlunparse((u.scheme, self.abc_hostname, u.path, u.params, u.query, u.fragment))
		#username = self.client_username
		username = self.did
		#self.event_session = requests.Session((self.source_address, 9999), False)#self.config.tunnelport))
		#self.msg_session = requests.Session((self.source_address, 9999), False) #self.config.tunnelport))
		self.event_session = requests.Session()#self.config.tunnelport))
		self.msg_session = requests.Session() #self.config.tunnelport))
		result = self.send_raw_message('login', {"app-id":"CASTool", "ticket":self.ticket,
                        "username" : username}, session=self.event_session, bindsource=True)

        	if 'SessionId' in result:
            		self.session_id = result['SessionId']
            		self.sequence = 1
			self.request = 1
			#subscribe first, then start event loop
			ret = self.subscribe()
			if (ret.get('response') != 0):
				self.log.debug('Subscribe FAILED')
			#start event loop that receives events from cas server
			#and put the events into a queue
			
			#gevent.spawn(self.get_events)
			#start event process thread
            
			#gevent.spawn(self.process_events)
			"""
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
			"""
            		return True
       	 	else:
            		return False


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
				self.log.debug('process_events result length: %s' % lenth)
				if (lenth > 1):
					for index in range(lenth):
						self.msgIDs.put(vmmsg[index][0])
						self.log.debug('process_events msgID: %s' % self.msgIDs)
					self.hasVM = True
			elif (result.get('message') == "download-location-evt"):
				vmmloc = result.get('location')
				vmmsgid = result.get('msg-id')
				self.log.debug('process_events download-location-evt loc %s' % vmmloc)
				#download the vm file here
				vmfile = urllib.URLopener()
				os.system("mkdir -p %s"%(os.getcwd()+"/vmfiles/"))
				fname = os.getcwd()+"/vmfiles/"+self.config.client_extension+"-"+vmmsgid+".wav"
				#vmfile.retrieve(vmmloc, fname)
				self.download_voicemail_final(fname, vmmloc)
				self.mark_voicemail_as_read(vmmsgid)

			elif (result.get('message') == "msg-added-evt"):
				vmmsgs = result.get('vm-messages')
				vmmsgid = (vmmsgs[1])[0]
				self.log.debug('process_events msg-added-evt msg %s' % vmmsgs)
				#self.delete_voicemail(vmmsgid)

			self.done = True

	def passwdchange(self):
		location = 'shoreauth/userauthpwdchange'
                headers = {}
                old_password = base64.b64encode(self.config.old_password)
                new_password = base64.b64encode(self.config.new_password)

		jsonmsg = json.dumps({"username": self.config.client_username ,"oldPassword64": old_password, "newPassword64": new_password})
                headers.update({
                        'Content-Type' : 'application/json',
                        'Host' : self.config.abc_hostname,
                        'User-Agent' : 'SLATE',
                        'Expect' : '100-continue',
                        'TE' : 'deflate,gzip;q=0.3',
                        'Connection' : 'keep-alive',
                        'Accept' : 'application/json'})

		session = requests.Session()
		r = requests.Request('POST','https://%s/%s'%(self.config.abc_hostname, location), headers = headers, data = jsonmsg)
		req = r.prepare()
		r = session.send(req, verify= False)

		self.log.debug('Password change request sent for user : %s with oldPassword : %s and newPassword : %s' %(self.config.client_username, self.config.old_password, self.config.new_password))

                self.log.debug('%s\n%s\n%s' % (
                                req.method + ' ' + req.url,
                                '\n'.join('%s: %s' % (k, v) for k, v in req.headers.items()),
                                req.body,
                        ), '->')

                if not r.ok:
			if r.status_code == 422:
                        	self.log.debug('Password change unsuccessfull ,Can try with strong password length : status_code=%s, reason=%s' % ( r.status_code, r.reason))
			else:	
				self.log.debug('Password change unsuccessfull : status_code=%s, reason=%s' % (r.status_code, r.reason))
			r.raise_for_status()
                else:
                        try:
                                json_result = self.dict_to_tagvalue(r.json())
                                self.log.debug('Password change successfull with response : %s' % ( json_result))
                        except ValueError:
                                self.log.debug('Password change exception : %s' % ( r.content))


	def download_history(self):
		 msg = {"topic":"history", "message":"get-recs", "timelabel-begin":0,"filter-by-call-type":1,"max":10,"forward":True}
	         return self.cas_send_message('Execute', msg)

	def prepare_downloadVM(self, msgid):
		msg = {"topic":"vm", "message":"prepare-download","msg-id":msgid, "mbox-id": self.config.client_extension, "ticket":self.ticket}
        	return self.cas_send_message('Execute', msg)

	def get_voicemailIDs(self):
        	msg = {"topic":"vm", "message":"get-msgs","mbox-id": self.config.client_extension}
		return self.cas_send_message('Execute', msg)

	def download_voicemail(self):
		msg = {"topic":"vm", "message":"prepare-download","mbox-id": self.config.client_extension}
        	return self.cas_send_message('Execute', msg)

	def subscribe(self):
		  msg = {"topic":"subscribe", "message":"subscribe-events", "subscribe":[["tel","device"],["tel","monitor",[self.config.client_extension]],["system","config.users",[{"UserDN":self.config.client_extension}]],["tel","call.control"], ["vm","accessible-mailboxes",[self.config.client_extension]], ["vm","",[self.config.client_extension]]]}
		  return self.cas_send_message('Execute', msg)

	def download_history(self):
		 msg = {"topic":"history", "message":"get-recs", "timelabel-begin":0,"filter-by-call-type":1,"max":10,"forward":True}
	         return self.cas_send_message('Execute', msg)


	def prepare_downloadVM(self, msgid):
		msg = {"topic":"vm", "message":"prepare-download","msg-id":msgid, "mbox-id": self.config.client_extension, "ticket":self.ticket}
        	return self.cas_send_message('Execute', msg)

	def get_voicemailIDs(self):
        	msg = {"topic":"vm", "message":"get-msgs","mbox-id": self.config.client_extension}
		return self.cas_send_message('Execute', msg)

	def download_voicemail(self):
		msg = {"topic":"vm", "message":"prepare-download","mbox-id": self.config.client_extension}
        	return self.cas_send_message('Execute', msg)

	def subscribe(self):
		  msg = {"topic":"subscribe", "message":"subscribe-events", "subscribe":[["tel","device"],["tel","monitor",[self.client_extension]],["system","config.users",[{"UserDN":self.client_extension}]],["tel","call.control"], ["vm","accessible-mailboxes",[self.client_extension]], ["vm","",[self.client_extension]]]}
		  return self.cas_send_message('Execute', msg)

	def assign_to_user(self, phone_mac_address):
		msg = {"topic":"tel", "message":"assign-to-phone",
#			"ip-address": phone_ip_address}
			"mac-address": phone_mac_address}
		print("%s: Entered assign_to_user\n" % phone_mac_address)
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
		msg = {'topic' : topic, 'message' : message}
		for key, value in args.items():
			key = key.replace('_', '-')
			msg[key] = value
		result = self.cas_send_message('Execute', msg)

		response = int(result.get('response', 0))
		if response:
			q = gevent.queue.Queue()
			self.open_transactions[response] = q
			try:
				with gevent.Timeout(10):
					event = q.get()
			except gevent.Timeout:
				raise Exception('timeout while waiting for CAS response to %s' % msg)
			if event['error'] != 0:
				raise Exception('error 0x%x received for CAS request %s' % (event['error'], msg))
		else:
			event = None
		return (result, event)

	def cas_send_message(self, location, msg = None, type='POST', session=None):
		if msg:
			msg['sequence-id'] = self.sequence
			self.sequence += 1
			msg['request-id'] = self.request
			self.request += 1

		rtn = self.send_raw_message(location, msg, parameters={ 'SessionId':self.session_id}, type=type, session=self.event_session, bindsource=False)
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

		self.log.debug('$CAS/%s %s' % (location, short_msg))

		r = requests.Request(type, full_url, headers=headers,
			data=json.dumps(msg) if msg else None)
		#reqdata = json.dumps(msg, separators=(',',':'))
		#r = requests.Request(type, full_url, headers=headers,
		#	data=reqdata if reqdata else None)

		req = r.prepare()

		#if 'cas' in slate.config.get('log', []):
		self.log.debug('%s\n%s\n%s' % (
			req.method + ' ' + req.url,
			'\n'.join('%s: %s' % (k, v) for k, v in req.headers.items()),
			req.body))

		if not session: session = self.msg_session
		#r = session.send(req, verify=False,bind_source=bindsource)
		#key_dir = (os.path.join('keys'))
		key_dir = (os.path.join('keys',self.cluster ))
		keyfile=os.path.join(key_dir, '%s.key' % self.mac_address)
		certfile=os.path.join(key_dir, '%s.crt' % self.mac_address)
		session.cert = ( certfile, keyfile)		
		r = session.send(req, verify=False)

		if not r.ok:
			self.log.debug('$CAS/%s ERROR: status_code=%s, reason=%s' % (location, r.status_code, r.reason))
			r.raise_for_status()
		else:
			try:
				json_result = self.dict_to_tagvalue(r.json())
				self.log.debug('$CAS/%s %s' % (location, json_result))
				return r.json()
			except ValueError:
				self.log.debug('$CAS/%s %s' % (location, r.content))
				return None


	def log(self, msg, header='--'):
		debug(msg, header)

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
		if not self.session_id: return
		return self.send_raw_message('Logout', parameters={'SessionId' : self.session_id,
			'timeout' : 6}, headers={'Content-Type': 'application/x-www-form-urlencoded'})

	def check_for_voicemail(self):
               	self.download_history()
                #vm downloading
                result = self.get_voicemailIDs()

		if (result.get('message') == "get-msgs"):
                                vmmsg = result.get('vm-messages')
                                lenth = len(vmmsg)
                                self.log.debug('process_events result length: %s' % lenth)
                                if (lenth > 1):
                                        for index in range(lenth):
                                                self.msgIDs.put(vmmsg[index][0])
                                                self.log.debug('process_events msgID: %s' % self.msgIDs)
                                        self.hasVM = True


                #prepare download vm one by one
                if (self.hasVM):
                	while not self.msgIDs.empty():
                        	self.msgid = self.msgIDs.get()
                                self.prepare_downloadVM(self.msgid)
		
		return (self.msgid)


	def download_voicemail_final(self, fname, dwnpath):
		session = self.event_session
		type    = 'GET'
		bindsource = False

                headers = {
                        'Host' : self.host,
                        'User-Agent' : 'SLATE',
                        'Expect' : '100-continue',
			'Accept-Encoding': 'identity;q=1, *;q=0',
                        'Range': 'bytes=0-',
                        'Connection' : 'keep-alive',
			'Cookie': 'SessionId=%s'%self.session_id,
                        'Accept' : '*/*'}

                full_url = dwnpath

                r = requests.Request(type, full_url, headers=headers,
                        data= None)

                req = r.prepare()

                if 'cas' in slate.config.get('log', []):
                        self.log.debug('%s\n%s\n%s' % (
                                req.method + ' ' + req.url,
                                '\n'.join('%s: %s' % (k, v) for k, v in req.headers.items()),
                                req.body,
                        ), '->')

                if not session: session = self.msg_session
                r = session.send(req, verify=False,bind_source=bindsource)

                if not r.ok:
                        self.log.debug('$CAS/%s ERROR: status_code=%s, reason=%s' % (location, r.status_code, r.reason))
                        r.raise_for_status()
                else:
			f = open(fname, "wb")
			f.write(r.content)
                        f.close()



	def mark_voicemail_as_read(self, vmmgid):
		msg = "[{\"topic\":\"vm\",\"message\":\"set-heard\",\"heard\":true,\"mbox-id\":\"%s\",\"msg-ids\":[\"%s\"], \"timestamp\":123456,\"request-id\":%s}]"%(self.config.client_extension, vmmgid, self.request)
		self.request += 1

		session = self.event_session
                type    = 'POST'
                bindsource = False
		location = 'Execute'
		parameters = {'SessionId':self.session_id} 

                headers = {
                        'Host' : self.host,
                        'User-Agent' : 'SLATE',
                        'Accept-Encoding': 'gzip, deflate',
			'Accept-Language': 'en-US,en-us;q=0.8,en;q=0.6',
                        'Connection' : 'keep-alive',
			'X-Requested-With': 'XMLHttpRequest',
                        'Cookie': 'SessionId=%s'%self.session_id,
                        'Accept' : 'application/json, text/javascript, */*; q=0.01',
			'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
			'Content-Length': len(msg)}

                full_url = '%s/%s'%(self.url, location)
	
		if parameters:
                        full_url += '?'
                        for (key, value) in parameters.items():
                                full_url += '%s=%s&' % (key, value)
                        full_url = full_url[:-1]
	
                r = requests.Request(type, full_url, headers=headers,
                        data= msg)

                req = r.prepare()

                if 'cas' in slate.config.get('log', []):
                        self.log.debug('%s\n%s\n%s' % (
                                req.method + ' ' + req.url,
                                '\n'.join('%s: %s' % (k, v) for k, v in req.headers.items()),
                                req.body,
                        ), '->')

                if not session: session = self.msg_session
                r = session.send(req, verify=False,bind_source=bindsource)

                if not r.ok:
                        self.log.debug('$CAS/%s ERROR: status_code=%s, reason=%s' % (location, r.status_code, r.reason))
                        r.raise_for_status()

	def delete_voicemail(self, vmmgid):
		msg = "[{\"topic\":\"vm\",\"message\":\"move-msgs\",\"vm-folder\":3,\"msg-ids\":[\"%s\"], \"timestamp\":123456,\"request-id\":%s}]"%(vmmgid, self.request)
                self.request += 1

		session = self.event_session
                type    = 'POST'
                bindsource = False
                location = 'Execute'
                parameters = {'SessionId':self.session_id}

                headers = {
                        'Host' : self.host,
                        'User-Agent' : 'SLATE',
                        'Accept-Encoding': 'gzip, deflate',
                        'Accept-Language': 'en-US,en-us;q=0.8,en;q=0.6',
                        'Connection' : 'keep-alive',
                        'X-Requested-With': 'XMLHttpRequest',
                        'Cookie': 'SessionId=%s'%self.session_id,
                        'Accept' : 'application/json, text/javascript, */*; q=0.01',
                        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
                        'Content-Length': len(msg)}

                full_url = '%s/%s'%(self.url, location)

                if parameters:
                        full_url += '?'
                        for (key, value) in parameters.items():
                                full_url += '%s=%s&' % (key, value)
                        full_url = full_url[:-1]

                r = requests.Request(type, full_url, headers=headers,
                        data= msg)

                req = r.prepare()

                if 'cas' in slate.config.get('log', []):
                        self.log.debug('%s\n%s\n%s' % (
                                req.method + ' ' + req.url,
                                '\n'.join('%s: %s' % (k, v) for k, v in req.headers.items()),
                                req.body,
                        ), '->')

                if not session: session = self.msg_session
                r = session.send(req, verify=False,bind_source=bindsource)

                if not r.ok:
			self.log.debug('$CAS/%s ERROR: status_code=%s, reason=%s' % (location, r.status_code, r.reason))
                        r.raise_for_status()


		


	
if __name__ == '__main__':
	import slate.util
	slate.util.put_context_var('config', {'log' : ['debug']})

	class Config:
		pass
	c = Config()
	c.abc_hostname = '10.32.160.11'
	c.client_username = '52001'
	c.client_password = c.vm_password = 'Shoreadmin1#'

	cas = CASClient(c)
	cas.boot()
	print(cas.shutdown())

