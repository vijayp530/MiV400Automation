"""Module for custom exception handling
   Author: Milton Villeda
"""
__author__ = "mvilleda"

import os
import sys
import time
import selenium
from selenium import webdriver
import paramiko
from sys import platform as _platform
from scp import SCPClient
import datetime

from disable_exception import disable_exception

from robot.libraries.BuiltIn import BuiltIn
from robot.libraries.Collections import Collections

class exception_handler(object):
    ''' Custom exception handler
    '''

    _DEFAULT_TIMEOUT = 10
    ROBOT_LIBRARY_SCOPE = 'GLOBAL'

    def __init__(self, browser, is_mt="false"):
        # import rpdb2; rpdb2.start_embedded_debugger('admin1')
        is_mt = BuiltIn().get_variable_value("${is_runtype_mt}")
        self.is_mt = is_mt.lower()
        # logger.info("MT enabled: %s " % self.is_mt )
        
        if _platform == "linux" or _platform == "linux2":
            # linux
            self.os_atf_path = LINUX_ATF_PATH
        elif _platform == "darwin":
            self.os_atf_path = MAC_ATF_PATH
            # OS X
        elif _platform == "win32":
            # Windows...
            self.os_atf_path = os.path.dirname(os.path.dirname(__file__))

        self._screenshot_index = 0
        self._browser = browser
        
        if self.is_mt == "false":
            self.pphone_hq_rsa = os.path.join(self.os_atf_path, 'phone_wrappers','phone_4xx','rsa_keys','hq_rsa')
        else:
            self.pphone_hq_rsa = os.path.join(self.os_atf_path, 'phone_wrappers','phone_4xx','rsa_keys','mt_hq_rsa')
            
    def pphone_get_dm_dumps(self, fn, ts):
        """Runs cmd via ssh on pphone user
        
        :param user: User dict
        :type user: type dict
        :param cmd: ssh cmd
        :type cmd: type str
        :return ret_val: ssh cmd result
        """
        for i in range(1,4):
            user = "${user0%s.ip}"%i
            user_ip = BuiltIn().get_variable_value(user)
            filename = "dmdump_" + user_ip + "_" + ts + fn + ".txt"
            filename = filename.replace(':','-')
            self.ssh = paramiko.SSHClient()
            self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            self.ssh.connect(user_ip,username="admin",key_filename=self.pphone_hq_rsa)
            
            cmd = "cli -c getdm > dmdump.txt"
            # logger.warn("Running ssh cmd: \"%s\"" % cmd)
            stdin, stdout, stderr = self.ssh.exec_command(cmd, get_pty=True)
            result = stdout.readlines()

            scp = SCPClient(self.ssh.get_transport())
            dump_path = os.path.join(os.getcwd(),"_dumps",filename)
            scp.get('/home/admin/dmdump.txt',dump_path)
                
            if  self.ssh:
                 self.ssh.close()
        return result

    def exception_cleanup(self, fn):
        """
            This function is called on any exception in the component
            and page classes
        """
        if not disable_exception:

            ts = str(datetime.datetime.now()).split('.')[0]

            return_msg = self.save_screenshot(fn, ts)        
            self.pphone_get_dm_dumps(fn, ts)
                    
            # Do something else
        else:
            return_msg = "var disable_exception flag enabled. Skipping exception cleanup. "
            
        return return_msg
     
    def create_directory(self, target_dir):
        if not os.path.exists(target_dir):
            try:
                os.makedirs(target_dir)
            except OSError as exc:
                if exc.errno == errno.EEXIST and os.path.isdir(target_dir):
                    pass
                else:
                    raise
                    
    def save_screenshot(self, fn, ts):
        try:        
            target_dir = os.path.join(os.getcwd(),"_screenshots")
            self.create_directory(target_dir)
                    
            testname = os.path.basename(BuiltIn().get_variable_value("${suitesource}"))
            filename = "screenshot-" + testname + "-" + ts + fn +".png"
            filename = filename.replace(':','-')
            path = os.path.join(target_dir,filename)
            
            while os.path.exists(path):
                self._screenshot_index += 1
                filename = "screenshot-" + testname + "-" + fn + "-%d.png" % self._screenshot_index
                path = os.path.join(target_dir,filename)
                
            self._browser._browser.save_screenshot(path)
            return "screenshot saved!"
        except Exception:
            return "screenshot NOT saved!"