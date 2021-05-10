__author__ = 'mkr'

from windows_machine import WindowsMachine
from util import netcopy
import wmi


class WMIService:
    def __init__(self, device_info):
        self.device_info = device_info
        # do some more initialization

    def connect(self):
        try:
            self.wm = WindowsMachine(self.device_info['ip'], self.device_info['username'], self.device_info['password'])
        except Exception:
            self.wm = None

    def disconnect(self):
        del self.wm

    def copyfrom(self, source, dest):
        if self.wm:
            self.wm.net_copy_back(source, dest)
        else:
            netcopy.netcopy(self.device_info['ip'],source, dest, self.device_info['username'], self.device_info['password'])

    def copyto(self, source, dest):
        if self.wm:
            self.wm.net_copy(source, dest)


    def exec_command(self, command, async=False):
        if self.wm:
            return self.wm.run_remote(command, output=True)

    def is_alive(self):
        # how to check wmi connection is alive or not?
        return True

if __name__ == '__main__':
    dut_info = {
        'ip': '10.198.107.18',
        'username': 'administrator',
        'password': 'Shoreadmin1'
    }
    wd = WMIService(dut_info)
    wd.connect()
    print(wd.is_alive())
    print(wd.exec_command('help'))
    wd.copyfrom(r'c:\Shoreline Data\Logs\authenticator-160219.000023.Log',r'.\authenticator-160219.000023.Log')