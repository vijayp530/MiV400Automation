import gevent.queue
import slate.util, slate.util.context, slate.test
import os, random, base64, string, uuid
import slate.config
from slate.util.log import *

from slate.util import counter

from slate.protocol.mgcp import MGCPMsg

from slate.device.cas_client import CASClient

from socketIO_client import SocketIO, BaseNamespace

from slate.resource import Config, int2ip, int2mac, ip2int, mac2int
from slate.device import Device

def new_id(length=10):
        result = ''
        for n in range(length):
                result += random.choice(string.digits)
        return result

def parse_sdp(sdp):
        lines = sdp.split("\n")
        header = {}
        media = []
        line = ''
        while lines:
                line = lines.pop(0).strip('\r')
		if not line: continue

                if line[0] == 'm':
                        break

                header[line[0]] = line[2:].split(' ')

        while True:
                if not lines:
                        break
                media_parameters = {'m' : line[2:].split(' ')}
                while lines:
                        line = lines.pop(0).strip('\r')
			if not line: continue

                       	if line[0] == 'm':
                                break
                       	parms = line[2:].split(' ')
                        media_parameters[parms[0]] = parms[1:]
                media.append(media_parameters)

        return (header, media)

def build_sdp_media(rtp_port, type, codecs):
        codec_ids = ' '.join([str(c[0]) for c in codecs])
        result = 'm=audio %s %s %s\n' % (rtp_port, type, codec_ids)
        for (num, desc) in codecs:
                result += 'a=rtpmap:%s %s\n' % (num, desc)
        return result

media_server = None

def start_media_server():
        global media_server
        if not media_server: media_server = slate.device.MediaServer.media_server()

class Call(object):
	def __init__(self, device, id):
		self.device = device
		self.id = id

                self.rtp_bridge = None
                self.audio_stream = None

                slate.test.test_instance().annotate('call_ids', self.id)

                if self.device.config.rtp == 'on':
                        result = media_server.new_rtp_stream(self.rtp_id, self.device.switch_ip, 0, self.device.config.codecs[0].upper())
                        try:
                            	(_, self.local_rtp_port, self.local_rtp_ip) = result
                        except ValueError:
                                raise Exception('new_rtp_stream returned unexpected result, %s' % result)
                else:
                       	self.local_rtp_port = 10000
                        self.local_rtp_ip = self.device.config.ip_address

	def complete(self, sdp):
                self.handle_sdp(sdp)

                self.device.log("SDP endpoint is %s:%s" % (self.remote_rtp_ip, self.remote_rtp_port))

                if self.device.config.rtp == 'on':
                        self.device.log('codecs are %s' % self.codecs)
                        media_server.set_stream_endpoint(self.rtp_id, self.remote_rtp_ip, self.remote_rtp_port, self.codecs[0][0])
                        if self.remote_srtp_key:
                                media_server.set_stream_encryption(self.rtp_id, self.srtp_key, self.remote_srtp_key)

                        self.rtp_bridge = media_server.new_bridge(self.rtp_id)
                       	media_server.join_bridge(self.rtp_id, self.rtp_id)
                        self.play_audio(self.default_audio_file)
                else:
                        self.device.log('rtp disabled')

        def play_audio(self, audio, loop=False):
                codec = self.device.config.codecs[0].upper()

                if audio[0] != '/':
                       	ext = 'ulaw'
                        audio = os.path.abspath(slate.util.root_path("usr/share/slate/media/%s.ulaw" % audio))

                if self.audio_stream:
                        media_server.delete_stream(self.audio_stream)
                        self.audio_stream = None

                self.audio_stream = 'audio-%s-%s' % (os.path.basename(audio), self.rtp_id)

                media_server.new_sound_stream(self.audio_stream, audio, loop=True, media_type='ulaw')
                media_server.join_bridge(self.rtp_id, self.audio_stream)

        def build_sdp(self, direction='sendrecv', sections=['RTP/AVP', 'RTP/SAVP', 'RTP/SAVPF']):
                self.sdp_session_id = random.randint(1,10000000)

                codec_map = { 'g711u' : (0, 'PCMU/8000'), 'g711a': (8, 'PCMA/8000'),
                        'g729' : (18, 'G729/8000'), 'iLBC' : (97, 'iLBC/8000'),
                        'l16' : (112, 'L16/8000')}

                codecs = []
                for c in self.device.config.codecs:
                       	if c in codec_map:
                                codecs.append(codec_map[c])
                        else:
				with self:
	                                debug('ignoring unknown codec %s' % c)

                codecs.append((102, 'telephone-event/8000'))

                sdp = 'v=0\no=MXSIP %s 1 IN IP4 %s\ns=SIP Call\nc=IN IP4 %s\nt=0 0\n' % (self.sdp_session_id, self.device.config.ip_address, self.local_rtp_ip)
		if 'RTP/AVP' in sections:
	                sdp += build_sdp_media(self.local_rtp_port, 'RTP/AVP', codecs)
        	        sdp += 'a=%s\n' % direction

                if self.device.config.srtp:
			for section in ['RTP/SAVP', 'RTP/SAVPF']:
        	                self.srtp_key = base64.b64encode(new_id(30))
				if section not in sections: continue

	                        if direction == 'sendrecv':
                	                sdp += build_sdp_media(self.local_rtp_port, section, codecs)
                        	       	sdp += 'a=crypto:1 AES_CM_128_HMAC_SHA1_32 inline:%s UNAUTHENTICATED_SRTP\n' % self.srtp_key
                               		sdp += 'a=%s\n' % direction
	                        else:
        	                        sdp += 'm=audio 0 %s' % section

                if 'sdp' in slate.config.get('log', []):
			with self:
	                        debug(sdp, '->')

                return sdp

        def handle_sdp(self, sdp):
                if 'sdp' in slate.config.get('log', []):
                        self.device.log(sdp, '<-')

                (header, media) = parse_sdp(sdp)
                self.remote_rtp_ip = media[0]['IN'][1]
                self.remote_rtp_port = None
                self.remote_srtp_key = None

                codec_map = { 'g711u' : (0, 'PCMU/8000'), 'g711a': (8, 'PCMA/8000'),
                        'g729' : (18, 'G729/8000'), 'iLBC' : (97, 'iLBC/8000'),
                        'l16' : (112, 'L16/8000') }

                self.codecs = []
                for m in media:
                        if m['m'][2] not in ['RTP/AVP', 'RTP/SAVP', 'RTP/SAVPF']: continue
                        if m['m'][1] == '0': continue
                        available_codecs = [int(i) for i in m['m'][3:]]
                       	self.remote_rtp_port = m['m'][1]
                        for c in self.device.config.codecs:
                               	if c not in codec_map: continue
                                (num, desc) = codec_map[c]
                               	if num in available_codecs: self.codecs.append((num, desc))
                                if 'crypto:1' in m:
                                       	crypto = m['crypto:1'][1]
                                       	if crypto[0:7] == 'inline:': self.remote_srtp_key = crypto[7:]

                if self.remote_rtp_port == None:
                        print("warning: couldn't find RTP port")

        def hangup(self):
                if self.local_rtp_port:
                        stats = media_server.delete_stream(self.rtp_id)
                        if stats: 
                                self.device.log(', '.join(['%s=%s' % (k, v) for k, v in stats.items()]))
                                for name, value in stats.items():
                                        counter(name, int(value))
                        self.local_rtp_port = None

                if self.audio_stream:
                        media_server.delete_stream(self.audio_stream)
                       	self.audio_stream = None

                if self.rtp_bridge:
                        media_server.delete_bridge(self.rtp_id)
                       	self.rtp_bridge = None

class IncomingCall(Call):
	def __init__(self, device, id):
		self.default_audio_file = slate.config.get('callee_audio', 'silence')
		self.rtp_id = 'incoming-call-%s' % id

		super(IncomingCall, self).__init__(device, id)

class OutgoingCall(Call):
	def __init__(self, device, id):
		self.default_audio_file = slate.config.get('caller_audio', 'silence')
		self.rtp_id = 'outgoing-call-%s' % id

		super(OutgoingCall, self).__init__(device, id)

@slate.util.context.object()
class Softphone(Device):
	def __init__(self, config):
		self.config = config
		self.config.client_extension = config.extension
		self.config.vm_password = self.config.client_password
		self.cas = CASClient(config)
		self.incoming_queue = gevent.queue.Queue()
		self.outgoing_queue = gevent.queue.Queue()
		self.incoming_queue2 = {'crcx': gevent.queue.Queue(),
			'dlcx': gevent.queue.Queue(), 'mdcx': gevent.queue.Queue(),
			'up': gevent.queue.Queue(), 'epid': gevent.queue.Queue()}
		self.softphone_id = 'EYEP_%s' % self.config.mac_address.replace(':', '')
		self.transaction_id = random.randint(1, 1000000000)
		self.incoming_calls = {}
		self.outgoing_calls = {}
		self.softphone_name = None
		self.config.source_address = self.config.ip_address

	@classmethod
	def config_template(cls):
		return { 'mac_address' : (str, ['macaddr']), 'extension' : (int, ['extn']),
			'client_username' : (str, ['userid']), 'client_password' : (str, ['password']),
			'ip_address' : (str, ['phoneipaddr']), 'ip_prefix' : (str, None, 19), 'interface' : (str, None, 'eth0'),
			'tenant_id' : (int, ['tenantid']), 'did' : (int), 'rtp' : (str), 'codecs' : (str), 'srtp' : (str) }

	@classmethod
	def build_no_need(cls, c, resource):
		starting_mac_address = mac2int(resource.get('starting_mac_address') or '00:00:00:00:00:00')
		starting_extension = int(resource.get('starting_extension') or 50000)
		starting_ip_address = ip2int(resource.starting_ip_address)
		password = resource.get('password')
		abc_hostname = resource.get('abc_hostname','10.132.160.11')
		ip_prefix = resource.get('ip_prefix', 19)
		interface = resource.get('interface', 'eth0')
		did = int(resource.get('did'))
		resources = []
		for i in range(0, int(resource.get('count', 10))):
			config = Config(client_password=password, vm_password=password, abc_hostname=abc_hostname)
			config.extension = starting_extension + i
			config.client_username = config.extension
			#config.client_username = 'user6@Scale-tenant1.com'
			config.mac_address = int2mac(starting_mac_address + i)
			config.ip_address = int2ip(starting_ip_address + i)
			config.ip_prefix = ip_prefix
			config.did = did+i
			config.interface = interface
			resources.append(Softphone(config))

		return resources

	def on_connect(self):
		debug('socket.io connection connected')

	def boot(self):
		self.cas.boot()
		self.wss_url = self.cas.abc.bootstrap('wss', self.cas.ticket)

		result = self.cas.execute('tel', 'get-soft-phone-params', mgcp_endpoint_id=self.softphone_id)
		self.switch_ip = result['config-switch-addresses'][0]
		self.switch_port = 5004 if result.get('use-port-5004', False) else 2727

		self.signin_queue = gevent.queue.Queue()
		self.connect()
		self.manage_socket_thread = slate.util.context.spawn(self.manage_socket, monitor=True)
		self.manage_incoming_thread = slate.util.context.spawn(self.manage_incoming, monitor=True)

		self.send_login()

		gevent.sleep(1)

#		try:
#			with gevent.Timeout(10):
#				self.incoming_queue2['up'].get()
#		except gevent.Timeout:
#			raise Exception('timeout waiting for initial RQNT')

		result = self.cas.execute2('tel', 'assign-soft-phone', soft_phone_type=4,soft_phone_id=self.softphone_id, timeout_secs=10)

	def reset(self):
		for id, call in self.incoming_calls.items() + self.outgoing_calls.items():
			try:
				self.hangup(call, timeout=0.1)
			except:
				pass

	def log_mgcp(self, msg, header='--'):
		with self:
			debug('$WSS %s' % msg, header)

	def log(self, msg, header='--'):
		with self:
			debug(msg, header)

        def __context__(self):
                return {'extension' : self.softphone_id}

	def connect(self):
		softphone_self = self

		class Events(BaseNamespace):
			def on_connect(self):
				softphone_self.socket_io.emit('myip')
				softphone_self.log_mgcp('myip', '->')
			def on_reconnect(self):
				warn('socket.io reconnect')
			def on_disconnect(self):
				softphone_self.socket_io = None
			def on_login_result(self, data):
				softphone_self.log_mgcp("login result=%s" % data, '<-')
			def on_raw_message(self, data):
				pass
			def on_message(self, data):
				msg = MGCPMsg.parse(data)
				softphone_self.log_mgcp("message='%s'" % msg, '<-')
				softphone_self.incoming_queue.put(msg)
			def on_response(self, data):
				msg = MGCPMsg.parse(data)
				softphone_self.log_mgcp("response='%s'" % msg, '<-')
				softphone_self.incoming_queue2['epid'].put(msg)
			def on_yourip(self, data):
				softphone_self.log_mgcp('yourip=%s' % data, '<-')
				softphone_self.config.ip_address = data
				softphone_self.signin_queue.put(True)

		# remove ip address from interface on exit?
                os.system('sudo ip addr add %s/%s dev %s >&/dev/null' % (self.config.ip_address, self.config.ip_prefix, self.config.interface))

		self.socket_io = SocketIO(self.wss_url, Namespace=Events, verify=False, source_address=(self.config.ip_address, 0))

	def manage_socket(self):
		while True:
			if not self.socket_io: raise Exception('socket.io disconnect')
			self.socket_io.wait(seconds=1)

	def send_login(self):
		self.signin_queue.get()
		msg = MGCPMsg('RSIP', '%s@[%s]' % (self.softphone_id, self.config.ip_address), self.transaction_id,
			RM='restart', MTID=self.config.did)


		self.transaction_id += 1

		initial_msg = {
			'ticket' : self.cas.full_ticket,
			'switchip' : self.switch_ip,
			'switchport' : str(self.switch_port),
			'payload' : msg.build()
		}

		self.send_socketio_message(initial_msg, ack=True)

		try:
			with gevent.Timeout(30):
				response = self.incoming_queue2['epid'].get()
		except gevent.Timeout:
			raise Exception('timeout while waiting for response to %s' % msg)
		gevent.sleep(45)
		

	def manage_incoming(self):
		up = False

		while True:
			msg = self.incoming_queue.get()

			self.fix_context()

			msg_type = msg.msg_type.lower()
			if msg_type == 'rqnt':
				self.softphone_name = msg.tags['N']
				self.respond(msg)
				if not up:
					self.incoming_queue2['up'].put(msg)
					up = True
				continue

			if msg_type == 'auep':
				self.respond(msg, N=self.softphone_name)
				continue

			if msg_type not in self.incoming_queue2:
				self.incoming_queue2[msg_type] = gevent.queue.Queue()

			self.incoming_queue2[msg_type].put(msg)

	def respond(self, mgcp_msg, response_code=200, response_text='OK', **args):
		msg = MGCPMsg('EPID', self.softphone_id, mgcp_msg.transaction_id,
			response_code, response_text, **args)
		self.send_mgcp_message(msg, ack=True, response=True)

	def send_mgcp_message(self, msg, ack=False, response=False):
		channel = 'message' if not response else 'response'
		self.send_socketio_message(msg, channel, ack)

		if response: return

		try:
			with gevent.Timeout(30):
				response = self.incoming_queue2['epid'].get()

		except gevent.Timeout:
			raise Exception('timeout while waiting for response to %s' % msg)

		if response.transaction_id != msg.transaction_id:
			raise Exception('expected response %s but received %s' % (msg.transaction_id, response.transaction_id))

	def send_socketio_message(self, msg, channel='message', ack=False):
		if 'debug' in slate.config.get('log', []):
			self.log_mgcp("%s='%s'" % (channel, msg), header='->')
		if ack:
			q = gevent.queue.Queue()
			def receive_ack(*args): q.put(args)
			ack_func = receive_ack
		else:
			ack_func = None

		if type(msg) is MGCPMsg: msg = msg.build()
		if not self.socket_io: raise Exception('socket.io disconnect')
		self.socket_io.emit(channel, msg, ack_func)

		if ack:
			try:
				with gevent.Timeout(10):
					result = q.get()
			except gevent.Timeout:
				raise Exception('timeout while waiting for socketio ack to %s' % msg)

	def off_hook(self):
		msg = MGCPMsg('NTFY', self.softphone_id, self.transaction_id,
			O='l/hd')
		self.transaction_id += 1
		self.send_mgcp_message(msg)

	def call(self, extension):
		self.off_hook()
		gevent.sleep(1.0)
		(result, event) = self.cas.execute2('tel', 'make-call', dest='%s' % extension)
		try:
			with gevent.Timeout(10):
				msg = self.incoming_queue2['crcx'].get()
		except gevent.Timeout:
			raise Exception('timeout while waiting for CRCX after CAS make-call')

		call_id = str(uuid.UUID('0' + msg.tags['C']))
		assert call_id == event['new-call-id']

		call = OutgoingCall(self, call_id)
		self.outgoing_calls[call_id] = call
		self.current_call = call

		sdp = call.build_sdp()

		response = MGCPMsg('EPID', self.softphone_id, msg.transaction_id,
			'200', 'OK', N=msg.tags['N'], I=2, P = msg.tags['P'])
		response.payload = sdp

		self.send_mgcp_message(response, ack=True, response=True)

		return call

	def answer(self):
		try:
			with gevent.Timeout(10):
				msg = self.incoming_queue2['crcx'].get()
		except gevent.Timeout:
			raise Exception('timeout waiting for CRCX during answer')

		call_id = str(uuid.UUID('0' + msg.tags['C']))

		call = IncomingCall(self, call_id)
		self.incoming_calls[call_id] = call
		self.current_call = call

		sdp = call.build_sdp()

		response = MGCPMsg('EPID', self.softphone_id, msg.transaction_id,
			'200', 'OK', N=msg.tags['N'], I=1, P = msg.tags['P'])
		response.payload = sdp

		self.send_mgcp_message(response, ack=True, response=True)

		self.off_hook()
		gevent.sleep(1.0)
		self.cas.execute('tel', 'answer', **{'call-id' : call_id})

		return call

	def media(self, call=None):
		if not call: call = self.current_call

		try:
			with gevent.Timeout(10):
				msg = self.incoming_queue2['mdcx'].get()
		except gevent.Timeout:
			raise Exception('timeout waiting for MDCX during media()')

		call.complete(msg.payload)

                sdp = call.build_sdp(sections='RTP/SAVPF')

		response = MGCPMsg('EPID', self.softphone_id, msg.transaction_id,
			'200', 'OK', N=msg.tags['N'], I=1, P = msg.tags['P'])
		response.payload = sdp

		self.send_mgcp_message(response, ack=True, response=True)

	def hangup(self, call=None, timeout=10):
		if not call: call = self.current_call

		call.hangup()
		if isinstance(call, IncomingCall):
			del self.incoming_calls[call.id]
		if isinstance(call, OutgoingCall):
			del self.outgoing_calls[call.id]

		self.cas.execute('tel', 'drop', **{'call-id' : call.id, 'no-query-continue':True})
		try:
			with gevent.Timeout(timeout):
				msg = self.incoming_queue2['dlcx'].get()
		except gevent.Timeout:
			raise Exception('timeout waiting for DLCX during hangup')

		self.respond(msg)

	def shutdown(self):
		self.cas.execute2('tel', 'assign-home')
		self.cas.execute2('tel', 'cleanup-soft-phone', **{'soft-phone-type' : 4, 'soft-phone-id' : self.softphone_id})
		if self.manage_socket_thread:
			gevent.kill(self.manage_socket_thread)
			self.manage_socket_thread = None
		if self.manage_incoming_thread:
			gevent.kill(self.manage_incoming_thread)
			self.manage_incoming_thread = None
		if self.socket_io:
			self.socket_io.disconnect()
			self.socket_io = None

	def wait_for_hangup(self, call):
		if not call: call = self.current_call

		try:
			with gevent.Timeout(10):
				msg = self.incoming_queue2['dlcx'].get()
		except gevent.Timeout:
			raise Exception('timeout waiting for DLCX during wait_for_hangup')
		self.respond(msg)

		call.hangup()
		if isinstance(call, IncomingCall):
			del self.incoming_calls[call.id]
		if isinstance(call, OutgoingCall):
			del self.outgoing_calls[call.id]


	def __str__(self):
		return 'Softphone(ext=%s)' % self.config.extension

def register_resource():
        import slate.resource
        slate.resource.register('softphone', Softphone)

if __name__ == '__main__':
	#slate.util.put_context_var('config', {})
	slate.util.put_context_var('config', {'log': ['debug']})
	switch_ip = '10.32.160.11'
	switch_port = '2727'
	password = 'Shoreadmin2#'
	starting_extension = '50006'
	config = Config(switch_ip = switch_ip, switch_port = switch_port, client_password = password, vm_password=password, abc_hostname='10.32.160.11')
	config.extension = starting_extension
	config.client_username = config.extension
	config.client_extension = config.extension
	config.mac_address = '9f:01:01:05:00:06'
	config.ip_address = '172.27.1.6'

	s = Softphone(config)
	with s:
		s.boot()

		s.call(50001)
		gevent.sleep(1)
		s.wait_for_hangup()
		gevent.sleep(5)

