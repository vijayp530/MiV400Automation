import gevent, gevent.socket, gevent.queue, gevent.ssl, ssl, re, urlparse, urllib
import os, random, string, socket, base64, hashlib, time, logging
import datetime
import gevent.monkey
import MediaServer
import Util
from cas_client import CASClient
media_server = None

def start_media_server():
    global media_server
    if not media_server: media_server = MediaServer.media_server()

def validate_csv_file(filename):
    import csv

    valid_csv = False

    for delimiter in [' ', '\t', ',']:
        try:
            csv_file = open(filename, 'rb')
        except IOError:
            raise slate.UsageException("can't open csv_db file %s" % filename)

        csv_reader = csv.reader(csv_file, delimiter=delimiter, quotechar='"')
        headers = next(csv_reader)

        if len(headers) == 1: continue

        required_headers = ['PhType', 'PhoneIPAddr', 'SwitchIP', 'Extn', 'Password',
            'Server', 'Password', 'FirstName', 'LastName', 'MacAddr', 'UserID' ]

        missing_headers = []
        for h in required_headers:
            if h not in headers:
                missing_headers.append(h)

        break

    return delimiter

class Unexpected(Exception):
    def __init__(self, received, expected, msg=None):
        self.received = received
        self.expected = expected
        self.msg = msg

    def __str__(self):
        return 'expected %s, received %s%s' % (self.expected, self.received, '\n%s\n' % self.msg.build() if self.msg else '')

def parse_sdp(sdp):
    lines = sdp.split("\n")
    header = {}
    media = []
    line = ''
    while lines:
        line = lines.pop(0).strip('\r')
        if line[0] == 'm':
            break

        header[line[0]] = line[2:].split(' ')

    while True:
        if not lines:
            break
        media_parameters = {'m' : line[2:].split(' ')}
        while lines:
            line = lines.pop(0).strip('\r')
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

def new_id(length=10):
    result = ''
    for n in range(length):
        result += random.choice(string.digits)
    return result
    return branchID
class SIPURI(object):
    def __init__(self, type='', user='', ip='', port='', parameters={}, label=''):
        self.type = type
        self.user = user
        self.ip = ip
        self.port = port
        self.parameters = parameters
        self.label = label

    def __str__(self):
        result = ''
        if self.label: result += '"%s" ' % self.label
        result += '<'
        if self.type: result += '%s:' % self.type
        if self.user: result += '%s@' % self.user
        result += self.ip
        if self.port: result += ':%s' % self.port
        result += '>'
        return result

    @classmethod
    def parse(cls, uri):
        type = ''
        user = ''
        ip = ''
        parameters = {}
        port = ''
        label = ''

        if '"' in uri:
            start = uri.index('"')
            end = uri.index('"', start+1)
            label = uri[start+1:end]
            uri = uri[end+1:]

        if ';' in uri:
            components = uri.split(';')
            uri = components.pop(0)

            parameters = {}
            while components:
                parameter = components.pop(0)
                try:
                    pos = parameter.index('=')
                    parameters[parameter[0:pos]] = parameter[pos+1:]
                except:
                    parameters[parameter] = None

        uri = uri.strip()
        uri = uri.strip('<>')
        if ':' in uri:
            elements = uri.split(':')
            i = elements.pop(0)
            if i in ['sip', 'sips']:
                type = i
                i = elements.pop(0)
            if len(elements) > 1:
                port = elements[1]

        if '@' in i:
            (user, ip) = i.split('@')
        else:
            ip = i

        return cls(type, user, ip, port, parameters, label)

class SIPMsg(object):
    def __init__(self, type, uri, headers={}, content="", version='SIP/2.0'):
        self.type = type
        self.uri = uri
        self.headers = headers
        self.content = content
        self.version = version
        self.queue = gevent.queue.Queue()
        if 'Call-ID' not in self.headers:
            self.headers['Call-ID'] = new_id()
        self.annotations = []

    @property
    def id(self):
        return self.headers['Call-ID']

    def annotate(self, msg):
        self.annotations.append(msg)

    def build(self):
        if self.is_response():
            msg = '%s %s %s\n' % (self.version, self.type, self.uri)
        else:
            msg = '%s %s %s\n' % (self.type, self.uri, self.version)
        d = {
            'Max-Forwards': '70',
            'Supported': '100rel, eventlist, from-change, join, gruu, replaces, tdialog, timer, answermode',
            'Allow': 'ACK, BYE, CANCEL, INFO, INVITE, NOTIFY, OPTIONS, PRACK, REFER, SUBSCRIBE, UPDATE',
            'Allow-Events': 'conference, refer, uaCSTA'
            }

        d.update(self.headers)

        for tag in ['Accept', 'Via', 'Route', 'Record-Route', 'Max-Forwards', 'From', 'To', 'Call-ID', 'CSeq', 'Allow', 'Allow-Events', 'Contact', 'Supported', 'User-Agent']:
            if tag in self.headers:
                value = d[tag]
                if type(value) is list:
                    for v in value:
                        msg += '%s: %s\n' % (tag, v)
                else:
                    msg += '%s: %s\n' % (tag, d[tag])
                del d[tag]
        for (header, value) in d.items():
            if type(value) is list:
                for v in value:
                    msg += '%s: %s\n' % (tag, v)
            else:
                msg += '%s: %s\n' % (header, value)
        msg += 'Content-Length: %s\n\n%s' % (len(self.content), self.content)

        return msg

    def is_response(self):
        try:
            if int(self.type) > 0: return True
        except:
            return False

    def __str__(self):
        result = self.headers['CSeq']
        if self.type == 'NOTIFY' : result += ' ' + self.headers['Event']
        if not self.is_response():
            result += ' ' + self.uri
        if 'Call-ID' in self.headers:
            result += ' ' + self.headers['Call-ID']
        if self.is_response():
            result += ': %s %s' % (self.type, self.uri)

        if self.annotations:
            result += '(%s)' % ', '.join(self.annotations)
        return result

    def get_parameters(self, header, split_on=';'):
        components = self.headers[header].split(split_on)
        parameters = {}
        while components:
            i = components.pop(0).strip(' ')
            try:
                pos = i.index('=')
                parameters[i[0:pos]] = i[pos+1:].strip(' "')
            except:
                parameters[i] = None
        return parameters

    @classmethod
    def parse(cls, msg):
        lines = msg.split('\n')

        header = lines.pop(0).strip('\r').split(' ')
        first_component = header.pop(0)
        if first_component == 'SIP/2.0':
            version = first_component
            msg_type = header.pop(0)
            uri = string.join(header, ' ')
        else:
            msg_type = first_component
            uri = header.pop(0)
            version = header.pop(0)

        headers = {}
        while True:
            line = lines.pop(0).strip('\r')
            i = line.index(':')
            (header, value) = (line[0:i], line[i+2:])
            if header == 'Content-Length':
                break
            if header not in headers:
                headers[header] = value
            elif type(headers[header]) is not list:
                headers[header] = [headers[header], value]
            else:
                headers[header].append(value)

        content=string.join(lines, '\n').strip('\r\n')

        return cls(msg_type, uri, headers, content, version)

class TransactionManager(object):
    def __init__(self):
        self.open_transactions = {}
        self.open_dialogs = {}

    def new(self, msg):
        self.open_transactions[msg.id] = msg
        return msg.id
    def receive_response(self, msg, timeout=10):
        try:
            with gevent.Timeout(timeout):
                #gevent.sleep(0.1)
                return self.open_transactions[msg.id].queue.get()
        except gevent.Timeout, e:
            if timeout == 5:
                error("Re-Invite didn't happen, normal scenario\n")
                return None
            else:
                raise Exception('timeout waiting for response to %s' % msg)
    def terminate(self, msg):
        del self.open_transactions[msg.id]

    def open(self, dialog):
        self.open_dialogs[dialog.id] = dialog
        #dialog.phone.log('dialog %s opened: %s -> %s' % (dialog.id, dialog.config.extension, dialog.peer))

    def receive_dialog_transaction(self, dialog, timeout=10):
        try:
            with gevent.Timeout(timeout):
                return self.open_dialogs[dialog.id].queue.get()
        except gevent.Timeout, e:
            raise Exception('timeout waiting for transaction for dialog %s' % dialog.id)

    def close(self, dialog):
        dialog.hangup()
        #dialog.phone.log('dialog %s closed: %s -> %s' % (dialog.id, dialog.config.extension, dialog.peer))
        del self.open_dialogs[dialog.id]

    def empty(self):
        return len(self.open_transactions) == 0 and len(self.open_dialogs) == 0

class UACManager(TransactionManager):
    def __init__(self):
        TransactionManager.__init__(self)

    def new(self, t, cseq):
        t.headers['CSeq'] = '%s %s' % (cseq, t.type)
        TransactionManager.new(self, t)

    def handle_message(self, msg):
        if msg.id in self.open_transactions and msg.headers['CSeq'].split(' ')[1] == self.open_transactions[msg.id].headers['CSeq'].split(' ')[1]:
            self.open_transactions[msg.id].queue.put_nowait(msg)
        elif msg.id in self.open_dialogs:
            self.open_dialogs[msg.id].queue.put_nowait(msg)
        else:
            print('ignoring unsolicited response: ' + str(msg))

class UASManager(TransactionManager):
    def __init__(self):
        TransactionManager.__init__(self)
        self.new_transactions = {
            'INVITE' : gevent.queue.Queue(),
            'OPTIONS' : gevent.queue.Queue(),
            'NOTIFY' : gevent.queue.Queue(),
            'BYE' : gevent.queue.Queue(),
            'UPDATE': gevent.queue.Queue(),
            'ACK' : gevent.queue.Queue()
                }

    def receive_new_transaction(self, type, timeout=10):
        try:
            with gevent.Timeout(timeout):
                return self.new_transactions[type].get()
        except gevent.Timeout, e:
            raise Exception('timeout waiting for new %s transaction' % type)

    def handle_message(self, msg):
        if msg.id in self.open_transactions and msg.headers['CSeq'].split(' ')[0] == self.open_transactions[msg.id].headers['CSeq'].split(' ')[0]:
            self.open_transactions[msg.id].queue.put_nowait(msg)
        elif msg.id in self.open_dialogs:
            self.open_dialogs[msg.id].queue.put_nowait(msg)
        else:
            self.new(msg)
            self.new_transactions[msg.type].put_nowait(msg)

class Actor(object):
    def __init__(self):
        self.mailbox = {}

    def deliver(key, msg):
        if key not in self.maibox:
            self.mailbox[key] = gevent.queue.Queue()
        self.mailbox[key].put(msg)

    def receive(key):
        if key not in self.mailbox:
            self.mailbox[key] = gevent.queue.Queue()
        self.mailbox[key].get()

class Config(object):
    def __init__(self, parent=None, **args):
        if parent:
            self.__dict__.update(parent.__dict__)
        self.__dict__.update(args)

class Dialog(object):
    def __init__(self, phone):
        self.phone = phone
        #self = phone.config

        self.local_rtp_port = None
        self.remote_rtp_port = None

        self.srtp_key = None
        self.remote_srtp_key = None

        self.queue = gevent.queue.Queue()

        self.rtp_bridge = None
        self.audio_stream = None

        self.local_hold = False
        self.local_deactivate = False
        #added for end call
        self.end_call = False

    def re_invite(self, hold=False, deactivate=False, extra_headers=None):
        direction = 'sendrecv'
        if hold: direction = 'sendonly'
        if deactivate: direction = 'inactive'
        self.sdp_session = self.sdp_session + 1
        sdp = self.build_sdp(direction)

        invite = SIPMsg('INVITE', self.uri, {
            'Accept': 'application/conference-info+xml, application/reginfo+xml, application/rlmi+xml,application/sdp, application/simple-message-summary, application/watcherinfo+xml, message/sipfrag, multipart/mixed, application/csta+xml',
            'Via': 'SIP/2.0/TLS %s:5061;branch=%s;rport;alias' % (self.ip_address, self.branch_id),
            'From': '<sips:%s@%s>;tag=%s' % (self.extension, self.switch_ip, self.to_tag),
            'To': '<sips:%s@%s>;tag=%s' % (self.peer, self.switch_ip,self.from_tag),
            'Call-ID': self.id,
            'Min-SE': '90',
            'Session-Expires': '1800',
            'Content-Disposition': 'session',
            'Content-Type': 'application/sdp'
        }, sdp)

        if hold: invite.annotate('hold')
        if deactivate: invite.annotate('deactivate')

        if extra_headers:
            invite.headers.update(extra_headers)

        self.local_hold = hold
        self.local_deactivate = deactivate

        return invite

    def hangup(self):
        if self.local_rtp_port:
            stats = media_server.delete_stream(self.id)
            self.phone.log.debug("deleting rtp stream of id %s" %self.id)
            if stats:
                self.phone.log.debug(', '.join(['%s=%s' % (k, v) for k, v in stats.items()]))               
            self.local_rtp_port = None

        if self.audio_stream:
            media_server.delete_stream(self.audio_stream)
            self.audio_stream = None

        if self.rtp_bridge:
            media_server.delete_bridge(self.id)
            self.rtp_bridge = None

    def build_sdp(self, direction='sendrecv'):
		self.sdp_session_id = random.randint(1,10000000)
		#self.codecs = ['g711u','g729']
		self.codecs = ['iLBC','g711u']
		codec_map = {'iLBC' : (109, 'iLBC/8000'),'g711u' : (0, 'PCMU/8000'),'g729' : (18, 'G729/8000'),'g722' : (9, 'G722/8000')}
		codecs = []
		for c in self.codecs:
			if c in codec_map:
				codecs.append(codec_map[c])
			elif c[:4] == "iLBC":
				c = "iLBC"
				codecs.append(codec_map[c])
			else :
				log('Ignoring Unsupported Codec %s' % c)
		if not codecs:
			raise Exception("Unsupported codecs ,Supported codecs are G711U/G729/iLBC30/G722" )

		codecs.append((102, 'telephone-event/8000'))

		sdp = 'v=0\no=MXSIP %s %s IN IP4 %s\ns=SIP Call\nc=IN IP4 %s\nt=0 0\n' % (self.sdp_session_id, self.sdp_session, self.phone.ip_address, self.local_rtp_ip)
		sdp += build_sdp_media(self.local_rtp_port, 'RTP/AVP', codecs)
		sdp += "a=fmtp:18 annexb=no\n"
		sdp += "a=fmtp:102 0-15\n"
		sdp += 'a=%s\n' % direction
		if self.phone.config['srtp'] == 'on':
			if direction == 'sendrecv':
				self.srtp_key = base64.b64encode(new_id(30))
				sdp += build_sdp_media(self.local_rtp_port, 'RTP/SAVP', codecs)
				sdp += 'a=crypto:1 AES_CM_128_HMAC_SHA1_32 inline:%s UNAUTHENTICATED_SRTP\n' % self.srtp_key
				sdp += 'a=%s\n' % direction
			else:
				sdp += 'm=audio 0 RTP/SAVP'

		return sdp

    def handle_sdp(self, sdp):
        (header, media) = parse_sdp(sdp)

        self.media_session = header['s'][0]
        self.remote_rtp_ip = header['c'][2]
        self.remote_rtp_port = None
        self.remote_srtp_key = None
        #self.remote_rtp_ip = header['o'][5]
        codec_map = { 'g711u' : (0, 'PCMU/8000'), 'g729' : (18, 'G729/8000'),'iLBC' : (109, 'iLBC/8000'),'l16' : (112, 'L16/8000'),'g722' : (9, 'G722/8000') }
        self.codecs = []
        for m in media:
            if m['m'][2] not in ['RTP/AVP', 'RTP/SAVP']: continue
            if m['m'][1] == '0': continue
            available_codecs = [int(i) for i in m['m'][3:]]
            self.remote_rtp_port = m['m'][1]
            for c in self.codecs:
                if c in codec_map:
                    (num, desc) = codec_map[c]
                elif c[:4] == 'iLBC':
                    c = 'iLBC'
                    (num, desc) = codec_map[c]
                else : continue
                #if c not in codec_map: continue
                #(num, desc) = codec_map[c]
                if num in available_codecs: self.codecs.append((num, desc))
                if 'crypto:1' in m:
                    crypto = m['crypto:1'][1]
                    if crypto[0:7] == 'inline:': self.remote_srtp_key = crypto[7:]
        #c = self.codecs[0]
                #if c[:4] == "iLBC":
                #         c = "iLBC"
        #(c, x) = codec_map[c]
                #if c != available_codecs[0]:
                #         log("preferred codec which is not supported %s\n"%c)
        #    self.end_call = True
        #if self.remote_rtp_port == None:
        #    print("warning: couldn't find RTP port")

    def dtmf_msg(self, signal, duration):
        cseq = int(self.invite.headers['CSeq'].split(' ')[0])

        return SIPMsg('INFO', 'sips:%s@%s:5061;transport=TLS' % (self.peer, self.switch_ip), {
            'Via': self.invite.headers['Via'],
            'Route': '<sips:%s:5061;transport=tls;lr>' % self.switch_ip,
            'From': self.ok.headers['From'],
            'To': self.ok.headers['To'],
            'Call-ID': self.invite.headers['Call-ID'],
            'CSeq': '%s BYE' % cseq,
            'Content-Type': 'application/dtmf-relay'
        }, 'Signal: %s\nDuration: %s\n')

    def bye_msg(self):
        cseq = int(self.invite.headers['CSeq'].split(' ')[0])

        return SIPMsg('BYE', 'sips:%s@%s:5061;transport=TLS' % (self.peer, self.switch_ip), {
            'Via': self.invite.headers['Via'],
            'Route': '<sips:%s:5061;transport=tls;lr>' % self.switch_ip,
            'From': self.ok.headers['From'],
            'To': '%s;tag=%s' % (self.invite.headers['To'], self.to_tag),
            'Call-ID': self.invite.headers['Call-ID'],
            'CSeq': '%s BYE' % cseq,
        })
        def publish_msg(self):
            cseq = int(self.invite.headers['CSeq'].split(' ')[0])
            self.branchID = ""
            from_tag = new_id(12)
            for n in range(10):
                self.branchID += random.choice(string.digits)
                self.branchID = 'z9hG4bK' + self.branchID
                #cseq += 1
                pubCallID = ""
                for n in range(10):
                        pubCallID += random.choice(string.digits)

                sdpMsg = "VQSessionReport: CallTerm\n\
                            CallID: %s\r\n\
                            LocalID: sips://%s@%s:5061/:\r\n\
                            RemoteID: sip://%s@%s:5061/0.0.0.0\r\n\
                            OrigID: sips://%s@%s:5061/:\r\n\
                            LocalGroup: %s\r\n\
                            LocalAddr: IP=%s PORT=%s SSRC=554840f\r\n\
                            RemoteAddr: IP=%s PORT=%s SSRC=6c1ab697\r\n\
                            LocalMAC: %s\r\n\
                            X-ShoreTel-CallGUID: %s\r\n\
                            LocalMetrics:\r\n\
                            Timestamps: START=%s STOP=%s\r\n\
                            SessionDesc: PT=9 PD=G722/8000 SR=8000 FD=20 FO=160 FPP=1 PPS=50 PLC=3 SSUP=off PS=20 PayloadEncryptionType=0x00000040\r\n\
                            JitterBuffer: JBA=3 JBR=0 JBN=0 JBM=1 O=0 U=14\r\n\
                            Delay: RTD=6 IAJ=0 WRTD=10 WIAJ=0\r\n\
                            VPN=0\r\n\
                            InviteTS: 2014-06-19T17:38:35Z\r\n\
                            RingTS: 2014-06-19T17:38:35Z\r\n\
                            ConnectTS: 2014-06-19T17:38:37Z\r\n\
                            DiscTS: 2014-06-19T17:38:54Z\r\n" %(self.id, self.extension,self.ip_address,self.peer, self.switch_ip,self.extension,self.ip_address,self.switch_ip, self.ip_address, self.local_rtp_port, self.remote_rtp_ip, self.remote_rtp_port,':'.join(a+b for a,b in zip(self.mac_address[::2], self.mac_address[1::2])), self.call_guid, self.utc_start_time.strftime("%Y-%m-%dT%H:%M:%SZ") , self.utc_end_time.strftime("%Y-%m-%dT%H:%M:%SZ"))

                strLength = len(sdpMsg)
                message = SIPMsg('PUBLISH', 'sips:vqswitch@%s:5061' % (self.switch_ip),{'Via': 'SIP/2.0/TLS %s:%s;branch=%s;rport' %(self.ip_address,self.local_port,self.branchID), 'Max-Forwards': '70', 'From': '<sips:%s@%s:5061>;tag=%s' %(self.extension, self.ip_address, from_tag), 'To': '<sips:vqswitch@%s:5061>' %self.switch_ip,'Call-ID': '%s' %pubCallID , 'CSeq': '%s PUBLISH' % cseq, 'Contact': '<sips:%s@%s:5061>' %(self.extension,self.ip_address), 'Event': 'vq-rtcpxr', 'Expires': '3600', 'User-Agent': self.user_agent, 'Content-Type': 'application/vq-rtcpxr'}, sdpMsg)
                return message

    def publish_msg1(self):
                cseq = int(self.invite.headers['CSeq'].split(' ')[0])
                self.branchID = ""
                from_tag = new_id(12)
                for n in range(10):
                        self.branchID += random.choice(string.digits)
                self.branchID = 'z9hG4bK' + self.branchID
                #cseq += 1
                pubCallID = ""
                for n in range(10):
                        pubCallID += random.choice(string.digits)

                sdpMsg = "VQSessionReport: CallTerm\n\
CallID: %s\r\n\
LocalID: sips://%s@%s:5061/:\r\n\
RemoteID: sip://%s@%s:5061/0.0.0.0\r\n\
OrigID: sips://%s@%s:5061/:\r\n\
LocalGroup: %s\r\n\
LocalAddr: IP=%s PORT=%s SSRC=554840f\r\n\
RemoteAddr: IP=%s PORT=%s SSRC=6c1ab697\r\n\
LocalMAC: %s\r\n\
X-ShoreTel-CallGUID: %s\r\n\
LocalMetrics:\r\n\
Path: PCNT=1 PCHG=1 PTIME=00:00:03\r\n\
Hop: HCNT=1 HIP=10.57.17.73 HMD=2\r\n" %(self.id, self.extension,self.ip_address,self.peer, self.switch_ip,self.extension,self.ip_address,self.switch_ip, self.ip_address, self.local_rtp_port, self.remote_rtp_ip, self.remote_rtp_port,':'.join(a+b for a,b in zip(self.mac_address[::2], self.mac_address[1::2])), self.call_guid)

                strLength = len(sdpMsg)
                message = SIPMsg('PUBLISH', 'sips:vqswitch@%s:5061' % (self.switch_ip),{'Via': 'SIP/2.0/TLS %s:%s;branch=%s;rport' %(self.ip_address,self.local_port,self.branchID), 'Max-Forwards': '70', 'From': '<sips:%s@%s:5061>;tag=%s' %(self.extension, self.ip_address, from_tag), 'To': '<sips:vqswitch@%s:5061>' %self.switch_ip,'Call-ID': '%s' %pubCallID , 'CSeq': '%s PUBLISH' % cseq, 'Contact': '<sips:%s@%s:5061>' %(self.extension,self.ip_address), 'Event': 'vq-rtcpxr', 'Expires': '3600', 'User-Agent': self.user_agent, 'Content-Type': 'application/vq-rtcpxr'}, sdpMsg)
                return message

    def ack_msg(self, request=None):
        if not request: request = self.ok
        cseq = int(request.headers['CSeq'].split(' ')[0])

        return SIPMsg('ACK', 'sips:%s@%s:5061;transport=TLS' % (self.peer, self.switch_ip), {
            'Via': request.headers['Via'],
            'Route': '<sips:%s:5061;transport=tls;lr>' % self.switch_ip,
            'From': request.headers['From'],
            'To': request.headers['To'],
            'Call-ID': request.headers['Call-ID'],
            'CSeq': '%s ACK' % cseq,
        })

    def handle_reinvite(self, invite):
        self.invite = invite
        self.handle_sdp(invite.content)
        self.phone.log("re-invite, new sdp endpoint is %s:%s" % (self.remote_rtp_ip, self.remote_rtp_port))
        self.sdp_session = self.sdp_session + 1

    def handle_refer(self, refer):
        self.refer = refer
        self.phone.log("refer to %s" % refer.headers['Refer-To'])

    def handle_cancel(self, cancel):
        self.cancel = cancel
        self.send_response_request_headers(cancel, '200', 'OK')
        self.terminate_request_msg()

    def handle_update(self, update):
                self.update = update
                self.send_response_request_headers(update, '200', 'OK')

    def send_response_request_headers(self, req, type, name, content='', headers={}):
                msg = SIPMsg(type, name, {
                        'Accept': 'application/conference-info+xml, application/reginfo+xml, application/rlmi+xml,application/sdp, application/simple-message-summary, application/watcherinfo+xml, message/sipfrag, multipart/mixed, application/csta+xml',
                        'Via': req.headers['Via'],
                        'From': req.headers['From'],
                        'To': req.headers['To'],
                        'Call-ID': req.headers['Call-ID'],
                        'CSeq': req.headers['CSeq'],
                }, content)


                msg.headers.update(headers)

                self.phone.send_sip(msg, True)

    def ok_msg(self,direction='sendrecv'):
        if not self.local_rtp_port:
            result = media_server.new_rtp_stream(self.id, self.phone.ip_address, self.remote_rtp_ip, self.remote_rtp_port, 'ILBC30')
            try:
                (_, self.local_rtp_port, self.local_rtp_ip) = result
                #self.local_rtp_ip = self.phone.ip_address
                self.phone.log.debug("The SDP local endpoint for incoming call is %s,%s\n" %(self.local_rtp_ip,self.local_rtp_port))
            except ValueError:
                    raise Exception('new_rtp_stream returned unexpected result, %s' % result)
            media_server.join_bridge(self.id, self.id)
        else:
            self.local_rtp_port = 10000
            self.local_rtp_ip = self.ip_address

        sdp = self.build_sdp(direction)

        to_header = self.invite.headers['To']
        via_header = self.invite.headers['Via']
        if to_header.find("tag=") == -1:
            self.to_tag = new_id()
            to_header = '%s;tag=%s' % (self.invite.headers['To'], self.to_tag)
        else:
            to_header = SIPURI.parse(self.invite.headers['To'])
            self.to_tag = to_header.parameters['tag']
            if direction == 'recvonly':
                via_header = '%s;received=%s' %(self.invite.headers['Via'],self.switch_ip)

        self.ok = SIPMsg('200', 'OK', {
            'Accept': 'application/conference-info+xml, application/reginfo+xml, application/rlmi+xml,application/sdp, application/simple-message-summary, application/watcherinfo+xml, message/sipfrag, multipart/mixed, application/csta+xml',
            'Via': via_header,
            'From': self.invite.headers['From'],
            'To': to_header,
            'Call-ID': self.invite.headers['Call-ID'],
            'CSeq': self.invite.headers['CSeq'],
            'Content-Disposition': 'session',
            'Content-Type': 'application/sdp'
        }, sdp)

        return self.ok

    def play_audio(self, filename, loop=False):
		#codec = self.codecs[0][1].split('/')[0]
		#codec = self.codecs[0].upper()
		#if audio[0] !='/':
		 #   codec_ext = {'G711U' : 'ulaw', 'G729' : 'g729', 'iLBC' : 'lbc', 'G722' : 'g722'}
		  #  if codec in codec_ext:
		  #      ext = codec_ext[codec]
		  #  else:
		   #     ext = 'ulaw'

			#audio = os.path.abspath(slate.util.root_path("usr/share/slate/media/%s.%s" % (audio, ext)))
		#audio = os.path.abspath("C:/Users/KVeeranan/Desktop/standalone/Mediaserver/hello-world.ulaw")
		#audio = ("C:/Users/KVeeranan/Desktop/standalone/Mediaserver/hello-world.ulaw")
		#audio = os.path.abspath(os.getcwd(),"./Mediaserver/hello-world.ulaw")
		#audio = os.path.dirname(__file__).replace("\\","//") + "//" + ("Mediaserver//%s") %(filename)
		audio = os.getcwd().replace("\\","//") + "//" + ("Mediaserver//%s") %(filename)
		self.audio_stream = 'audio-%s-%s' % (os.path.basename(audio), self.id)
		media_server.new_sound_stream(self.audio_stream, audio, loop=True, media_type="iLBC30")
		media_server.join_bridge(self.id, self.audio_stream)

    def send_ringing(self):
        self.to_tag = new_id()
        self.send_response('180', 'Ringing', headers = {
            'To' : '%s;tag=%s' % (self.invite.headers['To'], self.to_tag)})

    def send_cancel(self):
                self.cancel = SIPMsg('400', 'Bad Request', {
                        'Accept': 'application/conference-info+xml, application/reginfo+xml, application/rlmi+xml,application/sdp, application/simple-message-summary, application/watcherinfo+xml, message/sipfrag, multipart/mixed, application/csta+xml',
                        'Via': self.invite.headers['Via'],
                        'From': self.invite.headers['From'],
                        'To': self.invite.headers['To'],
                        'Call-ID': self.invite.headers['Call-ID'],
                        'CSeq': self.invite.headers['CSeq'],
                        'Content-Disposition': 'session',
                        'Content-Type': 'application/sdp'
                })
                self.phone.send_sip(self.cancel, True)
                return self.cancel

    def send_hold(self):
        sdp = self.build_sdp('sendonly')

        self.hold = SIPMsg('INVITE', self.uri, dict(self.invite.headers))

        self.phone.send_transaction(self.hold)

    def handle_hold(self, invite):
        self.invite = invite

        self.handle_sdp(invite.content)
        self.phone.log("hold, new sdp endpoint is %s:%s" % (self.remote_rtp_ip, self.remote_rtp_port))


    def send_response(self, type, name, content='', headers={}):
        msg = SIPMsg(type, name, {
            'Accept': 'application/conference-info+xml, application/reginfo+xml, application/rlmi+xml,application/sdp, application/simple-message-summary, application/watcherinfo+xml, message/sipfrag, multipart/mixed, application/csta+xml',
            'Via': self.invite.headers['Via'],
            'From': self.invite.headers['From'],
            'To': self.invite.headers['To'],
            'Call-ID': self.invite.headers['Call-ID'],
            'CSeq': self.invite.headers['CSeq'],
        }, content)

        msg.headers.update(headers)

        self.phone.send_sip(msg, True)

    def accept_msg(self):
        self.accept = SIPMsg('202', 'Accepted', {
            'Accept': 'application/conference-info+xml, application/reginfo+xml, application/rlmi+xml,application/sdp, application/simple-message-summary, application/watcherinfo+xml, message/sipfrag, multipart/mixed, application/csta+xml',
            'Via': self.refer.headers['Via'],
            'From': self.refer.headers['From'],
            'To': self.refer.headers['To'],
            'Call-ID': self.refer.headers['Call-ID'],
            'CSeq': self.refer.headers['CSeq'],
            'Content-Disposition': 'session',
            'Content-Type': 'application/sdp'
        })
        return self.accept

    def terminate_request_msg(self):
        msg = SIPMsg('487', 'Request Terminated', {
                        'Accept': 'application/conference-info+xml, application/reginfo+xml, application/rlmi+xml,application/sdp, application/simple-message-summary, application/watcherinfo+xml, message/sipfrag, multipart/mixed, application/csta+xml',
                        'Via': self.cancel.headers['Via'],
                        'From': self.cancel.headers['From'],
                        'To': self.cancel.headers['To'],
                        'Call-ID': self.cancel.headers['Call-ID'],
                        'CSeq': self.invite.headers['CSeq'],
                        'Content-Disposition': 'session',
                        'Content-Type': 'application/sdp'
                })

        self.phone.send_sip(msg, True)

    def notify_msg(self, headers, sipfrag):
        branch_id = 'z9hG4bK' + new_id()
        to_header = SIPURI.parse(self.invite.headers['To'])
        contact_header = self.invite.headers['Contact']
        contact_header = contact_header.strip("<>")
        user = urllib.unquote(contact_header[5:].split('@')[0])
        uri = urlparse.urlunparse(urlparse.ParseResult('sips', '', '%s@%s:5061;transport=TLS' % (user, self.switch_ip), '', '', ''))

        notify = SIPMsg('NOTIFY', uri, {
            'Accept': 'application/conference-info+xml, application/dialog-info+xml, application/reginfo+xml, application/rlmi+xml, application/sdp, application/simple-message-summary, application/watcherinfo+xml, message/sipfrag, multipart/mixed, application/csta+xml',
            'Via': 'SIP/2.0/TLS %s:5061;branch=%s;rport;alias' % (self.ip_address, branch_id),
                        'From': '<sips:%s@%s>;tag=%s' % (to_header.user, self.switch_ip, self.to_tag),
            'To': self.invite.headers['From'],
            'Call-ID': self.invite.headers['Call-ID'],
            'CSeq': self.invite.headers['CSeq'],
        }, '%s\r\n' % sipfrag)

        notify.headers.update(headers)

        return notify

class OutgoingCall(Dialog):
    def __init__(self, phone, peer, extra_headers=None):
        Dialog.__init__(self, phone)
        self.peer = peer
        self.switch_ip = phone.switch_ip
        self.ip_address = phone.ip_address
        self.branch_id = 'z9hG4bK' + new_id()
        self.from_tag = new_id(12)
        self.id = new_id()
        self.sdp_session = 1
        
        result = media_server.new_rtp_stream(self.id, self.ip_address, self.switch_ip, 0, 'ILBC30')
        try:
            (_, self.local_rtp_port, self.local_rtp_ip) = result
            #self.local_rtp_ip = self.phone.ip_address
            self.phone.log.debug("The SDP local endpoint for outgoing call is %s,%s\n" %(self.local_rtp_ip,self.local_rtp_port))
        except ValueError:
            raise Exception('new_rtp_stream returned unexpected result, %s' % result)

        #self.local_rtp_port = 10000
        #self.local_rtp_ip = phone.ip_address

        sdp = self.build_sdp()

        self.uri = urlparse.urlunparse(urlparse.ParseResult('sips', '', '%s@%s:5061' % (self.peer, self.phone.switch_ip), '', '', ''))

        self.invite = SIPMsg('INVITE', self.uri, {
            'Accept': 'application/conference-info+xml, application/reginfo+xml, application/rlmi+xml,application/sdp, application/simple-message-summary, application/watcherinfo+xml, message/sipfrag, multipart/mixed, application/csta+xml',
            'Via': 'SIP/2.0/TLS %s:5061;branch=%s;rport;alias' % (self.phone.ip_address, self.branch_id),
            'From': '<sips:%s@%s>;tag=%s' % (self.phone.extension, self.phone.switch_ip, self.from_tag),
            'To': '<sips:%s@%s>' % (self.peer, self.phone.switch_ip),
            'Call-ID': self.id,
            'Min-SE': '90',
            'Session-Expires': '1800',
            'Content-Disposition': 'session',
            'Content-Type': 'application/sdp'
        }, sdp)
        if extra_headers:
            self.invite.headers.update(extra_headers)

    def __str__(self):
        return 'OutgoingCall(id=%s)' % self.id

    def receive_ok(self, msg):
        self.ok = msg

        to_header = SIPURI.parse(msg.headers['To'])
        self.to_tag = to_header.parameters['tag']
        #added for publish message
        self.call_guid = msg.headers['X-ShoreTel-CallGUID']
        self.utc_start_time = datetime.datetime.utcnow()
                #utc_datetime.strftime("%Y-%m-%dT%H:%M:%SZ")
        self.handle_sdp(msg.content)
        if self.end_call == True:
            self.end_call = False
            self.phone.send_ack()
            self.phone.send_bye()
            raise Exception("codec mismatch: Desired codec not supported by switch\n")
        self.phone.log.debug("The SDP remote for outgoing call is %s,%s\n" %(self.remote_rtp_ip,self.remote_rtp_port))
		#self.phone.log("SDP endpoint is %s:%s, codec is %s" % (self.remote_rtp_ip, self.remote_rtp_port, self.final_codec['desc']))
        media_server.set_stream_endpoint(self.id, self.remote_rtp_ip, self.remote_rtp_port, 109)
        if self.remote_srtp_key:
            media_server.set_stream_encryption(self.id, self.srtp_key, self.remote_srtp_key)

        self.rtp_bridge = media_server.new_bridge(self.id)
        media_server.join_bridge(self.id, self.id)
        caller_audio = self.phone.config['caller_audio']
        #caller_audio = "hello-world"
        #caller_audio = self.phone.config.get('caller_audio','hello-world.ulaw')
        self.play_audio(caller_audio)

class IncomingCall(Dialog):
    def __init__(self, phone, invite,call_name):
		Dialog.__init__(self, phone)
		self.invite = invite
		self.sdp_session = 1
		from_header = SIPURI.parse(invite.headers['From'])
		to_header = SIPURI.parse(invite.headers['To'])
		self.peer = from_header.user
		self.from_tag = from_header.parameters['tag']
		self.id = invite.headers['Call-ID']
		self.to_tag = None
		self.paging = None
		#added for publish message
		try:
					self.call_guid = invite.headers['X-ShoreTel-CallGUID']
		except:
			self.to_tag = to_header.parameters['tag']
			pass

		try:
			self.paging = invite.headers['Answer-Mode']
		except:
			pass


		self.local_rtp_port = None

		self.handle_sdp(self.invite.content)
		self.phone.log.debug("remote SDP endpoint incoming call is %s:%s" % (self.remote_rtp_ip, self.remote_rtp_port))
		self.rtp_bridge = media_server.new_bridge(self.id)
		#callee_audio =  self.phone.config.get('callee_audio','silence.ulaw')
		callee_audio =  self.phone.config['callee_audio']
		self.play_audio(callee_audio)

    def receive_ok(self, msg):
                self.ok = msg

                to_header = SIPURI.parse(msg.headers['To'])
                if self.to_tag == None:
                    self.to_tag = to_header.parameters['tag']
                #added for publish message
                self.utc_start_time = datetime.datetime.utcnow()
                #utc_datetime.strftime("%Y-%m-%dT%H:%M:%SZ")
                self.handle_sdp(msg.content)
                media_server.set_stream_endpoint(self.id, self.remote_rtp_ip, self.remote_rtp_port, 109)

    def __str__(self):
        return 'IncomingCall(id=%s)' % self.id

class PPhone():
    def __init__(self, phone_info,config=None,log_h=None):
		print(phone_info)
		self.phone_info = phone_info
		self.config = config[phone_info['Cluster']]
		self.log = log_h
		self.ip_address = phone_info['PhoneIPAddr']
		self.switch_ip = phone_info['SwitchIP']
		self.did = phone_info['did']
		self.mac_address = phone_info['MacAddr']
		self.pin = phone_info['Pin']
		self.mode = 'multi-tenant'
		self.ip_prefix = '19'
		self.interface = 'eth0'
		#self.key_dir = (os.path.join('C:\Users\KVeeranan\Desktop\standalone\keys'))
		self.key_dir = (os.path.join('keys',phone_info['Cluster'] ))
		self.extension = phone_info['Extn']
		self.disaster_recovery = 0

		self.socket = None
		self.uac_transactions = UACManager()
		self.uas_transactions = UASManager()
		self.calls = {}
		self.cas = None

		self.register_thread = None
		self.read_sip_thread = None
		self.options_thread     = None
		self.update_thread     = None
		self.current_call = None
		self.reconnect = 0
		self.options_timeout = None
		self.tc = 0
		start_media_server()

		self.boot_time = None
		self.source_address = self.ip_address
		self.internal_ip = self.ip_address
		self.client_extension = self.extension
		self.boot_rest_time = 3
		self.user_agent = 'IP485g/802.842.1400.0'
		
		
    def __str__(self):
	
        tenant_id=''

        if self.tenant_id:
            tenant_id='t=%s, ' % self.tenant_id
        return 'PPhone(%sext=%s)' % (tenant_id, self.extension)

    @classmethod
    def build(cls, c, resource):
        hq_name = slate.util.select_first(c.host, class_='headquarters')
        hq = c.host[hq_name]



                #disaster recovery
        #options_flag = resource.get('options_flag', 0)
        #pin = resource.get('pin', '35505#')
        ip_prefix = resource.get('ip_prefix', 19)
        #interface = resource.get('interface', 'eth0')
        #user_agent = resource.get('user_agent', 'IP485g/802.842.1400.0')
        #cas = resource.get('cas', True)
        #if cas == True or cas == 'on' or cas == 'yes' or cas == '1': cas = True
        #else: cas = False

        #codec_resource = resource.get('codecs', ['g729'])
        #boot_rest_time = resource.get('boot_rest_time', 3)

        #cas_protocol = resource.get('cas_protocol', 'TLS')

        #resources = []
        #if resource.get('csv_db'):
        #    filename = resource.get('csv_db')
        #    delimiter = validate_csv_file(filename)

        #    import csv

        #    csv_count = int(resource.get('count', 0))
        #    start_row = int(resource.get('start_row', 1))

        #    index = 0
        #    with open(filename, 'rb') as csvfile:
        #        reader = csv.DictReader(csvfile, delimiter=delimiter, quotechar='"')
        #        for row in reader:
# FirstName LastName MacAddr PhoneIPAddr PhType SwitchIP Extn UserID Password Server TenantID MailBox Email DID DummyIP

        #            start_row = start_row - 1
        #            if start_row > 0: continue

        #            if row['PhType'] != '485g': continue

        #            tenant_prefix = row.get('TenantID', '10000')
        #            ip_address = row['PhoneIPAddr']
        #            switch_ip = row['SwitchIP']
        #            extension = row['Extn']
        #            client_password = row['Password']
        #            server = row['Server']
        #            vm_password = row['Password']
        #            pin = row.get('Pin',pin)
        #            codec_db = row.get('codecs')
        #            first_name = row['FirstName']
        #            last_name = row['LastName']
        #            mac_address = row['MacAddr']
        #            client_username = row['UserID']
        #            did = row.get('DID', '5553341212')
                    #did = row['DID']
        #            internal_ip = row.get('DummyIP', None) or row.get('ContactIP', None)

        #            srtp = resource.get('srtp', False)
        #            if srtp == 'off' or srtp == 'no': srtp = False
        #            codecs = []
        #            code = []
        #            try:
        #                if codec_db:
        #                    code = codec_db.split(",")
        #                else:
        #                    code = codec_resource
        #            except:
        #                code = codec_resource
        #            if type(code) != list:
                 #                    codecs.append(code)
                #            else:
                 #                    codecs = code[:]
        #            config = Config(options_flag = options_flag,  tenant_prefix = tenant_prefix, tenant_id = tenant_prefix, ip_address = ip_address, switch_ip = switch_ip,
        #                extension = extension, client_password=client_password, server = server,
        #                key_dir=slate.util.root_path('var/cache/%s/keys' % c.name),
        #                rtp = resource.get('rtp', 'no'), srtp = srtp, vm_password=vm_password, pin = pin,
        #                abc_hostname = abc.ip_address, did = did, parent = resource,
        #                internal_ip = internal_ip, ip_prefix = ip_prefix, interface = interface, cas = cas, codecs=codecs,
        #                boot_rest_time = boot_rest_time, disaster_recovery = disaster_recovery, enable_publish = enable_publish, user_agent = user_agent)

        #            for item in ['mac_address', 'first_name', 'last_name', 'client_username']:
        #                config.__dict__[item] = vars()[item] % config.__dict__

        #            resources.append(PPhone(config))
        #            if csv_count and len(resources) >= csv_count: break

        #            if 'Audio' in row:
        #                set_parameters(index, row)
        #                index = index+1

        #        return resources

        #ip_address = ip2int(resource.starting_ip_address)
        #extension = int(resource.starting_extension)
        #did = int(resource.starting_did)

        #first_name = resource.get('first_name') or '%s%%(extension)s' % (resource.get('first_name_prefix') or 'First-')
        #last_name = resource.get('last_name') or '%s%%(extension)s' % (resource.get('last_name_prefix') or 'Last-')
        #client_username = resource.get('client_username') or '%s%%(extension)s' % (resource.get('client_username_prefix') or 'User')

        #starting_mac_address = mac2int(resource.get('starting_mac_address') or '00:00:00:00:00:00')

        #for tenant_num in range(0, int(slate.config.get('tenants.count') or 1)):
        #    resource_count = int(resource.get('count') or 10)
        #    tenant_offset = tenant_num * resource_count
        #    tenant_prefix = starting_tenant_prefix + tenant_num

        #    for resource_num in range(0, int(resource.get('count', 10))):
        #        i = resource_num + tenant_offset
        #        config = Config(tenant_prefix = tenant_prefix, tenant_id = tenant_prefix, ip_address = int2ip(ip_address + i), switch_ip = switch.ip_address,
        #            extension = extension + resource_num, client_password=resource.client_password, server = hq.ip_address,
        #            key_dir=slate.util.root_path('var/cache/%s/keys' % c.name),
        #            rtp = resource.get('rtp', 'no'), srtp = resource.get('srtp', 'no'), vm_password=resource.vm_password, pin=resource.pin,
        #            abc_hostname = abc.ip_address, did = did + i, parent = resource, ip_prefix = ip_prefix, interface = interface, cas = cas, codecs=codecs,
        #            boot_rest_time = boot_rest_time)

        #        if starting_mac_address:
        #            config.mac_address = int2mac(starting_mac_address + i)
        #        else:
        #            mac = resource.get('mac_address')  % config.__dict__
        #            config.mac_address = '%s:%s:%s:%s:%s:%s' % (mac[0:2], mac[2:4], mac[4:6], mac[6:8], mac[8:10], mac[10:12])

        #        for item in ['first_name', 'last_name', 'client_username']:
        #            config.__dict__[item] = vars()[item] % config.__dict__

        #        resources.append(PPhone(config))

        #return resources

    def boot(self):
        self.tc = time.time()
        self.connect()
        self.register()
        if self.cas:
            self.boot_cas()

    def boot_cas(self):
		print("%s: Entered boot_cas\n" % self.mac_address)
		self.cas = CASClient(self.phone_info,self.config, self.log)
		self.cas.boot()
		self.cas.assign_to_user(self.mac_address)

    def reset(self):
        def shutdown_dialog(dialog):
            try:
                while not dialog.queue.empty():
                    msg = dialog.queue.get()

                    if msg.type == 'BYE':
                        self.send_response(msg, '200', 'OK')
                        dialog.manager.close(dialog)
                        return

                self.send_bye(dialog)
            except:
                pass

        for d in self.uac_transactions.open_dialogs.values():
            shutdown_dialog(d)

        for d in self.uas_transactions.open_dialogs.values():
            shutdown_dialog(d)

    def shutdown(self):
        self.shutdown_cas()
        self.disconnect()

    def shutdown_cas(self):
        if self.cas:
            self.cas.shutdown()

    def call(self, extension, extra_headers=None):
		self.log.debug("Entered call method\n")
		self.remote_extension = extension
		c = self.invite(extension, extra_headers)
		self.receive_invite_response(c, '100')
		self.current_call = c
		return c

    def play_audio(self, call, audio):
        c.play_audio(audio)

    def hold_call(self, call, hold=True):
        call.branch_id = 'z9hG4bK' + new_id()
        call.uri = urlparse.urlunparse(urlparse.ParseResult('sips', '', '%s@%s:5061' % (call.peer, self.switch_ip), '', '', ''))
        invite = call.re_invite(hold)
        call.hold = invite
        self.send_transaction(invite)

    def receive_hold_response(self, call):
        result = self.uac_transactions.receive_response(call.hold, timeout=10)
        if result.type != '200':
            raise Unexpected(result.type, '200')
        self.send_sip(call.ack_msg(result), True)
        self.uac_transactions.terminate(result)

    def deactivate_call(self, call):
        invite = call.re_invite(deactivate=True)
        call.deactivate = invite
        self.send_transaction(invite)

    def receive_deactivate_response(self, call):
        result = self.uac_transactions.receive_response(call.deactivate, timeout=10)
        if result.type != '200':
            raise Unexpected(result.type, '200')
        self.send_sip(call.ack_msg(result), True)
        self.uac_transactions.terminate(result)

    def connect(self):
		print("%s: Entered connect \n" % self.mac_address)
		if self.socket:
			return
		mac_address_file = os.path.join(self.key_dir, self.mac_address)
		# remove ip address from interface on exit?
		#os.system('sudo ip addr add %s/%s dev %s >&/dev/null' % (self.ip_address, self.ip_prefix, self.interface))
		#os.system('netsh -c "interface ipv4" add address name="Local Area Connection" %s 255.255.192.0' %self.ip_address)
		retries = 0
		while True:
			try:
				#print("Trying to connect, retry count = %s %s %s\n" %(retries,self.switch_ip,self.ip_address))
				retry_status = ' (retry %s of 10)' % retries if retries else ''
				port = random.randint(30001,65000)
				s = gevent.socket.create_connection((self.switch_ip, 5061), source_address=(self.ip_address, port))
				#print((" entered after s creation"))
				local = s.getsockname()
				remote = s.getpeername()
				self.socket = gevent.ssl.SSLSocket(s, keyfile=os.path.join(self.key_dir, '%s.key' % self.mac_address),
					certfile=os.path.join(self.key_dir, '%s.crt' % self.mac_address), ca_certs=os.path.join(self.key_dir, 'hq_ca.crt'))
				#print("kalai created ssl socket connection\n")
				break
			except Exception as e:
				retries = retries + 1
				if retries > 10:
					raise e
				gevent.sleep(10)

		print("%s: Connection has been established successfully\n" % self.mac_address)
		self.read_sip_thread = gevent.spawn(self.read_sip)
		self.cseq = 0
		self.register_call_id = new_id()        

		if self.reconnect == 1:
			self.reconnect = 0
			gevent.kill(self.read_sip_thread)
			gevent.kill(self.update_thread)
			gevent.kill(self.options_thread)
			
		print("%s: Existed Connect\n" % self.mac_address)
		
    def disconnect(self):
		print("%s: Entered Disconnect\n" % self.mac_address)
		if not self.socket:
			return

		#if not self.uac_transactions.empty() or not self.uas_transactions.empty():
		#    self.log('warning: active transactions during disconnect')
		if self.register_thread:
			gevent.kill(self.register_thread)
		gevent.kill(self.read_sip_thread)
		if self.update_thread:
			gevent.kill(self.update_thread)
		if self.options_thread:
			gevent.kill(self.options_thread)
		self.socket.close()
		self.socket = None
		print("%s: Exited Disconnect\n" % self.mac_address)
		
    def unRegister(self):
	
		print("%s: Entered unregister\n" % self.mac_address)
		branchID = 'z9hG4bK' + new_id()
		from_tag = new_id(12)

		msg = SIPMsg('REGISTER', 'sips:%s:5061' % self.switch_ip, headers = {
			'Accept': 'application/conference-info+xml, application/reginfo+xml, application/rlmi+xml,application/sdp, application/simple-message-summary, application/watcherinfo+xml, message/sipfrag, multipart/mixed, application/csta+xml',
			'Via': 'SIP/2.0/TLS %s:5061;branch=%s;rport;alias' % (self.ip_address, branchID),
			'From': '<sips:anonymous@%s>;tag=%s' % (self.switch_ip, from_tag),
			'To': '<sips:anonymous@%s>' % self.switch_ip,
			'CSeq': '%s REGISTER' % self.cseq,
			'Call-ID' : self.register_call_id,
			'Contact': '<sips:anonymous@%s>;+sip.instance=\"<urn:uuid:00000000-0000-1000-8000-%s>\";expires=0' % (self.internal_ip or self.ip_address, self.mac_address.replace(':', '')),})

		try:
			result = self.execute_transaction(msg, timeout=60)
		except gevent.timeout.Timeout, e:
			raise Exception("No response to unregister")

		if result.type == '200':
			return result
		else:
			return result
			
			
    def register(self):
		print("%s: Entered register\n" % self.mac_address)
		branchID = 'z9hG4bK' + new_id()
		from_tag = new_id(12)

		retries = 0

		auth_realm = None
		auth_nonce = None

		while True:
			msg = SIPMsg('REGISTER', 'sips:%s:5061' % self.switch_ip, headers = {
				'Accept': 'application/conference-info+xml, application/reginfo+xml, application/rlmi+xml,application/sdp, application/simple-message-summary, application/watcherinfo+xml, message/sipfrag, multipart/mixed, application/csta+xml',
				'Via': 'SIP/2.0/TLS %s:5061;branch=%s;rport;alias' % (self.ip_address, branchID),
				'From': '<sips:anonymous@%s>;tag=%s' % (self.switch_ip, from_tag),
				'To': '<sips:anonymous@%s>' % self.switch_ip,
				'CSeq': '%s REGISTER' % self.cseq,
				'Call-ID' : self.register_call_id,
				'Contact': '<sips:anonymous@%s>;+sip.instance=\"<urn:uuid:00000000-0000-1000-8000-%s>\";expires=3600' % (self.internal_ip or self.ip_address, self.mac_address.replace(':', '')),
				})

			#if auth_realm:
				#A1 = hashlib.md5('%s:%s:%s' % (self.did, auth_realm, self.client_password)).hexdigest()
				#A2 = hashlib.md5('REGISTER:%s' % auth_realm).hexdigest()

				#auth_resp = hashlib.md5("%s:%s:%s" % (A1, auth_nonce, A2)).hexdigest()

				#msg.headers['Authorization'] = 'Digest username="%s",realm="%s",response="%s",nonce="%s",opaque="0",algorithm=MD5' % (self.did, auth_realm, auth_resp, auth_nonce)

			if auth_realm:
				A1 = hashlib.md5('%s:%s:%s' % (self.did, auth_realm, self.pin)).hexdigest()

				if self.mode  == 'single-tenant':
					A2 = hashlib.md5('REGISTER:%s' % auth_realm).hexdigest()
					auth_resp = hashlib.md5("%s:%s:%s" % (A1, auth_nonce, A2)).hexdigest()
					msg.headers['Authorization'] = 'Digest username="%s",realm="%s",response="%s",nonce="%s",opaque="0",algorithm=MD5' % (self.did, auth_realm, auth_resp, auth_nonce)

				if self.mode == 'multi-tenant':
					A2 = hashlib.md5('REGISTER:sips:%s:5061' % auth_realm).hexdigest()
					auth_resp = hashlib.md5("%s:%s:%s" % (A1, auth_nonce, A2)).hexdigest()
					#uri = "sips:sbc.sky.shoretel.com:5061"
					uri = 'sips:%s:5061' % self.config['sbcURL']
					msg.headers['Authorization'] = 'Digest username="%s",realm="%s",response="%s",uri="%s",nonce="%s",opaque="0",algorithm=MD5' % (self.did, auth_realm, auth_resp, uri,auth_nonce)
			try:
				result = self.execute_transaction(msg, timeout=60)
			except gevent.timeout.Timeout, e:
				retries += 1
				if (retries > 10):
					raise Exception("too many retries during register")
				continue

			if result.type == '301':
				contact = result.headers['Contact']
				self.switch_ip = contact.split(':')[1]
				# TODO: persist the new switch_ip somewhere for the next run
				self.disconnect()
				self.connect()
				continue
			elif result.type == '200':

				#if self.options_flag == '1':
							#         self.options_timeout = 100
				self.update_thread = gevent.spawn(self.handle_update)
				self.options_thread = gevent.spawn(self.handle_options)

				if self.register_thread: return
				via = result.headers['Via']
				#added for publish message
				self.local_port = via.split('rport=')[1].split(';')[0]
				# switch delivers a bunch of notifies to feed configuration upon first registration
				while True:
					t = self.uas_transactions.receive_new_transaction('NOTIFY', 30)
					self.send_response(t, '200', 'OK')
					if t.headers['Event'] == 'firmware-query':
						break
				return result
			elif result.type == '480':
				gevent.sleep(5.0)
				self.disconnect()
				self.connect()
				gevent.sleep(5.0)
				#break
				continue
			elif result.type == '401':
				auth_header = result.get_parameters('WWW-Authenticate', split_on=',')
				auth_realm = auth_header['Digest realm'].strip('"')
				auth_nonce = auth_header['nonce'].strip('"')
				branchID = 'z9hG4bK' + new_id()
				gevent.sleep(1.0)
				continue
			elif result.type == '408':
				self.disconnect()
				self.connect()
				gevent.sleep(5.0)
				#break
				continue
			elif result.type == '500':
				retries += 1
				if (retries > 10):
						raise Exception("too many retries during register")
				gevent.sleep(10.0)
				continue
			else:
				return result
				break

				
				
    def invite(self, destination, extra_headers=None):
		self.log.debug("Entered invite method\n")
		c = OutgoingCall(self, destination, extra_headers)
		c.manager = self.uac_transactions
		self.uac_transactions.open(c)
		self.send_transaction(c.invite)
		return c

    def receive_invite_response(self, c=None, type='100'):
        if not c: c = self.current_call
        msg = self.uac_transactions.receive_response(c.invite)
        if msg.type == type:
            return
        #if msg.type == '200':
                #         return
        if msg.type == '403':
            c.ok = msg
            self.send_ack(c)
            raise Exception("Call disconnected due to codec mismatch")
        if msg.type >= '500' and msg.type <= '599':
            self.send_ack(c)
        raise Unexpected(msg.type, type)

    def receive_answer(self, c=None, timeout=10):
        if not c: c = self.current_call
        while True:
            #gevent.sleep(0.1)
            msg = self.uac_transactions.receive_response(c.invite, timeout=timeout)
            if msg.type == '200':
                c.receive_ok(msg)
                return
            if msg.type == '180':
                continue
            if msg.type == '100':
                continue
            if msg.type >= '500' and msg.type <= '599':
                self.send_ack(c)
            break
        raise Unexpected(msg.type, '200')

    def receive_invite2(self, timeout=10):
        return self.uas_transactions.receive_new_transaction('INVITE', timeout=timeout)

    def receive_invite(self, timeout=10):
        invite = self.receive_invite2(timeout)
        return self.process_invite(invite)

    def process_invite(self, invite, call_name=None):
        c = IncomingCall(self, invite, call_name)
        c.manager = self.uas_transactions
        self.uas_transactions.open(c)
        self.current_call = c
        return c

    def receive_hold(self, c=None):
        if not c: c = self.current_call
        msg = c.manager.receive_dialog_transaction(c, timeout=20)
        if msg.type != 'INVITE':
            raise Unexpected(msg.type, 'INVITE')
        c.handle_reinvite(msg)
        self.send_response(msg, '200', 'OK')
        msg = c.manager.receive_dialog_transaction(c, timeout=20)
        if msg.type != 'ACK':
            raise Unexpected(msg.type, 'ACK')

    def receive_deactivate(self, c=None):
        if not c: c = self.current_call
        msg = c.manager.receive_dialog_transaction(c, timeout=10)
        if msg.type != 'INVITE':
            raise Unexpected(msg.type, 'INVITE')
        c.handle_reinvite(msg)
        self.send_response(msg, '200', 'OK')
        msg = c.manager.receive_dialog_transaction(c, timeout=10)
        if msg.type != 'ACK':
            raise Unexpected(msg.type, 'ACK')

    def receive_reinvite(self, c=None, timeout=10):
        if not c: c = self.current_call
        invite = self.uac_transactions.receive_response(c.invite, timeout)
        if not invite:
            return None
        if invite.type != 'INVITE':
            raise Unexpected(invite.type, 'INVITE')
        c.handle_reinvite(invite)
        return invite

    def receive_refer(self, c=None):
        if not c: c = self.current_call
        refer = c.manager.receive_dialog_transaction(c, timeout=20)
        if refer.type == 'ACK':
                        refer = c.manager.receive_dialog_transaction(c, timeout=20)
        if refer.type != 'REFER':
            raise Unexpected(refer.type, 'REFER')
        c.handle_refer(refer)
        return refer

    def receive_cancel(self, c=None):
        if not c: 
            c = self.current_call
            cancel = c.manager.receive_response(c, timeout=20)
        if cancel.type != 'CANCEL':
                raise Unexpected(cancel.type, 'CANCEL')
                c.handle_cancel(cancel)
        return cancel

    def receive_update(self, c=None):
                if not c: c = self.current_call
                update = c.manager.receive_dialog_transaction(c, timeout=10)
                if update.type != 'UPDATE':
                        raise Unexpected(update.type, 'UPDATE')
                c.handle_update(update)
                return update

    def receive_notify(self, c=None):
        if not c: c = self.current_call
        notify = c.manager.receive_dialog_transaction(c, timeout=10)
        if notify.type != 'NOTIFY':
            raise Unexpected(notify.type, 'NOTIFY')
        self.send_response(notify, '200', 'OK')
        return notify

    def send_ringing(self, c=None):
        if not c: c = self.current_call
        c.send_ringing()

    def send_cancel(self, c=None):
                if not c: c = self.current_call
                c.send_cancel()

    def answer(self, c=None, direction='sendrecv'):
        if not c: c = self.current_call
        #added for publish message
        c.utc_start_time = datetime.datetime.utcnow()
        self.send_sip(c.ok_msg(direction), True)

    def accept(self, c=None):
        if not c: c = self.current_call
        self.send_sip(c.accept_msg(), True)

    def notify_trying(self, c=None):
        if not c: c = self.current_call
        headers = {'Subscription-State': 'pending;expires=4294966', 'Event': 'refer;id=2', 'Content-Type': 'message/sipfrag'}
        self.execute_transaction(c.notify_msg(headers, 'SIP/2.0 100 Trying'))

    def notify_ok(self, c=None):
        headers = {'Subscription-State': 'terminated;reason=noresource', 'Event': 'refer;id=2', 'Content-Type': 'message/sipfrag'}
        self.execute_transaction(c.notify_msg(headers, 'SIP/2.0 200 OK'))

    def notify_active(self, c=None):
                headers = {'Subscription-State': 'active', 'Event': 'uaCSTA', 'Content-Type': 'application/CSTA+XML'}
                self.execute_transaction(c.notify_msg(headers, '<?xml version="1.0" encoding="UTF-8"?>\n\
                        <HookSwitchStatus xmlns="http://www.ecma-international.org/standards/ecma-323/csta/ed3">\n\
                        <hookSwitchStatusList>\n\
                        <hookSwitchStatusItem>\n\
                        <hookSwitch>speaker</hookSwitch>\n\
                        <hookSwitchOnhook>false</hookSwitchOnhook>\n\
                        </hookSwitchStatusItem>\n\
                        <hookSwitchStatusItem>\n\
                        <hookSwitch>headset</hookSwitch>\n\
                        <hookSwitchOnhook>true</hookSwitchOnhook>\n\
                        </hookSwitchStatusItem>\n\
                        <hookSwitchStatusItem>\n\
                        <hookSwitch>handset</hookSwitch>\n\
                        <hookSwitchOnhook>true</hookSwitchOnhook>\n\
                        </hookSwitchStatusItem>\n\
                        </hookSwitchStatusList>\n\
                        </HookSwitchStatus>\n\
                        '))

    def send_ack(self, c=None):
        if not c: c = self.current_call
        # ACKs are weird, they're like half a transaction
        self.send_sip(c.ack_msg(), True)

    def receive_ack(self, c=None):
        if not c: c = self.current_call
        ack = self.uas_transactions.receive_response(c)
        self.uas_transactions.terminate(ack)

    def receive_cack(self, c=None):
        if not c: c = self.current_call
        ack = self.uac_transactions.receive_dialog_transaction(c)

    def send_transaction(self, t):
        self.cseq += 1
        self.uac_transactions.new(t, self.cseq)
        self.send_sip(t)

    def execute_transaction(self, msg, timeout=10):
        self.send_transaction(msg)
        result = self.uac_transactions.receive_response(msg, timeout=timeout)
        self.uac_transactions.terminate(msg)
        return result

    def send_sip(self, msg, response=False):
        if not response and self.boot_rest_time and self.boot_time:
            now = time.time()
            ready = self.boot_time + int(self.boot_rest_time)
            if now < ready:
                delay = ready - now
                if delay > 1:
                    print('waiting for boot rest time, ready in %ds' % delay)
                gevent.sleep(delay)
            self.boot_time = None

        if 'Contact' not in msg.headers:
            msg.headers['Contact'] = '<sips:%s@%s>' % (self.extension, self.internal_ip or self.ip_address)
        if 'User-Agent' not in msg.headers:
            msg.headers['User-Agent'] = '%s' %(self.user_agent)

        data = msg.build()
        #print("The sent sip message is %s\n"%data)
        self.log.debug("%s: The sent sip message is %s\n"%(self.mac_address,data))
        try:
            result = self.socket.write(data)
        except Exception as e:
            print("TLS connection broken in send_sip %s\n" % self.mac_address)
            raise e
        cseq_type = msg.headers['CSeq'].split(' ')[1]
        suppress = ['OPTIONS'] #suppress = ['OPTIONS', 'NOTIFY', 'UPDATE']

    def play_audio(self, c=None, filename='silence', loop=False):
        if not c: c = self.current_call
        c.play_audio(filename, loop)

    def send_bye(self, c=None):
        if not c: c = self.current_call
        bye = c.bye_msg()
        result = self.execute_transaction(bye)
        if result.type != '200':
                        raise Unexpected(result.type, '200')
        #added for publish message
        c.utc_end_time = datetime.datetime.utcnow()
        #if self.enable_publish == '1':
                #    publish = c.publish_msg()
        #    self.execute_transaction(publish)
        #    publish1 = c.publish_msg1()
                #    self.execute_transaction(publish1)
        c.manager.close(c)

    def receive_bye(self, c=None, timeout=10):
        if not c: c = self.current_call
        msg = c.manager.receive_dialog_transaction(c, timeout=10)
        if msg.type == 'ACK':
            msg = c.manager.receive_dialog_transaction(c, timeout=10)
        if msg.type == 'BYE':
            #added for timestamp in publish message
            c.utc_end_time = datetime.datetime.utcnow()

            self.send_response(msg, '200', 'OK')
            #if self.enable_publish == '1':
            #    publish = c.publish_msg()
                    #    self.execute_transaction(publish)
            #    publish1 = c.publish_msg1()
                    #    self.execute_transaction(publish1)
            c.manager.close(c)
            return
        raise Unexpected(msg.type, 'BYE')

    def receive_bye2(self, c=None, timeout=10):
        if not c: c = self.current_call
        msg = c.manager.receive_response(c, timeout=10)
        if msg.type == 'BYE':
            self.send_response(msg, '200', 'OK')
            c.manager.close(c)
            return
        raise Unexpected(msg.type, 'BYE', msg)

    def read_sip(self):
        while True:
            #try:
			data = self.socket.read(65535)
            #except:
                #data = None
                
			try:
				msg = SIPMsg.parse(data)
			except Exception as e:
				#import traceback
				continue

			#print("The received sip message is %s\n" %(msg.build()))
			self.log.debug("%s: The received sip message is %s\n" %(self.mac_address, msg.build()))
			if msg.type == 'UPDATE' and  msg.id in self.uas_transactions.open_transactions:
				self.receive_update_thread = gevent.spawn(self.receive_update)

			if (msg.is_response() or msg.id in self.uac_transactions.open_dialogs) and msg.type != 'UPDATE':
				self.uac_transactions.handle_message(msg)
			else:
				self.uas_transactions.handle_message(msg)
			#gevent.sleep(0.1)

    def handle_options(self):
        while True:
            update = self.uas_transactions.receive_new_transaction('OPTIONS',self.options_timeout)
            self.send_response(update, '200', 'OK')
            self.uas_transactions.terminate(update)

    def handle_update(self):
        while True:
            update = self.uas_transactions.receive_new_transaction('UPDATE', timeout=None)
            #self.fix_context()
            self.send_response(update, '200', 'OK')
            self.uas_transactions.terminate(update)


    def send_response(self, req, type, name, content='', headers={}):
        msg = SIPMsg(type, name, {
            'Accept': 'application/conference-info+xml, application/reginfo+xml, application/rlmi+xml,application/sdp, application/simple-message-summary, application/watcherinfo+xml, message/sipfrag, multipart/mixed, application/csta+xml',
            'Via': req.headers['Via'],
            'From': req.headers['From'],
            'To': req.headers['To'],
            'Call-ID': req.headers['Call-ID'],
            'CSeq': req.headers['CSeq'],
        }, content)

        msg.headers.update(headers)
        self.send_sip(msg, True)

    def log(self, msg, header='--'):
        with self:
            debug(msg, header)
            #log(msg, header)

    def __context__(self):
        return {'extension' : '%s-%s' % (self.tenant_id, self.extension)}

    def receive_code(self, call, code):
        result = media_server.wait_for_event(call.id)
        if code == result[1]:
            self.log.debug('receive RTP code %s' % result[1])
        else:
            raise Unexpected('code %s' % result[1], 'code %s' % code)

    def play_dtmf(self, call, tones):
        self.log.debug('play dtmf tones %s' % tones)
        #media_server.new_tone_stream('dtmfraw-%s-%s' % (call.id, tones))
        #media_server.join_bridge(call.id, 'dtmfraw-%s-%s' % (call.id, tones))
        #media_server.play_tone('dtmfraw-%s-%s' % (call.id, tones), tones)
        for i in range(0, len(tones)):
#                       # TODO: read payload type from SDP telephone-event rtpmap
#                       dtmf = call.dtmf_msg(tones[i], 240)
#                       self.execute_transaction(dtmf)

                       media_server.new_dtmf_stream('dtmf-%s' % call.id, tones[i], 240, 102)
                       media_server.join_bridge(call.id, 'dtmf-%s' % call.id)
                       result = media_server.wait_for_event('dtmf-%s' % call.id)
                       if result[0] == 'TIMEOUT STREAM':
                                continue
                       raise Unexpected(result, 'TIMEOUT STREAM')

    def play_bell(self, call, tones):
        media_server.new_tone_stream('tone-%s' % call.id, 'BELLMF')
        media_server.join_bridge(call.id, 'tone-%s' % call.id)
        media_server.play_tone('tone-%s' % call.id, tones)
        result = media_server.wait_for_event('tone-%s' % call.id)
        if result[0] == 'TONE COMPLETE':
            media_server.delete_stream('tone-%s' % call.id)
            return
        raise Unexpected(result, 'TONE COMPLETE')

    def receive_code2(self, call, code):
        self.log.debug('receive RTP code %s' % code)

    def receive_dtmf(self, call, code):
        self.log.debug('receive DTMF %s' % code)

    def receive_bell(self, call, code):
        self.log.debug('receive BELL TONE %s' % code)

    def maintain_registration(self):
        while True:
            gevent.sleep(3000)
            self.register()

    def start_makeme_conference(self, call, last_call):
        makeme_ext = '1108'
        extra_headers = {
            'To': '<sips:%s@%s>;Join=%s;to-tag=%s;from-tag=%s' %
                (makeme_ext, self.switch_ip, last_call.id, last_call.to_tag, last_call.from_tag),
            'Join' :
                '%s;to-tag=%s;from-tag=%s;makeme' % (call.id, call.to_tag, call.from_tag)
        }


        return self.call(makeme_ext, extra_headers=extra_headers)


    def process_meetme_refer(self, r):
        self.process_mesh_refer(r)

    def send_mesh_refer(self, referred_call, target_call):
        refer_id = target_call.id
        branch_id = 'z9hG4bK' + new_id()

        refer = SIPMsg('REFER', target_call.uri, {
            'Accept': 'application/conference-info+xml, application/reginfo+xml, application/rlmi+xml,application/sdp, application/simple-message-summary, application/watcherinfo+xml, message/sipfrag, multipart/mixed, application/csta+xml',
            'Via': 'SIP/2.0/TLS %s:5061;branch=%s;rport;alias' % (self.ip_address, branch_id),
            'From': target_call.ok.headers['From'],
            'To': target_call.ok.headers['To'],
            'Call-ID': refer_id,
            'Min-SE': '90',
            'Session-Expires': '1800',
            'Refer-To': '<%s?Join=%s%%3bto-tag%%3d%s%%3bfrom-tag%%3d%s%%3bmesh>' %
                (referred_call.uri, referred_call.id, referred_call.to_tag, referred_call.from_tag),
        })

        class ReferState:
            pass

        r = ReferState()
        r.id = refer_id
        r.source_ext = self.extension


        #self.log.debug('3 REFER sips:%s@%s %s' % (self.extension, self.switch_ip, r.id), '->')
        self.send_transaction(refer)

        return r

    def process_mesh_refer(self, r):
        iid = new_id()

class BrokenPPhone(PPhone):
    def execute_transaction(self, msg, timeout=10):
        if random.uniform(0,1) < 0.05: raise Exception('random demo failure')
        PPhone.execute_transaction(self, msg, timeout)

if __name__ == '__main__':
    refer = '''REFER sips:55001@10.42.9.1 SIP/2.0
Via: SIP/2.0/TLS 10.42.3.46:5061;alias;rport;branch=z9hG4bK-161837-564e96f0-579554aa-d3815930
Max-Forwards: 70
From: "Conference Ext."<sips:33702@10.42.3.45:5061>;tag=d1ef3dd8-0-13c4-6006-161831-5bbde72-161831
To: <sips:55001@10.42.3.46>;tag=046380098121
Call-ID: 8746462908
CSeq: 3 REFER
Contact: <sips:33702@10.42.3.46:5061;transport=TLS>
Supported: timer,replaces,info
User-Agent: ShoreGear/21.32.1800.0 (ShoreTel 15)
Refer-To: <sips:33702@10.42.3.46?Replaces=00a000004495467d387005056a008d7%3Bto-tag%3DShoreTel_1417538526-1557325808%3Bfrom-tag%3DShoreTel_1417538526-1430675265>
Referred-By: "Conference Ext."<sips:33702@10.42.3.46>
Content-Length: 0
'''

    msg = SIPMsg.parse(refer)
    import urlparse,urllib
    result = urlparse.urlparse(msg.headers['Refer-To'].strip("<>"))
    print(result.query)
    print(urllib.unquote(result.query))

    print(urlparse.urlunparse(result))

    result = urlparse.ParseResult(result.scheme, result.netloc, result.path, '', {}, '')

    print(urlparse.urlunparse(result))

