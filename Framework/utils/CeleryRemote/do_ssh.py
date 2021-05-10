__author__ = 'jahnavi'

import paramiko
from Crypto.PublicKey import RSA

from util import windows_machine
class DoSSH():
    def __init__(self):
        pass

    def copy_rsa(self,ip,username,password):
        remotePath=r'C:\\Shoreline Data\keystore\ssh\hq_rsa'
        dest_file=r'C:\hq_rsa'
        self.win_machine=windows_machine.WindowsMachine(ip,username,password)
        self.win_machine.net_copy_back(remotePath,dest_file)

    def ssh_connect_rsa(self,remoteHost,port,username,password):
        try:
            trans = paramiko.Transport((remoteHost,port))
            rsa_key = RSA.importKey((open(r'C:\hq_rsa')).read())
            #rsa_key=paramiko.RSAKey.from_private_key_file(r'C:\hq_rsa')
            trans.connect(username=username,password=password, pkey=rsa_key)
        except Exception as error:
            print("Failed to authenticate ",error)
            raise


    def ssh_connect(self,remoteHost,username,password):
        try:

            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(remoteHost, username=username, password=password)

        except Exception as error:
            print("Failed to authenticate ",error)




sshobj=DoSSH()
#sshobj.copy_rsa("10.198.166.27","administrator","shoreadmin1")
sshobj.ssh_connect_rsa("10.198.17.150",22,"USER_PSP2_01","changeme")