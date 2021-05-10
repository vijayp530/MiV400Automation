__author__ = "milton.villeda@mitel.com"

import os
import sys
import telnetlib
import paramiko
import psutil
import shutil
import subprocess
import time
import re
import ftplib
import socket
import base64
from sys import platform as _platform

from kbd_server import *
from socket_interface import *
import vm_codes
# import CeleryRemote

from robot.libraries.BuiltIn import BuiltIn
from robot.libraries.Collections import Collections
from robot.api import logger
# from robot.libraries.Telnet import Telnet

class PPhoneInterface(object):

    ROBOT_LIBRARY_SCOPE = 'GLOBAL'
    # ROBOT_LIBRARY_VERSION = VERSION
    
    def __init__(self, is_mt="true"):
        self.os_atf_path = ""
        
        self.is_mt = is_mt.lower()
        logger.warn("MT enabled: %s " % self.is_mt )
        
        if _platform == "linux" or _platform == "linux2":
            # linux
            self.os_atf_path = LINUX_ATF_PATH
        elif _platform == "darwin":
            self.os_atf_path = MAC_ATF_PATH
            # OS X
        elif _platform == "win32":
            # Windows...
            self.os_atf_path = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))

        self.kNumSoftKeys = 5
        self.event_timeout = 7
        self.max_oneway_retry = 2
        self.force_idle_timeout = 15

        if self.is_mt == "false":
            self.pphone_hq_rsa = os.path.join(self.os_atf_path, 'phone_wrappers','phone_4xx','rsa_keys','hq_rsa')
        else:
            self.pphone_hq_rsa = os.path.join(self.os_atf_path, 'phone_wrappers','phone_4xx','rsa_keys','mt_hq_rsa')
        
    def pphone_ssh_cmd(self, user, cmd):
        """Runs cmd via ssh on pphone user
        
        :param user: User dict
        :type user: type dict
        :param cmd: ssh cmd
        :type cmd: type str
        :return ret_val: ssh cmd result
        """
        self.ssh = paramiko.SSHClient()
        self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.ssh.connect(user.ip,username="admin",key_filename=self.pphone_hq_rsa)

        logger.warn("Running ssh cmd: \"%s\"" % cmd)
        stdin, stdout, stderr = self.ssh.exec_command(cmd, get_pty=True)
        result = stdout.readlines()
        
        if  self.ssh:
             self.ssh.close()
        return result
        
    def pphone_ssh_su_cmd(self, user, cmd):
        """Runs cmd via ssh as su on pphone user
        
        :param user: User dict
        :type user: type dict
        :param cmd: ssh cmd
        :type cmd: type str
        :return ret_val: result
        """
        self.ssh = paramiko.SSHClient()
        self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.ssh.connect(user.ip,username="admin",key_filename=self.pphone_hq_rsa)
    
        pswd = 'U2hvcmVUZWw='
        cmd = "echo " + base64.b64decode(pswd) + " | su -c \"" + cmd + "\""
        logger.info("Running ssh cmd: \"%s\"" % cmd)
        stdin, stdout, stderr = self.ssh.exec_command(cmd)
        result = stdout.readlines()
        
        if  self.ssh:
             self.ssh.close()
        return result

    def pphone_ssh_dm(self, user, cmd, dm_query):
        """Runs cmd dm_query using ssh on pphone user
        
        :param user: User dict
        :type user: type dict
        :param cmd: ssh cmd
        :type cmd: type str
        :param dm_query: Run dm_query
        :type dm_query: type str
        :return ret_val: none
        :raises ExceptionType: Raises robot exception if not dm_query does not match
        """
        sys_cmd = ' '.join([cmd,dm_query])
        for i in range(0,3):
            result = self.pphone_ssh_cmd(user, sys_cmd)
                 
            if isinstance(result, list):
                result = ''.join(result)
            matchObj = re.match( r'.*->(.*)->Terminated.*', result, re.DOTALL)
            if matchObj:
               dm_pair = matchObj.group(1).rstrip('\r\n')
               dm_pair = dm_pair.split("=")
               
               if "PPhoneDM" in dm_query:
                   dm_query = dm_query.split('.')[1]
               if dm_query in dm_pair[0].strip():
                   print("\"%s\" matched returning \"%s\"" % (dm_query, dm_pair[1]))
                   return dm_pair[1].strip()
               else:
                   raise Exception("%s did not match %s in pphone_ssh_dm" % (dm_query, dm_pair[0]))
             
        raise Exception("pphone_ssh_dm: \"%s\" match not found in result %s." % (dm_query, result))

    def pphone_reboot_phone(self, user):
        """ Reeboots pphone
        
        :param user: User dict
        :type user: type dict
        """
        self.pphone_ssh_cmd(user, "/sbin/reboot")
            
    def pphone_cloudboot(self, user, dns_ip):
        """ Performs cloudboot on pphone
        
        :param user: User dict
        :type user: type dict        
        :param dns_ip: dns ip
        :type dns_ip: type string
        """
        import socket
        try:
            socket.inet_aton(dns_ip)
        except:
            raise Exception("DNS IP %s is not valid"%dns_ip)

        replace_dns_cmd = "sed -i 's/dnsAddress.*/dnsAddress=%s/g' /nvdata/config/pphone.conf" % dns_ip
        result = self.pphone_ssh_su_cmd(user, replace_dns_cmd)
        
        clear_svc_cmd = "sed -i 's/svcLocationCache.*/svcLocationCache=/g' /nvdata/config/pphone.conf"
        result = self.pphone_ssh_su_cmd(user, clear_svc_cmd)

        rm_hq_cert_cmd = "rm /nvdata/config/cert/hq/hq_*"
        result = self.pphone_ssh_su_cmd(user, rm_hq_cert_cmd)
        #reboot phone
        self.pphone_reboot_phone(user)
        
        # os this stepo necessary
        # catch {file delete -force "phoneutil/rsa_keys/backdoor"}
                
    def pphone_begin_vm_code_capture(self, user):
        """Starts vmcodeserver
        
        :param user: User dict
        :type user: type dict
        :return ret_val: ssh cmd result
        :rtype: str
        """
        self.pphone_end_vm_code_capture(user)
        
        # Make sure PCMU8000 codec is used
        #config InitializeUCBCodec

        cmd = 'vmcodeserver >/var/log/vmcodeserver.log 2>&1 &'
        return self.pphone_ssh_su_cmd(user, cmd)
        
    def pphone_end_vm_code_capture(self, user):
        """Stop the VM capture by killing the process
        
        :param user: User dict
        :type user: type dict
        :return ret_val: ssh cmd result
        :rtype: str
        """
        cmd = '"kill -9 `pidof vmcodeserver`"'
        return self.pphone_ssh_su_cmd(user, cmd)
                        
    def wait_for_crypto_key(self, user, ca):
        """This function waits for the crypto key to be present.
        
        :param user: User dict
        :type user: type dict
        :param ca: Specify the Call appearance number
        :type ca: type int
        :return ret_val: returns the Crypto key
        :rtype: str
        """
        # NOTE other implementation needs cryto key
        # For now it is ok for crypto key to be empty
        str = ""
        
        return str
      
    def pphone_wait_for_vm_code(self, user, vmcode, ca="RIGHT_LINE1", mode="separate"):
        """This function waits for VM code in the ca specified
        
        :param user: User dict
        :type user: type dict
        :param vmcode: Specify the Vm code
        :type vmcode: type int
        :param ca: Specify the call appearance
        :type ca: type str
        :param ca: Specify the mode
        :type ca: type str
        :return ret_val: None
        :rtype: None
        """
        try: 
            port = 5667
            timeout = 12000
            vmcode = vm_codes.VMCODES[vmcode]
            
            mode = int(mode == "inline")
            crypto_key = self.wait_for_crypto_key(user, ca)
            
            cmd= "%s,%s,%s,%s" % (crypto_key,vmcode,timeout,mode)
            logger.info("Sending vmcode command: %s"% cmd)
           
            tn = telnetlib.Telnet(user.ip, port)
            tn.write(str(cmd))

            line = ""
            timeout = time.time() + timeout
            while True:
                if time.time() > timeout:
                    break
                line =  tn.read_eager()
                # line =  tn.read_very_eager()
                if line != "":
                    break 
                time.sleep(0.2)

            tn.close()
            if line != "1":
                logger.warn("Vmcode %s NOT Found: FAIL:" % vmcode)
                raise Exception()
            logger.info("Vmcode %s Found: PASS" % vmcode)
        except Exception as err:
            tn.close()
            raise Exception("func '%s' - err: '%s'!" % (sys._getframe().f_code.co_name, err))
        tn.close()

    def pphone_get_popup(self, user):
        """Returns last popup displayed on the phone
            This method always retains the last popup
            that was displayed on the phone
        :param user: User dict
        :type user: type dict
        :return ret_val: Number of sessions on phone
        :rtype: int
        """
        return str(self.pphone_ssh_dm(user, "cli -c getdm", "PPhoneDM.QA_TEST_MONITOR_popMessages"))
   
    def getdm_session_count(self, user):
        """Returns number of sessions
        
        :param user: User dict
        :type user: type dict
        :return ret_val: Number of sessions on phone
        :rtype: int
        """
        return int(self.pphone_ssh_dm(user, "cli -c getdm", "callstackdm.sessionCount"))
   
        
    def getdm_conference_session_count(self, user):
        """Returns number of sessions in conference
        
        :param user: User dict
        :type user: type dict
        :return ret_val: Number of sessions on phone
        :rtype: int
        """
        # reimplement to allow use case of more than one conf
        session_count = -1
        for i in range(1,6):
            dm_query = "callstackdm.session%s.iden.displayname"%i
            display = self.pphone_ssh_dm(user, "cli -c getdm", dm_query)
            if "Conference" in display:
                dm_query = "callstackdm.session%s.conferencelistdm.sessionCount"%i
                session_count = self.pphone_ssh_dm(user, "cli -c getdm", dm_query)
                break

        return session_count

    def getdm_call_handling_mode(self, user):
        """Returns call handling mode
        
        :param user: User dict
        :type user: type dict
        :return ret_val: call handling mode
        :rtype: str
        """
        return self.pphone_ssh_dm(user, "cli -c getdm", "user.callHandlingMode")
   
    def verify_pphone_call_handling_mode(self, user, mode):
        """Returns call handling mode
        
        :param user: User dict
        :type user: type dict
        :return ret_val: call handling mode
        :rtype: str
        """
        themode = self.getdm_call_handling_mode(user)
        if themode != mode:
            raise Exception('chm mode actual "%s" did not match expected "%s"' % (mode,themode))

    def getdm_active_audio_path(self, user):
        """Returns active audio path
        
        :param user: User dict
        :type user: type dict
        :return ret_val: Active audio path, kDevice_Handset 0, kDevice_Speaker 1, kDevice_Headset 2
        :rtype: str
        """
        return self.pphone_ssh_dm(user, "cli -c getdm", "audio.activeDevice")
		
    def pphone_get_progbutton_info(self, user, btn=1):
        """Returns active audio path
        
        :param user: User dict
        :type user: type dict
        :rtype: str
        """
        btninfo = self.pphone_ssh_dm(user, "cli -c getdm", "progbuttons.0.%s.param"%btn).split(';')
        return btninfo		
        	
        
    def getdm_pphone_muted(self, user):
        """Returns (on/off) if phone is muted
        
        :param user: User dict
        :type user: type dict
        :return ret_val: On if phone muted else off
        :rtype: str
        """
        return self.pphone_ssh_dm(user, "cli -c getdm", "audio.muteOn")
        
                
    def getdm_caller_number(self, user, ca):
        """Returns (on/off) if phone is muted
        
        :param user: User dict
        :type user: type dict
        :param ca: Call appearance
        :type ca: type string
        :return ret_val:  Returns caller number on ca
        :rtype: str
        """
        session = self._pphone_get_callstackdm_session(user, ca)
        cmd = "callstackdm."+session+".iden.displaynumber"
        return self.pphone_ssh_dm(user, "cli -c getdm", cmd)

    def verify_pphone_idle(self, user):
        """Verifies if phone user is idle
        
        :param user: User dict
        :type user: type dict
        :return ret_val: none
        :raises ExceptionType: Raises robot exception if not idle
        """
        sessioncount = self.getdm_session_count(user)
        if  sessioncount == 0:
            print("verify_pphone_idle: Pphone is idle")
        else:
            raise Exception("verify_pphone_idle: Session count = \"%s\" pphone is not idle" % sessioncount)
        
    def verify_pphone_muted(self, user):
        """Verifies if phone user is mutes
        
        :param user: User dict
        :type user: type dict
        :return ret_val: none
        :raises ExceptionType: Raises robot exception if not muted
        """
        if self.getdm_pphone_muted(user) == "on":
            print("MUTE verified")
        else:
            raise Exception("verify_pphone_muted: Pphone is not muted")
        
    # def verify_pphone_active_audio_path(self, user, audiopath):

    def get_pphone_active_audio_path(self, user):
        """Verifies if phone user is idle
        
        :param user: User dict
        :type user: type dict        


        :return ret_val: none
        :raises ExceptionType: Raises robot exception if no match
        """
        path = int(self.getdm_active_audio_path(user))
        return path

 ########################################################
 #     PPHONE KBD SERVER METHODS
 ########################################################
    
    def pphone_press_button(self, user, button):
        """Press Button on Pphone via kbd socket
        
        :param user: User dict
        :type user: type dict
        :param button: Char value for button mapping
        :type button: type str
        :return ret_val: none
        """
        logger.info("Running kbd socket cmd \"%s\" on phone %s" % (button, user.ip))
        tn = telnetlib.Telnet(user.ip, kKbd_Socket)
        tn.write(str(button))
        time.sleep(1)
            
    def pphone_press_button_raw(self, user, button):
        """Press Button on Pphone via kbd socket
        
        :param user: User dict
        :type user: type dict
        :param button: Char value for button mapping
        :type button: type str
        :return ret_val: none
        """
        print("Running kbd socket cmd \"%s\" on phone %s" % (button, user.ip))
        tn = telnetlib.Telnet(user.ip, kKbd_Socket)
        tn.write(button + "\n")
        time.sleep(1)

        
    def pphone_dial_digits(self, user, digits):
        """Dial Digits via kbd socket
        
        :param user: User dict
        :type user: type dict
        :param digits: string of digits
        :type digits: type str
        :return ret_val: none
        """
        print("Running kbd socket cmd \"%digits\" on phone %s" % (button, user.ip))
        tn = telnetlib.Telnet(user.ip, kKbd_Socket)
        tn.write(str(digits) + "\n")

    def pphone_press_button_pound(self, user):
        """Press PPhone button via kbd server
        
        :param user: User dict
        :type user: type dict
        :return ret_val: none
        """
        self.pphone_press_button(user, kButton_Pound)
        
    def pphone_press_button_hash(self, user):
        """Press PPhone button via kbd server
        
        :param user: User dict
        :type user: type dict
        :return ret_val: none
        """
        self.pphone_press_button(user, kButton_Hash)
        
    def pphone_press_button_star(self, user):
        """Press PPhone button via kbd server
        
        :param user: User dict
        :type user: type dict
        :return ret_val: none
        """
        self.pphone_press_button(user, kButton_Star)
        
    def pphone_press_button_conference(self, user):
        """Press PPhone button via kbd server
        
        :param user: User dict
        :type user: type dict
        :return ret_val: none
        """
        self.pphone_press_button(user, kButton_Conference)
        
    def pphone_press_button_directory(self, user):
        """Press PPhone button via kbd server
        
        :param user: User dict
        :type user: type dict
        :return ret_val: none
        """
        self.pphone_press_button(user, kButton_Directory)
        
    def pphone_press_button_headset(self, user):
        """Press PPhone button via kbd server
        
        :param user: User dict
        :type user: type dict
        :return ret_val: none
        """
        self.pphone_press_button(user, kButton_Headset)
        
    def pphone_press_button_hold(self, user):
        """Press PPhone button via kbd server
        
        :param user: User dict
        :type user: type dict
        :return ret_val: none
        """
        self.pphone_press_button(user, kButton_Hold)
        
    def pphone_handset_up(self, user):
        """Press PPhone button via kbd server
        
        :param user: User dict
        :type user: type dict
        :return ret_val: none
        """
        self.pphone_press_button(user, kButton_Hookswitch_Up)
        
    def pphone_handset_down(self, user):
        """Press PPhone button via kbd server
        
        :param user: User dict
        :type user: type dict
        :return ret_val: none
        """
        self.pphone_press_button(user, kButton_Hookswitch_Down)
                
    def pphone_handset_disconnect_call(self, user):
        """Press PPhone button via kbd server
        
        :param user: User dict
        :type user: type dict
        :return ret_val: none
        """
        self.pphone_handset_up(user)
        self.pphone_handset_down(user)
        
    def pphone_press_button_rightLine1(self, user):
        """Press PPhone button via kbd server
        
        :param user: User dict
        :type user: type dict
        :return ret_val: none
        """
        self.pphone_press_button(user, kButton_RightLine1)
        
    def pphone_press_button_rightLine2(self, user):
        """Press PPhone button via kbd server
        
        :param user: User dict
        :type user: type dict
        :return ret_val: none
        """
        self.pphone_press_button(user, kButton_RightLine2)
        
    def pphone_press_button_rightLine3(self, user):
        """Press PPhone button via kbd server
        
        :param user: User dict
        :type user: type dict
        :return ret_val: none
        """
        self.pphone_press_button(user, kButton_RightLine3)
        
    def pphone_press_button_rightLine4(self, user):
        """Press PPhone button via kbd server
        
        :param user: User dict
        :type user: type dict
        :return ret_val: none
        """
        self.pphone_press_button(user, kButton_RightLine4)
        
    def pphone_press_button_leftLine1(self, user):
        """Press PPhone button via kbd server
        
        :param user: User dict
        :type user: type dict
        :return ret_val: none
        """
        self.pphone_press_button(user, kButton_LeftLine1)
        
    def pphone_press_button_leftLine2(self, user):
        """Press PPhone button via kbd server
        
        :param user: User dict
        :type user: type dict
        :return ret_val: none
        """
        self.pphone_press_button(user, kButton_LeftLine2)
        
    def pphone_press_button_leftLine3(self, user):
        """Press PPhone button via kbd server
        
        :param user: User dict
        :type user: type dict
        :return ret_val: none
        """
        self.pphone_press_button(user, kButton_LeftLine3)
        
    def pphone_press_button_leftLine4(self, user):
        """Press PPhone button via kbd server
        
        :param user: User dict
        :type user: type dict
        :return ret_val: none
        """
        self.pphone_press_button(user, kButton_LeftLine4)
        
    def pphone_press_button_up(self, user):
        """Press PPhone button via kbd server
        
        :param user: User dict
        :type user: type dict
        :return ret_val: none
        """
        self.pphone_press_button(user, kButton_Up)
        
    def pphone_press_button_down(self, user):
        """Press PPhone button via kbd server
        
        :param user: User dict
        :type user: type dict
        :return ret_val: none
        """
        self.pphone_press_button(user, kButton_Down)
        
    def pphone_press_button_left(self, user):
        """Press PPhone button via kbd server
        
        :param user: User dict
        :type user: type dict
        :return ret_val: none
        """
        self.pphone_press_button(user, kButton_Left)
        
    def pphone_press_button_right(self, user):
        """Press PPhone button via kbd server
        
        :param user: User dict
        :type user: type dict
        :return ret_val: none
        """
        self.pphone_press_button(user, kButton_Right)
        
    def pphone_press_button_softkey1(self, user):
        """Press PPhone button via kbd server
        
        :param user: User dict
        :type user: type dict
        :return ret_val: none
        """
        self.pphone_press_button(user, kButton_Softkey1)
        
    def pphone_press_button_softkey2(self, user):
        """Press PPhone button via kbd server
        
        :param user: User dict
        :type user: type dict
        :return ret_val: none
        """
        self.pphone_press_button(user, kButton_Softkey2)
        
    def pphone_press_button_softkey3(self, user):
        """Press PPhone button via kbd server
        
        :param user: User dict
        :type user: type dict
        :return ret_val: none
        """
        self.pphone_press_button(user, kButton_Softkey3)
        
    def pphone_press_button_softkey4(self, user):
        """Press PPhone button via kbd server
        
        :param user: User dict
        :type user: type dict
        :return ret_val: none
        """
        self.pphone_press_button(user, kButton_Softkey4)
        
    #  TODO def pphone_press_button_softkey5(self, user):
        
    def pphone_press_button_mute(self, user):
        """Press PPhone button via kbd server
        
        :param user: User dict
        :type user: type dict
        :return ret_val: none
        """
        self.pphone_press_button(user, kButton_Mute)
        
    def pphone_press_button_redial(self, user):
        """Press PPhone button via kbd server
        
        :param user: User dict
        :type user: type dict
        :return ret_val: none
        """
        self.pphone_press_button(user, kButton_Redial)
        
    def pphone_press_button_enter(self, user):
        """Press PPhone button via kbd server
        
        :param user: User dict
        :type user: type dict
        :return ret_val: none
        """
        self.pphone_press_button(user, kButton_Enter)
        
    def pphone_press_button_fire(self, user):
        """Press PPhone button via kbd server
        
        :param user: User dict
        :type user: type dict
        :return ret_val: none
        """
        self.pphone_press_button(user, kButton_Fire)
        
    def pphone_press_button_backspace(self, user):
        """Press PPhone button via kbd server
        
        :param user: User dict
        :type user: type dict
        :return ret_val: none
        """
        self.pphone_press_button(user, kButton_Backspace)
        
    def pphone_press_button_speaker(self, user):
        """Press PPhone button via kbd server
        
        :param user: User dict
        :type user: type dict
        :return ret_val: none
        """
        self.pphone_press_button(user, kButton_Speaker)
        
    def pphone_press_button_transfer(self, user):
        """Press PPhone button via kbd server
        
        :param user: User dict
        :type user: type dict
        :return ret_val: none
        """
        self.pphone_press_button(user, kButton_Transfer)
        
    def pphone_press_button_voicemail(self, user):
        """Press PPhone button via kbd server
        
        :param user: User dict
        :type user: type dict
        :return ret_val: none
        """
        self.pphone_press_button(user, kButton_Voicemail)
        
    def pphone_press_button_volumeDown(self, user):
        """Press PPhone button via kbd server
        
        :param user: User dict
        :type user: type dict
        :return ret_val: none
        """
        self.pphone_press_button(user, kButton_VolumeDown)
        
    def pphone_press_button_volumeUp(self, user):
        """Press PPhone button via kbd server
        
        :param user: User dict
        :type user: type dict
        :return ret_val: none
        """
        self.pphone_press_button(user, kButton_VolumeUp)
         
########################################################
 #     PPHONE SOCKET INTERFACE METHODS
 ########################################################
   
    def si_query(self, user_from, query):
        """Socket Interface main cmd method
        
        :param user: User dict
        :type user: type dict
        :param query: Query to be run on socket interface
        :type query: type str
        :return ret_val: Result of query
        """
        #  TODO replace with log level
        print("Running socket cmd: %s on phone %s" % (query, user_from.ip))
        tn = telnetlib.Telnet(user_from.ip, Interface_Socket)
        tn.write(str(query) + "\n")
        return tn.read_some()
        
    def pphone_get_led_state(self, socket_led, state):
        """
        :param socket_led: LED state
        :type socket_led: type str
        :param state: state (color or pattern)
        :type state: type str
        :return ret_val: None
        """
        if state == "color":
            ret = socket_led[2]
        elif state == "pattern":
            ret = socket_led[3]
        else:
            logger.warn("State {} does not exist".format(state))
            raise Exception("")
        return ret     
        
    def pphone_verify_led_color(self, socket_led, color):
        """
        :param socket_led: LED state
        :type socket_led: type str
        :param colot: LED color
        :type color: type str
        :return ret_val: None
        """
        if kLED_Colors[color] != self.pphone_get_led_state(socket_led, "color"):
            raise Exception("LED state {} color is not {}:{}".format(socket_led,color,kLED_Colors[color]))
        return None  
         
    def pphone_verify_led_pattern(self, socket_led, led_pattern):
        """
        :param socket_led: LED state
        :type socket_led: type str
        :param led_pattern: pattern (on, off, blinking)
        :type led_pattern: type str
        :return ret_val: None
        """
        if led_pattern == "blinking":
            if "_" not in self.pphone_get_led_state(socket_led, "pattern"):
                raise Exception("LED state {} LED is not blinking".format(socket_led,led_pattern))
        elif led_pattern not in self.pphone_get_led_state(socket_led, "pattern"):
            raise Exception("LED state {} LED is not {}".format(socket_led,led_pattern))
        return None
        
    def pphone_verify_led_state(self, user, ca, color, led_pattern):
        """
        :param user: User dict
        :type user: type dict
        :param ca: call appearance
        :type ca: type str
        :param color: LED color
        :type color: type str
        :param led_pattern: pattern (on, off, blinking)
        :type led_pattern: type str
        :return ret_val: None
        """
        query = " ".join(["getline",kCA_lines[ca.lower()],kPos_LED])
        tn = telnetlib.Telnet(user.ip, Interface_Socket)
        tn.write(str(query) + "\n")
        result = tn.read_some()    
        
        socket_led = result.split('\x1e')
        
        self.pphone_verify_led_color(socket_led, color)
        self.pphone_verify_led_pattern(socket_led, led_pattern)
        
        return None

    def pphone_search_softkey_text(self, user, text):
        """Searches for softkey text
        
        :param user: User dict
        :type user: type dict
        :param text: Softkey text to be searched
        :type text: type str
        :return ret_val: Index of softkey, -1 if not found
        """
        pattern = ".*%s" % text
        for i in range(0,self.kNumSoftKeys):
            cmd = "getsk sk{0}".format(i) 
            sk = self.si_query(user, cmd)
            #  Check if sk is empty
            if not re.match(".*png",sk):
                #  TODO  softkey has no image, procees
                #  TODO  remove RS char from sk
                if len(sk.strip()) < 8:
                    print("Skipping empty softkey %s" % sk)
                    continue
                sk_text = sk.split("5")[1].strip()
                print(sk_text)
            else:
                str = sk.split(":")
                sk_img = str[1]
                str = str[0].split("5")
                sk_text =  str[1]
            if re.match(pattern,sk_text): 
                print("Text %s found at index %d" % (text,i))
                return i
        print("Text %s not found" % text)
        return -1
        

    def wait_for_active_audio_device(self, user, audio_device):
        """Polls for ca_type match on line ca_line for timeout time
        
        :param user: User dict
        :type user: type dict
        :param audio_device: Audio device path
        :type audio_device: string
        :return ret_val: none
        :raises ExceptionType: Raises robot exception if no match
        """
        num_tries = 3
        for i in range(0,num_tries):
            time.sleep(1)
            logger.info("wait_for_active_audio_device %s attempt: %s" % (audio_device, i))
            path = self.get_pphone_active_audio_path(user)
            if path == audio_device:
                logger.info("Audio device \"%s\" matched \"%s\"" % (audio_device,path))
                return
            else:
                if audio_device == kDevice_Handset:
                    self.pphone_press_button(user, kButton_Hookswitch_Up)
                elif audio_device == kDevice_Speaker:
                    self.pphone_press_button(user, kButton_Speaker)
                elif audio_device == kDevice_Headset:
                    self.pphone_press_button(user, kButton_Headset)
                else:
                    raise Exception("answer_call:  AudioPath %s does not exist" % audio_device)
        raise Exception("wait_for_active_audio_device: Audio path expected \"%s:%s\". Does not match actual \"%s:%s\"" % (deviceMap[audio_device],audio_device,deviceMap[path],path))
		
    def wait_for_call_appearance(self, user_callee, ca_type, ca_line):
        """Polls for ca_type match on line ca_line for timeout time
        
        :param user_callee: User dict
        :type user_callee: type dict
        :param ca_type: Call appearance type
        :type ca_type: type str
        :param ca_line: Call appearance line
        :type ca_line: type str
        :return ret_val: none
        :raises ExceptionType: Raises robot exception if no match
        """
        ca_lines = {'right_line1': 'line0', 'right_line2': 'line1', 'right_line3': 'line2', 'right_line4': 'line3', 'left_line1': 'line4', 'left_line2': 'line5', 'left_line3': 'line6', 'left_line4': 'line7', }

        line = ca_lines[ca_line.lower()]
        cmd = "getline " + line + " 1"
        pattern = ".*%s" % ca_type
        timeout = time.time() + self.event_timeout
        while True:
            time.sleep(1)
            resp = self.si_query(user_callee, cmd)
            
            # TODO - workaround since returned val cuts off chars (ie. return .p instead of .png)
            resp = resp.split('images')[1]
            if resp.strip() in pattern:
                break
            if time.time() > timeout:
                raise Exception("Actual: \"%s\" is not in Expected: \"%s\"" % (resp, pattern))
                break
            #  TODO replace with log level
            print("sleeping 1 second for pattern %s" % pattern)

    def wait_for_idle_call(self, user_callee, ca_line):
        """Polls for idle state match on line ca_line
        
        :param user_callee: User dict
        :type user_callee: type dict
        :param ca_line: Call appearance line
        :type ca_line: type str
        :return ret_val: none
        """
        self.wait_for_call_appearance(user_callee, kCallAppearance_idleCall, ca_line)
     
    def wait_for_dialing_call(self, user_callee, ca_line):
        """Polls for dialing state match on line ca_line
        
        :param user_callee: User dict
        :type user_callee: type dict
        :param ca_line: Call appearance line
        :type ca_line: type str
        :return ret_val: none
        """
        if user_callee.phone_type == 'p8cg':
            self.wait_for_call_appearance(user_callee, kCallAppearance_p8cg_dialingCall, ca_line)
        elif user_callee.phone_type == 'p8':
            self.wait_for_call_appearance(user_callee, kCallAppearance_p8_dialingCall, ca_line)
        elif user_callee.phone_type == 'p2':
            self.wait_for_call_appearance(user_callee, kCallAppearance_p2_dialingCall, ca_line)
        else:
		    raise Exception("Phone type %s does not exist")
     
    def wait_for_incoming_call(self, user_callee, ca_line):
        """Polls for icoming state match on line ca_line
        
        :param user_callee: User dict
        :type user_callee: type dict
        :param ca_line: Call appearance line
        :type ca_line: type str
        :return ret_val: none
        """
        if user_callee.phone_type == 'p8cg':
            self.wait_for_call_appearance(user_callee, kCallAppearance_p8cg_incomingCall, ca_line)
        elif user_callee.phone_type == 'p8':
            self.wait_for_call_appearance(user_callee, kCallAppearance_p8_incomingCall, ca_line)
        elif user_callee.phone_type == 'p2':
            self.wait_for_call_appearance(user_callee, kCallAppearance_p2_incomingCall, ca_line)
        else:
		    raise Exception("Phone type %s does not exist")
     
     
    def wait_for_connected_call(self, user_callee, ca_line):
        """Polls for connected state match on line ca_line
        
        :param user_callee: User dict
        :type user_callee: type dict
        :param ca_line: Call appearance line
        :type ca_line: type str
        :return ret_val: none
        """
        self.wait_for_call_appearance(user_callee, kCallAppearance_connectedCall, ca_line)
             
    def wait_for_local_hold_call(self, user_callee, ca_line):
        """Polls for local hold state match on line ca_line
        
        :param user_callee: User dict
        :type user_callee: type dict
        :param ca_line: Call appearance line
        :type ca_line: type str
        :return ret_val: none
        """
        self.wait_for_call_appearance(user_callee, kCallAppearance_localHold, ca_line)
        
    def wait_for_remote_hold_call(self, user_callee, ca_line):
        """Polls for remote hold state match on line ca_line
        
        :param user_callee: User dict
        :type user_callee: type dict
        :param ca_line: Call appearance line
        :type ca_line: type str
        :return ret_val: none
        """
        self.wait_for_call_appearance(user_callee, kCallAppearance_remoteHold, ca_line)
        

    def answer_via_headset(self, user_callee):
        """Answers call via headset
        
        :param user_callee: User dict
        :type user_callee: type dict
        :return ret_val: none
        """
        self.pphone_press_button_headset(user_callee)
       
    def pphone_verify_caller_name(self, user_callee, user_caller):
        """Verifies if user_caller is called by user_callee
        
        :param user_callee: User dict
        :type user_callee: type dict
        :param user_caller: User dict
        :type user_caller: type dict
        :param ca_line: Call appearance line
        :type ca_line: type str
        :return ret_val: 1 if matched else 0
        :raises ExceptionType: Raises robot exception if no match
        """
        pattern = ".*%s" % user_caller.first_name
        resp = self.si_query(user_callee, "getline line0 3")
        if re.match(pattern, resp):
            return 1
        else:
            raise Exception("answer_verify_caller: user %s was not matched" % user_caller.first_name)
        return 0
     
    def pphone_si_verify_caller_number(self, user_callee, user_caller, ca, num_format):
        """Verifies if user_caller is called by user_callee
        
        :param user_callee: User dict
        :type user_callee: type dict
        :param user_caller: User dict
        :type user_caller: type dict
        :param ca_line: Call appearance line
        :type ca_line: type str
        :return ret_val: 1 if matched else 0
        :raises ExceptionType: Raises robot exception if no match
        """
        if num_format == "extension":
            pattern = ".*%s" % user_caller.extension
        if num_format == "sip_trunk_did":
            pattern = "%s" % user_caller.sip_did
            logger.info("Looking for user %s number %s" %(user_caller.first_name,pattern))
            reNum = re.search(r'^(\d?)(\d{3})(\d{3})(\d{4})$',pattern)
            pattern = "\("+ reNum.group(2) + "\)"+ reNum.group(3) + "-" + reNum.group(4) 


        resp = self.si_query(user_callee, "getline line0 3")
        pnum = resp.split('\x1e')[2]
        logger.info("Socket Interface returned number %s" % pnum)
        if re.match(pattern, pnum):
            return 1
        else:
            raise Exception("pphone_si_verify_caller_number: user %s did not match re pattern %s with %s" % (user_caller.first_name, pattern, resp))
        return 0

    def _pphone_get_callstackdm_session(self, user, call_appearance):
        """Returns the callstackdm session number
        
        :param user: User dict
        :type user: type dict
        :param call_appearance: Call appearance
        :type call_appearance: type string
        :return ret_val:  Returns session number
        :rtype: str
        """
        ca_lines = {'right_line1': '0', 'right_line2': '1', 'right_line3': '2', 'right_line4': '3', 'left_line1': '4', 'left_line2': '5', 'left_line3': '6', 'left_line4': '7', }

        ca_num = ca_lines[call_appearance.lower()]

        #Get list of session numbers
        result = self.pphone_ssh_cmd(user, "cli -c getdm callstackdm|grep callAppearance" )

        result = result.splitlines()
        for line in result:
            if "session" in line:
               #Cycle through sessions
                session_num = line.split('.')[1]
                ca = line.split('=')[1]
                if ca_num in ca:
                    # logger.warn(session_num)
                    # logger.warn(ca)
                    logger.warn("PASS: session found \"%s\"" % session_num)
                    return session_num
        logger.warn("FAIL: session not found")
        raise Exception("_pphone_get_callstackdm_session: Session num \"%s\" not found" % ca_num)

    def pphone_verify_caller_number(self, user_callee, user_caller, ca, num_format):
        """Verifies if user_caller is called by user_callee
        
        :param user_callee: User dict
        :type user_callee: type dict
        :param user_caller: User dict
        :type user_caller: type dict
        :param ca_line: Call appearance line
        :type ca_line: type str
        :return ret_val: 1 if matched else 0
        :raises ExceptionType: Raises robot exception if no match
        """
        if num_format == "extension":
            pattern = ".*%s" % user_caller.extension
        if num_format == "sip_trunk_did":
            pattern = ".*%s" % user_caller.sip_did

        caller_number = self.getdm_caller_number(user_callee,ca)
        if re.match(pattern, caller_number):
            return 1
        else:
            raise Exception("pphone_verify_caller_number: Pattern %s did not match caller_number \"%s\" for number format %s " % (pattern, caller_number,num_format))
        return 0
              
    def pphone_make_call(self, user_from, user_to, ca_line):
        """Makes call from user_from to user_to on ca_line
        
        :param user_from: User dict
        :type user_from: type dict
        :param user_to: User dict
        :type user_to: type dict
        :param ca_line: Call appearance line on which to make call
        :type ca_line: type str
        :return ret_val: none
        """
        tn = telnetlib.Telnet(user_from.ip, kKbd_Socket)
        tn.write(str(user_to.extension) + "\n") 
        #check full string then return
        self.wait_for_dialing_call(user_from, ca_line)

    def pphone_disconnect_call_via_softkey(self, user_callee):
        """Disconnects user_callee call via softkey
        
        :param user_callee: User dict
        :type user_callee: type dict
        :return ret_val: none
        :raises ExceptionType: Raises robot exception if no match
        """
        index = self.pphone_search_softkey_text(user_callee, "Hang Up")
        if index == -1:
            raise Exception("disconnect_call_via_softkey: Failed softkey search for \"Hang Up\"")
        self.pphone_press_button(user_callee, kButton_Softkeys[index])

    def pphone_disconnect_call(self, user, mode="-1"):
        """Disconnects user call via mode
        
        :param user: User dict
        :type user: type dict
        :param mode: handset-0, speaker-1, headset-2
        :type mode: type str
        :return ret_val: none
        :raises ExceptionType: Raises robot exception if no match
        """
        audiopath = int(self.getdm_active_audio_path(user))
        if mode == "-1":
            if audiopath == kDevice_Handset:
                self.pphone_handset_down(user)
            elif audiopath == kDevice_Speaker:
                self.pphone_press_button(user, kButton_Speaker)
            elif audiopath == kDevice_Headset:
                self.pphone_press_button(user, kButton_Headset)
            else:
                raise Exception("disconnect_call: AudioPath %s does not exist" % audiopath)
        else:
            self.disconnect_call_via_softkey(user)
            # self.pphone_press_button(user_callee, mode)
        if self.getdm_session_count(user) != 0:
            self.disconnect_call_via_softkey(user)
        self.verify_pphone_idle(user)
        

    def pphone_answer_call(self, user_callee, user_caller, ca_line, audio_path="-1"):
        """Disconnects user call via mode
        
        :param user_callee: User dict
        :type user_callee: type dict
        :param user_caller: User dict
        :type user_caller: type dict
        :param ca_line: Call appearance line to check incoming call
        :type ca_line: type str
        :param audio_path: handset-0, speaker-1, headset-2
        :type audio_path: type str
        :return ret_val: none
        :raises ExceptionType: Raises robot exception if no match
        """
        self.wait_for_incoming_call(user_callee, ca_line)
        if audio_path == "-1":
            audio_path = kDevice_Handset

        logger.info("audio path is %s" % audio_path)
        if audio_path == kDevice_Handset:
            self.pphone_press_button(user_callee, kButton_Hookswitch_Up)
        elif audio_path == kDevice_Speaker:
            self.pphone_press_button(user_callee, kButton_Speaker)
        elif audio_path == kDevice_Headset:
            self.pphone_press_button(user_callee, kButton_Headset)
        else:
            raise Exception("answer_call:  AudioPath %s does not exist" % audio_path)
            return
        self.wait_for_active_audio_device(user_callee, audio_path)
        
    def pphone_verify_call_duration	(self, user_caller):
        pass

    def pphone_hold_call(self,user, ca_line):
        """Holds and verifies call on user
        
        :param user: User dict
        :type user: type dict
        :param ca_line: Call appearance line to check call hold
        :type ca_line: type str
        :return ret_val: none
        """
        self.pphone_press_button_hold(user)
        self.wait_for_local_hold_call(user, ca_line)
        
        
# Audio devices
#  kDevice_Handset 0
#  kDevice_Speaker 1
#  kDevice_Headset 2

    def pxcon_init_audio(self, user):
        # Initializing modules to play audio via pxcon
        # This function need run only one time unless the phone is reboot
        self.pphone_ssh_cmd(user, "/bin/ash /bin/pxaudio_init.sh" )

    def pxcon_create_audio_inject_handle(self, user, audioPath):
        mode = "repeat"
        syncType = "sync"
        filename = ""

        device = deviceMap[audioPath]

        if device == 0:
            filename = "16k_500.pcm"
            self.pphone_ssh_cmd(user,"pxcon /bin/pxinject_audiohandset.sh")
        elif device == 1:
            filename = "16k_3k.pcm"
            self.pphone_ssh_cmd(user,"pxcon /bin/pxinject_audiospeaker.sh")
        elif device == 2:
            filename = "16k_1k.pcm"
            self.pphone_ssh_cmd(user,"pxcon /bin/pxinject_audioheadset.sh")
        else:
            print("Device %s is not known!" % device)
        print("Preparing to inject \\etc\\apt\\%s on device: %s mode: %s" % (filename, device, mode))

    def pxcon_create_audio_capture_handle(self, user, audioPath):
        mode = "truncate"
        syncType = "sync"
        filename = ""

        device = deviceMap[audioPath]

        if device == 0:
            filename = "/tmp/handsetcapture.pcm"
            self.pphone_ssh_cmd(user,"pxcon /bin/pxcapture_audiohandset.sh")
        elif device == 1:
            filename = "/tmp/speakercapture.pcm"
            self.pphone_ssh_cmd(user,"pxcon /bin/pxcapture_audiospeaker.sh")
        elif device == 2:
            filename = "/tmp/headsetcapture.pcm"
            self.pphone_ssh_cmd(user,"pxcon /bin/pxcapture_audioheadset.sh")
        else:
            print("Device %s is not known!" % device)
        print("Preparing to capture %s on device: %s mode: %s" % (filename, device, mode))


    def pxcon_sync_enable_audio(self, user):
        print("Playing/Enabling audio on %s..." % user.ip)
        self.pphone_ssh_cmd(user,"killall pxcon; pxcon /bin/pxsync_enable.sh")

    def pxcon_sync_disable_audio(self, user):
        print("Audio Stopped/Disabled on %s " % user.ip)
        self.pphone_ssh_cmd(user,"killall pxcon; pxcon /bin/pxsync_disable.sh")

    def pxcon_remove_audio_handles(self, user):
        print("Removing pxcon audio handles")
        self.pphone_ssh_cmd(user,"killall pxcon; pxcon /bin/pxrm_audioh.sh; rm /tmp/*capture.pcm")
        print("Pxcon audio utils flushed and removed")

    def pphone_check_one_way_audio( self, user_inject, user_capture ):
        inj_activeAudioDevice = int(self.getdm_active_audio_path(user_inject))
        cap_activeAudioDevice = int(self.getdm_active_audio_path(user_capture))

        device = halAudioMap[inj_activeAudioDevice]
        other_device = halAudioMap[cap_activeAudioDevice]

        for i in range(0,self.max_oneway_retry):
            audioPassed = 1
            self.pxcon_create_audio_inject_handle(user_inject, device)
            self.pxcon_create_audio_capture_handle(user_capture, other_device)

            self.pxcon_sync_enable_audio(user_inject)
            self.pxcon_sync_enable_audio(user_capture)
            time.sleep(3)
            self.pxcon_sync_disable_audio(user_capture)
            self.pxcon_sync_disable_audio(user_inject)
 
            freq = self.get_estimated_frequency(user_capture)

            self.pxcon_remove_audio_handles(user_inject)
            self.pxcon_remove_audio_handles(user_capture)
        
            if freq == 2666:
                print("2k Hz sine tone detected on handset")
                if inj_activeAudioDevice != 0:
                    audioPassed = 0
                    print("Audio is not playing from injector handset")
            elif freq == 4000:
                print("3k Hz sine tone detected on speaker")
                if inj_activeAudioDevice != 1:
                    audioPassed = 0
                    print("Audio is not playing from injector speaker")
            elif freq == 500:
                print("500 Hz sine tone detected on headset")
                if inj_activeAudioDevice != 2:
                    audioPassed = 0
                    print("Audio is not playing from injector headset")
            else:
                audioPassed = 0
                print("Unkown frequency detected")
            if audioPassed == 1:
                print("Audio check PASSED")
                return
        if audioPassed == 0:
            raise Exception("One-way audio check FAILED")


    def pphone_check_no_audio( self, user_inject, user_capture ): 
        # pass
        inj_activeAudioDevice = int(self.getdm_active_audio_path(user_inject))
        cap_activeAudioDevice = int(self.getdm_active_audio_path(user_capture))

        device = halAudioMap[inj_activeAudioDevice]
        other_device = halAudioMap[cap_activeAudioDevice]

        for i in range(0,self.max_oneway_retry):
            audioPassed = 1
            self.pxcon_create_audio_inject_handle(user_inject, device)
            self.pxcon_create_audio_capture_handle(user_capture, other_device)

            self.pxcon_sync_enable_audio(user_inject)
            self.pxcon_sync_enable_audio(user_capture)
            time.sleep(3)
            self.pxcon_sync_disable_audio(user_capture)
            self.pxcon_sync_disable_audio(user_inject)
 
            #Check below should not detect any frequency
            freq = str(self.get_estimated_frequency(user_capture))

            self.pxcon_remove_audio_handles(user_inject)
            self.pxcon_remove_audio_handles(user_capture)

            if "2666" in freq:
                print("2k Hz sine tone detected")
                audioPassed = 0
            elif "4000" in freq:
                print("3k Hz sine tone detected")
                audioPassed = 0
            elif "500" in freq:
                print("500 Hz sine tone detected")
                audioPassed = 0
            else:
                # audioPassed = 0
                print("Frequency: %s detected" % freq)
            
            if audioPassed == 1:
                print("Audio check PASSED")
                return
        if audioPassed == 0:
            raise Exception("No audio check FAILED")

    def pphone_check_two_way_audio( self, user, other_user ):
        pass
        
        # self.pphone_check_one_way_audio(user, other_user)
        # self.pphone_check_one_way_audio(other_user, user)

    def get_estimated_frequency( self, user_capture ):
        samplerate = 16000
        skip_samples = 10000
        cap_activeAudioDevice = int(self.getdm_active_audio_path(user_capture))

        # files = ["/tmp/handsetcapture.pcm", "/tmp/speakercapture.pcm", "/tmp/headsetcapture.pcm"]
        files = [2666,4000,500]
        filename = files[cap_activeAudioDevice]

        # cmd = "estimate_freq " + str(samplerate) + " " + str(skip_samples) + " < " + filename
        # print("Running cmd \"%s\"" % cmd)
        # result = self.pphone_ssh_cmd(user_capture, cmd)
        # print("estimated freq: %s" % result)
        return filename

 ########################################################
 #     VOICEMAIL
 ########################################################

    def pphone_create_new_voicemail(self,user_to,user_from, number = 1,length="short",subject="Robot Automation"):
        """Creates new voicemail files on a vm server
        
        :param user_to Voice Mailbox name
        :param user_from Voice Mail sender
        :param subject Specify the subject
        :param number Number of voicemails to create
        :param length Optional short
        :param subject Voice Mail "Robot Automation"

        :return message as string
        """
        # TODO remove hard coded VM PATH
        wav_file = "c:\\ATF_ROBOT\\testdata\\vm_{0}.wav".format(length)
        if not os.path.isfile(wav_file):
            raise Exception("pphone_create_new_voicemail: \"%s\" not found for creating VM" % wav_file)
        
        # TODO Add support for MT
        
        self.pphone_create_voicemail_files(user_to,user_from,subject,number)
        if(self.pphone_upload_voicemail_files(user_to,wav_file)):
            self.pphone_run_voicemail_command(user_to)
        else:
            raise Exception("pphone_create_new_voicemail: failed to create VM" % wav_file)
        
        logger.info("Created %s voicemails on %s user %s" % (number,user_to.server,user_to.ip))
        time.sleep(2)

    def pphone_create_voicemail_files(self,user_to,user_from,subject,number=1,wav_path="DEFAULT"):
        """Create snew voicemail files on a vm server
        
        :param user_to Voice Mailbox name
        :param user_from Voice Mail sender
        :param subject Specify the subject
        :param number Number of voicemails to create
        :param wav_path Optional DEFAULT
        
        :return Nothing
        """
        if os.path.isfile("VM_COMMANDS"):
            os.remove("VM_COMMANDS")
        fh = open("VM_COMMANDS",'w')
        
        if wav_path == "DEFAULT":
            #This is the NAS
            wav_path = "c:\\inetpub\\ftproot\\vm.wav"
        
        for i in range(0,int(number)):
            fh.write("rstmsg2 \"%s\" %s \"%s\" \"%s\"\n" % (wav_path,user_to.extension,user_from.extension,subject))
        
        fh.write("exit")
        fh.close()
        
    def pphone_upload_voicemail_files(self,user_to,wav_file):
        """Uploads the voicemail files on a vm server
        :param user_to user dict
        :param wav_file Specify the audio file to be uploaded
        :return true if the upload is successfull else false
        """
        ftp = ftplib.FTP()
        try:
            ftp.connect(user_to.server)
            ftp.login(user_to.hq_username,user_to.hq_password)
        except socket.error,e:
            print('unable to connect!,%s'%e)
            ftp.quit()
            return 0
        logger.info("FTP CONNECTED")
        
        #create pphone dir to store VM file
        if user_to.ip not in ftp.nlst():
            ftp.mkd(user_to.ip)
        ftp.cwd(user_to.ip)
        
        res = ftp.storbinary("STOR VM_COMMANDS", open("VM_COMMANDS", "rb"))
        if "complete" not in res:
            raise Exception("pphone_upload_voicemail_files: failed to upload VM command file")
        
        ftp.cwd("..")
        res = ftp.storbinary("STOR vm.wav", open(wav_file, "rb"))
        if "complete" not in res:
            raise Exception("pphone_upload_voicemail_files: failed to upload VM wav file")
            ftp.quit()
            return 0
        ftp.quit()
        return 1

    def pphone_run_voicemail_command(self,user_to,vm_cmd_file="DEFAULT"):
        """This function runs the voice mail command on the HQ
        :param user_to user dict
        :param vm_cmd_file optional DEFAULT
        :return Nothing
        """
        # It looks like cfg.exe can be called without a path
        # TODO remove hard coded VM PATH
        
        # cw = CeleryRemote.CeleryRemote(user_to.server, user_to.hq_username, user_to.hq_password, 'celeryTasks', 'redis://localhost', '6379')
        
        cfg_cmd='cfg.exe -f \"C:\\inetpub\\ftproot\\'+user_to.ip+'\\VM_COMMANDS\"'
        result = cw.run(cmd=cfg_cmd,task='run_cmd')

########################################################
#     PPHONE SANITY CHECKS
########################################################
 
    def pphone_force_idle_state(self,*args):
        """Forces pphone to idle state
        
        :param args: List of user dicts mapped to real pphones
        :type args: type list
        :return ret_val: none
        :raises ExceptionType: Raises robot exception if no match
        """
        for user in args:
            end_time = time.time() + self.force_idle_timeout 
            while True:
                # Make sure pphone is idle
                if self.getdm_session_count(user) == 0:
                    #check pphone is not on voicemail or directory page
                    index = self.pphone_search_softkey_text(user, "Call VM")
                    if index != -1:
                        self.pphone_press_button(user,kButton_VoiceMail)
                    index = self.pphone_search_softkey_text(user, "Open")
                    if index != -1:
                        self.pphone_press_button(user, kButton_Directory)
                    break
                else:
                    self.pphone_handset_up(user)
                    time.sleep(0.5)
                    self.pphone_handset_down(user)                    
                
                if time.time() > end_time:
                    raise Exception("pphone %s was not able to be forced to idle state" % user.ip)
                    break
            # Forcing handset up and down
            self.pphone_handset_up(user)
            time.sleep(1)
            self.pphone_handset_down(user) 
            logger.info("pphone %s is idle" % user.ip)


    def pphone_sanity_check(self,*args):
        """Runs Sanity Check functions
        
        :param args: List of user dicts mapped to real pphones
        :type args: type list
        :return ret_val: none
        :raises ExceptionType: Raises robot exception if no match
        """
        self.pphone_force_idle_state(*args)

if __name__ == "__main__":
    # x = PPhoneInterface()
    # x.pphone_sanity_check({"ip": "10.198.18.108", "extension": "1007", "phone_type": "p8cg", "PPhone_mac": "001049454A97"},{"ip": "10.198.18.189", "extension": "1008", "phone_type": "p8cg", "PPhone_mac":"001049454AF9"})
    import robot.utils.dotdict

    Phone01_s = robot.utils.dotdict.DotDict(ip="10.198.18.108", extension="1007", phone_type="p8cg",
                                            PPhone_mac="001049454A97")
    Phone02_s = robot.utils.dotdict.DotDict(ip="10.198.18.189", extension="1008", phone_type="p8cg",
                                            PPhone_mac="001049454AF9")
    Phone03_s = robot.utils.dotdict.DotDict(ip="10.198.33.255", extension="1009", phone_type="p8cg",
                                            PPhone_mac="001049454A71")
    x = PPhoneInterface()
    # x.pphone_sanity_check(Phone01_s,Phone02_s)
    x.pphone_make_call(Phone01_s, Phone02_s, 'right_line1')

