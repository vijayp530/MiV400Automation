
import traceback
import gevent, gevent.queue
from gevent.subprocess import Popen, PIPE
import time
import os
import fnmatch, re

class Transaction:
    def __init__(self, msg):
        self.msg = msg
        self.result_queue = gevent.queue.Queue()

class RtpBridgeInstance:
    def __init__(self, name, remote_host=None):
        self.remote_host = remote_host

        self.transaction_queue = gevent.queue.Queue()
        self.read_queue = gevent.queue.Queue()
        self.event_queue = {}

        def detach_from_pgrp():
            # so that ctrl-c doesn't kill the rtp-bridge processes prematurely
            os.setpgrp()

        self.name = name

        #socket = '/tmp/rtp-bridge-%s' % name
        DEVNULL = open(os.devnull, 'w')
        if self.remote_host:
            self.server = Popen('ssh %s rtp-bridge -s socket' % (self.remote_host), shell=True, stdin=PIPE, stdout=PIPE, stderr=DEVNULL, preexec_fn=detach_from_pgrp)
            # TODO: racey, ensure server is started before starting client
            self.proc = Popen('ssh %s rtp-bridge -r socket' % (self.remote_host), shell=True, stdin=PIPE, stdout=PIPE, stderr=DEVNULL, preexec_fn=detach_from_pgrp)
        else:
            #self.server = Popen('rtp-bridge -s %s' % socket, shell=True, stderr=DEVNULL, preexec_fn=detach_from_pgrp)
            #cmd = "C:\\Users\\KVeeranan\\Desktop\\standalone\\Mediaserver\\rtp-bridge.exe -r C:\\Users\\KVeeranan\\Desktop\\standalone\\Mediaserver\\socket"
            cmd = "Mediaserver\\rtp-bridge.exe -r Mediaserver\\socket"
            self.proc = Popen(cmd, shell=True, stdin=PIPE, stdout=PIPE, stderr=DEVNULL)

        # eat RECOVER_OK message
        self.proc.stdout.readline()

        self.transaction_thread = gevent.spawn(self.process_transactions)
        self.read_thread = gevent.spawn(self.read_thread)

    def shutdown(self):
        #with self:
        #   debug('shutdown, current stack is %s' % ''.join(traceback.format_stack(self.transaction_thread.gr_frame)))

        self.transaction_thread.kill()
        self.transaction_thread.join()

    def read_thread(self):

        while self.proc.poll() is None:
            result = self.proc.stdout.readline().strip('\n')

            if not result:
                continue
                
            if result[0:10] == 'RECOVER_OK':
                continue

            c = False
            for event in ['CODE', 'TONE', 'TIMEOUT']:
                if result[0:len(event)] == event:
                    if log:
                        with self:
                            debug(result, '<-')
                    self.parse_event(result)
                    c = True
                    break

            if c: continue

            self.read_queue.put(result)

        self.read_queue.put('QUIT')
        
    def process_transactions(self):

        while self.proc.poll() is None:
            t = self.transaction_queue.get()

            self.proc.stdin.write(t.msg + '\n')
            self.proc.stdin.flush()

            result = tuple(self.read_queue.get().split(' '))
            t.result_queue.put(result)

            #if log:
            #   with self:
            #       debug('%s' % (result,), '<-')
            #   slate.util.context.pop(t.context)

        #if self.proc.poll():
        #   with self:
        #       debug('media server remote died with result %s' % self.proc.poll())

    def cmd(self, command, stream_name=None, cleanup_func=None):
        if stream_name:
            self.event_queue[stream_name] = gevent.queue.Queue()

        if cleanup_func:
            def cleanup(greenlet):
                if stream_name in self.event_queue:
                    cleanup_func(stream_name)
            #gevent.getcurrent().link(cleanup)

        #print('-> ' + command)
        t = Transaction(command)
        self.transaction_queue.put(t)
        result = t.result_queue.get()
        #print('<<- %s: %s' % (command, result))
        if result[0] == 'ERROR':
            raise Exception('Error: %s\nWhen processing command: %s' % (result, command))
        return result

    def parse_event(self, s):
        event = s.split(' ')
        if event[0] == 'CODE':
            name = 'CODE DETECT'
            stream_id = event[2]
            parameters = '%s%s%s' % (event[3], event[4], event[5])
        elif event[0] == 'TONE':
            name = 'TONE COMPLETE'
            stream_id = event[2]
            parameters = None
        elif event[0] == 'TIMEOUT' and event[1] == 'STREAM':
            name = 'TIMEOUT STREAM'
            stream_id = event[2]
            parameters = None
        elif event[0] == 'TIMEOUT' and event[1] == 'BRIDGE':
            debug('WARNING: bridge timeout %s' % event[2])
            # TODO: what to do here?
            return
        else:
            debug('unknown event %s' % event[0])
            return
        self.event_queue[stream_id].put((name, parameters))

    def wait_for_event(self, stream_id):
        return self.event_queue[stream_id].get()

    def __context__(self):
        return {'media_server_name' : 'rtp-bridge-%s' % self.name}


class MediaServer:
    def __init__(self):
        count = '1'
        #self.servers = [RtpBridgeInstance('%s' % i) for i in range(0, count)]
        self.servers = [RtpBridgeInstance(0)]

        self.listen_server = None
        self.listen_bridges = []

        #self.config = slate.config.get('media', {})
        #if 'remote_listen_host' in self.config:
        if False:
            self.listen_server = RtpBridgeInstance(name, remote_host = self.config.remote_listen_host)
            self.listen_thread = gevent.spawn(self.manage_listen_server)
            self.listen_queue = gevent.queue.Queue()

            self.listen_server.cmd('new rtp_bridge listen_bridge')
            self.listen_server.cmd('new alsa_stream alsa_stream')
            self.listen_server.cmd('join listen_bridge alsa_stream')

    def shutdown(self):
        for server in self.servers:
            server.shutdown()
        if self.listen_server: self.listen_server.shutdown()

    def wait_for_event(self, stream_id):
        return self.server.wait_for_event(stream_id)

    def new_rtp_stream(self, name, local_ip, remote_ip, remote_port, media_type='ULAW'):
        return self.server.cmd("new rtp_stream %s %s %s %s %s" % (name, local_ip, remote_ip, remote_port, media_type),
            name, self.delete_stream)

    def new_sound_stream(self, name, file, loop=False, media_type='ULAW'):
        return self.server.cmd('new sound_stream %s %s %s %s' % (name, file, 'loop' if loop is True else 'noloop', media_type),
            name, self.delete_stream)

    def new_alsa_stream(self, name):
        return self.server.cmd('new alsa_stream %s' % name, name, self.delete_stream)

    def new_tone_stream(self, name, type='DTMF', detect=False):
        return self.server.cmd('new tone_stream %s %s %s' % (name, type, 1 if detect else 0), name, self.delete_stream)

    def new_dtmf_stream(self, name, tone, duration, payload):
        return self.server.cmd('new dtmf_stream %s %s %s %s' % (name, tone, duration, payload), name, self.delete_stream)

    def play_tone(self, name, tones):
        return self.server.cmd('play tone %s %s' % (name, tones))

    def new_bridge(self, name):
        if name[0:7] != 'bridge-':
            name = 'bridge-%s' % name
        if self.listen_server and len(self.listen_bridges) < int(self.config.listen_count):
            if re.compile(fnmatch.translate(self.config.listen_match)).match(name):
                self.listen_bridges.append(name)
                self.listen_queue.put(('listen', name))
        return self.server.cmd("new rtp_bridge %s" % name, cleanup_func=self.delete_bridge)

    def join_bridge(self, bridge_name, stream_name):
        if bridge_name[0:7] != 'bridge-':
            bridge_name = 'bridge-%s' % bridge_name
        return self.server.cmd('join %s %s' % (bridge_name, stream_name))

    def set_stream_endpoint(self, name, remote_ip, remote_port, codec):
        return self.server.cmd('set stream %s endpoint %s %s' % (name, remote_ip, remote_port))

    def set_stream_encryption(self, name, incoming_key, outgoing_key):
        return self.server.cmd('set stream %s encryption %s %s' % (name, incoming_key, outgoing_key))

    def delete_stream(self, name):
        stats = {}
        try:
            result = self.server.cmd('delete stream %s' % name)
            if result[0] == 'SUCCESS':
                for stat in result[1:]:
                    name, value = stat.split("=")
                    stats[name] = value
        except Exception as e:
            result = ('SUCCESS',)
        if name in self.server.event_queue:
            del self.server.event_queue[name]
        return stats

    def delete_bridge(self, name):
        if name[0:7] != 'bridge-':
            name = 'bridge-%s' % name

        if name in self.listen_bridges:
            self.remote_media_queue.put(('delete', name))
            del self.listen_bridges[name]
        result = self.server.cmd('delete bridge %s' % name)
        if name in self.server.event_queue:
            del self.server.event_queue[name]
        return result

    def manage_listen_server(self):
        # TODO: play some ticking or something when no other stream is in bridge?
        while True:
            (action, name) = self.listen_queue.get()

            if action == 'listen':
                (_, remote_port, remote_host) = self.listen_server.cmd('new rtp_stream %s 127.0.0.1 0 ULAW' % name)
                remote_host = '10.10.127.225'
                print('-- listening to bridge %s, remote host is %s' % (name, remote_host))
                (_, local_port, local_host) = self.server.cmd('new rtp_stream listen-%s %s %s ULAW' % (name, remote_host, remote_port))
                self.listen_server.cmd('set stream %s endpoint %s %s' % (name, local_host, local_port))
                self.listen_server.cmd('join listen_bridge %s' % name)
                self.server.cmd('join %s listen-%s' % (name, name))
            elif action == 'delete':
                print('-- no longer listening to bridge %s' % name)
                self.listen_server.cmd('delete stream %s' % name)
                self.server.cmd('delete stream listen-%s' % name)
            else:
                print('-- warning: manage_listen_server ignoring unknown action (%s, %s)' % (action, name))

    @property
    def server(self):
        return self.servers[0]

_media_server = None

def media_server():
    global _media_server
    if not _media_server: _media_server = MediaServer()
    return _media_server

if __name__ == '__main__':
    m = MediaServer()
    key1 = "123456789012345678901234567890"
    key2 = "098765432109876543210987654321"
    for i in range(1, 500):
        m.new_sound_stream("mohA%s" % i, '/opt/cfi/var/media/moh/fpm-world-mix.ulaw', loop=True)
        (_, hosta, porta) = m.new_rtp_stream("rtpA%s"% i, '10.0.3.1', 65535)
        m.set_stream_encryption("rtpA%s" % i, key1, key2)
        m.new_sound_stream("mohB%s" % i, '/opt/cfi/var/media/moh/fpm-world-mix.ulaw', loop=True)
        (_, hostb, portb) = m.new_rtp_stream("rtpB%s"% i, '10.0.3.1', porta)
        m.set_stream_encryption("rtpB%s" % i, key2, key1)
        m.set_stream_endpoint("rtpA%s" % i, '10.0.3.1', portb)
        m.new_bridge("A%s" % i)
        m.new_bridge("B%s" % i)
        m.join_bridge("A%s" % i, "rtpA%s" % i)
        m.join_bridge("B%s" % i, "rtpB%s" % i)
        m.join_bridge("A%s" % i, "mohA%s" % i)
        m.join_bridge("B%s" % i, "mohB%s" % i)
    while True:
        time.sleep(1.0)


