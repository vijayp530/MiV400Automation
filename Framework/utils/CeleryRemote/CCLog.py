__author__ = 'mkr'

import difflib_ex
import time
import os

class CCLog:

    def __init__(self):
        self.logfiles = {}

    def start(self, dut, tcid, log_dir):
        self.logfiles[dut] = []
        # self.logfiles[dut] = [dut.wm.get_latest_file('c:', '\Shoreline Data\Logs\\', 'TMSMain')]
        self.logfiles[dut].append(dut.wm.get_latest_file('c:', '\Program Files (x86)\ShoreTel\ShoreTel Contact Center Server\Log\Bsw-Eos\\', 'syslog%log'))
        self.logfiles[dut].append(dut.wm.get_latest_file('c:', '\Program Files (x86)\ShoreTel\ShoreTel Contact Center Server\Log\ccd2\\', 'ccd'))
        for file in self.logfiles[dut]:
            dut.wm.net_copy_back(file, os.path.join(log_dir, str(tcid)+'_'+dut.device_info['ip'] +'_'+ os.path.basename(file) + 'before'))

    def stop(self, dut, tcid, log_dir):
        for file in self.logfiles[dut]:
            dut.wm.net_copy_back(file, os.path.join(log_dir, str(tcid)+'_'+dut.device_info['ip'] +'_'+ os.path.basename(file) + 'after'))

    def process(self, dut, tcid, log_dir):
        for file in self.logfiles[dut]:
            before = os.path.join(log_dir, str(tcid)+'_'+dut.device_info['ip'] +'_'+ os.path.basename(file) + 'before')
            after = os.path.join(log_dir, str(tcid)+'_'+dut.device_info['ip'] +'_'+ os.path.basename(file) + 'after')
            with open(os.path.join(log_dir, str(tcid)+'_'+dut.device_info['ip']+'_'+ os.path.basename(file)), 'wb') as f:
                f.write("".join(difflib_ex.get_diff(before, after)))
            os.remove(before)
            os.remove(after)

if __name__ == '__main__':
    from WMIService import WMIService
    dut_info = {
        'ip': '10.198.128.160',
        'username': 'administrator',
        'password': 'Shoreadmin1'
    }

    log_dir = os.path.join('.',r'salogs\200\4')
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    wd = WMIService(dut_info)
    wd.connect()
    ccLog = CCLog()
    ccLog.start(wd, 4,log_dir)
    time.sleep(30)
    ccLog.stop(wd, 4,log_dir)
    ccLog.process(wd, 4, log_dir)

