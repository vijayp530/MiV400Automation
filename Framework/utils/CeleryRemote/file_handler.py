###############################################################################
## Module: FileHandler
## File name: FileHandler.py
## Description: Will handles file operaions
##
##
##  -----------------------------------------------------------------------
##  Modification log:
##
##  Date        Engineer    Description
##  ---------   ---------   ---------     
##  27-Nov-14    Jahnavi        Module Created
###############################################################################

#python modules
import sys
import os
import paramiko
import glob
import shutil
import windows_net_copy
from windows_machine import WindowsMachine

class FileHandler:
    def __init__(self):
        #log.setLogHandlers()
        pass
    
    # def open_file(self,filename,mode):
    #     log.mjLog.LogReporter("FileHandler","info","open_file - Opened file "+filename+" successfully")
    #     if os.path.exists(filename):
    #         self.file= open(filename,mode)
    #     else:
    #         self.file=open(filename,'a')
    #     return self.file
    #
    # def read_file(self,filename):
    #     self.file=self.open_file(filename, 'r')
    #     log.mjLog.LogReporter("FileHandler","info","read_file - reading  file "+filename)
    #     return self.file.read()
    #
    #
    # def write_file(self,filename,text):
    #
    #     self.file=self.open_file(filename, "w+")
    #     #log.mjLog.LogReporter("FileHandler","info","write_file - writing text "+text+"  to file"+filename)
    #     return self.file.write(text)
    #
    # def readline_file(self,filename):
    #     self.file=self.open_file(filename,'r')
    #     log.mjLog.LogReporter("FileHandler","info","readline_file - reading firstline from file "+filename)
    #     return self.file.readline()
    #
    # def readlines_file(self,filename):
    #     self.file=self.open_file(filename,'r')
    #     log.mjLog.LogReporter("FileHandler","info","readlines_file - reading the file "+filename)
    #     return self.file.readlines()
    #
    # def close_file(self):
    #     log.mjLog.LogReporter("FileHandler","info","close_file - closing the file ")
    #     self.file.close()
    
    def sftp_dir(self,remoteHost,username,password,localDir,remoteDir):
        ssh = paramiko.SSHClient() 
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        #ssh.load_host_keys()
        ssh.connect(remoteHost, username=username, password=password)
        #transport = paramiko.Transport((remoteHost, 22))
        #transport.connect(username = username, password = password)
        sftp = ssh.open_sftp()
        try:
            sftp.chdir(remoteDir)  # Test if remote_path exists
        except IOError:
            sftp.mkdir(remoteDir)  # Create remote_path
            sftp.chdir(remoteDir)
        for dirname, dirnames, filenames in os.walk(localDir): 
            for filename in filenames:
                print(os.path.join(dirname, filename))
                sftp.put(os.path.join(dirname, filename), filename)    # At this point, you are in remote_path in either case
        sftp.close()
        ssh.close()
    
    def sftp_file(self,remoteHost,username,password,localFn,remoteDir,remoteFn):
        ssh = paramiko.SSHClient() 
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(remoteHost, username=username, password=password)
        sftp = ssh.open_sftp()
        try:
            sftp.chdir(remoteDir)  # Test if remote_path exists
        except IOError:
            sftp.mkdir(remoteDir)  # Create remote_path
            sftp.chdir(remoteDir)
        sftp.put(localFn, remoteFn)
        sftp.close()
        ssh.close()
    
    def remove_files_dir(self,dirname):
        '''
        :param dirname:  will remove all files from given dir
        :return:
        '''
        print("############## removing files from dir")
        files=glob.glob(dirname+"\*")
        for f in files:
            os.remove(f)
    
    def sftp_xml_file(self, remoteHost, username, password, localDir, Fn, remoteDir):
        wm = WindowsMachine(remoteHost, username, password)
        #ssh = paramiko.SSHClient()
        #ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        #ssh.connect(remoteHost, username=username, password=password)
        #sftp = ssh.open_sftp()
        print("REMOTE : ", remoteDir)
        print("FN : ", Fn)
        print("LOCAL : ", localDir)
        #sftp.get(remoteDir+Fn, localDir+Fn)
        wm.net_copy_back(remoteDir+Fn, localDir+Fn)

    def copy_certificate_files(self, hq_ip, hq_username, hq_password, input_params):
        """Copy certificate files from HQ to ATF machine
        """
        try:
            if input_params['project'].lower() == 'cosmo-pseries':
                if os.path.exists(r'Q:\testsuites\shared\testdata\ssh\hq_rsa'):
                    os.remove(r'Q:\testsuites\shared\testdata\ssh\hq_rsa')
                windows_net_copy.netcopy(hq_ip, r'C:\Shoreline Data\keystore\ssh\hq_rsa', r'Q:\testsuites\shared\testdata\ssh', hq_username, hq_password)
                if not os.path.exists(r'Q:\testsuites\shared\testdata\ssh\hq_rsa.'+hq_ip):
                    shutil.copy2(r'Q:\testsuites\shared\testdata\ssh\hq_rsa', r'Q:\testsuites\shared\testdata\ssh\hq_rsa.'+hq_ip)
                if os.path.exists(r'Q:\testsuites\shared\testdata\ssh\hq_rsa.pub'):
                    os.remove(r'Q:\testsuites\shared\testdata\ssh\hq_rsa.pub')
                windows_net_copy.netcopy(hq_ip, r'C:\Shoreline Data\keystore\ssh\hq_rsa.pub', r'Q:\testsuites\shared\testdata\ssh', hq_username, hq_password)
            else:
                if not os.path.exists(r'C:\certs'):
                    os.mkdir(r'C:\certs')
                windows_net_copy.netcopy_dir(hq_ip, r'C:\Shoreline Data\keystore\ssh', r'C:\certs', hq_username, hq_password)
                windows_net_copy.netcopy_dir(hq_ip, r'C:\Shoreline Data\keystore\certs', r'C:\certs', hq_username, hq_password)
                windows_net_copy.netcopy_dir(hq_ip, r'C:\Shoreline Data\keystore\private', r'C:\certs', hq_username, hq_password)
        except Exception as e:
            #self.logger.debug("Error in copying certificate files!")
            raise e

    def add_reverse_proxy(self, tb_info):
        """Add reverse proxy IP and MT_ABCAUTHENTICATION_URL to hosts file
        """
        fobj = open(r'C:\Windows\System32\drivers\etc\hosts', 'r')
        lines = fobj.readlines()
        fobj.close()
        linetoAdd = tb_info['REVERSE_PROXY_IP_FOR_HOST']+"   "+tb_info['MT_ABC_AUTHENTICATION_URL']  # "10.198.78.89    client.start.shoretel.com"
        fobj = open(r'C:\Windows\System32\drivers\etc\hosts', 'w')
        count = 0
        for line in lines:
            if line.startswith("#"):
                fobj.write(line)
            else:
                fobj.write(line)
                if line.rstrip("\n") == linetoAdd:
                    count = count + 1
        if count == 0:
            fobj.write("\n"+linetoAdd)
        fobj.close()
