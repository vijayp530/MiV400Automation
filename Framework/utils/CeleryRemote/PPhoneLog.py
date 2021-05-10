__author__ = 'mkr'

import time
import re
import urllib
import os
import urlparse


class PPhoneLog:
    # def __init__(self):
    #     pass
    #     # self.dutHandle = dutConnector.dutConnector(phone_info)

    def start(self, dut, tcid, log_dir):
        if not dut:
            return False
        # start packet capture
        # cmd = capture start
        shell = dut.get_shell()
        shell.expect('->')
        shell.send(r'capture start')
        shell.expect('->')

    def stop(self, dut, tcid, log_dir):
        if not dut:
            return False
        shell = dut.get_shell()
        shell.expect('->')
        shell.send(r'capture stop')
        shell.expect('->')
        shell.send(r'capture upload')
        shell.expect('.*successfully.*->')
        shell.send(r'log upload')
        shell.expect('->', timeout=600)

    def process(self, dut, tcid, log_dir):
        if not dut:
            return False
        # process your log files here
        
        s,out,e = dut.exec_command('grep pcap /var/log/messages | tail -10')
        print(out)
        pcap = None       
        for line in out.split(r'\n'):
            pcap = re.search('(ftp[^\s]*pcap)', line)
            if pcap:
                pcap = pcap.group(1)
                break
        # urllib.urlretrieve(pcap, os.path.join(log_dir,str(tcid)+'_'+dut.device_info['ip']+'_'+pcap.split('/')[-1]))
        
        s,out,e = dut.exec_command('grep tgz /var/log/messages | tail -10')
        print(out)
        tgz = None       
        for line in out.split(r'\n'):
            tgz = re.search('(ftp[^\s]*tgz)', line)
            if tgz:
                tgz = tgz.group(1)
                break
        # urllib.urlretrieve(tgz, os.path.join(log_dir,str(tcid)+'_'+dut.device_info['ip']+'_'+tgz.split('/')[-1]))
        
        with open(os.path.join(log_dir,'PPhone_'+dut.device_info['name']+'.log'),'w') as f:
            text = '-----------------------------\nPPhone : '+str(dut.device_info['name']+'\n')+'PCAP : '+str(pcap)+'\n''TGZ : '+str(tgz)+'\n'+'-----------------------------\n'
            f.write(text)
        print("pcap : " + str(pcap))
        print("tgz : " + str(tgz))


if __name__ == '__main__':
    from SSHService import SSHService
    dut_info = {
        'ip': '10.198.19.27',
        'username': 'admin',
        'pkey': r'hq_rsa',
        'password': ''
    }
    start_time = time.time()
    log_dir = os.path.join('.',r'salogs\100\1')
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    ld = SSHService(dut_info)
    ld.connect()
    print(ld.is_alive())
    plog = PPhoneLog()
    plog.start(ld, 1,log_dir)
    # time.sleep(30)
    plog.stop(ld, 1,log_dir)
    plog.process(ld,1,log_dir)
    print("--- %s seconds ---" % (time.time() - start_time))
