__author__ = 'mkr'

from WMIService import WMIService
from SSHService import SSHService

class dutConnector:
    def connect(self, dut_info):
        # connect based on type
        pass

    def is_alive(self, dut):
        # check based on type
        return True

    def disconnect(self):
        # disconnect based on type
        pass

    def connect_all(self, l_devices):
        # for dut in l_devices:
            # module_ = __import__(dut['type']+'Log', fromlist=[dut['type']+'Log'])
        # dut_handles = [getattr(dut['type']+'Log', dut['type']+'Log')(dut) for dut in l_devices]
        dut_handles = {}
        for dut in l_devices:
            print("connecting dut ", dut)
            if dut['os'] == 'Windows':
                # if dut['type'] == 'MHCLIENT':
                #     dut_handles[dut['name']]=dut['wm']
                # else:
                d = WMIService(dut)
                d.connect()
                dut_handles[dut['name']]=d
            elif dut['os'] == 'Linux':
                d = SSHService(dut)
                if not d.connect():
                    d=None
                dut_handles[dut['name']] = d
            elif dut['os'] == 'Android':
                dut_handles[dut['name']] = dut
            else:
                print("Unsupported device os: "+str(dut['os']))
        # [dh.connect() for dh in dut_handles]
        return dut_handles



if __name__ == '__main__':
    l_devices = [
        {'name': 'HQ', 'type':'HQ', 'os': 'Windows', 'ip':'10.198.166.27', 'username':'administrator', 'password':'shoreadmin1'},
        {'name': 'PPhone1', 'type':'PPhone', 'os': 'Linux', 'ip':'10.198.19.27', 'username':'admin', 'pkey':'hq_rsa.10.198.166.27'},
        {'name': 'PPhone2', 'type':'PPhone', 'os': 'Linux', 'ip':'10.198.18.248', 'username':'admin', 'pkey':'hq_rsa.10.198.166.27'},
        {'name': 'vSwitch1', 'type':'Switch', 'os': 'Linux', 'ip':'10.198.166.48', 'username':'admin', 'password':'ShoreTel'},
    ]

    mydutConnector = dutConnector()
    dut_handles = mydutConnector.connect_all(l_devices)