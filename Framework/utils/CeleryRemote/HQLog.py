__author__ = 'mkr'

import difflib_ex
import time
import os

class HQLog:

    def __init__(self):
        self.logfiles = {}

    def start(self, dut, tcid, log_dir):
        self.logfiles[dut] = dut.wm.get_latest_file('c:', '\Shoreline Data\Logs\\', 'TMSMain')
        dut.wm.net_copy_back(self.logfiles[dut], os.path.join(log_dir, str(tcid)+'_'+dut.device_info['ip'] +'_'+ os.path.basename(self.logfiles[dut]) + 'before'))

    def stop(self, dut, tcid, log_dir):
        dut.wm.net_copy_back(self.logfiles[dut], os.path.join(log_dir, str(tcid)+'_'+dut.device_info['ip']+'_'+ os.path.basename(self.logfiles[dut]) +  'after'))

    def process(self, dut, tcid, log_dir):
        before = os.path.join(log_dir, str(tcid)+'_'+dut.device_info['ip'] +'_'+ os.path.basename(self.logfiles[dut]) + 'before')
        after = os.path.join(log_dir, str(tcid)+'_'+dut.device_info['ip'] +'_'+ os.path.basename(self.logfiles[dut]) + 'after')
        try:
            with open(os.path.join(log_dir, str(tcid)+'_'+dut.device_info['ip']+'_HQ_'+ os.path.basename(self.logfiles[dut])), 'wb') as f:
                f.write("".join(difflib_ex.get_diff(before, after)))
            os.remove(before)
            os.remove(after)
        except OSError:
            pass

if __name__ == '__main__':
    from WMIService import WMIService
    dut_info = {
        'ip': '10.198.166.27',
        'username': 'administrator',
        'password': 'shoreadmin1'
    }

    log_dir = os.path.join('.',r'salogs\100\1')
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    wd = WMIService(dut_info)
    wd.connect()
    hqlog = HQLog()
    hqlog.start(wd, 1,log_dir)
    time.sleep(30)
    hqlog.stop(wd, 1,log_dir)
    hqlog.process(wd, 1, log_dir)

