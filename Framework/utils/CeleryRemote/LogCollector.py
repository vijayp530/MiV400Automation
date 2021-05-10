__author__ = 'mkr'


from util import PPhoneLog,HQLog,MHCLIENTLog,SwitchLog,CCLog,SMRLog,SMCLog,dutConnector, file_handler
import threading
# import gevent
import os
import zipfile
import shutil

from gevent import monkey
monkey.patch_all()

LOG_SERVER_IP = '10.198.159.12'
LOG_SERVER_USER = 'root'
LOG_SERVER_PASSWORD = 'shoreadmin1'
LOG_SERVER_PATH = r'/home/shoretel/salogs'

class LogCollector:
    def __init__(self, l_devices, run_id):
        self.devices = l_devices
        self.run_id = run_id
        self.filehandler = file_handler.FileHandler()
        # connect all devices....
        # self.dut_handles = dutConnector.dutConnector().connect_all(self.devices)
        self.Log = {
            "HQ": HQLog.HQLog(),
            "PPhone": PPhoneLog.PPhoneLog(),
            "SMC": SMCLog.SMCLog(),
            "Switch": SwitchLog.SwitchLog(),
            "MHCLIENT": MHCLIENTLog.MHCLIENTLog(),
            'CC': CCLog.CCLog(),
            'SMR': SMRLog.SMRLog(),
        }
        self.local_log_dir = os.path.join('salogs',str(run_id))
        if not os.path.exists(self.local_log_dir):
            os.makedirs(self.local_log_dir)

    def connect_all_devices(self):
        self.dut_handles = dutConnector.dutConnector().connect_all(self.devices)


    def start(self, tcid, l_devices=None):
        # for dut,dh in zip(self.devices, self.dut_handles):
        # return [self.Log[dut['type']].start(dh, tcid) for dut,dh in zip(self.devices, self.dut_handles)]
        # jobs = [gevent.spawn(self.Log[dut['type']].start, dh,tcid) for dut,dh in zip(self.devices, self.dut_handles)]
        # gevent.wait(jobs)
        if not l_devices:
            l_devices = self.devices
        log_dir = os.path.join(self.local_log_dir, str(tcid))
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)
        threads = [
            threading.Thread(
                    target=self.Log[dut['type']].start,
                    args=(self.dut_handles[dut['name']], tcid, log_dir)
            )
            for dut in l_devices
            ]
        for t in threads:
            t.start()
        for t in threads:
            t.join()


    def stop(self, tcid, l_devices=None):
        # return [self.Log[dut['type']].stop(dh, tcid) for dut,dh in zip(self.devices, self.dut_handles)]
        if not l_devices:
            l_devices = self.devices
        log_dir = os.path.join(self.local_log_dir,str(tcid))
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)
        threads = [
            threading.Thread(
                    target=self.Log[dut['type']].stop,
                    args=(self.dut_handles[dut['name']], tcid, log_dir)
            )
            for dut in l_devices
            ]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

    def process(self, tcid, l_devices=None):
        # process your log files here
        # return [self.Log[dut['type']].process(dh, tcid) for dut,dh in zip(self.devices, self.dut_handles)]
        if not l_devices:
            l_devices = self.devices
        log_dir = os.path.join(self.local_log_dir,str(tcid))
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)
        threads = [
            threading.Thread(
                    target=self.Log[dut['type']].process,
                    args=(self.dut_handles[dut['name']], tcid, log_dir)
            )
            for dut in l_devices
            ]
        for t in threads:
            t.start()
        for t in threads:
            t.join()
        shutil.make_archive(os.path.join(log_dir, '..', 'server_logs_for_testcaseid_'+str(tcid)+'_RoD_runid_'+str(self.run_id)), 'zip', log_dir)

        # zipf = zipfile.ZipFile(os.path.join(log_dir, str(self.run_id)+'_'+str(tcid)+'_Server_Application_Logs.zip'), 'w', zipfile.ZIP_DEFLATED)
        # zipdir(log_dir, zipf)
        # zipf.close()
        # zipit(log_dir, os.path.join(log_dir, str(self.run_id)+'_'+str(tcid)+'_Server_Application_Logs'))
        print("Done processing logs")

    def upload(self, tcid):
        log_dir = os.path.join(self.local_log_dir,str(tcid))
        filename = 'server_logs_for_testcaseid_'+str(tcid)+'_RoD_runid_'+str(self.run_id)+'.zip'
        self.filehandler.sftp_file(
            LOG_SERVER_IP,
            LOG_SERVER_USER,
            LOG_SERVER_PASSWORD,
            os.path.join(log_dir, '..', filename),
            LOG_SERVER_PATH+'/'+str(self.run_id),
            filename
        )

    def purge_sa_logs(self):
        print("inside purge_sa_logs")
        shutil.rmtree(self.local_log_dir)

    def __del__(self):
        self.purge_sa_logs()

def zipit(src, dst):
    zf = zipfile.ZipFile("%s.zip" % (dst), "w", zipfile.ZIP_DEFLATED)
    abs_src = os.path.abspath(src)
    for dirname, subdirs, files in os.walk(src):
        for filename in files:
            absname = os.path.abspath(os.path.join(dirname, filename))
            arcname = absname[len(abs_src) + 1:]
            print('zipping %s as %s' % (os.path.join(dirname, filename),)
                                        arcname)
            zf.write(absname, arcname)
    zf.close()
#
# zip("src", "dst")
# def zipdir(path, ziph):
#     # ziph is zipfile handle
#     for root, dirs, files in os.walk(path):
#         for file in files:
#             ziph.write(os.path.join(root, file))

def run_threads(logcollector):
    logcollector.start('1011')
    time.sleep(20)
    logcollector.stop('1011')
    logcollector.process('1011')
    logcollector.upload('1011')

if __name__ == '__main__':
    import time
    from windows_machine import WindowsMachine
    import d2_api
    # l_devices = d2_api.get_dut_info_from_hq('10.198.128.69','admin','changeme')
    # print(l_devices)
    start_time = time.time()
    # dut_info = {
    #     'ip': '10.198.128.69',
    #     'username': 'administrator',
    #     'password': 'Shoreadmin1'
    # }
    # wd = WindowsMachine(dut_info['ip'],dut_info['username'],dut_info['password'])
    # l_devices = [
    #     {'name': 'HQ', 'type':'HQ', 'os': 'Windows', 'ip':'10.198.166.27', 'username':'administrator', 'password':'shoreadmin1'},
    #     # {'name': 'PPhone1', 'type':'PPhone', 'os': 'Linux', 'ip':'10.198.19.27', 'username':'admin', 'pkey':'hq_rsa.10.198.166.27'},
    #     # {'name': 'PPhone2', 'type':'PPhone', 'os': 'Linux', 'ip':'10.198.18.248', 'username':'admin', 'pkey':'hq_rsa.10.198.166.27'},
    #     {'name': 'vSwitch1', 'type':'Switch', 'os': 'Linux', 'ip':'10.198.166.48', 'username':'admin', 'password':'ShoreTel'},
    #     # {'name': 'SMC1', 'type':'SMC', 'os':'Android', 'id':'06d81c0f'},
    #     # {'name': 'MHCLIENT1', 'type': 'MHCLIENT', 'os': 'Windows', 'ip': '10.198.128.105', 'username': 'administrator', 'password': 'shoreadmin1', 'wm': wd}
    # ]
    l_devices = [
        {'username': 'administrator', 'name': u'Headquarters', 'ip': u'10.198.166.18', 'type': 'HQ', 'password': 'Shoreadmin1', 'os': 'Windows'},
        # {'username': 'admin', 'name': u'vPhoneSwitch', 'ip': u'10.198.159.23', 'type': 'Switch', 'password': 'ShoreTel', 'os': 'Linux'},
        # {'username': 'admin', 'pkey': 'c:\\NextGenArc\\etc\\hq_rsa', 'name': u'SIP-1010-0131019332512345126', 'ip': u'10.198.159.27', 'type': 'PPhone', 'password': '', 'os': 'Linux'},
        # {'udid': '4d00b23e4f04a0ed', 'ip': '', 'os': 'Android', 'type': 'SMC', 'name': '4d00b23e4f04a0ed'},
        # {'udid': '009c8e8b61c6c1c6', 'ip': '', 'os': 'Android', 'type': 'SMC', 'name': '009c8e8b61c6c1c6'},
        # {'username': u'admin', 'name': 'SMR', 'ip': u'10.198.159.27', 'type': 'SMR', 'password': u'changeme', 'os': 'Linux'}
    ]
    logcollector = LogCollector(l_devices,400)
    logcollector.connect_all_devices()
    threads = [
            threading.Thread(
                    target=run_threads,
                    args=[logcollector]
            )
            for i in range(1,3)
            ]
    for t in threads:
        t.start()
    for t in threads:
        t.join()

    logcollector.start('1011')
    # time.sleep(20)
    logcollector.stop('1011')
    logcollector.process('1011')
    # logcollector.upload('1011')
    print("--- %s seconds ---" % (time.time() - start_time))
