"""
Module to interact with Mitel phones. This is a base class which will be inherited in other phone model specific
classes.
"""
__author__ = "nitin.kumar-2@mitel.com, milton.villeda@mitel.com"

import sys
import os
import clr
import time
import shutil
import base64
import subprocess
import random
import requests
from sys import platform as _platform
from robot.api import logger

# audio imports
from numpy.fft import rfft
from numpy import argmax, mean, diff, log
import numpy
#from matplotlib.mlab import find
from scipy.signal import blackmanharris, fftconvolve
from scipy.signal import butter, filtfilt
from scipy import signal 
import soundfile as sf
from . import parabolic
# end of audio imports
import socket
import paramiko
from paramiko import SSHClient
from scp import SCPClient

from .phone_constants_69xx import led_mode, led_type, line_state

halAudioMap = ['handset','speaker','headset']
class Phone6xxxInterface(object):
    """ 6xxx Phone Interface
    """
    def __init__(self, phone_info, **kwargs):
        """
        It is mandatory to call phone_sanity_check immediately to create the phone objects for mitel phones
        :param args:
        """
        logger.info("Initializing Mitel Phone Base class")
        self.atap_dll_name = "ATAP.dll"
        self.logger_dll_name = "Logger.dll"
        self.mslutil_dll_name = "MSLUtil.dll"
        
        if kwargs.get('atap_dll_path', None) is None:
            atap_dll_path = os.path.join(os.path.dirname(__file__), self.atap_dll_name)
            logger_dll_path = os.path.join(os.path.dirname(__file__), self.logger_dll_name)
            mslutil_dll_path = os.path.join(os.path.dirname(__file__), self.mslutil_dll_name)
        self.atap_dll_path = atap_dll_path
        self.logger_dll_path = logger_dll_path
        self.mslutil_dll_path = mslutil_dll_path
        
        if not os.path.exists(self.atap_dll_path):
            raise Exception("ATAP.dll does not exist in %s" %self.atap_dll_path)
        if not os.path.exists(self.logger_dll_path):
            raise Exception("Logger.dll does not exist in %s" %self.logger_dll_path)
        if not os.path.exists(self.mslutil_dll_path):
            raise Exception("MslUtil.dll does not exist in %s" %self.mslutil_dll_path)

        self.phone_info = phone_info
        self.phone_info['keypressMethod'] = phone_info.get("keypressMethod", "")

        # Add reference to the library
        self.copy_dll_to_pythonpath(self.atap_dll_path)
        self.copy_dll_to_pythonpath(self.logger_dll_path)
        self.copy_dll_to_pythonpath(self.mslutil_dll_path)
        self.add_reference_to_dll(self.atap_dll_name)
        self.create_phone(phone_info)
        # retrieving hardphone enums
        self.keys = sys.modules['PhoneHandler'].HardPhone.Keys
        self.OptionsMenuPages = sys.modules['PhoneHandler'].HardPhone.OptionsMenuPages
        self.OptionsScreens = sys.modules['PhoneHandler'].HardPhone.ScreenNames
        self.MoreTopSoftkeysPages = sys.modules['PhoneHandler'].HardPhone.MoreTopSoftKeysPages
        self.ExpansionKeys = sys.modules['PhoneHandler'].HardPhone.ExpansionKeys
        # the display on phone
        self.phone_display = {}
        # the led buffer
        self.led_buffer = {}
        self.connect_to_phone()
        # Secondary Buffer
        self.secondaryBuffer ={}
        self.phone_display_banner =""
        self.phone_display_foxkeys ={}
        self.phone_display_programmablekeys={}
        self.phone_display_contentscreen={}
        self.Mode = sys.modules['PhoneHandler'].HardPhone.Mode
        self.packet_id = set()
        
    def copy_dll_to_pythonpath(self, dll_path):
        """
        copy dll to the python installation directory
        This dependency which looks like the limitation/bug in .net module could be removed in future
        :param dll_path:
        :return:
        """
        python_installation_dir = os.path.dirname(sys.executable)
        # todo getting exception in copy from robot test case when executed from command line
        try:
            shutil.copy(dll_path, python_installation_dir)
        except Exception as e:
            # logger.warn("Unable to copy %s to %s"%(dll_path, python_installation_dir))
            # logger.warn("Exception occurred: %s"%str(e))
            pass


    def add_reference_to_dll(self, dll_name):
        """
        Add dll to python namespace and import required modules
        :param dll_name: the name of dll
        :return: None
        """
        try:
            import PhoneHandler
        except Exception as e:
            clr.AddReference(dll_name.split('.')[0])
            # importing the modules from the dll
            import PhoneHandler
            import Logger
            Logger.Logger.Initialize()

    def create_phone(self, phone_info):
        """
            This function will create a phone object based on the passed phone details.
            
            Valid phone_types: Mitel6940, Mitel6930, Mitel6xxx, etc.
        """

        phoneModel = phone_info["phoneModel"]
        vdpLogin = phone_info.get("vdpLogin", False)
        extensionNumber = phone_info["extensionNumber"]
        authCode = phone_info.get("authCode", "")
        directoryName = phone_info.get("directoryName", "")
        ipAddress = phone_info["ipAddress"]
        macAddress = phone_info.get("macAddress", "")
        phoneName = phone_info.get("phoneName", "")
        trunkISDN = phone_info.get("trunkISDN", "")
        trunkSIP = phone_info.get("trunkSIP", "")
        trunkPrivateISDN = phone_info.get("trunkPrivateISDN", "")
        trunkPrivateSIP = phone_info.get("trunkPrivateSIP", "")
        trunkH323 = phone_info.get("trunkH323", "")
        trunkSIPForcedGW = phone_info.get("trunkSIPForcedGW", "")
        switchIP = phone_info.get("switchIP", "")
        
        self.hq_rsa = phone_info.get("hq_rsa", "")
        self.hq_rsa_path = os.path.join(os.path.dirname(os.path.dirname(__file__)),'rsa_keys',self.hq_rsa)
        self.audio_path = os.path.join(os.path.dirname(os.path.dirname(__file__)),'audio_analysis')

        self.phone = self.get_object(phoneModel,[phoneModel, vdpLogin, extensionNumber, authCode, directoryName,
                                                 ipAddress, macAddress, phoneName, trunkISDN, trunkSIP, trunkPrivateISDN,
                                                 trunkPrivateSIP, trunkH323, trunkSIPForcedGW,switchIP])
        if not 'tftpServer' in phone_info:
            self.phone_info['tftpServer'] = self.getIP()

    def get_object(self, class_name, params):
        return getattr(sys.modules['PhoneHandler'], class_name)(*params)

    def getIP(self):
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            sock.connect(('10.255.255.255', 1))
            return sock.getsockname()[0]
        except:
            pass
    def connect_to_phone(self):
        self.phone.connectToPhone()
        # after connecting to the phone making off hook and on hook to populate the led buffers
        self.press_key("OffHook")
        time.sleep(1)
        self.press_key("OnHook")
        time.sleep(2)
        self.led_buffer =self.phone.getLEDBuffer()
        logger.info('ATAP Library : '+ self.phone.LibraryVersion)
    def upload_keyrcv_and_run(self):
        self.phone_console_cmd("tftp -g -r keyrecv " + str(self.phone_info['tftpServer']))
        self.phone_console_cmd("chmod 744 keyrecv")
        self.phone_console_cmd("mv keyrecv /bin", options='su')
    
        self.run_keyrecv_binary()
        
    def run_keyrecv_binary(self):
        result = self.phone_console_cmd("ps -ef| grep keyre")
        # Check if binary is already running
        if "/bin/keyrecv" not in str(result):
            self.phone_console_cmd("/bin/keyrecv &", options='su')
                
#############
# Public Methods
#############

    def dial_number(self, num):
        logger.info("Phone6xxxInterface dialing %s" % num)
        self.phone.dialAnumber(num)
        
    def log_off(self):
        raise NotImplementedError("Implement this function")
        
    def phone_sanity_check(self):
        logger.info("IN BASE SANITY FN")
        
    def make_call(self, phone):
        logger.info("Phone6xxxInterface make call to %s" % phone)

        self.phone.callToAnExtension(phone_info_dict['extensionNumber'])
        
    def answer_call(self):
        logger.info("Phone6xxxInterface answer_the_call")
        self.phone.answerTheCall()


    def verify_phone_display(self, phone_info_dict):
        self.phone.verifyInPhoneDisplay(phone_info_dict['extension'])

    def verify_led_notificaion_when_diversion_activated(self):
        """

        This method ...
        Args:

        """
        try:
            self.phone.verifyLEDNotificaionWhenDiversionActivated()
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception('func "%s" - err: "%s"!' % (fn, err))

    def verify_led_notificaion_when_diversion_de_activated(self):
        """

        This method ...
        Args:

        """
        try:
            self.phone.verifyLEDNotificaionWhenDiversionDeActivated()
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception('func "%s" - err: "%s"!' % (fn, err))

    def verify_led_notificaion_when_follow_me_activated(self):
        """

        This method ...
        Args:

        """
        try:
            self.phone.verifyLEDNotificaionWhenFollowMeActivated()
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception('func "%s" - err: "%s"!' % (fn, err))

    def verify_led_notificaion_when_do_not_disturb_activated(self):
        """

        This method ...
        Args:

        """
        try:
            self.phone.verifyLEDNotificaionWhenDoNotDisturbActivated()
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception('func "%s" - err: "%s"!' % (fn, err))

    def verify_call_profile_number(self, profile_number):
        """

        This method ...
        Args:
            profile_number: string

        """
        try:
            self.phone.verifyCallProfileNumber(profile_number)
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception('func "%s" - err: "%s"!' % (fn, err))

    def press_l1key(self):
        """

        This method ...
        Args:

        """
        try:
            self.phone.pressL1key()
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception('func "%s" - err: "%s"!' % (fn, err))

    def press_l2key(self):
        """

        This method ...
        Args:

        """
        try:
            self.phone.pressL2key()
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception('func "%s" - err: "%s"!' % (fn, err))

    def press_offhook(self):
        """

        This method ...
        Args:

        """
        try:
            self.phone.pressOffhook()
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception('func "%s" - err: "%s"!' % (fn, err))

    def press_onhook(self):
        """

        This method ...
        Args:

        """
        try:
            self.phone.OnHook()
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception('func "%s" - err: "%s"!' % (fn, err))

    def press_softkey(self, sk_num=1):
        """

        This method ...
        Args:

        """
        try:
            sk_num = int(sk_num)
            if sk_num == 1:
                self.phone.pressHardKey(sys.modules['PhoneHandler'].HardPhone.Keys.BottomKey1)
            elif sk_num == 2:
                self.phone.pressHardKey(sys.modules['PhoneHandler'].HardPhone.Keys.BottomKey2)
            elif sk_num == 3:
                self.phone.pressHardKey(sys.modules['PhoneHandler'].HardPhone.Keys.BottomKey3)
            elif sk_num == 4:
                self.phone.pressHardKey(sys.modules['PhoneHandler'].HardPhone.Keys.BottomKey4)
            elif sk_num == 5:
                self.phone.pressHardKey(sys.modules['PhoneHandler'].HardPhone.Keys.BottomKey5)
            elif sk_num == 6:
                self.phone.pressHardKey(sys.modules['PhoneHandler'].HardPhone.Keys.BottomKey6)
			
            else:
                raise Exception("FAIL!")
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception('func "%s" - err: "%s"!' % (fn, err))

    def press_softkey_three(self):
        """

        This method ...
        Args:

        """
        try:
            self.phone.pressHardKey(sys.modules['PhoneHandler'].HardPhone.Keys.BottomKey3)
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception('func "%s" - err: "%s"!' % (fn, err))

    def press_mute(self):
        """

        This method ...
        Args:

        """
        try:
            self.phone.pressHardKey(sys.modules['PhoneHandler'].HardPhone.Keys.Mute)
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception('func "%s" - err: "%s"!' % (fn, err))

    def press_hold(self):
        """

        This method ...
        Args:

        """
        try:
            # Sleep is sometimes necessary
            time.sleep(1)
            self.phone.pressHardKey(sys.modules['PhoneHandler'].HardPhone.Keys.Hold)
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception('func "%s" - err: "%s"!' % (fn, err))

    #tchen
    def press_hold_button(self):
        """

        This method ...
        Args:

        """
        self.press_hold()

    def press_park_button(self):
        """

        This method ...
        Args:

        """
        try:
            time.sleep(1)
            self.phone.pressHardKey(sys.modules['PhoneHandler'].HardPhone.Keys.BottomKey4)
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception('func "%s" - err: "%s"!' % (fn, err))

    def confirm_park_button(self):
        """

        This method ...
        Args:

        """
        try:
            self.phone.pressHardKey(sys.modules['PhoneHandler'].HardPhone.Keys.BottomKey3)
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception('func "%s" - err: "%s"!' % (fn, err))
        
    def press_unpark_button(self):
        """

        This method ...
        Args:

        """
        try:
            self.phone.pressHardKey(sys.modules['PhoneHandler'].HardPhone.Keys.BottomKey2)
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception('func "%s" - err: "%s"!' % (fn, err))
    def press_handsfree(self):
        """

        This method ...
        Args:

        """
        try:
            self.phone.pressHardKey(sys.modules['PhoneHandler'].HardPhone.Keys.HandsFree)
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception('func "%s" - err: "%s"!' % (fn, err))

    def press_volumeup(self):
        """

        This method ...
        Args:

        """
        try:
            self.phone.pressHardKey(sys.modules['PhoneHandler'].HardPhone.Keys.IncreaseVolume)
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception('func "%s" - err: "%s"!' % (fn, err))

    def press_volumedown(self):
        """

        This method ...
        Args:

        """
        try:
            self.phone.pressHardKey(sys.modules['PhoneHandler'].HardPhone.Keys.DecreaseVolume)
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception('func "%s" - err: "%s"!' % (fn, err))

    def verify_display_notification_when_in_ring(self, extension):
        """

        This method ...
        Args:
            diversion_category: string

        """
        try:
            ret_bool = self.phone.verifyDisplayNotificationsWhenInRing(extension)
            if not ret_bool:
                raise Exception("extension %s is not displayed on this phone %s" % (extension, self.phone.extensionNumber))
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception('func "%s" - err: "%s"!' % (fn, err))

    def verify_display_notification_when_diversion_activated(self, diversion_category):
        """

        This method ...
        Args:
            diversion_category: string

        """
        try:
            self.phone.verifyDisplayNotificationWhenDiversionActivated(diversion_category)
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception('func "%s" - err: "%s"!' % (fn, err))

    def de_activate_do_not_disturb(self):
        """

        This method ...
        Args:

        """
        try:
            self.phone.deActivateDoNotDisturb()
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception('func "%s" - err: "%s"!' % (fn, err))

    def enable_monitoring(self):
        """

        This method ...
        Args:

        """
        try:
            self.phone.enableMonitoring()
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception('func "%s" - err: "%s"!' % (fn, err))

    def enable_display_monitor(self):
        """

        This method ...
        Args:

        """
        try:
            self.phone.enableDisplayMonitor()
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception('func "%s" - err: "%s"!' % (fn, err))

    def enable_key_monitor(self):
        """

        This method ...
        Args:

        """
        try:
            self.phone.enableKeyMonitor()
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception('func "%s" - err: "%s"!' % (fn, err))

    def enable_led_monitor(self):
        """

        This method ...
        Args:

        """
        try:
            self.phone.enableLEDMonitor()
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception('func "%s" - err: "%s"!' % (fn, err))

    def disable_all_monitors(self):
        """

        This method ...
        Args:

        """
        try:
            self.phone.disableAllMonitors()
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception('func "%s" - err: "%s"!' % (fn, err))

    def enable_line_monitor(self):
        """

        This method ...
        Args:

        """
        try:
            self.phone.enableLineMonitor()
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception('func "%s" - err: "%s"!' % (fn, err))

    def set_to_idle(self):
        """

        This method ...
        Args:

        """
        try:
            self.phone.setToIdle()
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception('func "%s" - err: "%s"!' % (fn, err))

    def get_config(self):
        """

        This method ...
        Args:

        """
        try:
            self.phone.getConfig()
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception('func "%s" - err: "%s"!' % (fn, err))

    def connect_to_terminal(self):
        """

        This method ...
        Args:

        """
        try:
            self.phone.connectToTerminal()
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception('func "%s" - err: "%s"!' % (fn, err))

    def disconnect_terminal(self):
        """

        This method ...
        Args:

        """
        try:
            #self.phone.disconnectTerminal()
            self.phone.setToDefault()
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception('func "%s" - err: "%s"!' % (fn, err))

    def is_phone_in_active_call(self):
        """
        This method checks if the phone is in an active call
        The call canoot be on hold!
        Args:
        """
        try:
            cmd = '/voip/eptShow.sh |grep -i "codec"'
            result = self.phone_console_cmd(cmd)

            if not result:
                logger.warn("Phone is not in active call to determine active audio device")
                # TODO test hold scenario
                raise Exception("Phone is not in active call to determine active audio device")
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception('func "%s" - err: "%s"!' % (fn, err))

    def get_active_audio_device(self):
        """
        This method ...
        Args:
        """
        try:
            # cmd = '/voip/eptShow.sh |grep "is active"|grep -o "(.*)"'
            # result = str(self.phone_console_cmd(cmd))
            phone = self.phone_info['ipAddress']
            result = str(self.phone.activeVoicePath).lower() # 09-12-2019 Prob with fetching active audio path,updated to get from dll.(ENTA-3527)
            logger.info('active audio device on <%s> is %s' % (phone, result))
            return result
            # if "hf-sbaec" in result:
            #     # TODO determine if device is headset
            #     return "speaker"
            # elif "hs-hec" in result:
            #     return "handset"
            # elif "hd-hec" in result:
            #     return "headset"

            raise Exception("Active audio device '%s' is not recognized" % result)

        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception('func "%s" - err: "%s"!' % (fn, err))

    def get_audio_device(self):
        audio_device = 'speaker'
        val = self.get_handsfree_state()

        if val == 0:
            audio_device = 'handset'
        elif val == 1:
            logger.warn("Forcing audio path to headset. Audio testing not supported on headset")
            self.press_handsfree()

            val = self.get_handsfree_state()
            if val == 1:
                raise Exception("audio path should be in handsfree")
            audio_device = 'speaker'
        elif val == 2:
            audio_device = 'speaker'

        return audio_device

#
# AUDIO
    def format_response(self, response_signal):
        """

        This method ...
        Args:
            response_signal: string

        """
        try:
            self.phone.formatResponse(response_signal)
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception('func "%s" - err: "%s"!' % (fn, err))

    def press_hard_key(self, hardkey):
        """

        This method ...
        Args:
            1: HardPhone.Keys

        """
        try:
            if hardkey == '4':
                self.phone.pressHardKey(sys.modules['PhoneHandler'].HardPhone.Keys.DialPad4)
            elif hardkey == '5':
                self.phone.pressHardKey(sys.modules['PhoneHandler'].HardPhone.Keys.DialPad5)
            elif hardkey == '7':
                self.phone.pressHardKey(sys.modules['PhoneHandler'].HardPhone.Keys.DialPad7)
            elif hardkey == '1':
                self.phone.pressHardKey(sys.modules['PhoneHandler'].HardPhone.Keys.DialPad1)

        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception('func "%s" - err: "%s"!' % (fn, err))

##################################################################
#   PHYSICAL BUTTON PRESS using /bin/input command
##################################################################

    def press_physical_button_via_UDP(self, button_str, options=None):
        """This method presse a physical button
            using /bin/input
        Args:
            button_str: button to be pressed

        """
        try:
            exe = 'keysend.exe'
            phone_ip = self.phone_info['ipAddress']
            cmd_switch = '-k'
            if options is 'multiple_btns':
                cmd_switch = '-d'

            dir_path =  os.path.dirname(os.path.realpath(__file__))
            exe_path = os.path.join(dir_path, exe)

            output = subprocess.Popen([exe_path, '-t', phone_ip, cmd_switch, button_str], stdout=subprocess.PIPE)
            out, err = output.communicate()
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception('func "%s" - err: "%s"!' % (fn, err))

    def press_physical_button_via_console(self, button_str, options=None):
        """This method presse a physical button
            using /bin/input
        Args:
            button_str: button to be pressed

        """
        try:
            if options is 'multiple_btns':
                cmd = '/bin/input keystr ' + button_str
            else:
                button = str(self.phone_info['button_map'][button_str.upper()])
                if options is None:
                    cmd = '/bin/input pressrelkey ' + button
                elif options is 'offhook':
                    cmd = '/bin/input setkey ' + button + ' 1'
                elif options is 'onhook':
                    cmd = '/bin/input setkey ' + button + ' 0'
                else:
                    raise Exception("options: '%s' is not supported" % options)

            self.phone_console_cmd(cmd, 'su')
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception('func "%s" - err: "%s"!' % (fn, err))

    def press_physical_button(self, button_str, options=None):
        """This method presse a physical button
            using /bin/input
        Args:
            button_str: button to be pressed

        """
        try:
            if self.phone_info['keypressMethod'] == 'UDP':
                self.press_physical_button_via_UDP(button_str.upper(), options)
            else:
                self.press_physical_button_via_console(button_str, options)
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception('func "%s" - err: "%s"!' % (fn, err))

    def handset_up_down(self):
        """This method ...

        Args:

        """
        try:
            self.press_physical_button('HSW', 'offhook')
            time.sleep(.5)
            self.press_physical_button('HSW', 'onhook')
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception('func "%s" - err: "%s"!' % (fn, err))

##################################################################
#   PHYSICAL BUTTON PRESS       BLOCK END
##################################################################

    def collect_responses(self):
        """

        This method ...
        Args:

        """
        try:
            self.phone.collectResponses()
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception('func "%s" - err: "%s"!' % (fn, err))

    def collect_ack(self):
        """

        This method ...
        Args:

        """
        try:
            self.phone.collectACK()
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception('func "%s" - err: "%s"!' % (fn, err))

    def clear_response_buckets(self):
        """

        This method ...
        Args:

        """
        try:
            self.phone.clearResponseBuckets()
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception('func "%s" - err: "%s"!' % (fn, err))

    def send_request(self, signal_to_be_sent):
        """

        This method ...
        Args:
            signal_to_be_sent: byte[]

        """
        try:
            self.phone.sendRequest(signal_to_be_sent)
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception('func "%s" - err: "%s"!' % (fn, err))

    def send_request_with_fresh_sequence_number(self, signal_to_be_sent):
        """

        This method ...
        Args:
            signal_to_be_sent: byte[]

        """
        try:
            self.phone.sendRequestWithFreshSequenceNumber(signal_to_be_sent)
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception('func "%s" - err: "%s"!' % (fn, err))

    def answer_the_call(self, mode, line_number):
        """

        This method ...
        Args:

        """
        try:
            self.phone.answerTheCall(getattr(self.Mode, mode), line_number) #getattr(self.Mode,"Handset")
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception('func "%s" - err: "%s"!' % (fn, err))

    def reject_the_call(self):
        """

        This method ...
        Args:

        """
        try:
            self.phone.rejectTheCall()
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception('func "%s" - err: "%s"!' % (fn, err))

    def disconnect_the_call(self, line_number):
        """

        This method ...
        Args:

        """
        try:
            logger.info("Disconnecting the call")
            self.phone.disconnectTheActiveCall(line_number) #disconnectTheCall()
        except Exception as err:
            # if 'verifyLineNotificaionWhenInIdle - Mismatch in Line status. Expected 0 in' in str(err) and len(self.get_led_buffer()) == 0:
            #     logger.warn("Trying to disconnect the call when in idle.")
            # else:
            fn = sys._getframe().f_code.co_name
            raise Exception('func "%s" - err: "%s"!' % (fn, err))


    def off_hook(self):
        """

        This method ...
        Args:

        """
        try:
            self.phone.OffHook()
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception('func "%s" - err: "%s"!' % (fn, err))

    def on_hook(self):
        """

        This method ...
        Args:

        """
        try:
            self.phone.OnHook()
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception('func "%s" - err: "%s"!' % (fn, err))

    def call_to_an_extension(self, extension_to_be_called,**kwargs):
        """

        This method ...
        Args:
            extension_to_be_called: HardPhone

        """
        try:
            logger.info("Calling the extension %s"%(extension_to_be_called))
            self.phone.callToAnExtension(extension_to_be_called,getattr(self.Mode,kwargs.get('mode','Handset')))
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception('func "%s" - err: "%s"!' % (fn, err))

    def dial_service_code(self, service_code):
        """

        This method ...
        Args:
            service_code: string

        """
        try:
            self.phone.dialServiceCode(service_code)
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception('func "%s" - err: "%s"!' % (fn, err))

    def enter_a_number(self, terminal_phone):
        """

        This method ...
        Args:
            terminal_phone: HardPhone

        """
        try:
            self.phone.EnterAnumber(terminal_phone)
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception('func "%s" - err: "%s"!' % (fn, err))

    def dial_anumber(self, number_to_be_dialled):
        """

        This method ...
        Args:
            number_to_be_dialled: string

        """
        try:
            self.phone.dialAnumber(number_to_be_dialled)
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception('func "%s" - err: "%s"!' % (fn, err))

    # def dial_anumber(self, string_to_be_verified):
    #     """
    #
    #     This method ...
    #     Args:
    #         string_to_be_verified: string
    #
    #     """
    #     try:
    #         self.phone.dialAnumber(string_to_be_verified)
    #     except Exception as err:
    #         fn = sys._getframe().f_code.co_name
    #         raise Exception('func "%s" - err: "%s"!' % (fn, err))

    def press_key(self, key_to_be_pressed, press_count=1):
        """

        This method ...
        Args:
            key_to_be_pressed: int

        """
        try:
            self.phone.pressHardKey(getattr(self.keys,key_to_be_pressed), press_count)
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception('func "%s" - err: "%s"!' % (fn, err))

    def long_press_key(self, key_to_be_pressed, press_count=1):
        """

        This method ...
        Args:
            key_to_be_pressed: int

        """
        try:
            self.phone.longPressHardKey(getattr(self.keys,key_to_be_pressed), press_count)
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception('func "%s" - err: "%s"!' % (fn, err))

    def press_expansion_box_key(self, key_to_be_pressed, press_count=1):
        """

        This method will press a key in the extension box...
        Args:
            key_to_be_pressed: int

        """
        try:
            self.phone.pressHardKeyInExpansionModule(getattr(self.ExpansionKeys,key_to_be_pressed), press_count)
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception('func "%s" - err: "%s"!' % (fn, err))


    def release_key(self, key_to_be_released):
        """

        This method ...
        Args:
            key_to_be_released: HardPhone.Keys

        """
        try:
            self.phone.releaseKey(key_to_be_released)
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception('func "%s" - err: "%s"!' % (fn, err))


    def input_a_number(self, string_to_dial):
        """

        This method ...
        Args:
            string_to_dial: string

        """
        try:
            self.phone.inputANumber(string_to_dial)
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception('func "%s" - err: "%s"!' % (fn, err))

    def call_from_remote_extension(self, number_r1):
        """

        This method ...
        Args:
            number_r1: HardPhone

        """
        try:
            self.phone.callFromRemoteExtension(number_r1)
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception('func "%s" - err: "%s"!' % (fn, err))

    def call_from_sip_mobile_extension(self, number_r1):
        """

        This method ...
        Args:
            number_r1: HardPhone

        """
        try:
            self.phone.callFromSIPMobileExtension(number_r1)
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception('func "%s" - err: "%s"!' % (fn, err))

    def activate_ic_sdiversion_with_service_codes(self, diversion_category):
        """

        This method ...
        Args:
            diversion_category: string

        """
        try:
            self.phone.activateICSdiversionWithServiceCodes(diversion_category)
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception('func "%s" - err: "%s"!' % (fn, err))

    def activate_dn_dwith_service_code_and_verify_notifications(self, string_to_be_verified):
        """

        This method ...
        Args:
            string_to_be_verified: string

        """
        try:
            self.phone.activateDNDwithServiceCodeAndVerifyNotifications(string_to_be_verified)
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception('func "%s" - err: "%s"!' % (fn, err))

    def activate_dn_dwith_service_code(self):
        """

        This method ...
        Args:

        """
        try:
            self.phone.activateDNDwithServiceCode()
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception('func "%s" - err: "%s"!' % (fn, err))

    def deactivate_dn_dwith_service_code(self):
        """

        This method ...
        Args:

        """
        try:
            self.phone.deactivateDNDwithServiceCode()
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception('func "%s" - err: "%s"!' % (fn, err))

    def deactivate_group_dn_dwith_service_code(self, group_number):
        """

        This method ...
        Args:
            group_number: string

        """
        try:
            self.phone.deactivateGroupDNDwithServiceCode(group_number)
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception('func "%s" - err: "%s"!' % (fn, err))

    def dial_service_code_and_verify_display(self, string_to_be_verified):
        """

        This method ...
        Args:
            string_to_be_verified: string

        """
        try:
            self.phone.dialServiceCodeAndVerifyDisplay(string_to_be_verified)
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception('func "%s" - err: "%s"!' % (fn, err))

    def activate_group_dn_dwith_service_code(self, group_number):
        """

        This method ...
        Args:
            group_number: string

        """
        try:
            self.phone.activateGroupDNDwithServiceCode(group_number)
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception('func "%s" - err: "%s"!' % (fn, err))

    def check_phone_connection(self):
        """

        This method ...
        Args:

        """
        try:
            self.phone.checkPhoneConnection()
            time.sleep(1)
            logger.info('ATAP Library: ' + self.phone.LibraryVersion)
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception('func "%s" - err: "%s"!' % (fn, err))


    def program_follow_me_remotely(self, extension_number_to_be_routed):
        """

        This method ...
        Args:
            extension_number_to_be_routed: string

        """
        try:
            self.phone.programFollowMeRemotely(extension_number_to_be_routed)
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception('func "%s" - err: "%s"!' % (fn, err))

    def cancel_active_call_back(self):
        """

        This method ...
        Args:

        """
        try:
            self.phone.cancelActiveCallBack()
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception('func "%s" - err: "%s"!' % (fn, err))

    def login_with_dual_forking_extension(self, dual_forking_extension_number):
        """

        This method ...
        Args:
            dual_forking_extension_number: string

        """
        try:
            self.phone.loginWithDualForkingExtension(dual_forking_extension_number)
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception('func "%s" - err: "%s"!' % (fn, err))

    def login_with_different_extension(self, extension_number):
        """

        This method ...
        Args:
            extension_number: string

        """
        try:
            self.phone.loginWithDifferentExtension(extension_number)
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception('func "%s" - err: "%s"!' % (fn, err))

    def login_back_with_base_extension(self):
        """

        This method ...
        Args:

        """
        try:
            self.phone.loginBackWithBaseExtension()
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception('func "%s" - err: "%s"!' % (fn, err))

    def pick_call_with_non_member_of_group(self, extension):
        """

        This method ...
        Args:
            extension: string

        """
        try:
            self.phone.PickCallWithNonMemberOfGroup(extension)
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception('func "%s" - err: "%s"!' % (fn, err))

    def pick_call_with_member_of_group(self):
        """

        This method ...
        Args:

        """
        try:
            self.phone.PickCallWithMemberOfGroup()
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception('func "%s" - err: "%s"!' % (fn, err))

    def verify_line_state(self,LineStatus, LineNumber=1, activeLineNum=1, maxWaitTimeoutInSeconds = 10):
        """

        This method ...
        Args:

        """
        try:
            line_buffer = self.get_line_buffer()
            if activeLineNum in line_buffer.keys() and len(line_buffer) != 0:
                if len(LineStatus) <= 2:
                    return self.phone.verifyLineState(str(LineStatus),str(LineNumber), str(activeLineNum), int(maxWaitTimeoutInSeconds))
                else:
                    return self.phone.verifyLineState(str(self.phone_info['line_state'][LineStatus]),str(LineNumber), str(activeLineNum), int(maxWaitTimeoutInSeconds))
            else:
                logger.warn("Line buffers are empty or the requested active line is not present in the buffer")
                logger.warn("Line buffer is <%s>"%line_buffer)
                return LineStatus == "idle"
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception('func "%s" - err: "%s"!' % (fn, err))

    def get_line_buffer(self):
        """This method will return the buffer containing details of all lines on the phone...
        The return values are in decimal

        Args: None

        """
        try:
            dict = {}
            buffers = self.phone.getLINEbuffer()
            for buffer in buffers:
                dict[buffer.Key] = buffer.Value
            return dict
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception('func "%s" - err: "%s"!' % (fn, err))

    def verify_led_state(self,ledtype, mode,color, timeout = 10):
        """

        this method will verify the status of a led...
        Args: type : type of the led -> Table 8 of atap document
        mode : mode of led -> Table 9 of atap document
        timeout : max time to wait

        Args : Type and mode should be provided in hex format

        """
        try:
            #if self.phone_info['phoneModel'] in ['Mitel6865i', 'Mitel6867i', 'Mitel6869i']:  # ENTA 5000 and 5284
            #    if ledtype == 'Line1':
            #        ledtype = 'indicator_line'
            if "Line" in ledtype:
                key_num = ledtype.split("Line")[-1]
                # start_num = 23  # as per atap doc as function1 is 24
                start_num = self.phone_info['line_key_start_index']
                hex_key_val = (hex(start_num + int(key_num)))[2:]
                _ledtype = hex_key_val.upper()
            else:
                _ledtype = str(self.phone_info['led_type'][ledtype])
            # no need to update self.led_buffer as the same is bing done in dll
            # here self.led_buffer is useful to query the led before any key is pressed on the phone e.g. blinking MWI
            for _ in range(10):
                time.sleep(0.5)
                led_buffer = self.get_led_buffer()
                if not len(led_buffer):
                    led_buffer = self.led_buffer
                
                if str(type(led_buffer)) == str(list):  # ENTA 5513 : LED for 6940
                    if not len(led_buffer):
                        logger.warn("The response bucket is empty. Pressing vol decrease btn to populate the response bucket")
                        #self.press_key("DecreaseVolume")
                        led_buffer = {}
                elif str(type(led_buffer)) == str(dict):
                    pass
                else:
                    if not led_buffer.Count:
                        logger.warn("The response bucket is empty. Pressing vol decrease btn to populate the response bucket")
                        #self.press_key("DecreaseVolume")
                        led_buffer = {}
                
                if len(led_buffer) != 0 and str(int(_ledtype,16)) in led_buffer.keys():
                    if ',' in str(led_buffer[str(int(_ledtype, 16))]):
                        actual_mode = str.split(str(led_buffer[str(int(_ledtype, 16))]), ',')[0]
                        actual_color = str.split(str(led_buffer[str(int(_ledtype, 16))]), ',')[1]
                    else:
                        actual_mode = led_buffer[str(int(_ledtype, 16))]
                        actual_color = "NA" # lower Firmwares doesnt send color.
                    #     03-12-2019 Added color verification : Shankara Narayanan. M

                    if not color or str.lower(mode) == 'off':
                        if mode in ["blink", "blinking", "flash", "flashing"]:
                            return actual_mode in self.phone_info['led_mode']["blink"]
                        else:
                            return actual_mode == str(self.phone_info['led_mode'][mode])
                    else:
                        if mode in ["blink", "blinking", "flash", "flashing"]:
                            if actual_mode in self.phone_info['led_mode']["blink"] and str.lower(actual_color) == str.lower(color):
                                return True
                        else:
                            if actual_mode == str(self.phone_info['led_mode'][mode]) and str.lower(actual_color) == str.lower(color):
                                return True
                    return  False
                else:
                    logger.warn("Led buffers are empty or the requested led is not in the buffer")
                    return mode.lower() == "off"
            else:
                return False
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception('func "%s" - err: "%s"!' % (fn, err))

    def get_led_buffer(self):
        """This method will return the buffer containing details of all leds on the phone...
            The return values are in decimal
        Args: None

        """
        try:
            dict = {}
            buffers = self.phone.getLEDBuffer()
            for buffer in buffers:
                dict[buffer.Key] = buffer.Value
            return dict
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception('func "%s" - err: "%s"!' % (fn, err))


    # Deprecated 15-07-2010 Shankara Narayanan. M
    # def get_icon_buffer(self):
    #     """This method will return the buffer containing details of all leds on the phone...
    #         The return values are in decimal
    #     Args: None
    #
    #     """
    #     try:
    #         dict = {}
    #         buffers = self.phone.getIconBuffer()
    #         for buffer in buffers:
    #             dict[buffer.Key] = buffer.Value
    #         return dict
    #     except Exception as err:
    #         fn = sys._getframe().f_code.co_name
    #         raise Exception('func "%s" - err: "%s"!' % (fn, err))

    def get_icon_buffer(self):
        """This method will return the buffer containing details of Icon Responses from the phone...
        Args: None

        """

        try:
            iconBuffer=[]
            buffers = self.phone.getAllIconBuffer()
            for iconPackets in buffers: # List of Icon packets
                dict = {}
                for iconAttributes in iconPackets: # attributes in dict
                    dict[iconAttributes.Key] = iconAttributes.Value
                iconBuffer.append(dict)
                # dict.clear()
            return iconBuffer
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception('func "%s" - err: "%s"!' % (fn, err))

    def get_ringer_buffer(self):
        """This method will return the buffer containing details of Ringer Responses from the phone...
        Args: None

        """
        try:
            ringBuffer=[]
            buffers = self.phone.getRingerStates()
            for buffer in buffers:
                dict = {}
                dict['RingerType'] = buffer['RingerType']
                dict['RingerState'] = buffer['RingerState']
                dict['RingerTone'] = buffer['RingerTone']
                dict['RingerCadence'] = buffer['RingerCadence']
                dict['RingerVolume'] = buffer['RingerVolume']
                ringBuffer.append(dict)
                # dict.clear()
            return ringBuffer
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception('func "%s" - err: "%s"!' % (fn, err))


    def verify_ringer_state(self,ring_state,**kwargs):
        """
        this method will verify the states of a Ringer...
        Args: ring_state can be Ringing / off.
        Note: For 'Off', all other kwargs are invalid.
        kwargs: RingerType, RingerTone , RingerCadence, RingerVolume
        """
        try:
            for _ in range(10):
                time.sleep(0.5)
                ringer_buffer = self.get_ringer_buffer()
                for ringer in ringer_buffer:
                    if str(ringer.get('RingerState')).lower() == str(ring_state).lower():
                        if kwargs.get('RingerType') and str(kwargs.get('RingerType')).lower() != str(ringer.get('RingerType')).lower():
                            logger.error("Missmatch in Ringer Type, Expected: "+ str(kwargs.get('RingerType'))+", Actual: "+str(ringer.get('RingerType')))
                            return False
                        if kwargs.get('RingerTone') and str(kwargs.get('RingerTone')).lower() != str(ringer.get('RingerTone')).lower():
                            logger.error("Missmatch in Ringer Tone, Expected: "+ str(kwargs.get('RingerTone'))+", Actual: "+str(ringer.get('RingerTone')))
                            return False
                        if kwargs.get('RingerCadence') and str(kwargs.get('RingerCadence')).lower() != str(ringer.get('RingerCadence')).lower():
                            logger.error("Missmatch in Ringer Cadence, Expected: "+ str(kwargs.get('RingerCadence'))+", Actual: "+str(ringer.get('RingerCadence')))
                            return False
                        if kwargs.get('RingerVolume') and str(kwargs.get('RingerVolume')).lower() != str(ringer.get('RingerVolume')).lower():
                            logger.error("Missmatch in Ringer Volume, Expected: "+ str(kwargs.get('RingerVolume'))+", Actual: "+str(ringer.get('RingerVolume')))
                            return False
                        return True
            return False
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception('func "%s" - err: "%s"!' % (fn, err))

    
    def verify_icon_state(self,iconIndex, icon, iconText):
        """

        this method will verify the states of a icons...
        Args: iconIndex and icon:

        """
        try:
            for _ in range(10):
                time.sleep(0.5)
                icon_buffer = self.get_icon_buffer()
                if len(icon_buffer) != 0 and str(int(iconIndex,16)) in icon_buffer.keys():
                    # Added Icon Text to icon info 09-01-2020
                    # if str(icon_buffer[str(int(iconIndex, 16))]).lower() ==str(icon).lower():
                    if str(icon_buffer[str(int(iconIndex, 16))]).lower().split(':')[0] ==str(icon).lower():
                        if iconText:
                            if str(icon_buffer[str(int(iconIndex, 16))]).lower().split(':')[1] ==str(iconText).lower():
                                return True
                            else:
                                logger.error('Icon text verification failed, Actual: '+str(icon_buffer[str(int(iconIndex, 16))]).lower().split(':')[1] +', Expected: '+ iconText)
                                return False
                        else:
                            return True
            return False
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception('func "%s" - err: "%s"!' % (fn, err))

    def set_line_for_hunt_group(self, hunt_group_number):
        """

        This method ...
        Args:
            hunt_group_number: string

        """
        try:
            self.phone.setLineForHuntGroup(hunt_group_number)
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception('func "%s" - err: "%s"!' % (fn, err))

    def remove_line_for_hunt_group(self, hunt_group_number):
        """

        This method ...
        Args:
            hunt_group_number: string

        """
        try:
            self.phone.removeLineForHuntGroup(hunt_group_number)
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception('func "%s" - err: "%s"!' % (fn, err))

    def enable_message_waiting(self, extension):
        """

        This method ...
        Args:
            extension: string

        """
        try:
            self.phone.enableMessageWaiting(extension)
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception('func "%s" - err: "%s"!' % (fn, err))

    def intrusion_from_extension(self, extension):
        """

        This method ...
        Args:
            extension: HardPhone

        """
        try:
            self.phone.IntrusionFromExtension(extension)
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception('func "%s" - err: "%s"!' % (fn, err))

    def verify_notifications_when_pe_ndeactivated(self):
        """

        This method ...
        Args:

        """
        try:
            self.phone.verifyNotificationsWhenPENdeactivated()
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception('func "%s" - err: "%s"!' % (fn, err))

    def verify_reroutingto_in_attend_when_not_responding(self, phone2):
        """

        This method ...
        Args:
            phone2: string

        """
        try:
            self.phone.verifyReroutingtoInAttendWhenNotResponding(phone2)
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception('func "%s" - err: "%s"!' % (fn, err))

    def verify_reroutingto_in_attend_when_cancel_call(self, phone2):
        """

        This method ...
        Args:
            phone2: string

        """
        try:
            self.phone.verifyReroutingtoInAttendWhenCancelCall(phone2)
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception('func "%s" - err: "%s"!' % (fn, err))

    def verify_reroutingto_in_attend_when_dial_vacant_number(self, vacant_number):
        """

        This method ...
        Args:
            vacant_number: string

        """
        try:
            self.phone.verifyReroutingtoInAttendWhenDialVacantNumber(vacant_number)
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception('func "%s" - err: "%s"!' % (fn, err))

    def verify_reroutingto_in_attend_when_dial_logged_off_terminal(self, phone2):
        """

        This method ...
        Args:
            phone2: string

        """
        try:
            self.phone.verifyReroutingtoInAttendWhenDialLoggedOffTerminal(phone2)
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception('func "%s" - err: "%s"!' % (fn, err))

    def verify_private_trunk_reroutingto_in_attend_when_not_responding(self, phone2):
        """

        This method ...
        Args:
            phone2: string

        """
        try:
            self.phone.verifyPrivateTrunkReroutingtoInAttendWhenNotResponding(phone2)
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception('func "%s" - err: "%s"!' % (fn, err))

    def verify_private_reroutingto_in_attend_when_cancel_call(self, phone2):
        """

        This method ...
        Args:
            phone2: string

        """
        try:
            self.phone.verifyPrivateReroutingtoInAttendWhenCancelCall(phone2)
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception('func "%s" - err: "%s"!' % (fn, err))

    def verify_private_reroutingto_in_attend_when_dial_vacant_number(self, vacant_number):
        """

        This method ...
        Args:
            vacant_number: string

        """
        try:
            self.phone.verifyPrivateReroutingtoInAttendWhenDialVacantNumber(vacant_number)
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception('func "%s" - err: "%s"!' % (fn, err))

    def verify_private_reroutingto_in_attend_when_dial_logged_off_terminal(self, phone2):
        """

        This method ...
        Args:
            phone2: string

        """
        try:
            self.phone.verifyPrivateReroutingtoInAttendWhenDialLoggedOffTerminal(phone2)
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception('func "%s" - err: "%s"!' % (fn, err))

    def verify_external_call_to_in_attend(self, in_attend_number):
        """

        This method ...
        Args:
            in_attend_number: string

        """
        try:
            self.phone.verifyExternalCallToInAttend(in_attend_number)
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception('func "%s" - err: "%s"!' % (fn, err))

    def verify_line_notificaion_when_do_not_disturb_activated(self):
        """

        This method ...
        Args:

        """
        try:
            self.phone.verifyLineNotificaionWhenDoNotDisturbActivated()
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception('func "%s" - err: "%s"!' % (fn, err))

    def set_to_default(self):
        """

        This method ...
        Args:

        """
        try:
            self.phone.setToDefault()
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception('func "%s" - err: "%s"!' % (fn, err))

    def check_phone_is_online(self):
        """

        This method ...
        Args:

        """
        try:
            self.phone.checkPhoneIsOnline()
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception('func "%s" - err: "%s"!' % (fn, err))

    def sleep(self, seconds):
        """

        This method ...
        Args:
            seconds: double

        """
        try:
            self.phone.sleep(seconds)
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception('func "%s" - err: "%s"!' % (fn, err))

    def make_delay(self, sec=2):
        """

        This method ...
        Args:
            2.0: double

        """
        try:
            sleep(sec)
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception('func "%s" - err: "%s"!' % (fn, err))

    def deactivate_follow_me(self):
        """

        This method ...
        Args:

        """
        try:
            self.phone.deactivateFollowMe()
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception('func "%s" - err: "%s"!' % (fn, err))

    def activate_direct_diversion(self, extension_number):
        """

        This method ...
        Args:
            extension_number: string

        """
        try:
            self.phone.activateDirectDiversion(extension_number)
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception('func "%s" - err: "%s"!' % (fn, err))

    def verify_display_message_contents(self, contents):
        """

        This method ...
        Args:

        """
        try:
            return self.verify_display_on_screen(contents)
            # logger.info("verify_display_message_contents")
            # result = False
            # try:
            #     result = self.phone.verifyInDisplayResponses(contents)
            #     return result
            # except Exception as e: # as verifyInDisplayResponses never returns false
            #     logger.warn("Pressing vol decrease btn to populate the display buffers.")
            #     allcontent = self.get_phone_display("idle")
            #     if contents in allcontent:
            #         result = True
            #     else:
            #         logger.error("Expected: %s\nGot: %s"%(contents,allcontent))
            # return result
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception('func "%s" - err: "%s"!' % (fn, err))

    # def verify_in_displayBanner(self, contentToBeVerified):
    #     self.get_all_screen_content()
    #     print((self.phone_display_banner))
    #     # if self.phone.phoneModel.contains('6910'):
    #     #     print("Banners are not defined in Mitel 6910 phones")
    #     #     return False
    #     # else:
    #     #     if contentToBeVerified in self.phone_display_banner:
    #     #         return  True
    #     #     else:
    #     #         return  False
    # def verify_in_FoxKeys(self, contentToBeVerified):
    #     self.get_all_screen_content()
    #     print((self.phone_display_foxkeys.values()))
    #     # if self.phone.phoneModel.contains('6910'):
    #     #     print("Fox keys are not defined in Mitel 6910 phones")
    #     #     return False
    #     # else:
    #     #     if contentToBeVerified in self.phone_display_foxkeys:
    #     #         return  True
    #     #     else:
    #     #         return  False
    # def verify_in_ProgrammableKeys(self, contentToBeVerified):
    #     self.get_all_screen_content()
    #     print((self.phone_display_programmablekeys.values()))
    #     # if self.phone.phoneModel.contains('6910'):
    #     #     print("Programmable keys are not defined in Mitel 6910 phones")
    #     #     return False
    #     # else:
    #     #     if contentToBeVerified in self.phone_display_programmablekeys:
    #     #         return  True
    #     #     else:
    #     #         return  False
    #
    # def verify_in_ContentScreen(self, contentToBeVerified):
    #     self.get_all_screen_content()
    #     # print((self.phone_display_contentscreen.values()))
    #
    #     if contentToBeVerified in self.phone_display_contentscreen:
    #         return  True
    #     else:
    #         return  False

    def verify_display_on_screen(self, contents, **kwargs):
        """This method will verify the contents on the phone screen
        Args: contents: string to be verified
        """
        try:
            if self.phone.verifyInDisplayResponses(contents):
                return True
        except:
            #08-11-2019: Phone sends incomplete screen info after a screen reset.To overcome vol down key is pressed once, which will make the phone to send complete info
            self.press_key("DecreaseVolume")
            try:
                if self.phone.verifyInDisplayResponses(contents):
                    return True
            except:
                #self.capture_screenshot()
                self.get_all_screen_content()
                if self.phone.phoneModel in ["Mitel6910"]:
                    logger.error("Contents         : %s \n"%(" ".join(self.phone_display_contentscreen.values())))
                elif self.phone.phoneModel in ["Mitel6867i"]:
                    logger.error("Contents         : %s \n"%(self.phone_display_contents))
                else:
                    logger.error("Expected Message : '%s'"%contents)
                    logger.error("Available Contents in Phone %s are below \n" %self.phone.extensionNumber)
                    logger.error("Banner           : %s" % (self.phone_display_banner))
                    logger.error("Programmable Keys: %s"%(", ".join(self.phone_display_programmablekeys.values())))
                    logger.error("Bottom Soft Keys : %s"%(", ".join(self.phone_display_foxkeys.values())))
                #logger.error("oldBuffer        : %s \n" % (self.phone_display_contents))
                #logger.error("Contents in Secondary Display Buffer: %s"%(self.secondaryBuffer.keys()))
                return False
        # except Exception as err:
        #     fn = sys._getframe().f_code.co_name
        #     raise Exception('func "%s" - err: "%s"!' % (fn, err))

    def verify_notifications_when_in_ring(self,LineNumber=1):
        """

        This method ...
        Args:

        """
        try:
            logger.info("Verifying the notifications in ring")
            self.phone.verifyNotificationsWhenInRing(LineNumber)
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception('func "%s" - err: "%s"!' % (fn, err))

    def verify_notifications_when_call_back_ring(self, extension_to_be_verified):
        """

        This method ...
        Args:
            extension_to_be_verified: string

        """
        try:
            self.phone.verifyNotificationsWhenCallBackRing(extension_to_be_verified)
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception('func "%s" - err: "%s"!' % (fn, err))

    def verify_notifications_when_ed_ngets_call(self, number_of_responses_to_be_stored):
        """

        This method ...
        Args:
            number_of_responses_to_be_stored: int

        """
        try:
            self.phone.verifyNotificationsWhenEDNgetsCall(number_of_responses_to_be_stored)
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception('func "%s" - err: "%s"!' % (fn, err))

    def verify_notification_when_message_waiting(self):
        """

        This method ...
        Args:

        """
        try:
            self.phone.verifyNotificationWhenMessageWaiting()
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception('func "%s" - err: "%s"!' % (fn, err))

    def verify_notifications_when_in_idle(self):
        """

        This method ...
        Args:

        """
        try:
            self.phone.verifyNotificationsWhenInIdle()
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception('func "%s" - err: "%s"!' % (fn, err))

    # def verify_notifications_when_in_idle(self, str_to_bo_verified):
        # """

        # This method ...
        # Args:
            # str_to_bo_verified: string

        # """
        # try:
            # self.phone.verifyNotificationsWhenInIdle(str_to_bo_verified)
        # except Exception as err:
            # fn = sys._getframe().f_code.co_name
            # raise Exception('func "%s" - err: "%s"!' % (fn, err))

    def verify_notifications_when_in_busy(self):
        """

        This method ...
        Args:

        """
        try:
            self.phone.verifyNotificationsWhenInBusy()
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception('func "%s" - err: "%s"!' % (fn, err))


    def verify_notifications_when_in_connected(self):
        """

        This method ...
        Args:

        """
        try:
            logger.info("Verify the notifications when in connected.")

            self.phone.verifyLineNotificaionWhenInConnected()
            # self.phone.verifyNotificationsWhenInConnected()
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception('func "%s" - err: "%s"!' % (fn, err))

    def verify_notifications_when_follow_me_activated(self, remote_number):
        """

        This method ...
        Args:
            remote_number: string

        """
        try:
            self.phone.verifyNotificationsWhenFollowMeActivated(remote_number)
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception('func "%s" - err: "%s"!' % (fn, err))

    def verify_notifications_when_diversion_activated(self, diversion_category):
        """

        This method ...
        Args:
            diversion_category: string

        """
        try:
            self.phone.verifyNotificationsWhenDiversionActivated(diversion_category)
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception('func "%s" - err: "%s"!' % (fn, err))

    def verify_notifications_when_diversion_de_activated(self):
        """

        This method ...
        Args:

        """
        try:
            self.phone.verifyNotificationsWhenDiversionDeActivated()
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception('func "%s" - err: "%s"!' % (fn, err))

    def verify_led_notifications_when_pe_ndeactivated(self):
        """

        This method ...
        Args:

        """
        try:
            self.phone.verifyLEDNotificationsWhenPENdeactivated()
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception('func "%s" - err: "%s"!' % (fn, err))

    def verify_notifications_when_in_clearing(self):
        """

        This method ...
        Args:

        """
        try:
            self.phone.verifyNotificationsWhenInClearing()
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception('func "%s" - err: "%s"!' % (fn, err))

    def verify_line_notificaion_when_in_idle(self):
        """

        This method ...
        Args:

        """
        try:
            self.phone.verifyLineNotificaionWhenInIdle()
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception('func "%s" - err: "%s"!' % (fn, err))

    def verify_line_notificaion_when_in_clearing(self):
        """

        This method ...
        Args:

        """
        try:
            self.phone.verifyLineNotificaionWhenInClearing()
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception('func "%s" - err: "%s"!' % (fn, err))

    def verify_line_notificaion_when_in_connected(self):
        """

        This method ...
        Args:

        """
        try:
            self.phone.verifyLineNotificaionWhenInConnected()
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception('func "%s" - err: "%s"!' % (fn, err))

    def verify_line_notificaion_when_out_going(self):
        """

        This method ...
        Args:

        """
        try:
            self.phone.verifyLineNotificaionWhenOutGoing()
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception('func "%s" - err: "%s"!' % (fn, err))

    def verify_led_notificaion_when_in_idle(self):
        """

        This method ...
        Args:

        """
        try:
            self.phone.verifyLEDNotificaionWhenInIdle()
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception('func "%s" - err: "%s"!' % (fn, err))

    def verify_call_list_profile(self, profile_number):
        """

        This method ...
        Args:
            profile_number: string

        """
        try:
            self.phone.verifyCallListProfile(profile_number)
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception('func "%s" - err: "%s"!' % (fn, err))

    def verify_notifications_when_do_not_disturb_activated(self):
        """

        This method ...
        Args:

        """
        try:
            self.phone.verifyNotificationsWhenDoNotDisturbActivated()
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception('func "%s" - err: "%s"!' % (fn, err))

    def verify_line_notifications_when_do_not_disturb_activated(self):
        """

        This method ...
        Args:

        """
        try:
            self.phone.verifyLineNotificationsWhenDoNotDisturbActivated()
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception('func "%s" - err: "%s"!' % (fn, err))

    def verify_display_contents(self, string_to_be_verified):
        """

        This method ...
        Args:
            string_to_be_verified: string

        """
        try:
            self.phone.verifyDisplayContents(string_to_be_verified)
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception('func "%s" - err: "%s"!' % (fn, err))

    def verify_caller_name(self, phone, ca):
        """

        This method ...
        Args:
            string_to_be_verified: string

        """
        try:
            logger.info("TODO")
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception('func "%s" - err: "%s"!' % (fn, err))
    def verify_in_phone_display(self, string_to_be_verified):
        """

        This method ...
        Args:
            string_to_be_verified: string

        """
        try:
            logger.info("Verifying %s in the phone display"%string_to_be_verified)
            return self.phone.verifyInDisplayResponses(string_to_be_verified)
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception('func "%s" - err: "%s"!' % (fn, err))

    def get_phone_display(self, phone_mode = "non idle"):
        """

        returns everything on the phone display when the phones are in call
        Args:
            None

        """
        try:
            logger.info("Getting the phone display")
            if phone_mode == "idle":
                self.press_key("DecreaseVolume")
            return self.phone.getAllDisplayResponses()
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception('func "%s" - err: "%s"!' % (fn, err))

    def get_all_screen_content(self):
        """

        returns everything on the phone display when the phones are in call
        Args:
            None

        """
        try:
            # import pdb;
            # pdb.Pdb(stdout=sys.__stdout__).set_trace()
            logger.info("Getting the contents on the screen")
            self.phone_display_contentscreen.clear()
            self.phone_display_foxkeys.clear()
            self.phone_display_programmablekeys.clear()

            data = self.phone.getAllDisplayResponses("1")
            self.secondaryBuffer = data  # Just a copy of entire display buffer so that nothing is lost when sorted with location
            #if not data.Count:
            if str(type(data)) == str(list):
                if not len(data):
                    logger.warn("The response bucket is empty. Pressing vol decrease btn to populate the response bucket")
                    self.press_key("DecreaseVolume")
                    data = self.phone.getAllDisplayResponses("1")
                    self.secondaryBuffer = data
            else:
                if not data.Count:
                    logger.warn("The response bucket is empty. Pressing vol decrease btn to populate the response bucket")
                    self.press_key("DecreaseVolume")
                    data = self.phone.getAllDisplayResponses("1")
                    self.secondaryBuffer = data
            if self.phone.phoneModel in ["Mitel6910", "Mitel6865i"]:
                for content in data:
                    self.phone_display[content.DisplayMessageBody.Row + content.DisplayMessageBody.Column] = content.DisplayMessageBody.Data
                    self.phone_display_contents = ' '.join(self.phone_display.viewvalues())
                    self.phone_display_contentscreen[content.DisplayMessageBody.Row + content.DisplayMessageBody.Column] = content.DisplayMessageBody.Data
            elif self.phone.phoneModel in ["Mitel6867i"]:
                self.phone_display_contents =""
                for content in data:
                    #self.phone_display[content.DisplayMessageBody.Row + content.DisplayMessageBody.Column] = content.DisplayMessageBody.Data
                    self.phone_display_contents += content.DisplayMessageBody.Data
                    #self.phone_display_contentscreen[content.DisplayMessageBody.Row + content.DisplayMessageBody.Column] = content.DisplayMessageBody.Data
            else:
                for content in data:
                    if content.DisplayMessageBody.ResetScreen == '1':
                        self.phone_display_contentscreen.clear()
                        self.phone_display_foxkeys.clear()
                        self.phone_display_programmablekeys.clear()
                        self.phone_display_contents =""
                        pass
                    # else:
                    #     self.phone_display[content.DisplayMessageBody.positionX+content.DisplayMessageBody.positionY] = content.DisplayMessageBody.Data
                    #     self.phone_display_contents = ' '.join(self.phone_display.viewvalues())
                    #     if self.phone.phoneModel =="Mitel6920" or self.phone.phoneModel == "Mitel6930":
                    #         if content.DisplayMessageBody.positionX =="17" and content.DisplayMessageBody.positionY =="3":
                    #             self.phone_display_banner = content.DisplayMessageBody.Data
                    #         elif content.DisplayMessageBody.positionY =="D2":
                    #             if not self.phone_display_foxkeys.has_key(content.DisplayMessageBody.Data):
                    #                 self.phone_display_foxkeys[content.DisplayMessageBody.Data] = content.DisplayMessageBody.Data
                    #         elif content.DisplayMessageBody.positionX =="20":
                    #             if not self.phone_display_programmablekeys.has_key(content.DisplayMessageBody.Data):
                    #                 self.phone_display_programmablekeys[content.DisplayMessageBody.Data] = content.DisplayMessageBody.Data
                    #         elif self.phone.phoneModel =="Mitel6930" and content.DisplayMessageBody.positionX =="65": # 2nd column of 6930 phones
                    #              if not self.phone_display_programmablekeys.has_key(content.DisplayMessageBody.Data):
                    #                 self.phone_display_programmablekeys[content.DisplayMessageBody.Data] = content.DisplayMessageBody.Data
                    #         elif self.phone.phoneModel =="Mitel6930" and content.DisplayMessageBody.positionY =="EE": # 2nd column of 6930 phones
                    #              if not self.phone_display_programmablekeys.has_key(content.DisplayMessageBody.Data):
                    #                 self.phone_display_foxkeys[content.DisplayMessageBody.Data] = content.DisplayMessageBody.Data
                    #         else:
                    #             if not self.phone_display_contentscreen.has_key(content.DisplayMessageBody.Data):
                    #                 self.phone_display_contentscreen[content.DisplayMessageBody.Data] = content.DisplayMessageBody.Data# +" "+ content.DisplayMessageBody.positionX + "*" + content.DisplayMessageBody.positionY
                    #     elif self.phone.phoneModel == "Mitel6940":
                    #         if content.DisplayMessageBody.positionX =="1D" and content.DisplayMessageBody.positionY =="3":
                    #             self.phone_display_banner = content.DisplayMessageBody.Data
                    #         elif content.DisplayMessageBody.positionY =="A4":
                    #             if not self.phone_display_foxkeys.has_key(content.DisplayMessageBody.Data):
                    #                 self.phone_display_foxkeys[content.DisplayMessageBody.Data] = content.DisplayMessageBody.Data
                    #         elif content.DisplayMessageBody.positionX =="F8" or content.DisplayMessageBody.positionX =="30":
                    #             if not self.phone_display_programmablekeys.has_key(content.DisplayMessageBody.Data):
                    #                 self.phone_display_programmablekeys[content.DisplayMessageBody.Data] = content.DisplayMessageBody.Data
                    #         else:
                    #             if not self.phone_display_contentscreen.has_key(content.DisplayMessageBody.Data):
                    #                 self.phone_display_contentscreen[content.DisplayMessageBody.Data] = content.DisplayMessageBody.Data# +" "+ content.DisplayMessageBody.positionX + "*" + content.DisplayMessageBody.positionY
                    else:
                        self.phone_display[content.DisplayMessageBody.positionX + content.DisplayMessageBody.positionY] = content.DisplayMessageBody.Data
                        self.phone_display_contents = ' '.join(self.phone_display.viewvalues())
                        if self.phone.phoneModel == "Mitel6920" or self.phone.phoneModel == "Mitel6930":
                            if content.DisplayMessageBody.positionX == "17" and content.DisplayMessageBody.positionY == "3":
                                self.phone_display_banner = content.DisplayMessageBody.Data
                            elif content.DisplayMessageBody.positionY == "D2":
                                # if not self.phone_display_foxkeys.has_key(content.DisplayMessageBody.Data):
                                self.phone_display_foxkeys[
                                    content.DisplayMessageBody.positionX + "_" + content.DisplayMessageBody.positionY] = content.DisplayMessageBody.Data
                            elif content.DisplayMessageBody.positionX == "20":
                                # if not self.phone_display_programmablekeys.has_key(content.DisplayMessageBody.Data):
                                self.phone_display_programmablekeys[
                                    content.DisplayMessageBody.positionX + "_" + content.DisplayMessageBody.positionY] = content.DisplayMessageBody.Data
                            elif self.phone.phoneModel == "Mitel6930" and content.DisplayMessageBody.positionX == "65":  # 2nd column of 6930 phones
                                # if not self.phone_display_programmablekeys.has_key(content.DisplayMessageBody.Data):
                                self.phone_display_programmablekeys[
                                    content.DisplayMessageBody.positionX + "_" + content.DisplayMessageBody.positionY] = content.DisplayMessageBody.Data
                            elif self.phone.phoneModel == "Mitel6930" and content.DisplayMessageBody.positionY == "EE":  # 2nd column of 6930 phones
                                # if not self.phone_display_programmablekeys.has_key(content.DisplayMessageBody.Data):
                                self.phone_display_foxkeys[
                                    content.DisplayMessageBody.positionX + "_" + content.DisplayMessageBody.positionY] = content.DisplayMessageBody.Data
                            else:
                                if not self.phone_display_contentscreen.has_key(content.DisplayMessageBody.Data):
                                    self.phone_display_contentscreen[
                                        content.DisplayMessageBody.Data] = content.DisplayMessageBody.Data + " " + content.DisplayMessageBody.positionX + "*" + content.DisplayMessageBody.positionY
                        elif self.phone.phoneModel == "Mitel6940":
                            if content.DisplayMessageBody.positionX == "1D" and content.DisplayMessageBody.positionY == "3":
                                self.phone_display_banner = content.DisplayMessageBody.Data
                            elif content.DisplayMessageBody.positionY == "A4":
                                # if not self.phone_display_foxkeys.has_key(content.DisplayMessageBody.Data):
                                self.phone_display_foxkeys[
                                    content.DisplayMessageBody.positionX + "_" + content.DisplayMessageBody.positionY] = content.DisplayMessageBody.Data
                            elif content.DisplayMessageBody.positionX == "F8" or content.DisplayMessageBody.positionX == "30":
                                # if not self.phone_display_programmablekeys.has_key(content.DisplayMessageBody.Data):
                                self.phone_display_programmablekeys[
                                    content.DisplayMessageBody.positionX + "_" + content.DisplayMessageBody.positionY] = content.DisplayMessageBody.Data
                            else:
                                # if not self.phone_display_contentscreen.has_key(content.DisplayMessageBody.Data):
                                self.phone_display_contentscreen[
                                    content.DisplayMessageBody.positionX + "_" + content.DisplayMessageBody.positionY] = content.DisplayMessageBody.Data + " " + content.DisplayMessageBody.positionX + "*" + content.DisplayMessageBody.positionY


        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception('func "%s" - err: "%s"!' % (fn, err))

    def get_all_display_contents(self):
        """
        Returns all the text from the phone screen
        """
        try:
            logger.info("Getting display data from the phone....")
            self.get_all_screen_content()
            return self.phone_display_contents
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception('func "%s" - err: "%s"!' % (fn, err))
    
    
    def reboot_terminal(self):
        """
        reboot the phone
        Args:
            None

        """
        try:
            logger.info("Rebooting the phone")
            self.phone.rebootPhone()
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception('func "%s" - err: "%s"!' % (fn, err))

    def get_firmware_version(self):
        """
        Firmware version of the phone
        Args:
            Firmware version of the phone

        """
        try:
            return self.phone.FirmwareVersion
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception('func "%s" - err: "%s"!' % (fn, err))

    def WaitTillPhoneComesOnline(self, timeOutInSeconds):
        """
        this function will wait till the phone comes back online
        Args:
            timeOutInSeconds : this time will be added to an inbuilt wait of 20 seconds

        """
        try:
            return self.phone.WaitTillPhoneComesOnline(timeOutInSeconds)
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception('func "%s" - err: "%s"!' % (fn, err))


    def get_library_version(self):
        """
        Library version of ATAP
        Args:
            Library version of ATAP

        """
        try:
            return self.phone.LibraryVersion
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception('func "%s" - err: "%s"!' % (fn, err))

    def clear_sip_traces(self):
        '''
        Clears the sip traces on the phone
        :return: None
        '''
        try:
            self.phone.clearSIPtraces()
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception('func "%s" - err: "%s"!' % (fn, err))

    def get_sip_in_messages(self):
        '''
        sip messages received by the phone
        :return: SIP IN messages from the phone
        '''
        try:
            sip_messages = []
            for message in self.phone.SIPMessageRecieved:
                sip_messages.append(message)
            return sip_messages
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception('func "%s" - err: "%s"!' % (fn, err))

    def get_sip_out_messages(self):
        '''
        sip messages sent by the phone
        :return: SIP OUT messages from the phone
        '''
        try:
            sip_messages = []
            for message in self.phone.SIPMessageSent:
                sip_messages.append(message)
            return sip_messages
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception('func "%s" - err: "%s"!' % (fn, err))

    def verify_sip_private_trunk_reroutingto_in_attend_when_not_responding(self, phone2):
        """

        This method ...
        Args:
            phone2: string

        """
        try:
            self.phone.verifySIPPrivateTrunkReroutingtoInAttendWhenNotResponding(phone2)
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception('func "%s" - err: "%s"!' % (fn, err))

    def phone_console_cmd(self, cmd, options=None):
        """Runs cmd via phone console

        :param cmd:  cmd
        :type cmd: type str
        :return ret_val:  cmd result
        """
        # import rpdb2; rpdb2.start_embedded_debugger('admin1')
        if options is not None and 'su' in options:
            return self.phone_ssh_su_cmd(cmd)

        return self.phone_ssh_cmd(cmd)

    def phone_ssh_cmd(self, cmd):
        """Runs cmd via ssh on phone

        :param cmd: ssh cmd
        :type cmd: type str
        :return ret_val: ssh cmd result
        """
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        try:
            if self.hq_rsa:
                ssh.connect(self.phone_info['ipAddress'], username="admin", key_filename=self.hq_rsa_path)
            else:
                ssh.connect(self.phone_info['ipAddress'], username="root", password=self.phone_info['ssh_password'])
            # if str(self.get_firmware_version()).startswith('5.1'):
            #     ssh.connect(self.phone_info['ipAddress'], username="root", password=self.phone_info['ssh_password'])
            # else:
            #     ssh.connect(self.phone_info['ipAddress'], username="admin", key_filename=self.hq_rsa_path)
        except (paramiko.BadHostKeyException, paramiko.AuthenticationException,paramiko.SSHException):
            ssh.close()
            raise Exception("SSH connection failed!! IP, uname, or rsa may be incorrect")
            return

        logger.info("Running ssh cmd: \"%s\" on phone %s" % (cmd, self.phone_info['ipAddress']))
        stdin, stdout, stderr = ssh.exec_command(cmd, get_pty=True)
        result = stdout.readlines()

        if  ssh:
             ssh.close()
        return result

    def phone_ssh_su_cmd(self, cmd):
        """Runs cmd via ssh as su on phone

        :param cmd: ssh cmd
        :type cmd: type str
        :return ret_val: result
        """
        # logger.info("using rsa %s" % self.hq_rsa_path)
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        if self.hq_rsa:
            ssh.connect(self.phone_info['ipAddress'], username="admin", key_filename=self.hq_rsa_path)
            pswd = 'SkBjcXVlc0NAcnQxZXI='
            cmd = "echo " + base64.b64decode(pswd) + " | su -c \"" + cmd + "\""
            logger.info("Running ssh cmd as su: \"%s\" on phone %s" % (cmd, self.phone_info['ipAddress']))
            stdin, stdout, stderr = ssh.exec_command(cmd)
            result = stdout.readlines()
            logger.info("Cmd result: %s" % (result))
            if not stderr:
                logger.error("Cmd :" + cmd + ", Error: " + str(stderr))
        else:
            ssh.connect(self.phone_info['ipAddress'], username="root", password=self.phone_info['ssh_password'])
            logger.info("Running ssh cmd: \"%s\" on phone %s" % (cmd, self.phone_info['ipAddress']))
            stdin, stdout, stderr = ssh.exec_command(cmd)
            result = stdout.readlines()
            logger.info("Cmd result: %s" % (result))
            if not stderr:
                logger.error("Cmd :" + cmd + ", Error: " + str(stderr))
        # if str(self.get_firmware_version()).startswith('5.2'):
        #     ssh.connect(self.phone_info['ipAddress'], username="root", password=self.phone_info['ssh_password'])
        #     logger.info("Running ssh cmd: \"%s\" on phone %s" % (cmd, self.phone_info['ipAddress']))
        #     stdin, stdout, stderr = ssh.exec_command(cmd)
        #     result = stdout.readlines()
        #     logger.info("Cmd result: %s" % (result))
        #     if not stderr:
        #         logger.error("Cmd :" + cmd +", Error: "+ str(stderr))
        # else:
        #     ssh.connect(self.phone_info['ipAddress'],username="admin",key_filename=self.hq_rsa_path)
        #     pswd = 'SkBjcXVlc0NAcnQxZXI='
        #     cmd = "echo " + base64.b64decode(pswd) + " | su -c \"" + cmd + "\""
        #     logger.info("Running ssh cmd as su: \"%s\" on phone %s" % (cmd, self.phone_info['ipAddress']))
        #     stdin, stdout, stderr = ssh.exec_command(cmd)
        #     result = stdout.readlines()
        #     logger.info("Cmd result: %s" % (result))
        #     if not stderr:
        #         logger.error("Cmd :" + cmd +", Error: "+ str(stderr))
        if  ssh:
             ssh.close()
        return result

    def get_missing_apt_files(self):
        missing_files = []
        files = ['pxaudio_init.sh', \
                'pxcapture_audiohandset.sh', \
                'pxcapture_audiohandsetOldModels.sh',\
                'pxcapture_audioheadset.sh', \
                'pxcapture_audiospeaker.sh', \
                'pxcapture_audiospeakerOldModels.sh',\
                'pxinject_audiohandset.sh', \
                'pxinject_audioheadset.sh', \
                'pxinject_audiospeaker.sh', \
                'pxinject_audiospeakerOldModels.sh',\
                'pxrm_audio.sh', \
                'pxsync_enable.sh', \
                'pxsync_disable.sh', 'pxrm_audioOldModels.sh', 'pxsync_enableOldModels.sh',
                'pxinject_audiohandset_bt.sh', 'pxcapture_audiohandset_bt.sh']

        file_list = self.phone_console_cmd('ls .')
        file_list = ''.join(file_list)

        for file in files:
            if file not in file_list:
                missing_files.append(file)

        return missing_files

    def get_missing_pcm_apt_files(self):
        missing_files = []
        files = ['16k_500.pcm', \
                '16k_1k.pcm', \
                '16k_2k.pcm', \
                '16k_3k.pcm']

        file_list = self.phone_console_cmd('ls /tmp/')
        file_list = ''.join(file_list)

        for file in files:
            if file not in file_list:
                missing_files.append(file)

        return missing_files

    def upload_apt_files_to_phone(self, files_to_upload):

        # check if list is empty
        if not files_to_upload :
            return

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

        if ssh:
            ssh.close()

    def upload_path_confirmation_files(self):
        """scp path confirmation files

        :return ret_val: None
        """
        pcm_to_upload = self.get_missing_pcm_apt_files()
        files_to_upload = self.get_missing_apt_files() + pcm_to_upload
        logger.info("Files to upload on phone %s: %s" % (self.phone_info['ipAddress'], files_to_upload))
        self.upload_apt_files_to_phone(files_to_upload)

        cmd = 'chmod 754 pxaudio_init.sh'
        self.phone_console_cmd(cmd, 'su')

        # Remove non-linux chars from file
        cmd = "sed 's/\\r$//g' pxaudio_init.sh > tmpfile"
        self.phone_console_cmd(cmd)
        cmd = " mv tmpfile pxaudio_init.sh"
        self.phone_console_cmd(cmd, 'su')

    def scp_put(self, file):
        """Runs cmd via ssh on phone

        :param cmd: ssh cmd
        :type cmd: type str
        :return ret_val: ssh cmd result
        """
        logger.info("SCP putting %s " % file)
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(self.phone_info['ipAddress'],username="admin",key_filename=self.hq_rsa_path)

        with SCPClient(ssh.get_transport()) as scp:
           scp.put(file)

        if ssh:
            ssh.close()

    def scp_get(self, file):
        """Runs cmd via ssh on phone

        :param cmd: ssh cmd
        :type cmd: type str
        :return ret_val: ssh cmd result
        """
        logger.info("SCP getting %s " % file)
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(self.phone_info['ipAddress'],username="admin",key_filename=self.hq_rsa_path)

        with SCPClient(ssh.get_transport()) as scp:
           scp.get(file)
        if ssh:
            ssh.close()

    def pxcon_inject_capture_audio(self, other_phone, file):
        try:
            # default_audio_path = 'speaker'
            # audio_path = self.get_audio_path()
            # otherPhone_audio_path = other_phone.get_audio_path()

            self.run_bash_cmd('sh pxaudio_init.sh')
            other_phone.run_bash_cmd('sh pxaudio_init.sh')

            # if default_audio_path == 'speaker':
            self.run_pxcon_script('pxinject_audio_mos_male1.sh')
            other_phone.run_pxcon_script('pxcapture_audio_mos_male1.sh')
            # elif default_audio_path == 'handset':
            # elif default_audio_path == 'speaker':
            # other_phone.run_pxcon_script('pxcapture_audiohandset.sh')

            self.run_pxcon_script('pxsync_enable.sh')
            other_phone.run_pxcon_script('pxsync_enable.sh')

            # Audio plays for at least a second. No need for a sleep
            time.sleep(5)

            self.run_pxcon_script('pxrm_audio.sh')
            other_phone.run_pxcon_script('pxrm_audio.sh')

            other_phone.scp_get('/tmp/mos_male1_capture.pcm')

        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception("func '%s' - err: '%s'!" % (fn, err))


    def get_value(self, arg, delim='='):
        if delim in arg:
            value = arg.split(delim)[1].split()
            return value
        return None

    def find_key_value(self, arg, key, delim='='):
        for line in arg:
            if key in line:
                value = line.split(delim)[1].split()
                if isinstance(value, list):
                    return value[0]
                return value
        return None

    def verify_two_way_packets(self):
        """

        :param cmd: ssh cmd
        :type cmd: type str
        :return ret_val: result
        """
        cmd = 'cat /proc/ept/rtpstats'

        result = self.run_bash_cmd(cmd)
        ingress = self.find_key_value(result, 'ingressRtpPkt')
        egress = self.find_key_value(result, 'egressRtpPkt')
        time.sleep(2)
        result = self.run_bash_cmd(cmd)
        ingresss = self.find_key_value(result, 'ingressRtpPkt')
        egresss = self.find_key_value(result, 'egressRtpPkt')

        if int(ingresss) > int(ingress) and int(egresss) > int(egress):
            return

        pckt_list = list(ingesss,ingress, egress, egresss)
        raise Exception("verify_two_way_packets fail! %s" % pckt_list)

    def verify_hold_state_packets(self):
        """
        :param cmd: ssh cmd
        :type cmd: type str
        :return ret_val: result
        """
        cmd = 'cat /proc/ept/rtpstats'
        result = self.run_bash_cmd(cmd)

        # Result is empty when phone is on hold
        if not result:
            return

        raise Exception("verify_hold_state_packets fail! %s" % result)

    def check_audio_is_on_hold_NotUSED(self, other_phone, moh_enabled):
       # if moh_enabled:
            #silence_energy_threshold = 8.0e-10
        #else:
            #silence_energy_threshold = 3.0e-11

        if self.verify_hold_state_packets():
            print(("TRUE"))

        self.update_devnull_permissions()
        self.upload_path_confirmation_files()

        other_phone.update_devnull_permissions()
        other_phone.upload_path_confirmation_files()

        filename, self_audio_device = self.run_pxcon_one_way_audio(other_phone)
        energy = self.estimate_energy(filename)

        if moh_enabled:
            if energy > 3.0e-11 and energy < 8.0e-10:
                return
            raise Exception("Energy of %s should be between threshold %s and %s" % (energy, 3.0e-11, 8.0e-10))
        else:
            if energy < 3.0e-11:
                return
            raise Exception("Energy of %s should be less than threshold %s" % (energy, 3.0e-11))

        #if energy > silence_energy_threshold:
        #    raise Exception("Energy of %s should be less than threshold %s" % (energy, silence_energy_threshold))

    def check_music_on_hold(self, expectedFqOutput):
        '''
        :param expectedFqOutput:
        :return:
        '''


        # self.update_devnull_permissions()
        # self.upload_path_confirmation_files()
        # self_audio_device = self.get_active_audio_device()
        # self.run_bash_cmd('sh pxaudio_init.sh')
        # self.enableKernalsIf6910()
        # if self_audio_device == 'speaker':
        #     self.run_pxcon_script('pxcapture_audiospeaker.sh')
        # elif self_audio_device == 'handset':
        #     self.run_pxcon_script('pxcapture_audiohandset.sh')
        # elif self_audio_device == 'headset':
        #     self.run_pxcon_script('pxcapture_audioheadset.sh')
        # else:
        #     raise Exception("check_one_way_audio audio path fail")
        # self.run_pxcon_script('pxsync_enable.sh')
        # self.run_pxcon_script('pxrm_audio.sh')
        # # move pcm from tmp to /home/admin/
        # filename = self_audio_device + "_capture.wav"
        # mv_cmd = 'mv /tmp/' + filename + ' ' + filename
        # self.run_bash_cmd(mv_cmd)
        #
        # self.get_file_from_phone(self, filename)
        # self.remove_file_on_phone(self, filename)
        # self.estimate_frequency_moh(filename,self_audio_device)
        # # energy = self.estimate_energy(filename)

        self.check_prerequisites()
        self.enable_pxcon_modules()
        time.sleep(1)
        self.capture_audio()
        time.sleep(2)
        self.sync_enable()
        time.sleep(2)
        self.disable_audio_modules()
        # Download captured file
        self_audio_device = self.get_active_audio_device()
        filename = self_audio_device + "_capture.pcm"
        mv_cmd = 'mv /tmp/' + filename + ' ' + filename
        self.run_bash_cmd(mv_cmd)
        self.get_file_from_phone(filename)
        self.remove_file_on_phone(filename)
        freqOutput = self.estimate_frequency_moh(filename, self_audio_device)
        if freqOutput <= expectedFqOutput+100 and freqOutput >= expectedFqOutput-100:
            return True
        else:
            print("captured frequency is "+ str(freqOutput))
            logger.error('check_music_on_hold: expected frequency '+ str(expectedFqOutput)+', actual is '+ str(freqOutput))
            return False

    def verify_codec(self):
        """

        :param cmd: ssh cmd
        :type cmd: type str
        :return ret_val: result
        """
        supported_codecs = ['ILBC30']
        cmd = 'cat /proc/ept/activeAudioCodec'
        result = self.run_bash_cmd(cmd)

        for i,item in enumerate(result):
            if 'stream 0' in item:
                if self.get_value(result[i+1]) in supported_codecs:
                    return
        raise Exception("Codec verification fail! %s" % result)


    def check_dtmf(self):
        try:
            # self_audio_device = 'speaker'
            # audio_path = self.get_audio_path()
            # other_audio_device = other_phone.get_audio_path()

            self.run_bash_cmd('sh pxaudio_init.sh')

            # if self_audio_device == 'speaker':
            # self.run_pxcon_script('pxcapture_audiospeaker.sh')
            self.run_pxcon_script('pxcapture_audiohandset.sh')

            self.run_pxcon_script('pxsync_enable.sh')

        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception("func '%s' - err: '%s'!" % (fn, err))

    def check_pesq_mos_score(self, other_phone, voice):
        """
        Checks MOS score via PESQ algorithm
        """
        voice_files = ['male1.pcm', 'male2.pcm', 'female1.pcm', 'female2.pcm']
        exe = 'pesq.exe'
        mos_score = ''

        if voice == '':
            secure_random = random.SystemRandom()
            file = secure_random.choice(voice_files)
        else:
            file = voice

        self.pxcon_inject_capture_audio(other_phone, file)

        reference = os.path.join(self.audio_path,file)
        exe_path = os.path.join(self.audio_path,exe)
        logger.info("Using voice file %s" % reference)

        degraded = reference
        output = subprocess.Popen([exe_path, '+16000', reference, degraded], stdout=subprocess.PIPE)

        out, err = output.communicate()
        out = out.splitlines()
        for line in out:
            if 'MOS-LQO' in line:
                 mos_score = line.split('=')
                 logger.info(mos_score)

        if mos_score == '':
            raise Exception('MOS score is not resolved. pesq output %s' % out)

    def update_devnull_permissions(self):
        """Runs cmd via ssh as su on phone

        :param cmd: ssh cmd
        :type cmd: type str
        :return ret_val: result
        """
        cmd = 'chmod a+rw /dev/null'

        self.run_bash_cmd(cmd)

    def run_pxcon_script(self, cmd):
        """Runs cmd via ssh as su on phone

        :param cmd: ssh cmd
        :type cmd: type str
        :return ret_val: result
        """
        cmd = 'pxcon ' + cmd

        self.phone_console_cmd(cmd, 'su')

    def run_bash_cmd(self, cmd):
        """Runs cmd via ssh as su on phone

        :param cmd: ssh cmd
        :type cmd: type str
        :return ret_val: result
        """

        self.phone_console_cmd(cmd, 'su')


#
# AUDIO
#


    def freq_from_fft(self, sig, fs):
        """
        Estimate frequency from peak of FFT
        """
        # Compute Fourier transform of windowed signal
        try:
            windowed = sig * blackmanharris(len(sig))
            f = rfft(windowed)

            # Find the peak and interpolate to get a more accurate peak
            i = argmax(abs(f))  # Just use this for less-accurate, naive version
            if i ==0:
                return 0
            true_i = parabolic.parabolic(log(abs(f)), i)[0]

            # Convert to equivalent frequency
            return fs * true_i / len(windowed)
        except:
            logger.info('freq_from_fft :' + str(sys.exc_info()[0]))
            return 0

    def freq_from_crossings(self, sig, fs):
        """
        Estimate frequency by counting zero crossings
        """
        # Find all indices right before a rising-edge zero crossing
        indices = find((sig[1:] >= 0) & (sig[:-1] < 0))

        # Naive (Measures 1000.185 Hz for 1000 Hz, for instance)
        # crossings = indices

        # More accurate, using linear interpolation to find intersample
        # zero-crossings (Measures 1000.000129 Hz for 1000 Hz, for instance)
        crossings = [i - sig[i] / (sig[i+1] - sig[i]) for i in indices]

        # Some other interpolation based on neighboring points might be better.
        # Spline, cubic, whatever

        return fs / mean(diff(crossings))


    def freq_from_autocorr(self, sig, fs):
        """
        Estimate frequency using autocorrelation
        """
        # Calculate autocorrelation (same thing as convolution, but with
        # one input reversed in time), and throw away the negative lags
        corr = fftconvolve(sig, sig[::-1], mode='full')
        corr = corr[len(corr)//2:]

        # Find the first low point
        d = diff(corr)
        start = find(d > 0)[0]

        # Find the next peak after the low point (other than 0 lag).  This bit is
        # not reliable for long signals, due to the desired peak occurring between
        # samples, and other peaks appearing higher.
        # Should use a weighting function to de-emphasize the peaks at longer lags.
        peak = argmax(corr[start:]) + start
        px, py = parabolic.parabolic(corr, peak)

        return fs / px

    def butter_highpass(self, cutoff, fs, order=5):
        nyq = 0.5 * fs
        normal_cutoff = cutoff / nyq
        b, a = butter(order, normal_cutoff, btype='high', analog=False)
        return b, a

    # Shankara Narayanan. M 21-06-2019
    def butter_lowpass(self, cutoff, fs, order=5):
        nyq = 0.5 * fs
        normal_cutoff = cutoff / nyq
        b, a = butter(order, normal_cutoff, btype='lowpass', analog=False)
        return b, a

    def butter_lowpass_filter(self, data, cutoff, fs, order=5):
        b, a = self.butter_lowpass(cutoff, fs, order=order)
        y = filtfilt(b, a, data)
        return y

    def butter_highpass_filter(self, data, cutoff, fs, order=5):
        b, a = self.butter_highpass(cutoff, fs, order=order)
        y = filtfilt(b, a, data)
        return y

    def estimate_energy(self, raw_audio_file):
        try:
            cutoff = 0
            order = 2
            fs = 16000
            cutoff = 250

            logger.info('Reading file "%s"\n' % raw_audio_file)
            raw_audio, fs = sf.read(raw_audio_file, format='RAW', samplerate=fs, channels=1, subtype='PCM_16')
            raw_audio_filt = self.butter_highpass_filter(raw_audio, cutoff, fs, order)

            f, p = signal.periodogram(raw_audio_filt, fs)
            signal_energy = numpy.mean(p)
            logger.info("Energy: %s" % signal_energy)
            energy =0
            for i in range(0, len(raw_audio_filt)):
                sampleVal = (raw_audio_filt[i] - 128) * 256.0
                energy += sampleVal*sampleVal
            logger.info(energy)

            return signal_energy

        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception("func '%s' - err: '%s'!" % (fn, err))

    def estimate_frequency(self, file, audiopath):
        try:
            cutoff = 0
            order = 2
            fs = 16000

            audiopath = audiopath.lower()
            if audiopath == 'handset':
                cutoff = 1000
            elif audiopath == 'headset':
                cutoff = 250
            elif audiopath == 'speaker':
                cutoff = 2500
            else:
                logger.info("audiopath %s does not exist" % audiopath)
                raise Exception("Audio path confirmation FAILED")

            logger.info('Reading file "%s"\n' % file)
            raw_audio, fs = sf.read(file, format='RAW', samplerate=fs, channels=1, subtype='PCM_16')
            raw_audio_filt = self.butter_highpass_filter(raw_audio, cutoff, fs, order)

            # Voice path improvements! Shankara Narayanan. M
            # raw_audio_filt_1 = raw_audio_filt
            # raw_audio_filt_LOW = self.butter_lowpass_filter(raw_audio_filt_1, 3500, fs, order)
            # logger.info('Calculating frequency from FFT: LOWPASS Added')
            # start_time = time.time()
            # freq3 = self.freq_from_fft(raw_audio_filt_LOW, fs)
            # logger.info('%f Hz' % freq3)
            # logger.info('Time elapsed: %.3f s\n' % (time.time() - start_time))
            # freq = freq3




            #
            # Leaving two freq estimation methods for testing purposes
            #

            # logger.info('Calculating frequency from zero crossings:')
            # start_time = time.time()
            # freq = self.freq_from_crossings(raw_audio_filt, fs)
            # logger.info('Time elapsed: %.3f s\n' % (time.time() - start_time))
            # logger.info('%f Hz' % freq)

            # logger.info('Calculating frequency from autocorrelation:')
            # start_time = time.time()
            # freq2 = self.freq_from_autocorr(raw_audio_filt, fs)
            # logger.info('%f Hz' % freq2)
            # logger.info('Time elapsed: %.3f s\n' % (time.time() - start_time))

            logger.info('Calculating frequency from FFT:')
            start_time = time.time()
            freq3 = self.freq_from_fft(raw_audio_filt, fs)
            logger.info('%f Hz' % freq3)
            logger.info('Time elapsed: %.3f s\n' % (time.time() - start_time))
            freq = freq3

            if audiopath == 'handset':
                if int(freq) >= 1950 and int(freq) <= 2050:
                    logger.info("HANDSET PASS")
                else:
                    logger.info("Handset Freq Check FAILED, Expected frequency between 1950 and 2050")
                    raise Exception("Audio path confirmation FAILED")
            elif audiopath == 'headset' and int(freq) == 500:
                # TODO  improve robustness of headset
                if int(freq) >= 450 and int(freq) <= 550:
                    logger.info("HEADSET PASS")
                else:
                    logger.info("Headset Freq Check FAILED, Expected frequency between 450 and 550")
                    raise Exception("Audio path confirmation FAILED")
            elif audiopath == 'speaker':
                if int(freq) >= 2900 and int(freq) <= 3000:
                    logger.info("SPEAKER PASS")
                elif int(freq) > 3000:
                    logger.warn("SPEAKER PASS with High frequency(" + str(freq) +")")
                else:
                    logger.info("Speaker Freq Check FAILED, Expected frequency between 2900 and 3000")
                    raise Exception("Audio path confirmation FAILED")

        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception("func '%s' - err: '%s'!" % (fn, err))


    def estimate_frequency_moh(self, file, audiopath):
        try:
            cutoff = 0
            order = 2
            fs = 16000
            audiopath = audiopath.lower()
            raw_audio, fs = sf.read(file, format='RAW', samplerate=fs, channels=1, subtype='PCM_16')
            logger.info('Calculating frequency from FFT:')
            start_time = time.time()
            freq3 = self.freq_from_fft(raw_audio, fs)
            logger.info('%f Hz' % freq3)
            logger.info('Time elapsed: %.3f s\n' % (time.time() - start_time))
            return freq3
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception("func '%s' - err: '%s'!" % (fn, err))

    def verify_no_audiopath(self, file, audiopath):
        try:
            cutoff = 0
            order = 2
            fs = 16000

            audiopath = audiopath.lower()
            if audiopath == 'handset':
                cutoff = 1000
            elif audiopath == 'headset':
                cutoff = 250
            elif audiopath == 'speaker':
                cutoff = 2500
            else:
                logger.info("Audiopath is unknown / not listed, " % audiopath)
                raise Exception("Audio path confirmation FAILED")

            logger.info('Reading file "%s"\n' % file)
            raw_audio, fs = sf.read(file, format='RAW', samplerate=fs, channels=1, subtype='PCM_16')
            raw_audio_filt = self.butter_highpass_filter(raw_audio, cutoff, fs, order)
            logger.info('Calculating frequency from FFT:')
            start_time = time.time()
            freq3 = self.freq_from_fft(raw_audio_filt, fs)
            logger.info('%f Hz' % freq3)
            logger.info('Time elapsed: %.3f s\n' % (time.time() - start_time))
            #return freq3
            freq = freq3
            if audiopath == 'handset':
                 if int(freq) == 2000:
                     raise Exception("Audio path exist" +str(freq))
                 else:
                    logger.info("Audio path doesn't exist")
            elif audiopath == 'headset' and int(freq) == 500:
                 # TODO  improve robustness of headset
                 if int(freq) >= 450 and int(freq) <= 550:
                     raise Exception("Audio path exist"+str(freq))
                 else:
                     logger.info("Audio path doesn't exist")
            elif audiopath == 'speaker':
                 if int(freq) == 3000:
                     raise Exception("Audio path exist"+str(freq))
                 else:
                     logger.info("Audio path doesn't exist")

        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception("func '%s' - err: '%s'!" % (fn, err))

    def update_apt_filepath(self, file):
        # Might need path logic in future
        return file

    def enableKernalsIf6910(self):
        if self.phone.phoneModel in ["Mitel6910", "Mitel6865i"]:
                self.run_bash_cmd('/sbin/modprobe csx_gist_drv')
                self.run_bash_cmd('/sbin/modprobe csx_gist_drv.ko')
                self.run_bash_cmd('mknod /dev/csx_gist_drv c 239 0')
        return

    def check_prerequisites(self):
        self.update_devnull_permissions()
        self.upload_path_confirmation_files()

    def enable_pxcon_modules(self):
        self.run_bash_cmd('sh pxaudio_init.sh')
        self.enableKernalsIf6910()

    def capture_audio(self):
        self_audio_device = self.get_active_audio_device()
        if self.phone.phoneModel== "Mitel6910" or self.phone.phoneModel== "Mitel6865i":
            if self_audio_device == 'speaker':
                self.run_pxcon_script('pxcapture_audiospeakerOldModels.sh')
            elif self_audio_device == 'handset':
                self.run_pxcon_script('pxcapture_audiohandsetOldModels.sh')
            elif self_audio_device == 'headset':
                self.run_pxcon_script('pxcapture_audioheadset.sh')
            else:
                raise Exception("capture_audio: unidentified audio path" + self_audio_device)
        else:
            if self_audio_device == 'speaker':
                self.run_pxcon_script('pxcapture_audiospeaker.sh')
            elif self_audio_device == 'handset':
                self.run_pxcon_script('pxcapture_audiohandset.sh')
            elif self_audio_device == 'headset':
                self.run_pxcon_script('pxcapture_audioheadset.sh')
            else:
                raise Exception("capture_audio: unidentified audio path" + self_audio_device)

    def inject_audio(self):
        self_audio_device = self.get_active_audio_device()
        if self_audio_device == 'speaker':
            if self.phone.phoneModel== "Mitel6910" or self.phone.phoneModel== "Mitel6865i":
                self.run_pxcon_script('pxinject_audiospeakerOldModels.sh')
            else:
                self.run_pxcon_script('pxinject_audiospeaker.sh')
        elif self_audio_device == 'handset':
            self.run_pxcon_script('pxinject_audiohandset.sh')
        elif self_audio_device == 'headset':
            self.run_pxcon_script('pxinject_audioheadset.sh')
        else:
            raise Exception("check_one_way_audio audio path fail")

    def sync_enable(self):
        self.run_pxcon_script('pxsync_enable.sh')

    def disable_audio_modules(self):
        self.run_pxcon_script('pxrm_audio.sh')

    def verify_frequency_from_captured_file(self):
        # move pcm from tmp to /home/admin/
        self_audio_device = self.get_active_audio_device()
        filename = self_audio_device + "_capture.pcm"
        mv_cmd = 'mv /tmp/' + filename + ' ' + filename
        self.run_bash_cmd(mv_cmd)
        self.get_file_from_phone(filename)
        self.remove_file_on_phone(filename)
        self.estimate_frequency(filename, self_audio_device)

    def checkAndMute(self):
        if self.phone.isOnMute != "1":
            self.press_key("Mute")
            self.alreadyOnMute = False
        else:
            self.alreadyOnMute = True

    def run_pxcon_one_way_audio(self, other_phone):
        try:
            self_audio_device = None #self.get_active_audio_device()
            other_audio_device = None #other_phone.get_active_audio_device()

            if type(other_phone).__name__ == 'Phone_69xx' or type(other_phone).__name__ == 'Phone_68xx':
                self_audio_device = self.get_active_audio_device()
                other_audio_device = other_phone.get_active_audio_device()
            elif type(other_phone).__name__ == 'IP4xxInterface':
                self_audio_device = self.get_active_audio_device()
                cap_activeAudioDevice = int(other_phone.getdm_active_audio_path(other_phone.ip4xx_user))
                other_audio_device = halAudioMap[cap_activeAudioDevice]

            self.run_bash_cmd('sh pxaudio_init.sh')
            self.enableKernalsIf6910()

            other_phone.run_bash_cmd('sh pxaudio_init.sh')
            other_phone.enableKernalsIf6910()

            other_phone.checkAndMute()
            # Capture Audio
            if other_phone.phone.phoneModel== "Mitel6910" or other_phone.phone.phoneModel== "Mitel6865i":
                if other_audio_device == 'speaker':
                    other_phone.run_pxcon_script('pxcapture_audiospeakerOldModels.sh')
                elif other_audio_device == 'handset':
                    other_phone.run_pxcon_script('pxcapture_audiohandsetOldModels.sh')
                elif other_audio_device == 'headset':
                    other_phone.run_pxcon_script('pxcapture_audioheadset.sh')
                else:
                    raise Exception("check_one_way_audio audio path fail")
            elif other_phone.phone.phoneModel in ["Mitel6940"]:
                if other_audio_device == 'speaker':
                    other_phone.run_pxcon_script('pxcapture_audiospeaker.sh')
                elif other_audio_device == 'handset':
                    other_phone.run_pxcon_script('pxcapture_audiohandset_bt.sh')
                elif other_audio_device == 'headset':
                    other_phone.run_pxcon_script('pxcapture_audioheadset.sh')
                else:
                    raise Exception("check_one_way_audio audio path fail")
            else:
                if other_audio_device == 'speaker':
                    other_phone.run_pxcon_script('pxcapture_audiospeaker.sh')
                elif other_audio_device == 'handset':
                    other_phone.run_pxcon_script('pxcapture_audiohandset.sh')
                elif other_audio_device == 'headset':
                    other_phone.run_pxcon_script('pxcapture_audioheadset.sh')
                else:
                    raise Exception("check_one_way_audio audio path fail")

            # Inject Audio
            if self_audio_device == 'speaker':
                if self.phone.phoneModel== "Mitel6910" or self.phone.phoneModel== "Mitel6865i":
                    self.run_pxcon_script('pxinject_audiospeakerOldModels.sh')
                else:
                    self.run_pxcon_script('pxinject_audiospeaker.sh')
            elif self_audio_device == 'handset':
                if self.phone.phoneModel in ["Mitel6940"]:
                    self.run_pxcon_script('pxinject_audiohandset_bt.sh')
                else:
                    self.run_pxcon_script('pxinject_audiohandset.sh')
            elif self_audio_device == 'headset':
                self.run_pxcon_script('pxinject_audioheadset.sh')
            else:
                raise Exception("check_one_way_audio audio path fail")

            if self.phone.phoneModel== "Mitel6865i":
                self.run_pxcon_script('pxsync_enableOldModels.sh')
            else:
                self.run_pxcon_script('pxsync_enable.sh')
                
            if other_phone.phone.phoneModel== "Mitel6865i":
                other_phone.run_pxcon_script('pxsync_enableOldModels.sh')
            else:
                other_phone.run_pxcon_script('pxsync_enable.sh')
            # Audio plays for at least a second. No need for a sleep
            # time.sleep(.5)
            if self.phone.phoneModel== "Mitel6865i":
                self.run_pxcon_script('pxrm_audioOldModels.sh')
            else:
                self.run_pxcon_script('pxrm_audio.sh')
                
            if other_phone.phone.phoneModel== "Mitel6865i":
                other_phone.run_pxcon_script('pxrm_audioOldModels.sh')
            else:
                other_phone.run_pxcon_script('pxrm_audio.sh')

            if not other_phone.alreadyOnMute:
                other_phone.press_key("Mute")
            # move pcm from tmp to /home/admin/
            filename = other_audio_device + "_capture.pcm"
            mv_cmd = 'mv /tmp/' + filename + ' ' + filename
            other_phone.run_bash_cmd(mv_cmd)

            other_phone.get_file_from_phone(filename)
            other_phone.remove_file_on_phone(filename)

            return (self.update_apt_filepath(filename), self_audio_device)

        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception("func '%s' - err: '%s'!" % (fn, err))

    def check_two_way_audio(self, other_phone):
        try:
            self.update_devnull_permissions()
            self.upload_path_confirmation_files()

            other_phone.update_devnull_permissions()
            other_phone.upload_path_confirmation_files()

            self.press_key('DecreaseVolume',2)
            other_phone.press_key('DecreaseVolume',2)

            filename, self_audio_device = self.run_pxcon_one_way_audio(other_phone)
            self.estimate_frequency(filename, self_audio_device)

            filename, self_audio_device = other_phone.run_pxcon_one_way_audio(self)
            self.estimate_frequency(filename, self_audio_device)
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            logger.info("LINE states of "+self.phone.extensionNumber+": " + str(self.get_line_buffer()))
            logger.info("LINE states of "+other_phone.phone.extensionNumber+": " + str(other_phone.get_line_buffer()))
            self.capture_screenshot()
            other_phone.capture_screenshot()
            raise Exception("func '%s' - err: '%s'!" % (fn, err))

    def check_oneway_conference_audio(self, phones):
        try:
            self.check_prerequisites()
            self.press_key('DecreaseVolume',2)
            self.enable_pxcon_modules()

            for phone in phones:
                phone.check_prerequisites()
                phone.press_key('DecreaseVolume',2)
                phone.enable_pxcon_modules()
                # phone.press_key('Mute')
                phone.checkAndMute()
                phone.capture_audio()

            #Play from phone 1
            self.inject_audio()

            for phone in phones:
                phone.sync_enable()

            self.sync_enable()
            for phone in phones:
                phone.disable_audio_modules()

            self.disable_audio_modules()

            for phone in phones:
                if not phone.alreadyOnMute:
                    phone.press_key('Mute')
                logger.info('Verify voice path between '+ self.phone.extensionNumber + " and "+ phone.phone.extensionNumber)
                phone.verify_frequency_from_captured_file()

        except Exception as err:
            fn = sys._getframe().f_code.co_nametmpfile
            logger.info("LINE states of "+self.phone.extensionNumber+": " + str(self.get_line_buffer()))
            self.capture_screenshot()
            for phone in phones:
                logger.info("LINE states of "+phone.phone.extensionNumber+": " + str(phone.get_line_buffer()))
                phone.capture_screenshot()
            raise Exception("func '%s' - err: '%s'!" % (fn, err))

    # For one way audio check
    def check_one_way_audio(self, other_phone):
        try:
            self.update_devnull_permissions()
            self.upload_path_confirmation_files()
			
            other_phone.update_devnull_permissions()
            other_phone.upload_path_confirmation_files()

            self.press_key('DecreaseVolume',2)
            other_phone.press_key('DecreaseVolume',2)

            filename, self_audio_device = self.run_pxcon_one_way_audio(other_phone)
            self.estimate_frequency(filename, self_audio_device)
        
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception("func '%s' - err: '%s'!" % (fn, err))

    def check_no_audio(self, other_phone):
        try:
            self.update_devnull_permissions()
            self.upload_path_confirmation_files()

            other_phone.update_devnull_permissions()
            other_phone.upload_path_confirmation_files()

            self.press_key('DecreaseVolume',2)
            other_phone.press_key('DecreaseVolume',2)

            filename, self_audio_device = self.run_pxcon_one_way_audio(other_phone)
            self.verify_no_audiopath(filename, self_audio_device)

        except Exception as err:
            fn = sys._getframe().f_code.co_name
            logger.info("LINE states of "+self.phone.extensionNumber+": " + str(self.get_line_buffer()))
            logger.info("LINE states of "+other_phone.phone.extensionNumber+": " + str(other_phone.get_line_buffer()))
            raise Exception("func '%s' - err: '%s'!" % (fn, err))

    # def get_file_from_phone(self, phone, get_path):
    #     try:
    #         phone.scp_get(get_path)
    #     except Exception as err:
    #         fn = sys._getframe().f_code.co_name
    #         raise Exception("func '%s' - err: '%s'!" % (fn, err))

    def get_file_from_phone(self, get_path):
        try:
            self.scp_get(get_path)
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception("func '%s' - err: '%s'!" % (fn, err))

    # def remove_file_on_phone(self, phone, rm_path):
    #     try:
    #         phone.phone_console_cmd('rm ' + rm_path, 'su')
    #     except Exception as err:
    #         fn = sys._getframe().f_code.co_name
    #         raise Exception("func '%s' - err: '%s'!" % (fn, err))

    def remove_file_on_phone(self, rm_path):
        try:
            self.phone_console_cmd('rm ' + rm_path, 'su')
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception("func '%s' - err: '%s'!" % (fn, err))

    def capture_screenshot(self, path=None, username="admin", password="1234"):
        try:         
            if self.phone_info["phoneModel"] in ["Mitel6940", "Mitel6930", "Mitel6920"]:
                fname = datetime.datetime.now().strftime("%d-%m-%Y-%H-%M-%S")
                if not path:
                    file_path = os.path.join(os.getcwd(), fname + ".png")
                else:
                    file_path = os.path.join(path, fname + ".png")
                r = self.generate_screenshot(path, username, password)
                if r.status_code == 200:
                    with open(file_path, 'wb') as out_file:
                        shutil.copyfileobj(r.raw, out_file)
                        logger.info("Saving screen shot at %s"%(file_path))
                elif r.status_code == 401:
                    r = self.generate_screenshot(path, username, "22222")
                    with open(file_path, 'wb') as out_file:
                        shutil.copyfileobj(r.raw, out_file)
                        logger.info("Saving screen shot at %s"%(file_path))
                else:
                    logger.error("Error in taking phone screen shot")
                r.connection.close()
            else:
                logger.info("Phone model %s does not support screen shot" % (self.phone_info["phoneModel"]))
        except Exception as e:
            logger.error(str(e.message))
            
    def generate_screenshot(self, path=None, username="admin", password="1234"):        
        try:            
            authorization = base64.b64encode(b":".join([('%s'%username).encode(), ('%s'%password).encode()])).decode()
            admin_header = {'Cookie' : 'Authorization=Basic %s' % authorization}
            ip = self.phone_info['ipAddress']
            url = {"auth": "http://%s/" % ip, "ss": "http://%s/ScreenShotFile.png" % ip}
            r = requests.get(url["ss"], stream=True, headers=admin_header)
            return r           
        except Exception as e:
            logger.error(str(e.message))

                           
    def check_pesq_mos_score(self, other_phone, voice=''):
        try:
            self.phone_obj.check_pesq_mos_score(other_phone, voice)
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception("func '%s' - err: '%s'!" % (fn, err))
            
    def get_all_brightness_buffer(self):
        try:
            return self.phone.getAllBrightness()
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception("func '%s' - err: '%s'!" % (fn, err))

    def get_phone_brightness(self):
        try:
            b_buffer = self.get_all_brightness_buffer()
            if b_buffer.Count:
                return b_buffer[0]["BNLevel"]
            return "No change in brightness"
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception("func '%s' - err: '%s'!" % (fn, err))
            
    def is_background_image_set(self):
        try:
            i_buffer = self.get_icon_buffer()
            if len(i_buffer):
                if i_buffer[0]["IsBGImageSet"] == "0":
                    return False
                else:
                    return True
            return "No icons on the screen"
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception("func '%s' - err: '%s'!" % (fn, err))
            
    def get_all_tone_buffer(self):
        try:
            return self.phone.getRingtoneBuffer()
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception("func '%s' - err: '%s'!" % (fn, err))
            
    def get_tone_at_phone(self):
        try:
            t_buffer = self.get_all_tone_buffer()
            if t_buffer.Count:
                if t_buffer[0]["SeqNumber"] in self.packet_id:
                    return -1
                else:
                    self.packet_id.add(t_buffer[0]["SeqNumber"])
                    return t_buffer[0]["ToneId"]
            return "No tone detected at phone."
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception("func '%s' - err: '%s'!" % (fn, err))

    def get_highlighted_text_buffer(self):
        try:
            return self.phone.getHighlightedTextBuffer()
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception("func '%s' - err: '%s'!" % (fn, err))

    def get_highlighted_text_properties(self):
        try:
            # waiting so that messages in the background can be processed
            time.sleep(2.5) 
            #text_seen = []
            ht_buffer = self.get_highlighted_text_buffer()
            if ht_buffer.Count:
                buffer_to_return = {}
                for _ht_buffer in ht_buffer:
                    result = {}
                    result["Index"] = _ht_buffer["Index"]
                    result["UIType"] = _ht_buffer["UIType"]
                    result["Value"] = _ht_buffer["Value"]
                    result["IsHighlighted"] = _ht_buffer["IsHighlighted"]
                    result["ScrnType"] = _ht_buffer["ScrnType"]
                    result["IsReadOnly"] = _ht_buffer["IsReadOnly"]
                    result["InputType"] = _ht_buffer["InputType"]
                    result["ItemText"] = _ht_buffer["ItemText"].replace("\x00","")
                    # updating the duplicate entries
                    buffer_to_return[result["ItemText"]] = result
                    #buffer_to_return.append(result)
                return buffer_to_return.values()
            return "No highlighted text on screen"
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception("func '%s' - err: '%s'!" % (fn, err))

    def get_menu_text_buffer(self):
        try:
            return self.phone.getTextMenuBuffer()
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception("func '%s' - err: '%s'!" % (fn, err))

    def get_menu_text_properties(self):
        try:
            tm_buffer = self.get_menu_text_buffer()
            if tm_buffer.Count:
                _tm_buffer = tm_buffer[0]
                result = {}
                result["screenType"] = _tm_buffer["screenType"]
                result["Beep"] = _tm_buffer["Beep"]
                result["TimeOut"] = _tm_buffer["TimeOut"]
                result["WrapList"] = _tm_buffer["WrapList"]
                result["LockIn"] = _tm_buffer["LockIn"]
                result["allowDTMF"] = _tm_buffer["allowDTMF"]
                result["alloXfer"] = _tm_buffer["alloXfer"]
                result["allowConf"] = _tm_buffer["allowConf"]
                result["allowDrop"] = _tm_buffer["allowDrop"]
                result["destroyOnExit"] = _tm_buffer["destroyOnExit"]
                result["allowAnswer"] = _tm_buffer["allowAnswer"]
                result["wrapTitle"] = _tm_buffer["wrapTitle"]
                return result
            return "No menu text found on phone"
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception("func '%s' - err: '%s'!" % (fn, err))

    def get_formatted_text_buffer(self):
        try:
            return self.phone.getFormattedTextBuffer()
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception("func '%s' - err: '%s'!" % (fn, err))

    def get_formatted_text_properties(self):
        try:
            ft_buffer = self.get_formatted_text_buffer()
            #print(ft_buffer.Count)
            if ft_buffer.Count: 
                formatted_text_properties = []
                for index in range(ft_buffer.Count):
                    _ft_buffer = ft_buffer[index]
                    result = {}
                    result["screenType"] = _ft_buffer["screenType"]
                    result["TextType"] = _ft_buffer["TextType"]
                    result["LineNumber"] = _ft_buffer["LineNumber"]
                    result["LineSize"] = _ft_buffer["LineSize"]
                    result["Align"] = _ft_buffer["Align"]
                    result["blink"] = _ft_buffer["blink"]
                    result["color"] = _ft_buffer["color"]
                    result["wrap"] = _ft_buffer["wrap"]
                    result["Scrollheight"] = _ft_buffer["Scrollheight"]
                    formatted_text_properties.append(result)
                return formatted_text_properties
            return "No formatted text found on the phone"
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception("func '%s' - err: '%s'!" % (fn, err))
            
    def get_screensaver_buffer(self):
        try:
            return self.phone.getAllScreenSaver()
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception("func '%s' - err: '%s'!" % (fn, err))

    def get_screensaver_properties(self):
        try:
            ss_buffer = self.get_screensaver_buffer()
            if ss_buffer.Count:
                _ss_buffer = ss_buffer[0]
                result = {}
                result["Module"] = _ss_buffer["Module"]
                result["ScreenType"] = _ss_buffer["ScreenType"]
                result["ImgIndex"] = _ss_buffer["ImgIndex"]
                result["IsMissedCallImgVisible"] = _ss_buffer["IsMissedCallImgVisible"]
                result["MissedCallCount"] = _ss_buffer["MissedCallCount"]
                result["RefreshTime"] = _ss_buffer["RefreshTime"]
                result["DD"] = _ss_buffer["DD"]
                result["MM"] = _ss_buffer["MM"]
                result["Hour"] = _ss_buffer["Hour"]
                result["Mins"] = _ss_buffer["Mins"]
                result["PMA"] = _ss_buffer["PMA"]
                result["SSTime"] = _ss_buffer["SSTime"]
                return result
            return "No screen saver found on the phone"
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception("func '%s' - err: '%s'!" % (fn, err))
            
    def change_options_menu_page(self, page_to_goto):
        """This method will change the options page. Applicable on touchscreen phone e.g. 6940
        Args:
            page_to_goto ; Page1, Page2, Page3 and Page4
        """
        try:
            self.phone.navigateToOptionsMenuPage(getattr(self.OptionsMenuPages, page_to_goto))
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception('func "%s" - err: "%s"!' % (fn, err))
            
    def select_option_on_options_menu(self, option_to_select):
        """This method will select an option(screen) on the options menu screen. Applicable on touchscreen phone e.g. 6940
        Args:
            option_to_select ; List given at DTP 57652
        """
        try:
            return self.phone.selectOptionOnOptionsMenu(getattr(self.OptionsScreens, option_to_select))
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception('func "%s" - err: "%s"!' % (fn, err))
            
    def select_page_in_moresoftkeys_pages(self, page_to_goto):
        """This method will select a page in more top soft keys pages.Applicable on touchscreen phone e.g. 6940
        Args:
            page_to_goto : Page1, Page2, Page3 and Page4
        """
        try:
            return self.phone.selectPageInMoreTopSoftKeysPages(getattr(self.MoreTopSoftkeysPages, page_to_goto))
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception('func "%s" - err: "%s"!' % (fn, err))








