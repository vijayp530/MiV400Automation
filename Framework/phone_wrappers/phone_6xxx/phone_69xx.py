"""
Module to interact with Mitel phones. 
"""
__author__ = "milton.villeda@mitel.com"

import sys
from robot.api import logger
import time
from .mitel_phone_base import Phone6xxxInterface
from . import phone_button_map
import telnetlib
import paramiko
from scp import SCPClient
import os
import socket
from .phone_constants_69xx import led_mode, led_type, line_state, line_key_start_index
class Phone_69xx(Phone6xxxInterface):
    """ 69xx Phone Interface
    """
    def __init__(self, phone_info, **kwargs):
        """
        It is mandatory to call phone_sanity_check immediately to create the phone objects for mitel phones
        :param args:
        """
        logger.info("Initializing Mitel 69xx Phone class")
        self.phone_type = phone_info['phoneModel']
        phone_info['led_mode'] = led_mode
        phone_info['led_type'] = led_type
        phone_info['line_state'] = line_state
        phone_info['line_key_start_index'] = line_key_start_index
        if "Mitel6940" in self.phone_type:
            phone_info['button_map'] = phone_button_map.phone_6940_button_map
        elif "Mitel6930" in self.phone_type:
            phone_info['button_map'] = phone_button_map.phone_6930_button_map
        elif "Mitel6920" in self.phone_type:
            phone_info['button_map'] = phone_button_map.phone_6920_button_map
        #elif "Mitel6910" in self.phone_type:
           # phone_info['button_map'] = phone_button_map.phone_6920_button_map

        if not 'telnet_password' in phone_info:
            phone_info['telnet_password'] = 'J@cquesC@rt1er'
        if not 'ssh_password' in phone_info:
            phone_info['ssh_password'] = 'J@cquesC@rt1er'

        phone_info['tftpServerPath'] = "C:\\TFTP-Root\\"
        # if not 'tftpServer' in phone_info:
        #     phone_info['tftpServer'] = self.getIP()

        Phone6xxxInterface.__init__(self, phone_info)
        if not str(self.get_firmware_version()).startswith('5.2'):
            logger.info('Enable SSH through Telnet')
            self.useTelnet = True
            self.enable_ssh_on_69xx()
        else:
            self.useTelnet =False

    def log_off(self):
        raise NotImplementedError("Implement this function")

    def enable_ssh_on_69xx(self):
        if str(self.get_firmware_version()).startswith('5.1'):
            if self.is_dropbear_ssh_enabled():
                return
            cmd_list = list()
            result = self.phone_telnet_cmd("find /dropbearmulti")
            if "No such file or directory" in result.decode('utf-8'):
                cmd_list.append("tftp -g -r dropbearmulti " + str(self.phone_info['tftpServer']))
            result = self.phone_telnet_cmd("find /dropbear_rsa_host_key")
            if "No such file or directory" in result.decode('utf-8'):
                cmd_list.append("tftp -g -r dropbear_rsa_host_key " + str(self.phone_info['tftpServer']))
            # cmd_list.append("tftp -g -r dropbear_rsa_host_key " + str(self.phone_info['tftpServer']))
            # cmd_list.append("tftp -g -r dropbearmulti " + str(self.phone_info['tftpServer']))
            cmd_list.append("chmod a+x dropbearmulti")
            cmd_list.append("mv dropbear_rsa_host_key /nvdata/etc/")
            cmd_list.append("mv dropbearmulti /usr/bin/")
            cmd_list.append("ln -s /usr/bin/dropbearmulti /usr/bin/dropbearconvert")
            cmd_list.append("ln -s /usr/bin/dropbearmulti /usr/bin/dropbearkey")
            cmd_list.append("ln -s /usr/bin/dropbearmulti /usr/sbin/dropbear")
            #run server
            cmd_list.append("/usr/sbin/dropbear -r /nvdata/etc/dropbear_rsa_host_key")
            self.phone_telnet_cmd(cmd_list)
        else:
            self.phone_telnet_cmd("killall -q dropbear")
            self.phone_telnet_cmd("nice -n 15 /usr/sbin/dropbear -r /nvdata/etc/dropbear_rsa_host_key -P /var/lock/dropbear.pid &")


    # def getIP(self):
    #     try:
    #         sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    #         sock.connect(('10.255.255.255', 1))
    #         return sock.getsockname()[0]
    #     except:
    #         pass

    def get_file_from_phone(self, get_path):
        try:
            if self.useTelnet:
                tftp_cmd = "tftp -p -l " + get_path + " " + str(self.phone_info['tftpServer'])
                self.phone_console_cmd(tftp_cmd)
                time.sleep(30)
            else:
                self.scp_get(get_path)
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception("func '%s' - err: '%s'!" % (fn, err))
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception("func '%s' - err: '%s'!" % (fn, err))

    def phone_telnet_cmd(self, cmd):
        """ Runs cmd via telnet on phone

        :param cmd: ssh cmd
        :type cmd: type str
        :return ret_val: ssh cmd result
        """
        user = "root"
        password = self.phone_info['telnet_password']

        cmd_list = list()
        if type(cmd) is str:
            cmd_list.append(cmd)
        elif type(cmd) is list:
            cmd_list = cmd
        else:
            raise Exception("cmd type %s is not supported" % type(cmd))

        start_time = time.time()
        for command in cmd_list:
            tn = telnetlib.Telnet(self.phone_info['ipAddress'])
            # Hangs if there no sleep
            time.sleep(.1)

            # tn.read_until("login: ")
            tn.write(user + "\n")
            if password:
                tn.read_until("Password: ",8)
                tn.write(password + "\n")
            tn.write(command + '\n')
            tn.write("exit\n")

            result = tn.read_all()
            logger.info("cmd '%s' ran on phone %s" % (command, self.phone_info['ipAddress']))
            tn.close()
        logger.info('Time elapsed for telnet cmd(s): %.3f s\n%s' % ((time.time() - start_time), cmd))

        return result

    def is_dropbear_ssh_enabled(self):
        """
            Check if dropbear is already running

        """
        cmd = "ps -ef | grep /usr/sbin/dropbear"
        result = self.phone_telnet_cmd(cmd)

        if "-r /nvdata/etc/dropbear_rsa_host_key" in result.decode('utf-8'):
            logger.info("Dropbear SSH is already running")
            return True

        return False

    def update_apt_filepath(self, file):
        if self.useTelnet:
            filename = os.path.join(str(self.phone_info["tftpServerPath"]), file)
            return filename
        else:
            return file

    def upload_apt_files_to_phone(self, files_to_upload):
        if not files_to_upload :
                return
        if self.useTelnet:
            for file in files_to_upload:
                tftp_cmd = "tftp -g -r " + file + " " + str(self.phone_info['tftpServer'])
                self.phone_console_cmd(tftp_cmd)
                if "pcm" in file:
                    mv_cmd = 'mv ' + file + ' /tmp/' + file
                    self.phone_console_cmd(mv_cmd)
        else:
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(self.phone_info['ipAddress'],username="admin",key_filename=self.hq_rsa_path)
            with SCPClient(ssh.get_transport()) as scp:
                for file in files_to_upload:
                    filename = os.path.join(self.audio_path,file)
                    try:
                        scp.put(filename)
                    except:
                        raise Exception("An error occured with scp.put(%s) " % filename)

                    if "pcm" in file:
                        # Need to move file to tmp dir otherwise
                        # pxcon will not play the file
                        cmd = 'mv ' + file + ' /tmp/' + file
                        self.phone_console_cmd(cmd, 'su')





