__author__ = 'mkr'

import time
import paramiko
from paramikoe import SSHClientInteraction


class SSHService:
    def __init__(self, device_info):
        self.device_info = device_info
        # do some more initialization

    def connect(self):
        self.sftp = None
        try:
            self.ssh = paramiko.SSHClient()
            self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            # if device info has private key then load it
            if 'pkey' in self.device_info:
                # k = paramiko.RSAKey.from_private_key_file(r'C:\Users\MKR\Desktop\hq_rsa.10.198.166.27')
                k = paramiko.RSAKey.from_private_key_file(self.device_info['pkey'])
                # self.ssh.connect('10.198.18.248', username='admin', pkey=k)
                # print(k)
                self.ssh.connect(self.device_info['ip'], username=self.device_info['username'], pkey=k)
            else:
                self.ssh.connect(self.device_info['ip'], username=self.device_info['username'], password=self.device_info['password'])

            # self.transport = paramiko.Transport(('10.198.18.248', 22))
            # self.transport.connect(username = 'admin', pkey=k)
            try:
                # self.sftp = paramiko.SFTPClient.from_transport(self.ssh.get_transport())
                self.sftp = self.ssh.open_sftp()
            except paramiko.SSHException:
                self.sftp = None
            return True
        except Exception:
            return False


    def is_alive(self):
        try:
            return self.ssh.get_transport().is_active()
        except EOFError:
            return False

    def disconnect(self):
        # disconnect
        self.ssh.close()

    def copyfrom(self, source, dest):
        if self.sftp:
            return self.sftp.get(source, dest)
        else:
            return False

    def copyto(self, source, dest):
        if self.sftp:
            return self.sftp.put(source, dest)
        else:
            return False

    def exec_command(self, command, async=False):
        print("Executing Command : " + str(command))
        stdin , stdout, stderr = self.ssh.exec_command(command)
        status = stdout.channel.recv_exit_status()
        output = "".join(stdout.readlines())
        errors = "".join(stderr.readlines())
        print("Status : " + str(status))
        print("Output : " + output)
        print("Errors : " + errors)
        return status, output, errors

    def get_shell(self):
        # return self.ssh.invoke_shell()
        return SSHClientInteraction(self.ssh, display=True)

if __name__ == '__main__':
    dut_info = {
        'ip': '10.198.159.27',
        'username': 'admin',
        # 'pkey': r'C:\Users\MKR\Desktop\hq_rsa.10.198.166.27',
        'password': 'changeme'
    }
    start_time = time.time()
    ld = SSHService(dut_info)
    ld.connect()
    print(ld.is_alive())
    print("--- %s seconds ---" % (time.time() - start_time))
    ld.copyfrom('/var/log/messages','salogs\messages')
    # ld.copyfrom('/cf/shorelinedata/Logs/STTS-160211.222915.Log', r'C:\test\STTS-160211.222915.Log')
    ld.exec_command('show')
