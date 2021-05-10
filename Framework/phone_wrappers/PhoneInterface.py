"""
Interface for mitel 6xxx and shoretel ip4xx phones
This wrapper will abstract the different phone models's basic operations.

e.g. Below input_a_number abstracts different methods on different phone types
Shoretel(IP4xx) phone has pphone_dial_digits method while
Mitel(6xxx) phones has input_a_number method.

def input_a_number(self, string_to_dial):
    if "IP4" in self.phone_type:
        self.phone_obj.pphone_dial_digits(string_to_dial)
    else:
        self.phone_obj.input_a_number(string_to_dial)

"""
from __future__ import division

__author__ = "milton.villeda@mitel.com, nitin.kumar-2@mitel.com, shankara.mangalam@mitel.com"

import sys
import time

from phone_4xx import IP4xxInterface
from phone_6xxx.phone_69xx import Phone_69xx
from phone_6xxx.phone_68xx import Phone_68xx

from robot.api import logger

class PhoneInterface(object):
    """ This class is the Phone workflow layer
    """
    ROBOT_LIBRARY_SCOPE = 'GLOBAL'
    phone_types = ["IP485", "IP480", "IP420","Mitel6910", "Mitel6940", "Mitel6930", "Mitel6920", "Mitel6863i", "Mitel6865i", "Mitel6867i", "Mitel6869i"]
    total_phones = 0

    def __init__(self, phone_info, *args):
        """
        :param phone_info:    phone_info Dict
        :param args:
        """
        self.phone_type = phone_info['phoneModel']

        if self.phone_type not in self.phone_types:
            raise Exception("Phone type: \"%s\" is not supported. Please use a phone type from the list %s" % (self.phone_type,self.phone_types))

        if "IP4" in self.phone_type:
            self.phone_obj = IP4xxInterface.IP4xxInterface(phone_info)
        elif "Mitel69" in self.phone_type:
            self.phone_obj = Phone_69xx(phone_info)
        elif "Mitel68" in self.phone_type:
            self.phone_obj = Phone_68xx(phone_info)

        PhoneInterface.total_phones += 1
        # self.sanity_check()

    def print_total_phones(self):
        logger.info("Total phones in the test: %s" % PhoneInterface.total_phones)

    def upload_keyrcv_and_run(self):
        try:
            self.phone_obj.upload_keyrcv_and_run()
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception('func "%s" - err: "%s"!' % (fn, err))

    def enable_ssh_on_68xx(self):
        try:
            self.phone_obj.enable_ssh_on_68xx()
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception('func "%s" - err: "%s"!' % (fn, err))

    def run_pxcon_one_way_audio(self, other_phone):
        try:
            self.phone_obj.run_pxcon_one_way_audio(other_phone.phone_obj)
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception('func "%s" - err: "%s"!' % (fn, err))

    def check_two_way_audio(self, other_phone):
        '''
        :param other_phone:
        :return:
        Note: This method wont work when tested in 'Handset' mode on bluetooth headsets (like in 6940)
        '''
        try:
            self.phone_obj.check_two_way_audio(other_phone.phone_obj)
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception('func "%s" - err: "%s"!' % (fn, err))
    # Shankara narayanan -
    def check_one_way_audio(self, other_phone):
        try:
            self.phone_obj.check_one_way_audio(other_phone.phone_obj)
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception('func "%s" - err: "%s"!' % (fn, err))

    def check_no_audio(self, other_phone):
        try:
            self.phone_obj.check_no_audio(other_phone.phone_obj)
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception('func "%s" - err: "%s"!' % (fn, err))

    def check_audio_in_three_party_conference_call(self, phone1, phone2):
        try:
            self.phone_obj.check_oneway_conference_audio([phone1.phone_obj,phone2.phone_obj])
            phone1.phone_obj.check_oneway_conference_audio([self.phone_obj,phone2.phone_obj])
            phone2.phone_obj.check_oneway_conference_audio([self.phone_obj,phone1.phone_obj])
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception('func "%s" - err: "%s"!' % (fn, err))

    def check_audio_in_four_party_conference_call(self, phone1, phone2, phone3):
        try:
            self.phone_obj.check_oneway_conference_audio([phone1.phone_obj,phone2.phone_obj,phone3.phone_obj])
            phone1.phone_obj.check_oneway_conference_audio([self.phone_obj,phone2.phone_obj,phone3.phone_obj])
            phone2.phone_obj.check_oneway_conference_audio([self.phone_obj,phone1.phone_obj,phone3.phone_obj])
            phone3.phone_obj.check_oneway_conference_audio([self.phone_obj,phone1.phone_obj,phone2.phone_obj])
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception('func "%s" - err: "%s"!' % (fn, err))

    def check_audio_on_hold(self, expectedFreq = 200):
        '''
        :param expectedFreq: A MOH sine wave of 200 Hz wave file sampled at 8000Hz file should be created and uploaded into the system.
        :return:
        '''
        # try:
        #     self.phone_obj.check_audio_is_on_hold(other_phone.phone_obj, moh_enabled)
        # except Exception as err:
        #     fn = sys._getframe().f_code.co_name
        #     raise Exception('func "%s" - err: "%s"!' % (fn, err))
        try:
            return self.phone_obj.check_music_on_hold(expectedFreq)
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception('func "%s" - err: "%s"!' % (fn, err))

    def scp_put(self, file):
        try:
            self.phone_obj.scp_put(file)
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception("func '%s' - err: '%s'!" % (fn, err))

    def scp_get(self, file):
        try:
            self.phone_obj.scp_get(file)
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception("func '%s' - err: '%s'!" % (fn, err))

    def upload_path_confirmation_files(self):
        try:
            self.phone_obj.upload_path_confirmation_files()
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception("func '%s' - err: '%s'!" % (fn, err))

    def update_devnull_permissions(self):
        try:
            self.phone_obj.update_devnull_permissions()
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception("func '%s' - err: '%s'!" % (fn, err))

    def sanity_check(self):
        try:
            self.phone_obj.phone_sanity_check()
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception("func '%s' - err: '%s'!" % (fn, err))

    def make_call(self, phone_info_dict):
        try:
            self.phone_obj.make_call(phone_info_dict)
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception("func '%s' - err: '%s'!" % (fn, err))

    def answer_call(self):
        try:
            self.phone_obj.answer_call()
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception("func '%s' - err: '%s'!" % (fn, err))

    def dial_number(self, num):
        try:
            self.phone_obj.dial_number(num)
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception("func '%s' - err: '%s'!" % (fn, err))

    def enter_a_number(self, num):
        try:
            self.phone_obj.enter_a_number(num)
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception("func '%s' - err: '%s'!" % (fn, err))

    def handset_up(self):
        try:
            self.phone_obj.handset_up()
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception("func '%s' - err: '%s'!" % (fn, err))

    def get_active_audio_device(self):
        try:
            self.phone_obj.get_active_audio_device()
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception("func '%s' - err: '%s'!" % (fn, err))

    def verify_led_notificaion_when_diversion_activated(self):
        """This method ...

        Args:

        """
        try:
            self.phone_obj.verify_led_notificaion_when_diversion_activated()
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception('func "%s" - err: "%s"!' % (fn, err))

    def verify_led_notificaion_when_diversion_de_activated(self):
        """This method ...

        Args:

        """
        try:
            self.phone_obj.verify_led_notificaion_when_diversion_de_activated()
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception('func "%s" - err: "%s"!' % (fn, err))

    def verify_led_notificaion_when_follow_me_activated(self):
        """This method ...

        Args:

        """
        try:
            self.phone_obj.verify_led_notificaion_when_follow_me_activated()
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception('func "%s" - err: "%s"!' % (fn, err))

    def verify_led_notificaion_when_do_not_disturb_activated(self):
        """This method ...

        Args:

        """
        try:
            self.phone_obj.verify_led_notificaion_when_do_not_disturb_activated()
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception('func "%s" - err: "%s"!' % (fn, err))

    def verify_call_profile_number(self, profile_number):
        """This method ...

        Args:
            profile_number: string

        """
        try:
            self.phone_obj.verify_call_profile_number(profile_number)
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception('func "%s" - err: "%s"!' % (fn, err))

    def press_l1key(self):
        """This method ...

        Args:

        """
        try:
            self.phone_obj.press_l1key()
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception('func "%s" - err: "%s"!' % (fn, err))

    def press_l2key(self):
        """This method ...

        Args:

        """
        try:
            self.phone_obj.press_l2key()
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception('func "%s" - err: "%s"!' % (fn, err))

    # def press_softkey(self, sk_num):
    #     """This method ...
    #
    #     Args:
    #
    #     """
    #     try:
    #         self.phone_obj.press_hold()
    #     except Exception as err:
    #         fn = sys._getframe().f_code.co_name
    #         raise Exception('func "%s" - err: "%s"!' % (fn, err))

    def press_softkey(self, sk_num=1):
        """This method ...

        Args:

        """
        try:
            self.phone_obj.press_softkey(sk_num)
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception('func "%s" - err: "%s"!' % (fn, err))

    def press_softkey_three(self):
        """This method ...

        Args:

        """
        try:
            self.phone_obj.press_softkey_three()
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception('func "%s" - err: "%s"!' % (fn, err))

    def press_mute(self):
        """This method ...

        Args:

        """
        try:
            self.phone_obj.press_mute()
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception('func "%s" - err: "%s"!' % (fn, err))

    def press_hold(self):
        """This method ...

        Args:

        """
        try:
            self.phone_obj.press_hold()
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception('func "%s" - err: "%s"!' % (fn, err))

    def press_handsfree(self):
        """This method ...

        Args:

        """
        try:
            self.phone_obj.press_handsfree()
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception('func "%s" - err: "%s"!' % (fn, err))

    def press_offhook(self):
        """This method ...

        Args:

        """
        try:
            self.phone_obj.press_offhook()
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception('func "%s" - err: "%s"!' % (fn, err))

    def press_onhook(self):
        """This method ...

        Args:

        """
        try:
            self.phone_obj.press_onhook()
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception('func "%s" - err: "%s"!' % (fn, err))

    def press_volumeup(self):
        """This method ...

        Args:

        """
        try:
            self.phone_obj.press_volumeup()
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception('func "%s" - err: "%s"!' % (fn, err))

    def press_volumedown(self):
        """This method ...

        Args:

        """
        try:
            self.phone_obj.press_volumedown()
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception('func "%s" - err: "%s"!' % (fn, err))

    def verify_display_notification_in_ring(self, extension):
        """This method ...

        Args:
            diversion_category: string

        """
        try:
            self.phone_obj.verify_display_notification_when_in_ring(extension)
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception('func "%s" - err: "%s"!' % (fn, err))

    def verify_display_notification_when_diversion_activated(self, diversion_category):
        """This method ...

        Args:
            diversion_category: string

        """
        try:
            self.phone_obj.verify_display_notification_when_diversion_activated(diversion_category)
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception('func "%s" - err: "%s"!' % (fn, err))

    def de_activate_do_not_disturb(self):
        """This method ...

        Args:

        """
        try:
            self.phone_obj.de_activate_do_not_disturb()
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception('func "%s" - err: "%s"!' % (fn, err))

    def enable_monitoring(self):
        """This method ...

        Args:

        """
        try:
            self.phone_obj.enable_monitoring()
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception('func "%s" - err: "%s"!' % (fn, err))

    def enable_display_monitor(self):
        """This method ...

        Args:

        """
        try:
            self.phone_obj.enable_display_monitor()
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception('func "%s" - err: "%s"!' % (fn, err))

    def enable_key_monitor(self):
        """This method ...

        Args:

        """
        try:
            self.phone_obj.enable_key_monitor()
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception('func "%s" - err: "%s"!' % (fn, err))

    def enable_led_monitor(self):
        """This method ...

        Args:

        """
        try:
            self.phone_obj.enable_led_monitor()
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception('func "%s" - err: "%s"!' % (fn, err))

    def disable_all_monitors(self):
        """This method ...

        Args:

        """
        try:
            self.phone_obj.disable_all_monitors()
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception('func "%s" - err: "%s"!' % (fn, err))

    def enable_line_monitor(self):
        """This method ...

        Args:

        """
        try:
            self.phone_obj.enable_line_monitor()
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception('func "%s" - err: "%s"!' % (fn, err))

    def set_to_idle(self):
        """This method ...

        Args:

        """
        try:
            self.phone_obj.set_to_idle()
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception('func "%s" - err: "%s"!' % (fn, err))

    def get_config(self):
        """This method ...

        Args:

        """
        try:
            self.phone_obj.get_config()
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception('func "%s" - err: "%s"!' % (fn, err))

    def connect_to_terminal(self):
        """This method ...

        Args:

        """
        try:
            self.phone_obj.connect_to_terminal()
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception('func "%s" - err: "%s"!' % (fn, err))

    def disconnect_terminal(self):
        """This method ...

        Args:

        """
        try:
            self.phone_obj.disconnect_terminal()
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception('func "%s" - err: "%s"!' % (fn, err))

    def format_response(self, response_signal):
        """This method ...

        Args:
            response_signal: string

        """
        try:
            self.phone_obj.format_response(response_signal)
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception('func "%s" - err: "%s"!' % (fn, err))

##################################################################
#   PHYSICAL BUTTON PRESS using /bin/input command
##################################################################

    def press_physical_button(self, button_str, options=None):
        """This method presse a physical button
            using /bin/input
        Args:
            button_str: button to be pressed
        """
        try:
            # start_time = time.time()
            logger.info('Phone "%s" pressing button "%s" with options "%s"\n' % (self.phone_obj.phone_info['ipAddress'], button_str, options))
            self.phone_obj.press_physical_button(button_str.lower(), options)
            # logger.warn('Time elapsed on phone %s pressing button "%s" with options "%s": %.3f s\n' % (self.phone_obj.phone_info['ipAddress'], button_str, options, (time.time() - start_time)))
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception('func "%s" - err: "%s"!' % (fn, err))

    def dial_digits(self, digit_str):
        """This method presses digits

        Args: Nonw
        """
        self.press_physical_button(digit_str, 'multiple_btns')

    def end_call(self):
        """This method presses digits

        Args: Nonw
        """
        self.press_physical_button('BYE')

    def press_handsfree_button(self):
        """This method presses the physical button handsfree

        Args: Nonw

        """
        self.press_handsfree()

    def handset_offhook(self):
        """This method simulates going offhook on handset

        Args: Nonw
        """
        self.press_physical_button('HSW', 'offhook')

    def handset_onhook(self):
        """This method simulates going onhook on handset

        Args: Nonw
        """
        self.press_physical_button('HSW', 'onhook')

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

    # def press_hard_key(self, todo_hardphonekeys):
    #     """This method ...
    #
    #     Args:
    #         1: HardPhone.Keys
    #
    #     """
    #     try:
    #         self.phone_obj.press_hard_key(1)
    #     except Exception as err:
    #         fn = sys._getframe().f_code.co_name
    #         raise Exception('func "%s" - err: "%s"!' % (fn, err))

    def collect_responses(self):
        """This method ...

        Args:

        """
        try:
            self.phone_obj.collect_responses()
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception('func "%s" - err: "%s"!' % (fn, err))

    def collect_ack(self):
        """This method ...

        Args:

        """
        try:
            self.phone_obj.collect_ack()
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception('func "%s" - err: "%s"!' % (fn, err))

    def clear_response_buckets(self):
        """This method ...

        Args:

        """
        try:
            self.phone_obj.clear_response_buckets()
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception('func "%s" - err: "%s"!' % (fn, err))

    def send_request(self, signal_to_be_sent):
        """This method ...

        Args:
            signal_to_be_sent: byte[]

        """
        try:
            self.phone_obj.send_request(signal_to_be_sent)
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception('func "%s" - err: "%s"!' % (fn, err))

    def send_request_with_fresh_sequence_number(self, signal_to_be_sent):
        """This method ...

        Args:
            signal_to_be_sent: byte[]

        """
        try:
            self.phone_obj.send_request_with_fresh_sequence_number(signal_to_be_sent)
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception('func "%s" - err: "%s"!' % (fn, err))

    def answer_the_call(self, mode="Speaker", line_number = '1'):
        """This method ...
        mode = Speaker or Headset or Handset
        line_number = active line
        Args:

        """
        try:
            self.phone_obj.answer_the_call(mode, str(line_number))
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception('func "%s" - err: "%s"!' % (fn, err))

    def reject_the_call(self):
        """This method ...

        Args:

        """
        try:
            self.phone_obj.reject_the_call()
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception('func "%s" - err: "%s"!' % (fn, err))

    def disconnect_the_call(self, line_number='1'):
        """This method ...

        Args:

        """
        try:
            self.phone_obj.disconnect_the_call(line_number)
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception('func "%s" - err: "%s"!' % (fn, err))


    def off_hook(self):
        """This method ...

        Args:

        """
        try:
            self.phone_obj.off_hook()
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception('func "%s" - err: "%s"!' % (fn, err))

    def on_hook(self):
        """This method ...

        Args:

        """
        try:
            self.phone_obj.on_hook()
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception('func "%s" - err: "%s"!' % (fn, err))

    def call_extension(self, extension_to_be_called,**kwargs):
        """This method ...

        Args:
            extension_to_be_called: HardPhone

        """
        try:
            self.phone_obj.call_to_an_extension(extension_to_be_called,**kwargs)
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception('func "%s" - err: "%s"!' % (fn, err))

    def dial_service_code(self, service_code):
        """This method ...

        Args:
            service_code: string

        """
        try:
            self.phone_obj.dial_service_code(service_code)
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception('func "%s" - err: "%s"!' % (fn, err))

    def dial_anumber(self, terminal_phone):
        """This method ...

        Args:
            terminal_phone: HardPhone

        """
        try:
            self.phone_obj.dial_anumber(terminal_phone)
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception('func "%s" - err: "%s"!' % (fn, err))

    def press_key(self, key_to_be_pressed, press_count=1):
        """This method ...

        Args:
            key_to_be_pressed: int

        """
        try:
            self.phone_obj.press_key(key_to_be_pressed, press_count)
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception('func "%s" - err: "%s"!' % (fn, err))

    def long_press_key(self, key_to_be_pressed, press_count=1):
        """This method ...

        Args:
            key_to_be_pressed: int

        """
        try:
            self.phone_obj.long_press_key(key_to_be_pressed, press_count)
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception('func "%s" - err: "%s"!' % (fn, err))

    def press_expansion_box_key(self, key_to_be_pressed, press_count=1):
        """This method ...

        Args:
            key_to_be_pressed: int

        """
        try:
            self.phone_obj.press_expansion_box_key(key_to_be_pressed, press_count)
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception('func "%s" - err: "%s"!' % (fn, err))


    def release_key(self, key_to_be_released):
        """This method ...

        Args:
            key_to_be_released: HardPhone.Keys

        """
        try:
            self.phone_obj.release_key(key_to_be_released)
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception('func "%s" - err: "%s"!' % (fn, err))


    def input_a_number(self, string_to_dial):
        """This method ...

        Args:
            terminal_phone: string

        """
        try:
            self.phone_obj.input_a_number(string_to_dial)
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception('func "%s" - err: "%s"!' % (fn, err))

    def call_from_remote_extension(self, number_r1):
        """This method ...

        Args:
            number_r1: HardPhone

        """
        try:
            self.phone_obj.call_from_remote_extension(number_r1)
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception('func "%s" - err: "%s"!' % (fn, err))

    def call_from_sip_mobile_extension(self, number_r1):
        """This method ...

        Args:
            number_r1: HardPhone

        """
        try:
            self.phone_obj.call_from_sip_mobile_extension(number_r1)
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception('func "%s" - err: "%s"!' % (fn, err))

    def activate_ic_sdiversion_with_service_codes(self, diversion_category):
        """This method ...

        Args:
            diversion_category: string

        """
        try:
            self.phone_obj.activate_ic_sdiversion_with_service_codes(diversion_category)
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception('func "%s" - err: "%s"!' % (fn, err))

    def activate_dn_dwith_service_code_and_verify_notifications(self, string_to_be_verified):
        """This method ...

        Args:
            string_to_be_verified: string

        """
        try:
            self.phone_obj.activate_dn_dwith_service_code_and_verify_notifications(string_to_be_verified)
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception('func "%s" - err: "%s"!' % (fn, err))

    def activate_dn_dwith_service_code(self):
        """This method ...

        Args:

        """
        try:
            self.phone_obj.activate_dn_dwith_service_code()
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception('func "%s" - err: "%s"!' % (fn, err))

    def deactivate_dn_dwith_service_code(self):
        """This method ...

        Args:

        """
        try:
            self.phone_obj.deactivate_dn_dwith_service_code()
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception('func "%s" - err: "%s"!' % (fn, err))

    def deactivate_group_dn_dwith_service_code(self, group_number):
        """This method ...

        Args:
            group_number: string

        """
        try:
            self.phone_obj.deactivate_group_dn_dwith_service_code(group_number)
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception('func "%s" - err: "%s"!' % (fn, err))

    def dial_service_code_and_verify_display(self, string_to_be_verified):
        """This method ...

        Args:
            string_to_be_verified: string

        """
        try:
            self.phone_obj.dial_service_code_and_verify_display(string_to_be_verified)
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception('func "%s" - err: "%s"!' % (fn, err))

    def activate_group_dn_dwith_service_code(self, group_number):
        """This method ...

        Args:
            group_number: string

        """
        try:
            self.phone_obj.activate_group_dn_dwith_service_code(group_number)
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception('func "%s" - err: "%s"!' % (fn, err))

    def check_phone_connection(self):
        """This method ...

        Args:

        """
        try:
            self.phone_obj.check_phone_connection()
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception('func "%s" - err: "%s"!' % (fn, err))

    def connect_to_phone(self):
        """This method ...

        Args:

        """
        try:
            self.phone_obj.connect_to_phone()
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception('func "%s" - err: "%s"!' % (fn, err))

    def program_follow_me_remotely(self, extension_number_to_be_routed):
        """This method ...

        Args:
            extension_number_to_be_routed: string

        """
        try:
            self.phone_obj.program_follow_me_remotely(extension_number_to_be_routed)
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception('func "%s" - err: "%s"!' % (fn, err))

    def cancel_active_call_back(self):
        """This method ...

        Args:

        """
        try:
            self.phone_obj.cancel_active_call_back()
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception('func "%s" - err: "%s"!' % (fn, err))

    def login_with_dual_forking_extension(self, dual_forking_extension_number):
        """This method ...

        Args:
            dual_forking_extension_number: string

        """
        try:
            self.phone_obj.login_with_dual_forking_extension(dual_forking_extension_number)
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception('func "%s" - err: "%s"!' % (fn, err))

    def login_with_different_extension(self, extension_number):
        """This method ...

        Args:
            extension_number: string

        """
        try:
            self.phone_obj.login_with_different_extension(extension_number)
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception('func "%s" - err: "%s"!' % (fn, err))

    def login_back_with_base_extension(self):
        """This method ...

        Args:

        """
        try:
            self.phone_obj.login_back_with_base_extension()
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception('func "%s" - err: "%s"!' % (fn, err))

    def pick_call_with_non_member_of_group(self, extension):
        """This method ...

        Args:
            extension: string

        """
        try:
            self.phone_obj.pick_call_with_non_member_of_group(extension)
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception('func "%s" - err: "%s"!' % (fn, err))

    def pick_call_with_member_of_group(self):
        """This method ...

        Args:

        """
        try:
            self.phone_obj.pick_call_with_member_of_group()
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception('func "%s" - err: "%s"!' % (fn, err))

    def verify_line_state(self,LineStatus,LineNumber="1", activeLineNum="1", maxWaitTimeoutInSeconds = 10):
        """This method will verify the status of a line...

        Args:

        """
        try:
            return self.phone_obj.verify_line_state(str(LineStatus),str(LineNumber), str(activeLineNum), maxWaitTimeoutInSeconds)
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception('func "%s" - err: "%s"!' % (fn, err))

    def get_line_buffer(self):
        """This method will return the buffer containing the state of al the lines on the phone...

        Args: None

        """
        try:
            return self.phone_obj.get_line_buffer()
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception('func "%s" - err: "%s"!' % (fn, err))

    def verify_led_state(self,type, mode,color ="" ,timeout = 10):
        """This method will verify the status of a led...

        Args:

        """
        try:
            if str.isdigit(str(color)):
                return self.phone_obj.verify_led_state(str(type), str(mode),"", timeout)
            else:
                return self.phone_obj.verify_led_state(str(type), str(mode),str(color), timeout)
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception('func "%s" - err: "%s"!' % (fn, err))

    def get_icons(self, **filters):

        """
        This method will return a list of icon packets which matches the filters passed as arugument

        filter:
            Module          : 0 = Phones, 1= expansion module
            IconIndex       : 1 to N where N varies on maximum number of icon types e.g 1-12 in case of home
            Icon            : As described in icon table
            IconColour      : As decribed in the icon color table
            Text1           : 0 = No character ,First character/text on/with Icon Range(0-9,A-Z,a-z)
            Text2           : 0 = No character .Second character/text on/with Icon Range(0-9,A-Z,a-z)
            View            : 0 = Default, 1=MXONE/Mi 400, 2=Mivoice connect
            State           :
            Par1 to Par6    : For Future

        :return
            A list of icon packets.
        """

        available_icons = self.phone_obj.get_icon_buffer() # List of icon packets
        print (available_icons)
        if not len(filters):
            return available_icons
        out = []
        for icons in available_icons:
            counter  = 0
            for key, value in filters.items():
                if str(icons.get(key)).lower() == str(value).lower():
                    counter  +=1
                else:
                    break
            if len(filters) == counter:
                out.append(icons)
        return out
    
    def verify_line_icon_state(self,lineNumber, state):
        """This method will verify the icon states against line number..
        <lineNumber>    :Range from 1 to 12 which will tell on which line any icon is created.for example, 6930 has 12 lines (by default).
        <state>         :Here which type of icon is associated. Ref: 'Table 19: Phone Icon Id in ATAP doc'

        Args:

        """

        raise Exception('Deprecated, please use get_icons() method')

    def verify_state_icon(self, state):
        """This method will verify the state of a phone
        <state>         :Ref: 'Table 19: Phone Icon Id in ATAP doc'
        Available Icon states :Available, In a meeting, Out of office, Vacation, Custom, Do Not Disturb
        Note: Please make sure at least once the 'State' button is pressed before using this method / after connection. Ideal place is to have in Test Setup
        """
        raise Exception('Deprecated, please use get_icons() method')

    def verify_call_history_icon(self, state):
        """This method will verify different icons in Call History Window
        <state>         :Ref: 'Table 19: Phone Icon Id in ATAP doc'
        Available Icon states : CALL_HISTORY_ALL, CALL_HISTORY_MISSED,CALL_HISTORY_OUTGOING,  CALL_HISTORY_INCOMING_RECEIVED

        """

        raise Exception('Deprecated, please use get_icons() method')

    def verify_voice_mail_window_icons(self, icon, icon_text):
        """This method will verify different icons in Voice Mail Window
        <state>         :Ref: 'Table 19: Phone Icon Id in ATAP doc'
        Available Icon states : VOICE_MAIL_SAVED, VOICE_MAIL_DELETED, VOICE_MAIL_INBOX,VOICE_MAIL_PAUSE, VOICE_MAIL_PLAY
        """

        raise Exception('Deprecated, please use get_icons() method')

    def get_led_buffer(self):
        """This method will return the buffer containing details of all leds on the phone...

        Args: None

        """
        try:
            return self.phone_obj.get_led_buffer()
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception('func "%s" - err: "%s"!' % (fn, err))

    def set_line_for_hunt_group(self, hunt_group_number):
        """This method ...

        Args:
            hunt_group_number: string

        """
        try:
            self.phone_obj.set_line_for_hunt_group(hunt_group_number)
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception('func "%s" - err: "%s"!' % (fn, err))

    def remove_line_for_hunt_group(self, hunt_group_number):
        """This method ...

        Args:
            hunt_group_number: string

        """
        try:
            self.phone_obj.remove_line_for_hunt_group(hunt_group_number)
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception('func "%s" - err: "%s"!' % (fn, err))

    def enable_message_waiting(self, extension):
        """This method ...

        Args:
            extension: string

        """
        try:
            self.phone_obj.enable_message_waiting(extension)
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception('func "%s" - err: "%s"!' % (fn, err))

    def intrusion_from_extension(self, extension):
        """This method ...

        Args:
            extension: HardPhone

        """
        try:
            self.phone_obj.intrusion_from_extension(extension)
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception('func "%s" - err: "%s"!' % (fn, err))

    def verify_notifications_when_pe_ndeactivated(self):
        """This method ...

        Args:

        """
        try:
            self.phone_obj.verify_notifications_when_pe_ndeactivated()
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception('func "%s" - err: "%s"!' % (fn, err))

    def verify_reroutingto_in_attend_when_not_responding(self, phone2):
        """This method ...

        Args:
            phone2: string

        """
        try:
            self.phone_obj.verify_reroutingto_in_attend_when_not_responding(phone2)
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception('func "%s" - err: "%s"!' % (fn, err))

    def verify_reroutingto_in_attend_when_cancel_call(self, phone2):
        """This method ...

        Args:
            phone2: string

        """
        try:
            self.phone_obj.verify_reroutingto_in_attend_when_cancel_call(phone2)
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception('func "%s" - err: "%s"!' % (fn, err))

    def verify_reroutingto_in_attend_when_dial_vacant_number(self, vacant_number):
        """This method ...

        Args:
            vacant_number: string

        """
        try:
            self.phone_obj.verify_reroutingto_in_attend_when_dial_vacant_number(vacant_number)
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception('func "%s" - err: "%s"!' % (fn, err))

    def verify_reroutingto_in_attend_when_dial_logged_off_terminal(self, phone2):
        """This method ...

        Args:
            phone2: string

        """
        try:
            self.phone_obj.verify_reroutingto_in_attend_when_dial_logged_off_terminal(phone2)
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception('func "%s" - err: "%s"!' % (fn, err))

    def verify_private_trunk_reroutingto_in_attend_when_not_responding(self, phone2):
        """This method ...

        Args:
            phone2: string

        """
        try:
            self.phone_obj.verify_private_trunk_reroutingto_in_attend_when_not_responding(phone2)
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception('func "%s" - err: "%s"!' % (fn, err))

    def verify_private_reroutingto_in_attend_when_cancel_call(self, phone2):
        """This method ...

        Args:
            phone2: string

        """
        try:
            self.phone_obj.verify_private_reroutingto_in_attend_when_cancel_call(phone2)
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception('func "%s" - err: "%s"!' % (fn, err))

    def verify_private_reroutingto_in_attend_when_dial_vacant_number(self, vacant_number):
        """This method ...

        Args:
            vacant_number: string

        """
        try:
            self.phone_obj.verify_private_reroutingto_in_attend_when_dial_vacant_number(vacant_number)
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception('func "%s" - err: "%s"!' % (fn, err))

    def verify_private_reroutingto_in_attend_when_dial_logged_off_terminal(self, phone2):
        """This method ...

        Args:
            phone2: string

        """
        try:
            self.phone_obj.verify_private_reroutingto_in_attend_when_dial_logged_off_terminal(phone2)
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception('func "%s" - err: "%s"!' % (fn, err))

    def verify_external_call_to_in_attend(self, in_attend_number):
        """This method ...

        Args:
            in_attend_number: string

        """
        try:
            self.phone_obj.verify_external_call_to_in_attend(in_attend_number)
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception('func "%s" - err: "%s"!' % (fn, err))

    def verify_line_notificaion_when_do_not_disturb_activated(self):
        """This method ...

        Args:

        """
        try:
            self.phone_obj.verify_line_notificaion_when_do_not_disturb_activated()
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception('func "%s" - err: "%s"!' % (fn, err))

    def set_to_default(self):
        """This method ...

        Args:

        """
        try:
            self.phone_obj.set_to_default()
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception('func "%s" - err: "%s"!' % (fn, err))

    def check_phone_is_online(self):
        """This method ...

        Args:

        """
        try:
            self.phone_obj.check_phone_is_online()
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception('func "%s" - err: "%s"!' % (fn, err))

    def sleep(self, seconds):
        """This method ...

        Args:
            seconds: double

        """
        try:
            self.phone_obj.sleep(seconds)
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception('func "%s" - err: "%s"!' % (fn, err))

    def make_delay(self, sec):
        """This method ...

        Args:
            2.0: double

        """
        try:
            sleep(sec)
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception('func "%s" - err: "%s"!' % (fn, err))

    def deactivate_follow_me(self):
        """This method ...

        Args:

        """
        try:
            self.phone_obj.deactivate_follow_me()
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception('func "%s" - err: "%s"!' % (fn, err))

    def activate_direct_diversion(self, extension_number):
        """ This method ...

        Args:
            extension_number: string

        """
        try:
            self.phone_obj.activate_direct_diversion(extension_number)
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception('func "%s" - err: "%s"!' % (fn, err))

    def verify_display_message_contents(self, contents):
        """This method ...

        Args:

        """
        try:
            return self.phone_obj.verify_display_message_contents(contents)
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception('func "%s" - err: "%s"!' % (fn, err))

    def verify_display_on_screen(self, contents):
        """This method ...

        Args:

        """
        try:
            return self.phone_obj.verify_display_on_screen(contents)
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception('func "%s" - err: "%s"!' % (fn, err))

    def verify_notifications_in_ring(self,LineNumber=1):
        """This method ...

        Args:

        """
        try:
            self.phone_obj.verify_notifications_when_in_ring(LineNumber)
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception('func "%s" - err: "%s"!' % (fn, err))


    def verify_notifications_when_call_back_ring(self, extension_to_be_verified):
        """This method ...

        Args:
            extension_to_be_verified: string

        """
        try:
            self.phone_obj.verify_notifications_when_call_back_ring(extension_to_be_verified)
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception('func "%s" - err: "%s"!' % (fn, err))

    def verify_notifications_when_ed_ngets_call(self, number_of_responses_to_be_stored):
        """This method ...

        Args:
            number_of_responses_to_be_stored: int

        """
        try:
            self.phone_obj.verify_notifications_when_ed_ngets_call(number_of_responses_to_be_stored)
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception('func "%s" - err: "%s"!' % (fn, err))

    def verify_notification_when_message_waiting(self):
        """This method ...

        Args:

        """
        try:
            self.phone_obj.verify_notification_when_message_waiting()
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception('func "%s" - err: "%s"!' % (fn, err))

    def verify_notifications_in_idle(self):
        """This method ...

        Args:

        """
        try:
            # import rpdb2; rpdb2.start_embedded_debugger('admin1')

            self.phone_obj.verify_notifications_when_in_idle()
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
            # self.phone_obj.verify_notifications_when_in_idle(str_to_bo_verified)
        # except Exception as err:
            # fn = sys._getframe().f_code.co_name
            # raise Exception('func "%s" - err: "%s"!' % (fn, err))

    def verify_notifications_when_in_busy(self):
        """This method ...

        Args:

        """
        try:
            self.phone_obj.verify_notifications_when_in_busy()
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception('func "%s" - err: "%s"!' % (fn, err))


    def verify_notifications_in_connected(self):
        """This method ...

        Args:

        """
        try:
            self.phone_obj.verify_notifications_when_in_connected()
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception('func "%s" - err: "%s"!' % (fn, err))

    def verify_notifications_when_follow_me_activated(self, remote_number):
        """This method ...

        Args:
            remote_number: string

        """
        try:
            self.phone_obj.verify_notifications_when_follow_me_activated(remote_number)
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception('func "%s" - err: "%s"!' % (fn, err))

    def verify_notifications_when_diversion_activated(self, diversion_category):
        """This method ...

        Args:
            diversion_category: string

        """
        try:
            self.phone_obj.verify_notifications_when_diversion_activated(diversion_category)
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception('func "%s" - err: "%s"!' % (fn, err))

    def verify_notifications_when_diversion_de_activated(self):
        """This method ...

        Args:

        """
        try:
            self.phone_obj.verify_notifications_when_diversion_de_activated()
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception('func "%s" - err: "%s"!' % (fn, err))

    def verify_led_notifications_when_pe_ndeactivated(self):
        """This method ...

        Args:

        """
        try:
            self.phone_obj.verify_led_notifications_when_pe_ndeactivated()
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception('func "%s" - err: "%s"!' % (fn, err))

    def verify_notifications_when_in_clearing(self):
        """This method ...

        Args:

        """
        try:
            self.phone_obj.verify_notifications_when_in_clearing()
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception('func "%s" - err: "%s"!' % (fn, err))

    def verify_line_notificaion_when_in_idle(self):
        """This method ...

        Args:

        """
        try:
            self.phone_obj.verify_line_notificaion_when_in_idle()
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception('func "%s" - err: "%s"!' % (fn, err))

    def verify_line_notificaion_when_in_clearing(self):
        """This method ...

        Args:

        """
        try:
            self.phone_obj.verify_line_notificaion_when_in_clearing()
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception('func "%s" - err: "%s"!' % (fn, err))

    def verify_line_notificaion_when_in_connected(self):
        """This method ...

        Args:

        """
        try:
            self.phone_obj.verify_line_notificaion_when_in_connected()
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception('func "%s" - err: "%s"!' % (fn, err))

    def verify_line_notificaion_when_out_going(self):
        """This method ...

        Args:

        """
        try:
            self.phone_obj.verify_line_notificaion_when_out_going()
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception('func "%s" - err: "%s"!' % (fn, err))

    def verify_led_notificaion_when_in_idle(self):
        """This method ...

        Args:

        """
        try:
            self.phone_obj.verify_led_notificaion_when_in_idle()
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception('func "%s" - err: "%s"!' % (fn, err))

    def verify_call_list_profile(self, profile_number):
        """This method ...

        Args:
            profile_number: string

        """
        try:
            self.phone_obj.verify_call_list_profile(profile_number)
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception('func "%s" - err: "%s"!' % (fn, err))

    def verify_notifications_when_do_not_disturb_activated(self):
        """This method ...

        Args:

        """
        try:
            self.phone_obj.verify_notifications_when_do_not_disturb_activated()
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception('func "%s" - err: "%s"!' % (fn, err))

    def verify_line_notifications_when_do_not_disturb_activated(self):
        """This method ...

        Args:

        """
        try:
            self.phone_obj.verify_line_notifications_when_do_not_disturb_activated()
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception('func "%s" - err: "%s"!' % (fn, err))

    def verify_display_contents(self, string_to_be_verified):
        """This method ...

        Args:
            string_to_be_verified: string

        """
        try:
            return self.phone_obj.verify_display_contents(string_to_be_verified)
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception('func "%s" - err: "%s"!' % (fn, err))

    def verify_phone_display(self, string_to_be_verified):
        """This method ...

        Args:
            string_to_be_verified: string

        """
        try:
            return self.phone_obj.verify_in_phone_display(string_to_be_verified)
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception('func "%s" - err: "%s"!' % (fn, err))

    def get_phone_display(self, phone_mode = "non idle"):
        """returns everything on the phone display...

        Args:
            phone_mode : idle if phone is not in use
                       : non idle if the phone is in use i.e. in a call or any key pressed
        """
        try:
            return self.phone_obj.get_phone_display(phone_mode)
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception('func "%s" - err: "%s"!' % (fn, err))

    def reboot_terminal(self, wait_till_online=True, timeout=300):
        '''
        wait_till_online : if true, this function will wait till the phone comes back online
        timeout : this time will be added to an inbuilt wait of 20 seconds
        reboot the phone
        :return: None
        '''
        try:
            self.phone_obj.reboot_terminal()
            if wait_till_online:
                self.phone_obj.WaitTillPhoneComesOnline(timeout)
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception('func "%s" - err: "%s"!' % (fn, err))

    def get_firmware_version(self):
        '''
        Firmware version of the phone
        :return: Firmware version of the phone
        '''
        try:
            return self.phone_obj.get_firmware_version()
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception('func "%s" - err: "%s"!' % (fn, err))

    def get_library_version(self):
        '''
        Library version of ATAP
        :return: Library version of ATAP
        '''
        try:
            return self.phone_obj.get_library_version()
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception('func "%s" - err: "%s"!' % (fn, err))

    def clear_sip_traces(self):
        '''
        Clears the sip traces on the phone
        :return: None
        '''
        try:
            return self.phone_obj.clear_sip_traces()
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception('func "%s" - err: "%s"!' % (fn, err))

    def get_sip_in_messages(self):
        '''
        sip messages received by the phone
        :return: SIP IN messages from the phone
        '''
        try:
            return self.phone_obj.get_sip_in_messages()
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception('func "%s" - err: "%s"!' % (fn, err))

    def get_sip_out_messages(self):
        '''
        sip messages sent by the phone
        :return: SIP OUT messages from the phone
        '''
        try:
            return self.phone_obj.get_sip_out_messages()
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception('func "%s" - err: "%s"!' % (fn, err))



    def verify_sip_private_trunk_reroutingto_in_attend_when_not_responding(self, phone2):
        """This method ...

        Args:
            phone2: string

        """
        try:
            self.phone_obj.verify_sip_private_trunk_reroutingto_in_attend_when_not_responding(phone2)
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception('func "%s" - err: "%s"!' % (fn, err))
            
    def get_phone_brightness(self):
        """This method will return the current brightness level of the screen...

        Args:
            None

        """
        try:
            if "IP4" in self.phone_type:
                pass#self.phone_obj.pget_phone_brightness()
            else:
                return self.phone_obj.get_phone_brightness()
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception('func "%s" - err: "%s"!' % (fn, err))
            
    def is_background_image_set(self):
        """This method will return True if some custom background image is set on idle screen...
        Args:
            None

        """
        try:
            if "IP4" in self.phone_type:
                pass  # self.phone_obj.is_background_image_set()
            else:
                return self.phone_obj.is_background_image_set()
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception('func "%s" - err: "%s"!' % (fn, err))
            
    def get_tone_at_phone(self):
        """This method will return the Tone at the phone...
        Args:
            None
        """
        try:
            if "IP4" in self.phone_type:
                pass  # self.phone_obj.is_background_image_set()
            else:
                return self.phone_obj.get_tone_at_phone()
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception('func "%s" - err: "%s"!' % (fn, err))

    def get_highlighted_text_properties(self):
        """This method will return the Highlighted text on the phone...
        Args:
            None
        """
        try:
            if "IP4" in self.phone_type:
                pass  # self.phone_obj.is_background_image_set()
            else:
                return self.phone_obj.get_highlighted_text_properties()
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception('func "%s" - err: "%s"!' % (fn, err))

    def get_menu_text_properties(self):
        """This method will return the Highlighted text on the phone...
        Args:
            None
        """
        try:
            if "IP4" in self.phone_type:
                pass  # self.phone_obj.is_background_image_set()
            else:
                return self.phone_obj.get_menu_text_properties()
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception('func "%s" - err: "%s"!' % (fn, err))

    def get_formatted_text_properties(self):
        """This method will return the Highlighted text on the phone...
        Args:
            None
        """
        try:
            if "IP4" in self.phone_type:
                pass  # self.phone_obj.is_background_image_set()
            else:
                return self.phone_obj.get_formatted_text_properties()
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception('func "%s" - err: "%s"!' % (fn, err))
            
    def get_phone_screensaver(self):
        """This method will return the details about the screen saver...
        Args:
            None
        """
        try:
            if "IP4" in self.phone_type:
                pass#self.phone_obj.pget_phone_brightness()
            else:
                return self.phone_obj.get_screensaver_properties()
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception('func "%s" - err: "%s"!' % (fn, err))
            
    def change_options_menu_page(self, page_to_goto):
        """This method will change the options page. Applicable on touchscreen phone e.g. 6940
        Args:
            page_to_goto ; Page1, Page2, Page3 and Page4
        """
        try:
            if "IP4" in self.phone_type:
                pass#self.phone_obj.change_options_menu_page()
            else:
                return self.phone_obj.change_options_menu_page(page_to_goto)
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception('func "%s" - err: "%s"!' % (fn, err))
            
    def select_option_on_options_menu(self, option_to_select):
        """This method will select an option(screen) on the options menu screen. Applicable on touchscreen phone e.g. 6940
        Args:
            option_to_select ; List given at DTP 57652
            
        Note : This function will not verify if the screen has been changed.
        """
        try:
            if "IP4" in self.phone_type:
                pass#self.phone_obj.select_option_on_options_menu()
            else:
                return self.phone_obj.select_option_on_options_menu(option_to_select)
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception('func "%s" - err: "%s"!' % (fn, err))
            
    def select_page_in_moresoftkeys_pages(self, page_to_goto):
        """This method will select a page in more top soft keys pages.Applicable on touchscreen phone e.g. 6940
        Args:
            page_to_goto : Page1, Page2, Page3 and Page4
            
        """
        try:
            if "IP4" in self.phone_type:
                pass#self.phone_obj.select_page_in_moresoftkeys_pages()
            else:
                return self.phone_obj.select_page_in_moresoftkeys_pages(page_to_goto)
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception('func "%s" - err: "%s"!' % (fn, err))
    
    def capture_screenshot(self, path=None, username="admin", password="1234"):
        """This method will take screen shot on phone
        Args:
            path : Location to save the screen shot, current working dir will be used if not provided
            username : username
            password : password
            
        """
        try:
            if "IP4" in self.phone_type:
                pass#self.phone_obj.capture_screenshot()
            else:
                return self.phone_obj.capture_screenshot(path, username, password)
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception('func "%s" - err: "%s"!' % (fn, err))
            
    def get_all_display_contents(self):
        """This method will return all the text present on the phone UI

        """
        try:
            if "IP4" in self.phone_type:
                pass#self.phone_obj.get_all_display_contents()
            else:
                return self.phone_obj.get_all_display_contents()
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception('func "%s" - err: "%s"!' % (fn, err))


if __name__ == "__main__":
    import logging
    import os
    framework_path = os.path.join(os.path.dirname((os.path.dirname(os.path.dirname(__file__)))),"Framework")
    sys.path.append(os.path.join(framework_path,"provisioning_wrappers","boss_wrappers"))
    sys.path.append(os.path.join(framework_path,"phone_wrappers"))
    sys.path.append(os.path.join(framework_path,"utils"))

    #from D2API import D2API
    #import robot.utils.dotdict


    logger = logging.getLogger("RobotFramework")
    logger.setLevel(logging.DEBUG)
    logger.addHandler(logging.StreamHandler())
    # phone_2 = PhoneInterface({"phoneModel":"Mitel6930", "ipAddress":"10.198.34.75", "extensionNumber":"4098", "phoneName":"yo1"})

    # phone_12 = PhoneInterface({"phoneModel": "Mitel6920", "ipAddress": "10.211.41.202", "extensionNumber":"70008", "phoneName":"yo1","hq_rsa":"hq.rsa"})
    # phone_13 = PhoneInterface({"phoneModel": "Mitel6920", "ipAddress": "10.211.41.202", "extensionNumber":"70008", "phoneName":"yo1","hq_rsa":"hq.rsa"})

    # phone_2 = PhoneInterface({"phoneModel": "Mitel6920", "ipAddress": "10.112.123.110", "extensionNumber": "4165142503", "phoneName": "yo2"})
    # phone_1 = PhoneInterface({"phoneModel": "Mitel6920", "ipAddress": "10.112.123.166", "extensionNumber": "4165142504", "phoneName": "yo12dsds2sd2sw3333rx3xds"})
    # phone_1 = PhoneInterface({"phoneModel": "Mitel6867i", "ipAddress": "10.112.91.151", "extensionNumber": "4165142504", "phoneName": "yo2"})
    # phone_1 = PhoneInterface({"phoneModel": "Mitel6867i", "ipAddress": "10.112.91.38", "extensionNumber": "4165142542", "phoneName": "yo2"})

    # phone_2 = PhoneInterface({"phoneModel": "Mitel6920", "ipAddress": "192.168.0.7", "extensionNumber": "10", "phoneName": "yo2"})
    # phone_1 = PhoneInterface({"phoneModel": "Mitel6920", "ipAddress": "192.168.0.5", "extensionNumber":"11", "phoneName":"yo2"})

    # phone_1 = PhoneInterface({"phoneModel": "Mitel6920", "ipAddress": "10.112.123.155", "extensionNumber": "4165142541", "phoneName": "yo2"})
    # phone_2 = PhoneInterface({"phoneModel": "Mitel6920", "ipAddress": "10.112.123.166", "extensionNumber": "4165142512", "phoneName":"yo1"})

    # phone_1 = PhoneInterface({"phoneModel": "Mitel6867i", "ipAddress": "10.112.91.151", "extensionNumber": "4165142503", "phoneName": "yo2"})
    # phone_2 = PhoneInterface({"phoneModel": "Mitel6865i", "ipAddress": "10.112.91.78", "extensionNumber": "4165142504", "phoneName": "yo2"})

    #phone_1 = PhoneInterface({"phoneModel": "Mitel6930", "ipAddress": "10.112.123.39", "extensionNumber": "4165142518",
    #                          "phoneName": "robot1"})
    #phone_2 = PhoneInterface({"phoneModel": "Mitel6867i", "ipAddress": "10.112.123.30", "extensionNumber": "4165142539",
    #                          "phoneName": "robot2"})        


    # answer_the_call and disconnect_call
    # phone_1 = PhoneInterface({"phoneModel": "Mitel6940", "ipAddress": "10.211.22.86", "extensionNumber": "3002",
    #                        "phoneName": "3002"})
    phone_1 = PhoneInterface({"phoneModel": "Mitel6930", "ipAddress": "10.211.22.240", "extensionNumber": "3001",
                            "phoneName": "3001"})
    # phone_1= PhoneInterface({"phoneModel": "Mitel6867i", "ipAddress": "10.211.22.241", "extensionNumber": "3003",
    #                          "phoneName": "3003"})
    # phone_4 = PhoneInterface({"phoneModel": "Mitel6865i", "ipAddress": "10.211.22.242", "extensionNumber": "3000",
    #                           "phoneName": "3000"})
    
    # Issue with verifylinenotificationwhen in connected

    time.sleep(3)
   # phone_1.press_softkey(2)
   #  phone_1.check_two_way_audio(phone_2)
   #  time.sleep(10)
   #  # # phone_1.disconnect_the_call(line_number='1')
    phone_1.press_key("Redial")
    time.sleep(10)
    print(phone_1.get)

   # phone_1.press_softkey(3)
    # print(phone_1.verify_display_message_contents("Phone lock"))
    # phone_1.press_softkey(1)
  #   time.sleep(10)
  #   phone_1.press_softkey(1)
  #   phone_1.input_a_number("1111")
  #   phone_1.press_key("ScrollDown")
  #   phone_1.input_a_number("1111")
  #   time.sleep(10)
  #   phone_1.press_softkey(1)
  #   phone_1.press_softkey(3)
    time.sleep(10)
   # print(phone_1.get_icons())
   #  phone_2.input_a_number("3001")
   #  phone_2.press_softkey(1)
   #  time.sleep(3)
   #  phone_4.press_key("OffHook")
   #  phone_1.press_key("Redial")
   #  time.sleep(1)
   #  print(phone_1.verify_display_message_contents("Redial list"))
  #  phone_1.press_softkey(1)
    time.sleep(15)
    # phone_2.input_a_number("3001")
    # phone_2.press_softkey(1)


   # phone_1.press_softkey(2)
   # phone_1.press_key("ScrollDown")
    time.sleep(30)
   #  phone_1.press_key("ScrollRight")
   #  time.sleep(30)
   #  phone_3.press_softkey(1)
   #  time.sleep(30)
   #  phone_2.press_softkey(1)
   #  phone_3.input_a_number("#21")
   #  phone_3.press_softkey(1)
    phone_1.disconnect_terminal()
   # phone_1.enable_ssh_on_68xx()

    
    
    
    # ENTA 5453
    # phone_1.capture_screenshot()
    # phone_1.capture_screenshot(path=r"C:\PhoneScreenshots")
    #
    # ENTA 5000 and 5284
    #phone_1.call_extension(phone_2.phone_obj.phone, mode='Speaker')
    #phone_1.press_softkey(1)
    #import pdb, sys; pdb.Pdb(stdout=sys.__stdout__).set_trace()
    #print(phone_1.verify_led_state('indicator_line_1', 'on'))
    #phone_2.press_key('HandsFree')
    #print(phone_2.verify_led_state('Line1', 'on'))
    #import pdb, sys; pdb.Pdb(stdout=sys.__stdout__).set_trace()
    #phone_2.disconnect_the_call()
    
    #phone_2.press_key('ProgramKey1')    # DND on
    #print("TopSoftkey1: ")
    #print(phone_2.verify_led_state('Line1', 'on', 'Red'))
    #print(phone_2.verify_led_state('Line1', 'on'))

    #print("Topsoftkey2")
    #print(phone_2.verify_led_state('Line2', 'on', 'red'))
    #print(phone_2.verify_led_state('Line2', 'on', 'Red'))
    #print(phone_2.verify_led_state('Line2', 'on', 'RED'))
    #print(phone_2.verify_led_state('Line2', 'on'))

    #print("Topsoftkey3")
    #print(phone_2.verify_led_state('Line3', 'on', 'red'))
    #print(phone_2.verify_led_state('Line3', 'on', 'Red'))
    #print(phone_2.verify_led_state('Line3', 'on', 'RED'))
    #print(phone_2.verify_led_state('Line3', 'on'))
    #phone_2.press_key('ProgramKey1')    # DND off
    
    # DTP 49074
    #phone_2 = PhoneInterface({"phoneModel": "Mitel6930", "ipAddress": "10.112.123.43", "extensionNumber": "4165142502",
    #                          "phoneName": "robot1"})
    #phone_1 = PhoneInterface({"phoneModel": "Mitel6920", "ipAddress": "10.112.123.206", "extensionNumber": "4165142501",
    #                          "phoneName": "robot2"}) 
    #phone_1.clear_rtp_traces()
    #phone_2.clear_rtp_traces()
    #phone_1.call_extension(phone_2.phone_obj.phone)
    #time.sleep(5)
    #phone_2.press_key("HandsFree")
    #time.sleep(15)
    #import pdb, sys; pdb.Pdb(stdout=sys.__stdout__).set_trace()
    #rtp1 = phone_1.get_rtp_messages()
    #rtp2 = phone_2.get_rtp_messages()
    #print(rtp1)
    #print(rtp2)
    #print(len(rtp1))
    #print(len(rtp2))
    #import pdb, sys; pdb.Pdb(stdout=sys.__stdout__).set_trace()
    #phone_2.disconnect_the_call()
    #6970   10.211.43.173
    #phone_1 = PhoneInterface({"phoneModel": "Mitel6930", "ipAddress": "10.112.123.21", "extensionNumber": "4165142503",
    #                          "phoneName": "robot1"})

    #import pdb, sys; pdb.Pdb(stdout=sys.__stdout__).set_trace()
    #print(phone_1.verify_display_on_screen("Fri"))
    #print(phone_1.verify_display_on_screen("am"))
    
    
    # 6940  
    #phone_1 = PhoneInterface({"phoneModel": "Mitel6940", "ipAddress": "10.112.123.40", "extensionNumber": "4011",
    #                          "phoneName": "robot1"})
    #for _ in range(15):
    #    print(phone_1.verify_display_on_screen("Fri"))
    #    print(phone_1.verify_display_on_screen("pm"))
    #phone_1.select_page_in_moresoftkeys_pages("Page2")
    #import pdb, sys; pdb.Pdb(stdout=sys.__stdout__).set_trace()
    #phone_1.press_key("Menu")
    #time.sleep(2)
    #phone_1.change_options_menu_page("Page2")
    #time.sleep(1)
    #phone_1.select_option_on_options_menu("WIFI")
    #import pdb, sys; pdb.Pdb(stdout=sys.__stdout__).set_trace()
    
    
    # ENTA 4371
    #phone_1.press_key("CallersList")
    #phone_1.press_key("ScrollRight")

    #print("HTProp at phone are %s" % (phone_1.get_highlighted_text_properties()))
    #import pdb, sys; pdb.Pdb(stdout=sys.__stdout__).set_trace()
    #phone_1.press_key("Menu")
    #phone_1.press_key("ScrollRight")
    #phone_1.press_key("ScrollRight")
    #phone_1.press_key("ScrollDown")
    #phone_1.press_key("ScrollDown")
    #phone_1.press_key("Enter")
    #phone_1.press_key("ScrollDown")
    #phone_1.press_key("BottomKey1")
    #phone_1.press_key("BottomKey4")   
    
    
    # LED issue and ringer state
    #phone_2 = PhoneInterface({"phoneModel": "Mitel6867i", "ipAddress": "10.112.123.30", "extensionNumber": "4165142504",
    #                      "phoneName": "yo2"})
    #phone_1 = PhoneInterface({"phoneModel": "Mitel6930", "ipAddress": "10.112.123.45", "extensionNumber": "4165142501",
    #                     "phoneName": "robot1"})

    #print(phone_2.phone_obj.verify_ringer_state('Off'))
    #phone_1.call_extension(phone_2.phone_obj.phone)
    #import pdb, sys; pdb.Pdb(stdout=sys.__stdout__).set_trace()
    #time.sleep(5)
    #print(phone_1.verify_led_state('Line1', 'on'))
    #print(phone_2.verify_led_state('Line1', 'blink'))
    #print(phone_2.phone_obj.verify_ringer_state('Off'))
    #print(phone_2.phone_obj.verify_ringer_state('Ringing'))
    #print(phone_1.phone_obj.verify_ringer_state('Ringing'))
    #phone_2.press_key("HandsFree")
    #time.sleep(10)
    #import pdb, sys; pdb.Pdb(stdout=sys.__stdout__).set_trace()
    #phone_2.disconnect_the_call()
    
    
    #ENTA Audio issue 6865i
    #phone_1 = PhoneInterface(
    #                {"phoneModel": "Mitel6930", "ipAddress": "10.112.123.46", "extensionNumber": "4011", "phoneName": "robot1"}
    #                )
    #phone_2 = PhoneInterface(
    #                {"phoneModel": "Mitel6930", "ipAddress": "10.112.123.67", "extensionNumber": "4013", "phoneName": "robot2"}
    #                )
    #import pdb, sys; pdb.Pdb(stdout=sys.__stdout__).set_trace()
    

    #phone_1.call_extension(phone_2.phone_obj.phone)
    #time.sleep(5)
    #phone_2.press_key("HandsFree")
    #time.sleep(5)
    #phone_1.press_key("HandsFree")
    #time.sleep(5)
    #phone_1.check_two_way_audio(phone_2)
    #phone_2.disconnect_the_call()
    #print("Tone at phone is %s"%(phone_1.get_tone_at_phone()))
    #import pdb, sys; pdb.Pdb(stdout=sys.__stdout__).set_trace()
         
    # ENTA 5047
    #print(phone_2.verify_display_on_screen("Tue"))
    #print("first")
    #print(phone_2.verify_display_on_screen("Dial"))
    #print("SECOND ****************")
    #print(phone_2.verify_display_on_screen("Tue"))
    #print("THIRD #########")
         
         
         
    # Verify background Image
    # print(phone_2.is_background_image_set())
    # Verify brightness level
    # phone_2.input_a_number(phone_2.phone_obj.phone_info["extensionNumber"])
    # change and get brightness
    #phone_2.press_key("Menu")
    #phone_2.press_key("ScrollRight")
    #phone_2.press_key("ScrollRight")
    #phone_2.press_key("ScrollRight")
    #phone_2.press_key("Enter")
    #phone_2.press_key("ScrollDown")
    #phone_2.press_key("ScrollDown")
    #phone_2.press_key("ScrollLeft")
    #phone_2.press_key("BottomKey1")
    #time.sleep(15)
    #print("Brightness is %s"%phone_2.get_phone_brightness())
    #print("SS is %s" % phone_2.get_phone_screensaver())
    #print("Tone at phone is %s"%(phone_1.get_tone_at_phone()))
    #phone_1.press_key("CallersList")
    #phone_1.press_key("ScrollRight")
    #time.sleep(5)
    #print("HTProp at phone are %s" % (phone_1.get_highlighted_text_properties()))
    #print("MT at phone are %s" % (phone_1.get_menu_text_properties()))
    #print("FTP at phone are %s" % (phone_1.get_formatted_text_properties()))


    #print(phone_1.get_icons()) # To return all the icons
    # print(phone_1.get_icons(IconColour = "WHITE",IconIndex="2")) # can keep filters to validate.

    # Ringer
    # phone_1.call_extension(phone_2.phone_obj.phone)
    # time.sleep(3)
    # print(phone_2.phone_obj.verify_ringer_state("Ringing"))
    # print(phone_2.phone_obj.verify_ringer_state("Ringing",RingerVolume="2"))
    # phone_1.disconnect_the_call()
    # print(phone_2.phone_obj.verify_ringer_state("Off") # For 'Off', all other kwargs are invalid.)

    # VOICE_MAIL_SAVED, VOICE_MAIL_DELETED, VOICE_MAIL_INBOX,VOICE_MAIL_PAUSE, VOICE_MAIL_PLAY
    # phone_1.press_key('VoiceMail')
    # time.sleep(2)
    # phone_1.input_a_number("4321")
    # phone_1.press_key('BottomKey1')
    # time.sleep(5)
    # print(phone_1.verify_voice_mail_window_icons('VOICE_MAIL_INBOX', '59'))
    # phone_1.press_key('ScrollDown')
    # time.sleep(2)
    # print(phone_1.verify_voice_mail_window_icons('VOICE_MAIL_SAVED',''))
    # phone_1.press_key('ScrollDown')
    # time.sleep(2)
    # print(phone_1.verify_voice_mail_window_icons('VOICE_MAIL_DELETED',''))


    # Call History Icon Available from FW 5.2.1.1057

    # phone_1.press_key('CallersList')
    # time.sleep(3)
    # print(phone_1.verify_call_history_icon('CALL_HISTORY_INCOMING_RECEIVED'))
    # phone_1.press_key('ScrollUp')
    # time.sleep(2)
    # print(phone_1.verify_call_history_icon('CALL_HISTORY_OUTGOING'))
    # phone_1.press_key('ScrollUp')
    # time.sleep(2)
    # print(phone_1.verify_call_history_icon('CALL_HISTORY_MISSED'))
    # phone_1.press_key('ScrollUp')
    # time.sleep(2)
    # print(phone_1.verify_call_history_icon('CALL_HISTORY_ALL'))


    # MOH Verifications
    # Please pick 'MOH_200Hz_HF.wav'/ 'MOH_50Hz_HF.wav' / 'MOH_150Hz_HF.wav'/'MOH_250Hz_HF.wav' file from \\Framework\phone_wrappers\audio_analysis\ and upload into the system and make as MOH file.
    # fo = D2API("10.211.41.103:5478", "admin", "Connect@12")
    # fo.create_modify_user_groups(user_group_name='Executives',file_to_select='MOH_250')
    # phone_1.call_extension(phone_2.phone_obj.phone)
    # time.sleep(3)
    # phone_2.answer_the_call()
    #
    # phone_2.press_hold()
    # print(phone_1.check_audio_on_hold(250) # change this frequency as per the file)

    # ICON Available from FW 5.2.1.1035
    # <lineNumber>    :Range from 1 to 12 which will tell on which line any icon is created.for example, 6930 has 12 lines (by default).
    # <state>         :Here which type of icon is associated. Ref: 'Table 19: Phone Icon Id in ATAP doc'

    # phone_2.call_extension(phone_1.phone_obj.phone)
    # time.sleep(3)
    # print(phone_1.verify_line_icon_state('1', 'CALL_APPEARANCE_IDLE'))
    # print(phone_1.verify_line_icon_state('2', 'CALL_APPEARANCE_IDLE'))
    # print(phone_1.verify_line_icon_state('3', 'CALL_APPEARANCE_IDLE'))
    # print(phone_1.verify_line_icon_state('1', 'CALL_APPEARANCE_IDLE'))
    # print(phone_1.verify_line_icon_state('2', 'PB_HOTLINE'))
    # print(phone_1.verify_line_icon_state('3', 'CALL_APPEARANCE_IDLE'))
    # phone_1.press_key("BottomKey4")
    # print(phone_1.verify_state_icon('Vacation') ## State button should be pressed at least once after connection.)
    # phone_1.press_key("GoodBye")
    # phone_1.press_key("HandsFree")
    # print(phone_1.verify_led_state('speaker', 'on','RED',10))
    # print(phone_1.verify_line_icon_state('1', 'CALL_APPEARANCE_ACTIVE'))
    # print(phone_1.verify_line_icon_state('2', 'CALL_APPEARANCE_IDLE'))
    # print(phone_1.verify_line_icon_state('3', 'CALL_APPEARANCE_IDLE'))
    # phone_1.press_key("GoodBye")
    # LED Color

    # phone_1.press_key("HandsFree")
    # print(phone_1.verify_led_state('speaker', 'on','RED',10))
    # phone_1.press_key("GoodBye")
    # print(phone_1.verify_led_state('speaker', 'off',10))


     #Conference
    # phone_2.verify_notifications_in_ring()
    # phone_2.answer_call()
    # phone_1.check_two_way_audio(phone_2)
    # phone_2.disconnect_terminal()
    # phone_1.disconnect_terminal()
    # phone_2.press_key("BottomKey2")
    # phone_2.input_a_number(phone_3.phone_obj.phone.extensionNumber)
    # phone_2.press_key("BottomKey1")
    # phone_3.verify_notifications_in_ring()
    # phone_3.answer_call()
    # phone_2.press_key("BottomKey2")
    # phone_1.check_audio_in_three_party_conference_call(phone_2,phone_3)
    #
    #

    #ENTA-3270
    # phone_2.press_key('DecreaseVolume',2)
    #
    # phone_1.call_extension(phone_2.phone_obj.phone)
    # time.sleep(3)
    # phone_2.answer_the_call()
    # phone_1.check_two_way_audio(phone_2)
    # phone_2.press_key('OffHook')
    # phone_2.input_a_number("162")
    # phone_1.verify_notifications_in_ring()
    # time.sleep(3)
    # # phone_1.press_key('OffHook')
    # # time.sleep(3)
    # phone_1.answer_call()
    #
    # print(phone_1.get_line_buffer())
    # phone_2.verify_display_message_contents("fdfdfdfdf")
    #phone_2.disconnect_the_call()
    #phone_2.verify_display_message_contents("120")

    # d2 = D2API("10.211.41.103", "admin", "Mitel@123")
    # d2.configure_prog_button(user_extension ="196",button_box =0,soft_key =8,function="Barge In",label ="YYYYYYYY",target_extension ='161')

    # phone_1.phone_obj.verify_in_displayBanner("")
    # phone_1.phone_obj.verify_in_FoxKeys("")
    #
    # time.sleep(5)
    # phone_1.phone_obj.verify_in_ProgrammableKeys("")
    # # phone_1.phone_obj.verify_in_displayBanner("")
    # phone_1.phone_obj.verify_in_FoxKeys("")
    # phone_1.phone_obj.verify_in_ContentScreen("")
    # print(phone_2.verify_display_message_contents("Dwedsial"))
    # ENTA-3185
    # phone_2.input_a_number("1")
    # phone_2.verify_display_message_contents("Dials")
    # phone_2.input_a_number("2")
    # phone_2.verify_display_message_contents("Cancel")
    # phone_2.input_a_number("3")
    # phone_2.verify_display_message_contents("Dial")
    # phone_2.input_a_number("4")
    # phone_2.verify_display_message_contents("Cancel")

    # phone_2.press_key("Menu")
    # time.sleep(1)
    # phone_2.press_key("BottomKey3")
    # phone_2.call_extension(phone_3.phone_obj.phone)
    # time.sleep(3)
    # phone_3.answer_the_call()
    # time.sleep(3)
    # phone_3.verify_display_message_contents("121")
    # phone_3.disconnect_the_call()
    # time.sleep(3)
    # phone_2.verify_display_message_contents("Logging Is2sue")
    # phone_2.press_key("Hold")
    # phone_1.check_audio_is_on_hold()
    # ENTA-3185
    #phone_1.call_extension(phone_2.phone_obj.phone)
    #time.sleep(3)
    #phone_2.answer_the_call()
    #phone_1.press_key("Hold")
    #time.sleep(3)
    #phone_1.check_no_audio(phone_2)
    #phone_2.check_no_audio(phone_1)

    #phone_1.print_total_phones()

    # press special key
    # phone_1.dial_service_code("*") # input and dial
    # phone_1.input_a_number("*")  # only input


    # LED and LINE state
    # phone_1.call_extension(phone_2.phone_obj.phone)
    # time.sleep(2)
    # phone_2.answer_the_call()
    # time.sleep(16)
    # phone_1.press_key("Mute")
    # time.sleep(2)
    # print(phone_1.get_led_buffer())
    # print(phone_2.get_led_buffer())
    # checking message waiting('57') for blinking('15')
    # print(phone_1.verify_led_state('39', 'F', 10))
    # print(phone_1.verify_led_state('Line1', 'on', 10))
    # print(phone_2.verify_led_state('Line1', 'blink', 10))
    # print(phone_2.verify_led_state('Line1', 'blink', 10))
    # print(phone_2.verify_led_state('message_waiting', 'blink', 10))
    # print(phone_1.verify_led_state('mute', 'blink', 10))
    # print(phone_2.verify_led_state('mute', 'off', 10))
    # print(phone_1.verify_led_state('Line2', 'off', 10))
    # print(phone_2.verify_led_state('Line3', 'off', 10))
    # print(phone_1.verify_led_state('1D', '1', 10))
    # phone_1.set_to_idle()
    # phone_1.verify_line_notificaion_when_in_idle()
    # print(phone_1.verify_led_state('Function1', 'off', 10))
    # print(phone_1.verify_line_state(8))
    # print(phone_1.verify_line_state("incoming"))
    # print(phone_1.get_led_buffer())

    # phone_1.call_extension(phone_2.phone_obj.phone)
    # time.sleep(5)
    # phone_2.answer_the_call()
    # time.sleep(6)
    # print(phone_1.get_line_buffer())
    # print(phone_2.get_line_buffer())
    # print(phone_1.verify_line_state(4))
    # print(phone_1.verify_line_state(5))
    # print(phone_2.verify_line_state("incoming"))
    # print(phone_2.verify_line_state("incoming","2"))
    # pass

    # making and answering a call
    # phone_1.call_extension(phone_2.phone_obj.phone)
    # phone_2.verify_notifications_in_ring()
    # phone_2.answer_the_call()
    # phone_2.press_offhook()
    # phone_2.verify_phone_display(phone_1.phone_obj.phone.extensionNumber)
    # time.sleep(5)
    # phone_2.disconnect_the_call()

    # press programmable key
    # phone_2.press_key("ProgramKey12")
    # phone_2.press_expansion_box_key("ProgramKey1")

    # get display output
    # when in connected
    # phone_1.call_extension(phone_2.phone_obj.phone)
    # time.sleep(5)
    # phone_2.answer_the_call()
    # time.sleep(2)
    # phone_1.press_key("Directory")
    # print(phone_1.get_phone_display())
    # phone_2.press_key("CallersList")
    # time.sleep(2)
    # print(phone_2.get_phone_display())
    # new method
    # phone_1.input_a_number("1")
    # print(phone_1.verify_display_on_screen("Dial"))
    # phone_1.input_a_number("2")
    # print(phone_1.verify_display_on_screen("Dial"))
    # phone_1.input_a_number("3")
    # phone_1.input_a_number("3")
    # phone_2.input_a_number("3")
    # phone_1.press_key("Enter")
    # phone_2.press_key("Enter")
    # time.sleep(2)
    # print(phone_1.get_led_buffer())
    # print(phone_2.get_led_buffer())

    # phone_1.press_key("VoiceMail")
    # phone_1.input_a_number("654321")
    # print(phone_1.verify_display_on_screen("***"))
    # phone_1.press_key("BottomKey1")
    # time.sleep(5)
    # print(phone_1.verify_display_on_screen("Voicemail"))
    # print(phone_1.verify_display_on_screen("Call VM"))

    # phone_2.press_key("VoiceMail")
    # phone_2.input_a_number("1234")
    # phone_2.press_key("BottomKey1")
    # time.sleep(5)
    # phone_2.press_key("ScrollRight")
    # time.sleep(2)
    # phone_2.press_key("BottomKey5")
    # time.sleep(2)
    # phone_2.press_key("BottomKey2")
    # time.sleep(2)
    # phone_2.press_key("BottomKey5")
    # print(phone_2.verify_display_on_screen("Inbox"))
    # print(phone_2.verify_display_on_screen("Saved"))
    # print(phone_2.verify_display_on_screen("Deleted"))
    # old method
    #phone_1.input_a_number("1")
    # print(phone_1.verify_display_message_contents("Dial"))
    ##phone_1.input_a_number("2")
    #print(phone_1.verify_display_message_contents("Dial"))
    #phone_1.input_a_number("3")
    #print(phone_1.verify_display_message_contents("Dial"))
    # time.sleep(2)
    # phone_1.press_key("DecreaseVolume")
    # print(phone_1.get_led_buffer())
    # print(phone_1.verify_led_state('Line1', 'on', 10))

    # print(phone_2.verify_phone_display("Today"))

    # when in idle
    # print(phone_1.get_phone_display("idle"))
    # print(phone_2.get_phone_display("idle"))

    # audio path verification
    #phone_2 = PhoneInterface({"phoneModel": "Mitel6920", "ipAddress": "10.211.41.236", "extensionNumber": "121", "phoneName": "yo2","hq_rsa": "hq.rsa"})
    #phone_1 = PhoneInterface({"phoneModel": "Mitel6940", "ipAddress": "10.211.41.229", "extensionNumber": "120", "phoneName": "yo2","hq_rsa": "hq.rsa"})
    #phone_3 = PhoneInterface({"phoneModel": "Mitel6930", "ipAddress": "10.211.41.238", "extensionNumber": "162", "phoneName": "yo2","hq_rsa": "hq.rsa"})
    #phone_4 = PhoneInterface({"phoneModel": "Mitel6910", "ipAddress": "10.211.41.245", "extensionNumber": "161", "phoneName": "yo2","hq_rsa": "hq.rsa"})
    #phone_1.update_devnull_permissions()
    #phone_2.update_devnull_permissions()
    #phone_1.upload_path_confirmation_files()
    #phone_2.upload_path_confirmation_files()
   # phone_1.call_extension(phone_2.phone_obj.phone)
   # time.sleep(3)
    #phone_2.answer_the_call()
    #phone_1.check_audio_is_on_hold(phone_2)
    #phone_2.press_offhook()
    #phone_1.press_offhook()
    #phone_1.press_handsfree()
    #phone_2.press_handsfree()
    # time.sleep(5)
    #phone_1.check_no_audio(phone_2)
   # phone_2.check_two_way_audio(phone_3)

    # sip messages
    # phone_1.clear_sip_traces()
    # phone_2.clear_sip_traces()
    # phone_1.call_extension(phone_2.phone_obj.phone)
    # time.sleep(5)
    # phone_2.answer_the_call()
    # time.sleep(2)
    # print(phone_1.get_sip_in_messages())
    # print(phone_1.get_sip_out_messages())
    # print(phone_2.get_sip_in_messages())
    # print(phone_2.get_sip_out_messages())

    # reboot the phone
    # print(phone_1.get_firmware_version())
    # print(phone_1.get_library_version())
    # phone_1.reboot_terminal()

    # ENTA-3268
   #  phone_2 = PhoneInterface({"phoneModel": "Mitel6920", "ipAddress": "10.211.41.236", "extensionNumber": "121", "phoneName": "yo2","hq_rsa": "hq.rsa"})
   #  phone_2 = PhoneInterface({"phoneModel": "Mitel6920", "ipAddress": "10.112.95.12", "extensionNumber": "4013", "phoneName": "yo2","hq_rsa": "hq.rsa"})
   #  phone_2.press_key("CallersList")
   #  phone_2.sleep(8)
   #  phone_2.press_key("ScrollRight")
   #  phone_2.sleep(5)
   # print(phone_2.verify_display_message_contents("Dial"))
   # print(phone_2.verify_display_message_contents("Delete"))
   #  print(phone_2.verify_display_message_contents("Details"))
   #  print(phone_2.verify_display_message_contents("Quit"))

    #ENTA-3272

    #print(phone_1.verify_display_message_contents("121"))
    #print(phone_2.verify_display_message_contents("120"))
    #print(phone_3.verify_display_message_contents("162"))
    #print(phone_4.verify_display_message_contents("1621"))
