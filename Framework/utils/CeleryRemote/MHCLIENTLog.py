__author__ = 'mkr'

import difflib_ex
import time
import os

class MHCLIENTLog:

    def __init__(self):
        self.logfiles = {}

    def start(self, dut, tcid, log_dir):
        if dut:
            self.logfiles[dut] = dut.wm.get_latest_file('c:', '\Users\Administrator\AppData\Local\ShoreTel\Logs\\', 'Connect')
            dut.wm.net_copy_back(self.logfiles[dut], os.path.join(log_dir, str(tcid)+'_'+dut.device_info['ip'] +'_'+ os.path.basename(self.logfiles[dut]) + 'before'))

    def stop(self, dut, tcid, log_dir):
        if dut:
            dut.wm.net_copy_back(self.logfiles[dut], os.path.join(log_dir, str(tcid)+'_'+dut.device_info['ip'] +'_'+ os.path.basename(self.logfiles[dut]) + 'after'))

    def process(self, dut, tcid, log_dir):
        before = os.path.join(log_dir, str(tcid)+'_'+dut.device_info['ip'] +'_'+ os.path.basename(self.logfiles[dut]) + 'before')
        after = os.path.join(log_dir, str(tcid)+'_'+dut.device_info['ip']+'_'+ os.path.basename(self.logfiles[dut]) + 'after')
        try:
            with open(os.path.join(log_dir, str(tcid)+'_'+dut.device_info['ip'] +'_MHCLIENT_'+ os.path.basename(self.logfiles[dut])), 'wb') as f:
                f.write("".join(difflib_ex.get_diff(before, after)))
            os.remove(before)
            os.remove(after)
        except OSError:
            pass

if __name__ == '__main__':
    from windows_machine import WindowsMachine
    dut_info = {
        'ip': '10.198.128.105',
        'username': 'administrator',
        'password': 'shoreadmin1'
    }

    log_dir = os.path.join('.',r'salogs\100\1')
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    wd = WindowsMachine(dut_info['ip'],dut_info['username'],dut_info['password'])

    # wd.connect()
    mhclientlog = MHCLIENTLog()
    mhclientlog.start(wd, 1,log_dir)
    time.sleep(30)
    mhclientlog.stop(wd, 1,log_dir)
    mhclientlog.process(wd, 1, log_dir)

