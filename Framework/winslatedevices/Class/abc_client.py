import requests, base64, json, logging, os
#import slate.config
import urlparse
import Util
#from slate.util.log import *

class ABCClient(object):
	def __init__(self, abc_hostname, mac_address, did, pin, cluster, logFile):
		self.url = 'https://%s' % abc_hostname
		self.session = requests.Session()
		self.host = urlparse.urlparse(self.url).netloc
		self.mac_address = mac_address
		self.did = did
		self.pin = pin
		self.cluster = cluster
		self.log = logFile

	def authenticate(self, username, password, expiry=10000):
		'''
		Retrieve a ticket from the ABC service.
		'''

		location = 'shoreauth/certauth'
		print("%s: Entered  authenticate\n" % self.mac_address)
		self.log.debug('%s, username=%s, password=%s' % (location, username, password))
		body = 'expiry=10000&tn=%s&pin=%s' %( self.did, self.pin)
		r = requests.Request('POST', '%s/%s' % (self.url, location), headers={
			'tn' : self.did,
			'pin' : self.pin,
			'SHOR-ABC-expiry' : "10000",
			'Host' : self.host,
			'Connection' : 'close',
			'Content-Type' : 'application/x-www-form-urlencoded'
		}, data = body)

		req = r.prepare()

		#if 'abc' in slate.config.get('log', ['abc']):
		self.log.debug('%s\n%s\n%s' % (
				req.url,
				'\n'.join('%s: %s' % (k, v) for k, v in req.headers.items()),
				req.body,
				))
		#key_dir = (os.path.join('keys'))
		key_dir = (os.path.join('keys',self.cluster ))
		keyfile=os.path.join(key_dir, '%s.key' % self.mac_address)
		certfile=os.path.join(key_dir, '%s.crt' % self.mac_address)
		self.session.cert = ( certfile, keyfile)
		r = self.session.send(req, verify=False)

		if not r.ok:
			self.log.debug('$ABC/%s %s %s' % (location, r.status_code, r.reason))
			r.raise_for_status()
		else:
			short_msg = dict(r.json())
			self.full_ticket = r.content
			short_msg['signature'] = '...'
			self.log.debug('$ABC/%s %s' % (location, short_msg))
			return base64.b64encode(r.content)

	def bootstrap(self, service, ticket):
		'''
		Retrieve the connection location for a specified service.

		:param ticket: ABC ticket requested using authenticate
		'''

		location = 'shorestart/start'
		
		#key_dir = (os.path.join('keys'))
		key_dir = (os.path.join('keys',self.cluster ))
		keyfile=os.path.join(key_dir, '%s.key' % self.mac_address)
		certfile=os.path.join(key_dir, '%s.crt' % self.mac_address)
		certFiles = ( certfile, keyfile)
		
		self.log.debug('$ABC/%s, service=%s' % (location, service))

		r = requests.get('%s/%s' % (self.url, location), headers={
			'SHOR-ABC-svc' : service,
			'SHOR-ABC-ticket' : ticket,
			'Host' : self.host
		}, cert = certFiles, verify=False) #'/root/TrustmeRootCA.crt')

		if not r.ok:
			self.log.debug('$ABC/%s %s %s' % (location, r.status_code, r.reason))
			r.raise_for_status()
		else:
			self.log.debug('$ABC/%s %s' % (location, r.json()))
			return r.json()['svcLocation']

	def log(self, msg, header='--'):
		with self:
			debug(msg, header)
