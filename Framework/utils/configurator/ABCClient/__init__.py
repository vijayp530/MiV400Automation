import requests, base64, json
# import slate.config
import urlparse
# from slate.util.log import *
from robot.api import logger
 
class ABCClient(object):
	def __init__(self, abc_hostname):
		self.url = 'https://%s' % abc_hostname
		self.session = requests.Session()
		self.host = urlparse.urlparse(self.url).netloc
		logger.info('url=%s, session=%s, host=%s' % (self.url, self.session, self.host))

 
	def authenticate(self, username, password, expiry=10000):
		'''
		Retrieve a ticket from the ABC service.
		'''
		
 
		location = 'shoreauth/userauth'
 
		logger.info('$ABC/%s, username=%s, password=%s' % (location, username, password))
 
		r = requests.Request('GET', '%s/%s' % (self.url, location), headers={
			'SHOR-ABC-username' : username,
			'SHOR-ABC-password64' : base64.b64encode(password),
			'SHOR-ABC-expiry' : str(expiry),
			'Host' : self.host
		})
 
		req = r.prepare()
 
		# if 'abc' in slate.config.get('log', ['abc']):
			# debug('%s\n%s\n%s' % (
				# req.url,
				# '\n'.join('%s: %s' % (k, v) for k, v in req.headers.items()),
				# req.body,
				# ), '->')
 
		r = self.session.send(req, verify=False)
 
		if not r.ok:
			logger.info('$ABC/%s %s %s' % (location, r.status_code, r.reason))
			r.raise_for_status()
		else:
			short_msg = dict(r.json())
			self.full_ticket = r.content
			short_msg['signature'] = '...'
			logger.info('$ABC/%s %s' % (location, short_msg))
			return base64.b64encode(r.content)
 
	def bootstrap(self, service, ticket):
		'''
		Retrieve the connection location for a specified service.
 
		:param ticket: ABC ticket requested using authenticate
		'''
 
		location = 'shorestart/start'
 
		logger.info('$ABC/%s, service=%s' % (location, service))
 
		r = requests.get('%s/%s' % (self.url, location), headers={
			'SHOR-ABC-svc' : service,
			'SHOR-ABC-ticket' : ticket,
			'Host' : self.host
		}, verify=False) #'/root/TrustmeRootCA.crt')
 
		if not r.ok:
			logger.info('$ABC/%s %s %s' % (location, r.status_code, r.reason))
			r.raise_for_status()
		else:
			logger.info('$ABC/%s %s' % (location, r.json()))
			return r.json()['svcLocation']
 
	# def log(self, msg, header='--'):
			# debug(msg, header)
