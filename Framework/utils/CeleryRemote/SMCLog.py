__author__ = 'Varun Tyagi'

import androidlogutils
import os
import shutil

log_file_location = '/mnt/sdcard/com.shoretel.RADialer/files/'

class SMCLog:
    def __init__(self):
        self.andro = androidlogutils.adbHelper()
        # pass

    def start(self, dut, tcid, log_dir):
        self.andro.removeFiles(dut['udid'],log_file_location)

    def stop(self, dut, tcid, log_dir):
        log_file_name = self.andro.get_latest_file(dut['udid'], log_file_location).strip()
        # print(" -----------------------------------------------------------------")
        if log_file_name:
            tmpdir = os.path.join(log_dir, dut['udid'])
            if not os.path.exists(tmpdir):
                os.makedirs(tmpdir)
            print("Copying File from Device: " + dut['udid'] + " to location: " + os.path.abspath(tmpdir))

            try:
                self.andro.copyFileFromDevice(dut['udid'], log_file_name, log_file_location, tmpdir)
                shutil.copy(os.path.join(tmpdir,log_file_name),os.path.join(log_dir,str(tcid)+'_SMC_'+dut['udid']+'_'+log_file_name))
            finally:
                shutil.rmtree(tmpdir)




    def process(self, dut, tcid, log_dir):
        pass


if __name__ == '__main__':
    import time
    dut_info = {
        'name': '4d00b23e4f04a0ed',
        'ip': '',
        'udid': '4d00b23e4f04a0ed'
    }

    log_dir = os.path.join('.',r'salogs\100\1')
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    smcl = SMCLog()
    smcl.start(dut_info,1, log_dir)
    # time.sleep(20)
    smcl.stop(dut_info,1, log_dir)
