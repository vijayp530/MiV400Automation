__authhor__ = 'Varun'
__author__ = 'mkr'

import difflib_ex
import os

default_log_location = r"/cf/shorelinedata/Logs"
command_for_latest_log = "ls -t /cf/shorelinedata/Logs | grep STTS | head -n1"

class SwitchLog:

    def __init__(self):
        self.log_files = {}

    def start(self, dut, tcid, log_dir):
        if dut:
            s,log_filename,e = dut.exec_command(command_for_latest_log)
            # print(log_filename)
            self.log_files[dut] = str.rstrip(str(log_filename),'\n')
            dut.copyfrom(default_log_location+"/"+self.log_files[dut], os.path.join(log_dir, str(tcid)+'_'+dut.device_info['ip']+'_'+self.log_files[dut]+'_before'))


    def stop(self, dut, tcid, log_dir):
        if dut:
            dut.copyfrom(default_log_location+"/"+self.log_files[dut], os.path.join(log_dir, str(tcid)+'_'+dut.device_info['ip']+'_'+self.log_files[dut]+'_after'))

    def process(self, dut, tcid, log_dir):
        before = os.path.join(log_dir, str(tcid)+'_'+dut.device_info['ip']+'_'+self.log_files[dut]+'_before')
        after = os.path.join(log_dir, str(tcid)+'_'+dut.device_info['ip']+'_'+self.log_files[dut]+'_after')
        try:
            with open(os.path.join(log_dir, str(tcid)+'_'+dut.device_info['ip']+'_vSwitch_'+ os.path.basename(self.log_files[dut])), 'wb') as f:
                f.write("\n".join(difflib_ex.get_diff(before, after)))
            os.remove(before)
            os.remove(after)
        except OSError:
            pass

if __name__=='__main__':
    from SSHService import SSHService
    dut_info = {
        'ip': '10.198.166.48',
        'username': 'admin',
        'password': 'ShoreTel'
    }

    log_dir = os.path.join('.',r'salogs\100\2')
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    ld = SSHService(dut_info)
    ld.connect()
    swlog = SwitchLog()
    swlog.start(ld, 2,log_dir)
    # time.sleep(30)
    swlog.stop(ld, 2,log_dir)
    swlog.process(ld, 2, log_dir)