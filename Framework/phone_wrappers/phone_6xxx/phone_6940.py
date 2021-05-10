"""
Interface to mitel and/or shoretel pphones
"""
__author__ = "milton.villeda@mitel.com"

import sys
from mitel_phone_base import Phone6xxxInterface

from robot.api import logger

class PhoneInterface6940(Phone6xxxInterface):

    def __init__(self, phone_info):
        """
        It is mandatory to call pphone_sanity_check immediately to create the phone objects for mitel phones
        :param args:
        """
        logger.info("In Mitel 6940 Phone class")
        Phone6xxxInterface.__init__(self, phone_info)

    # def phone_sanity_check(self):
    #     """
    #
    #     This method ...
    #     Args:
    #
    #     """
    #     logger.info("6940 phone_sanity_check")
    #
    # def log_off(self):
    #     """
    #
    #     This method ...
    #     Args:
    #
    #     """
    #     try:
    #         self.atap_dll.logOff()
    #     except Exception as err:
    #         fn = sys._getframe().f_code.co_name
    #         raise Exception('func "%s" - err: "%s"!' % (fn, err))
    #
    # def call_back_from_caller_list(self):
    #     """
    #
    #     This method ...
    #     Args:
    #
    #     """
    #     try:
    #         self.atap_dll.callBackFromCallerList()
    #     except Exception as err:
    #         fn = sys._getframe().f_code.co_name
    #         raise Exception('func "%s" - err: "%s"!' % (fn, err))
    #
    # def verify_led_notificaion_when_follow_me_activated(self):
    #     """
    #
    #     This method ...
    #     Args:
    #
    #     """
    #     try:
    #         self.atap_dll.verifyLEDNotificaionWhenFollowMeActivated()
    #     except Exception as err:
    #         fn = sys._getframe().f_code.co_name
    #         raise Exception('func "%s" - err: "%s"!' % (fn, err))
    #
    # def verify_led_notificaion_when_diversion_activated(self):
    #     """
    #
    #     This method ...
    #     Args:
    #
    #     """
    #     try:
    #         self.atap_dll.verifyLEDNotificaionWhenDiversionActivated()
    #     except Exception as err:
    #         fn = sys._getframe().f_code.co_name
    #         raise Exception('func "%s" - err: "%s"!' % (fn, err))
    #
    # def verify_led_notificaion_when_diversion_de_activated(self):
    #     """
    #
    #     This method ...
    #     Args:
    #
    #     """
    #     try:
    #         self.atap_dll.verifyLEDNotificaionWhenDiversionDeActivated()
    #     except Exception as err:
    #         fn = sys._getframe().f_code.co_name
    #         raise Exception('func "%s" - err: "%s"!' % (fn, err))
    #
    # def de_activate_follow_me(self):
    #     """
    #
    #     This method ...
    #     Args:
    #
    #     """
    #     try:
    #         self.atap_dll.deActivateFollowMe()
    #     except Exception as err:
    #         fn = sys._getframe().f_code.co_name
    #         raise Exception('func "%s" - err: "%s"!' % (fn, err))
    #
    # def disable_diversion(self):
    #     """
    #
    #     This method ...
    #     Args:
    #
    #     """
    #     try:
    #         self.atap_dll.disableDiversion()
    #     except Exception as err:
    #         fn = sys._getframe().f_code.co_name
    #         raise Exception('func "%s" - err: "%s"!' % (fn, err))
    #
    # def transfer_internal_call_directly(self, extension_number_to_transfer_the_call):
    #     """
    #
    #     This method ...
    #     Args:
    #         extension_number_to_transfer_the_call: HardPhone
    #
    #     """
    #     try:
    #         self.atap_dll.transferInternalCallDirectly(extension_number_to_transfer_the_call)
    #     except Exception as err:
    #         fn = sys._getframe().f_code.co_name
    #         raise Exception('func "%s" - err: "%s"!' % (fn, err))
    #
    # def transfer_internal_call_after_answering(self, park_pool_number):
    #     """
    #
    #     This method ...
    #     Args:
    #         park_pool_number: string
    #
    #     """
    #     try:
    #         self.atap_dll.transferInternalCallAfterAnswering(park_pool_number)
    #     except Exception as err:
    #         fn = sys._getframe().f_code.co_name
    #         raise Exception('func "%s" - err: "%s"!' % (fn, err))
    #
    # def transfer_internal_call_after_answering(self, extension_to_transfer_the_call):
    #     """
    #
    #     This method ...
    #     Args:
    #         extension_to_transfer_the_call: HardPhone
    #
    #     """
    #     try:
    #         self.atap_dll.transferInternalCallAfterAnswering(extension_to_transfer_the_call)
    #     except Exception as err:
    #         fn = sys._getframe().f_code.co_name
    #         raise Exception('func "%s" - err: "%s"!' % (fn, err))
    #
    # def transfer_internal_call_directly(self, park_pool_number):
    #     """
    #
    #     This method ...
    #     Args:
    #         park_pool_number: string
    #
    #     """
    #     try:
    #         self.atap_dll.transferInternalCallDirectly(park_pool_number)
    #     except Exception as err:
    #         fn = sys._getframe().f_code.co_name
    #         raise Exception('func "%s" - err: "%s"!' % (fn, err))
    #
    # def enable_direct_diversion(self):
    #     """
    #
    #     This method ...
    #     Args:
    #
    #     """
    #     try:
    #         self.atap_dll.enableDirectDiversion()
    #     except Exception as err:
    #         fn = sys._getframe().f_code.co_name
    #         raise Exception('func "%s" - err: "%s"!' % (fn, err))
    #
    # def enable_diversion_on_no_answer(self):
    #     """
    #
    #     This method ...
    #     Args:
    #
    #     """
    #     try:
    #         self.atap_dll.enableDiversionOnNoAnswer()
    #     except Exception as err:
    #         fn = sys._getframe().f_code.co_name
    #         raise Exception('func "%s" - err: "%s"!' % (fn, err))
    #
    # def enable_diversion_on_busy(self):
    #     """
    #
    #     This method ...
    #     Args:
    #
    #     """
    #     try:
    #         self.atap_dll.enableDiversionOnBusy()
    #     except Exception as err:
    #         fn = sys._getframe().f_code.co_name
    #         raise Exception('func "%s" - err: "%s"!' % (fn, err))
    #
    # def activate_call_back(self):
    #     """
    #
    #     This method ...
    #     Args:
    #
    #     """
    #     try:
    #         self.atap_dll.activateCallBack()
    #     except Exception as err:
    #         fn = sys._getframe().f_code.co_name
    #         raise Exception('func "%s" - err: "%s"!' % (fn, err))
    #
    # def activate_call_back_at_no_answer(self):
    #     """
    #
    #     This method ...
    #     Args:
    #
    #     """
    #     try:
    #         self.atap_dll.activateCallBackAtNoAnswer()
    #     except Exception as err:
    #         fn = sys._getframe().f_code.co_name
    #         raise Exception('func "%s" - err: "%s"!' % (fn, err))
    #
    # def activate_ic_sdiversion_with_menu_system(self, diversion_category):
    #     """
    #
    #     This method ...
    #     Args:
    #         diversion_category: int
    #
    #     """
    #     try:
    #         self.atap_dll.activateICSdiversionWithMenuSystem(diversion_category)
    #     except Exception as err:
    #         fn = sys._getframe().f_code.co_name
    #         raise Exception('func "%s" - err: "%s"!' % (fn, err))
    #
    # def select_call_list_profile_through_menu(self, profile_number):
    #     """
    #
    #     This method ...
    #     Args:
    #         profile_number: int
    #
    #     """
    #     try:
    #         self.atap_dll.selectCallListProfileThroughMenu(profile_number)
    #     except Exception as err:
    #         fn = sys._getframe().f_code.co_name
    #         raise Exception('func "%s" - err: "%s"!' % (fn, err))
    #
    # def activate_do_not_disturb(self):
    #     """
    #
    #     This method ...
    #     Args:
    #
    #     """
    #     try:
    #         self.atap_dll.activateDoNotDisturb()
    #     except Exception as err:
    #         fn = sys._getframe().f_code.co_name
    #         raise Exception('func "%s" - err: "%s"!' % (fn, err))
    #
    # def de_activate_do_not_disturb(self):
    #     """
    #
    #     This method ...
    #     Args:
    #
    #     """
    #     try:
    #         self.atap_dll.deActivateDoNotDisturb()
    #     except Exception as err:
    #         fn = sys._getframe().f_code.co_name
    #         raise Exception('func "%s" - err: "%s"!' % (fn, err))
    #
    # def verify_led_notificaion_when_do_not_disturb_activated(self):
    #     """
    #
    #     This method ...
    #     Args:
    #
    #     """
    #     try:
    #         self.atap_dll.verifyLEDNotificaionWhenDoNotDisturbActivated()
    #     except Exception as err:
    #         fn = sys._getframe().f_code.co_name
    #         raise Exception('func "%s" - err: "%s"!' % (fn, err))
    #
    # def activate_follow_me(self, in_attend_number):
    #     """
    #
    #     This method ...
    #     Args:
    #         in_attend_number: string
    #
    #     """
    #     try:
    #         self.atap_dll.activateFollowMe(in_attend_number)
    #     except Exception as err:
    #         fn = sys._getframe().f_code.co_name
    #         raise Exception('func "%s" - err: "%s"!' % (fn, err))
    #
