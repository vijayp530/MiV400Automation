
#import sip
import gevent, gevent.socket, gevent.queue, gevent.ssl, ssl, time, logging
import os, random, string, socket, base64
import Util
import re

from robot.api import logger

#from sip import SIPURI
#from sip import *

import MediaServer
media_server = None


def start_media_server():
        global media_server
        media_server = MediaServer.media_server()

class Unexpected(Exception):
    def __init__(self, received, expected):
        self.received = received
        self.expected = expected

    def __str__(self):
        return 'expected %s, received %s' % (self.expected, self.received)

def build_sdp_header(session_id, phone_ip, rtp_ip):
    return 'v=0\no=MXSIP %s 1 IN IP4 %s\ns=SIP Call\nc=IN IP4 %s\nt=0 0\n' % (session_id, phone_ip, rtp_ip)

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

def build_sdp_media(rtp_port, type, rtpmap):
    codec = 0
    result = 'm=audio %s %s %s 102\n' % (rtp_port, type, codec)
    for i in rtpmap:
        result += 'a=%s\n' % i
    result += 'a=sendrecv\n'
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

        self.retries = 0

    @property
    def id(self):
        return self.headers['Call-ID']

    def build(self):
        d = dict(self.headers)
        if self.is_response():
            msg = '%s %s %s\n' % (self.version, self.type, self.uri)
        else:
            msg = '%s %s %s\n' % (self.type, self.uri, self.version)
        for tag in ['Accept', 'Via', 'Route', 'Record-Route', 'Max-Forwards', 'From', 'To', 'Call-ID', 'CSeq', 'Allow', 'Allow-Events', 'Contact', 'Supported', 'User-Agent']:
            if tag in self.headers:
                msg += '%s: %s\n' % (tag, d[tag])
                del d[tag]
        for (header, value) in d.items():
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

        if self.retries > 0:
            result += ' (RETRY %s)' % self.retries
    
        return result

    def get_parameters(self, header):
        components = self.headers[header].split(';')
        parameters = {}
        value = components.pop(0)
        while components:
            i = components.pop(0)
            try:
                pos = index(i, '=')
                parameters[i[0:pos]] = i[pos+1]
            except:
                parameters[i] = None
        return (value_parameters)

    @classmethod
    def parse(cls, msg):
        lines = msg.split('\n')

        header = lines.pop(0).strip('\r').split(' ')
        first_component = header.pop(0)
        if first_component == 'SIP/2.0':
            version = first_component
            type = header.pop(0)
            uri = string.join(header, ' ')
        else:
            type = first_component
            uri = header.pop(0)
            version = header.pop(0)

        headers = {}
        while True:
            line = lines.pop(0).strip('\r')
            i = line.index(':')
            (header, value) = (line[0:i], line[i+2:])
            if header == 'Content-Length':
                break
            headers[header] = value

        content=string.join(lines, '\n').strip('\r\n')

        return cls(type, uri, headers, content, version)

class TransactionManager(object):
    def __init__(self, device):
        self.open_transactions = {}
        self.open_dialogs = {}
        self.device = device

    def new(self, msg):
        self.open_transactions[msg.id] = msg
        return msg.id

    def receive_response(self, msg, timeout=30):
        with gevent.Timeout(timeout):
            retries = 0
            while retries < 7:
                try:
                    with gevent.Timeout(0.2*2**retries):
                        return self.open_transactions[msg.id].queue.get()
                except gevent.Timeout, e:
                    if e.seconds >= timeout:
                        raise Exception('timeout waiting for response to %s' % msg)

                retries += 1

        raise Exception('too many retries waiting for response to %s' % msg)

    def terminate(self, msg):
        del self.open_transactions[msg.id]

    def open(self, dialog):
        self.open_dialogs[dialog.id] = dialog

    def receive_dialog_transaction(self, dialog, timeout=10):
        try:
            with gevent.Timeout(timeout):
                return self.open_dialogs[dialog.id].queue.get()
        except gevent.Timeout, e:
            raise Exception('timeout waiting for transaction for dialog %s' % dialog)

    def close(self, dialog):
        dialog.hangup()
        del self.open_dialogs[dialog.id]

    def empty(self):
        return len(self.open_transactions) == 0 and len(self.open_dialogs) == 0

class UACManager(TransactionManager):
    def __init__(self, device):
        TransactionManager.__init__(self, device)

    def new(self, t, cseq):
        t.headers['CSeq'] = '%s %s' % (cseq, t.type)
        TransactionManager.new(self, t)

    def handle_message(self, msg):
        if msg.id in self.open_transactions:
            self.open_transactions[msg.id].queue.put(msg)
        elif msg.id in self.open_dialogs:
            self.open_dialogs[msg.id].queue.put(msg)
        else:
            print('ignoring unsolicited response: %s' % msg)

class UASManager(TransactionManager):
    def __init__(self, device):
        TransactionManager.__init__(self, device)
        self.new_transactions = {
            'INVITE' : gevent.queue.Queue(),
            'OPTIONS' : gevent.queue.Queue(),
            'NOTIFY' : gevent.queue.Queue(),
            'BYE' : gevent.queue.Queue(),
            'UPDATE' : gevent.queue.Queue(),
            'ACK' : gevent.queue.Queue()
        }

    def receive_new_transaction(self, type, timeout=10):
        try:
            with gevent.Timeout(timeout):
                return self.new_transactions[type].get()
        except gevent.Timeout, e:
            raise Exception('timeout waiting for new %s transaction' % type)

    def handle_message(self, msg):
        if msg.id in self.open_transactions and  msg.headers['CSeq'].split(' ')[1] != 'UPDATE':
            self.open_transactions[msg.id].queue.put(msg)
        elif msg.id in self.open_dialogs and  msg.headers['CSeq'].split(' ')[1] != 'UPDATE':
            self.open_dialogs[msg.id].queue.put(msg)
        else:
            self.new(msg)
            self.new_transactions[msg.type].put(msg)

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
        #self.config = phone.config

        self.local_rtp_port = None
        self.remote_rtp_port = None
        self.rtp_bridge = None
        self.audio_stream = None
        self.queue = gevent.queue.Queue()

        self.audio_stream = None
        #added new flag
        self.end_call = None

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
                self.phone.send_sip(self.cancel)
                return self.cancel


    def handle_codec(self, sdp):
        (header, media) = parse_sdp(sdp)
        for m in media:
            available_codecs = [int(i) for i in m['m'][3:]]

        if 0 not in available_codecs:
            self.end_call = True

    def hangup(self):
        if self.local_rtp_port:
                stats = media_server.delete_stream(self.id)
                if stats:
                        self.phone.log.debug(', '.join(['%s=%s' % (k, v) for k, v in stats.items()]))
                        if type(stats) is tuple: self.phone.log.debug('incoming RTP packets %d, outgoing RTP packets %d' % (stats[0], stats[1]))
                        self.local_rtp_port = None

                if self.audio_stream:
                        media_server.delete_stream(self.audio_stream)
                        self.audio_stream = None

                if self.rtp_bridge:
                        media_server.delete_bridge(self.id)
                        self.rtp_bridge = None

    def build_sdp(self):
        self.sdp_session_id = random.randint(1,10000000)


        sdp = build_sdp_header(self.sdp_session_id, self.phone.ip_address, self.local_rtp_ip)
        sdp += build_sdp_media(self.local_rtp_port, 'RTP/AVP', ['rtpmap:0 PCMU/8000', 'rtpmap:102 telephone-event/8000'])
        return sdp

    def dtmf_msg(self, signal, duration):
        cseq = int(self.invite.headers['CSeq'].split(' ')[0])

        return SIPMsg('INFO', 'sip:%s@%s:5060' % (self.peer, self.switch_ip), {
            'Via': self.invite.headers['Via'],
            'Route': '<sip:%s:5060;lr>' % self.switch_ip,
            'Max-Forwards': '70',
            'From': self.ok.headers['From'],
            'To': self.ok.headers['To'],
            'Call-ID': self.invite.headers['Call-ID'],
            'CSeq': '%s BYE' % cseq,
            'Contact': self.invite.headers['Contact'],
            'Supported': self.invite.headers['Supported'],
            'User-Agent': self.invite.headers['User-Agent'],
            'Content-Type': 'application/dtmf-relay'
        }, 'Signal: %s\nDuration: %s\n')

    def bye_msg(self):
        cseq = int(self.invite.headers['CSeq'].split(' ')[0])

        return SIPMsg('BYE', 'sip:%s@%s:5060' % (self.peer, self.phone.switch_ip), {
            'Via': 'SIP/2.0/UDP %s:5060;rport;branch=%s' % (self.phone.ip_address, self.branch_id),
            'Route': '<sip:%s:5060;lr>' % self.phone.switch_ip,
            'Max-Forwards': '70',
            'From': self.bye_from,
            'To': self.bye_to,
            'Call-ID': self.invite.headers['Call-ID'],
            'CSeq': '%s BYE' % cseq,
            'Contact': '<sip:%s@%s>' % (self.phone.did, self.phone.ip_address),
            'Supported': self.invite.headers['Supported'],
            'User-Agent': self.invite.headers['User-Agent']
        })

    def ack_msg(self):
        cseq = int(self.invite.headers['CSeq'].split(' ')[0])

        return SIPMsg('ACK', 'sip:%s@%s:5060' % (self.peer, self.switch_ip), {
            'Via': self.invite.headers['Via'],
            'Route': '<sip:%s:5060;lr>' % self.switch_ip,
            'Max-Forwards': '70',
            'From': self.ok.headers['From'],
            'To': self.ok.headers['To'],
            'Call-ID': self.invite.headers['Call-ID'],
            'CSeq': '%s ACK' % cseq,
            'Contact': self.invite.headers['Contact'],
            'Supported': self.invite.headers['Supported'],
            'User-Agent': self.invite.headers['User-Agent']
        })

    def ack_msg_hg(self, targeturl, request=None):
                if not request: request = self.ok
                cseq = int(request.headers['CSeq'].split(' ')[0])

                return SIPMsg('ACK', targeturl, {
                        'Via': request.headers['Via'],
                        'Route': '<sips:%s:5061;transport=tls;lr>' % self.switch_ip,
                        'From': request.headers['From'],
                        'To': request.headers['To'],
                        'Call-ID': request.headers['Call-ID'],
                        'CSeq': '%s ACK' % cseq,
                })


    def handle_reinvite(self, invite):
        self.invite = invite

        (header, media) = parse_sdp(invite.content)
        self.remote_rtp_ip = header['c'][2]
        self.remote_rtp_port = None
        for m in media:
            if m['m'][2] == 'RTP/AVP':
                self.remote_rtp_port = m['m'][1]
        if self.remote_rtp_port == None:
            print("warning: couldn't find RTP port")


    def ok_msg(self):
        if not self.local_rtp_port:
                (_, self.local_rtp_port, self.local_rtp_ip) = media_server.new_rtp_stream(self.id, self.phone.ip_address, self.remote_rtp_ip, self.remote_rtp_port)
                media_server.join_bridge(self.id, self.id)
        else:
                self.local_rtp_port = 10000
                self.local_rtp_ip = self.phone.ip_address

        sdp = self.build_sdp()

        self.ok = SIPMsg('200', 'OK', {
            'Accept': 'application/conference-info+xml, application/reginfo+xml, application/rlmi+xml,application/sdp, application/simple-message-summary, application/watcherinfo+xml, message/sipfrag, multipart/mixed, application/csta+xml',
            'Via': self.invite.headers['Via'],
            'Max-Forwards': '70',
            'From': self.invite.headers['From'],
            'To': '%s;tag=%s' % (self.invite.headers['To'], self.to_tag),
            'Call-ID': self.invite.headers['Call-ID'],
            'CSeq': self.invite.headers['CSeq'],
            'Allow': 'ACK, BYE, CANCEL, INFO, INVITE, NOTIFY, OPTIONS, PRACK, REFER, SUBSCRIBE, UPDATE',
            'Allow-Events': 'conference, refer, uaCSTA',
            'Contact': '<sip:%s@%s>' % (self.phone.did, self.phone.ip_address),
            'Supported': '100rel, eventlist, from-change, gruu, join, replaces, tdialog, timer, answermode',
            'User-Agent': 'IP485g/802.0.2700.0',
            'Content-Disposition': 'session',
            'Content-Type': 'application/sdp'
        }, sdp)

        return self.ok

    def play_audio(self, audio, loop=False):
		#audio = ("C:/Users/KVeeranan/Desktop/standalone/Mediaserver/hello-world.ulaw")
		audio = os.path.dirname(os.path.dirname(os.path.abspath(__file__))).replace("\\","//") + "//" + ("Mediaserver//%s") %(audio)
		# audio = os.getcwd().replace("\\","//") + "//" + ("Mediaserver//%s") %(audio)
		self.audio_stream = 'audio-%s-%s' % (os.path.basename(audio), self.id)
		media_server.new_sound_stream(self.audio_stream, audio, loop=True, media_type='G711U')
		media_server.join_bridge(self.id, self.audio_stream)
    def send_ringing(self):
        self.send_response('180', 'Ringing', headers = {
            'To' : '%s;tag=%s' % (self.invite.headers['To'], self.to_tag)})

    def send_response(self, type, name, content='', headers={}):
            msg = SIPMsg(type, name, {
            'Accept': 'application/conference-info+xml, application/reginfo+xml, application/rlmi+xml,application/sdp, application/simple-message-summary, application/watcherinfo+xml, message/sipfrag, multipart/mixed, application/csta+xml',
            'Via': self.invite.headers['Via'],
            'From': self.invite.headers['From'],
            'To': self.invite.headers['To'],
            'Call-ID': self.invite.headers['Call-ID'],
            'CSeq': self.invite.headers['CSeq'],
            'Contact': '<sip:%s@%s>' % (self.phone.did, self.phone.ip_address),
        }, content)

            msg.headers.update(headers)

            self.phone.send_sip(msg)


    def re_invite(self, hold=False, deactivate=False, extra_headers=None):
                direction = 'sendrecv'
                if hold: direction = 'sendonly'
                if deactivate: direction = 'inactive'
                self.sdp_session = self.sdp_session + 1
                sdp = self.build_sdp(direction)
                uri = self.uri
                invite = SIPMsg('INVITE', uri, {
                        'Accept': 'application/conference-info+xml, application/reginfo+xml, application/rlmi+xml,application/sdp, application/simple-message-summary, application/watcherinfo+xml, message/sipfrag, multipart/mixed, application/csta+xml',
                        'Via': 'SIP/2.0/TLS %s:5061;branch=%s;rport;alias' % (self.ip_address, self.branch_id),
                        'From': '<sips:%s@%s>;tag=%s' % (self.extension, self.switch_ip, self.from_tag),
                        'To': '<sips:%s@%s>;tag=%s' % (self.peer, self.switch_ip,self.to_tag),
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
    
class OutgoingCall(Dialog):
    def __init__(self, phone, peer):
        Dialog.__init__(self, phone)
        self.peer = peer
        
        self.branch_id = 'z9hG4bK' + new_id()
        self.from_tag = new_id(12)
        self.id = new_id()
        self.ip_address = phone.ip_address
        self.switch_ip = phone.switch_ip
        self.did = phone.did

        #slate.test.test_instance().annotate('call_ids', self.id)
        (_, self.local_rtp_port, self.local_rtp_ip) = media_server.new_rtp_stream(self.id, self.ip_address, self.switch_ip, 0, 0)
        
        #self.local_rtp_port = 10000
        #self.local_rtp_ip = phone.ip_address
        
        sdp = self.build_sdp()

        self.invite = SIPMsg('INVITE', 'sip:%s@%s:5060' % (self.peer, self.switch_ip), {
            'Via': 'SIP/2.0/UDP %s:5060;branch=%s' % (self.ip_address, self.branch_id),
            'Max-Forwards': '70',
            'From': '<sip:%s@%s>;tag=%s' % (self.did, self.ip_address, self.from_tag),
            'To': '<sip:%s@%s>' % (self.peer, self.switch_ip),
            'Call-ID': self.id,
            'Allow': 'ACK, BYE, CANCEL, INFO, INVITE, NOTIFY, OPTIONS, PRACK, REFER, SUBSCRIBE, UPDATE',
            'Contact': '<sip:%s@%s>' % (self.did, self.ip_address),
            'Supported': '100rel, eventlist, from-change, gruu, join, replaces, tdialog, timer, answermode',
            'User-Agent': 'SLATE',
            'Content-Disposition': 'session',
            'Content-Type': 'application/sdp'
        }, sdp)

        self.bye_from = self.invite.headers['From']
        self.bye_to = self.invite.headers['To']

    def receive_ok(self, msg):
        self.ok = msg

        to_header = SIPURI.parse(msg.headers['To'])
        self.to_tag = to_header.parameters['tag']
        self.bye_to = '%s;tag=%s' % (self.invite.headers['To'], self.to_tag)

        (header, media) = parse_sdp(msg.content)
    
        self.handle_codec(msg.content)      
        if self.end_call == True:   
                self.end_call = False
                self.phone.send_ack(self)
                self.phone.send_bye(self)
                raise Exception("codec mismatch: Desired codec not supported by switch\n")

        self.remote_rtp_ip = header['c'][2]
        self.remote_rtp_port = None

        for m in media:
            if m['m'][2] == 'RTP/AVP':
                self.remote_rtp_port = m['m'][1]
            available_codecs = [int(i) for i in m['m'][3:]] 

        if self.remote_rtp_port == None:
            print("warning: couldn't find RTP port")

        media_server.set_stream_endpoint(self.id, self.remote_rtp_ip, self.remote_rtp_port,"g711u")
                        #self.rtp_bridge = self.id
        self.rtp_bridge = media_server.new_bridge(self.id)
        media_server.join_bridge(self.id, self.id)
                        #media_server.set_stream_endpoint(self.id, self.remote_rtp_ip, self.remote_rtp_port, 0)
        #caller_audio = "hello-world"
        caller_audio = self.phone.config.get('caller_audio','hello-world.ulaw')
        self.play_audio(caller_audio)

class IncomingCall(Dialog):
    def __init__(self, phone, invite):
        Dialog.__init__(self, phone)
        self.invite = invite
        from_header=invite.headers['From']
        if '"' in from_header:
            i = from_header[1:].index('"')
            from_header = from_header[i+2:]
        from_header = SIPURI.parse(from_header)
        self.peer = from_header.user
        self.id = invite.headers['Call-ID']

        #slate.test.test_instance().annotate('call_ids', self.id)

        via_header = SIPURI.parse(invite.headers['Via'])
        self.branch_id = via_header.parameters['branch']

        self.to_tag = new_id()

        self.bye_to = invite.headers['From']
        self.bye_from = '%s;tag=%s' % (self.invite.headers['To'], self.to_tag)
        print('*** BYE TO is %s' % self.bye_to)

        self.local_rtp_port = None

        (header, media) = parse_sdp(self.invite.content)
        self.remote_rtp_ip = header['c'][2]
        self.remote_rtp_port = None

        self.handle_codec(self.invite.content)
        if self.end_call == True:
                        self.end_call == False
                        self.send_cancel()      
                        log("codec mismatch: Desired codec not supported by switch\n")

        for m in media:
            if m['m'][2] == 'RTP/AVP':
                self.remote_rtp_port = m['m'][1]
        if self.remote_rtp_port == None:
            print("warning: couldn't find RTP port")
        self.rtp_bridge = self.id
        media_server.new_bridge(self.id)
        callee_audio = self.phone.config.get('callee_audio', 'silence.ulaw')
        self.play_audio(callee_audio)



managers = {}
trunks = {}

def register_trunk(trunk):
    global managers
    global trunks
    if trunk.did not in managers:
        ip = trunk.ip_address
        if ip not in managers:
            managers[ip] = TrunkManager(ip)
        managers[trunk.did] = managers[trunk.ip_address]
        managers[trunk.did].child_count =+ 1
    if trunk.did not in trunks:
        trunks[trunk.did] = trunk

def unregister_trunk(trunk):
    global managers
    global trunks
    if trunk.did in trunks:
        del trunks[trunk.did]
    if trunk.did in managers:
        manager = managers[trunk.did]
        del managers[trunk.did]
        manager.child_count =- 1
        if not manager.child_count:
            manager.shutdown()
            del manager[trunk.ip_address]

class TrunkManager(object):
    def __init__(self, ip_address):
        
        self.socket = gevent.socket.socket(type=gevent.socket.SOCK_DGRAM)
        self.socket.bind((ip_address, 5060))
        self.read_thread = gevent.spawn(self.read_sip)
        self.ip_address = ip_address
        self.child_count = 0
        self.options_received = False
        print("waiting for OPTIONS message\n")
        logger.warn("waiting for OPTIONS message\n")
        while not self.options_received:
            gevent.sleep(1)
        print("OPTIONS message received\n")
        logger.warn("OPTIONS message received\n")
        start_media_server()

    def shutdown(self):
        self.sock.close()
        gevent.kill(self.read_thread)
        gevent.join(self.read_thread)

    def read_sip(self):
        while True:
            (data, source_addr) = self.socket.recvfrom(65535)
            try:
                msg = SIPMsg.parse(data)
            except Exception as e:
                continue

            if msg.type == 'OPTIONS':
                self.handle_options(msg, source_addr)
                continue

            if msg.type == 'UPDATE':
                self.handle_update(msg, source_addr)
                continue

            if msg.is_response():
                key = msg.headers['From'].split(':')[1].split('@')[0][-11:]
            else:
                key = msg.headers['To'].split(':')[1].split('@')[0][-10:]

            global trunks
               
            if key in trunks:
                if msg.type == 'BYE' and not msg.is_response() and msg.id in trunks[key].uas_transactions.open_transactions:
                                    self.receive_terminate_thread = gevent.spawn(trunks[key].receive_terminate)
                print("The receive sip message is %s\n" %(msg.build()))
                trunks[key].handle_msg(msg)
                continue

            if msg.is_response():
                key = msg.headers['From'].split(':')[1].split('@')[0][-10:]
                if key in trunks:
                    print("kalai printing in msg response %s\n" %(msg.build()))
                    trunks[key].handle_msg(msg)
                    continue

    def handle_options(self, req, source_addr):
            msg = SIPMsg('200', 'OK', {
            'Via': req.headers['Via'],
            'From': req.headers['From'],
            'To': req.headers['To'],
            'Call-ID': req.headers['Call-ID'],
            'CSeq': req.headers['CSeq'],
        }, '')

            self.socket.sendto(msg.build(), source_addr)

            if not self.options_received:
                self.options_received = True

    def handle_update(self, req, source_addr):
        msg = SIPMsg('200', 'OK', {
                        'Via': req.headers['Via'],
                        'From': req.headers['From'],
                        'To': req.headers['To'],
                        'Call-ID': req.headers['Call-ID'],
                        'CSeq': req.headers['CSeq'],
                }, '')
        self.socket.sendto(msg.build(), source_addr)

class Trunk():
    
    def __init__(self,config,cluserName, log_h):
		# import rpdb2; rpdb2.start_embedded_debugger('admin1') 

		self.did = config[cluserName]['trunkDID']
		self.ip_address = config[cluserName]['trunkIP']
		self.switch_ip = config[cluserName]['trunkSwitchIP']      
		self.ring_duration = config[cluserName]['RingDuration']      
		self.ring_duration = int(re.search('\d+',self.ring_duration).group())     
		self.call_duration = config[cluserName]['CallDuration']      
		self.call_duration = int(re.search('\d+',self.call_duration).group())     

		self.uac_transactions = UACManager(self)
		self.uas_transactions = UASManager(self)
		self.calls = {}
		self.cseq = 0
		self.config = config[cluserName]
		self.log = log_h
		register_trunk(self)

    def __str__(self):
        return 'Trunk(%s)' % self.did

    def boot(self):
        pass

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

                def shutdown_dialog(dialog):
                        try:
                                while not dialog.queue.empty():
                                        msg = dialog.queue.get()

                                        if msg.type == 'BYE':
                                                self.send_response(msg, '200', 'OK')
                                                return
                #if self.connected == 1:
                                        if dialog.manager.open_dialogs[dialog.id]:
                                                self.execute_transaction(dialog.bye_msg())
                        except:
                                pass

                for d in self.uac_transactions.open_dialogs.values():
                        shutdown_dialog(d)

                for d in self.uas_transactions.open_dialogs.values():
                        shutdown_dialog(d)

                unregister_trunk(self)

    def sleep_ring_duration(self):
        time.sleep(int(self.ring_duration))

    def sleep_call_duration(self):
        time.sleep(int(self.call_duration))

    def call(self, extension):
        c = self.invite(extension)
        self.receive_invite_response(c, '100')
        self.current_call = c
        return c

    def send_reinvite(self, call):
                call.branch_id = 'z9hG4bK' + new_id()
                okmsg = call.ok
                si = okmsg.headers['Contact'].index('<')
                ei = okmsg.headers['Contact'].index('>')
                targeturl = okmsg.headers['Contact'][si+1:ei]

                call.uri = targeturl #urlparse.urlunparse(urlparse.ParseResult('sips', '', '%s@%s:5061' % (call.peer, self.config.switch_ip), '', '', ''))
                invite = call.re_invite()
                call.reinvite = invite
                self.send_transaction(invite)
    
    def receive_reinvite_response(self, call):
                result = self.uac_transactions.receive_response(call.reinvite, timeout=10)
                if result.type != '200':
                        raise Unexpected(result.type, '200')
                self.send_sip(call.ack_msg_hg(call.uri, result), True)
                self.uac_transactions.terminate(result)


    def invite(self, destination):
        c = OutgoingCall(self, destination)
        c.manager = self.uac_transactions
        self.uac_transactions.open(c)
        self.send_transaction(c.invite)
        return c

    def receive_invite_response(self, c, type):
        msg = self.uac_transactions.receive_response(c.invite)
        if msg.type == '403':
            c.ok = msg
            self.send_ack(c)
            raise Exception("Call disconnected due to codec mismatch")
        if msg.type == type:
            return
        raise Unexpected(msg.type, type)

    def receive_answer(self, c):
        while True:
            msg = self.uac_transactions.receive_response(c.invite)
            if msg.type == '200':
                c.receive_ok(msg)
                return
            if msg.type == '180':
                continue
            if msg.type == '100':
                continue
            if msg.type == '403':
                self.send_ack(c)
                continue
            break
        raise Unexpected(msg.type, '200')

    def receive_invite(self):
        invite = self.uas_transactions.receive_new_transaction('INVITE')
        c = IncomingCall(self, invite)
        c.manager = self.uas_transactions
        self.uas_transactions.open(c)
        self.current_call = c
        return c

    def receive_reinvite(self, c):
        invite = self.uac_transactions.receive_response(c.invite)
        c.handle_reinvite(invite)

    def receive_refer(self, c):
        refer = self.uac_transactions.receive_response(c.invite)
        return refer

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




    def send_ringing(self, c):
        c.send_ringing()

    def answer(self, c):
        self.send_sip(c.ok_msg())
    
    def send_ack(self, c):
        # ACKs are weird, they're like half a transaction
        self.send_sip(c.ack_msg())

    def receive_ack(self, c):
        ack = self.uas_transactions.receive_response(c)
        self.uas_transactions.terminate(ack)

    def receive_cack(self, c):
        ack = self.uac_transactions.receive_response(c)

    def send_transaction(self, t):
        self.cseq += 1
        self.uac_transactions.new(t, self.cseq)
        self.send_sip(t)

    def resend_transaction(self, t):
        #t.retries += 1
        self.send_sip(t)

    def execute_transaction(self, msg):
        self.send_transaction(msg)
        result = self.uac_transactions.receive_response(msg)
        self.uac_transactions.terminate(msg)
        return result

    def send_sip(self, msg):
        data = msg.build()
        print("Sent sip message is %s\n" %data)
        self.log.debug("sent sip message is %s\n" %data)
        result = managers[self.did].socket.sendto(data, (self.switch_ip, 5060))

        cseq_type = msg.headers['CSeq'].split(' ')[1]
        suppress = ['OPTIONS', 'NOTIFY', 'UPDATE']

    def handle_msg(self, msg):
            print("Received sip message is %s\n" %(msg.build()))
            self.log.debug("Received sip message is %s\n" %(msg.build()))
            if (msg.is_response() or msg.id in self.uac_transactions.open_dialogs) and msg.type != 'UPDATE':
                self.uac_transactions.handle_message(msg)
            else:
                self.uas_transactions.handle_message(msg)

    def send_bye(self, c):
        if c.manager.open_dialogs[c.id]:
            bye = c.bye_msg()
            result = self.execute_transaction(bye)
            if result.type != '200':
                            raise Unexpected(result.type, '200')
            c.manager.close(c)

    def receive_bye(self, c):
        if not c: c = self.current_call
        msg = c.manager.receive_dialog_transaction(c)
        if msg.type == 'BYE':
            self.send_response(msg, '200', 'OK')
            c.manager.close(c)
            return
        raise Unexpected(msg.type, 'BYE')

    def receive_terminate(self, c=None, bye_timeout = 10):
                if not c: c = self.current_call
                msg = c.manager.receive_response(c, bye_timeout)
                if msg.type == 'BYE':
                        self.send_response(msg, '200', 'OK')
                        c.manager.close(c)
                        return
                raise Unexpected(msg.type, 'BYE')

    def handle_options(self):
        while True:
            update = self.uas_transactions.receive_new_transaction('OPTIONS')
            self.send_response(update, '200', 'OK')

    def handle_update(self):
        while True:
            update = self.uas_transactions.receive_new_transaction('UPDATE',timeout=None)
            self.send_response(update, '200', 'OK')

    def send_response(self, req, type, name, content=''):
            msg = SIPMsg(type, name, {
            'Accept': 'application/conference-info+xml, application/reginfo+xml, application/rlmi+xml,application/sdp, application/simple-message-summary, application/watcherinfo+xml, message/sipfrag, multipart/mixed, application/csta+xml',
            'Via': req.headers['Via'],
            'From': req.headers['From'],
            'To': req.headers['To'],
            'Call-ID': req.headers['Call-ID'],
            'CSeq': req.headers['CSeq'],
            'Allow': 'ACK, BYE, CANCEL, INFO, INVITE, NOTIFY, OPTIONS, PRACK, REFER, SUBSCRIBE, UPDATE',
            'Allow-Events': 'conference, refer, uaCSTA',
            'Contact': '<sip:%s@%s>' % (self.did, self.ip_address),
            'Supported': '100rel, eventlist, from-change, gruu, join, replaces, tdialog, timer, answermode'
        }, content)

            self.send_sip(msg)


    def __context__(self):
        return {'extension' : '%s' % (self.did)}


