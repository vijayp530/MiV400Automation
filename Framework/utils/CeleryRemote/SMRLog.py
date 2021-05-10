__authhor__ = 'Varun'
__author__ = 'mkr'

import difflib_ex
import os

log_file = '/var/log/messages'

class SMRLog:

    def __init__(self):
        self.log_files = {}

    def start(self, dut, tcid, log_dir):
        dut.copyfrom(log_file, os.path.join(log_dir, str(tcid)+'_'+dut.device_info['ip']+'_'+os.path.basename(log_file)+'_before'))


    def stop(self, dut, tcid, log_dir):
        dut.copyfrom(log_file, os.path.join(log_dir, str(tcid)+'_'+dut.device_info['ip']+'_'+os.path.basename(log_file)+'_after'))

    def process(self, dut, tcid, log_dir):
        before = os.path.join(log_dir, str(tcid)+'_'+dut.device_info['ip']+'_'+os.path.basename(log_file)+'_before')
        after = os.path.join(log_dir, str(tcid)+'_'+dut.device_info['ip']+'_'+os.path.basename(log_file)+'_after')
        try:
            with open(os.path.join(log_dir, str(tcid)+'_SMR_'+dut.device_info['ip']+'_'+ os.path.basename(log_file)), 'wb') as f:
                f.write("\n".join(difflib_ex.get_diff(before, after)))
            os.remove(before)
            os.remove(after)
        except OSError:
            pass

if __name__=='__main__':
    from SSHService import SSHService
    dut_info = {
        'ip': '10.198.159.27',
        'username': 'admin',
        'password': 'changeme'
    }

    log_dir = os.path.join('.',r'salogs\100\3')
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    ld = SSHService(dut_info)
    ld.connect()
    swlog = SMRLog()
    swlog.start(ld, 2,log_dir)
    # time.sleep(30)
    swlog.stop(ld, 2,log_dir)
    swlog.process(ld, 2, log_dir)