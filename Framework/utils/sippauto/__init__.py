import os
import sys
from sys import platform as _platform
from os import listdir, rmdir, remove

import psutil
import shutil
import paramiko
import scp as SCPClient

import re
import time

from robot.libraries.BuiltIn import BuiltIn
from robot.libraries.Collections import Collections
from robot.api import logger


# mvilleda - Automation Test

class sippauto(object):
    ROBOT_LIBRARY_SCOPE = 'GLOBAL'
    # ROBOT_LIBRARY_VERSION = VERSION

    def __init__(self, *testbed_dict): 
        # import rpdb2; rpdb2.start_embedded_debugger('admin1')
        self.sipp_host_ip = testbed_dict[0]['SIPP_HOST_IP']
        self.sipp_host_user = testbed_dict[0]['SIPP_HOST_USER']
        self.sipp_host_password = testbed_dict[0]['SIPP_HOST_PASSWORD']
        self.sipp_host_sippdir = testbed_dict[0]['SIPP_HOST_SIPPDIR']
        self.phone_switch_ip = testbed_dict[0]['PHONE_SWITCH_IP']
              
        self.ssh = paramiko.SSHClient()
        self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.ssh.connect(hostname=self.sipp_host_ip, username=self.sipp_host_user, password=self.sipp_host_password,compress = True,look_for_keys=False, allow_agent=False)

        self.sipp_logdir = "_sipplogs"
        # Remove all sipp logs
        self.sipp_remove_remote_logs()

    def __del__(self):
        self.ssh.close()
                

    def sipp_run_cmd_non_block(self, cmd):
        try:
            logger.warn("Running cmd %s" % cmd)
            self.ssh.exec_command(cmd)
        except Exception as err:
            raise Exception("func '%s' - err: '%s'!" % (sys._getframe().f_code.co_name, err)) 

    def sipp_run_cmd(self, cmd):
        try:
            logger.warn("Running cmd %s" % cmd)
            stdin, stdout, ssh_stderr = self.ssh.exec_command(cmd)
            out = stdout.read(); err = ssh_stderr.read();
            
            stdin.flush()
            return out
        except Exception as err:
            raise Exception("func '%s' - err: '%s'!" % (sys._getframe().f_code.co_name, err)) 

    def sipp_remove_remote_logs(self):
        try:
            cmd = 'cd ' + self.sipp_host_sippdir + '; ./run_removelogs.sh'
            self.sipp_run_cmd(cmd)
        except Exception as err:
            raise Exception("func '%s' - err: '%s'!" % (sys._getframe().f_code.co_name, err))
          
    def sipp_register_uas(self, sf, inf):
        try:
            cmd = 'cd ' + self.sipp_host_sippdir + '; xterm -display :0 -e ./sipp '
            cmd = cmd + self.phone_switch_ip + ' -sf ' + sf + ' -inf ' + inf
            cmd = cmd + ' -m 1 -i ' + self.sipp_host_ip + ' -trace_err -trace_msg'
            self.sipp_run_cmd(cmd)
            
        except Exception as err:
            raise Exception("func '%s' - err: '%s'!" % (sys._getframe().f_code.co_name, err))
        
    def sipp_register_uac(self, sf, inf):
        try:
            cmd = 'cd ' + self.sipp_host_sippdir + '; xterm -display :0 -e ./sipp '
            cmd = cmd + self.phone_switch_ip + ' -sf ' + sf + ' -inf ' + inf
            cmd = cmd + ' -m 1 -i ' + self.sipp_host_ip + ' -trace_err -trace_msg'
            self.sipp_run_cmd(cmd)
            
        except Exception as err:
            raise Exception("func '%s' - err: '%s'!" % (sys._getframe().f_code.co_name, err))
                         
    def sipp_run_test_snd(self, sf, inf):
        try:
            cmd = 'cd ' + self.sipp_host_sippdir + '; xterm -display :0 -e ./sipp '
            cmd = cmd + self.phone_switch_ip + ' -sf ' + sf + ' -inf ' + inf
            cmd = cmd + ' -m 1 -i ' + self.sipp_host_ip + ' -trace_err -trace_msg'
            self.sipp_run_cmd_non_block(cmd)
            
        except Exception as err:
            raise Exception("func '%s' - err: '%s'!" % (sys._getframe().f_code.co_name, err))
               
    def sipp_run_test_rcv(self, sf):
        try:
            cmd = 'cd ' + self.sipp_host_sippdir + '; xterm -display :0 -e ./sipp '
            cmd = cmd + self.phone_switch_ip + ' -sf ' + sf + ' -m 1 -i ' 
            cmd = cmd + self.sipp_host_ip + ' -trace_err -trace_msg'
            self.sipp_run_cmd_non_block(cmd)
            
        except Exception as err:
            raise Exception("func '%s' - err: '%s'!" % (sys._getframe().f_code.co_name, err))
                      
    def sipp_run_test(self, sf, inf=None):
        try:
            cmd = 'cd ' + self.sipp_host_sippdir + '; xterm -display :0 -e ./sipp ' + self.phone_switch_ip + ' -sf ' + sf 
            if inf is not None:
                cmd = cmd + ' -inf ' + inf
            
            cmd = cmd + ' -m 1 -l 1 -trace_msg -trace_err'
            self.sipp_run_cmd(cmd)
            
        except Exception as err:
            raise Exception("func '%s' - err: '%s'!" % (sys._getframe().f_code.co_name, err))
            
    def backup_sipp_logs(self, tcid):
        try:
            file = self.sipp_host_sippdir + self.remote_filepath
            logger.warn("copying file %s" % file)
            
            scp = SCPClient.SCPClient(self.ssh.get_transport())
            scp.get(file,self.sipp_logdir)
            scp.close()
            
            #rename file
            self.local_sipp_log =  os.path.join(self.sipp_logdir,tcid+'_'+self.sf_file+".log")
            if os.path.isfile(self.local_sipp_log):
                os.remove(self.local_sipp_log)
                
            os.rename(self.local_filepath, self.local_sipp_log)
        except Exception as err:
            raise Exception("func '%s' - err: '%s'!" % (sys._getframe().f_code.co_name, err)) 

            
    def verify_sipp_pass(self, tcid, sf):
        try:
            # import rpdb2; rpdb2.start_embedded_debugger('admin1')
            self.sf_file = os.path.basename(sf).split('.')[0]
            # cmd = 'cd /home/slate/Downloads/sipp-3.3; find . -name "REGISTER_client_UAC*" |grep -v .xml'
            cmd = 'cd ' + self.sipp_host_sippdir + '; find . -name ' + self.sf_file + '_*'
            self.remote_filepath = self.sipp_run_cmd(cmd).strip("./").strip()
            self.local_filepath = os.path.join(self.sipp_logdir,self.remote_filepath.split("/")[1])
            self.backup_sipp_logs(tcid)
            
            #check file for unexpected
            with open(self.local_sipp_log,'r') as fp:
                if "unexpected" in fp.read():
                    logger.warn("FAIL")
                    raise

        except Exception as err:
            raise Exception("func '%s' - err: '%s'!" % (sys._getframe().f_code.co_name, err))        
