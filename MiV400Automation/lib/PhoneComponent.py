#!/usr/bin/python
# -*- coding: UTF-8 -*-

import sys
import os
import re
import requests
import yaml
import pysftp
import csv
import time
import var_pbx
from urllib3 import *
from urllib3.exceptions import InsecureRequestWarning
from requests import ConnectionError
from requests.packages.urllib3.exceptions import InsecureRequestWarning

boss_path = os.path.dirname(os.path.dirname(__file__))
framework_path = os.path.join(os.path.dirname((os.path.dirname(os.path.dirname(__file__)))), "Framework")
#framework_path = os.path.join(os.path.dirname((os.path.dirname(__file__))), "Framework")
sys.path.append(os.path.join(framework_path, "phone_wrappers"))

from PhoneInterface import PhoneInterface
from robot.api.logger import console
from robot.api import logger
from Var import *

from selenium import webdriver
from selenium.webdriver.common.by import By

func_param_dict = {}
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
disable_warnings(InsecureRequestWarning)



class PhoneComponent(object):
    ROBOT_LIBRARY_SCOPE = 'GLOBAL'

    def __init__(self, **params):
        startTime = time.time()
        self.phone_obj = PhoneInterface(params)
        logger.info("Took {:.2f} seconds to initialize {} model with extension {}.".format((time.time() - startTime)
                    , params['phoneModel'], params['extensionNumber']), also_console=True)

    def makeCall(self, **kwargs):
        """
        This method makes a two party call either by pressing loudspeaker or off hook or any of the line keys.

        Keyword Args:
            phoneObj: the phone to be dialed
            dialingMode: the dialing mode for the call i.e., LoudSpeaker/Off hook/ Line keys

        :returns: None
        :created by: Manoj Karakoti
        :creation date: 17/12/2018
        :last update by: Vikhyat Sharma
        :last update date: 01/02/2021
        """
        if len(kwargs) > 1:
            phoneObj = kwargs['phoneObj']
            dialingMode = str(kwargs['dialingMode'])
        else:
            raise Exception("LESS NUMBER OF ARGUMENTS PASSED!!")

        logger.info("Making call from extension <b>" + self.phone_obj.phone_obj.phone.extensionNumber
                    + "</b> to <b>" + phoneObj.phone_obj.phone_obj.phone.extensionNumber
                    + "</b> using <b>" + dialingMode + "</b>.", html=True)
        console("Making call from extension " + self.phone_obj.phone_obj.phone.extensionNumber
                + " to " + phoneObj.phone_obj.phone_obj.phone.extensionNumber
                + " using " + dialingMode)

        dialingNumber = phoneObj.phone_obj.phone_obj.phone.extensionNumber

        if dialingMode == "Loudspeaker":
            self.phone_obj.press_key("HandsFree")
            self.phone_obj.sleep(1)

        elif dialingMode == "OffHook":
            self.phone_obj.press_key("OffHook")
            self.phone_obj.sleep(3)

        elif "ProgramKey" in dialingMode:
            lineKey = "Line" + filter(str.isdigit, dialingMode)
            if self.phone_obj.phone_type in ["Mitel6867i", "Mitel6865i"]:
                if dialingMode == "ProgramKey1" or dialingMode == "ProgramKey2":
                    dialingMode = dialingMode.replace("ProgramKey", "Line")
            logger.info("Pressing " + dialingMode + " on extension: " + self.phone_obj.phone_obj.phone.extensionNumber)
            console("Pressing " + dialingMode + " on extension: " + self.phone_obj.phone_obj.phone.extensionNumber)
            self.phone_obj.press_key(dialingMode)
            self.phone_obj.sleep(3)
            self.verifyLedState(ledType=lineKey, ledMode='on')
            self.phone_obj.sleep(2)
        else:
            self.phone_obj.press_key(dialingMode)

        self.phone_obj.input_a_number(dialingNumber)
        self.phone_obj.sleep(2)
        self.pressSoftkeyInDialingState(softKey='Dial')
        self.phone_obj.sleep(3)
        self.verifyDisplayMessageUtil(phoneObj.phone_obj.phone_obj.phone.extensionNumber)
        self.phone_obj.sleep(3)

        if dialingMode == "Loudspeaker":
            self.verifyLedState(ledType='speaker', ledMode='on')
        else:
            self.verifyLedState(ledType='speaker', ledMode='off')

    def answerCall(self, **kwargs):
        """
        This method answers the incoming call on the phone by pressing speaker/softkey/LineN/offhook.

        Keyword Args:
            answerMode: Mode of answering a call

        :returns: None
        :created by: Manoj Karakoti
        :creation date: 17/12/2018
        :last update by: Vikhyat Sharma
        :last update date: 03/02/2021
        """

        answerMode = kwargs['answerMode']
        logger.info("Answering the call using <b>" + answerMode + "</b> on phone <b>%s</b>"
                    % self.phone_obj.phone_obj.phone.extensionNumber, html=True)
        console("Answering the call using " + answerMode + " on phone %s"
                % self.phone_obj.phone_obj.phone.extensionNumber)

        if answerMode == "Loudspeaker":
            self.phone_obj.press_key("HandsFree")
        elif answerMode == "Softkey" or answerMode == "SoftKey":
            if self.phone_obj.phone_type == 'Mitel6910':
                logger.warn("Mitel6910 model does not have softkeys. So answering the call using loudspeaker.")
                self.answerCall(answerMode='Loudspeaker')
            else:
                self.phone_obj.press_softkey(1)
        elif answerMode == "OffHook":
            self.phone_obj.press_key("OffHook")
        else:
            if "ProgramKey" in answerMode and self.phone_obj.phone_type in ("Mitel6865i", "Mitel6867i"):
                answerMode = answerMode.replace("ProgramKey", "Line")
            self.phone_obj.press_key(answerMode)
            self.phone_obj.press_key("HandsFree")
        self.phone_obj.sleep(4)

        if answerMode == "OffHook":
            self.verifyLedState(ledType='speaker', ledMode='off')
        else:
            self.verifyLedState(ledType='speaker', ledMode='on')

        if self.phone_obj.phone_type not in ["Mitel6910", "Mitel6865i"]:
            self.verifyDisplayMessageUtil("Drop")

        self.phone_obj.sleep(2)

    def pressLineKey(self, **kwargs):
        """
        This method is used to press the available Line keys on the phone.

        Keyword Args:
            lineKey: Line Key to press

        :returns: None
        :created by: Aman Bhardwaj
        :creation date: 17/12/2018
        :last update by: Milind Patil
        :last update date: 01/02/2021
        """

        if len(kwargs) >= 1:
            lineKey = kwargs['lineKey']
            logger.info("Pressing <b> " + lineKey + " </b> on "
                        + self.phone_obj.phone_obj.phone.extensionNumber, html=True)
            console("Pressing " + lineKey + " on "
                    + self.phone_obj.phone_obj.phone.extensionNumber)
            self.phone_obj.press_key(lineKey)
            self.phone_obj.sleep(2)
        else:
            raise Exception("Check the arguments passed !!!")

    def clearCall(self):
        """
        This method is used to clear the connected call on the phone.

        :param:
            :self: PhoneComponent object of the phone.
        :returns: None
        :created by: Gaurav Sharma
        :creation date:
        :last update by: Milind Patil
        :last update Date: 17/12/2020

        """
        logger.info("Clearing the call on extension: <b>" + self.phone_obj.phone_obj.phone.extensionNumber
                    + "</b>.", html=True)
        console("Clearing the call on extension: " + self.phone_obj.phone_obj.phone.extensionNumber)

        self.phone_obj.sleep(2)
        self.phone_obj.press_key("GoodBye")
        self.phone_obj.press_key("OnHook")

    def pressPhoneHook(self, **kwargs):
        """
        Below method hook state of the phone as off hook or on hook.

        :param
            :self: PhoneComponent object
            :kwargs: Dictionary for getting the arguments needed:
                    :phoneHookMode: Hook mode to change to i.e., OffHook/OnHook
        :returns: None
        :created by: Gaurav Sharma
        :creation date: 01/11/2019
        :last update by: Sharma
        :last update Date: 26/11/2019
        """

        hookMode = kwargs['phoneHookMode']
        logger.info("Pressing <b>" + hookMode + "</b> on extension: <b>"
                    + self.phone_obj.phone_obj.phone.extensionNumber + "</b>.", html=True)
        console("Pressing " + hookMode + " on extension: " + self.phone_obj.phone_obj.phone.extensionNumber)

        self.phone_obj.sleep(3)
        if hookMode == "OffHook":
            self.phone_obj.press_key("OffHook")
        elif hookMode == "OnHook":
            self.phone_obj.press_key("OnHook")
        else:
            logger.error("Check the arguments  passed %s" % kwargs)
            raise Exception("Check the arguments  passed %s" % kwargs)
        self.phone_obj.sleep(3)

    def pressSoftkeyInRingingState(self, **kwargs):
        """
        This method presses the available softkeys while the phone is in ringing state i.e., call is coming on the phone

        Keyword Args:
            softKey: softkey to press i.e., ToVM/Answer/Ignore/Transfer/ScrollUp

        :returns: None
        :created by:
        :creation date:
        :last update by: Ramkumar. G
        :last update date : 17/02/2021

        """
        softkey = kwargs["softKey"]

        logger.info("Pressing key: <b>" + softkey + "</b> on extension: <b>"
                    + self.phone_obj.phone_obj.phone.extensionNumber + "</b> while in Ringing State.", html=True)
        console("Pressing key: " + softkey + " on extension: " + self.phone_obj.phone_obj.phone.extensionNumber
                + " while in Ringing state.")

        if softkey == "ToVm":
            if self.phone_obj.phone_type == 'Mitel6910':
                self.phone_obj.input_a_number('#')
            else:
                self.phone_obj.press_softkey(3)

        elif softkey == "Answer":
            if self.phone_obj.phone_type in ('Mitel6865i', "Mitel6910"):
                self.phone_obj.press_key("HandsFree")
            else:
                self.phone_obj.press_softkey(1)

        elif (softkey == "Ignore"):
            self.phone_obj.press_softkey(2)

        elif (softkey == "Transfer"):
            if self.phone_obj.phone_type in ('Mitel6865i', "Mitel6910"):
                self.phone_obj.press_key("Transfer")
            else:
                self.phone_obj.press_softkey(2)

        elif (softkey == "ScrollUp"):
            self.phone_obj.press_softkey(3)

        elif (softkey == "Deflect"):
            if (self.phone_obj.phone_type == "Mitel6865i"):
                self.phone_obj.press_key("Transfer")
            else:
                self.phone_obj.press_softkey(3) 
                self.phone_obj.sleep(3)

        elif (softkey == "Deflect_number"):
            self.phone_obj.press_softkey(1)  
            self.phone_obj.sleep(3)


        else:
            logger.info("Please check the softkey passed %s" % softkey)

    def pressSoftkeyInAnswerState(self, **kwargs):
        """
        This method is used to press the different softkeys available while the phone has active call.

        Keyword Args:
            softkey: Soft key which is need to press when call is running

        :returns: None
        :created by:
        :creation date:
        :last update by: Vikhyat Sharma
        :last update Date: 20/11/2020
        """
        softkey = kwargs["softKey"]
        pbx = kwargs['pbx']
        logger.info("Pressing key: <b>" + softkey + "</b> on extension: <b>"
                    + self.phone_obj.phone_obj.phone.extensionNumber + "</b> while in Answer State.", html=True)
        console("Pressing key: " + softkey + " on extension: " + self.phone_obj.phone_obj.phone.extensionNumber
                + " while in Answer call state.")

        if softkey == "Drop":
            if self.phone_obj.phone_type in ('Mitel6865i', "Mitel6910"):
                self.phone_obj.press_key("GoodBye")
            else:
                self.phone_obj.press_softkey(1)

        elif softkey == "Pickup":
            if self.phone_obj.phone_type in ["Mitel6910", "Mitel6865i"]:
                self.phone_obj.press_key("ScrollRight")
            else:
                self.phone_obj.press_softkey(1)

        elif softkey == "Conference":
            if self.phone_obj.phone_type in ('Mitel6865i', "Mitel6910"):
                self.phone_obj.press_key("Conference")
            else:
                self.phone_obj.press_softkey(2)

        elif softkey == "Transfer":
            if self.phone_obj.phone_type in ('Mitel6865i', "Mitel6910"):
                self.phone_obj.press_key("Transfer")
                self.phone_obj.verify_display_message_contents("Dial")
                if pbx in ('MiVoice', 'MiCloud'):
                    self.phone_obj.verify_display_message_contents("Bksp")
            else:
                if not self.phone_obj.verify_display_message_contents("Merge"):
                    self.phone_obj.press_softkey(3)
                else:
                    if (self.phone_obj.phone_type == "Mitel6920"):
                        self.phone_obj.press_softkey(4)
                        self.phone_obj.press_softkey(1)
                    else:
                        self.phone_obj.press_softkey(4)
                self.phone_obj.verify_display_message_contents("Transfer")

        elif (softkey == "Park"):
            self.phone_obj.sleep(2)
            if (self.phone_obj.phone_type == "Mitel6920"):
                if self.phone_obj.verify_display_message_contents("Merge"):
                    self.phone_obj.press_softkey(4)
                    self.phone_obj.press_softkey(2)
                else:
                    self.phone_obj.press_softkey(4)
                    self.phone_obj.press_softkey(1)
            else:
                if not self.phone_obj.verify_display_message_contents("Merge"):
                    self.phone_obj.press_softkey(4)
                else:
                    self.phone_obj.press_softkey(5)
                    self.phone_obj.press_softkey(1)

        elif (softkey == "Merge"):
            self.phone_obj.press_softkey(3)
            self.phone_obj.sleep(3)

        elif softkey in ('Lock', 'Unlock'):
            if self.phone_obj.verify_display_message_contents(softkey):
                self.phone_obj.press_softkey(3)
                if softkey == "Lock":
                    self.verifyDisplayMessageUtil("Unlock")
                else:
                    self.verifyDisplayMessageUtil("Lock")
            else:
                if self.phone_obj.phone_type == "Mitel6920":
                    self.phone_obj.press_softkey(4)
                    self.phone_obj.press_softkey(2)

                    self.phone_obj.press_softkey(4)
                    if softkey == "Lock":
                        self.verifyDisplayMessageUtil("Unlock")
                    else:
                        self.verifyDisplayMessageUtil("Lock")
                    self.phone_obj.press_softkey(4)
                    self.phone_obj.press_softkey(4)
                else:
                    self.phone_obj.press_softkey(5)
                    if softkey == "Lock":
                        self.verifyDisplayMessageUtil("Unlock")
                    else:
                        self.verifyDisplayMessageUtil("Lock")

        elif softkey == "Park Cancel":
            if (self.phone_obj.phone_type == "Mitel6920"):
                self.phone_obj.press_softkey(4)
                self.phone_obj.press_softkey(1)
            else:
                self.phone_obj.press_softkey(4)

        elif (softkey == "transferDrop"):
            if (self.phone_obj.phone_type == "Mitel6910"):
                self.phone_obj.press_key("ScrollRight")
            else:
                self.phone_obj.press_softkey(1)

        else:
            raise Exception("Please check the softkey passed %s" % softkey)

    def pressSoftkeyInConferenceCall(self, **kwargs):
        """
        This method is used to press the soft key when phone is in conference call.

        Keyword Args:
            softkey: soft key to be pressed in during Conference call
        :returns: None
        :created by:
        :creation date:
        :last update by: Sharma
        :last update date: 04/09/2020
        """

        softkey = kwargs["softKey"]
        logger.info("Pressing key: <b>" + softkey + "</b> on extension: <b>"
                    + self.phone_obj.phone_obj.phone.extensionNumber + "</b> while in Conference call State.",
                    html=True)
        console("Pressing key: " + softkey + " on extension: " + self.phone_obj.phone_obj.phone.extensionNumber
                + " while in Conference call state.")

        if (softkey == "Drop"):
            if self.phone_obj.phone_type in ("Mitel6910", "Mitel6865i"):
                self.phone_obj.press_key("GoodBye")
            else:
                self.phone_obj.press_softkey(1)

        elif softkey == "Consult":
            if self.phone_obj.phone_type in ("Mitel6910", "Mitel6865i"):
                self.phone_obj.press_key("ScrollRight")
            else:
                self.phone_obj.press_softkey(1)

        elif softkey == "Conference":
            if self.phone_obj.phone_type not in ("Mitel6910", "Mitel6865i"):
                self.phone_obj.press_softkey(2)
            else:
                mydict = {"key": kwargs["softKey"]}
                self.pressHardkey(**mydict)
                self.phone_obj.sleep(2)

        elif softkey == "Show":
            self.phone_obj.press_softkey(3)
            self.phone_obj.sleep(5)

        elif softkey == "Merge":
            self.phone_obj.press_softkey(3)
            self.phone_obj.sleep(3)

        elif softkey == "Leave":
            if self.phone_obj.phone_type in ('Mitel6865i', 'Mitel6910'):
                self.phone_obj.press_key('GoodBye')
            elif self.phone_obj.phone_type in ("Mitel6920", 'Mitel6867i'):
                self.phone_obj.press_softkey(4)
            elif self.phone_obj.phone_type == "Mitel6940":
                self.phone_obj.press_key("BottomKey6")
            else:
                self.phone_obj.press_softkey(5)

        elif softkey in ('Lock', 'Unlock'):
            if self.phone_obj.verify_display_message_contents('Show'):
                if self.phone_obj.phone_type == 'Mitel6920':
                    self.phone_obj.press_softkey(4)
                    self.phone_obj.press_softkey(2)

                    self.phone_obj.press_softkey(4)
                    if softkey == "Lock":
                        self.verifyDisplayMessageUtil('Unlock')
                    else:
                        self.verifyDisplayMessageUtil("Lock")
                    self.phone_obj.press_softkey(4)
                else:
                    self.phone_obj.press_softkey(4)
                    if softkey == "Lock":
                        self.verifyDisplayMessageUtil('Unlock')
                    else:
                        self.verifyDisplayMessageUtil("Lock")
            else:
                self.phone_obj.press_softkey(3)
                if softkey == "Lock":
                    self.verifyDisplayMessageUtil("Unlock")
                else:
                    self.verifyDisplayMessageUtil("Lock")

        elif (softkey == "Transfer"):
            if self.phone_obj.phone_type in ('Mitel6865i', "Mitel6910"):
                self.phone_obj.press_key("Transfer")
            else:
                self.phone_obj.press_softkey(3)
        else:
            raise Exception("Please check the softkey passed %s" % softkey)

    def directorySearch(self, **kwargs):
        """
        This method is used to search a number in directory
        """
        action = kwargs['action']
        self.phone_obj.press_key("Directory")
        self.phone_obj.sleep(4)
        if self.phone_obj.phone_type != "Mitel6910":
            self.phone_obj.press_key("DialPad4")
            self.phone_obj.press_softkey(2)
            self.phone_obj.press_softkey(2)
            self.phone_obj.press_softkey(1)
            self.phone_obj.dial_anumber(action.phone_obj.phone_obj.phone.extensionNumber)
            self.phone_obj.sleep(2)
            self.phone_obj.press_key("ScrollDown")
            self.phone_obj.sleep(2)

    def pressSoftkeyInDialingState(self, **kwargs):
        """
        This method is used to press any of the available softkeys while the phone is in dialing state.


        This state is when the phone is dialing the number. If a call is coming on the phone, use
        pressSoftkeyInRingingState method instead.

        Keyword Args:
            softKey: softkey to press i.e., Cancel/Backspace/Dial

        :returns: None
        :created by: Anuj Giri
        :last update by: Vikhyat Sharma
        :last update date: 11/01/2021
        """

        softkey = kwargs["softKey"]
        logger.info("Pressing key: <b>" + softkey + "</b> on extension: <b>"
                    + self.phone_obj.phone_obj.phone.extensionNumber + "</b> while in Dialing State.", html=True)
        console("Pressing key: " + softkey + " on extension: " + self.phone_obj.phone_obj.phone.extensionNumber
                + " while in Dialing state.")

        if softkey == "Cancel":
            if self.phone_obj.phone_type in ["Mitel6920", "Mitel6867i"]:
                self.phone_obj.press_softkey(4)
            elif self.phone_obj.phone_type == "Mitel6930":
                self.phone_obj.press_softkey(5)
            elif self.phone_obj.phone_type == "Mitel6940":
                self.phone_obj.press_key("BottomKey6")
            elif self.phone_obj.phone_type in ["Mitel6910", "Mitel6865i"]:
                self.phone_obj.press_key("ScrollLeft")

        elif softkey == "Backspace":
            if self.phone_obj.phone_type in ["Mitel6910", "Mitel6865i"]:
                self.phone_obj.press_key("ScrollLeft")
            else:
                self.phone_obj.press_softkey(2)

        elif softkey == "Dial" or softkey == "Submit":
            if self.phone_obj.phone_type in ["Mitel6910", "Mitel6865i"]:
                console("Scrolling Right on 6910")
                self.phone_obj.press_key("ScrollRight")
            else:
                self.phone_obj.press_softkey(1)
            self.phone_obj.sleep(1)

        elif softkey == "Transfer":
            if self.phone_obj.phone_type in ["Mitel6910", "Mitel6865i"]:
                self.phone_obj.press_key("ScrollRight")
            elif self.phone_obj.phone_type in ["Mitel6920", "Mitel6867i"]:
                self.phone_obj.press_softkey(3)
            elif self.phone_obj.phone_type == 'Mitel6930':
                self.phone_obj.press_softkey(4)
            else:
                self.phone_obj.press_softkey(5)

        else:
            raise Exception("Invalid Arguments Passed !!. The argument passed: " + softkey + " is not supported.")

    def pressSoftkeyInVoiceMailState(self, **kwargs):
        """
        This method is used to press any of the available softkeys
        while the phone is in VoiceMailState.

        :param
            :softKey: More/CallBack/Open/Cancel/Call VM/Call Inbox VM/Quit/Delete/
                   /Play/startPlay/StopPlay/Send/Back/moreBack/Forward/Reply
                   /Save/SaveReply/Edit

        :returns: None
        :Created By:  abhishek khanchi(nof)
        :last update by: Sharma
        :last update date: 24/12/2019
          """

        softkey = kwargs["softKey"]
        logger.info("Pressing key: <b>" + softkey + "</b> on extension: <b>"
                    + self.phone_obj.phone_obj.phone.extensionNumber + "</b> while in Voicemail State.", html=True)
        console("Pressing key: " + softkey + " on extension: " + self.phone_obj.phone_obj.phone.extensionNumber
                + " while in Voicemail state.")

        if softkey == "More":
            if self.phone_obj.phone_type == "Mitel6920":
                self.phone_obj.press_softkey(4)
            if (self.phone_obj.phone_type == "Mitel6940"):
                self.phone_obj.press_key("BottomKey6")
            else:
                self.phone_obj.press_softkey(5)

        elif softkey == "CallBack":
            self.phone_obj.press_softkey(2)
            self.phone_obj.sleep(2)

        elif softkey == "Open":
            if self.phone_obj.phone_type == "Mitel6920":
                self.phone_obj.press_softkey(4)
                self.phone_obj.sleep(2)
                self.phone_obj.press_softkey(1)
            else:
                self.phone_obj.sleep(2)
                self.phone_obj.press_softkey(4)

        elif softkey == "Cancel":
            if self.phone_obj.phone_type == "Mitel6920":
                self.phone_obj.press_softkey(4)
                self.phone_obj.sleep(2)
                self.phone_obj.press_softkey(1)
            else:
                self.phone_obj.sleep(2)
                self.phone_obj.press_softkey(4)

        elif softkey == "Call VM":
            self.phone_obj.press_softkey(2)

        elif softkey == "Call Inbox VM":
            if self.phone_obj.phone_type == "Mitel6920":
                self.phone_obj.press_softkey(4)
                self.phone_obj.press_softkey(4)
                self.phone_obj.sleep(2)
                self.phone_obj.press_softkey(2)
            elif self.phone_obj.phone_type == 'Mitel6930':
                self.phone_obj.press_softkey(5)
                self.phone_obj.press_softkey(5)
                self.phone_obj.sleep(1)
                self.phone_obj.press_softkey(2)
            else:
                self.phone_obj.press_softkey(5)
                self.phone_obj.sleep(1)
                self.phone_obj.press_softkey(4)

        elif softkey == "Quit":
            if self.phone_obj.phone_type == "Mitel6920":
                self.phone_obj.press_softkey(4)
                self.phone_obj.sleep(2)
                self.phone_obj.press_softkey(4)
                self.phone_obj.sleep(2)
                self.phone_obj.press_softkey(3)
            if self.phone_obj.phone_type == "Mitel6940":
                self.phone_obj.press_key("BottomKey6")
                self.phone_obj.sleep(2)
                self.phone_obj.press_key("BottomKey6")
                self.phone_obj.sleep(2)
                self.phone_obj.press_key("BottomKey5")
            else:
                self.phone_obj.sleep(2)
                self.phone_obj.press_softkey(5)
                self.phone_obj.sleep(2)
                self.phone_obj.press_softkey(4)

        elif softkey == "Delete":
            self.phone_obj.press_softkey(3)
            self.phone_obj.sleep(3)
            self.phone_obj.press_softkey(2)
            self.phone_obj.sleep(2)

        elif softkey in ('Play', 'Pause'):
            self.phone_obj.press_softkey(1)
            self.phone_obj.sleep(3)

        elif (softkey == "startPlay"):
            self.phone_obj.press_softkey(3)

        elif softkey == "Start" or softkey == "Stop":
            self.phone_obj.press_softkey(2)
            self.phone_obj.sleep(5)

        elif softkey == "StopPlay":
            if self.phone_obj.phone_type == "Mitel6920":
                self.phone_obj.press_softkey(4)
                self.phone_obj.press_softkey(1)
            else:
                self.phone_obj.press_softkey(4)
            self.phone_obj.sleep(1)

        elif (softkey == "Send"):
            if (self.phone_obj.phone_type == "Mitel6920"):
                self.phone_obj.press_softkey(4)
                self.phone_obj.sleep(3)
                self.phone_obj.press_softkey(1)
            else:
                self.phone_obj.press_softkey(4)

        elif (softkey == "SendF"):
            self.phone_obj.press_softkey(3)

        elif (softkey == "Back"):
            if (self.phone_obj.phone_type == "Mitel6920"):
                self.phone_obj.press_softkey(4)
                self.phone_obj.sleep(3)
            if (self.phone_obj.phone_type == "Mitel6940"):
                self.phone_obj.press_key("BottomKey6")
                self.phone_obj.sleep(3)
            else:
                self.phone_obj.press_softkey(5)
                self.phone_obj.sleep(3)

        elif (softkey == "moreBack"):
            if (self.phone_obj.phone_type == "Mitel6920"):
                self.phone_obj.press_softkey(3)
                self.phone_obj.sleep(3)
            else:
                self.phone_obj.press_softkey(4)
                self.phone_obj.sleep(3)

        elif (softkey == "Forward"):
            if (self.phone_obj.phone_type == "Mitel6920"):
                self.phone_obj.press_softkey(4)
                self.phone_obj.sleep(3)
                self.phone_obj.press_softkey(4)
                self.phone_obj.sleep(3)
                self.phone_obj.press_softkey(1)
                self.phone_obj.sleep(5)
            elif (self.phone_obj.phone_type == "Mitel6940"):
                self.phone_obj.press_key("BottomKey6")
                self.phone_obj.sleep(3)
                self.phone_obj.press_softkey(2)
            else:
                self.phone_obj.press_softkey(5)
                self.phone_obj.sleep(3)
                self.phone_obj.press_softkey(3)
                self.phone_obj.sleep(5)

        elif (softkey == "Reply"):
            if (self.phone_obj.phone_type == "Mitel6920"):
                self.phone_obj.press_softkey(3)
            else:
                self.phone_obj.press_softkey(2)

        elif softkey == "Save":
            if self.phone_obj.phone_type == "Mitel6920":
                self.phone_obj.press_softkey(4)
                self.phone_obj.press_softkey(2)
                self.phone_obj.sleep(2)
            elif self.phone_obj.phone_type == "Mitel6930":
                self.phone_obj.press_softkey(5)
                self.phone_obj.press_softkey(1)
                self.phone_obj.sleep(2)
            elif self.phone_obj.phone_type == "Mitel6940":
                self.phone_obj.press_softkey(5)

        elif (softkey == "SaveReply"):
            if (self.phone_obj.phone_type == "Mitel6920"):
                self.phone_obj.press_softkey(4)
                self.phone_obj.press_softkey(2)
            if (self.phone_obj.phone_type == "Mitel6940"):
                self.phone_obj.press_softkey(5)
            else:
                self.phone_obj.press_softkey(5)
                self.phone_obj.press_softkey(1)

        elif (softkey == "Edit"):
            self.phone_obj.press_softkey(1)

        elif softkey == "Call Saved VM":
            if self.phone_obj.phone_type == "Mitel6920":
                self.phone_obj.press_softkey(4)
                self.phone_obj.press_softkey(4)
                self.phone_obj.press_softkey(1)
            elif self.phone_obj.phone_type == "Mitel6930" or self.phone_obj.phone_type == "Mitel6940":
                self.phone_obj.press_softkey(5)
                self.phone_obj.press_softkey(3)
        else:
            raise Exception("Please check the softkey passed %s" % softkey)

    def pressSoftKeyInTransferState(self, **kwargs):
        """
        This method is used to press any of the available softkeys while the phone is in transfer state.

        Keyword Args:
            softKey: Drop/Pickup/Transfer/ToVm/BCATransfer/Backspace/Blind Transfer
            pbx: Call Manager of the phone

        :returns: None
        :Created By:  abhishek khanchi(nof)
        :creation date:
        :last update by: Vikhyat Sharma
        :last update date: 11/01/2021
        """

        softkey = kwargs["softKey"]
        pbx = kwargs['pbx']
        logger.info("Pressing key: <b>" + softkey + "</b> on extension: <b>"
                    + self.phone_obj.phone_obj.phone.extensionNumber + "</b> in Transfer State.", html=True)
        console("Pressing softkey: " + softkey + " on extension: " + self.phone_obj.phone_obj.phone.extensionNumber
                + " while in Transfer State.")

        if softkey == "Drop":
            if self.phone_obj.phone_type in ["Mitel6910", "Mitel6865i"]:
                self.phone_obj.press_key("GoodBye")
            else:
                self.phone_obj.press_softkey(1)

        elif softkey == "Pickup" or softkey == "Consult":
            if self.phone_obj.phone_type in ["Mitel6910", "Mitel6865i"]:
                self.phone_obj.press_key("ScrollRight")
            else:
                self.phone_obj.press_softkey(1)

        elif softkey == "Transfer":
            if self.phone_obj.phone_type in ('Mitel6865i', "Mitel6910"):
                self.phone_obj.press_key("Transfer")
            else:
                self.phone_obj.press_softkey(3)

        elif softkey == "ToVm":
            if self.phone_obj.phone_type == "Mitel6910":
                self.phone_obj.input_a_number("#")
            elif self.phone_obj.phone_type == "Mitel6920":
                self.phone_obj.press_softkey(4)
                self.phone_obj.press_softkey(3)
            elif self.phone_obj.phone_type == "Mitel6930":
                self.phone_obj.press_softkey(5)
                self.phone_obj.press_softkey(2)
            elif self.phone_obj.phone_type == "Mitel6940":
                self.phone_obj.press_key("BottomKey6")

        elif softkey == "BCATransfer":
            if self.phone_obj.phone_type == "Mitel6910":
                logger.warn("NOT DOING ANYTHING HERE!!")
            elif self.phone_obj.phone_type == "Mitel6930":
                self.phone_obj.press_softkey(4)
            else:
                self.phone_obj.press_softkey(3)

        elif softkey == "Cancel":
            if self.phone_obj.phone_type in ('Mitel6865i', "Mitel6910"):
                self.phone_obj.press_key("GoodBye")
            elif self.phone_obj.phone_type == "Mitel6920":
                if pbx in ('MiVoice', 'MiCloud'):
                    self.phone_obj.press_softkey(4)
                    self.phone_obj.sleep(2)
                    self.phone_obj.press_softkey(1)
                else:
                    self.phone_obj.press_softkey(4)
            elif self.phone_obj.phone_type == "Mitel6930":
                if pbx in ('MiVoice', 'MiCloud'):
                    self.phone_obj.press_softkey(4)
                else:
                    self.phone_obj.press_softkey(5)
            elif self.phone_obj.phone_type == 'Mitel6940':
                if pbx in ('MiVoice', 'MiCloud'):
                    self.phone_obj.press_softkey(4)
                else:
                    # self.phone_obj.press_softkey(6)
                    self.phone_obj.press_key('BottomKey6')

        elif softkey == "Backspace":
            if self.phone_obj.phone_type != "Mitel6910":
                self.phone_obj.press_softkey(2)

        elif softkey == "Blind Transfer":
            if self.phone_obj.phone_type == "Mitel6920":
                self.phone_obj.press_softkey(3)
            else:
                self.phone_obj.press_softkey(4)

        elif softkey == "More":
            if self.phone_obj.phone_type != "Mitel6910":
                if self.phone_obj.phone_type == "Mitel6940":
                    self.phone_obj.press_key("BottomKey6")
                elif self.phone_obj.phone_type == "Mitel6930":
                    self.phone_obj.press_softkey(5)
                else:
                    self.phone_obj.press_softkey(4)

        else:
            raise Exception("Incorrect parameter passed for softkey: " + softkey + " passed !!")

    def pressKeyInState(self, *args):
        """
        This routine is used to press any of the key passed in a particular state.
        :param
            self :  Caller set object
            :args: Arguments needed:
                    :key: Key to press i.e., Mute/UnMute/Scroll up/Cancel
                    :state: State of the phone i.e., Ringing/Answer/Idle
        :returns: None
        :created by: Manoj Karakoti
        :creation date: 04/09/2019
        :last update by: Vikhyat Sharma
        :last update date: 01/12/2020
        """

        key = args[0]
        state = args[1]

        logger.info("Pressing key: <b>" + key + "</b> on extension: <b>" +
                    self.phone_obj.phone_obj.phone.extensionNumber + "</b> while in <b>" + state
                    + "</b> state.", html=True)
        console("Pressing key: " + key + " on extension: " + self.phone_obj.phone_obj.phone.extensionNumber
                + " while in " + state + " state.")

        self.phone_obj.sleep(2)
        if state == "Ringing":
            if key == "ScrollUp":
                self.phone_obj.press_key("ScrollUp")

        elif state == "Answer":
            if key == "Mute":
                self.phone_obj.press_key("Mute")
                # self.phone_obj.verify_led_state("mute", "blink", 10)
                self.verifyLedState(ledType='Mute', ledMode='blink')
            elif key == "UnMute":
                self.phone_obj.press_key("Mute")
                # self.phone_obj.verify_led_state("mute", "off", 10)
                self.verifyLedState(ledType='Mute', ledMode='blink')
            elif key == "Hold":
                self.phone_obj.press_key("Hold")

        elif state == "Idle":
            if key == "Conference":
                if self.phone_obj.phone_type in ('Mitel6865i', "Mitel6910"):
                    self.phone_obj.press_key("Conference")
                else:
                    self.phone_obj.press_softkey(3)
                self.phone_obj.sleep(2)

        elif state == "Diagnostics":
            if key == "Cancel":
                if self.phone_obj.phone_type in ("Mitel6930", "Mitel6940"):
                    self.phone_obj.press_softkey(5)
                elif self.phone_obj.phone_type == "Mitel6920":
                    self.phone_obj.press_softkey(4)
                    self.phone_obj.press_softkey(3)
                elif self.phone_obj.phone_type in ('Mitel6865i', "Mitel6910"):
                    self.phone_obj.press_key("ScrollUp")
                self.phone_obj.sleep(2)

        elif state == "Ping":
            if key == "Ping":
                if self.phone_obj.phone_type in ("Mitel6930", "Mitel6940"):
                    self.phone_obj.press_softkey(1)
                elif self.phone_obj.phone_type == "Mitel6920":
                    self.phone_obj.press_softkey(4)
                    self.phone_obj.press_softkey(1)
                elif self.phone_obj.phone_type in ('Mitel6865i', "Mitel6910"):
                    self.phone_obj.press_key("ScrollDown")
                self.phone_obj.sleep(1)

        elif state == "Directory":
            if key == "Add New":
                if self.phone_obj.phone_type in ("Mitel6865i", "Mitel6910"):
                    pass
                else:
                    self.phone_obj.press_softkey(3)
            elif key in ("By First", "By Last"):
                if not self.phone_obj.verify_display_message_contents(key):
                    logger.warn("Directory is already sorted " + key + " on extension: "
                                + self.phone_obj.phone_obj.phone.extensionNumber)
                else:
                    if self.phone_obj.phone_type == 'Mitel6920':
                        self.phone_obj.press_softkey(2)
                    elif self.phone_obj.phone_type == 'Mitel6930':
                        self.phone_obj.press_softkey(3)
                    elif self.phone_obj.phone_type == 'Mitel6940':
                        self.phone_obj.press_softkey(4)
                    else:
                        raise Exception(key + " is not supported on " + self.phone_obj.phone_type + " model!!")
            elif key == 'Close':
                if self.phone_obj.phone_type == 'Mitel6920':
                    self.phone_obj.press_softkey(4)
                elif self.phone_obj.phone_type == 'Mitel6930':
                    self.phone_obj.press_softkey(5)
                elif self.phone_obj.phone_type == 'Mitel6940':
                    # self.phone_obj.press_softkey(6)
                    self.phone_obj.press_key('BottomKey6')
                else:
                    raise Exception(key + " is not supported on " + self.phone_obj.phone_type + " model!!")

        elif state == "Call History":
            if key == "Quit":
                if self.phone_obj.phone_type in ('Mitel6865i', "Mitel6910"):
                    self.phone_obj.press_key("GoodBye")
                elif self.phone_obj.phone_type == "Mitel6920":
                    self.phone_obj.press_softkey(4)
                elif self.phone_obj.phone_type == "Mitel6940":
                    self.phone_obj.press_key("BottomKey6")
                else:
                    self.phone_obj.press_softkey(5)
            elif key == "Details":
                if self.phone_obj.phone_type in ('Mitel6865i', "Mitel6910"):
                    logger.warn("Details Key is not there on the 6910 set.")
                elif self.phone_obj.phone_type == "Mitel6920":
                    self.phone_obj.press_softkey(3)
                elif self.phone_obj.phone_type == "Mitel6940":
                    self.phone_obj.press_softkey(5)
                else:
                    self.phone_obj.press_softkey(4)
            elif key == "Dial":
                if self.phone_obj.phone_type in ('Mitel6865i', "Mitel6910"):
                    self.phone_obj.press_key("Enter")
                else:
                    self.phone_obj.press_softkey(1)

        else:
            raise Exception("INVALID STATE PASSED !!")

    def makeConference(self, **kwargs):
        """
        This method is used to make a three-party direct/consultive conference call.

        Keyword Args:
            phoneObj: Called set object
            confMode: Way to invoke conference call i.e., Consultive/Direct

        :returns: None
        :created by: Manoj Karakoti
        :creation date: 14/01/2019
        :last update by: Vikhyat Sharma
        :last update date: 07/12/2020
        """

        phoneObj = kwargs['phoneObj']
        confMode = kwargs['ConferenceMode']
        pbx = kwargs['pbx']
        # number = str(phoneObj.phone_obj.phone_obj.phone.extensionNumber)

        logger.info("Making a <b>" + confMode + "</b> call from extension: <b>"
                    + self.phone_obj.phone_obj.phone.extensionNumber
                    + "</b> to add extension: <b>" + phoneObj.phone_obj.phone_obj.phone.extensionNumber
                    + "</b> on the call.", html=True)
        console("Making a " + confMode + " call from extension: " + self.phone_obj.phone_obj.phone.extensionNumber
                + " to add extension: " + phoneObj.phone_obj.phone_obj.phone.extensionNumber + " on the call.")

        if self.phone_obj.phone_type in ["Mitel6910", "Mitel6865i"]:
            self.phone_obj.press_key("Conference")
        else:
            self.phone_obj.press_softkey(2)

        self.phone_obj.sleep(2)
        self.phone_obj.enter_a_number(phoneObj.phone_obj.phone_obj.phone)

        if confMode == "ConsultiveConference":
            if self.phone_obj.phone_type in ["Mitel6910", "Mitel6865i"]:
                self.phone_obj.press_key("ScrollRight")
            else:
                self.phone_obj.press_softkey(1)

            self.phone_obj.sleep(2)

            if phoneObj.phone_obj.phone_type in ["Mitel6910", "Mitel6865i"]:
                phoneObj.phone_obj.press_key("HandsFree")
            else:
                phoneObj.phone_obj.press_softkey(1)

            self.phone_obj.sleep(2)
            if self.phone_obj.phone_type in ["Mitel6910", "Mitel6865i"]:
                self.phone_obj.press_key("Conference")
            else:
                self.phone_obj.press_softkey(2)
            self.phone_obj.sleep(5)

        elif confMode == "DirectConference":
            if self.phone_obj.phone_type in ["Mitel6910", "Mitel6865i"]:
                self.phone_obj.press_key("Conference")
            else:
                self.phone_obj.press_softkey(2)
            self.phone_obj.sleep(2)

            if phoneObj.phone_obj.phone_type in ["Mitel6910", "Mitel6865i"]:
                phoneObj.phone_obj.press_key("HandsFree")
            else:
                phoneObj.phone_obj.press_softkey(1)
            self.phone_obj.sleep(4)
        else:
            self.phone_obj.press_softkey(1)
            self.phone_obj.sleep(2)
            phoneObj.phone_obj.press_softkey(1)
            self.phone_obj.sleep(2)
            self.phone_obj.press_softkey(2)
            self.phone_obj.sleep(2)

        if pbx not in ('MiV5000', 'Asterisk', 'MxOne'):
            self.verifyDisplayMessageUtil("Conference")
            phoneObj.verifyDisplayMessageUtil("Conference")

    def verifyCallid(self, **kwargs):
        """
        Below method verifies the caller id of phones while being in a call.
        :param:
           kwargs: Dictionary used to get the arguments:
                    phoneObj: PhoneComponent object of the other phone on call

        :returns: None
        :created by: Gaurav
        :creation date:
        :last update by: Sharma
        :last update Date: 25/08/2020
        """

        phoneObj = kwargs['phoneObj']
        extensionPhoneB = phoneObj.phone_obj.phone_obj.phone.extensionNumber
        extensionPhoneA = self.phone_obj.phone_obj.phone.extensionNumber

        logger.info("Verifying the caller IDs on extensions: <b>" + extensionPhoneA + "</b> and <b>"
                    + extensionPhoneB + "</b>.", html=True)
        console("Verifying the caller IDs on extensions: " + extensionPhoneA + " and " + extensionPhoneB)
        if kwargs['pbx'] == "Clearspan":
            phoneObj.verifyDisplayMessageUtil(extensionPhoneA[-4:])
            self.verifyDisplayMessageUtil(extensionPhoneB[-4:])
        else:
            phoneObj.verifyDisplayMessageUtil(extensionPhoneA)
            self.verifyDisplayMessageUtil(extensionPhoneB)

    def verifyDisplayRinging(self, **kwargs):
        """
            Below method verifies the display of the phones while they are ringing.

            :param:
                :self: Called phone
                :kwargs: Dictionary used to get the arguments:
                    phoneObj: Caller phone
            :returns: None

            :created by: Manoj Karakoti
            :creation date: 14/01/2019
            :last update by: Sharma
            :last update date: 08/08/2020
        """
        phoneObj = kwargs['phoneObj']
        calledPhone = phoneObj.phone_obj.phone_obj.phone.extensionNumber

        logger.info("Verifying Display Ringing on extensions: <b>" + self.phone_obj.phone_obj.phone.extensionNumber
                    + "</b> and <b>" + calledPhone + "</b>.", html=True)
        console("Verifying Display Ringing on extensions: " + self.phone_obj.phone_obj.phone.extensionNumber
                + " and " + calledPhone)

        import re
        self.verifyDisplayMessageUtil(calledPhone)
        if not bool(re.search(r"5.1.\d", self.phone_obj.get_firmware_version())):
            if self.phone_obj.phone_type not in ("Mitel6910", "Mitel6865i"):
                self.verifyDisplayMessageUtil("Is Calling")
        if not bool(re.search(r"5.1.\d", self.phone_obj.get_firmware_version())):
            if phoneObj.phone_obj.phone_type not in ("Mitel6910", "Mitel6865i"):
                phoneObj.verifyDisplayMessageUtil("Ringing")

    def verifyCallForwardRinging(self, **kwargs):
        """
            Below method verifies the display of the phones while they are ringing when call is forwarded

            :param:
                :self: Caller phone
                :kwargs: Dictionary used to get the arguments:
                    phoneObj1: phone whose call are forwarded
                    phoneObj2: Actual Called phone
                    forwardMode: Unconditional/NoResponse/Busy/DND
            :returns: None

            :created by: Vijay Pawar
            :creation date: 07/05/2021
            :last update by:
            :last update date:
        """
        phoneObj1 = kwargs['phoneObj1']
        phoneObj2 = kwargs['phoneObj2']
        forwardMode = kwargs['forwardMode']
        callerPhone = self.phone_obj.phone_obj.phone.extensionNumber
        extension1 = phoneObj1.phone_obj.phone_obj.phone.extensionNumber
        extension2 = phoneObj2.phone_obj.phone_obj.phone.extensionNumber

        logger.info("Verifying Display Ringing on extensions: <b>" + callerPhone
                    + "</b> and <b>" + extension2 + "</b>.", html=True)
        console("Verifying Display Ringing on extensions: " + callerPhone
                + " and " + extension2 )

        import re
        if self.phone_obj.phone_type not in ("Mitel6910", "Mitel6865i"):
            self.verifyDisplayMessageUtil(phoneObj1.phone_obj.phone_obj.phone.phoneName)
            self.verifyDisplayMessageUtil(extension1[-4:])
            if not bool(re.search(r"5.1.\d", self.phone_obj.get_firmware_version())):
                    self.verifyDisplayMessageUtil("Ringing")
                    if forwardMode in ("Unconditional", "Busy", "DND"):
                        if forwardMode == "Unconditional" or "DND":
                          self.verifyDisplayMessageUtil("Unconditional")
                        elif forwardMode == "Busy":
                          self.verifyDisplayMessageUtil("User-Busy")
                        self.verifyDisplayMessageUtil("Diverted to: ")
                        self.verifyDisplayMessageUtil(extension2[-4:])
        else:
            logger.warn("Model : " + phoneObj2.phone_obj.phone_type + " has no display verification")
            pass

        if phoneObj2.phone_obj.phone_type not in ("Mitel6910", "Mitel6865i"):
            if not bool(re.search(r"5.1.\d", self.phone_obj.get_firmware_version())):
                     phoneObj2.verifyDisplayMessageUtil("Is Calling")
                     phoneObj2.verifyDisplayMessageUtil("Via: ")
                     phoneObj2.verifyDisplayMessageUtil(phoneObj1.phone_obj.phone_obj.phone.phoneName)
        else:
            logger.warn("Model : "+ phoneObj2.phone_obj.phone_type + " has no display verification")
            pass




    def disableCallForward(self):
        """
        This method is used to disable call forward
        :return:
        """
        time.sleep(2)

        if self.phone_obj.phone_type not in ("Mitel6910", "Mitel6865i"):
            if self.phone_obj.verify_display_message_contents("CFU"):
                logger.info("Disabling Call forwarding Unconditional mode on: extension <b>" +
                            self.phone_obj.phone_obj.phone.extensionNumber
                            + "</b>", html=True)
                console("Disabling Call forwarding Uncondtional mode on: extension " +
                            self.phone_obj.phone_obj.phone.extensionNumber)
                try:
                    self.phone_obj.input_a_number("#21")
                    self.phone_obj.sleep(1)
                    self.phone_obj.press_softkey(1)
                except:
                    time.sleep(5)
                    self.phone_obj.input_a_number("#21")
                    self.phone_obj.sleep(1)
                    self.phone_obj.press_softkey(1)

            elif self.phone_obj.verify_display_message_contents("CFNR"):
                logger.info("Disabling Call forwarding If NoResponse on: extension <b>" +
                            self.phone_obj.phone_obj.phone.extensionNumber
                            + "</b>", html=True)
                console("Disabling Call forwarding If NoResponse on: extension " +
                            self.phone_obj.phone_obj.phone.extensionNumber)
                try:
                    self.phone_obj.input_a_number("#61")
                    self.phone_obj.sleep(1)
                    self.phone_obj.press_softkey(1)
                except:
                    time.sleep(5)
                    self.phone_obj.input_a_number("#61")
                    self.phone_obj.sleep(1)
                    self.phone_obj.press_softkey(1)

            elif self.phone_obj.verify_display_message_contents("Forw. busy"):
                logger.info("Disabling Call forwarding If busy on: extension <b>" +
                            self.phone_obj.phone_obj.phone.extensionNumber
                            + "</b>", html=True)
                console("Disabling Call forwarding If busy on: extension " +
                            self.phone_obj.phone_obj.phone.extensionNumber)
                try:
                    self.phone_obj.input_a_number("#67")
                    self.phone_obj.sleep(1)
                    self.phone_obj.press_softkey(1)
                except:
                    time.sleep(5)
                    self.phone_obj.input_a_number("#67")
                    self.phone_obj.sleep(1)
                    self.phone_obj.press_softkey(1)

            elif self.phone_obj.verify_display_message_contents("Do not disturb"):
                logger.info("Disabling Call forwarding on DND on: extension <b>" +
                            self.phone_obj.phone_obj.phone.extensionNumber
                            + "</b>", html=True)
                console("Disabling Call forwarding on DND on: extension " +
                        self.phone_obj.phone_obj.phone.extensionNumber)
                try:
                    self.phone_obj.input_a_number("#26")
                    self.phone_obj.sleep(1)
                    self.phone_obj.press_softkey(1)
                except:
                    time.sleep(5)
                    self.phone_obj.input_a_number("#26")
                    self.phone_obj.sleep(1)
                    self.phone_obj.press_softkey(1)

            else:
                raise Exception("CALL FORWARD NOT ACTIVATE !!")

        else:
            self.phone_obj.input_a_number("#21")
            self.phone_obj.press_key("OffHook")
            self.phone_obj.sleep(10)
            self.phone_obj.input_a_number("#61")
            self.phone_obj.press_key("OffHook")
            self.phone_obj.sleep(10)
            self.phone_obj.input_a_number("#67")
            self.phone_obj.press_key("OffHook")
            self.phone_obj.sleep(10)
            self.phone_obj.input_a_number("#26")
            self.phone_obj.press_key("OffHook")
            self.phone_obj.sleep(10)




    def verifyDisplayMessage(self, **kwargs):
        """
        This method is used to verify passed message on the display of the phones.

        Args:
            self: PhoneComponent object of the caller phone
        Keyword Args:
            message: Message to be verified on the display screen
            pbx: Call Manager of the phone

        :returns: None
        :created by: Gaurav
        :creation date:
        :last update by: Milind Patil
        :last update Date: 27/01/2021
        """

        messageToVerify = kwargs["message"]
        pbx = kwargs['pbx']

        if isinstance(messageToVerify, PhoneComponent):
            messageToVerify = messageToVerify.phone_obj.phone_obj.phone.extensionNumber

        if self.phone_obj.phone_type in ("Mitel6910", "Mitel6865i"):
            if messageToVerify in softKeysNotOn6910:
                logger.warn("Message: {} cannot be verified on Model: {}".format(messageToVerify,
                                                                                 self.phone_obj.phone_type), html=True)
            elif messageToVerify == "Traceroute Command":
                messageToVerify = 'Hostname/ IP addr.'
                self.verifyDisplayMessageUtil(messageToVerify)
        else:
            if messageToVerify in ('Backup Auto', 'Request denied') and pbx == 'MiCloud':
                logger.info(messageToVerify + " does not come on MiCloud Call manager. "
                                              "Verifying 'Not Permitted on this call' instead on "
                            + self.phone_obj.phone_obj.phone.extensionNumber)
                messageToVerify = "Not Permitted on this call"

            messageToVerify = kwargs.get('prefix', '') + messageToVerify + kwargs.get('suffix', '')
            self.verifyDisplayMessageUtil(messageToVerify)

        self.phone_obj.sleep(3)

    def verifyDisplayMessageUtil(self, message):
        """
        This method verifies the display on the sets.

        param:
            message: Message to be verified

        :returns: None
        :created by: Abhishek Pathak
        :creation date:
        :last update by: None
        :last update date: 24/10/2019
        """
        if self.phone_obj.verify_display_message_contents(message):
            logger.info("Message : <b>%s" % message + "</b> Verified on extension "
                        + self.phone_obj.phone_obj.phone.extensionNumber, html=True)
            console("Message : %s" % message + " Verified on extension "
                    + self.phone_obj.phone_obj.phone.extensionNumber)

        else:

            raise Exception("Message : %s" % message + " not verified on " + self.phone_obj.phone_type
                            + " with extension " + self.phone_obj.phone_obj.phone.extensionNumber + " and IP: "
                            + self.phone_obj.phone_obj.phone.ipAddress)


    def verifySoftkeysInDifferentPhoneState(self, **kwargs):
        """
        This method verifies the softkeys available on the phone depending upon its state.

        Keyword Args:
            phoneState: State of the phone: Talk/Conference/Idle/Voicemail/Availability/Settings/Dial/Transfer

        :returns: None

        :created by: Manoj Karakoti
        :creation date: 21/01/2019
        :last update by: Ramkumar. G
        :last update date: 17/02/2021
        """

        phoneState = kwargs['phoneState']

        logger.info("Verifying the softkeys in <b>" + phoneState + "</b> state on extension <b>"
                    + self.phone_obj.phone_obj.phone.extensionNumber + "</b>", html=True)
        console("Verifying the softkeys in " + phoneState + " state on extension "
                + self.phone_obj.phone_obj.phone.extensionNumber)

        if phoneState == "Talk":
            if self.phone_obj.phone_type not in ('Mitel6865i', 'Mitel6910'):
                self.verifyDisplayMessageUtil("Drop")
                self.verifyDisplayMessageUtil("Conference")
                self.verifyDisplayMessageUtil("Transfer")

                if self.phone_obj.phone_type in ("Mitel6920", 'Mitel6867i'):
                    self.phone_obj.press_softkey(4)
                self.verifyDisplayMessageUtil("Park")
                if self.phone_obj.phone_type in ("Mitel6920", 'Mitel6867i'):
                    self.phone_obj.press_softkey(4)

        elif phoneState == "Ringing":
            if self.phone_obj.phone_type not in ('Mitel6865i', "Mitel6910"):
                self.verifyDisplayMessageUtil("Answer")
                self.verifyDisplayMessageUtil("Ignore")
                self.verifyDisplayMessageUtil("Transfer")
                if (self.phone_obj.phone_type == "Mitel6920"):
                    self.phone_obj.press_softkey(4)
                self.verifyDisplayMessageUtil("To Vm")
                if self.phone_obj.phone_type == "Mitel6920":
                    self.phone_obj.press_softkey(4)

        elif phoneState == "Conference":
            self.verifyDisplayMessageUtil("Drop")
            self.verifyDisplayMessageUtil("Conference")
            self.verifyDisplayMessageUtil("Leave")

        elif phoneState == "Idle" or phoneState == "idle":
            if self.phone_obj.phone_type in ('Mitel6865i', "Mitel6910"):
                extensionPhoneA = self.phone_obj.phone_obj.phone.extensionNumber
                self.verifyDisplayMessageUtil(extensionPhoneA)
            else:
                self.verifyDisplayMessageUtil(self.phone_obj.phone_obj.phone.extensionNumber)
                self.verifyDisplayMessageUtil("Pickup")
                self.verifyDisplayMessageUtil("UnPark")
                self.verifyDisplayMessageUtil("Conference")
                self.verifyDisplayMessageUtil("State")

        elif phoneState in ('VoiceMail', 'Saved', 'Voicemail Inbox'):
            self.verifyDisplayMessageUtil("Play")
            self.verifyDisplayMessageUtil("Call Back")
            self.verifyDisplayMessageUtil("Delete")
            if self.phone_obj.phone_type == "Mitel6920":
                self.phone_obj.press_softkey(4)
                self.verifyDisplayMessageUtil("Open")
                self.phone_obj.press_softkey(4)
                self.verifyDisplayMessageUtil("Call VM")
                self.verifyDisplayMessageUtil("Quit")
                self.phone_obj.press_softkey(4)
            elif self.phone_obj.phone_type == "Mitel6930":
                self.verifyDisplayMessageUtil("Open")
                self.phone_obj.press_softkey(5)

                if phoneState != "Saved":
                    self.phone_obj.press_softkey(5)
                self.verifyDisplayMessageUtil("Call VM")
                self.verifyDisplayMessageUtil("Quit")
                self.phone_obj.press_softkey(5)
            elif self.phone_obj.phone_type == "Mitel6940":
                self.verifyDisplayMessageUtil("Open")
                self.verifyDisplayMessageUtil("Save")
                self.phone_obj.press_key("BottomKey6")
                self.verifyDisplayMessageUtil("Call VM")
                self.phone_obj.press_key("BottomKey6")
                self.verifyDisplayMessageUtil("Quit")
                # going to original state
                self.phone_obj.press_key("BottomKey6")

        elif phoneState in ("Voicemail Play", "Voicemail Pause"):
            if phoneState == "Voicemail Play":
                self.verifyDisplayMessageUtil('Pause')
            else:
                self.verifyDisplayMessageUtil("Play")

            self.verifyDisplayMessageUtil("Skip Back")
            self.verifyDisplayMessageUtil("Skip Forward")
            if self.phone_obj.phone_type == "Mitel6920":
                self.phone_obj.press_softkey(4)
            self.verifyDisplayMessageUtil("Stop")

            # going to the original state
            if self.phone_obj.phone_type == "Mitel6920":
                self.phone_obj.press_softkey(4)

        elif phoneState == "UserAvailability":
            self.verifyDisplayMessageUtil("Save")
            self.verifyDisplayMessageUtil("Cancel")

        elif phoneState == "Settings":
            self.verifyDisplayMessageUtil("Select")
            self.verifyDisplayMessageUtil("Advanced")
            self.verifyDisplayMessageUtil("Log Issue")
            self.verifyDisplayMessageUtil("Quit")

        elif (phoneState == "Dial"):
            if self.phone_obj.phone_type == "Mitel6910":
                self.verifyDisplayMessageUtil("Bksp")
                self.verifyDisplayMessageUtil("Dial")
            else:
                self.verifyDisplayMessageUtil("UnPark")
                self.verifyDisplayMessageUtil("Backspace")
                self.verifyDisplayMessageUtil("Dial")
                self.verifyDisplayMessageUtil("Cancel")

        elif phoneState == "Transfer":
            if (self.phone_obj.phone_type == "Mitel6920"):
                self.verifyDisplayMessageUtil("Consult")
                self.verifyDisplayMessageUtil("Backspace")
                self.verifyDisplayMessageUtil("Transfer")
                self.phone_obj.press_softkey(4)
                self.verifyDisplayMessageUtil("Cancel")
                self.phone_obj.press_softkey(4)
            elif (self.phone_obj.phone_type in ("Mitel6930", "Mitel6940")):
                self.verifyDisplayMessageUtil("Consult")
                self.verifyDisplayMessageUtil("Backspace")
                self.verifyDisplayMessageUtil("Transfer")
                self.verifyDisplayMessageUtil("Cancel")

        elif (phoneState == "BCA"):
            if (self.phone_obj.phone_type == "Mitel6920"):
                self.verifyDisplayMessageUtil("Drop")
                self.verifyDisplayMessageUtil("Conference")
                self.verifyDisplayMessageUtil("Transfer")
                self.phone_obj.press_softkey(4)
                self.verifyDisplayMessageUtil("Park")
                self.verifyDisplayMessageUtil("Unlock")
            elif self.phone_obj.phone_type == "Mitel6930":
                self.verifyDisplayMessageUtil("Drop")
                self.verifyDisplayMessageUtil("Park")
                self.verifyDisplayMessageUtil("Conference")
                self.verifyDisplayMessageUtil("Transfer")
                self.verifyDisplayMessageUtil("Unlock")
            elif self.phone_obj.phone_type == "Mitel6940":
                self.verifyDisplayMessageUtil("Drop")
                self.verifyDisplayMessageUtil("Park")
                self.verifyDisplayMessageUtil("Conference")
                self.verifyDisplayMessageUtil("Transfer")

        elif (phoneState == "TransferWpd"):
            if self.phone_obj.phone_type == "Mitel6920":
                console('Inside TransferWpd Mitel6920 ')
                self.verifyDisplayMessageUtil("Consult")
                self.verifyDisplayMessageUtil("Backspace")
                self.verifyDisplayMessageUtil("Transfer")
                self.phone_obj.press_softkey(4)
                self.verifyDisplayMessageUtil("Cancel")
                self.phone_obj.press_softkey(4)

            elif self.phone_obj.phone_type in ("Mitel6930", "Mitel6940"):
                console('Inside TransferWpd')
                self.verifyDisplayMessageUtil("Consult")
                self.verifyDisplayMessageUtil("Backspace")
                self.verifyDisplayMessageUtil("Transfer")
                self.verifyDisplayMessageUtil("Cancel")

        elif phoneState == "Directory":
            if (self.phone_obj.phone_type == "Mitel6920"):
                self.verifyDisplayMessageUtil("Enterprise")
                self.verifyDisplayMessageUtil("Directory")
                self.verifyDisplayMessageUtil("Quit")
            elif (self.phone_obj.phone_type in ("Mitel6930", "Mitel6940")):
                self.verifyDisplayMessageUtil("Enterprise")
                self.verifyDisplayMessageUtil("Mobile Contacts")
                self.verifyDisplayMessageUtil("Directory")
                self.verifyDisplayMessageUtil("Quit")

        elif phoneState == "Menu":
            if (self.phone_obj.phone_type == "Mitel6930"):
                self.verifyDisplayMessageUtil("Availability")
                self.phone_obj.press_key("ScrollRight")
                self.verifyDisplayMessageUtil("Time and Date")
                self.phone_obj.press_key("ScrollRight")
                self.verifyDisplayMessageUtil("Wi-Fi")
                self.phone_obj.press_key("ScrollRight")
                self.verifyDisplayMessageUtil("Directory")
                self.phone_obj.press_key("ScrollRight")
                self.verifyDisplayMessageUtil("Status")
                self.phone_obj.press_key("ScrollRight")
                self.verifyDisplayMessageUtil("Bluetooth")
                self.phone_obj.press_key("ScrollRight")
                self.verifyDisplayMessageUtil("Unassign user")
                self.phone_obj.press_key("ScrollRight")
                self.verifyDisplayMessageUtil("Diagnostics")
                self.phone_obj.press_key("ScrollRight")
                self.verifyDisplayMessageUtil("Audio Mode")
                self.phone_obj.press_key("ScrollRight")
                self.verifyDisplayMessageUtil("Display")
                self.phone_obj.press_key("ScrollRight")
                self.verifyDisplayMessageUtil("Program Keys")
                self.phone_obj.press_key("ScrollRight")
                self.verifyDisplayMessageUtil("Restart")
            elif (self.phone_obj.phone_type == "Mitel6940"):
                self.verifyDisplayMessageUtil("Availability")
                self.verifyDisplayMessageUtil("Time and Date")
                self.verifyDisplayMessageUtil("Status")
                self.verifyDisplayMessageUtil("Bluetooth")
                self.verifyDisplayMessageUtil("Wi-Fi")
                self.verifyDisplayMessageUtil("Directory")
                self.verifyDisplayMessageUtil("Unassign user")
                self.verifyDisplayMessageUtil("Audio")
                self.verifyDisplayMessageUtil("Display")
                self.phone_obj.change_options_menu_page("Page2")
                self.verifyDisplayMessageUtil("Program Keys")
                self.verifyDisplayMessageUtil("Restart")
            # elif (self.phone_obj.phone_type == "Mitel6920"):
            # self.phone_obj.press_key("ScrollRight")

            # self.verifyDisplayMessageUtil("Diagnostics")
            # self.phone_obj.press_key("ScrollRight")
            # self.verifyDisplayMessageUtil("Audio")
            # self.phone_obj.press_key("ScrollRight")
            # self.verifyDisplayMessageUtil("Display")
            # self.phone_obj.press_key("ScrollRight")
            # self.phone_obj.press_key("ScrollRight")
            # self.verifyDisplayMessageUtil("Restart")

        elif phoneState == "Cancel":
            if (self.phone_obj.phone_type in ("Mitel6930", "Mitel6940")):
                self.verifyDisplayMessageUtil("Cancel")

            elif (self.phone_obj.phone_type == "Mitel6920"):
                self.phone_obj.press_softkey(4)
                self.verifyDisplayMessageUtil("Cancel")
                self.phone_obj.press_softkey(4)

        elif phoneState == "Park":
            if (self.phone_obj.phone_type in ("Mitel6930", "Mitel6940")):
                self.verifyDisplayMessageUtil("Park")
            elif (self.phone_obj.phone_type == "Mitel6920"):
                self.phone_obj.press_softkey(4)
                self.verifyDisplayMessageUtil("Park")
                self.phone_obj.press_softkey(4)

        elif phoneState == "Call History":
            if (self.phone_obj.phone_type in ("Mitel6920", "Mitel6930", "Mitel6940",)):
                self.verifyDisplayMessageUtil("Call History")
                self.verifyDisplayMessageUtil("All")
                self.verifyDisplayMessageUtil("Missed")
                self.verifyDisplayMessageUtil("Outgoing")
                self.verifyDisplayMessageUtil("Received")
                self.verifyDisplayMessageUtil("Delete")
                self.verifyDisplayMessageUtil("Quit")

        elif phoneState == "VoicemailDelete":
            logger.error("Add condition here!!")

        elif phoneState == "Restart":
            if self.phone_obj.phone_type == "Mitel6920":
                for i in range(6):
                    self.phone_obj.press_key("ScrollRight")
            elif self.phone_obj.phone_type == "Mitel6930":
                for i in range(7):
                    self.phone_obj.press_key("ScrollRight")
            elif self.phone_obj.phone_type == "Mitel6940":
                logger.error("Not implemented for 6940")
            self.verifyDisplayMessageUtil("Quit")

        elif phoneState == "Availability":
            if self.phone_obj.phone_type == "Mitel6920" or self.phone_obj.phone_type == "Mitel6930":
                for i in range(3):
                    self.phone_obj.press_key("ScrollLeft")
            elif self.phone_obj.phone_type == "Mitel6940":
                logger.error("Not implimented for 6940")
            self.verifyDisplayMessageUtil("Quit")

        elif phoneState == "Availability":
            self.verifyDisplayMessageUtil("Deflect")
            self.verifyDisplayMessageUtil("Backspace")
            self.verifyDisplayMessageUtil("Cancel")

        else:
            raise Exception("Check the arguments passed %s" % kwargs)

    def addUserInConferenceCall(self, **kwargs):
        """
        This method adds a new member in a conference call.
        :param:
            :self: PhoneComponent object
            :phoneObj: PhoneComponent object of the phone to be added in conference

        :returns: None
        :created by: Abhishek Pathak
        :last update by: Vikhyat Sharma
        :last update date: 25/11/2019
        """

        if len(kwargs) >= 1:
            phoneObj = kwargs['phoneObj']

            logger.info("Adding the extension: <b>" + phoneObj.phone_obj.phone_obj.phone.extensionNumber
                        + "</b> in conference call on extension: <b>" + self.phone_obj.phone_obj.phone.extensionNumber
                        + "</b>.", html=True)

            console("Adding the extension: " + phoneObj.phone_obj.phone_obj.phone.extensionNumber
                    + " in conference call on extension: " + self.phone_obj.phone_obj.phone.extensionNumber)

            self.phone_obj.sleep(3)
            if self.phone_obj.phone_type in ["Mitel6910", "Mitel6865i"]:
                self.phone_obj.press_key("Conference")
            else:
                self.phone_obj.press_softkey(2)
            self.phone_obj.sleep(3)

            self.phone_obj.dial_number(phoneObj.phone_obj.phone_obj.phone.extensionNumber)
            self.phone_obj.sleep(5)
            if phoneObj.phone_obj.phone_type in ('Mitel6865i', "Mitel6910"):
                phoneObj.phone_obj.press_key("HandsFree")
            else:
                phoneObj.phone_obj.press_softkey(1)
            phoneObj.phone_obj.sleep(4)

            if self.phone_obj.phone_type in ('Mitel6865i', "Mitel6910"):
                self.phone_obj.press_key("Conference")
            else:
                self.phone_obj.press_softkey(2)
            phoneObj.phone_obj.sleep(5)

            phoneObj.verifyDisplayMessageUtil("Conference")

            if not phoneObj.phone_obj.phone_type == "Mitel6910":
                phoneObj.verifyDisplayMessageUtil("Show")
            phoneObj.phone_obj.sleep(5)
        else:
            raise Exception("Check the arguments passed %s" % kwargs)

    def holdUnhold(self, **kwargs):
        """
        This routine is used for hold/unhold the call & verifying the line state.
        :param:
            :hold_unhold:- Hold/Unhold the call

        :ret None
        :created by: Avishek Ranjan
        :creation date: 24/07/2019
        :last update by: Vikhyat Sharma
        :last update on: 04/02/2021
        """
        self.phone_obj.sleep(3)
        if len(kwargs) >= 2:
            lineKey = kwargs['line']
            holdUnhold = kwargs['hold_unhold']
            pbx = kwargs['pbx']

            logger.info("Putting the <b>" + lineKey + "</b> on <b>" + holdUnhold + "</b> on extension: "
                        + self.phone_obj.phone_obj.phone.extensionNumber)
            console("Putting the " + lineKey + " on " + holdUnhold + " on extension: "
                    + self.phone_obj.phone_obj.phone.extensionNumber)
            self.phone_obj.press_hold()
            self.phone_obj.sleep(5)

            if holdUnhold == "hold":
                if self.phone_obj.phone_type == "Mitel6940":
                    if pbx in ('MiVoice', 'MiCloud'):
                        self.verifyLineIconState(line=lineKey, state='CALL_APPEARANCE_LOCAL_HOLD')
                    else:
                        self.verifyLineIconState(line=lineKey, state='SOFT_LINE_HOLD')
                else:
                    if self.phone_obj.verify_led_state(lineKey, 'blink', 10):
                        logger.info("<b>" + lineKey + "</b> has been put on hold state for extension: %s"
                                    % self.phone_obj.phone_obj.phone.extensionNumber)
                        console(lineKey + " hold state verified for extension: %s"
                                % self.phone_obj.phone_obj.phone.extensionNumber)
                    else:
                        raise Exception(lineKey + " could not be put on hold state for extension: %s"
                                        % self.phone_obj.phone_obj.phone.extensionNumber)

            elif holdUnhold == "Unhold":
                if self.phone_obj.phone_type == "Mitel6940":
                    if pbx in ('MiVoice', 'MiCloud'):
                        self.verifyLineIconState(line=lineKey, state='CALL_APPEARANCE_ACTIVE')
                    else:
                        self.verifyLineIconState(line=lineKey, state='SOFT_LINE_ACTIVE')
                else:
                    if self.phone_obj.verify_led_state(lineKey, 'on', 10):
                        logger.info("<b>" + lineKey + " Unhold state </b>verified for extension: %s"
                                    % self.phone_obj.phone_obj.phone.extensionNumber, html=True)

                        console(lineKey + " Unhold state verified for extension: %s"
                                % self.phone_obj.phone_obj.phone.extensionNumber)
                    else:
                        raise Exception(lineKey + " Unhold state verification failed for extension: %s"
                                        % self.phone_obj.phone_obj.phone.extensionNumber)
            else:
                raise Exception("Check the passed argument for hold/Unhold")
        else:
            raise Exception("Please check the arguments passed for: %s" % kwargs)
        self.phone_obj.sleep(5)

    def verify_call_hold_unhold(self, **kwargs):
        """
        this verify line state for hold/unhold
        :param kwargs:
        :return:
        """
        self.phone_obj.sleep(3)
        self.value ={}
        if len(kwargs) >= 2:
            lineKey = kwargs['line']
            state = kwargs['hold_unhold']
            pbx = kwargs['pbx']

            logger.info("checking the <b>" + lineKey + "</b> on <b>" + state + "</b> on extension: "
                        + self.phone_obj.phone_obj.phone.extensionNumber, html=True)
            console("checking the " + lineKey + " on " + state + " on extension: "
                    + self.phone_obj.phone_obj.phone.extensionNumber)

            self.phone_obj.sleep(5)

            if state == "hold":
                if self.phone_obj.phone_type == "Mitel6940":
                    if pbx in ('MiVoice', 'MiCloud'):
                        self.verifyLineIconState(line=lineKey, state='CALL_APPEARANCE_LOCAL_HOLD')
                    else:
                        self.verifyLineIconState(line=lineKey, state='SOFT_LINE_HOLD')
                else:
                    value = {"ledType":lineKey , "ledMode":"blink"}
                    if self.verifyLedState(**value):
                        logger.info("<b>" + lineKey + "</b> is on hold state for extension: %s"
                                    % self.phone_obj.phone_obj.phone.extensionNumber, html=True)
                        console(lineKey + " hold state verified for extension: %s"
                                % self.phone_obj.phone_obj.phone.extensionNumber)
                    else:
                        raise Exception(lineKey + " could not be verify on hold state for extension: %s"
                                        % self.phone_obj.phone_obj.phone.extensionNumber)

            elif state == "Unhold":
                if self.phone_obj.phone_type == "Mitel6940":
                    if pbx in ('MiVoice', 'MiCloud'):
                        self.verifyLineIconState(line=lineKey, state='CALL_APPEARANCE_ACTIVE')
                    else:
                        self.verifyLineIconState(line=lineKey, state='SOFT_LINE_ACTIVE')
                else:
                    value = {"ledType":lineKey , "ledMode":"on"}
                    if self.verifyLedState(**value):
                        logger.info("<b>" + lineKey + " Unhold state </b>verified for extension: %s"
                                    % self.phone_obj.phone_obj.phone.extensionNumber, html=True)

                        console(lineKey + " Unhold state verified for extension: %s"
                                % self.phone_obj.phone_obj.phone.extensionNumber)
                    else:
                        raise Exception(lineKey + " Unhold state verification failed for extension: %s"
                                        % self.phone_obj.phone_obj.phone.extensionNumber)
            else:
                raise Exception("Check the passed argument for hold/Unhold")
        else:
            raise Exception("Please check the arguments passed for: %s" % kwargs)
        self.phone_obj.sleep(5)


    def pressSoftkey(self, **kwargs):
        """
        This method presses the passed softkeys on the phone.

        :param:
            :self: PhoneComponent object
            :Softkey: Softkey to press

        :returns: None
        :created by:
        :creation date:
        :last updated by: Vikhyat Sharma
        :last update on: 23/11/2020
        """
        self.phone_obj.sleep(8)
        phoneType = self.phone_obj.phone_obj.phone.phoneModel
        softKey = str(kwargs['Softkey'])

        logger.info("Pressed the <b>" + softKey + "</b> on extension: <b>"
                    + self.phone_obj.phone_obj.phone.extensionNumber + "</b>.", html=True)
        console("Pressed the " + softKey + " on extension: " + self.phone_obj.phone_obj.phone.extensionNumber)

        if softKey == "More":
            if self.phone_obj.phone_type == 'Mitel6920':
                self.phone_obj.press_softkey(4)
            elif self.phone_obj.phone_type == 'Mitel6930':
                self.phone_obj.press_softkey(5)
            elif self.phone_obj.phone_type == 'Mitel6940':
                # self.phone_obj.press_softkey(6)
                self.phone_obj.press_key('BottomKey6')
            else:
                raise Exception("Phone model: " + self.phone_obj.phone_type + " is not supported by this method.")
        else:
            softKeyValue = int(filter(str.isdigit, softKey))
            self.phone_obj.press_softkey(softKeyValue)

    def pressKeys(self, **kwargs):
        """
        This method presses the soft-keys based on the set type of the phone.
        :param:
            :self: PhoneComponent object
            :keyName: Softkey to press

        :returns: None
        :created by:
        :creation date:
        :last updated by: Vikhyat Sharma
        :last update on: 23/11/2020
        """
        self.phone_obj.sleep(2)
        phoneType = self.phone_obj.phone_obj.phone.phoneModel
        key = str(kwargs['keyName'])

        logger.info("Pressed the <b>" + key + "</b> on extension: <b>"
                    + self.phone_obj.phone_obj.phone.extensionNumber + "</b>.", html=True)
        console("Pressed the " + key + " on extension: " + self.phone_obj.phone_obj.phone.extensionNumber)

        if key.lower() in ('close', 'quit', 'cancel'):
            if phoneType == "Mitel6920":
                self.phone_obj.press_softkey(4)
            elif phoneType == "Mitel6930":
                self.phone_obj.press_softkey(5)
            elif phoneType == 'Mitel6940':
                self.phone_obj.press_key('BottomKey6')
                # self.phone_obj.press_softkey(6)

        elif key == "Details":
            if phoneType == "Mitel6920":
                self.phone_obj.press_softkey(3)
            elif phoneType == "Mitel6930":
                self.phone_obj.press_softkey(4)
            elif phoneType == 'Mitel6940':
                self.phone_obj.press_softkey(5)

        elif key == "Save":
            if phoneType in ('Mitel6865i', "Mitel6910"):
                self.phone_obj.press_key('Enter')
            else:
                self.phone_obj.press_softkey(1)

        elif key == "Park":
            if phoneType == "Mitel6920":
                self.phone_obj.press_softkey(4)
                self.phone_obj.press_softkey(1)
            elif phoneType in ("Mitel6930", 'Mitel6940'):
                self.phone_obj.press_softkey(4)
            else:
                raise Exception(
                    "Phone model: " + self.phone_obj.phone_type + " is not supported by pressKeys method for"
                    + key + " softkey.")

        elif key == "More":
            if self.phone_obj.phone_type == 'Mitel6920':
                self.phone_obj.press_softkey(4)
            elif self.phone_obj.phone_type == 'Mitel6930':
                self.phone_obj.press_softkey(5)
            elif self.phone_obj.phone_type == 'Mitel6940':
                self.phone_obj.press_key('BottomKey6')
                # self.phone_obj.press_softkey(6)
            else:
                raise Exception(
                    "Phone model: " + self.phone_obj.phone_type + " is not supported by pressKeys method for"
                    + key + " softkey.")
        else:
            raise Exception("Please check the arguments passed for: %s" % kwargs)

    def pressHardkey(self, **kwargs):
        """
        This method presses the hard keys available on the phone.
        :param:
            :self: PhoneComponent object
            :hardKey: Hard key to press on the phone.

        :returns: None
        :created by:
        :creation date:
        :last updated by: Sharma
        :last update on: 25/11/2019
        """

        if len(kwargs) >= 1:
            hardKey = kwargs['key']
            logger.info("Pressing hardkey: <b>" + hardKey + "</b> on extension: <b>"
                        + self.phone_obj.phone_obj.phone.extensionNumber + "</b>.", html=True)
            console("Pressing hardkey: " + hardKey + " on extension: " + self.phone_obj.phone_obj.phone.extensionNumber)

            self.phone_obj.press_key(hardKey)
        else:
            raise Exception("Please check the arguments passed: %s" % kwargs)
        self.phone_obj.sleep(3)

    def pressHardkeynavigation(self, **kwargs):
        """
        This method is used to navigate between the different held/active calls using navigation keys.
        :param:
            :self: PhoneComponent object
            :hardKey: Navigation key to press i.e, ScrollLeft/ScrollRight/ScrollUp/ScrollDown

        :returns: None
        :created by:
        :creation date:
        :last updated by: Vikhyat Sharma
        :last update on: 23/11/2020
        """

        if len(kwargs) >= 1:
            hardKey = kwargs['key']
            number = int(kwargs['number'])
            logger.info("Pressing <b>" + self.phone_obj.phone_obj.phone.extensionNumber
                        + "</b> to navigate between different calls on extension: <b>"
                        + self.phone_obj.phone_obj.phone.extensionNumber + "</b>", html=True)

            console("Pressing " + self.phone_obj.phone_obj.phone.extensionNumber
                    + " to navigate between different calls on extension: "
                    + self.phone_obj.phone_obj.phone.extensionNumber)

            if self.phone_obj.phone_type not in ('Mitel6865i', "Mitel6910"):
                for i in range(number + 1):
                    self.phone_obj.press_key(hardKey)
            else:
                if "ScrollUp" in hardKey:
                    for i in range(number):
                        self.phone_obj.press_key("ScrollLeft")
                else:
                    for i in range(number):
                        self.phone_obj.press_key("ScrollRight")
        else:
            raise Exception("Please check the arguments passed: %s" % kwargs)

        self.phone_obj.sleep(5)

    def verifyLineState(self, **kwargs):
        """
        This method verifies the passed state for Line 1 on the phone.
        :param:
            :self: PhoneComponent object
            :lineState: Line State to verify

        :returns: None
        :created by:
        :creation date:
        :last updated by: Sharma
        :last update on: 25/11/2019

        """
        if (len(kwargs) >= 1):
            lineState = kwargs['lineState']
            if (self.phone_obj.verify_line_state(lineState)):
                logger.info("Verified the line state for extension %s" % self.phone_obj.phone_obj.phone.extensionNumber)
            else:
                logger.error("Verification of line state failed for extension %s"
                             % self.phone_obj.phone_obj.phone.extensionNumber)
                raise Exception("Verification of line state failed for extension %s"
                                % self.phone_obj.phone_obj.phone.extensionNumber)
        else:
            raise Exception("Please check the arguments passed: %s" % kwargs)

    def verifyLedState(self, **kwargs):
        """
        This method verifies the led state of the line keys on the phone.

        Keyword Args:
            ledType: Key to verify LED of e.g., LineN, mute, speaker
            ledMode: LED Mode to verify i.e., On/Blink/Off
            ledColor: LED Color to verify (Optional)

        :returns: None
        :created by:
        :creation date:
        :last updated by: Vikhyat Sharma
        :last update on: 20/12/2020
        """
        if len(kwargs) >= 2:
            ledType = kwargs['ledType']
            ledMode = kwargs['ledMode']
            ledColor = kwargs.get('ledColor', '')
            extensionNum = self.phone_obj.phone_obj.phone.extensionNumber

            if ledType == "Mute":
                ledType = ledType.lower()

            if self.phone_obj.phone_type in ('Mitel6865i', 'Mitel6867i', 'Mitel6869i'):
                if ledType == 'Line1':
                    ledType = 'indicator_line_1'
                elif ledType == 'Line2':
                    ledType = 'indicator_line_2'

            if self.phone_obj.phone_type in ('Mitel6865i', 'Mitel6910'):
                ledColor = ''
                logger.warn("Lower-end models does not support LED Color Verification!!")
            else:
                if not ledColor:    # if there is no LED color specified by the TC, then set the default values
                    if ledType in ('message_waiting', 'speaker', 'mute'):
                        ledColor = 'RED'
                    else:
                        if self.phone_obj.phone_type in ('Mitel6867i', 'Mitel6869i'):
                            if ledType in ('indicator_line_1', 'indicator_line_2'):
                                ledColor = 'GREEN'
                            else:
                                ledColor = 'RED'
                        else:
                            ledColor = 'RED'

            self.phone_obj.sleep(2)
            if self.phone_obj.phone_type == 'Mitel6940':
                logger.warn("Mitel6940 set does not have LEDs verification!!")
            else:
                if self.phone_obj.verify_led_state(ledType, ledMode, ledColor):
                    if ledColor:
                        logger.info("LED state of <b>" + ledType + "</b> verified as <b>"
                                    + ledMode + "</b> with <b>" + ledColor + "</b> color on " + extensionNum, html=True)
                        console("LED state of " + ledType + " verified as "
                                + ledMode + " with " + ledColor + " color on " + extensionNum)
                    else:
                        logger.info("LED state of <b>" + ledType + "</b> verified as <b>"
                                    + ledMode + "</b> on " + extensionNum, html=True)
                        console("LED state of " + ledType + " verified as "
                                + ledMode + " on " + extensionNum)
                    return True
                else:
                    actualState = ''.join([ledState for ledState in ('on', 'off', 'blink') if
                                           self.phone_obj.verify_led_state(ledType, ledState)])
                    if actualState == ledMode:
                        exceptionMsg = "LED state of {0} as {1} failed on {2} color verification on {3}".format(
                                        ledType, ledMode, ledColor, extensionNum)
                    else:
                        exceptionMsg = "LED state verification of {0} as {1} failed on {2}. Got {3} " \
                                       "state instead!!".format(ledType, ledMode, extensionNum, actualState)
                    raise Exception(exceptionMsg)
        else:
            raise Exception("LESS NUMBER OF ARGUMENTS PASSED!!" % kwargs)

    def transferCall(self, **kwargs):
        """
        This method is used to transfer the call from one phone to other phone.

        Keyword Args:
            phoneObj: PhoneComponent object
            transferMode: BlindTransfer/ConsultiveTransfer/SemiAttendedTransfer

        :returns: None
        :created by: Sharma
        :creation date: 11/01/2019
        :updated by: Vikhyat Sharma
        :last update date: 07/12/2020
        """
        if len(kwargs) >= 1:
            phoneObj = kwargs['phoneObj']
            transferMode = kwargs['transferMode']

            logger.info("Transferring the call from extension: <b>" + self.phone_obj.phone_obj.phone.extensionNumber
                        + "</b> to extension: <b>" + phoneObj.phone_obj.phone_obj.phone.extensionNumber
                        + "</b> using <b>" + transferMode + "</b> mode.", html=True)

            console("Transferring the call from extension: " + self.phone_obj.phone_obj.phone.extensionNumber
                    + " to extension: " + phoneObj.phone_obj.phone_obj.phone.extensionNumber
                    + " using " + transferMode + " mode.")

            if not self.phone_obj.verify_display_message_contents("Merge"):
                if self.phone_obj.phone_type in ("Mitel6920", "Mitel6930", "Mitel6867i", 'Mitel6940'):
                    self.phone_obj.press_softkey(3)
                elif self.phone_obj.phone_type in ("Mitel6910", "Mitel6865i"):
                    self.phone_obj.press_key("Transfer")
                else:
                    raise Exception("INVALID PHONE TYPE {} USED!!".format(self.phone_obj.phone_type))
            else:
                if self.phone_obj.phone_type in ('Mitel6930', 'Mitel6940'):
                    self.phone_obj.press_softkey(4)
                elif self.phone_obj.phone_type in ["Mitel6920", "Mitel6867i"]:
                    self.phone_obj.press_softkey(4)
                    self.phone_obj.sleep(1)
                    self.phone_obj.press_softkey(1)
                elif self.phone_obj.phone_type in ("Mitel6910", "Mitel6865i"):
                    self.phone_obj.press_key("Transfer")
                else:
                    raise Exception("INVALID PHONE TYPE {} USED!!".format(self.phone_obj.phone_type))

            self.phone_obj.sleep(1)

            if self.phone_obj.phone_type not in ("Mitel6910", "Mitel6865i"):
                self.verifyDisplayMessageUtil(">")

            self.phone_obj.enter_a_number(phoneObj.phone_obj.phone_obj.phone)
            self.phone_obj.sleep(1)

            if transferMode == "BlindTransfer":
                if self.phone_obj.phone_type in ["Mitel6930", "Mitel6920", "Mitel6867i", 'Mitel6940']:
                    self.phone_obj.press_softkey(3)
                elif self.phone_obj.phone_obj.phone.phoneModel in ("Mitel6910", "Mitel6865i"):
                    self.phone_obj.press_key("Transfer")

                self.phone_obj.sleep(2)
                if self.phone_obj.phone_type not in ("Mitel6910", "Mitel6865i"):
                    self.verifyDisplayMessageUtil("Call Transferred")

            elif transferMode == "ConsultiveTransfer":
                if self.phone_obj.phone_obj.phone.phoneModel in ("Mitel6930", "Mitel6920", "Mitel6867i", 'Mitel6940'):
                    self.phone_obj.press_softkey(1)  # consult
                elif self.phone_obj.phone_obj.phone.phoneModel in ("Mitel6910", "Mitel6865i"):
                    self.phone_obj.press_key("ScrollRight")

                if self.phone_obj.phone_type in ("Mitel6930", "Mitel6920", "Mitel6867i", 'Mitel6940'):
                    self.verifyDisplayMessageUtil("Transfer")
                    self.verifyDisplayMessageUtil("Cancel")

                self.phone_obj.sleep(2)

                if phoneObj.phone_obj.phone_obj.phone.phoneModel in ("Mitel6910", "Mitel6865i"):
                    phoneObj.phone_obj.press_key("HandsFree")
                else:
                    phoneObj.phone_obj.press_softkey(1)
                self.phone_obj.sleep(2)

                if self.phone_obj.phone_obj.phone.phoneModel in ("Mitel6930", "Mitel6920", "Mitel6867i"):
                    self.phone_obj.press_softkey(3)  # transfer
                elif self.phone_obj.phone_obj.phone.phoneModel in ("Mitel6910", "Mitel6865i"):
                    self.phone_obj.press_key("Transfer")
                elif self.phone_obj.phone_type == 'Mitel6940':
                    self.phone_obj.press_softkey(3)
                else:
                    raise Exception("UNSUPPORTED PHONE TYPE({}) PASSED!!".format(self.phone_obj.phone_type))

                self.phone_obj.sleep(1)
                if self.phone_obj.phone_type not in ("Mitel6910", "Mitel6865i"):
                    self.verifyDisplayMessageUtil("Call Transferred")

            elif transferMode == "SemiAttendedTransfer":
                if self.phone_obj.phone_obj.phone.phoneModel in ("Mitel6930", "Mitel6920", "Mitel6867i", 'Mitel6940'):
                    self.phone_obj.press_softkey(1)  # consult
                elif self.phone_obj.phone_obj.phone.phoneModel in ("Mitel6910", "Mitel6865i"):
                    self.phone_obj.press_key("ScrollRight")  # consult

                phoneObj.verifyDisplayMessageUtil(self.phone_obj.phone_obj.phone.extensionNumber)

                if self.phone_obj.phone_type in ("Mitel6920", "Mitel6867i"):
                    self.phone_obj.press_softkey(3)
                elif self.phone_obj.phone_type in ("Mitel6930", "Mitel6869i"):
                    self.phone_obj.press_softkey(4)
                elif self.phone_obj.phone_type in ("Mitel6910", "Mitel6865i"):
                    self.phone_obj.press_key("Transfer")
                elif self.phone_obj.phone_type == 'Mitel6940':
                    self.phone_obj.press_softkey(5)
                else:
                    raise Exception("UNSUPPORTED PHONE TYPE ({}) PASSED!!".format(self.phone_obj.phone_type))

                if self.phone_obj.phone_type not in ("Mitel6910", "Mitel6865i"):
                    self.verifyDisplayMessageUtil("Call Transferred")
                self.phone_obj.sleep(2)

                if phoneObj.phone_obj.phone_obj.phone.phoneModel in ("Mitel6910", "Mitel6865i"):
                    phoneObj.phone_obj.press_key("HandsFree")
                else:
                    phoneObj.phone_obj.press_softkey(1)

            elif transferMode == "unattendedtransfer":
                if self.phone_obj.phone_type in ('Mitel6920', 'Mitel6930', 'Mitel6940'):
                    self.phone_obj.press_softkey(2)
                elif self.phone_obj.phone_type in ('Mitel6865i', "Mitel6910"):
                    self.phone_obj.press_key("ScrollRight")
                self.phone_obj.sleep(2)

            elif transferMode == "temp":
                if self.phone_obj.phone_type in ('Mitel6920', 'Mitel6930', 'Mitel6940'):
                    self.phone_obj.press_softkey(1)  # consult
                elif self.phone_obj.phone_type in ('Mitel6865i', "Mitel6910"):
                    self.phone_obj.press_key("ScrollRight")
                self.phone_obj.sleep(2)

            else:
                raise Exception("INVALID TRANSFER MODE ({}) PASSED!!".format(transferMode))

        else:
            raise Exception("Check the arguments passed behind %s" % kwargs)

    def forwardCall(self, **kwargs):
        """
        This method is used to forward calls to other phone in different conditions.

        Keyword Args:
            phoneObj: PhoneComponent object
            forwardMode: Unconditional/NoResponse/Busy/DND

        :param kwargs:
        :return: None
        :created by: Vijay Pawar
        :creation date: 07/05/2021

        """
        if len(kwargs) >= 1:
            phoneObj = kwargs['phoneObj']
            forwardMode = kwargs['forwardMode']
            self.number = ''
            logger.info("Forwarding the call from extension: <b>" + self.phone_obj.phone_obj.phone.extensionNumber
                        + "</b> to extension: <b>" + phoneObj.phone_obj.phone_obj.phone.extensionNumber
                        + "</b> using <b>" + forwardMode + "</b> mode.", html=True)

            console("Forwarding the call from extension: " + self.phone_obj.phone_obj.phone.extensionNumber
                    + " to extension: " + phoneObj.phone_obj.phone_obj.phone.extensionNumber
                    + " using " + forwardMode + " mode.")

            if forwardMode == 'Unconditional':
                number = '*21' + str(phoneObj.phone_obj.phone_obj.phone.extensionNumber)
                self.phone_obj.input_a_number(number)
                self.phone_obj.sleep(1)
                if self.phone_obj.phone_obj.phone.phoneModel in ("Mitel6910", "Mitel6865i"):
                    self.phone_obj.press_key("OffHook")
                else:
                    self.phone_obj.press_softkey(1)
                self.phone_obj.sleep(10)
                try:
                  if self.phone_obj.phone_obj.phone.phoneModel not in ("Mitel6910", "Mitel6865i"):
                    self.verifyDisplayMessageUtil(
                        "CFU user " + phoneObj.phone_obj.phone_obj.phone.phoneName + " "+str(
                           phoneObj.phone_obj.phone_obj.phone.extensionNumber))
                  else:
                      logger.warn("Model :" + self.phone_obj.phone_type + " has not display verification")
                      pass
                except:
                    time.sleep(5)
                    if self.phone_obj.phone_obj.phone.phoneModel not in ("Mitel6910", "Mitel6865i"):
                      self.verifyDisplayMessageUtil(
                          "CFU user " + phoneObj.phone_obj.phone_obj.phone.phoneName + " " + str(
                              phoneObj.phone_obj.phone_obj.phone.extensionNumber))
                    else:
                        logger.warn("Model :" + self.phone_obj.phone_type + " has not display verification")
                        pass

            elif forwardMode == 'NoResponse':
                number = '*61' + str(phoneObj.phone_obj.phone_obj.phone.extensionNumber)
                self.phone_obj.input_a_number(number)
                self.phone_obj.sleep(1)
                if self.phone_obj.phone_obj.phone.phoneModel in ("Mitel6910", "Mitel6865i"):
                    self.phone_obj.press_key("OffHook")
                else:
                    self.phone_obj.press_softkey(1)
                self.phone_obj.sleep(10)
                try:
                  if self.phone_obj.phone_obj.phone.phoneModel not in ("Mitel6910", "Mitel6865i"):
                    self.verifyDisplayMessageUtil(
                        "CFNR " + phoneObj.phone_obj.phone_obj.phone.phoneName + " "+str(
                            phoneObj.phone_obj.phone_obj.phone.extensionNumber))
                  else:
                      logger.warn("Model :" + self.phone_obj.phone_type + " has not display verification")
                      pass
                except:
                  time.sleep(5)
                  if self.phone_obj.phone_obj.phone.phoneModel not in ("Mitel6910", "Mitel6865i"):
                      self.verifyDisplayMessageUtil(
                          "CFNR " + phoneObj.phone_obj.phone_obj.phone.phoneName + " " + str(
                              phoneObj.phone_obj.phone_obj.phone.extensionNumber))
                  else:
                      logger.warn("Model :" + self.phone_obj.phone_type + " has not display verification")
                      pass

            elif forwardMode == 'Busy':
                number = '*67' + str(phoneObj.phone_obj.phone_obj.phone.extensionNumber)
                self.phone_obj.input_a_number(number)
                self.phone_obj.sleep(1)
                if self.phone_obj.phone_obj.phone.phoneModel in ("Mitel6910", "Mitel6865i"):
                    self.phone_obj.press_key("OffHook")
                else:
                    self.phone_obj.press_softkey(1)
                self.phone_obj.sleep(10)
                try:
                    if self.phone_obj.phone_obj.phone.phoneModel not in ("Mitel6910", "Mitel6865i"):
                      self.verifyDisplayMessageUtil(
                         "Forw. busy " + phoneObj.phone_obj.phone_obj.phone.phoneName + " "+str(
                            phoneObj.phone_obj.phone_obj.phone.extensionNumber))
                    else:
                        logger.warn("Model :" + self.phone_obj.phone_type + " has not display verification")
                        pass
                except:
                    time.sleep(5)
                    if self.phone_obj.phone_obj.phone.phoneModel not in ("Mitel6910", "Mitel6865i"):
                      self.verifyDisplayMessageUtil(
                          "Forw. busy " + phoneObj.phone_obj.phone_obj.phone.phoneName + " " + str(
                              phoneObj.phone_obj.phone_obj.phone.extensionNumber))
                    else:
                        logger.warn("Model :" + self.phone_obj.phone_type + " has not display verification")
                        pass

            elif forwardMode == 'DND':
                number = '*26'
                self.phone_obj.input_a_number(number)
                self.phone_obj.sleep(1)
                if self.phone_obj.phone_obj.phone.phoneModel in ("Mitel6910", "Mitel6865i"):
                    self.phone_obj.press_key("OffHook")
                else:
                    self.phone_obj.press_softkey(1)
                self.phone_obj.sleep(10)
                try:
                    if self.phone_obj.phone_obj.phone.phoneModel not in ("Mitel6910", "Mitel6865i"):
                      self.verifyDisplayMessageUtil("Do not disturb (forw.)")
                    else:
                        logger.warn("Model :" + self.phone_obj.phone_type + " has not display verification")
                        pass
                except:
                    time.sleep(5)
                    if self.phone_obj.phone_obj.phone.phoneModel not in ("Mitel6910", "Mitel6865i"):
                      self.verifyDisplayMessageUtil("Do not disturb (forw.)")
                    else:
                        logger.warn("Model :" + self.phone_obj.phone_type + " has not display verification")
                        pass

            else:
                raise Exception("INVALID TRANSFER MODE ({}) PASSED!!".format(forwardMode))


        else:
            raise Exception("Check the arguments passed behind %s" % kwargs)


    def openRedialList(self):
        """

        This method is used to disapy redial list on terminal
        :return: boolean result

        :created by: Vijay Pawar
        :creation date: 10/05/2021
        :Updated by:
        :last update date:
        """


        time.sleep(1)
        self.phone_obj.press_key('Redial')
        time.sleep(2)
        if not self.phone_obj.phone_type in ("Mitel6865i", "Mitel6910"):

            if self.phone_obj.verify_display_message_contents("Redial list"):
                logger.info("Redial list for : <b>"+ self.phone_obj.phone_obj.phone
                            .extensionNumber + "</b> is displayed.", html=True)
                console("Redial list for : "+ self.phone_obj.phone_obj.phone
                            .extensionNumber + " is displayed.")
                return True
            elif self.phone_obj.verify_display_message_contents("Phone lock"):
                logger.error("<b> Please change default PIN ,to see redial list on : " +
                            self.phone_obj.phone_obj.phone.extensionNumber + " </b>.", html=True)
                console("Please change default PIN for : "+
                        self.phone_obj.phone_obj.phone.extensionNumber)
                return False
        else:
            logger.warn(self.phone_obj.phone_type + " has no display verification.")


    def redialNumber(self ,**kwargs):
        """
        This method is used to call a number in redial list.

        :param kwargs: phoneObj = Number to be dialed.
        :return:
        :created by: Vijay Pawar
        :creation date: 10/05/2021
        :Updated by:
        :last update date:

        """
        time.sleep(1)

        phoneObj = kwargs['phoneObj']
        phoneName = phoneObj.phone_obj.phone_obj.phone.phoneName
        if not self.phone_obj.phone_type in ("Mitel6910", "Mitel6865i"):
            while 1:
                if self.phone_obj.verify_display_message_contents(phoneName):
                 break
                self.phone_obj.press_key("ScrollDown")
                self.phone_obj.sleep(1)

            while 1 :
                self.phone_obj.press_softkey(3)  #Details
                self.phone_obj.sleep(1)
                if self.phone_obj.verify_display_message_contents(phoneName):
                    logger.info("User <b>"+phoneName+" </b> found in redial list having extension number <b>"
                                + phoneObj.phone_obj.phone_obj.phone.extensionNumber+ " </b>.", html=True)
                    console("User "+phoneName+" found in redial list having extension number "
                                + phoneObj.phone_obj.phone_obj.phone.extensionNumber+ ".")
                    break
                else:
                    self.phone_obj.press_softkey(5)  #back press
                    self.phone_obj.sleep(1)
                self.phone_obj.press_key("ScrollDown")

            self.phone_obj.press_softkey(1)  #Dial
            self.phone_obj.sleep(1)
            self.verifyDisplayMessageUtil(phoneName)
            self.verifyDisplayMessageUtil("Ringing")

        else:
            logger.warn(self.phone_obj.phone_type + " has no display verification.")
            self.phone_obj.sleep(1)
            self.phone_obj.press_key("Enter")



    def disconnectTerminal(self, **kwargs):
        """
        This method disconnects the call from the phone and checks its connection.

        Keyword Args:
            phoneObj: PhoneComponent object of the phone to disconnect terminal  (Optional)
        :returns: None

        :created by: Surender Singh
        :creation date:
        :Updated by: Vikhyat Sharma
        :last update date: 22/11/2020
        """
        if len(kwargs) == 0:
            logger.info("Disconnecting the terminal of extension: <b>" +
                        self.phone_obj.phone_obj.phone.extensionNumber + "</b>.")
            console("Disconnecting the terminal of extension: " + self.phone_obj.phone_obj.phone.extensionNumber)
            self.phone_obj.disconnect_terminal()
        else:
            for key in kwargs:
                phoneObj = kwargs[key]
                logger.info("Disconnecting the terminal of extension: <b>" +
                            phoneObj.phone_obj.phone_obj.phone.extensionNumber + "</b>.")
                console("Disconnecting the terminal of extension: " +
                        phoneObj.phone_obj.phone_obj.phone.extensionNumber)
                phoneObj.phone_obj.disconnect_terminal()

    def checkConnection(self, **kwargs):
        """
        This method checks the phones' connection and ensures they are in idle state.

        Keyword Args:
            phoneObj: PhoneComponent object   (Optional)

        :returns: None
        :created by :Surender singh
        :creation date:
        :last updated by: Vikhyat Sharma
        :last update date: 02/02/2021
        """
        if len(kwargs) == 0:
            logger.info("Checking connection of extension: " + self.phone_obj.phone_obj.phone.extensionNumber,
                        also_console=True)
            self.phone_obj.check_phone_connection()
            if self.phone_obj.verify_led_state("message_waiting", 'blink', 10):
                logger.info("Deleting the unread voicemail(s) on " + self.phone_obj.phone_obj.phone.extensionNumber
                            + " during test setup.")
                console("Deleting the unread voicemail(s) on " + self.phone_obj.phone_obj.phone.extensionNumber
                        + " during test setup.")
                values = {"option": "Inbox", "passCode": voicemailPassword}
                self.deleteVoicemailMsg(**values)
        else:
            for key in kwargs:
                phoneObj = kwargs[key]
                logger.info("Checking connection of extension: " + phoneObj.phone_obj.phone_obj.phone.extensionNumber,
                            also_console=True)
                phoneObj.phone_obj.check_phone_connection()

            for key in kwargs:
                phoneObj = kwargs[key]
                if not self.phone_obj.phone_type == "Mitel6940":
                    if phoneObj.phone_obj.verify_led_state("message_waiting", 'blink', 10):
                        logger.info("Deleting the unread voicemail(s) on " +
                                    phoneObj.phone_obj.phone_obj.phone.extensionNumber + " during test setup.")
                        console("Deleting the unread voicemail(s) on " +
                                phoneObj.phone_obj.phone_obj.phone.extensionNumber + " during test setup.")
                        values = {"option": "Inbox", "passCode": voicemailPassword}
                        phoneObj.deleteVoicemailMsg(**values)

            logger.info("All the setup phones are in idle state.", also_console=True)

    def callUnPark(self, **kwargs):
        """
        This method unparks the call from the different modes available.

         Keyword Args:
            phoneObj: PhoneComponent object
            mode: Unpark mode i.e., Default/ Call history/ Digit Terminator/ Directory/ FAC
            initiateMode: Mode to initiate the unpark i.e., Dial/ Terminator String/ Timeout

        :returns: None
        :created by :Surender singh
        :creation date:
        :last updated by: Vikhyat Sharma
        :last update date: 07/12/2019

        """
        if len(kwargs) >= 2:
            phoneObj = kwargs['phoneObj']
            unParkMode = kwargs['mode']
            dialMode = kwargs['initiateMode']

            logger.info("Unparking the parked call from extension: <b>" +
                        phoneObj.phone_obj.phone_obj.phone.extensionNumber + "</b> on extension: <b>" +
                        self.phone_obj.phone_obj.phone.extensionNumber + "</b> using <b>" + unParkMode +
                        "</b> mode and <b>" + dialMode + "</b>.", html=True)

            console("Unparking the parked call from extension: " + phoneObj.phone_obj.phone_obj.phone.extensionNumber
                    + " on extension: " + self.phone_obj.phone_obj.phone.extensionNumber + " using " + unParkMode
                    + " mode and " + dialMode)

            self.phone_obj.sleep(3)
            if unParkMode in ('default', 'Call History', 'digitTerminator', 'Directory'):
                self.verifyDisplayMessageUtil("UnPark")
                self.phone_obj.press_softkey(2)
                self.verifyDisplayMessageUtil("UnPark")
                self.verifyDisplayMessageUtil("Backspace")
                self.verifyDisplayMessageUtil("Cancel")
                if unParkMode == "default":
                    self.phone_obj.enter_a_number(phoneObj.phone_obj.phone_obj.phone)
                elif unParkMode == "Call History":
                    self.phone_obj.press_key("CallersList")
                    self.phone_obj.sleep(8)
                    self.phone_obj.press_key("ScrollUp")
                    self.phone_obj.sleep(1)
                    self.phone_obj.press_key("ScrollUp")
                    self.phone_obj.sleep(1)
                    self.phone_obj.press_key("ScrollUp")
                    self.phone_obj.sleep(1)
                    self.phone_obj.press_key("ScrollRight")
                    self.phone_obj.sleep(1)
                    self.phone_obj.press_key("ScrollDown")
                    self.phone_obj.sleep(3)
                    self.phone_obj.press_softkey(1)
                elif unParkMode == "Directory":
                    self.phone_obj.press_key("Directory")

                    if not bool(re.match(r'6.0.0.\d|5.2.1.2\d{3}', self.phone_obj.get_firmware_version())):
                        self.phone_obj.press_key("DialPad4")
                        self.phone_obj.press_softkey(2)
                        self.phone_obj.press_softkey(2)
                        self.phone_obj.press_softkey(1)
                    self.phone_obj.dial_anumber(phoneObj.phone_obj.phone_obj.phone.extensionNumber)
                    self.phone_obj.sleep(2)
                    self.phone_obj.press_key("ScrollDown")
                elif unParkMode == "digitTerminator":
                    self.phone_obj.dial_number(phoneObj.phone_obj.phone_obj.phone.extensionNumber)

            elif unParkMode == "FAC":
                self.phone_obj.dial_number(FACunpark + phoneObj.phone_obj.phone_obj.phone.extensionNumber)

            else:
                raise Exception("INVALID UNPARK MODE ({}) PASSED!!".format(unParkMode))

            if dialMode in ('Dial', 'Consult', 'Select'):
                self.phone_obj.press_softkey(1)

            elif dialMode == "TerminatorString":
                self.phone_obj.dial_number(StringTerminator)

            elif dialMode == "timeout":
                self.phone_obj.sleep(5)

            else:
                raise Exception("INVALID DIALMODE ({}) PASSED!!".format(dialMode))
            self.phone_obj.sleep(5)

        else:
            raise Exception("Please check the arguments passed: %s" % str(kwargs[0]))

    def callPark(self, **kwargs):
        """
        This method parks the call using the different modes available.

         Keyword Args:
            self: PhoneComponent object
            phoneObj: PhoneComponent object
            mode: Park mode i.e., Default/ Hold/ Directory/ FAC
            initiateMode: Mode to initiate the park i.e., Consult/ Dial/ Park/ Timeout

        :returns: None
        :created by: Surender singh
        :creation date:
        :last updated by: Vikhyat Sharma
        :last update date: 08/01/2021
        """
        if len(kwargs) >= 2:
            phoneObj = kwargs['phoneObj']
            parkMode = str(kwargs['mode'])
            dialingMode = str(kwargs['initiateMode'])

            logger.info("Parking the call to extension: <b>" + phoneObj.phone_obj.phone_obj.phone.extensionNumber
                        + "</b> from extension: <b>" + self.phone_obj.phone_obj.phone.extensionNumber + "</b> using <b>"
                        + parkMode + "</b> mode and <b>" + dialingMode + "</b>.", html=True)

            console("Parking the call to extension: " + phoneObj.phone_obj.phone_obj.phone.extensionNumber
                    + " from extension: " + self.phone_obj.phone_obj.phone.extensionNumber + " using "
                    + parkMode + " mode and " + dialingMode + ".")

            if parkMode == "default":
                if self.phone_obj.phone_type == "Mitel6930" or self.phone_obj.phone_type == "Mitel6940":
                    self.phone_obj.press_key("BottomKey4")
                else:
                    self.phone_obj.press_key("BottomKey4")
                    self.phone_obj.press_key("BottomKey1")
                    self.phone_obj.sleep(2)
                self.phone_obj.enter_a_number(phoneObj.phone_obj.phone_obj.phone)

            elif parkMode == "hold":
                if self.phone_obj.phone_obj.phone.phoneModel == "Mitel6930":
                    self.phone_obj.press_key("BottomKey5")
                    self.phone_obj.press_key("BottomKey1")
                else:
                    self.phone_obj.press_key("BottomKey4")
                    self.phone_obj.press_key("BottomKey1")
                    self.phone_obj.sleep(2)
                self.phone_obj.enter_a_number(phoneObj.phone_obj.phone_obj.phone)

            elif parkMode == "Directory":
                if self.phone_obj.phone_types == "Mitel6930":
                    self.phone_obj.press_key("BottomKey4")
                else:
                    self.phone_obj.press_key("BottomKey4")
                    self.phone_obj.press_key("BottomKey1")
                    self.phone_obj.sleep(2)

                self.phone_obj.press_key("Directory")
                if not re.match(r'6.0.0.\d{3}|5.2.1.\d{4}', self.phone_obj.get_firmware_version()):
                    self.phone_obj.press_key("DialPad4")
                    self.phone_obj.press_softkey(2)
                    self.phone_obj.press_softkey(2)
                    self.phone_obj.press_softkey(1)

                self.phone_obj.dial_anumber(phoneObj.phone_obj.phone_obj.phone.extensionNumber)
                self.phone_obj.sleep(2)
                self.phone_obj.press_key("ScrollDown")
                self.phone_obj.press_key("Enter")
                self.phone_obj.sleep(3)

            elif parkMode == "FAC":
                self.phone_obj.dial_number(FACpark + phoneObj.phone_obj.phone_obj.phone.extensionNumber)

            if dialingMode == "consult" or dialingMode == "Dial":
                console("FAC dialing")
                if self.phone_obj.phone_type in ('Mitel6865i', "Mitel6910"):
                    self.phone_obj.press_key("ScrollRight")
                else:
                    self.phone_obj.press_softkey(1)

            elif dialingMode == "Park":
                console("Pressing Park key")
                self.phone_obj.press_softkey(3)

            elif dialingMode == "timeout":
                self.phone_obj.sleep(2)

            elif dialingMode == "Cancel":
                if self.phone_obj.phone_obj.phone.phoneModel == "Mitel6930":
                    self.verifyDisplayMessageUtil("Cancel")
                    self.phone_obj.press_key("BottomKey4")
                else:
                    self.phone_obj.press_key("BottomKey4")
                    self.phone_obj.press_key("BottomKey1")
            else:
                raise Exception("Invalid DialingMode ({0}) passed!!".format(dialingMode))

        else:
            raise Exception("Please check the arguments passed: %s" % kwargs)

    def initiateTransfer(self, **kwargs):
        """
        This method initiates the transfer of a call to another extension.

        :param:
            :self: PhoneComponent object
            :phoneObj: PhoneComponent object
            :initiateMode: Mode to initiate the transfer i.e., Consult/ Timeout/ Cancel

        :returns: None
        :created by :Surender singh
        :creation date:
        :last updated by: Milind Patil
        :last update date: 27/01/2021
        """
        if len(kwargs) >= 2:
            phoneObj = kwargs['phoneObj']
            initiateMode = kwargs['initiateMode']

            logger.info(
                "Initiating the call transfer from extension: <b>" + self.phone_obj.phone_obj.phone.extensionNumber
                + "</b> to extension: <b>" + phoneObj.phone_obj.phone_obj.phone.extensionNumber
                + "</b> using <b>" + initiateMode + "</b> initiation mode.", html=True)

            console("Initiating the call transfer from extension: " + self.phone_obj.phone_obj.phone.extensionNumber
                    + " to extension: " + phoneObj.phone_obj.phone_obj.phone.extensionNumber
                    + " using " + initiateMode + " initiation mode.")

            if self.phone_obj.phone_type in ('Mitel6865i', "Mitel6910"):
                self.phone_obj.press_key("Transfer")
            else:
                self.phone_obj.press_softkey(3)
                self.verifyDisplayMessageUtil(">")
            self.phone_obj.sleep(2)

            self.phone_obj.enter_a_number(phoneObj.phone_obj.phone_obj.phone)

            if initiateMode == "Consult":
                if self.phone_obj.phone_type in ('Mitel6865i', "Mitel6910"):
                    self.phone_obj.sleep(1)
                    self.phone_obj.press_key("ScrollRight")
                else:
                    self.phone_obj.press_softkey(1)

            elif initiateMode == "timeout":
                console("Waiting 5 seconds because initiation mode is timeout.")
                self.phone_obj.sleep(5)
                self.verifyCallid(**kwargs)

            elif initiateMode == "Cancel":
                if self.phone_obj.phone_type in ('Mitel6865i', "Mitel6910"):
                    self.phone_obj.press_key("GoodBye")
                elif self.phone_obj.phone_type == "Mitel6920":
                    self.phone_obj.press_softkey(4)
                    self.phone_obj.press_softkey(1)
                elif self.phone_obj.phone_type in ("Mitel6930", 'Mitel6940'):
                    self.phone_obj.press_softkey(4)
                else:
                    raise Exception("UNSUPPORTED PHONE TYPE ({}) PASSED!!".format(self.phone_obj.phone_type))
            else:
                raise Exception("INVALID INITIATION MODE ({0}) PASSED!!".format(initiateMode))
        else:
            raise Exception("Please check the arguments passed: %s" % kwargs)

    def waitTill(self, **kwargs):
        """
        Below method will wait for the passed number of seconds on the phone.

        :param:
            :self: Phone Component object
            :timeInSeconds: Time (in seconds) to wait on the phone.

        :returns: None

        :created by: Surender Singh
        :creation date:
        :last update by: Sharma
        :last update date: 21/11/2019
        """
        secondsToWait = kwargs['timeInSeconds']
        logger.info("Waiting for %s" % secondsToWait + " seconds on " + self.phone_obj.phone_obj.phone.extensionNumber)
        console("Waiting for %s" % secondsToWait + " seconds on " + self.phone_obj.phone_obj.phone.extensionNumber)
        self.phone_obj.sleep(secondsToWait)

    def voicemailUserLogin(self, **kwargs):
        """
        This method logs in to the phone's voicemail system.
        :param:
            :self: PhoneComponent Object
            :passCode: the voicemail login password

        :returns: None
        :created by: Surender Singh (OM)
        :creation date:
        :last update by: Vikhyat Sharma
        :last update date: 07/12/2020
        """

        if len(kwargs) >= 1:
            voicemailPassCode = str(kwargs["passCode"])
        else:
            raise Exception("Please check the arguments passed %s " % kwargs)

        logger.info("Logging in to the voicemail system on extension: <b>"
                    + self.phone_obj.phone_obj.phone.extensionNumber + "</b>", html=True)
        console("Logging in to the voicemail system on extension: " + self.phone_obj.phone_obj.phone.extensionNumber)

        if self.phone_obj.phone_type == "Mitel6910":
            self.phone_obj.input_a_number("#")
            self.phone_obj.sleep(5)
        else:
            self.phone_obj.press_key("VoiceMail")
            self.phone_obj.sleep(2)
        self.phone_obj.input_a_number(voicemailPassCode)

        self.phone_obj.sleep(2)

        if self.phone_obj.phone_type == "Mitel6910":
            self.phone_obj.input_a_number("#")
        else:
            self.phone_obj.press_softkey(1)

        if self.phone_obj.phone_type not in ('Mitel6910', 'Mitel6865i'):
            self.verifyDisplayMessageUtil('Inbox')
            self.verifyDisplayMessageUtil('Saved')
            self.verifyDisplayMessageUtil('Delete')

    def pressCallHistory(self, **kwargs):
        """
        This method opens call history screen and performs the possible actions.

        Keyword Args:
            folderName: folder to open i.e., Outgoing/ Missed/ Received
            action: action to perform i.e., Details/Dial/Delete/Quit/OffHook/Loudspeaker
        :returns: None

        :created by: Surender Singh (OM)
        :creation date:
        :last update by: Vikhyat Sharma
        :last update date: 20/11/2020
        """
        folderName = str(kwargs['folderName'])
        action = kwargs['action']
        pbx = kwargs['pbx']

        if pbx == 'Telepo':
            self.callHistoryForTelepo(**kwargs)
        else:
            logger.info("Opening the <b>" + folderName + "</b> folder of Call History on <b>"
                        + self.phone_obj.phone_obj.phone.extensionNumber + "</b> and performing <b>" + action
                        + "</b> action.", html=True)

            console("Opening the " + folderName + " folder of Call History on "
                    + self.phone_obj.phone_obj.phone.extensionNumber + " and performing " + action + " action.")
            self.phone_obj.press_key("CallersList")
            self.phone_obj.sleep(5)
            if self.phone_obj.phone_type in ('Mitel6865i', "Mitel6910"):
                console("inside 6910")
                self.phone_obj.sleep(5)
            else:
                self.verifyDisplayMessageUtil("Call History")
                for i in range(3):
                    self.phone_obj.press_key("ScrollUp")
                self.phone_obj.press_key("ScrollDown")

                self.phone_obj.sleep(3)
                if folderName == "Outgoing":
                    self.phone_obj.press_key("ScrollDown")
                    self.verify_call_history_icon(icons="CALL_HISTORY_OUTGOING")

                elif folderName == "Missed":
                    self.verify_call_history_icon(icons="CALL_HISTORY_MISSED")

                elif folderName == "Received":
                    self.phone_obj.press_key("ScrollDown")
                    self.phone_obj.press_key("ScrollDown")
                    self.verify_call_history_icon(icons="CALL_HISTORY_INCOMING_RECEIVED")

                elif folderName == "All":
                    self.phone_obj.press_key("ScrollUp")
                    self.verify_call_history_icon(icons="CALL_HISTORY_ALL")

                else:
                    raise Exception("Check the folderName argument passed!! %s" % kwargs)
                self.phone_obj.press_key("ScrollRight")
                self.phone_obj.sleep(3)

                self.verifyDisplayMessageUtil("Dial")
                self.verifyDisplayMessageUtil("Delete")
                if pbx in ('MiV5000', 'MiV400'):
                    self.verifyDisplayMessageUtil('Copy')
                else:
                    self.verifyDisplayMessageUtil("Details")
                self.verifyDisplayMessageUtil("Quit")

            if action == "Details":
                if self.phone_obj.phone_type == "Mitel6920":
                    self.phone_obj.press_softkey(3)
                elif self.phone_obj.phone_type == "Mitel6930":
                    self.phone_obj.press_softkey(4)
                elif self.phone_obj.phone_type == 'Mitel6940':
                    self.phone_obj.press_softkey(5)

                if self.phone_obj.phone_type != "Mitel6910":
                    self.verifyDisplayMessageUtil("Work 1")
                    self.verifyDisplayMessageUtil("Dial")
                    self.verifyDisplayMessageUtil("Close")

            elif action == "Dial":
                if self.phone_obj.phone_type == "Mitel6910":
                    self.phone_obj.press_key("Enter")
                else:
                    self.phone_obj.press_softkey(1)

            elif action == "Delete":
                if not self.phone_obj.phone_type == "Mitel6910":
                    self.phone_obj.press_key('ScrollLeft')
                    self.phone_obj.press_softkey(2)
                    self.verifyDisplayMessageUtil("Delete")
                    self.phone_obj.press_softkey(2)
                    self.verifyDisplayMessageUtil("Missed")
                    self.verifyDisplayMessageUtil("Received")
                    console("coming out of delete")

            elif action == "Quit":
                if self.phone_obj.phone_type == "Mitel6920":
                    self.phone_obj.press_softkey(4)
                elif self.phone_obj.phone_type == 'Mitel6930':
                    self.phone_obj.press_softkey(5)
                elif self.phone_obj.phone_type == 'Mitel6940':
                    self.phone_obj.press_key('BottomKey6')
                    # self.phone_obj.press_softkey(6)

            elif action == "Loudspeaker":
                self.phone_obj.press_key("HandsFree")

            elif action == "Select":
                self.phone_obj.press_key("Enter")

            elif action == "OffHook":
                self.phone_obj.press_key("OffHook")

            elif action == "Nothing":
                self.phone_obj.sleep(2)

            else:
                self.phone_obj.press_key("GoodBye")

            self.phone_obj.sleep(3)

    def leaveVoiceMailMessage(self, **kwargs):
        """
        Below method leaves a voicemail from the phone to the specified extension.

        :param:
            :self: PhoneComponent Object
            :kwargs: Dictionary for getting the arguments needed:
                    :phone: Phone to leave voicemail on.
        :returns: None

        :created by: Surender Singh (OM)
        :creation date:
        :last update by: Sharma
        :last update date: 18/12/2019
        """

        phone = kwargs["phone"]

        logger.info("Leaving a voicemail on extension: <b>" + phone.phone_obj.phone_obj.phone.extensionNumber
                    + "</b> from <b>" + self.phone_obj.phone_obj.phone.extensionNumber + "</b>.", html=True)
        console("Leaving a voicemail on extension: " + phone.phone_obj.phone_obj.phone.extensionNumber
                + " from " + self.phone_obj.phone_obj.phone.extensionNumber)

        self.phone_obj.press_key("HandsFree")
        self.phone_obj.input_a_number(phone.phone_obj.phone_obj.phone.extensionNumber)
        self.phone_obj.sleep(5)
        phone.phone_obj.input_a_number("#")
        self.phone_obj.sleep(50)
        self.phone_obj.press_key("GoodBye")

    def directoryAction(self, **kwargs):
        """
        This method perform the specified actions inside directory.

        :param:
            :self: PhoneComponent Object
            :phoneObj: PhoneComponent object to search/ dial in directory
            :action: action to perform i.e., Details/ Dial/ Loud speaker
        :returns: None

        :created by: Saurabh Sharma
        :creation date: 27/02/2019
        :last update by: Sharma
        :last update date: 25/11/2019
        """
        if len(kwargs) >= 2:
            phoneObj = kwargs['phoneObj']
            action = kwargs['action']
        else:
            raise Exception("Please check the arguments passed %s " % kwargs)

        logger.info("Pressing directory on <b>" + self.phone_obj.phone_obj.phone.extensionNumber
                    + "</b> to perform <b>" + action + "</b> action.", html=True)

        console("Pressing directory on " + self.phone_obj.phone_obj.phone.extensionNumber
                + " to perform " + action + " action.")

        self.phone_obj.press_key("Directory")
        self.phone_obj.sleep(4)

        if self.phone_obj.phone_type == "Mitel6910":
            self.searchDirectoryIn6910(**kwargs)
        elif self.phone_obj.phone_type in ('Mitel6920', 'Mitel6930', 'Mitel6940'):
            if kwargs['pbx'] not in ('MiVoice', 'MiCloud'):
                self.phone_obj.press_key("DialPad4")
                self.phone_obj.press_softkey(2)
                self.phone_obj.press_softkey(2)
                self.phone_obj.press_softkey(1)
            if isinstance(phoneObj, PhoneComponent):
                self.phone_obj.dial_anumber(phoneObj.phone_obj.phone_obj.phone.extensionNumber)
            else:
                self.phone_obj.dial_number(phoneObj)
            self.phone_obj.sleep(2)
            self.phone_obj.press_key("ScrollDown")
            self.phone_obj.sleep(2)
        else:
            raise Exception("Check the Phone type")

        if action == "Details":
            logger.info("Verifying the details screen of <b>" + phoneObj.phone_obj.phone_obj.phone.extensionNumber
                        + "</b> inside directory on <b>" + self.phone_obj.phone_obj.phone.extensionNumber
                        + "</b>.", html=True)
            console("Verifying the details screen of " + phoneObj.phone_obj.phone_obj.phone.extensionNumber
                    + " inside directory on " + self.phone_obj.phone_obj.phone.extensionNumber)

            if self.phone_obj.phone_type == "Mitel6910":
                self.verifyDisplayMessageUtil(phoneObj.phone_obj.phone_obj.phone.extensionNumber)
                self.verifyDisplayMessageUtil("W1")
            elif self.phone_obj.phone_type in ('Mitel6920', 'Mitel6930'):
                if self.phone_obj.phone_type == "Mitel6920":
                    self.phone_obj.press_key("BottomKey3")
                else:
                    self.phone_obj.press_key("BottomKey4")
                self.verifyDisplayMessageUtil(phoneObj.phone_obj.phone_obj.phone.extensionNumber)
                self.verifyDisplayMessageUtil("Intercom")
                self.verifyDisplayMessageUtil("Close")
                self.verifyDisplayMessageUtil("Available")
            elif self.phone_obj.phone_type == "Mitel6940":
                self.phone_obj.press_key("BottomKey5")
                self.phone_obj.sleep(2)
                self.verifyDisplayMessageUtil(phoneObj.phone_obj.phone_obj.phone.extensionNumber)
                self.verifyDisplayMessageUtil("Dial")
                self.verifyDisplayMessageUtil("Intercom")
                self.verifyDisplayMessageUtil("Dial Voicemail")
                self.verifyDisplayMessageUtil("Close")

        elif action == "Dial":
            logger.info("Dialing the extension: <b>" + phoneObj.phone_obj.phone_obj.phone.extensionNumber
                        + "</b> inside directory.", html=True)

            console("Dialing the extension: " + phoneObj.phone_obj.phone_obj.phone.extensionNumber
                    + " inside directory.")

            self.phone_obj.press_key("Enter")
            self.phone_obj.sleep(3)
            if not self.phone_obj.phone_type == "Mitel6910":
                self.verifyDisplayMessageUtil("Ringing")

        elif action == "Loudspeaker":
            self.phone_obj.press_key("HandsFree")

        elif action == "Select":
            self.phone_obj.press_softkey(1)

        elif action == "OffHook":
            self.phone_obj.press_key("OffHook")

    def dialNumber(self, **kwargs):
        """
        Below method dials the passed number on the phone.

        :param:
            :self: PhoneComponent Object
            :kwargs: Dictionary for getting the arguments needed:
                    :self: PhoneComponent Object
                    :number: number to dial
        :returns: None

        :created by: Ramkumar
        :creation date: 27/02/2019
        :last update by: Sharma
        :last update date: 25/11/2019
        """
        if (len(kwargs) >= 1):
            number = kwargs["number"]
            logger.info("Dialing the number <b>" + number + "</b> from extension "
                        + self.phone_obj.phone_obj.phone.extensionNumber, html=True)
            console("Dialing the number " + number + " from extension "
                    + self.phone_obj.phone_obj.phone.extensionNumber)

            self.phone_obj.input_a_number(number)
        else:
            raise Exception("Check the arguments passed behind %s" % kwargs)

    def enterNumber(self, **kwargs):
        """
        This method enters a number on the phone.

        :param:
            :self: PhoneComponent Object
            :phoneObj: number to enter
        :returns: None

        :created by: Ramkumar
        :creation date: 27/02/2019
        :last update by: Sharma
        :last update date: 25/11/2019
        """
        if len(kwargs) >= 1:
            phoneObj = kwargs["phoneObj"]

            if isinstance(phoneObj, PhoneComponent):
                logger.info("Entering the extension <b>" + phoneObj.phone_obj.phone_obj.phone.extensionNumber
                            + "</b> on <b>" + self.phone_obj.phone_obj.phone.extensionNumber + "</b>", html=True)
                console("Entering the extension " + phoneObj.phone_obj.phone_obj.phone.extensionNumber
                        + " on " + self.phone_obj.phone_obj.phone.extensionNumber)

                self.phone_obj.input_a_number(phoneObj.phone_obj.phone_obj.phone.extensionNumber)
            else:
                logger.info("Entering number <b>" + phoneObj + "</b> on "
                            + self.phone_obj.phone_obj.phone.extensionNumber, html=True)
                console("Entering number <b>" + phoneObj + "</b> on "
                        + self.phone_obj.phone_obj.phone.extensionNumber)

                self.phone_obj.dial_digits(phoneObj)
        else:
            raise Exception("LESS NUMBER OF ARGUMENTS PASSED!! %s" % kwargs)

    def pressKey(self, **kwargs):
        """
        This method presses the passed hardkey or softkey on the phones for 'n' times.

        Keyword Args:
            keyValue: key to press
            number: number of times to press.
            keyType: Type of Key to press i.e., Softkey or Hardkey
        :returns: None

        :created by: Ramkumar
        :creation date: 01/03/2019
        :last update by: Sharma
        :last update date: 25/11/2019
        """
        if len(kwargs) >= 2:
            keyValue = str(kwargs['keyValue'])
            number = int(kwargs['number'])
            keyType = kwargs['keyType']
            logger.info("Pressing <b>" + keyType + ": " + keyValue + "</b> on <b>" +
                        self.phone_obj.phone_obj.phone.extensionNumber + "</b> for <b>" + str(number) +
                        "</b> time(s).", html=True)
            console("Pressing " + keyType + ": " + keyValue + " on " + self.phone_obj.phone_obj.phone.extensionNumber +
                    " for " + str(number) + " time(s).")

            if keyValue.isdigit():
                for i in range(number):
                    self.phone_obj.press_softkey(keyValue)
                    self.phone_obj.sleep(2)
            else:
                for _ in range(number):
                    if self.phone_obj.phone_type in ('Mitel6867i', 'Mitel6865i'):
                        if 'ProgramKey2' in keyValue or 'ProgramKey1' in keyValue:
                            keyValue = keyValue.replace('ProgramKey', 'Line')
                    self.phone_obj.press_key(keyValue)
                    self.phone_obj.sleep(2)
        else:
            raise Exception("Please check the arguments passed: %s" % kwargs)

    def userSettings(self, **kwargs):
        """
        This method navigates to the specified settings option on the phone.

        Keyword Args:
            :option: settings to navigate to.
            :pbx: Call Manager the phone is registered with

        :returns: None
        :created by: Surender Singh
        :creation date:
        :last update by: Vikhyat Sharma
        :last update date: 08/01/2021
        """
        option = kwargs['option']
        pbx = kwargs['pbx']
        self.phone_obj.press_key('Menu')

        logger.info("Navigating to the <b>" + option + "</b> option inside settings menu of extension: <i>"
                    + self.phone_obj.phone_obj.phone.extensionNumber + "</i>", html=True)
        console("Navigating to the " + option + " option inside settings of extension: "
                + self.phone_obj.phone_obj.phone.extensionNumber)

        self.phone_obj.sleep(2)
        if self.phone_obj.phone_type in ('Mitel6910', 'Mitel6865i'):
            self.phone_obj.press_key("ScrollDown")
            self.phone_obj.press_key("ScrollRight")
            self.phone_obj.press_key("ScrollDown")
        else:
            if pbx in ('MiVoice', 'MiCloud'):
                self.phone_obj.input_a_number(voicemailPassword)
                self.phone_obj.sleep(1)
                self.phone_obj.press_softkey(1)
                self.phone_obj.sleep(3)

        if option == "Availability":
            if self.phone_obj.phone_type == 'Mitel6940':
                self.phone_obj.select_option_on_options_menu('AVAILABILITY')
            else:
                for i in range(4):
                    self.phone_obj.press_key("ScrollLeft")
                self.verifyDisplayMessageUtil("Availability")
                self.phone_obj.press_softkey(1)
            self.phone_obj.sleep(2)
            self.verifyDisplayMessageUtil("Availability")

        elif option == "Audio":
            subOption = kwargs.get('opt_sub', '')
            if self.phone_obj.phone_type == 'Mitel6940':
                if subOption:
                    if subOption == 'Ring Tones':
                        self.phone_obj.select_option_on_options_menu('AUDIO_RINGTONES')
                    elif subOption == 'Audio Mode':
                        self.phone_obj.select_option_on_options_menu('AUDIO_MODE')
                    elif subOption == 'Toneset':
                        self.phone_obj.select_option_on_options_menu('AUDIO_TONESET')
                    elif subOption == 'Headset':
                        self.phone_obj.select_option_on_options_menu('AUDIO_HEADSET')
                    else:
                        raise Exception('INVALID OPTION({}) PASSED FOR 6940!!'.format(subOption))

                    self.phone_obj.sleep(3)
                    self.verifyDisplayMessageUtil(subOption)
                else:
                    raise Exception("Please specify sub option for 6940 set!!")
            else:
                if pbx not in ('MiVoice', 'MiCloud'):
                    if self.phone_obj.phone_type in ("Mitel6920", 'Mitel6867i', 'Mitel6930'):
                        for i in range(3):
                            self.phone_obj.press_key("ScrollRight")
                    elif self.phone_obj.phone_type in ("Mitel6910", 'Mitel6865i'):
                        self.phone_obj.press_key("Enter")
                        for i in range(5):
                            self.phone_obj.press_key("ScrollDown")
                else:
                    self.phone_obj.press_key('ScrollRight')
                    if self.phone_obj.phone_type == 'Mitel6930':
                        self.phone_obj.press_key('ScrollRight')

                    if not self.phone_obj.verify_display_message_contents('Unassign user'):
                        self.phone_obj.press_key("ScrollLeft")
                        if self.phone_obj.phone_type == 'Mitel6930':
                            self.phone_obj.press_key('ScrollLeft')

                    for i in range(2):
                        self.phone_obj.press_key("ScrollRight")

                self.verifyDisplayMessageUtil("Audio")
                if subOption:
                    if subOption == "Ring Tones":
                        if self.phone_obj.phone_type == "Mitel6910":
                            self.phone_obj.press_key("Enter")
                            self.phone_obj.press_key("ScrollDown")
                        else:
                            for i in range(2):
                                self.phone_obj.press_key("ScrollDown")
                    elif subOption == "Audio Mode":
                        if self.phone_obj.phone_type == "Mitel6910":
                            self.phone_obj.press_key("Enter")
                            self.phone_obj.press_key("ScrollDown")
                            self.phone_obj.press_key("ScrollDown")
                            self.phone_obj.press_key("Enter")
                            self.phone_obj.press_key("ScrollDown")
                    else:
                        raise Exception("INVALID SUB-OPTION({}) PASSED FOR AUDIO MODE!!".format(subOption))
                    self.phone_obj.press_key("Enter")

        elif option == "Diagnostics":
            self.advanced_settings_login(pbx=pbx)
            subOption = kwargs.get('opt_sub', '')
            if self.phone_obj.phone_type == 'Mitel6940':
                self.phone_obj.select_option_on_options_menu(subOption.upper())
                self.verifyDisplayMessageUtil(subOption)
            elif self.phone_obj.phone_type in ("Mitel6910", 'Mitel6865i'):
                for _ in range(4):
                    self.phone_obj.press_key("ScrollDown")
                self.phone_obj.press_key("ScrollRight")
            else:
                if self.phone_obj.phone_type == "Mitel6920":
                    for i in range(2):
                        self.phone_obj.press_key("ScrollRight")
                else:
                    for i in range(3):
                        self.phone_obj.press_key("ScrollRight")

                if subOption == 'Troubleshooting':
                    if self.phone_obj.phone_type == 'Mitel6910':
                        self.phone_obj.press_key('ScrollDown')
                elif subOption == "Ping":
                    self.phone_obj.press_key('ScrollDown')
                    if self.phone_obj.phone_type == "Mitel6910":
                        self.phone_obj.press_key("ScrollDown")

                elif subOption == "Traceroute":
                    for _ in range(2):
                        self.phone_obj.press_key('ScrollDown')
                    if self.phone_obj.phone_type == "Mitel6910":
                        self.phone_obj.press_key("ScrollDown")

                elif subOption == 'startCapture':
                    console("start capture")
                    if self.phone_obj.phone_type == "Mitel6910":
                        for i in range(5):
                            self.phone_obj.press_key("ScrollDown")
                        self.phone_obj.press_key("Enter")
                        self.phone_obj.press_key("ScrollDown")
                        self.phone_obj.press_key("ScrollDown")
                        self.phone_obj.press_key("Enter")
                        self.phone_obj.input_a_number("#")
                    else:
                        for i in range(3):
                            self.phone_obj.press_key("ScrollDown")
                        self.phone_obj.press_key("Enter")
                        self.phone_obj.press_softkey(1)
                elif subOption == 'log_upload':
                    for _ in range(4):
                        self.phone_obj.press_key('ScrollDown')
                    if self.phone_obj.phone_type == "Mitel6910":
                        self.phone_obj.press_key("ScrollDown")

                self.phone_obj.press_key('Enter')

        elif option == "Login":
            self.phone_obj.sleep(2)

        elif option.lower() == 'default':
            if not self.phone_obj.phone_type == "Mitel6910":
                if pbx == "MiVoice":
                    voicemailNumber = MiVoicevoicemailNumber
                else:
                    voicemailNumber = MiCloudvoicemailNumber
                if self.phone_obj.phone_type == 'Mitel6940':
                    self.phone_obj.select_option_on_options_menu('AVAILABILITY')
                else:
                    for i in range(4):
                        self.phone_obj.press_key("ScrollLeft")
                    self.phone_obj.press_softkey(1)

                self.verifyDisplayMessageUtil("Availability")
                self.phone_obj.press_key("ScrollDown")
                if self.phone_obj.verify_display_message_contents("Never"):
                    self.phone_obj.press_key("ScrollLeft")
                elif self.phone_obj.verify_display_message_contents("Always"):
                    self.phone_obj.press_key("ScrollRight")
                self.verifyDisplayMessageUtil("No Answer")
                self.phone_obj.press_key("ScrollDown")
                for i in range(4):
                    self.phone_obj.press_softkey(2)
                self.phone_obj.dial_digits(voicemailNumber)
                self.phone_obj.sleep(3)
                self.phone_obj.press_key("ScrollDown")
                self.phone_obj.press_softkey(2)
                self.phone_obj.press_softkey(2)
                self.phone_obj.dial_digits("5")
                self.phone_obj.press_key("ScrollDown")
                for i in range(4):
                    self.phone_obj.press_softkey(2)
                self.phone_obj.dial_digits(voicemailNumber)
                self.phone_obj.sleep(3)
                self.phone_obj.press_softkey(1)
                self.phone_obj.press_key("GoodBye")
            else:
                logger.warn("Cannot change availability for 6910 set.")
                self.phone_obj.press_key("GoodBye")

        elif option == "Time and Date":
            subOption = kwargs.get('opt_sub', '')
            if self.phone_obj.phone_type == 'Mitel6940':
                self.phone_obj.select_option_on_options_menu(subOption.upper().replace(' ', '_'))
            else:
                if pbx in ('MiVoice', 'MiCloud'):
                    for _ in range(2):
                        self.phone_obj.press_key('ScrollLeft')
                    if self.phone_obj.phone_type == 'Mitel6930':
                        self.phone_obj.press_key('ScrollLeft')
                else:
                    for _ in range(4):
                        self.phone_obj.press_key('ScrollLeft')
                    if self.phone_obj.phone_type == 'Mitel6930':
                        self.phone_obj.press_key('ScrollLeft')

            self.verifyDisplayMessageUtil("Time and Date")

            if self.phone_obj.phone_type != 'Mitel6940':
                if subOption == 'Time Zone':
                    self.phone_obj.press_key("ScrollDown")
                self.phone_obj.press_key("Enter")

            self.verifyDisplayMessageUtil(subOption)
            self.phone_obj.sleep(3)

        elif option == "directoryFormat":
            if self.phone_obj.phone_type == "Mitel6910":
                for i in range(2):
                    self.phone_obj.press_key("ScrollDown")
                self.phone_obj.press_key("ScrollRight")
                self.phone_obj.press_key("ScrollDown")
            elif self.phone_obj.phone_type == 'Mitel6940':
                self.phone_obj.select_option_on_options_menu('DIR_SETTINGS')
                self.verifyDisplayMessageUtil("Directory")
            else:
                self.phone_obj.press_key("ScrollLeft")
                self.verifyDisplayMessageUtil("Directory")
                self.phone_obj.press_softkey(1)
                self.phone_obj.sleep(3)

        elif option == "Unassign user":
            if self.phone_obj.phone_type == 'Mitel6940':
                self.phone_obj.select_option_on_options_menu('UNASSIGN_USER')
            else:
                self.phone_obj.press_key("ScrollRight")
                if self.phone_obj.phone_type == "Mitel6930":
                    self.phone_obj.press_key("ScrollRight")
                self.phone_obj.press_softkey(1)

            self.verifyDisplayMessageUtil("Unassign user")
            self.phone_obj.sleep(1)
            self.phone_obj.press_key("ScrollLeft")
            self.phone_obj.press_key("Enter")
            self.phone_obj.sleep(12)

        elif option == 'Language':
            subOption = kwargs.get('sub_option', '')
            if self.phone_obj.press_type in ("Mitel6910", "Mitel6865i"):
                logger.warn("NOT DOING ANYTHING HERE!!")
            elif self.phone_obj.phone_type in ('Mitel6867i', 'Mitel6920', 'Mitel6930'):
                for i in range(5):
                    self.phone_obj.press_key("ScrollLeft")
                self.phone_obj.press_key("Enter")
            elif self.phone_obj.phone_type == 'Mitel6940':
                self.phone_obj.select_option_on_options_menu(subOption.upper().replace(' ', '_'))

            if self.phone_obj.phone_type != 'Mitel6940':
                if subOption == 'Input Language':
                    self.phone_obj.press_key("ScrollDown")
                self.phone_obj.press_key("ScrollRight")
            self.verifyDisplayMessageUtil(subOption)

        elif option == 'Status':
            if self.phone_obj.phone_type in ("Mitel6920", "Mitel6930", 'Mitel6867i', 'Mitel6869i'):
                self.phone_obj.press_key("Enter")
            elif self.phone_obj.phone_type == 'Mitel6940':
                self.phone_obj.select_option_on_options_menu('STATUS')

            if 'sub_option' in kwargs:
                subOption = kwargs['sub_option']
                if subOption == 'Network':
                    self.phone_obj.press_key("ScrollDown")
                self.phone_obj.press_key("ScrollRight")

        elif option == 'Network':
            self.advanced_settings_login(pbx=pbx)
            if self.phone_obj.phone_type in ('Mitel6865i', 'Mitel6910'):
                for _ in range(5):
                    self.phone_obj.press_key('ScrollDown')
            else:
                for _ in range(6):
                    self.phone_obj.press_key('ScrollRight')
            self.verifyDisplayMessageUtil('Network')

            subOption = kwargs.get('opt_sub', '')
            if subOption == 'IPv6 Settings':
                if self.phone_obj.phone_type in ('Mitel6865i', 'Mitel6910'):
                    self.phone_obj.press_key('ScrollDown')
            elif subOption == 'Settings':
                if self.phone_obj.phone_type in ('Mitel6865i', 'Mitel6910'):
                    for _ in range(2):
                        self.phone_obj.press_key('ScrollDown')
                else:
                    self.phone_obj.press_key('ScrollDown')
            elif subOption == 'Ethernet Ports':
                if self.phone_obj.phone_type in ('Mitel6865i', 'Mitel6910'):
                    for _ in range(3):
                        self.phone_obj.press_key('ScrollDown')
                else:
                    for _ in range(2):
                        self.phone_obj.press_key('ScrollDown')
            elif subOption == 'VLAN':
                if self.phone_obj.phone_type in ('Mitel6865i', 'Mitel6910'):
                    for _ in range(4):
                        self.phone_obj.press_key('ScrollDown')
                else:
                    for _ in range(3):
                        self.phone_obj.press_key('ScrollDown')
            elif subOption == 'DSCP':
                if self.phone_obj.phone_type in ('Mitel6865i', 'Mitel6910'):
                    for _ in range(5):
                        self.phone_obj.press_key('ScrollDown')
                else:
                    for _ in range(4):
                        self.phone_obj.press_key('ScrollDown')
            elif subOption == '802.1x':
                if self.phone_obj.phone_type in ('Mitel6865i', 'Mitel6910'):
                    for _ in range(6):
                        self.phone_obj.press_key('ScrollDown')
                else:
                    for _ in range(5):
                        self.phone_obj.press_key('ScrollDown')
            elif subOption == 'LLDP':
                if self.phone_obj.phone_type in ('Mitel6865i', 'Mitel6910'):
                    for _ in range(7):
                        self.phone_obj.press_key('ScrollDown')
                else:
                    for _ in range(6):
                        self.phone_obj.press_key('ScrollDown')
            else:
                raise Exception("INVALID SUB-OPTION ({}) PASSED FOR NETWORK".format(subOption))
            self.phone_obj.press_key('Enter')
            self.verifyDisplayMessageUtil(subOption)
        else:
            raise Exception("INVALID OPTION MENU ({0}) PASSED FOR EXTENSION: {1}".format(option,
                                                                                         self.phone_obj.phone_obj.phone.extensionNumber))

    def callHandlerMode(self, **kwargs):
        """
        This routine is used to set the call handler Availability and Call Forward Mode on phone.

        Keyword Args:
            availability: Available/In a meeting/Out of office/Vacation/Custom/Do not Disturb
            mode: Always/No Answer/Never
        :returns: None

        :created by : Ramkumar
        :creation date:
        :updated by: Vikhyat Sharma
        :last update date : 23/11/2020
        """

        if len(kwargs) >= 2:
            availability = kwargs['availability']
            mode = kwargs['mode']
            count = 0
            logger.info("Changing the CHM on extension: <b>" + self.phone_obj.phone_obj.phone.extensionNumber
                        + "</b> to <b>" + availability + "</b> and Call Forward Mode to <b>"
                        + mode + "</b>.", html=True)

            console("Changing the CHM on extension: " + self.phone_obj.phone_obj.phone.extensionNumber
                    + " to " + availability + " and Call Forward Mode to " + mode + ".")

            if availability == "In a meeting":
                while not self.phone_obj.verify_display_message_contents("In a meeting"):
                    self.phone_obj.press_key("ScrollRight")
                    count += 1
                    if count > 5:
                        break
                    self.phone_obj.sleep(2)

            elif availability == "Extended Absence":
                while not self.phone_obj.verify_display_message_contents("Vacation"):
                    self.phone_obj.press_key("ScrollRight")
                    count += 1
                    if count > 5:
                        break
                    self.phone_obj.sleep(2)

            elif availability == "Custom":
                while not self.phone_obj.verify_display_message_contents("Custom"):
                    self.phone_obj.press_key("ScrollRight")
                    count += 1
                    if count > 5:
                        break
                    self.phone_obj.sleep(2)

            elif availability == "Do not disturb":
                while not self.phone_obj.verify_display_message_contents("Do not disturb"):
                    self.phone_obj.press_key("ScrollRight")
                    count += 1
                    if count > 5:
                        break
                    self.phone_obj.sleep(2)

            elif availability == "Out of office":
                while not self.phone_obj.verify_display_message_contents("Out of office"):
                    self.phone_obj.press_key("ScrollRight")
                    count += 1
                    if count > 5:
                        break
                    self.phone_obj.sleep(2)

            elif availability == "Available":
                while not self.phone_obj.verify_display_message_contents('Available'):
                    self.phone_obj.press_key('ScrollLeft')
                    count += 1
                    if count > 5:
                        break
                    self.phone_obj.sleep(2)

            elif availability == "Custom":
                while not self.phone_obj.verify_display_message_contents("Custom"):
                    self.phone_obj.press_key("ScrollRight")
                    count += 1
                    if count > 5:
                        break
                    self.phone_obj.sleep(2)

            elif availability == "All":
                self.verifyDisplayMessageUtil("Available")
                self.phone_obj.press_key("ScrollRight")
                self.verifyDisplayMessageUtil("In a meeting")
                self.phone_obj.press_key("ScrollRight")
                self.verifyDisplayMessageUtil("Out of office")
                self.phone_obj.press_key("ScrollRight")
                self.verifyDisplayMessageUtil("Vacation")
                self.phone_obj.press_key("ScrollRight")
                self.verifyDisplayMessageUtil("Custom")
                self.phone_obj.press_key("ScrollRight")
                self.verifyDisplayMessageUtil("Do not disturb")
                self.verifyDisplayMessageUtil("Save")
                self.verifyDisplayMessageUtil("Cancel")

            if availability != 'All':
                self.verifyDisplayMessageUtil(availability)

            self.phone_obj.press_key("ScrollDown")
            self.phone_obj.sleep(1)
            self.phone_obj.press_key("ScrollLeft")
            self.phone_obj.press_key("ScrollLeft")

            if mode == "Always":
                while not self.phone_obj.verify_display_message_contents("Always"):
                    self.phone_obj.press_key("ScrollLeft")
                    count += 1
                    if count > 5:
                        break
                self.verifyDisplayMessageUtil("Always")
                self.verifyDisplayMessageUtil("Always destination")
                self.verifyDisplayMessageUtil("Simulring")

            elif mode == "No Answer":
                while not self.phone_obj.verify_display_message_contents("No Answer"):
                    self.phone_obj.press_key("ScrollRight")
                    count += 1
                    if count > 5:
                        break
                self.verifyDisplayMessageUtil("No Answer")
                self.verifyDisplayMessageUtil("No answer destination")
                self.verifyDisplayMessageUtil("Number of Rings")
                self.verifyDisplayMessageUtil("Busy destination")
                self.verifyDisplayMessageUtil("Simulring")

            elif mode == "Never":
                while not self.phone_obj.verify_display_message_contents("Never"):
                    self.phone_obj.press_key("ScrollRight")
                    count += 1
                    if count > 5:
                        break
                self.verifyDisplayMessageUtil("Never")
                self.verifyDisplayMessageUtil("Simulring")

            elif mode == "No Mode":
                self.phone_obj.press_key("ScrollUp")

            elif mode == "All":
                while not self.phone_obj.verify_display_message_contents("Always"):
                    self.phone_obj.press_key("ScrollLeft")
                    count += 1
                    if count > 5:
                        break
                self.verifyDisplayMessageUtil("Always")
                self.verifyDisplayMessageUtil("Always destination")
                self.verifyDisplayMessageUtil("Simulring")

                while not self.phone_obj.verify_display_message_contents("No Answer"):
                    self.phone_obj.press_key("ScrollRight")
                    count += 1
                    if count > 5:
                        break
                self.verifyDisplayMessageUtil("No Answer")
                self.verifyDisplayMessageUtil("No answer destination")
                self.verifyDisplayMessageUtil("Number of Rings")
                self.verifyDisplayMessageUtil("Busy destination")
                self.verifyDisplayMessageUtil("Simulring")

                while not self.phone_obj.verify_display_message_contents("Never"):
                    self.phone_obj.press_key("ScrollRight")
                    count += 1
                    if count > 5:
                        break
                self.verifyDisplayMessageUtil("Never")
                self.verifyDisplayMessageUtil("Simulring")

            self.phone_obj.sleep(3)
            self.verifyDisplayMessageUtil("Save")
            self.phone_obj.sleep(3)
            self.verifyDisplayMessageUtil("Cancel")

        else:
            raise Exception("Please check the arguments passed: %s" % kwargs)

    def pressSoftkeyInSettingState(self, **kwargs):
        """
        This method presses the available softkeys in the settings menu.
        :param:
            :self: PhoneComponent object
            :softKey: softkey to press i.e., Assign/ Advanced/ Log Issue/ Quit

        :returns: None
        :created by : Manoj Karakoti
        :creation date: 17/12/2019
        :updated by : Vikhyat Sharma
        :last update date : 30/11/2020
        """

        if len(kwargs) >= 1:
            softkey = kwargs["softKey"]

            logger.info("Pressing key: <b>" + softkey + "</b> on extension: <b>"
                        + self.phone_obj.phone_obj.phone.extensionNumber + "</b> while in Settings State.", html=True)
            console("Pressing key: " + softkey + " on extension: " + self.phone_obj.phone_obj.phone.extensionNumber
                    + " while in Settings state.")

            self.phone_obj.sleep(3)
            if softkey == "Assign":
                self.phone_obj.press_softkey(1)

            elif softkey == "Advanced":
                self.phone_obj.press_softkey(2)

            elif softkey == "Log Issue":
                if self.phone_obj.phone_type != "Mitel6910":
                    self.phone_obj.press_softkey(3)
                else:
                    for i in range(3):
                        self.phone_obj.press_key("ScrollDown")
                    self.phone_obj.press_key("ScrollRight")

            elif softkey in ("Quit", 'Cancel'):
                if self.phone_obj.phone_type == "Mitel6920":
                    self.phone_obj.press_softkey(4)
                elif self.phone_obj.phone_type == "Mitel6910":
                    self.phone_obj.press_key("GoodBye")
                elif self.phone_obj.phone_type == 'Mitel6930':
                    self.phone_obj.press_softkey(5)
                elif self.phone_obj.press_type == 'Mitel6940':
                    self.phone_obj.press_key('BottomKey6')
                    # self.phone_obj.press_softkey(6)

            elif softkey == 'Save':
                if self.phone_obj.phone_type in ('Mitel6865i', 'Mitel6910'):
                    self.phone_obj.press_key('Enter')
                else:
                    self.phone_obj.press_softkey(1)
            else:
                raise Exception("Please check the softkey passed %s" % softkey)
            self.phone_obj.sleep(2)
        else:
            raise Exception("Invalid number of arguments passed: %s" % kwargs)

    def ChangePhoneToDefaultState(self):
        """
        Below method is used to change the phone state to available.

        :param:
            :self: PhoneComponent object
        :returns: None

        :created by : Ramkumar
        :creation date: 07/03/2019
        :updated by : Ramkumar.G
        :last update date : 20/12/2019

        """
        logger.info("Changing the CHM state to available on " + self.phone_obj.phone_obj.phone.extensionNumber)
        console("Changing the CHM state to available on " + self.phone_obj.phone_obj.phone.extensionNumber)

        if not self.phone_obj.phone_type == "Mitel6910":
            self.phone_obj.press_key("GoodBye")
            self.phone_obj.sleep(3)
            self.phone_obj.press_softkey(4)
            for i in range(6):
                self.phone_obj.press_key("ScrollUp")
            self.phone_obj.press_softkey(1)
            self.phone_obj.sleep(3)

    def verifyVoicepathBetweenPhones(self, phone):
        """
        This method verifies the audio path between phones when in a call.

        :param:
            :self: PhoneComponent object
            :phone: PhoneComponent object of the phone to check the audio path.

        :returns: None
        :created by: Surender Singh (OM)
        :creation date:
        :updated by: Sharma
        :last update date : 25/11/2019
        """
        logger.info("Checking two way audio between <b>" + self.phone_obj.phone_obj.phone.extensionNumber
                    + "</b> and <b>" + phone.phone_obj.phone_obj.phone.extensionNumber + "</b>.", html=True)
        console("Checking two way audio between " + self.phone_obj.phone_obj.phone.extensionNumber
                + " and " + phone.phone_obj.phone_obj.phone.extensionNumber)
        self.phone_obj.sleep(5)
        self.phone_obj.check_two_way_audio(phone.phone_obj)
        logger.info("Two way audio verified between <b>" + self.phone_obj.phone_obj.phone.extensionNumber
                    + "</b> and <b>" + phone.phone_obj.phone_obj.phone.extensionNumber + "</b>.", html=True)
        console("Two way audio verified between " + self.phone_obj.phone_obj.phone.extensionNumber
                + " and " + phone.phone_obj.phone_obj.phone.extensionNumber)

    def threePartyVoicePath(self, **kwargs):
        """
        Below method is used to check the audio path between three phones while in a conference call.

        :param:
            :self: PhoneComponent object
            :phoneB_obj: PhoneComponent object of the other phone on the call
            :phoneC_obj: PhoneComponent object of the other phone on the call

        :returns: None
        :created by : Surender Singh (OM)
        :creation date:
        :updated by : Sharma
        :last update date : 25/11/2019
        """
        phoneB = kwargs['phoneB_obj']
        phoneC = kwargs['phoneC_obj']

        self.phone_obj.sleep(3)
        logger.info("<b>Three Way Audio Verification between " + self.phone_obj.phone_obj.phone.extensionNumber + ", "
                    + phoneB.phone_obj.phone_obj.phone.extensionNumber + " and "
                    + phoneC.phone_obj.phone_obj.phone.extensionNumber + ".</b>", html=True)
        console("Three Way Audio Verification between " + self.phone_obj.phone_obj.phone.extensionNumber + ", "
                + phoneB.phone_obj.phone_obj.phone.extensionNumber + " and "
                + phoneC.phone_obj.phone_obj.phone.extensionNumber)

        self.verifyVoicepathBetweenPhones(phoneB)
        self.phone_obj.sleep(3)
        self.verifyVoicepathBetweenPhones(phoneC)
        phoneB.verifyVoicepathBetweenPhones(phoneC)
        self.phone_obj.sleep(3)

        logger.info("<b>Three Way Audio Verified between " + self.phone_obj.phone_obj.phone.extensionNumber + ", "
                    + phoneB.phone_obj.phone_obj.phone.extensionNumber + " and "
                    + phoneC.phone_obj.phone_obj.phone.extensionNumber + ".</b>", html=True)
        console("Three Way Audio Verified between " + self.phone_obj.phone_obj.phone.extensionNumber + ", "
                + phoneB.phone_obj.phone_obj.phone.extensionNumber + " and "
                + phoneC.phone_obj.phone_obj.phone.extensionNumber)

    def fourPartyVoicePath(self, **kwargs):
        """
        This method verifies the audio path between the phones while in a four party conference call.

        :param:
            :self: PhoneComponent object
            :phoneB_obj: PhoneComponent object of the second phone on the call
            :phoneC_obj: PhoneComponent object of the third phone on the call
            :phoneD_obj: PhoneComponent object of the fourth phone on the call

        :returns: None
        :created by : Surender Singh (OM)
        :creation date:
        :updated by : Sharma
        :last update date : 25/11/2019
        """
        phoneB = kwargs['phoneB_obj']
        phoneC = kwargs['phoneC_obj']
        phoneD = kwargs['phoneD_obj']
        logger.info("<b>Four party audio verification between " + self.phone_obj.phone_obj.phone.extensionNumber + ", "
                    + phoneB.phone_obj.phone_obj.phone.extensionNumber + ", "
                    + phoneC.phone_obj.phone_obj.phone.extensionNumber + " and "
                    + phoneD.phone_obj.phone_obj.phone.extensionNumber + "</b>fno", html=True)
        console("Four party audio verification between " + self.phone_obj.phone_obj.phone.extensionNumber + ", "
                + phoneB.phone_obj.phone_obj.phone.extensionNumber + ", "
                + phoneC.phone_obj.phone_obj.phone.extensionNumber + " and "
                + phoneD.phone_obj.phone_obj.phone.extensionNumber)

        self.verifyVoicepathBetweenPhones(phoneB)
        self.verifyVoicepathBetweenPhones(phoneC)
        self.verifyVoicepathBetweenPhones(phoneD)
        phoneB.verifyVoicepathBetweenPhones(phoneC)
        phoneC.verifyVoicepathBetweenPhones(phoneD)
        phoneB.verifyVoicepathBetweenPhones(phoneD)
        self.phone_obj.sleep(2)

    def deleteVoicemailMsg(self, **kwargs):
        """
        This method will delete the voicemail messages from the different folders in the voicemail system.
        :param:
            :self: PhoneComponent object of the phone
            :option: the folder to delete the messages from i.e., Inbox, Saved, Deleted.
            :passCode: the voicemail login password

        :returns: None
        :created by: Ramkumar
        :creation date: 14/03/2019
        :last update by: Vikhyat Sharma
        :last update date: 10/12/2020
        """

        self.voicemailUserLogin(**kwargs)

        if len(kwargs) >= 1:
            option = kwargs["option"]
            if option == "Inbox":
                logger.info("Deleting the inbox voicemail(s) on extension: <b>"
                            + self.phone_obj.phone_obj.phone.extensionNumber + " </b>", html=True)
                console("Deleting the inbox voicemail(s) on extension: "
                        + self.phone_obj.phone_obj.phone.extensionNumber)

                startTime = time.time()
                while self.phone_obj.verify_led_state("message_waiting", 'blink', 10):
                    if self.phone_obj.phone_type == "Mitel6910":
                        self.phone_obj.input_a_number("1")
                        self.phone_obj.sleep(2)
                        self.phone_obj.input_a_number("3")
                        self.phone_obj.sleep(3)
                    else:
                        self.phone_obj.press_key("ScrollRight")
                        self.phone_obj.press_softkey(3)
                        self.phone_obj.press_softkey(2)
                    iterationTime = time.time()
                    if iterationTime - startTime > 30:
                        logger.error("Stopping deletion of voicemails. Took more than 30s in deleting voicemails on "
                                     + self.phone_obj.phone_obj.phone.extensionNumber)
                        break

            elif option == "Save":
                count = 0
                logger.info("Deleting the <b>saved</b> voicemail(s) on extension: <b>"
                            + self.phone_obj.phone_obj.phone.extensionNumber + " </b>", html=True)
                console("Deleting the saved voicemail(s) on extension: "
                        + self.phone_obj.phone_obj.phone.extensionNumber)
                self.phone_obj.press_key("ScrollDown")
                self.phone_obj.press_key("ScrollRight")
                while not self.phone_obj.verify_display_message_contents("Call VM"):
                    self.phone_obj.press_softkey(3)
                    self.phone_obj.press_softkey(2)
                    self.phone_obj.sleep(3)
                    self.phone_obj.press_key("ScrollRight")
                    count += 1
                    if count == 20:
                        break

            elif option == "Delete":
                logger.info("Deleting the voicemails in <b>deleted</b> folder on extension: <b>"
                            + self.phone_obj.phone_obj.phone.extensionNumber + " </b>", html=True)
                console("Deleting the voicemails in deleted folder on extension: "
                        + self.phone_obj.phone_obj.phone.extensionNumber)

                self.phone_obj.press_key("ScrollDown")
                self.phone_obj.press_key("ScrollDown")
                self.phone_obj.press_key("ScrollRight")
                self.phone_obj.press_softkey(3)
            else:
                raise Exception("INVALID voicemail folder:{} passed!!".format(option))

            self.phone_obj.press_key("GoodBye")

        else:
            raise Exception("Please check the arguments passed: %s" % kwargs)

    def moveVoicemailMsg(self, **kwargs):
        """
        This method is used to move the voicemails from one folder to another inside the voicemail screen.

        Keyword Args:
            folder: folder to move to i.e., InboxToSaved/ DeleteToInbox/ SavedToDelete

        :returns: None
        :created by: Ramkumar
        :creation date: 04/04/2019
        :last updated by: Sharma
        :last update date: 25/11/2019
        """
        if (len(kwargs) >= 1):
            folder = kwargs["folder"]

            if folder == "InboxToSaved":
                logger.info("Moving the voicemail from <b>inbox to saved</b> folder on extension: "
                            + self.phone_obj.phone_obj.phone.extensionNumber, html=True)
                console("Moving the voicemail from inbox to saved on extension: "
                        + self.phone_obj.phone_obj.phone.extensionNumber)
                self.phone_obj.press_key("ScrollRight")
                self.phone_obj.sleep(2)
                if (self.phone_obj.phone_type == "Mitel6920"):
                    self.phone_obj.press_softkey(4)
                    self.phone_obj.press_softkey(2)
                elif (self.phone_obj.phone_type == "Mitel6940"):
                    self.phone_obj.press_softkey(5)
                else:
                    self.phone_obj.press_softkey(5)
                    self.phone_obj.press_softkey(1)

                self.phone_obj.sleep(2)
                self.phone_obj.press_key("ScrollDown")
                self.phone_obj.press_key("ScrollRight")
                self.phone_obj.sleep(2)

            elif folder == "DeleteToInbox":
                logger.info("Moving the voicemail from <b>delete to inbox</b> folder on extension: "
                            + self.phone_obj.phone_obj.phone.extensionNumber, html=True)
                console("Moving the voicemail from delete to inbox folder on extension: "
                        + self.phone_obj.phone_obj.phone.extensionNumber)
                self.phone_obj.press_key("ScrollRight")
                self.phone_obj.press_softkey(3)
                self.phone_obj.press_softkey(2)
                self.phone_obj.sleep(5)
                self.phone_obj.press_key("ScrollDown")
                self.phone_obj.press_key("ScrollDown")
                self.phone_obj.press_key("ScrollRight")
                self.phone_obj.press_softkey(3)
                self.phone_obj.sleep(5)
                self.phone_obj.press_key("ScrollRight")

            elif folder == "SavedToDelete":
                logger.info("Moving the voicemail from <b>saved to delete</b> folder on extension: "
                            + self.phone_obj.phone_obj.phone.extensionNumber, html=True)
                console("Moving the voicemail from saved to delete folder on extension: "
                        + self.phone_obj.phone_obj.phone.extensionNumber)
                self.phone_obj.press_key("ScrollRight")

                if self.phone_obj.phone_type in ("Mitel6920", "Mitel6930", "Mitel6940"):
                    self.phone_obj.press_softkey(3)
                    self.phone_obj.sleep(2)
                    self.phone_obj.press_softkey(2)
                self.phone_obj.sleep(3)
                self.phone_obj.press_key("ScrollLeft")
                self.phone_obj.press_key("ScrollDown")
                self.phone_obj.press_key("ScrollRight")
                self.phone_obj.press_softkey(3)
                self.phone_obj.sleep(2)
                self.phone_obj.press_softkey(2)
                self.phone_obj.sleep(3)
                self.phone_obj.press_key("ScrollDown")
                self.phone_obj.press_key("ScrollRight")
        else:
            raise Exception("Please check the arguments passed: %s" % kwargs)

    def verifyDirectoryDetails(self, **kwargs):
        """
        This method is used to verify the details screen of a directory entry.
        :param:
            :self: PhoneComponent object
            :pbx: Call Manager of the phone

        :returns: None
        :created by: Saurabh
        :creation date: 22/02/2019
        :last updated by: Vikhyat Sharma
        :last update date: 23/11/2020
        """
        pbx = kwargs.get('pbx', 'MiVoice')
        logger.info("Verifying the Details screen of a contact in Directory on extension: "
                    + self.phone_obj.phone_obj.phone.extensionNumber)
        console("Verifying the Details screen of a contact in Directory on extension: "
                + self.phone_obj.phone_obj.phone.extensionNumber)

        if self.phone_obj.phone_type == "Mitel6910":
            self.verifyDisplayMessageUtil("W1")
        else:
            self.verifyDisplayMessageUtil("Dial")
            self.verifyDisplayMessageUtil("Details")
            if pbx in ('MiVoice', 'MiCloud'):
                self.verifyDisplayMessageUtil("Close")
                self.verifyDisplayMessageUtil("Email")
                self.verifyDisplayMessageUtil("Work 1")

    def verifyDefaultDirectoryScreen(self, **kwargs):
        """
        This method verifies the main screen of the directory on the phone.

        Keyword Args:
            pbx: Call Manager of the phone

        :returns: None
        :created by: Saurabh
        :creation date: 22/02/2019
        :last updated by: Vikhyat Sharma
        :last update date: 23/11/2020
        """
        pbx = kwargs['pbx']

        logger.info("Verifying the main screen of Directory on extension: "
                    + self.phone_obj.phone_obj.phone.extensionNumber)
        console("Verifying the main screen of Directory on extension: "
                + self.phone_obj.phone_obj.phone.extensionNumber)

        self.phone_obj.press_key("Directory")
        self.phone_obj.sleep(5)
        if not (self.phone_obj.phone_type == "Mitel6910"):
            if not self.phone_obj.verify_display_message_contents('Directory'):
                self.phone_obj.press_key("Directory")
            if pbx in ('MiVoice', 'MiCloud') and bool(re.search(r"6.0.0.\d|5.2.1.2\d{3}",
                                                                self.phone_obj.get_firmware_version())):
                self.phone_obj.press_key('ScrollDown')
                self.phone_obj.press_key('ScrollLeft')
                self.phone_obj.sleep(2)

            if self.phone_obj.verify_display_message_contents("By First"):
                logger.info("Directory is sorted using Last Name. Changing it to First name on extension: "
                            + self.phone_obj.phone_obj.phone.extensionNumber, also_console=True)
                if self.phone_obj.phone_type == "Mitel6920":
                    self.phone_obj.press_softkey(2)
                elif self.phone_obj.phone_type == "Mitel6930":
                    self.phone_obj.press_softkey(3)
                elif self.phone_obj.phone_type == "Mitel6940":
                    self.phone_obj.press_softkey(4)
                self.phone_obj.sleep(2)
                self.phone_obj.press_key('ScrollDown')
                self.phone_obj.press_key('ScrollLeft')

            self.verifyDisplayMessageUtil("Quit")
            self.phone_obj.press_key("ScrollRight")
            self.phone_obj.sleep(2)
            self.verifyDisplayMessageUtil("Dial")
            self.verifyDisplayMessageUtil("Details")
        else:
            self.verifyDisplayMessageUtil("W1")

    def verifyDirectoryAction(self, **kwargs):
        """
        This method performs search related actions in the directory of the phone.

        Keyword Args:
            phoneObj: PhoneComponent object of the phone to search
            directoryAction: Action to perform i.e., default/searchOnly/searchWithDial/searchMultiple, etc
            pbx: Call Manager of the phone

        :returns: None
        :created by:
        :creation date:
        :last updated by: Milind Patil
        :last update date: 2/2/2021
        """

        if len(kwargs) >= 2:
            phoneObj = kwargs["phoneObj"]
            action = kwargs['directoryAction']
            pbx = kwargs['pbx']
        else:
            raise Exception("Please check the arguments passed %s" % kwargs)
        startTime = time.time()
        if pbx == 'Telepo':
            self.directoryActionsForTelepo(**kwargs)
        else:
            logger.info("Performing <b>" + action + "</b> action inside directory of extension: <b>"
                        + self.phone_obj.phone_obj.phone.extensionNumber + "</b>.", html=True)
            console("Performing " + action + " action inside directory of extension: "
                    + self.phone_obj.phone_obj.phone.extensionNumber)

            if action == "default":
                self.verifyDefaultDirectoryScreen(pbx=pbx)
                if not self.phone_obj.phone_type == "Mitel6910":
                    for i in range(4):
                        self.phone_obj.press_key("ScrollDown")
                    endTime = time.time()
                    while endTime < 180:
                        if pbx == "MiCloud":
                            while not self.phone_obj.verify_display_message_contents("1005"):
                                self.phone_obj.press_key("ScrollDown")
                        else:
                            while not (self.phone_obj.verify_display_message_contents("4005")):
                                self.phone_obj.press_key("ScrollDown")
                        endTime = time.time()
                    for i in range(4):
                        self.phone_obj.press_key("ScrollUp")
                    self.phone_obj.press_key("ScrollRight")
                    self.phone_obj.sleep(4)
                else:
                    endTime = time.time()
                    while (endTime-startTime) < 180:
                        if pbx == "MiCloud":
                            while not self.phone_obj.verify_display_message_contents("1001"):
                                self.phone_obj.press_key("ScrollDown")
                        else:
                            while not self.phone_obj.verify_display_message_contents("4001"):
                                self.phone_obj.press_key("ScrollDown")
                        endTime = time.time()
                self.verifyDirectoryDetails(pbx=pbx)

            elif action == "selectOnly":
                self.phone_obj.press_key("Directory")
                if self.phone_obj.phone_type == "Mitel6910":
                    self.searchDirectoryIn6910(**kwargs)
                else:
                    if not bool(re.search(r'6.0.0.\d|5.2.1.2\d{3}', self.phone_obj.get_firmware_version())):
                        self.phone_obj.press_key("DialPad4")
                        self.verifyDisplayMessageUtil("Directory")
                        self.phone_obj.press_key("BottomKey2")
                        self.phone_obj.press_key("BottomKey2")
                        self.phone_obj.press_key("BottomKey1")
                        self.phone_obj.sleep(3)
                    if isinstance(phoneObj, PhoneComponent):
                        self.phone_obj.enter_a_number(phoneObj.phone_obj.phone_obj.phone)
                    else:
                        self.phone_obj.dial_digits(phoneObj)

                    self.phone_obj.press_key("ScrollDown")
                    self.verifyDisplayMessageUtil("Select")
                    self.phone_obj.sleep(3)
                    self.phone_obj.press_softkey(1)

            elif action in ('searchOnly', 'searchWithDial', 'searchMultiple', 'searchInvalid'):
                self.verifyDefaultDirectoryScreen(pbx=pbx)
                if self.phone_obj.phone_type == "Mitel6910":
                    if not action == "searchMultiple":
                        self.searchDirectoryIn6910(**kwargs)
                else:
                    if not bool(re.search(r'6.0.0.\d|5.2.1.2\d{3}', self.phone_obj.get_firmware_version())):
                        self.phone_obj.press_key("DialPad4")
                        self.phone_obj.press_key("BottomKey2")
                        self.phone_obj.press_key("BottomKey2")
                        self.phone_obj.press_key("BottomKey1")
                        self.phone_obj.sleep(3)
                    if isinstance(phoneObj, PhoneComponent):
                        self.phone_obj.enter_a_number(phoneObj.phone_obj.phone_obj.phone)
                    else:
                        self.phone_obj.dial_digits(phoneObj)
                    self.verifyDisplayMessageUtil("Quit")
                    self.verifyDisplayMessageUtil("Backspace")
                    self.phone_obj.press_key('ScrollDown')

                if action == "searchMultiple":
                    if self.phone_obj.phone_type == 'Mitel6910':
                        for _ in range(2):
                            self.phone_obj.press_key('ScrollLeft')
                        for _ in range(2):
                            self.phone_obj.press_key('ScrollDown')
                    else:
                        for _ in range(2):
                            self.phone_obj.press_softkey(1)
                    self.phone_obj.sleep(3)
                elif action == "searchWithDial" or action == "searchOnly":
                    self.phone_obj.press_key("ScrollDown")
                    if self.phone_obj.phone_type == "Mitel6920":
                        self.phone_obj.press_softkey(3)
                    elif self.phone_obj.phone_type == 'Mitel6930':
                        self.phone_obj.press_softkey(4)
                    elif self.phone_obj.phone_type == 'Mitel6940':
                        self.phone_obj.press_softkey(5)
                    self.phone_obj.sleep(3)
                    self.verifyDirectoryDetails(pbx=pbx)

                    if action == "searchWithDial":
                        if self.phone_obj.phone_type == "Mitel6910":
                            self.phone_obj.press_key("Enter")
                        else:
                            self.phone_obj.press_softkey(1)
                            self.verifyDisplayMessageUtil("Ringing")
                elif action == "searchInvalid":
                    self.phone_obj.press_key("DialPad4")
                    if self.phone_obj.phone_type == "Mitel6910":
                        self.phone_obj.press_key("ScrollDown")

                    self.verifyDisplayMessageUtil("No Matches Found")

            elif action.lower() == "close":
                if self.phone_obj.phone_type == "Mitel6910":
                    logger.info("<b>Closing Details screen is not possible on 6910.</b>", html=True)
                    console("Closing Details screen is not possible on 6910.")
                if self.phone_obj.phone_type == "Mitel6920":
                    self.phone_obj.press_softkey(4)
                elif self.phone_obj.phone_type == "Mitel6930":
                    self.phone_obj.press_softkey(5)
                elif self.phone_obj.phone_type == "Mitel6940":
                    self.phone_obj.press_key('BottomKey6')
                    # self.phone_obj.press_softkey(6)

                if not self.phone_obj.phone_type == "Mitel6910":
                    self.verifyDisplayMessageUtil("Directory")

            elif action.lower() == "quit":
                if self.phone_obj.phone_type == "Mitel6920":
                    self.phone_obj.press_softkey(4)
                elif self.phone_obj.phone_type == "Mitel6930":
                    self.phone_obj.press_softkey(5)
                elif self.phone_obj.phone_type == "Mitel6940":
                    self.phone_obj.press_key('BottomKey6')
                    # self.phone_obj.press_softkey(6)
                else:
                    self.phone_obj.press_key("GoodBye")

            elif action.lower() == "whisper":
                if self.phone_obj.phone_type == "Mitel6910" or self.phone_obj.phone_type == "Mitel6920":
                    raise Exception("Cannot perform Whisper Action on 6910 and 6920 sets.")
                else:
                    self.phone_obj.press_key("Directory")
                    if not bool(re.search(r'6.0.0.\d|5.2.1.2\d{3}', self.phone_obj.get_firmware_version())):
                        self.phone_obj.press_key("DialPad4")
                        self.phone_obj.press_softkey(2)
                        self.phone_obj.sleep(1)
                        self.phone_obj.press_softkey(2)
                        self.phone_obj.sleep(1)
                        self.phone_obj.press_softkey(1)
                        self.phone_obj.sleep(3)
                    self.phone_obj.enter_a_number(phoneObj.phone_obj.phone_obj.phone)
                    self.phone_obj.press_key("ScrollDown")
                    if self.phone_obj.phone_type == 'Mitel6930':
                        self.phone_obj.press_softkey(4)
                    elif self.phone_obj.phone_type == 'Mitel6940':
                        self.phone_obj.press_softkey(5)
                    self.phone_obj.sleep(1)
                    self.phone_obj.press_softkey(4)
                    self.verifyDisplayMessageUtil("Whisper Page")

            elif action.lower() == "dialvoicemail":
                if not bool(re.search(r'6.0.0.\d|5.2.1.2\d{3}', self.phone_obj.get_firmware_version())):
                    self.phone_obj.press_key("Directory")
                    self.phone_obj.press_key("DialPad4")
                    self.phone_obj.press_key("BottomKey2")
                    self.phone_obj.press_key("BottomKey2")
                    self.phone_obj.press_key("BottomKey1")
                self.phone_obj.sleep(3)
                self.phone_obj.enter_a_number(phoneObj.phone_obj.phone_obj.phone)
                self.phone_obj.press_key("ScrollDown")

                if self.phone_obj.phone_type == "Mitel6920":
                    self.phone_obj.press_softkey(3)
                elif self.phone_obj.phone_type == 'Mitel6930':
                    self.phone_obj.press_softkey(4)
                elif self.phone_obj.phone_type == 'Mitel6940':
                    self.phone_obj.press_softkey(5)
                self.phone_obj.press_softkey(3)
                self.phone_obj.sleep(3)
                self.verifyDisplayMessageUtil('Voice Mail')

            elif action == "mainMenu":
                self.verifyDefaultDirectoryScreen(pbx=pbx)

            elif action == "Reset":
                self.verifyDefaultDirectoryScreen(pbx=pbx)
                self.phone_obj.dial_digits("40")
                if self.phone_obj.phone_type == 'Mitel6910':
                    self.phone_obj.press_key('ScrollDown')
                else:
                    self.verifyDisplayMessageUtil("Backspace")
                    self.verifyDisplayMessageUtil("Quit")
                    if bool(re.search(r'6.0.0.\d|5.2.1.2\d{3}', self.phone_obj.get_firmware_version())):
                        self.verifyDisplayMessageUtil('123')
                    else:
                        self.verifyDisplayMessageUtil("ABC")
                if self.phone_obj.phone_type == "Mitel6920" or self.phone_obj.phone_type == "Mitel6910":
                    self.verifyNegativeMessage(negMessage="Reset")
                else:
                    self.verifyDisplayMessageUtil("Reset")
            else:
                raise Exception("INVALID ACTION: " + action + " PASSED FOR DIRECTORY!!")

    def verifyNegativeMessage(self, **kwargs):
        """
        This method is used to verify the passed message does not exist on the phone.

        :param:
                :self: PhoneComponent object of the phone
                :negMessage: message to verify for non availability

        :returns: None
        :created by: Saurabh
        :creation date: 22/02/2019
        :last updated by: Sharma
        :last update on: 27/11/2019
        """
        if len(kwargs) >= 1:
            message = kwargs['negMessage']

            if isinstance(message, PhoneComponent):
                message = message.phone_obj.phone_obj.phone.extensionNumber

            if not self.phone_obj.verify_display_message_contents(message):
                logger.info("Message: <b>" + message + "</b> is not on the display of extension: <b>"
                            + self.phone_obj.phone_obj.phone.extensionNumber + "</b>.", html=True)
                console("Message: " + message + " is not on the display of extension: "
                        + self.phone_obj.phone_obj.phone.extensionNumber)
            else:
                raise Exception("Message: " + message + " is present on display of extension: "
                                + self.phone_obj.phone_obj.phone.extensionNumber)
        else:
            raise Exception("Please check the arguments passed %s" % kwargs)

    def rebootPhone(self, waitTillPhoneComesOnline='True'):
        """
        This method is used to reboot the phone.

        Keyword Args:
            waitTillPhoneComesOnline: Whether to wait till the phone boots up or not
        :returns: None
        :created by:
        :creation date:
        :last updated by: Vikhyat Sharma
        :last update on: 10/11/2020
        """
        logger.info("Rebooting extension: <b>" + self.phone_obj.phone_obj.phone.extensionNumber + "</b>", html=True)
        console("Rebooting extension: " + self.phone_obj.phone_obj.phone.extensionNumber)

        waitTillPhoneComesOnline = True if waitTillPhoneComesOnline.lower() == 'true' else False
        self.phone_obj.reboot_terminal(wait_till_online=waitTillPhoneComesOnline)

    def changeDirectoryNameFormat(self, **kwargs):
        """
        This method is used to change the directory sorting preference from the setting of the phone.

        :param:
            :dirFormat: Directory Sorting Preference i.e., LastFirst

        :returns: None
        :created by: Aman Bhardwaj
        :creation date:
        :last update by: Vikhyat Sharma
        :last update date: 10/12/2020
        """
        if len(kwargs) >= 1:
            action = kwargs['dirFormat']
        else:
            raise Exception("Please check the arguments passed %s" % kwargs)

        self.verifyDisplayMessageUtil('Sorting Preferences')
        self.phone_obj.press_key("ScrollRight")
        self.phone_obj.press_key("ScrollUp")

        if action == "LastFirst":
            self.phone_obj.press_key("ScrollDown")

        if self.phone_obj.phone_type in ('Mitel6865i', 'Mitel6910'):
            logger.warn("Changing Directory Sorting Preference is not supported on {} model!!".format(
                self.phone_obj.phone_type))
        else:
            self.phone_obj.press_softkey(1)

    def assignUser(self, **kwargs):
        """
        This method is used to assign extension to the phone in assigned/unassigned state.

        :param:
                :self: PhoneComponent object of the phone
                :phone: PhoneComponent object of the phone to assign
                :state: State of the phone i.e., Assigned/Unassigned

        :returns: None
        :created by:
        :creation date:
        :last updated by: Vikhyat Sharma
        :last update on: 23/11/2020
        """
        state = kwargs['state']
        phone = kwargs['phone']
        if self.phone_obj.phone_type == "Mitel6910":
            logger.warn("Assign/Unassign extensions through settings is not supported on 6910 SETS.")

        else:
            if isinstance(phone, PhoneComponent):
                logger.info("Assigning extension: <b>" + phone.phone_obj.phone_obj.phone.extensionNumber + "</b> on <b>"
                            + self.phone_obj.phone_obj.phone.extensionNumber + "</b> in <b>" + state
                            + "</b> state.", html=True)
                console("Assigning extension: " + phone.phone_obj.phone_obj.phone.extensionNumber + " on "
                        + self.phone_obj.phone_obj.phone.extensionNumber + " in " + state + " state.")
            if not self.phone_obj.verify_display_message_contents(self.phone_obj.phone_obj.phone.extensionNumber):
                if state == "Assigned":
                    self.phone_obj.press_key("Menu")
                    self.phone_obj.sleep(1)
                    self.phone_obj.press_softkey(1)
                    self.phone_obj.sleep(2)

                    if phone == "GoodBye":
                        logger.info("Pressing Goodbye while in Assign Extension screen on extension: "
                                    + self.phone_obj.phone_obj.phone.extensionNumber, also_console=True)
                        self.phone_obj.press_key("GoodBye")
                        self.phone_obj.sleep(4)
                elif state == "UnAssigned":
                    if self.phone_obj.verify_display_message_contents(
                            "Available") or self.phone_obj.verify_display_message_contents("Anonymous"):
                        self.verifyDisplayMessageUtil("Assign")
                        self.phone_obj.sleep(1)
                        self.phone_obj.press_softkey(1)
                        self.verifyDisplayMessageUtil("Assign user")
                    else:
                        logger.warn("Phone with IP: " + self.phone_obj.phone_obj.phone.ipAddress
                                    + " is already assigned a number so assigning extension in assigned condition.")
                        self.assignUser(phone=kwargs['phone'], state='Assigned')

                if self.phone_obj.verify_display_message_contents("Assign user"):
                    self.phone_obj.dial_anumber(phone.phone_obj.phone_obj.phone.extensionNumber)
                    self.phone_obj.press_key("ScrollDown")
                    self.phone_obj.input_a_number(voicemailPassword)
                    self.phone_obj.sleep(2)
                    self.phone_obj.press_softkey(1)
                    self.waitTill(timeInSeconds=20)
                    self.verifyDisplayMessageUtil(phone.phone_obj.phone_obj.phone.extensionNumber)
                else:
                    raise Exception("Could not verify the Assign User Menu on extension: "
                                    + self.phone_obj.phone_obj.phone.extensionNumber + "!!")
            else:
                logger.info("Extension number: <b>" + self.phone_obj.phone_obj.phone.extensionNumber
                            + "</b> is already assigned to the " + self.phone_obj.phone_type + " phone.", html=True)
                console("Extension number: " + self.phone_obj.phone_obj.phone.extensionNumber
                        + " is already assigned to " + self.phone_obj.phone_type + " phone.")

    def factoryReset(self, pbx):
        """
        This method is used to factory reset the phone.

        :param:
                :self: PhoneComponent object of the phone

        :returns: None
        :created by: Abhishek Khanchi
        :creation date:
        :last updated by: Ramkumar. G
        :last update on: 10/01/2020
        """
        logger.info("Factory Resetting extension: <b>" + self.phone_obj.phone_obj.phone.extensionNumber
                    + "</b>.", html=True)
        console("Factory Resetting extension: " + self.phone_obj.phone_obj.phone.extensionNumber)

        self.phone_obj.press_key("Menu")
        self.advanced_settings_login(pbx=pbx)

        if self.phone_obj.phone_type == "Mitel6930":
            for i in range(9):
                self.phone_obj.press_key("ScrollRight")
            self.phone_obj.press_key("Enter")
            self.phone_obj.press_key("Enter")
            self.phone_obj.press_key("ScrollRight")

        elif self.phone_obj.phone_type == "Mitel6920":
            for i in range(8):
                self.phone_obj.press_key("ScrollRight")
            self.phone_obj.press_key("Enter")
            self.phone_obj.press_key("Enter")
            self.phone_obj.press_key("ScrollRight")
        else:
            for i in range(9):
                self.phone_obj.press_key("ScrollDown")
            self.phone_obj.press_key("Enter")
        self.phone_obj.press_key("Enter")

    def sipMessageVerification(self, **kwargs):
        """
        Below method is used to verify the SIP message from the SIP packets received on the phone.

        :param:
                :self: PhoneComponent object of the phone
                :kwargs: Dictionary for getting the arguments needed:
                        :phoneObject:
                        :sipMethod:
                        :sipHeader:
                        :msgToVerify:
                        :messageDirection:

        :returns:
        :created by:
        :creation date:
        :last updated by: Sharma
        :last update on: 27/11/2019
        """
        phoneObject = kwargs['phoneObj']
        sipMethod = kwargs['sipMethod']
        sipHeader = kwargs['sipHeader']
        msgToVerify = kwargs['msgToVerify']
        in_out = kwargs['messageDirection']

        if in_out == 'incoming':
            sipPackets = phoneObject.phone_obj.get_sip_in_messages()
        else:
            sipPackets = phoneObject.phone_obj.get_sip_out_messages()

        dict = {}
        for data in sipPackets:
            b = re.split("\xda", data)
            if b != ['']:
                for i in b:
                    if ":" in i:
                        a = i.split(": ")
                        if len(a) == 2:
                            if b[0] not in dict:
                                dict[b[0]] = {a[0]: a[1]}
                            else:
                                dict[b[0]].update({a[0]: a[1]})

        for k, v in dict.items():
            if "INVITE" in k:
                dict["INVITE"] = dict.pop(k)

        if sipMethod not in dict.keys():
            raise Exception("sip message " + sipMethod + " is wrong")
        elif sipHeader not in dict[sipMethod].keys():
            raise Exception("Sip header " + sipHeader + " is wrong")
        elif msgToVerify not in dict[sipMethod][sipHeader]:
            raise Exception("text " + msgToVerify + " is wrong")
        else:
            print(msgToVerify in dict[sipMethod][sipHeader])

    def pingSettings(self, **kwargs):
        """
        This method is used to ping a particular ID address on the phone.

        :param:
                :self: PhoneComponent object of the phone
                :value: Status of the IP Address i.e., Invalid IP/ Valid IP/ Invalid DNS

        :returns: None
        :created by:
        :creation date:
        :last updated by: Vikhyat Sharma
        :last update on: 10/12/2020
        """
        if len(kwargs) >= 1:
            value = kwargs["value"]
            self.userSettings(option='Diagnostics', opt_sub='Ping', pbx=kwargs['pbx'])

            logger.info("Pinging <b>" + value + "</b> on extension: "
                        + self.phone_obj.phone_obj.phone.extensionNumber, html=True)
            console("Pinging " + value + ": " + invalidIP + " on extension: "
                    + self.phone_obj.phone_obj.phone.extensionNumber)

            self.phone_obj.sleep(3)

            if value == "invalid_ip":
                self.phone_obj.dial_digits(invalidIP)
            elif value == "valid_ip":
                self.phone_obj.dial_digits(validIP)
            elif value == "invalid_dns":
                if not self.phone_obj.verify_display_message_contents('abc'):
                    if self.phone_obj.phone_type == "Mitel6920":
                        self.phone_obj.press_softkey(3)
                    elif self.phone_obj.phone_type in ('Mitel6930', 'Mitel6940'):
                        self.phone_obj.press_softkey(4)

                self.phone_obj.dial_digits("9")
                self.phone_obj.dial_digits("9")
                self.phone_obj.dial_digits("*")

            if self.phone_obj.phone_type == 'Mitel6910':
                self.phone_obj.press_key('ScrollDown')
            if self.phone_obj.phone_type == "Mitel6920":
                self.phone_obj.press_softkey(4)
                self.phone_obj.sleep(2)
                self.phone_obj.press_softkey(1)
            elif self.phone_obj.phone_type in ('Mitel6930', 'Mitel6940'):
                self.phone_obj.press_softkey(1)
            self.phone_obj.sleep(20)

    def pickup_call(self, **kwargs):
        """
        This method is used to pickup the held call on the phone.

        :param:
                :self: PhoneComponent object of the phone.
                :phoneObj: PhoneComponent object of the phone to pick the held call from.
                :mode: Mode to search the number
                :initiateMode: Initiation mode of the pickup

        :returns: None
        :created by:
        :creation date:
        :updated by: Vikhyat Sharma
        :updated on: 23/11/2020
        """

        if len(kwargs) >= 2:
            phoneObj = kwargs['phoneObj']
            mode = str(kwargs['mode']).strip()
            initiateMode = str(kwargs['initiateMode'])

            logger.info("Picking up the call from extension: <b>" + phoneObj.phone_obj.phone_obj.phone.extensionNumber
                        + "</b> on <b>" + self.phone_obj.phone_obj.phone.extensionNumber + " using " + mode
                        + "</b> and <b>" + initiateMode + "</b> initiate mode.", html=True)
            console("Picking up the call from extension: " + phoneObj.phone_obj.phone_obj.phone.extensionNumber
                    + " on " + self.phone_obj.phone_obj.phone.extensionNumber + " using " + mode
                    + " and " + initiateMode + " initiate mode.")

            if mode == "Pickup":
                self.phone_obj.press_softkey(1)
            elif mode == "FAC":
                self.phone_obj.dial_number(FACpickup + phoneObj.phone_obj.phone_obj.phone.extensionNumber)
                self.phone_obj.press_softkey(1)
            else:
                raise Exception("INVALID MODE: " + mode + " PASSED FOR PICKUP!!")

            if initiateMode == "Dial":
                self.phone_obj.press_softkey(1)

            elif initiateMode == "timeout":
                self.phone_obj.sleep(4)

            else:
                raise Exception("INVALID INITIATION MODE PASSED: " + initiateMode + " FOR PICKUP!!")
        else:
            raise Exception("INVALID NUMBER OF ARGUMENTS!!!")

    def type_FAC(self, **kwargs):
        """
        Below method allows the usage of different Feature Access Code(FACs) on the phone.

        :param:
            :self: PhoneComponent Object
            :kwargs: Dictionary for getting the arguments needed:
                    :phoneObj: PhoneComponent object of the phone to dial
                    :feature: FAC to use on the phone

        :returns: None
        :created by:
        :creation date:
        :updated by: Sharma
        :updated on: 27/11/2019
        """

        if len(kwargs) >= 1:
            phoneObj = kwargs['phoneObj']
            feature = kwargs['feature']
            if isinstance(phoneObj, PhoneComponent):
                logger.info("Dialing extension: <b>" + phoneObj.phone_obj.phone_obj.phone.extensionNumber
                            + "</b> with FAC of <b>" + feature + "</b> on extension: <b>"
                            + self.phone_obj.phone_obj.phone.extensionNumber + "</b> ", html=True)
                console("Dialing extension: " + phoneObj.phone_obj.phone_obj.phone.extensionNumber
                        + " with FAC of " + feature + " on extension: "
                        + self.phone_obj.phone_obj.phone.extensionNumber)

                if feature == "Intercom":
                    self.phone_obj.dial_number(FACintercom + phoneObj.phone_obj.phone_obj.phone.extensionNumber)

                elif feature == "Bargein":
                    self.phone_obj.dial_number(FACbargein + phoneObj.phone_obj.phone_obj.phone.extensionNumber)

                elif feature == "Silentmonitor":
                    self.phone_obj.dial_number(FACsilentmonitor + phoneObj.phone_obj.phone_obj.phone.extensionNumber)

                elif feature == "Silentcoach":
                    self.phone_obj.dial_number(FACsilentcoach + phoneObj.phone_obj.phone_obj.phone.extensionNumber)

                elif feature == "Privatecall":
                    self.phone_obj.dial_number(
                        FACmakecallprivate_blockCID + phoneObj.phone_obj.phone_obj.phone.extensionNumber)

                elif feature == "Whisperpage":
                    self.phone_obj.dial_number(FACwhisperpage + phoneObj.phone_obj.phone_obj.phone.extensionNumber)

                elif feature == "Busyouthuntgroup":
                    self.phone_obj.dial_number(FACbusyouthuntgroup + phoneObj.phone_obj.phone_obj.phone.extensionNumber)

                elif feature == "Pickup":
                    self.phone_obj.dial_number(FACpickup + phoneObj.phone_obj.phone_obj.phone.extensionNumber)

            else:
                dialingNumber = str(phoneObj)
                logger.info("Dialing number: <b>" + dialingNumber
                            + "</b> with FAC of <b>" + feature + "</b> on extension: <b>"
                            + self.phone_obj.phone_obj.phone.extensionNumber + "</b> ", html=True)
                console("Dialing number: " + dialingNumber
                        + " with FAC of " + feature + " on extension: "
                        + self.phone_obj.phone_obj.phone.extensionNumber)
                if feature == "Intercom":
                    self.phone_obj.dial_number(FACintercom + dialingNumber)

                elif feature == "Bargein":
                    self.phone_obj.dial_number(FACbargein + dialingNumber)

                elif feature == "Silentmonitor":
                    self.phone_obj.dial_number(FACsilentmonitor + dialingNumber)

                elif feature == "Silentcoach":
                    self.phone_obj.dial_number(FACsilentcoach + dialingNumber)

                elif feature == "Privatecall":
                    self.phone_obj.dial_number(FACmakecallprivate_blockCID + dialingNumber)

                elif feature == "Whisperpage":
                    self.phone_obj.dial_number(FACwhisperpage + dialingNumber)

                elif feature == "Busyouthuntgroup":
                    self.phone_obj.dial_number(FACbusyouthuntgroup + dialingNumber)

                elif feature == "Pickup":
                    self.phone_obj.dial_digits(FACpickup + str(phoneObj))

            self.phone_obj.sleep(2)
        else:
            raise Exception("INVALID NUMBER OF ARGUMENTS !!")

    def VerifyNoAudioPathBetweenPhones(self, **kwargs):
        """
        This method is used to verify no audio path between the passed phones.

        :param:
                :self: PhoneComponent object of the phone
                :kwargs: Dictionary for getting the arguments needed:
                    :phoneObj: PhoneComponent object of the phone to check no audio with

        :returns: None
        :created by: Ramkumar
        :creation date: 27/05/2019
        :updated by: Sharma
        :updated on: 27/11/2019
        """
        if len(kwargs) >= 1:
            phone = kwargs["phoneObj"]
            logger.info("Checking no audio path from extension: <b>" + self.phone_obj.phone_obj.phone.extensionNumber
                        + "</b> to <b>" + phone.phone_obj.phone_obj.phone.extensionNumber + "</b>", html=True)
            console("Checking no audio path from extensions: " + self.phone_obj.phone_obj.phone.extensionNumber
                    + " to " + phone.phone_obj.phone_obj.phone.extensionNumber)

            self.phone_obj.check_no_audio(phone.phone_obj)
            self.phone_obj.sleep(3)
            logger.info("No audio path from extension: <b>" + self.phone_obj.phone_obj.phone.extensionNumber
                        + "</b> to <b>" + phone.phone_obj.phone_obj.phone.extensionNumber + "</b>", html=True)
            console("No audio path from extensions: " + self.phone_obj.phone_obj.phone.extensionNumber
                    + " to " + phone.phone_obj.phone_obj.phone.extensionNumber)

    def bargeIn(self, **kwargs):
        """
        This method is used to Barge in another extension on the phone while it is in a call.

        :param:
                :self: PhoneComponent object of the phone.
                :phoneObj: PhoneComponent object of the phone to barge in
                :mode: Place to get the contact i.e., Call History/Directory

        :returns: None
        :created by: Ramkumar
        :creation date: 27/05/2019
        :updated by: Vikhyat Sharma
        :updated on: 10/12/2020
         """

        if len(kwargs) >= 2:
            phoneObj = kwargs["phoneObj"]
            mode = kwargs["mode"]
            initiateMode = kwargs["initiateMode"]
        else:
            raise Exception("Please check the arguments passed %s" % kwargs)

        logger.info("Barging in extension: <b>" + phoneObj.phone_obj.phone_obj.phone.extensionNumber + "</b> on <b>"
                    + self.phone_obj.phone_obj.phone.extensionNumber + "</b> using <b>" + mode + " mode.", html=True)
        console("Barging in extension: " + phoneObj.phone_obj.phone_obj.phone.extensionNumber + " on "
                + self.phone_obj.phone_obj.phone.extensionNumber + " using " + mode + " mode.")

        if mode == "Call History":
            self.phone_obj.press_key("CallersList")
            self.phone_obj.sleep(8)
            self.phone_obj.press_key("ScrollUp")
            self.phone_obj.sleep(1)
            self.phone_obj.press_key("ScrollUp")
            self.phone_obj.sleep(1)
            self.phone_obj.press_key("ScrollUp")
            self.phone_obj.sleep(1)
            self.phone_obj.press_key("ScrollRight")
            self.phone_obj.sleep(1)

        elif mode == "Directory":
            self.phone_obj.press_key("Directory")
            if not bool(re.match(r'6.0.0.\d|5.2.1.2\d{3}', self.phone_obj.get_firmware_version())):
                self.phone_obj.press_key("DialPad4")
                self.phone_obj.press_softkey(2)
                self.phone_obj.press_softkey(2)
                self.phone_obj.press_softkey(1)
            self.phone_obj.dial_anumber(phoneObj.phone_obj.phone_obj.phone.extensionNumber)
            self.phone_obj.sleep(2)
            self.phone_obj.press_key("ScrollDown")
            self.phone_obj.sleep(3)

        if initiateMode == "Select":
            self.phone_obj.press_softkey(1)
        else:
            raise Exception("INVALID BARGE-IN INITIATION MODE: {} PASSED!!".format(initiateMode))

    def VerifyOneWayAudio(self, **kwargs):
        """
        This method is used to verify one way audio while the call is on hold between the passed phones.

        :param:
                :self: PhoneComponent object of the phone.
                :kwargs: Dictionary for getting the arguments needed:
                        :phoneObj: PhoneComponent object of the other phone on the call.
        :returns: None
        :created by: Ramkumar
        :creation date: 28/05/2019
        :updated by: Sharma
        :updated on: 27/11/2019
        """
        if (len(kwargs) >= 1):
            phone = kwargs["phoneObj"]
            logger.info("Checking one way audio from extension: <b>" + self.phone_obj.phone_obj.phone.extensionNumber
                        + "</b> to <b>" + phone.phone_obj.phone_obj.phone.extensionNumber + "</b>.", html=True)
            console("Checking one way audio from extension: " + self.phone_obj.phone_obj.phone.extensionNumber
                    + " to extension: " + phone.phone_obj.phone_obj.phone.extensionNumber)

            self.phone_obj.check_one_way_audio(phone.phone_obj)
            self.phone_obj.sleep(3)

    def dialPartialNumber(self, **kwargs):
        """
        This method is used to dial partial extension number of a phone.
        :param:
                :self: PhoneComponent object of the dialing phone.
                :kwargs: Dictionary for getting the arguments needed:
                        :type: 'lastTwo'/'fiveDigit'/'firstTwo'/'firstDigit'
        :returns: None
        :created by: Manoj Karakoti
        :creation date: 03/06/2019
        :updated by: Sharma
        :updated on: 27/11/2019
        """

        if (len(kwargs) >= 1):
            phoneObj = kwargs["phoneObj"]
            number = str(phoneObj.phone_obj.phone_obj.phone.extensionNumber)

            logger.info("Dialing the <b>" + kwargs["type"] + " digits</b> of extension: <b>"
                        + self.phone_obj.phone_obj.phone.extensionNumber + "</b>", html=True)
            console("Dialing the " + kwargs["type"] + " digits of extension: "
                    + self.phone_obj.phone_obj.phone.extensionNumber)

            if kwargs['type'] == 'fiveDigit':
                numberToDial = number + str('1')
                self.phone_obj.input_a_number(numberToDial)
                if self.phone_obj.phone_type == "Mitel6910":
                    self.phone_obj.press_key("ScrollLeft")
                else:
                    self.phone_obj.press_softkey(2)
            elif kwargs['type'] == 'firstTwo':
                firstTwoDigit = number[:2]
                self.phone_obj.input_a_number(firstTwoDigit)
            elif kwargs['type'] == 'lastTwo':
                lastTwoDigit = number[2:]
                self.phone_obj.input_a_number(lastTwoDigit)
            elif kwargs['type'] == 'firstDigit':
                firstDigit = number[:1]
                lastThree = number[1:]
                self.phone_obj.input_a_number(firstDigit)
                self.verifyDisplayMessageUtil(firstDigit)
                self.phone_obj.input_a_number(lastThree)
                self.phone_obj.sleep(5)
                self.verifyDisplayMessageUtil(number)

            elif kwargs['type'] == 'both':
                firstTwoDigit = number[:2]
                lastTwoDigit = number[2:]
                self.phone_obj.input_a_number(firstTwoDigit)
                self.phone_obj.press_key("HandsFree")
                self.phone_obj.input_a_number(lastTwoDigit)
            else:
                raise Exception("Check the arguments passed behind %s" % kwargs)
        else:
            raise Exception("Check the arguments passed behind %s" % kwargs)

    def extensionType(self, **kwargs):
        """
        Below method verifies the extension number/name of the passed phone
        on the display of the phone.
        :param:
                :self: PhoneComponent object of the phone.
                :kwargs: Dictionary for getting the arguments needed:
                        :phoneObj: PhoneComponent object of the phone to verify
                        :type: the thing to verify i.e., name/number
        :returns: None
        :created by: Aman Bhardwaj
        :creation date:
        :updated by: Sharma
        :updated on: 28/11/2019
        """

        phoneObj = kwargs['phoneObj']
        type = kwargs['type']
        number = str(phoneObj.phone_obj.phone_obj.phone.extensionNumber)
        name = phoneObj.phone_obj.phone_obj.phone.phoneName

        if type == "Name":
            if (self.phone_obj.verify_display_message_contents(name)):
                logger.info("Verified name: <b>" + name + "</b> of extension: <b>" + number + "</b> on <b>"
                            + self.phone_obj.phone_obj.phone.extensionNumber + "</b>.", html=True)
                console("Verified name: " + name + " of extension: " + number + " on "
                        + self.phone_obj.phone_obj.phone.extensionNumber)
            else:
                raise Exception("Name: " + name + " of extension: " + number + " could not be verified on "
                                + self.phone_obj.phone_obj.phone.extensionNumber)

        elif type == "Number":
            if (self.phone_obj.verify_display_message_contents(number)):
                logger.info("Extension Number: <b>" + number + "</b> verified on <b>"
                            + self.phone_obj.phone_obj.phone.extensionNumber + "</b>.", html=True)
                console("Extension Number: " + number + " Verified on "
                        + self.phone_obj.phone_obj.phone.extensionNumber)
            else:
                raise Exception("Extension Number: " + number + " could not be verified on "
                                + self.phone_obj.phone_obj.phone.extensionNumber)

    def transferTovm(self, **kwargs):
        self.phone_obj.press_softkey(3)
        softkey = kwargs["softKey"]
        if (softkey == "ToVm"):
            if (self.phone_obj.phone_type == "Mitel6920"):
                self.phone_obj.press_softkey(4)
                self.phone_obj.press_softkey(1)
            else:
                self.phone_obj.press_softkey(5)

        else:
            logger.info("Please check the softkey passed %s" % softkey)

    def popup_Message_verifier(self, **kwargs):
        """

        :created by: Abhishek Khanchi
        :creation date:
        :last update by:
        :last update date:
        """
        import threading
        func = kwargs['action_name_dict']['action_name']
        pmargs = kwargs['action_name_dict']['pmargs']
        wait = kwargs['wait']
        tg = str(func.encode("ascii"))
        func = getattr(self, tg)
        t1 = threading.Thread(target=func, kwargs=pmargs)
        t1.start()
        self.phone_obj.sleep(wait)
        messageToVerify = kwargs['message']
        if messageToVerify == "Phone number is invalid or not properly formatted" and self.phone_obj.phone_type == 'Mitel6910':
            messageToVerify = 'Transfer Failed'

        self.verifyDisplayMessage(message=messageToVerify, pbx=kwargs['pbx'])
        t1.join()

    def conferenc_hold_tc(self, **kwargs):
        """

        :created by: Abhishek Khanchi
        :creation date:
        :last update by:
        :last update date:
        """
        console(kwargs)
        if len(kwargs) == 6:
            Flag = kwargs['Flag']
            my_dict = {'key': 'Conference'}
            my_dict_two = {'key': 'Hold', 'message': kwargs['messageValue_two'], 'f_name': kwargs['f_name']}
            if Flag == '0':
                if self.phone_obj.phone_type != "Mitel6910":
                    console(self.phone_obj.phone_type)
                    self.phone_obj.press_softkey(3)

                    result = self.popup_Message_verifier(**kwargs)
                    console(result)
                else:
                    console("t1")
                    self.pressHardkey(**my_dict)
                    self.phone_obj.sleep(3)
                    result = self.popup_Message_verifier(**my_dict_two)

                if result:
                    console('message Verification passed')
                    logger.warn("NOT DOING ANYTHING HERE!!")
                else:
                    raise Exception("message Verification Failed")
            elif Flag == '1':
                if self.phone_obj.phone_type != "Mitel6910":
                    self.dialNumber(**kwargs)
                    result = self.popup_Message_verifier(**kwargs)
                    console(result)
                else:
                    self.dialNumber(**kwargs)
                    result = self.popup_Message_verifier(**my_dict_two)
                    console(result)

                if result == True:
                    console('message Verification passed')
                else:
                    logger.error("message Verification Failed")
                    raise Exception("message Verification Failed")

                print("Done!")

            elif Flag == '2':

                self.dialNumber(**kwargs)
                self.phone_obj.sleep(3)
                self.pressHardkey(**kwargs)
                self.phone_obj.sleep(3)

        else:
            raise Exception("Please check the arguments passed: %s" % kwargs)

    def display_verifier(self, **kwargs):
        """

        :created by: Abhishek Khanchi
        :creation date:
        :last update by:
        :last update date:
        """
        if self.phone_obj.phone_type != "Mitel6910":
            message = kwargs['mydict']['conference']
            console("Verifying Message: " + message + " on Conference Display on extension: "
                    + self.phone_obj.phone_obj.phone.extensionNumber)
            self.verifyDisplayMessageUtil(message)
            message = kwargs['mydict']['offhook']
            self.verifyDisplayMessageUtil(message)
        else:
            message = kwargs['mydict']['conference_6910']
            self.verifyDisplayMessageUtil(message)

    def searchDirectoryIn6910(self, **kwargs):
        """
        This method is used to search for the number in the directory of 6910 model phones.

        :param:
            :phoneObj: PhoneComponent object of the phone to search

        :returns: None
        :created by: Avishek Ranjan
        :creation date:
        :last update by:
        :last update date:
        """
        phoneObj = kwargs['phoneObj']
        num = phoneObj.phone_obj.phone_obj.phone.extensionNumber

        self.phone_obj.sleep(1)
        self.phone_obj.press_key("DialPad4")
        self.phone_obj.sleep(1)
        self.phone_obj.press_key("ScrollLeft")
        self.phone_obj.sleep(2)

        if re.match(r'6.0.\d|5.2.1.2\d\d\d', self.phone_obj.get_firmware_version()):
            self.phone_obj.input_a_number(num)
        else:
            for digit in num:
                self.phone_obj.sleep(1)
                if digit == '0' or digit == '1':
                    self.phone_obj.press_key("DialPad" + digit)
                elif digit == '7' or digit == '9':
                    for i in range(5):
                        self.phone_obj.press_key("DialPad" + digit)
                else:
                    for i in range(4):
                        self.phone_obj.press_key("DialPad" + digit)

        self.phone_obj.press_key("ScrollDown")
        self.verifyDisplayMessageUtil(num)

    def directoryTransfer(self, **kwargs):
        """
        This method is used to transfer the call by selecting a contact from the directory.

        Keyword Args:
            phoneObj: PhoneComponent Object of the destination extension
            transfer: Mode of transfer i.e., Blind/Consultive/SemiAttended
            pbx: Call manager of the transferor phone

        :returns: None
        :created by: Anuj Giri
        :creation date:
        :last update by: Vikhyat Sharma
        :last update date: 10/12/2020
        """
        transfer = kwargs['transfer']
        phoneObj = kwargs['phoneObj']
        pbx = kwargs['pbx']

        logger.info(transfer + "ring the call from extension: " + self.phone_obj.phone_obj.phone.extensionNumber
                    + " to " + phoneObj.phone_obj.phone_obj.phone.extensionNumber + " using directory.")
        console(transfer + "ring the call from extension: " + self.phone_obj.phone_obj.phone.extensionNumber
                + " to " + phoneObj.phone_obj.phone_obj.phone.extensionNumber + " using directory.")

        if self.phone_obj.phone_type == "Mitel6910":
            self.phone_obj.press_key("Transfer")
            self.phone_obj.sleep(2)
            self.phone_obj.press_key("Directory")
            self.phone_obj.verify_display_message_contents("W1")
            self.searchDirectoryIn6910(**kwargs)
        else:
            if self.phone_obj.verify_display_message_contents('Merge'):
                if self.phone_obj.phone_type == "Mitel6920":
                    self.phone_obj.press_key("BottomKey4")
                    self.phone_obj.press_key("BottomKey1")
                else:
                    self.phone_obj.press_key("BottomKey4")
            else:
                self.phone_obj.press_key("BottomKey3")

            self.phone_obj.sleep(2)
            self.phone_obj.press_key("Directory")
            self.verifyDisplayMessage(message="Directory", pbx=pbx)

            if pbx not in ('MiVoice', 'MiCloud'):
                self.phone_obj.press_key("DialPad4")
                self.phone_obj.press_softkey(2)
                self.phone_obj.press_softkey(2)
                self.phone_obj.press_softkey(1)
            self.phone_obj.dial_anumber(phoneObj.phone_obj.phone_obj.phone.extensionNumber)
            self.phone_obj.sleep(2)
            self.phone_obj.press_key("ScrollDown")
            self.phone_obj.sleep(2)

        if transfer == "BlindTransfer":
            if self.phone_obj.phone_type == "Mitel6910":
                self.phone_obj.press_key("Transfer")
            else:
                self.phone_obj.press_key("BottomKey2")

        elif transfer == "ConsultiveTransfer":
            if self.phone_obj.phone_type == "Mitel6910":
                self.phone_obj.press_key("Enter")
            else:
                self.phone_obj.press_key("BottomKey1")
                self.phone_obj.sleep(4)

            self.verifyCallid(**kwargs)
            phoneObj.phone_obj.press_key("HandsFree")
            self.phone_obj.sleep(1)

            if self.phone_obj.phone_type == "Mitel6910":
                self.phone_obj.press_key("Transfer")
            else:
                self.phone_obj.press_key("BottomKey3")

        elif transfer == "ConsultiveTransfervp":
            if self.phone_obj.phone_type == "Mitel6910":
                self.phone_obj.press_key("Enter")
            else:
                self.phone_obj.press_key("BottomKey1")
                self.phone_obj.sleep(4)

            self.verifyCallid(**kwargs)
            phoneObj.phone_obj.press_key("HandsFree")
            self.phone_obj.sleep(3)
            self.phone_obj.check_two_way_audio(phoneObj.phone_obj)
            phoneObj.phone_obj.press_hold()
            self.verifyLedState(ledType='Line1', ledMode='blink')
            if self.phone_obj.phone_type == "Mitel6910":
                self.phone_obj.press_key("Transfer")
            else:
                self.phone_obj.press_key("BottomKey3")

        elif transfer == "SemiAttendedTransfer":
            if self.phone_obj.phone_type == "Mitel6910":
                self.phone_obj.press_key("Enter")
            else:
                self.phone_obj.press_key("BottomKey1")
                self.phone_obj.sleep(4)
                self.verifyDisplayMessageUtil("Cancel")
                self.verifyDisplayMessageUtil("Backspace")
            self.verifyCallid(**kwargs)

            if self.phone_obj.phone_type == "Mitel6910":
                self.phone_obj.press_key("Transfer")
            elif self.phone_obj.phone_type == "Mitel6920":
                self.phone_obj.press_key("BottomKey3")
            elif self.phone_obj.phone_type == "Mitel6940":
                self.phone_obj.press_key("BottomKey5")
            else:
                self.phone_obj.press_key("BottomKey4")

        elif transfer == "SemiAttendedTransferVSK":
            if self.phone_obj.phone_type == "Mitel6910":
                self.phone_obj.press_key("Enter")
            else:
                self.phone_obj.press_key("BottomKey1")
                self.phone_obj.sleep(4)

            phoneState = {"phoneState": "Transfer"}
            self.verifySoftkeysInDifferentPhoneState(**phoneState)
            if self.phone_obj.phone_type == "Mitel6910":
                self.phone_obj.press_key("Transfer")
            elif self.phone_obj.phone_type == "Mitel6920":
                self.phone_obj.press_key("BottomKey3")
            elif self.phone_obj.phone_type == "Mitel6940":
                self.phone_obj.press_key("BottomKey5")
            else:
                self.phone_obj.press_key("BottomKey4")
        else:
            raise Exception("INVALID TRANSFER MODE ({}) PASSED FOR DIRECTORY TRANSFER!!".format(transfer))
        self.verifyDisplayMessage(message="Call Transferred", pbx=pbx)

    def ethernetSettings(self):
        """
        This method is used to verify the ethernet settings on the phones.
        :param:
            :self: PhoneComponent object of the phone

        :returns: None
        :created by:
        :creation date:
        :last update by: Vikhyat Sharma
        :last update date: 30/12/2020
        """
        logger.info("Verifying the ethernet settings on extension: <>"
                    + self.phone_obj.phone_obj.phone.extensionNumber + "</b>", html=True)
        console("Verifying the ethernet settings on extension: " + self.phone_obj.phone_obj.phone.extensionNumber)

        self.phone_obj.press_key("Menu")
        if self.phone_obj.phone_type == "Mitel6910":
            self.phone_obj.press_key("ScrollDown")
            self.phone_obj.press_key("ScrollDown")
            self.phone_obj.press_key("ScrollRight")
            for i in range(1, 5):
                Dial = "DialPad" + str(i)
                self.phone_obj.press_key(Dial)
            self.phone_obj.press_key("Enter")

            # Go to network setting
            for i in range(6):
                self.phone_obj.press_key("ScrollDown")
            self.phone_obj.press_key("ScrollRight")

            # Go to Ethernet and VLAN
            for i in range(10):
                self.phone_obj.press_key("ScrollDown")
            self.phone_obj.press_key("ScrollRight")
            self.phone_obj.press_key("ScrollDown")
            # c1 = 0
            ethernet_ports = ['LAN Port', 'PC Port']
            for setting in ethernet_ports:
                self.verifyDisplayMessageUtil(setting)
                self.phone_obj.press_key('ScrollRight')
                speedValues = ['Auto', 'Full 10Mbps', 'Full 100Mbps', 'Full 1000Mbps', 'Half 10Mbps', 'Half 100Mbps',
                               'Half 1000Mbps']
                for speedValue in speedValues:
                    self.verifyDisplayMessageUtil(speedValue)
                    self.phone_obj.press_key('ScrollDown')
                self.phone_obj.press_key('ScrollLeft')
                self.phone_obj.press_key('ScrollDown')

            self.phone_obj.press_key("ScrollDown")
            self.verifyDisplayMessageUtil("Pass Thru Port")
            self.phone_obj.press_key("ScrollRight")
            self.verifyDisplayMessageUtil("Enable")
            self.phone_obj.press_key("ScrollDown")
            self.verifyDisplayMessageUtil("Disable")
        else:
            self.phone_obj.press_key("BottomKey2")
            for i in range(1, 5):
                Dial = "DialPad" + str(i)
                self.phone_obj.press_key(Dial)
            self.phone_obj.press_key("BottomKey1")
            self.verifyDisplayMessageUtil("Advanced Settings")

            if self.phone_obj.phone_type in ("Mitel6920", "Mitel6930"):
                for i in range(6):
                    self.phone_obj.press_key("ScrollRight")

                self.phone_obj.press_key("ScrollDown")
                self.phone_obj.press_key("ScrollDown")
                self.phone_obj.press_key("Enter")
            elif self.phone_obj.phone_type == "Mitel6940":
                self.phone_obj.select_option_on_options_menu("ETHERNET")
                self.phone_obj.sleep(1)

            self.verifyDisplayMessageUtil("Ethernet")
            self.verifyDisplayMessageUtil("Save")
            self.verifyDisplayMessageUtil("Cancel")

            self.verifyDisplayMessageUtil("LAN Port")
            self.phone_obj.press_key("ScrollRight")
            self.verifyDisplayMessageUtil("Auto")
            self.verifyDisplayMessageUtil("Full 10Mbps")
            self.phone_obj.press_key("ScrollDown")
            self.verifyDisplayMessageUtil("Full 100Mbps")
            self.phone_obj.press_key("ScrollDown")
            self.verifyDisplayMessageUtil("Full 1000Mbps")
            self.phone_obj.press_key("ScrollDown")
            self.verifyDisplayMessageUtil("Half 10Mbps")
            self.phone_obj.press_key("ScrollDown")
            self.verifyDisplayMessageUtil("Half 100Mbps")
            self.phone_obj.press_key("ScrollDown")
            self.verifyDisplayMessageUtil("Half 1000Mbps")

            self.phone_obj.press_key("ScrollLeft")
            self.phone_obj.press_key("ScrollDown")
            self.verifyDisplayMessageUtil("PC Port")
            self.phone_obj.press_key("ScrollRight")
            self.verifyDisplayMessageUtil("Auto")
            self.verifyDisplayMessageUtil("Full 10Mbps")
            self.phone_obj.press_key("ScrollDown")
            self.verifyDisplayMessageUtil("Full 100Mbps")
            self.phone_obj.press_key("ScrollDown")
            self.verifyDisplayMessageUtil("Full 1000Mbps")
            self.phone_obj.press_key("ScrollDown")
            self.verifyDisplayMessageUtil("Half 10Mbps")
            self.phone_obj.press_key("ScrollDown")
            self.verifyDisplayMessageUtil("Half 100Mbps")
            self.phone_obj.press_key("ScrollDown")
            self.verifyDisplayMessageUtil("Half 1000Mbps")

            self.phone_obj.press_key("ScrollLeft")
            self.phone_obj.press_key("ScrollDown")
            self.phone_obj.press_key("ScrollDown")
            self.verifyDisplayMessageUtil("Pass Thru Port")
            self.phone_obj.press_key("ScrollRight")
            self.verifyDisplayMessageUtil("Disable")
            self.verifyDisplayMessageUtil("Enable")

        self.phone_obj.press_key("GoodBye")

    def ipChecker(self, ipaddrstr):
        """
        This check ipv4 address availibility in text and return the count of ip_address found
        :param kwargs: string containing ipaddress

        :returns: len_ipls
        :created by: Abhishek Khanchi
        :creation date:
        :last update by:
        :last update date:
        """
        from re import findall
        ip = ipaddrstr
        len_ipls = len(findall(r"\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b", ip))
        return len_ipls

    def ip_Addr_Dialer(self):
        """

        :created by: Abhishek Khanchi
        :creation date:
        :last update by:
        :last update date:
        """
        if (self.phone_obj.phone_type == "Mitel6910"):
            console('inside IP Dialer 6910')
            id_dot = id('.')
            for key in self.ipaddrstr:
                if id(key) != id_dot:
                    Dial = "DialPad" + str(key)
                    console(Dial)
                    self.phone_obj.press_key(Dial)
                else:
                    keyone = 1
                    Dial = "DialPad" + str(keyone)
                    console(Dial)
                    self.phone_obj.press_key(Dial)
                    self.phone_obj.press_key(Dial)
            self.phone_obj.press_key("Enter")

        else:
            id_dot = id('.')
            for key in self.ipaddrstr:
                if id(key) != id_dot:
                    Dial = "DialPad" + str(key)
                    self.phone_obj.press_key(Dial)
                else:
                    if self.phone_obj.phone_type == "Mitel6920":
                        self.phone_obj.press_softkey(2)
                    else:
                        self.phone_obj.press_softkey(3)

    def get_display_content(self):
        """
        This method Get the whole conent of current display and returns to caller.
        :param :
            :self:  PhoneComponent object

        :returns: content object
        :Created by: Abhishek Khanchi
        :last update by: None
        :last update Date:10/07/2019
        """

        try:
            disp_Obj = self.phone_obj.phone_obj.phone.getAllDisplayResponses('1')

            return disp_Obj
        except:
            raise Exception("An exception occurred while retriving display content from dll")

    def ipAddressDialer(self, **kwargs):
        """
        This method perform operations  like Ping  and Traceroute
        :param:
            :self: PhoneComponent object
            :Ipaddrstr: Ipv4addr string  (eg : 8.8.8.8)
            :opt_sub: Ping or Traceroute

        :returns: None
        :created by : Abhishek Khanchi
        :creation date:
        :last update by: Vikhyat Sharma
        :last update date: 20/11/2020
        """

        ipAddress = kwargs['ipAddress']
        settingsOption = kwargs['opt_sub']

        logger.info("Entering IP Address: <b>" + ipAddress + "</b> in <b>" + settingsOption
                    + "</b> settings on extension: " + self.phone_obj.phone_obj.phone.extensionNumber, html=True)
        console("Entering IP Address: " + ipAddress + " in " + settingsOption + " settings on extension: "
                + self.phone_obj.phone_obj.phone.extensionNumber)

        ipAddress = ipAddress.replace('.', '*')
        self.phone_obj.input_a_number(ipAddress)
        self.phone_obj.press_key('Enter')

        self.phone_obj.sleep(2)

    def ip_validatorFdsp_Content(self):
        """
        Description :
        :param kwargs:
        :returns:

        :created by: Abhishek Khanchi
        :creation date:
        :last update by: None
        :last update date:
        """
        ip_add_status = []
        del ip_add_status[:]
        for i in self.get_display_content():
            console(i.DisplayMessageBody.Data)
            for j in unicode(i.DisplayMessageBody.Data).split(','):
                for k in j.split(':'):
                    for m in k.encode('UTF-8').__str__().split('\xc2'):
                        if self.ipChecker(m) != 0:
                            ip_add_status.append(0)
                        else:
                            ip_add_status.append(1)
        else:
            if len(filter(lambda x: (x == 0), ip_add_status)) == 0:
                logger.error("An exception occurred while retriving display content from the object")
                console("An exception occurred while retriving display content from the object")
                raise Exception("An exception occurred while retriving display content from the object")
                result = filter(lambda x: (x == 0), ip_add_status)
                return 1

            else:
                logger.info("Ip address validation pass")
                console(filter(lambda x: (x == 0), ip_add_status))
                result = filter(lambda x: (x == 0), ip_add_status)
                return 0

    def ip_validatorFdsp_Content_caller(self, **kwargs):
        """
        :created by: Abhishek Khanchi
        :creation date:
        :last update by:
        :last update date:
        """
        if self.phone_obj.phone_type != "Mitel6910":
            self.ip_validatorFdsp_Content()

    def advanced_settings_login(self, **kwargs):
        """
        This method is used to log in to the advanced settings menu on the phone.
        :param:
                :self: PhoneComponent object of the phone.
                :pbx: Call Manager of the phone

        :returns: None
        :created by: Abhishek Khanchi
        :creation date:
        :last update by: Vikhyat Sharma
        :last update Date: 10/12/2020
        """

        logger.info("Logging in to the advanced settings menu on extension: <b>"
                    + self.phone_obj.phone_obj.phone.extensionNumber + "</b>.", html=True)
        console("Logging in to the advanced settings menu on extension: "
                + self.phone_obj.phone_obj.phone.extensionNumber)

        if self.phone_obj.phone_type == "Mitel6910":
            for i in range(2):
                self.phone_obj.press_key("ScrollDown")
            self.phone_obj.press_key("ScrollRight")
        else:
            self.phone_obj.press_softkey(2)

        if kwargs['pbx'] in ('MiVoice', 'MiCloud'):
            self.phone_obj.input_a_number('1234')
        else:
            self.phone_obj.input_a_number('22222')
        self.phone_obj.sleep(1)
        self.phone_obj.press_key("Enter")

    def recordMessage(self, **kwargs):
        """
        This method is used to form a reply to a voicemail on the phone.
        :param:
                :self: PhoneComponent object of the phone
                :phoneObj: PhoneComponent object to reply to
                :action: Action to perform i.e., Play/Pause

        :returns: None
        :created by:
        :creation date:
        :last update by: Vikhyat Sharma
        :last update Date: 10/12/2020
        """
        phoneObj = kwargs['phoneObj']
        action = kwargs['action']

        voicemailPassCode = {"passCode": "12345"}
        self.voicemailUserLogin(**voicemailPassCode)
        self.phone_obj.press_key("ScrollRight")
        softkey = {"softKey": "More"}
        self.pressSoftkeyInVoiceMailState(**softkey)

        logger.info("Forming a reply to the voicemail on extension: <b>"
                    + self.phone_obj.phone_obj.phone.extensionNumber + "</b>", html=True)
        console("Forming a reply to the voicemail on extension: " + self.phone_obj.phone_obj.phone.extensionNumber)

        if self.phone_obj.phone_type == "Mitel6930":
            self.phone_obj.press_softkey(2)
        elif self.phone_obj.phone_type == 'Mitel6940':
            self.phone_obj.press_softkey(1)
        else:
            self.phone_obj.press_softkey(3)

        self.phone_obj.press_softkey(1)

        if re.match('6.0', self.phone_obj.get_firmware_version()):
            if self.phone_obj.phone_type == 'Mitel6940':  # pressing list
                self.phone_obj.press_softkey(5)
                self.phone_obj.press_softkey(1)
                self.phone_obj.press_softkey(5)
            else:
                logger.warn("NOT DOING ANYTHING HERE!!")
            self.phone_obj.input_a_number(phoneObj.phone_obj.phone_obj.phone.extensionNumber)
            self.phone_obj.press_key('ScrollDown')
            self.phone_obj.press_softkey(1)
        elif re.match(r'5.2.1.\d\d\d\d', self.phone_obj.get_firmware_version()):
            for _ in range(4):
                self.phone_obj.press_softkey(1)
            self.phone_obj.enter_a_number(phoneObj.phone_obj.phone_obj.phone)
        else:
            self.phone_obj.enter_a_number(phoneObj.phone_obj.phone_obj.phone)
        self.pressSoftkeyInVoiceMailState(**softkey)
        self.phone_obj.sleep(2)
        self.phone_obj.press_softkey(2)
        self.phone_obj.sleep(15)
        self.phone_obj.press_softkey(2)

        if action == "Play":
            self.phone_obj.sleep(2)
            self.phone_obj.press_softkey(3)
            self.verifyDisplayMessageUtil("Pause")
        elif action == 'Send':
            if self.phone_obj.phone_type == 'Mitel6920':
                self.phone_obj.press_softkey(5)
                self.phone_obj.press_softkey(1)
            else:
                self.phone_obj.press_softkey(4)
        else:
            raise Exception("{} ACTION IS NOT SUPPORTED!!".format(action))

    def advanced_Setting(self, **kwargs):
        """
        Below method performs the advanced settings options available on the phone.

        :param
            :self: PhoneComponent object
            :kwargs: Dictionary for getting the arguments needed:
                    :option: Option to navigate to i.e., Diagnostics.
                    :opt_sub: Sub-option to navigate to i.e., Ping/Traceroute/Server/Delete Server
        :returns: None
        :created by:
        :creation date:
        :last update by:
        :last update date:
        """
        option = kwargs['option']
        logger.info("Moving to <b>" + option + "</b> option with <b>" + kwargs['opt_sub']
                    + "</b> sub-option in advanced settings on extension: <b>"
                    + self.phone_obj.phone_obj.phone.extensionNumber + "</b>.", html=True)
        console("Moving to " + option + " option with " + kwargs['opt_sub']
                + " sub-option in advanced settings on extension: " + self.phone_obj.phone_obj.phone.extensionNumber)

        self.phone_obj.press_key('Menu')
        self.phone_obj.sleep(2)
        self.advanced_settings_login()
        self.verifyDisplayMessageUtil("Advanced Settings")
        if option == "Diagnostics":
            if (self.phone_obj.phone_type == "Mitel6920"):
                for i in range(2):
                    self.phone_obj.press_key("ScrollRight")
                self.verifyDisplayMessageUtil("Diagnostics")

                if kwargs.has_key('opt_sub'):
                    if kwargs['opt_sub'] == "Ping":
                        self.phone_obj.press_key("ScrollDown")
                        self.verifyDisplayMessageUtil("Ping")
                        return
                    elif kwargs['opt_sub'] == "Traceroute":
                        for i in range(2):
                            self.phone_obj.press_key("ScrollDown")
                        self.verifyDisplayMessageUtil("Traceroute")
                        self.phone_obj.press_key("Enter")
                        return
                    elif kwargs['opt_sub'] == 'log_upload':
                        for i in range(4):
                            self.phone_obj.press_key("ScrollDown")
                        self.phone_obj.press_key("Enter")

                    elif kwargs['opt_sub'] == 'diagnostic_server':
                        for i in range(5):
                            self.phone_obj.press_key("ScrollDown")
                        self.phone_obj.press_key("Enter")

                    elif kwargs['opt_sub'] == 'diagnostic_server_delete':
                        for i in range(5):
                            self.phone_obj.press_key("ScrollDown")
                        self.phone_obj.press_key("Enter")

                        for i in range(15):
                            self.phone_obj.press_softkey(1)
                        self.phone_obj.press_softkey(4)
                        self.phone_obj.press_softkey(1)
                    else:
                        logger.error("Please check the arguments passed: %s" % kwargs)
                        raise Exception("Please check the arguments passed: %s" % kwargs)
                else:
                    return

            elif self.phone_obj.phone_type == "Mitel6910":
                # Enter into Diagnostics
                for i in range(4):
                    self.phone_obj.press_key("ScrollDown")
                self.phone_obj.press_key("ScrollRight")

                # Enter into Submenus
                if kwargs.has_key('opt_sub'):
                    opt_sub = kwargs['opt_sub']
                    console(opt_sub)
                    if opt_sub == None:
                        return
                    elif opt_sub == 'Ping':
                        for i in range(2):
                            self.phone_obj.press_key("ScrollDown")
                        self.phone_obj.press_key("ScrollRight")
                        return

                    elif opt_sub == 'Traceroute':
                        for i in range(3):
                            self.phone_obj.press_key("ScrollDown")
                        self.phone_obj.press_key("ScrollRight")
                        return
                else:
                    return
            else:
                # Navigating into Advanced Menu
                for i in range(3):
                    self.phone_obj.press_key("ScrollRight")
                self.verifyDisplayMessageUtil("Diagnostics")
                if kwargs.has_key('opt_sub'):
                    if kwargs['opt_sub'] == 'Ping':
                        self.phone_obj.press_key("ScrollDown")
                        self.phone_obj.press_key("Enter")

                    elif kwargs['opt_sub'] == 'Traceroute':
                        for i in range(2):
                            self.phone_obj.press_key("ScrollDown")
                        self.phone_obj.press_key("Enter")
                        return

                    elif kwargs['opt_sub'] == 'log_upload':
                        for i in range(4):
                            self.phone_obj.press_key("ScrollDown")
                        self.phone_obj.press_key("Enter")

                    elif kwargs['opt_sub'] == 'diagnostic_server':
                        for i in range(5):
                            self.phone_obj.press_key("ScrollDown")
                        self.phone_obj.press_key("Enter")

                    elif kwargs['opt_sub'] == 'diagnostic_server_delete':
                        for i in range(5):
                            self.phone_obj.press_key("ScrollDown")
                        self.phone_obj.press_key("Enter")

                        for i in range(15):
                            self.phone_obj.press_softkey(2)
                        self.phone_obj.press_softkey(1)

                    else:
                        raise Exception("Please check the arguments passed: %s" % kwargs)

    def sipMessageVerification(self, **kewrgs):
        """

        Args:
            **kewrgs:
            This method fetched the sip incoming/outgoing messages .
        Returns:

        """
        console(kewrgs)
        phoneObject = kewrgs['phoneObj']
        sipMethod = kewrgs['sipMethod']
        sipHeader = kewrgs['sipHeader']
        msgToVerify = kewrgs['msgToVerify']
        in_out = kewrgs['messageDirection']

        if in_out == 'incoming':
            sipPackets = phoneObject.phone_obj.get_sip_in_messages()
        else:
            sipPackets = phoneObject.phone_obj.get_sip_out_messages()

        dict = {}
        console(sipPackets)
        for data in sipPackets:
            b = re.split("\xda", data)

            if b != ['']:
                for i in b:
                    if ":" in i:
                        a = i.split(": ")
                        if len(a) == 2:
                            if b[0] not in dict and "INVITE" in b[0]:
                                console(b[0])
                                dict[b[0]] = {a[0]: a[1]}
                            elif b[0] not in dict and "INVITE" not in b[0]:
                                console(b[0])
                                dict[b[0]] = {a[0]: a[1]}
                            else:
                                dict[b[0]].update({a[0]: a[1]})
        console(dict.keys())
        console("""""""""""""""""")
        console(sipMethod)
        console("""""""""""""""""")

        a = ["" for num in dict.keys() if sipMethod not in num]
        if len(a) < 1:
            raise Exception("sip message " + sipMethod + " is wrong")

        a = ["" for num in dict[sipMethod].keys() if sipHeader not in num]
        if len(a) < 1:
            raise Exception("Sip header " + sipHeader + "is wrong")

    def capture_sip_packets(self, **kwargs):
        """
        Below Method is used to capture the sip message passed by one phone to other phone
        when we perform any action like park call.
        sip message : ["INVITE", "ACK", "REFER", "PUBLISH"]

        :param:
                :self: PhoneComponent object of the phone
                :kwargs: Dictionary for getting the required arguments:
                        :message_type: Direction type of the SIP Method i.e., Incoming/Outgoing

        :returns: the captured SIP packets
        :created by: Anuj Giri
        :creation date: 01/09/2019
        :last update by: Sharma
        :last update date: 28/11/2019
        """
        direction = kwargs['message_type'].lower()
        logger.info("Capturing SIP Packets on extension: <b>" + self.phone_obj.phone_obj.phone.extensionNumber
                    + "</b> in <b>" + direction + "</b> direction.", html=True)
        console("Capturing SIP Packets on extension: " + self.phone_obj.phone_obj.phone.extensionNumber
                + " in " + direction + " direction.")

        if direction == "incomming":
            return self.phone_obj.get_sip_in_messages()
        elif direction == "outgoing":
            console(direction)
            return self.phone_obj.get_sip_out_messages()

    def verifySipMessage(self, **kwargs):
        """This method is used to capture the sip message passed by one phone to other phone and header also
        inside that sip message when we perform any action like park call
           sip message : ["INVITE", "ACK", "REFER", "PUBLISH"]
           Header:
                PUBLISH:VQSessionReport (Here PUBLIC is sip message and VQSessionReport is the header of PUBLIC message)


           :self: PhoneComponent Object
           :kwargs: Dictionary for getting the required arguments:
               sip_method_header[sip_message]: It will give the captured sip message value by phone, like call transferred from A to B than for a particular message what value we get
               sip_method_header[sip_message][sip_message_value]: It will give the captured sip message header by phone, like call transferred from A to B then A will send a sip message and this SIP message has header also. Using this method we will get this header

            :returns: None
           History:
           dd/mm/yyyy 		Name				Change description
           01-09-19		    Anuj Giri		    Creation
                                                last updated
         """
        sip_message = kwargs['sip_message']
        console(sip_message)
        sip_message_value = kwargs['sip_message_value']
        console(sip_message_value)
        sip_method = {}
        sip_method_header = {}
        sip_message_data = ["INVITE", "ACK", "REFER", "PUBLISH", "REGISTER"]
        sipdata = self.capture_sip_packets(**kwargs)
        for data in sipdata:
            data = re.sub(r'[^\x00-\x7F]+|u"\ufffd"', ' ---- ', data)
            if data.startswith(tuple(sip_message_data)):
                sip_method[data.split(" ", 1)[0]] = data.split(" ", 1)[1]
                message_value = data.split(" ", 1)[1].strip()
                for i in message_value.split(" ----"):
                    if data.split(" ", 1)[0].strip() not in sip_method_header.keys():
                        key = i.split(":", 1)[0].strip()
                        value = i.split(":", 1)[1].strip()
                        sip_method_header[data.split(" ", 1)[0].strip()] = {key: value}
                    else:
                        if ":" in i:
                            key = i.split(":", 1)[0].strip()
                            value = i.split(":", 1)[1].strip()
                            sip_method_header[data.split(" ", 1)[0].strip()].update({key: value})
        if not sip_message:
            if not sip_message:
                if 'PUBLISH' not in sip_method_header.keys():
                    console("sip message does not exist")
            else:
                logger.error("sip message exist")
                raise Exception("sip message exist")

        elif not sip_message_value:
            if sip_message in sip_method_header.keys():
                console(sip_method_header[sip_message])
                console("sip message value exist")
            else:
                logger.error("sip message value does not exist")
                raise Exception("sip message value does not exist")

        elif sip_message_value:
            if sip_method_header[sip_message][sip_message_value] == 'CallTerm':
                console("sip header exist," + sip_method_header[sip_message][sip_message_value])
            else:
                raise Exception("sip header does not exist")

    def fivePartyVoicePath(self, **kwargs):
        """
        This method verifies five way audio between the 5 parties of a conference call.

        :param:
                :self: PhoneComponent object of the phone
                :kwargs: Dictionary for getting the arguments needed:
                        :phoneB_obj: PhoneComponent object of the other phone
                        :phoneC_obj: PhoneComponent object of the other phone
                        :phoneD_obj: PhoneComponent object of the other phone
                        :phoneE_obj: PhoneComponent object of the other phone
        :returns: None
        :created by: Ramkumar
        :created on:
        :updated by: Sharma
        :updated on: 27/11/2019

        """
        phoneB = kwargs['phoneB_obj']
        phoneC = kwargs['phoneC_obj']
        phoneD = kwargs['phoneD_obj']
        phoneE = kwargs['phoneE_obj']
        logger.info("Five party voicepath verification between " + self.phone_obj.phone_obj.phone.extensionNumber + ", "
                    + phoneB.phone_obj.phone_obj.phone.extensionNumber + ", "
                    + phoneC.phone_obj.phone_obj.phone.extensionNumber + ", "
                    + phoneD.phone_obj.phone_obj.phone.extensionNumber + " and "
                    + phoneE.phone_obj.phone_obj.phone.extensionNumber)
        console("Five party voicepath verification between " + self.phone_obj.phone_obj.phone.extensionNumber + ", "
                + phoneB.phone_obj.phone_obj.phone.extensionNumber + ", "
                + phoneC.phone_obj.phone_obj.phone.extensionNumber + ", "
                + phoneD.phone_obj.phone_obj.phone.extensionNumber + " and "
                + phoneE.phone_obj.phone_obj.phone.extensionNumber)

        self.verifyVoicepathBetweenPhones(phoneB)
        self.verifyVoicepathBetweenPhones(phoneC)
        self.verifyVoicepathBetweenPhones(phoneD)
        self.verifyVoicepathBetweenPhones(phoneE)

        phoneB.verifyVoicepathBetweenPhones(phoneC)
        phoneB.verifyVoicepathBetweenPhones(phoneD)
        phoneB.verifyVoicepathBetweenPhones(phoneE)

        phoneC.verifyVoicepathBetweenPhones(phoneD)
        phoneC.verifyVoicepathBetweenPhones(phoneD)

        phoneD.verifyVoicepathBetweenPhones(phoneE)

        self.phone_obj.sleep(2)

    def changeVoicemailPassword(self, **kwargs):
        """
        Below method will change the voicemail password currently being used on the phone with a new password.

        :param:
            :self: PhoneComponent object of the phone
            :kwargs: Dictionary for getting the arguments needed:
                    :old password: password currently being used
                    :new Password: new password that needs to be used

        :returns: None

        :created by: Ramkumar
        :created on:
        :updated by: Sharma
        :updated on: 30/10/2019
        """
        oldPassword = kwargs['oldPassword']
        newPassword = kwargs['newPassword']

        logger.info("Changing the voicemail login password from <b>" + oldPassword + "</b> to <b>"
                    + newPassword + "</b> on extension: " + self.phone_obj.phone_obj.phone.extensionNumber, html=True)
        console("Changing the voicemail login password from " + oldPassword + " to " + newPassword + " on extension: "
                + self.phone_obj.phone_obj.phone.extensionNumber)

        if not self.phone_obj.verify_display_message_contents("New voicemail password"):
            self.phone_obj.press_key("VoiceMail")
            self.phone_obj.sleep(5)
            self.phone_obj.input_a_number(oldPassword)
            self.phone_obj.press_softkey(1)
            self.phone_obj.sleep(5)
        self.verifyDisplayMessageUtil("New voicemail password")
        self.phone_obj.input_a_number(newPassword)
        self.phone_obj.sleep(3)
        self.phone_obj.press_key("ScrollDown")
        self.phone_obj.input_a_number(newPassword)
        self.phone_obj.sleep(3)
        self.phone_obj.press_key("Enter")
        self.phone_obj.sleep(5)

    def setRings(self, **kwargs):
        """
        This method changes the number of rings to happen while on a call

        Keyword Args:
            number: (int) Number of rings to set

        :returns: None
        :created by:
        :creation date:
        :last update by: Vikhyat Sharma
        :last update date: 05/01/2021
        """
        number = kwargs['number']
        pbx = kwargs['pbx']

        if self.phone_obj.phone_type == 'Mitel6910':
            logger.warn("Cannot change number of rings on 6910 models!!")
        else:
            logger.info("Setting number of rings to <b>{}</b> on <b>{}</b>.".format(number,
                        self.phone_obj.phone_obj.phone.extensionNumber), html=True)
            console("Setting number of rings to {} on {}.".format(number, self.phone_obj.phone_obj.phone.extensionNumber))
            self.phone_obj.press_key('GoodBye')
            self.userSettings(option='Availability', pbx=pbx)

            self.phone_obj.sleep(1)

            for i in range(3):
                self.phone_obj.press_key("ScrollDown")

            self.phone_obj.sleep(1)
            self.phone_obj.press_softkey(2)
            self.phone_obj.press_softkey(2)
            self.phone_obj.sleep(1)

            if number.isdigit():
                self.phone_obj.dial_digits(number)
            else:
                raise Exception("Check the arguments passed behind %s" % kwargs)
            self.phone_obj.sleep(1)

            self.phone_obj.press_softkey(1)
            self.phone_obj.press_key("GoodBye")

    def verifyLineIconState(self, **kwargs):
        """
        This method verifies the icon on phone's call appearance (line).

        Keyword Args:
            line: line to verify the icon state on
            state: icon state to verify on the line

        :returns: None
        :created by: Ramkumar.G
        :creation Date: 05/12/2019
        :last update by: Vikhyat Sharma
        :last update Date: 17/12/2020
        """
        linekey = str(kwargs['line'])
        line = linekey[4:]
        state = str(kwargs['state'])

        if self.phone_obj.phone_type in ('Mitel6865i', 'Mitel6910'):
            logger.warn(self.phone_obj.phone_type + " does not support icon verification.")
        else:
            logger.info("Verifying the icon state of <b>" + linekey + "</b> as <b>" + state + "</b> on extension: <b>"
                        + self.phone_obj.phone_obj.phone.extensionNumber + "</b>", html=True)
            console("Verifying the icon state of " + linekey + " as " + state + " on extension: "
                    + self.phone_obj.phone_obj.phone.extensionNumber)

            iconInfo = self.phone_obj.get_icons(IconIndex=line)
            iconType = iconInfo[0]['Icon']
            logger.info("Icon Info: " + str(iconInfo))
            logger.info("Icon Type: " + str(iconType))
            if iconType == state:
                console("Icon State: %s" % state + " Verified on %s" % self.phone_obj.phone_obj.phone.extensionNumber
                        + " for line " + line)
                logger.info("Icon State: <b>%s</b>" % state + " Verified on <b>%s</b>"
                            % self.phone_obj.phone_obj.phone.extensionNumber + " for line " + line, html=True)
            else:
                raise Exception("Icon State: %s" % state + " Not Verified on %s"
                                % self.phone_obj.phone_obj.phone.extensionNumber + " for line " + line + ". Got "
                                + iconType + " instead!!")

    def getDutDetails(self):
        """
        This method is used for get the information of the DUT.

        :returns: None
        :created by: Vikhyat Sharma
        :creation date:
        :last update by: Vikhyat Sharma
        :last update date: 12/08/2020
        """
        logger.info("DUT Details are as follows: ")
        logger.info("DUT Number       : <b>" + self.phone_obj.phone_obj.phone.extensionNumber + "</b>", html=True)
        logger.info("DUT Phone Type   : <b>" + self.phone_obj.phone_type + "</b>", html=True)
        logger.info("DUT Firmware     : <b>" + self.phone_obj.get_firmware_version() + "</b>", html=True)

    def verifyAvailabilityStateIcon(self, **kwargs):
        """
        This method verifies the current availability state icon on idle screen of the phone.

        Keyword Args:
            state: Availability state to check

        :returns: None
        :created by: Ramkumar.G
        :creation date: 16/12/2019
        :last update by: Vikhyat Sharma
        :last update date: 21/12/2020
        """
        state = str(kwargs['state'])
        self.phone_obj.press_key("BottomKey4")   # State button should be pressed at least once before checking state of the phone
        self.phone_obj.press_key("GoodBye")
        logger.info("ICONS PRESENT:")
        logger.info(self.phone_obj.get_icons())
        # if self.phone_obj.verify_state_icon(state):
        #     console("State Icon: %s" % state + " state Verified on %s" % self.phone_obj.phone_obj.phone.extensionNumber)
        #     logger.info("State Icon : %s" % state + " state Verified on %s" % self.phone_obj.phone_obj.phone.extensionNumber)
        # else:
        #     raise Exception("Icon State : %s" % state + " state Not Verified on %s" % self.phone_obj.phone_obj.phone.extensionNumber)

    def check_audio_on_hold(self, **kwargs):
        """
        This method verifies audio on hold
        :param :
         :self:  PhoneComponent object
        :returns: none
        :Created by: Ramkumar.G
        :Creation Date:19/12/2019
        :last update by: Ram
        :last update Date:03/01/2020
        """
        freq = int(kwargs['expectedFreq'])
        if self.phone_obj.check_audio_on_hold(expectedFreq=freq):
            console("Checked audio on hold on %s" % self.phone_obj.phone_obj.phone.extensionNumber)
            logger.info("Checked audio on hold on %s" % self.phone_obj.phone_obj.phone.extensionNumber)
        else:
            raise Exception("Check audio on hold failed on %s" % self.phone_obj.phone_obj.phone.extensionNumber)

    def check_no_audio_on_hold(self):
        """
        This method verifies there is no audio on hold
        :param:
            :self:  PhoneComponent object

        :returns: none
        :Created by: Ramkumar.G
        :Creation Date:20/12/2019
        :last update by: None
        :last update Date:None
        """
        if not self.phone_obj.check_audio_on_hold(expectedFreq=200):
            console("There is no music when the call is on hold on extension: "
                    + self.phone_obj.phone_obj.phone.extensionNumber)
            logger.info("There is no music when the call is on hold on extension: <b>"
                        + self.phone_obj.phone_obj.phone.extensionNumber + "</b>", html=True)
        else:
            raise Exception("Music on hold is there on extension: " + self.phone_obj.phone_obj.phone.extensionNumber)

    def verify_call_history_icon(self, **kwargs):
        """
        This method is used to verify the call history icons.
        :param:
            self: PhoneComponent object
        Keyword Args:
            icon: Icon to verify

        :returns: None
        :Created by: Ramkumar.G
        :Creation Date:19/12/2019
        :last update by: Vikhyat Sharma
        :last update Date: 21/12/2020
        """
        state = kwargs['icons']
        logger.info(self.phone_obj.get_icons(Icon=state))
        # if self.phone_obj.verify_call_history_icon(state):
        #     console("Call History Icon: %s" % state + " icon Verified on %s" % self.phone_obj.phone_obj.phone.extensionNumber)
        #     logger.info("Call History Icon : %s" % state + " icon Verified on %s" % self.phone_obj.phone_obj.phone.extensionNumber)
        # else:
        #     raise Exception("Call History Icon : %s" % state + " icon Not Verified on %s" % self.phone_obj.phone_obj.phone.extensionNumber)

    def pressPKMLineKey(self, **kwargs):

        """
        This method press key on PKM
        :param :
         :self:  PhoneComponent object
         :kwargs: lineKey: which key to press on PKM

        :returns: none
        :Created by: Ramkumar.G
        :Creation Date:03/01/2020
        :last update by: None
        :last update Date:None
        """
        if (len(kwargs) >= 1):
            lineKey = kwargs['lineKey']
            logger.info("Pressing key: <b>" + lineKey + "</b> on PKM attached to "
                        + self.phone_obj.phone_obj.phone.extensionNumber, html=True)
            console("Pressing key: " + lineKey + " on PKM attached to "
                    + self.phone_obj.phone_obj.phone.extensionNumber)
            self.phone_obj.press_expansion_box_key(lineKey)
        else:
            raise Exception("Please check the arguments passed %s" % kwargs)

    def verifyPKMLedState(self, **kwargs):
        logger.warn("NOT DOING ANYTHING HERE!!")

    def verifyDisplayMessageOnPKM(self, **kwargs):
        logger.warn("NOT DOING ANYTHING HERE!!")

    def verify_PKM_icon_state(self, **kwargs):
        logger.warn("NOT DOING ANYTHING HERE!!")

    def verifyPKMNegativeMessage(self, **kwargs):
        logger.warn("NOT DOING ANYTHING HERE!!")

    def verify_voice_mail_window_icons(self, **kwargs):
        """
        This method verify voicemail icons in the voicemail window
        :param:
         :kwargs: option: icon to be verified
                  value: value to be verified

        :returns: True/False
        :Created by: Ramkumar.G
        :Creation Date:20/01/2020
        :last update by: None
        :last update Date:None
        """
        pass
        # if (len(kwargs) == 2):
        #     icon=kwargs['option']
        #     icon_text=kwargs['value']
        #     console("Verifying " + icon + " Voicemail icons value " + icon_text  + " on "
        #             + self.phone_obj.phone_obj.phone.extensionNumber)
        #     logger.info("Verifying " + icon + " Voicemail icons value " + icon_text  + " on "
        #                 + self.phone_obj.phone_obj.phone.extensionNumber)
        #     self.phone_obj.verify_voice_mail_window_icons(icon,icon_text)
        # else:
        #     raise Exception("Please check the arguments passed %s" % kwargs)

    def deleteCallHistory(self, **kwargs):
        """
        :created by:
        :creation date:
        :last update by:
        :last update date:
        """
        value = kwargs['option']
        self.phone_obj.press_key("CallersList")
        if value == "All":
            for i in range(3):
                self.phone_obj.press_key("ScrollUp")
            self.phone_obj.press_key("BottomKey2")
            self.phone_obj.press_key("BottomKey2")
            self.phone_obj.press_key("GoodBye")
        elif value == "Missed":
            for i in range(2):
                self.phone_obj.press_key("ScrollUp")
            self.phone_obj.press_key("BottomKey2")
            self.phone_obj.press_key("BottomKey2")
            self.phone_obj.press_key("GoodBye")

    def configureProgramButton(self, **kwargs):
        """
        This method is used to configure top softkeys of the phone.

        :kwargs:
            :function: Type of the top softkey to configure
            :number: Number of top softkey to configure i.e., 1-24

        :returns: None
        :created by: Ramkumar. G
        :creation date:
        :last update by: Sharma
        :last update date: 20/09/2020
        """
        logger.info("Configuring parameters on Web UI of extension: " + self.phone_obj.phone_obj.phone.extensionNumber,
                    also_console=True)
        ip = self.phone_obj.phone_obj.phone.ipAddress
        key = str(int(kwargs['position']))
        values = kwargs.get('value', '')

        type = "type" + key
        value = "value" + key
        label = "label" + key
        function = str(kwargs['function']).lower()

        if isinstance(values, PhoneComponent):
            val = str(values.phone_obj.phone_obj.phone.extensionNumber)
        elif self.ipChecker(values) > 0:
            labelip = str(kwargs['label'])
            val = str(values) + labelip + ".xml"
        else:
            val = str(values)
        data = {type: function, value: val, label: function}

        session = requests.Session()
        loginURL = "http://" + ip + "/sysinfo.html"
        topSoftkeyURL = "http://" + ip + "/topsoftkey.html"
        auth = (userid, passcode)
        try:
            loginResponse = session.get(loginURL, auth=auth, verify=False)

            for i in range(2):
                str(i)
                if loginResponse.status_code != 200 or 'Session Expired' in loginResponse.text:
                    console("Attempt to login failed. Trying Again !!")
                    loginResponse = session.get(loginURL, auth=auth)

            post = session.post(topSoftkeyURL, auth=auth, data=data)

            if "Provisioning complete" in post.text:
                logger.info("Successfully configured parameters on Web UI of extension: "
                            + self.phone_obj.phone_obj.phone.extensionNumber, also_console=True)
            else:
                logger.info("POST TEXT START", also_console=True)
                logger.info(post.text, also_console=True)
                logger.info("POST TEXT STOP", also_console=True)
                raise Exception("Something went wrong while configuring parameters on Web UI of extension: "
                                + self.phone_obj.phone_obj.phone.extensionNumber)
        except ConnectionError as e:
            raise Exception("Could not connect to the Web UI of the phone. Error: " + e.message)
        except Exception as e:
            raise Exception('Error occurred while configuring top softkeys on extension: '
                            + self.phone_obj.phone_obj.phone.extensionNumber + ". Error: " + e.message)
        finally:
            session.close()

    def configureExpansionModule(self, **kwargs):
        """

        :created by: Ramkumar. G
        :creation date:
        :last update by:
        :last update date:
        """
        console(kwargs)
        pageNumber = str(kwargs['page_number'])
        lab = str(kwargs.get('label'))
        ip = self.phone_obj.phone_obj.phone.ipAddress
        key = str(int(kwargs['position']))
        console("Key position: " + key)
        values = kwargs.get('value', '')
        type = "type" + key
        value = "value" + key
        label = "label" + key
        console(label)
        function = str(kwargs['function']).lower()
        console(function)

        if isinstance(values, PhoneComponent):
            val = str(values.phone_obj.phone_obj.phone.extensionNumber)
            data = {type: function, value: val, label: label}
        elif self.ipChecker(values) > 0:
            labelip = str(kwargs['label'])
            val = str(values) + labelip + ".xml"
            data = {type: function, value: val, label: labelip}
        else:
            val = str(values)
            data = {type: function, value: val, label: lab}

        session = requests.Session()
        loginURL = "http://" + ip + "/sysinfo.html"

        path = ""
        if "page1" in pageNumber:
            path = "/expmodule1page1.html"
        elif "page2" in pageNumber:
            path = "/expmodule1page2.html"
        elif "page3" in pageNumber:
            path = "/expmodule1page3.html"
        console(data)
        url = "http://" + ip + path
        console(url)
        auth = (userid, passcode)
        try:
            loginResponse = session.get(loginURL, auth=auth)

            for i in range(2):
                if loginResponse.status_code != 200 or 'Session Expired' in loginResponse.text:
                    console("Attempt to login failed. Trying Again !! ")
                    loginResponse = session.get(loginURL, auth=auth)

            post = session.post(url, auth=auth, data=data)

            if "Provisioning complete" in post.text:
                console("Successfully Configured")
            else:
                raise Exception("something went wrong")
        except ConnectionError as e:
            raise Exception("Could not connect to the Web UI of the phone. Error: " + e.message)
        except Exception as e:
            raise Exception('Error occurred while Registering on extension: '
                            + self.phone_obj.phone_obj.phone.extensionNumber + ". Error: " + e.message)
        finally:
            session.close()

    def configurePhoneParameters(self, **kwargs):
        """
        This method is used to configure Parameters on the phone WUI.

        Keyword Args:
            parameters: Parameters to configure with their values (Dictionary)
        :returns: None
        :created by: Ramkumar. G
        :creation date:
        :last update by:
        :last update date:
        """
        parameters = str(kwargs.get('parameters', ''))
        if parameters == "Network":
            return self.networkSettings(**kwargs)
        elif parameters == "ConfigurationServer":
            return self.configServer(**kwargs)
        elif parameters == "Preferences":
            return self.preferences(**kwargs)
        elif parameters == "GlobalSettings":
            return self.regPhone(**kwargs)
        elif parameters == "AccountConfiguration":
            return self.accountConfig(**kwargs)
        elif parameters == "TroubleShootings":
            return self.troubleShooting(**kwargs)
        elif parameters == "ActionUrl":
            self.actionUrl(**kwargs)
        elif parameters == "expandableModule":
            return self.expandableModule(**kwargs)
        else:
            raise Exception("Wrong parameter passed.")

    def expandableModule(self, **kwargs):
        """
        :created by: Ramkumar. G
        :creation date:
        :last update by:
        :last update date:
        """
        console(kwargs)
        pageNumber = str(kwargs['page_number'])
        lab = str(kwargs.get('label'))
        ip = self.phone_obj.phone_obj.phone.ipAddress
        key = str(int(kwargs['position']))
        console("Key position: " + key)
        values = kwargs.get('value', '')
        type = "type" + key
        value = "value" + key
        label = "label" + key
        console(label)
        function = str(kwargs['function']).lower()
        console(function)

        if isinstance(values, PhoneComponent):
            val = str(values.phone_obj.phone_obj.phone.extensionNumber)
            data = {type: function, value: val, label: label}
        elif self.ipChecker(values) > 0:
            labelip = str(kwargs['label'])
            val = str(values) + labelip + ".xml"
            data = {type: function, value: val, label: labelip}
        else:
            val = str(values)
            data = {type: function, value: val, label: lab}

        session = requests.Session()
        loginURL = "http://" + ip + "/sysinfo.html"

        path = ""
        if "page1" in pageNumber:
            path = "/expmodule1page1.html"
        elif "page2" in pageNumber:
            path = "/expmodule1page2.html"
        elif "page3" in pageNumber:
            path = "/expmodule1page3.html"
        console(data)
        url = "http://" + ip + path
        console(url)
        auth = (userid, passcode)
        try:
            loginResponse = session.get(loginURL, auth=auth)

            for i in range(2):
                if loginResponse.status_code != 200 or 'Session Expired' in loginResponse.text:
                    console("Attempt to login failed. Trying Again !! ")
                    loginResponse = session.get(loginURL, auth=auth)

            post = session.post(url, auth=auth, data=data)

            if "Provisioning complete" in post.text:
                console("Successfully Configured")
            else:
                raise Exception("something went wrong")
        except ConnectionError as e:
            console("Could not connect to the Web UI of the phone. Error: ", newline=False)
            console(e.message)
        except Exception as e:
            logger.info('Error occurred while configuring expansion module settings on extension: '
                        + self.phone_obj.phone_obj.phone.extensionNumber, also_console=True)
            logger.info('ERROR: ' + e.message)
        finally:
            session.close()

    def accountConfig(self, **kwargs):
        """

        :created by: Ramkumar. G
        :creation date:
        :last update by:
        :last update date:
        """
        ip = self.phone_obj.phone_obj.phone.ipAddress
        session = requests.Session()
        loginURL = "http://" + ip + "/sysinfo.html"

        url = "http://" + ip + "/callforward.html"

        forwardAll = kwargs.get("ForwardNumberAll", "")
        StateAll1 = 0

        if isinstance(forwardAll, PhoneComponent):
            forwardAll = forwardAll.phone_obj.phone_obj.phone.extensionNumber
            StateAll1 = 1

        forwardBusy = kwargs.get("ForwardNumberBusy", "")
        StateBusy1 = 0

        if isinstance(forwardBusy, PhoneComponent):
            forwardBusy = forwardBusy.phone_obj.phone_obj.phone.extensionNumber
            StateBusy1 = 1

        forwardNoAnswer = kwargs.get("ForwardNumberNoAnswer", "")
        StateNoAnswer1 = 0

        if isinstance(forwardNoAnswer, PhoneComponent):
            forwardNoAnswer = forwardNoAnswer.phone_obj.phone_obj.phone.extensionNumber
            StateNoAnswer1 = 1

        ringNumber = str(kwargs.get("RingNumber", ""))
        dnd1 = int(kwargs.get("dnd", 0))

        payload = {
            "fwdNumberAll1": forwardAll,
            "StateAll1": StateAll1,
            "fwdNumberBusy1": forwardBusy,
            "StateBusy1": StateBusy1,
            "fwdNumberNoAnswer1": forwardNoAnswer,
            "StateNoAnswer1": StateNoAnswer1,
            "ringNumber1": ringNumber,
            "dnd1": dnd1
        }

        auth = (userid, passcode)
        try:
            loginResponse = session.get(loginURL, auth=auth)

            for i in range(2):
                if loginResponse.status_code != 200 or 'Session Expired' in loginResponse.text:
                    console("Attempt to login failed. Trying Again !! ")
                    loginResponse = session.get(loginURL, auth=auth)

            post = session.post(url, auth=auth, data=payload)
        except ConnectionError as e:
            console("Could not connect to the Web UI of the phone. Error: ", newline=False)
            console(e.message)
        except Exception as e:
            logger.info('Error occurred while configuring account configuration settings on extension: '
                        + self.phone_obj.phone_obj.phone.extensionNumber, also_console=True)
            logger.info('ERROR: ' + e.message)
        finally:
            session.close()

    def troubleShooting(self, **kwargs):
        """
        :created by: Ramkumar. G
        :creation date:
        :last update by:
        :last update date:
        """
        ip = self.phone_obj.phone_obj.phone.ipAddress
        session = requests.Session()
        loginURL = "http://" + ip + "/sysinfo.html"

        url = "http://" + ip + "/troubleshooting.html"

        logIp = kwargs.get('logIP', '0.0.0.0')
        logPort = kwargs.get('logPort', 514)
        payload = {
            "logIp": logIp,
            "logPort": logPort
        }

        auth = (userid, passcode)

        try:
            loginResponse = session.get(loginURL, auth=auth)

            for i in range(2):
                if loginResponse.status_code != 200 or 'Session Expired' in loginResponse.text:
                    console("Attempt to login failed. Trying Again !! ")
                    loginResponse = session.get(loginURL, auth=auth)

            post = session.post(url, auth=auth, data=payload)
        except ConnectionError as e:
            console("Could not connect to the Web UI of the phone. Error: ", newline=False)
            console(e.message)
        except Exception as e:
            logger.info('Error occurred while configuring Troubleshooting settings on extension: '
                        + self.phone_obj.phone_obj.phone.extensionNumber, also_console=True)
            logger.info('ERROR: ' + e.message)
        finally:
            session.close()

    def preferences(self, **kwargs):
        """
        This method is used to configure settings under Preferences section of the Phone WUI.

        :param:
            :parameters: Parameter to configure on WUI (Dictionary)
        :returns: None
        :created by: Ramkumar. G
        :creation date:
        :last update by:
        :last update date:
        """

        ip = self.phone_obj.phone_obj.phone.ipAddress
        session = requests.Session()
        loginURL = "http://" + ip + "/sysinfo.html"

        url = "http://" + ip + "/preferences.html"

        console("Going to " + url + " URL.")
        dialPlan = str(kwargs.get("DialPlan", "x+#|xx+*"))
        digitTimeout = int(kwargs.get("DigitTimeout", 4))
        displayDtmfDigits = kwargs.get("displayDtmfDigits", 0)
        allowAutoAnswer = int(kwargs.get("AllowAutoAnswer", 1))
        mapConfTo = str(kwargs.get("MapConferenceTo", ""))
        switchFocusToRingingLine = kwargs.get("switchFocusToRingingLine", 1)
        preferedLine = kwargs.get("preferedLine", 1)
        preferedLineTimeout = kwargs.get("preferedLineTimeout", 0)
        goodbyeCancelIncomingCall = kwargs.get("goodbyeCancelIncomingCall", 1)
        intercomType = kwargs.get("intercomType", 0)

        payload = {
            "dialPlan": dialPlan,
            "digitTimeout": digitTimeout,
            "sprecode": "",
            "pickupsprecode": "",
            "displayDtmfDigits": displayDtmfDigits,
            "playCallWaiting": 1,
            "stutteredDialTone": 1,
            "beepSupport": 1,
            "scrollDelay": 5,
            "switchFocusToRingingLine": switchFocusToRingingLine,
            "RemindCallWaiting": 0,
            "preferedLine": preferedLine,
            "preferedLineTimeout": preferedLineTimeout,
            "goodbyeCancelIncomingCall": goodbyeCancelIncomingCall,
            "mwiLedLine": 0,
            "dndApplicability": 1,
            "cfwdApplicability": 0,
            "intercomType": intercomType,
            "allowAutoAnswer": allowAutoAnswer,
            "intercomMuteMic": 1,
            "intercomWarn": 1,
            "intercomAllowBargeIn": 1,
            "groupListening": "",
            "mapRedialTo": "",
            "mapConfTo": mapConfTo,
            "toneSet": "US",
            "globalRingTone": 0,
            "ringToneLine1": -1,
            "ringToneLine2": -1,
            "ringToneLine3": -1,
            "ringToneLine4": -1,
            "ringToneLine5": -1,
            "ringToneLine6": -1,
            "ringToneLine7": -1,
            "ringToneLine8": -1,
            "ringToneLine9": -1,
            "ringToneLine10": -1,
            "ringToneLine11": -1,
            "ringToneLine12": -1,
            "ringToneLine13": -1,
            "ringToneLine14": -1,
            "ringToneLine15": -1,
            "ringToneLine16": -1,
            "ringToneLine17": -1,
            "ringToneLine18": -1,
            "ringToneLine19": -1,
            "ringToneLine20": -1,
            "ringToneLine21": -1,
            "ringToneLine22": -1,
            "ringToneLine23": -1,
            "ringToneLine24": -1,
            "prioAlertingEn": 1,
            "palertingkeyword1": 0,
            "palertingkeyword2": 0,
            "palertingkeyword3": 0,
            "palertingkeyword4": 0,
            "palertingkeyword5": 0,
            "palertingkeyword6": 0,
            "palertingkeyword7": 0,
            "palertingkeyword8": 0,
            "palertingkeyword9": 0,
            "palertingkeyword10": 0,
            "directedCallPickupPrefix": "",
            "ringSplash": 0,
            "acdAutoAvailTmr": 60,
            "timeFormat": 0,
            "dateFormat": 0,
            "timeServersEnabled": 1,
            "timeSrv1": "1.aastra.pool.ntp.org",
            "timeSrv2": "2.aastra.pool.ntp.org",
            "timeSrv3": "3.aastra.pool.ntp.org",
            "webLanguage": 0,
            "inputLanguage": "English",
            "language 1": "ftp://10.112.123.107//lan//lang_zh_cn.txt",
            "language 2": "",
            "language 3": "",
        }
        auth = (userid, passcode)

        try:
            loginResponse = session.get(loginURL, auth=auth)

            for i in range(2):
                str(i)
                if loginResponse.status_code != 200 or 'Session Expired' in loginResponse.text:
                    console("Attempt to login failed. Trying Again !! ")
                    loginResponse = session.get(loginURL, auth=auth)

            post = session.post(url, auth=auth, data=payload)
            if "Provisioning complete" in post.text:
                if kwargs.has_key("switchFocusToRingingLine"):
                    self.rebootPhone()
                return True
            else:
                logger.info("POST TEXT START", also_console=True)
                logger.info(post.text, also_console=True)
                logger.info("POST TEXT STOP", also_console=True)
                raise Exception("Something went wrong while configuring parameters on Web UI.")
        except ConnectionError as e:
            console("Could not connect to the Web UI of the phone. Error: ", newline=False)
            console(e.message)
        except Exception as e:
            logger.info('Error occurred while configuring Preferences settings on extension: '
                        + self.phone_obj.phone_obj.phone.extensionNumber, also_console=True)
            logger.info('ERROR: ' + e.message)
        finally:
            session.close()

    def networkSettings(self, **kwargs):
        """
        :created by: Ramkumar. G
        :creation date:
        :last update by:
        :last update date:
        """
        ip = self.phone_obj.phone_obj.phone.ipAddress
        models = self.phone_obj.phone_obj.phone.phoneModel
        model = models[5:]
        session = requests.Session()
        loginURL = "http://" + ip + "/sysinfo.html"

        url = "http://" + ip + "/provis.html"
        dhcpv6 = kwargs.get('IPv6', 0)
        dhcp = kwargs.get('DHCP', 0)
        hostname = kwargs.get('hostname', int(model))
        Validate_Certificates = kwargs.get('https_validate_certificates', 1)
        Check_Certificate_Expiration = kwargs.get('https_validate_expires', 1)
        Check_Certificate_Hostnames = kwargs.get('https_validate_hostname', 1)
        Trusted_Certificates_Filename = kwargs.get('https_trusted_certs', '')
        https_client_method = kwargs.get('client_method', 'TLS_SSLv3')
        PC_Port = kwargs.get('ethernet_link_port1', 0)
        DHCP_Download_Option = kwargs.get('dhcpoverride', 0)

        data = {
            "dhcpv6": dhcpv6,
            "dhcp": dhcp,
            "hostname": hostname,
            'DHCP_Download_Option': DHCP_Download_Option,
            'Validate_Certificates': Validate_Certificates,
            'Check_Certificate_Expiration': Check_Certificate_Expiration,
            'Check_Certificate_Hostnames': Check_Certificate_Hostnames,
            'Trusted_Certificates_Filename': Trusted_Certificates_Filename,
            'https_client_method': https_client_method,
            "ethernet_link_port0": 0,
            "ethernet_link_port1": PC_Port,
            "dhcpoverride": 0,
            "lldp": 1,
            "lldpInterval": 30,
            "natIp": "0.0.0.0",
            "natPort": 51620,
            "natRtpPort": 51720,
            "https_validate_certificates": 1,
            "https_validate_expires": 1,
            "https_validate_hostname": 1,
            "https_trusted_certs": "",
            "nonippri": 5,
            "vlanid1": 4095,
            "port1pri": 0
        }
        auth = (userid, passcode)
        try:
            loginURL = "http://" + ip + "/sysinfo.html"
            loginResponse = session.get(loginURL, auth=auth)

            for i in range(2):
                str(i)
                if loginResponse.status_code != 200 or 'Session Expired' in loginResponse.text:
                    console("Attempt to login failed. Trying Again !! ")
                    loginResponse = session.get(loginURL, auth=auth)

            post = session.post(url, auth=auth, data=data)

            if "Provisioning complete" in post.text:
                return True
            else:
                logger.info("POST TEXT START", also_console=True)
                logger.info(post.text, also_console=True)
                logger.info("POST TEXT STOP", also_console=True)
                raise Exception("Something went wrong while configuring network parameters on Web UI.")
        except ConnectionError as e:
            console("Could not connect to the Web UI of the phone. Error: ", newline=False)
            console(e.message)
        except Exception as e:
            logger.info('Error occurred while configuring network settings on extension: '
                        + self.phone_obj.phone_obj.phone.extensionNumber, also_console=True)
            logger.info('ERROR: ' + e.message)
        finally:
            session.close()

    def configServer(self, **kwargs):
        """

        :param kwargs:
        :returns:
        :created by: Ramkumar. G
        :creation date:
        :last update by:
        :last update date:
        """
        console("Inside config server")
        ip = self.phone_obj.phone_obj.phone.ipAddress
        models = self.phone_obj.phone_obj.phone.phoneModel
        model = models[5:]
        session = requests.Session()
        loginURL = "http://" + ip + "/sysinfo.html"

        url = "http://" + ip + "/configurationServer.html"
        protocol = str(kwargs.get('DownloadProtocol'))

        if protocol == "FTP":
            ftpserv = kwargs.get("FTP_Server", '')
            ftppath = kwargs.get('FTP_Path', '')
            ftpuser = kwargs.get('FTP_Username', '')
            ftppass = kwargs.get('FTP_Password', '')
            alttftp = kwargs.get('AlternateFTP', '')
            alttftppath = kwargs.get('AlternateFTPPath', '')
            value = {'ftpserv': ftpserv, 'ftppath': ftppath, 'ftpuser': ftpuser, 'ftppass': ftppass, 'alttftp': alttftp,
                     'alttftppath': alttftppath}

        elif protocol == "TFTP":
            tftp = kwargs.get('Primary_Server', '')
            tftppath = kwargs.get('Pri_TFTP_Path', '')
            alttftp = kwargs.get('AlternateTFTP', '')
            alttftppath = kwargs.get('AltTFTPPath', '')
            value = {'tftp': tftp, 'tftppath': tftppath, 'alttftp': alttftp, 'alttftppat': alttftppath}

        elif protocol == "HTTPS":
            alttftp = kwargs.get('AlternateTFTP', '')
            alttftppath = kwargs.get('AltTFTPPath', '')
            httpsserv = kwargs.get('Https_Serv', '')
            httpspath = kwargs.get('Https_Path', '')
            httpsport = kwargs.get('Https_Port', 443)
            value = {'httpsserv': httpsserv, 'httpspath': httpspath, 'httpsport': httpsport, 'alttftp': alttftp,
                     'alttftppat': alttftppath}

        elif protocol == "HTTP":
            console("http")
            alttftp = kwargs.get('AlternateTFTP', '')
            alttftppath = kwargs.get('AltTFTPPath', '')
            httpserv = kwargs.get('Http_Serv', '')
            httppath = kwargs.get('Http_Path', '')
            httpport = kwargs.get('Http_Port', 80)
            value = {'httpserv': httpserv, 'httppath': httppath, 'httpport': httpport, 'alttftp': alttftp,
                     'alttftppat': alttftppath}

        autoResyncMode = kwargs.get('autoResyncMode', '')
        autoResyncTime = kwargs.get('autoResyncTime', '')
        maxDelay = kwargs.get('maxDelay', '')
        days = kwargs.get('days', '')
        postList = kwargs.get('postList', '')

        values = {'autoResyncMode': autoResyncMode, 'autoResyncTime': autoResyncTime, 'maxDelay': maxDelay,
                  'days': days, 'postList': postList, 'protocol': protocol}

        data = value.copy()
        data.update(values)

        auth = (userid, passcode)

        try:
            loginResponse = session.get(loginURL, auth=auth)

            for i in range(2):
                str(i)
                if loginResponse.status_code != 200 or 'Session Expired' in loginResponse.text:
                    console("Attempt to login failed. Trying Again !! ")
                    loginResponse = session.get(loginURL, auth=auth)
            post = session.post(url, auth=auth, data=data)

            if "Provisioning complete" in post.text:
                return logger.info("Successfully Configured")
            else:
                logger.info("POST TEXT START", also_console=True)
                logger.info(post.text, also_console=True)
                logger.info("POST TEXT STOP", also_console=True)
                raise Exception("Something went wrong while configuring parameters on Web UI.")
        except ConnectionError as e:
            console("Could not connect to the Web UI of the phone. Error: ", newline=False)
            console(e.message)
        except Exception as e:
            logger.info('Error occurred while configuring Configuration Server settings on extension: '
                        + self.phone_obj.phone_obj.phone.extensionNumber, also_console=True)
            logger.info('ERROR: ' + e.message)
        finally:
            session.close()

    def regPhone(self, **kwargs):
        """
        This method is used to register the phone with the Mitel call Managers.

        In case of MiVoice 400, only line1 is registered by default. Pass the other lines in a list to register them
        also.

        :param:
            :pbx: Call Manager of the phone
            :additionalLines: Additional Lines to register (Optional)

        :returns:
        :created by: Ramkumar. G
        :creation date:
        :last update by: Milind Patil
        :last update date: 07/01/2021
        """
        ip = self.phone_obj.phone_obj.phone.ipAddress
        phone = self.phone_obj.phone_obj.phone.extensionNumber
        pbx = kwargs['pbx']
        callWaiting = kwargs.get('CallWaiting', 1)
        screenName = kwargs.get('ScreenName', phone)
        authName=kwargs.get('AuthName',phone)
        if isinstance(authName,PhoneComponent):
            authName=authName.phone_obj.phone_obj.phone.extensionNumber
        registrationPeriod = kwargs.get('registrationPeriod', 0)
        regRenewal = kwargs.get('regRenewal', 15)

        outboundProxyPort = '5060'
        if pbx == "MiV400" or pbx == "MiV5000":
            if pbx == "MiV400":
                pbxIP = MiV400
                OutProxy = ''
                outboundProxyPort = '0'
            else:
                pbxIP = MiV5000
                OutProxy = MiV5000
            password = '22222222'
        elif pbx == "Clearspan":
            pbxIP = Clearspan
            OutProxy = ClearspanOutProxy
            password = 'hclindia'
        else:
            if pbx == "Asterisk":
                pbxIP = Asterisk
                OutProxy = Asterisk
            elif pbx == "MxOne":
                pbxIP = MxOne
                OutProxy = MxOne
            elif pbx == "SipX":
                pbxIP = SipX
                OutProxy = SipX
            password = self.phone_obj.phone_obj.phone.extensionNumber

        session = requests.Session()
        loginURL = "http://" + ip + "/sysinfo.html"

        if kwargs['pbx'] == 'MiV400':
            url = "https://" + ip + "/SIPsettingsLine1.html"
        else:
            url = "http://" + ip + "/globalSIPsettings.html"
        auth = (userid, passcode)

        try:
            loginResponse = session.get(loginURL, auth=auth, verify=False)

            for i in range(2):
                if loginResponse.status_code != 200 or 'Session Expired' in loginResponse.text:
                    console("Attempt to login failed. Trying Again !! ")
                    loginResponse = session.get(loginURL, auth=auth)

            payload = {'screenName': screenName,
                       'screenName2': phone,
                       'userName': phone,
                       'dispName': phone,
                       'authName': authName,
                       'password': password,
                       'blaName': '',
                       'mode': '',
                       'callWaiting': callWaiting,
                       'proxyIp': pbxIP,
                       'proxyPort': 5060,
                       'backupProxyIp': "0.0.0.0",
                       'backupProxyPort': 0,
                       'outboundProxy': OutProxy,
                       'outboundProxyPort': 5060,
                       'backupOutboundProxy': "0.0.0.0",
                       'backupOutboundProxyPort': 0,
                       'regIp': pbxIP,
                       'regPort': 5060,
                       'backupRegIp': "0.0.0.0",
                       'backupRegPort': 0,
                       'registrationPeriod': registrationPeriod,
                       'centraconf': '',
                       'AFESubscriptionPeriod': 3600,
                       'UaProfileSub': 0,
                       'UaProfileSubsciptionPeriod': 86400,
                       'sessionTimer': 0,
                       't1Timer': 0,
                       't2Timer': 0,
                       'transTimer': 4000,
                       'transportProtocol': 1,
                       'sipLocalPort': 5060,
                       'sipLocalTLSPort': 5061, 'regRetry': 1800, 'regTimeout': 120, 'regRenewal': regRenewal,
                       'blfPeriod': 3600, 'acdPeriod': 3600, 'blaPeriod': 300,
                       'blacklistDur': 300, 'park+pickup+config': '', 'rtpPort': 3000, 'useNTE': 1, 'dtmfMethod': 0,
                       'srtpMode': 0, 'codec1': -3, 'codec2': -1, 'codec3': -1, 'codec4': -1, 'codec5': -1,
                       'codec6': -1, 'codec7': -1, 'codec8': -1, 'codec9': -1, 'codec10': -1,
                       'ptime': 30, 'adNumber': '', 'adTimeout': 0
                       }

            post = session.post(url, auth=auth, data=payload)

            if "Provisioning complete" in post.text:
                logger.info("Successfully registered the phone with URL: " + self.phone_obj.phone_obj.phone.ipAddress
                            + " with " + pbx + " call manager", also_console=True)
            else:
                raise Exception("Something went wrong while configuring parameters on Web UI.")
        except ConnectionError as e:
            logger.error("Could not connect to the Web UI of the phone. Error: ")
            logger.error(e.message)
            raise Exception("Could not connect to the URL" + self.phone_obj.phone_obj.phone.ipAddress
                            + ". Check logs for more info.")
        except Exception as e:
            logger.info('ERROR: ' + e.message)
            raise Exception('Error occurred while Registering on extension: '
                            + self.phone_obj.phone_obj.phone.extensionNumber + ". Check logs for more info.")
        finally:
            session.close()

    def unregPhone(self, **kwargs):
        """
        This method is used to unregister the phone.

        :created by: Ramkumar. G
        :creation date:
        :last update by: Vikhyat Sharma
        :last update date: 17/10/2020
        """
        ip = self.phone_obj.phone_obj.phone.ipAddress

        session = requests.Session()
        loginURL = "http://" + ip + "/sysinfo.html"

        url = "http://" + ip + "/globalSIPsettings.html"
        if kwargs['pbx'] == 'MiV400':
            url = "https://" + ip + "/SIPsettingsLine1.html"

        auth = (userid, passcode)
        try:
            loginResponse = session.get(loginURL, auth=auth, verify=False)

            for i in range(2):
                if loginResponse.status_code != 200 or 'Session Expired' in loginResponse.text:
                    console("Attempt to login failed. Trying Again !! ")
                    loginResponse = session.get(loginURL, auth=auth, verify=False)

            payload = {'screenName': '', 'screenName2': '', 'userName': '', 'dispName': '', 'authName': '',
                       'password': '',
                       'blaName': '', 'mode': '', 'callWaiting': 1,
                       'proxyIp': '', 'proxyPort': 0,
                       'backupProxyIp': 0, 'backupProxyPort': 0,
                       'outboundProxy': '', 'outboundProxyPort': 0,
                       'backupOutboundProxy': 0, 'backupOutboundProxyPort': 0,
                       'regIp': '', 'regPort': 0,
                       'backupRegIp': 0, 'backupRegPort': 0,
                       'registrationPeriod': 0, 'centraconf': '',
                       'AFESubscriptionPeriod': 3600,
                       'UaProfileSub': 0, 'UaProfileSubsciptionPeriod': 86400,
                       'sessionTimer': 0, 't1Timer': 0, 't2Timer': 0, 'transTimer': 4000,
                       'transportProtocol': 1,
                       'sipLocalPort': 5060, 'sipLocalTLSPort': 5061, 'regRetry': 1800, 'regTimeout': 120,
                       'regRenewal': 15,
                       'blfPeriod': 3600, 'acdPeriod': 3600, 'blaPeriod': 300,
                       'blacklistDur': 300, 'park+pickup+config': '', 'rtpPort': 3000, 'useNTE': 1, 'dtmfMethod': 0,
                       'srtpMode': 0,
                       'codec1': -3, 'codec2': -1, 'codec3': -1, 'codec4': -1, 'codec5': -1,
                       'codec6': -1, 'codec7': -1, 'codec8': -1, 'codec9': -1, 'codec10': -1,
                       'ptime': 30, 'adNumber': '', 'adTimeout': 0}

            post = session.post(url, auth=auth, data=payload)
            if "Provisioning complete" in post.text:
                logger.info("Successfully configured parameters on Web UI.", also_console=True)
                return True
            else:
                console("POST START")
                console(post.text)
                console("POST START")
                raise Exception("Something went wrong while configuring parameters on Web UI.")
        except ConnectionError as e:
            logger.error("Could not connect to the Web UI of the phone. Error: ")
            logger.error(e.message)
            console("Could not connect to the Web UI of the phone. Error: ", newline=False)
            console(e.message)
        except Exception as e:
            logger.info('Error occurred while Registering on extension: '
                        + self.phone_obj.phone_obj.phone.extensionNumber, also_console=True)
            logger.info('ERROR: ' + e.message)
        finally:
            session.close()

    def updatePhoneFirmware(self, **kwargs):
        """
        :created by: Ramkumar. G
        :creation date:
        :last update by:
        :last update date:
        """
        ip = self.phone_obj.phone_obj.phone.ipAddress
        session = requests.Session()
        loginURL = "http://" + ip + "/sysinfo.html"

        if kwargs['pbx'] == 'MiV400':
            url = "https://" + ip + "/upgrade.html"
        else:
            url = "http://" + ip + "/upgrade.html"

        auth = (userid, passcode)
        models = self.phone_obj.phone_obj.phone.phoneModel
        model = models[5:]

        try:
            loginResponse = session.get(loginURL, auth=auth)

            for i in range(2):
                if loginResponse.status_code != 200 or 'Session Expired' in loginResponse.text:
                    console("Attempt to login failed. Trying Again !! ")
                    loginResponse = session.get(loginURL, auth=auth)
            protocol = str(kwargs.get('protocol', 'ftp')).lower()
            if protocol == "ftp":
                server = kwargs['ServerIP']
                path = kwargs.get('path', '')
                username = kwargs['username']
                password = kwargs['password']
                file = model + '.st'
                payload = {
                    'protocol': protocol,
                    'server': server,
                    'path': path,
                    'username': username,
                    'password': password,
                    'file': file
                }

            post = session.post(url, auth=auth, data=payload)
        except ConnectionError as e:
            console("Could not connect to the Web UI of the phone. Error: ", newline=False)
            console(e.message)
        except Exception as e:
            logger.info('Error occurred while Registering on extension: '
                        + self.phone_obj.phone_obj.phone.extensionNumber, also_console=True)
            logger.info('ERROR: ' + e.message)
        finally:
            session.close()

    def deleteFromDirectory(self, **kwargs):
        """
        This method is used to delete the extensions from the directory.

        Keyword Args:
            entryToDelete: Entry to delete from directory (Specific phone/ all)
            directoryKey: Directory key to press (Optional)

        :returns: None
        :creation date: 08/04/2020
        :created by: Sharma
        :last update by: Vikhyat Sharma
        :last update date: 24/08/2020
        """
        entryToDelete = kwargs['entryToDelete']
        if isinstance(entryToDelete, PhoneComponent):
            entryToDelete = entryToDelete.phone_obj.phone_obj.phone.extensionNumber

        directoryKey = kwargs.get('directoryKey', 'Directory')
        self.phone_obj.press_key(directoryKey)

        if self.phone_obj.phone_type in ("Mitel6865i", "Mitel6910"):
            self.phone_obj.press_key("ProgramKey8")
            self.phone_obj.press_key("ScrollDown")
            self.phone_obj.press_key("ScrollRight")
            self.phone_obj.sleep(1)
            if self.phone_obj.verify_display_message_contents('Directory empty'):
                logger.warn("No saved entry to delete from directory.")
            else:
                for _ in range(2):
                    self.phone_obj.press_key("ScrollDown")
                    self.phone_obj.sleep(1)
                for _ in range(2):
                    self.phone_obj.press_key('ProgramKey6')
            self.phone_obj.press_key("GoodBye")
        elif self.phone_obj.phone_type in ("Mitel6867i", "Mitel6869i", "Mitel6920", "Mitel6930"):
            if self.phone_obj.verify_display_message_contents("Delete"):
                logger.info("Deleting Existing Entries in Directory on extension: "
                            + self.phone_obj.phone_obj.phone.extensionNumber)
                console("Deleting Existing Entries in Directory on extension: "
                        + self.phone_obj.phone_obj.phone.extensionNumber)
                if entryToDelete == "All":
                    self.phone_obj.press_key('ScrollLeft')
                else:
                    self.phone_obj.press_key('ScrollRight')
                self.phone_obj.press_softkey(2)
                self.phone_obj.press_softkey(2)
            else:
                logger.info("No saved entry to delete from directory.", also_console=True)
        else:
            raise Exception("Model " + self.phone_obj.phone_type + " is not supported for now.")

    def addInDirectory(self, **kwargs):
        """
        This method is used to save a number in directory.

        Keyword Args:
            phone: Phone to save in directory
            directoryKey: Directory Key to press (Optional)
            prefix: Prefix to add while saving the number (Optional)
            suffix: Suffix to add while saving the number (Optional)

        :returns: None
        :created by: Sharma
        :creation date: 08/04/2020
        :last update by: Vikhyat Sharma
        :last update date: 04/02/2021
        """
        phoneToSave = kwargs['phone']
        directoryKey = kwargs.get('directoryKey', 'Directory')
        prefix = kwargs.get('prefix', '')
        suffix = kwargs.get('suffix', '')

        if isinstance(phoneToSave, PhoneComponent):
            phoneToSave = phoneToSave.phone_obj.phone_obj.phone.extensionNumber

        self.deleteFromDirectory(entryToDelete='All', directoryKey=directoryKey)

        # adding new entry
        if self.phone_obj.phone_type == "Mitel6865i":
            self.phone_obj.press_key("ProgramKey8")
            self.phone_obj.press_key("ScrollDown")
            self.phone_obj.sleep(1)

            for i in range(2):
                self.phone_obj.press_key("ScrollRight")
                self.phone_obj.sleep(1)

            if prefix == '+':
                self.phone_obj.long_press_key("DialPad0")
            else:
                self.phone_obj.input_a_number(prefix)
            self.phone_obj.input_a_number(phoneToSave)

            if suffix == '+':
                self.phone_obj.long_press_key('DialPad0')
            else:
                self.phone_obj.input_a_number(suffix)

            for i in range(5):
                self.phone_obj.press_key("ScrollDown")

            self.phone_obj.input_a_number("7777333333222222266666688888866666")  # SECNUM
            self.phone_obj.sleep(6)
            for i in range(2):
                self.phone_obj.press_key("ScrollDown")

            self.phone_obj.press_key("GoodBye")

        elif self.phone_obj.phone_type in ('Mitel6920', 'Mitel6930', 'Mitel6867i', 'Mitel6869i'):
            self.phone_obj.press_softkey(3)
            self.phone_obj.press_key("ScrollDown")
            self.phone_obj.input_a_number("77773322266886")  # SECNUM
            self.phone_obj.press_key("ScrollUp")
            self.phone_obj.press_key("ScrollRight")
            self.phone_obj.press_key("ScrollDown")

            if prefix == '+':
                self.phone_obj.long_press_key("DialPad0")
            else:
                self.phone_obj.input_a_number(prefix)
            self.phone_obj.input_a_number(phoneToSave)

            if suffix == '+':
                self.phone_obj.long_press_key('DialPad0')
            else:
                self.phone_obj.input_a_number(suffix)
            self.phone_obj.press_softkey(1)
            self.phone_obj.press_key("GoodBye")
        elif self.phone_obj.phone_type == 'Mitel6940':
            self.phone_obj.press_softkey(3)
            self.phone_obj.input_a_number("77773322266886")  # SECNUM
            self.phone_obj.press_key("ScrollLeft")
            self.phone_obj.press_key("ScrollDown")
            self.phone_obj.press_key("ScrollRight")
            if prefix == '+':
                self.phone_obj.long_press_key("DialPad0")
            else:
                self.phone_obj.input_a_number(prefix)
            self.phone_obj.input_a_number(phoneToSave)

            if suffix == '+':
                self.phone_obj.long_press_key('DialPad0')
            else:
                self.phone_obj.input_a_number(suffix)
            self.phone_obj.press_softkey(1)
            self.phone_obj.press_key("GoodBye")
        else:
            raise Exception("SET Type: " + str(self.phone_obj.phone_type) + " is not supported for now.")

    def configureXMLParameter(self, **kwargs):
        """
        This method is used to configure the parameters on the phone through XML.

        :param: Parameters to configure

        :returns: None
        :created by: Avishek Ranjan/ Abhishek Pathak
        :creation date:
        :last modified by: Sharma
        :last modification date: 30/04/2020
        """

        logger.info("Configuring parameters on extension: " + self.phone_obj.phone_obj.phone.extensionNumber +
                    " using XML.", also_console=True)
        ip_phone = str(self.phone_obj.phone_obj.phone.ipAddress)
        # ip_phone = ipAddress
        ip_phone_new = str(ip_phone)
        # console(ip_phone_new)
        xmlInput = self.prettify(**kwargs)
        # console(xmlInput)
        self.callPerl(xmlInput, ip_phone_new)

    def prettify(self, **kwargs):
        """
        Below method is used to create a preetified XML file.

        :param:
            :kwargs: Dictionary containing the parameters and values to set in the XML File.
                :xmlType: the root element of the XML i.e., AastraIPPhoneConfiguration, AastraIPExecute

        :returns: Preetified XML String
        :created by: Abhishek Pathak/Avishek Ranjan
        :creation date:
        :last update by: Sharma
        :last update date: 29/06/2020
        """
        from xml.etree.ElementTree import Element, SubElement, Comment
        from xml.etree import ElementTree
        from xml.dom import minidom

        local = "local"

        rootElement = Element('AastraIPPhoneConfiguration', {'setType': local})
        for parameter, value in kwargs.items():
            ConfigurationItem = SubElement(rootElement, 'ConfigurationItem', {'setType': local})
            Parameter = SubElement(ConfigurationItem, 'Parameter')
            Parameter.text = str(parameter)
            Value = SubElement(ConfigurationItem, 'Value')
            if isinstance(value, PhoneComponent):
                value = value.phone_obj.phone_obj.phone.extensionNumber
            Value.text = str(value)

        rough_string = ElementTree.tostring(rootElement, 'utf-8')
        reparsed = minidom.parseString(rough_string)
        return reparsed.toprettyxml(indent="  ")

    def callPerl(self, xml_input, ip_phone_new):
        """

        :param xml_input:
        :param ip_phone_new:
        :returns: None
        :created by: Avishek Ranjan/Abhishek Pathak
        :creation date:
        :last modified by:
        :last modification date:
        """
        import subprocess
        console("Inside the perl method")
        retCode = subprocess.call(
            ["perl", "C:\\Robo_SVN_5.1\\Desktop_Automation\\lib\\Test.pl", xml_input, ip_phone_new],
            stdout=subprocess.PIPE)
        if retCode == 0:
            logger.info("Successfully configured XML Parameters", also_console=True)
        else:
            raise Exception("Could not configure XML parameters.")

    def serverConnection(self, **kwargs):
        """

        """
        import pysftp
        console(kwargs)
        yaml_file = yaml.load(open(os.path.join(os.path.dirname((os.path.dirname(__file__))),
                                                'Variables/WebUIDetails.yaml')), Loader=yaml.FullLoader)
        hostname = kwargs['parameter']['Hostname']
        Username = kwargs['parameter']['Username']
        Password = kwargs['parameter']['Password']
        fileName = kwargs['fileName']
        console(fileName)
        remoteFilePath = yaml_file['remoteFilePath'] + '/' + fileName
        console(remoteFilePath)
        localFilePath = os.path.join(os.path.dirname((os.path.dirname(__file__))), 'Downloads/' + fileName)
        console(localFilePath)
        sftp = pysftp.Connection(host=hostname, username=Username, password=Password)
        directory_structure = sftp.listdir_attr()
        sftp.cwd('/var/www/html/configuration/')
        directory_structure = sftp.listdir_attr()
        sftp.put(localFilePath, remoteFilePath)
        for attr in directory_structure:
            print ("file has moved")

    def addParamtersToCfgfile(self, **kwargs):
        fileName = kwargs['fileName']
        parameter = kwargs['parameter']
        if not os.path.exists("C:/Robo_SVN_5.1/Desktop_Automation/Downloads/"):
            os.makedirs("C:/Robo_SVN_5.1/Desktop_Automation/Downloads/")
        write_file = open("C:/Robo_SVN_5.1/Desktop_Automation/Downloads/" + fileName, "wb")
        write_file.write("$telnet enabled: Telnet for support1410!$\n")
        write_file.write("sip register blocking: 0\n")
        for k, v in parameter.items():
            write_file.write(k + '\n')
            write_file.write(v + '\n')

    def delete_file(self, **kwargs):
        fileName = kwargs['fileName']
        if os.path.exists("C:/Robo_SVN_5.1/Desktop_Automation/Downloads" + "/" + fileName):
            os.remove("C:/Robo_SVN_5.1/Desktop_Automation/Downloads" + "/" + fileName)

    def updateDateTime(self, **kwargs):
        """
        Below routine is used to set the Date and Time on phone.

        :param:
            :self: PhoneComponent object
            :kwargs: Dictionary for getting the arguments needed:
                :date: Date in 'DD/MM/YYYY' format or 'Today'
                :time: Time in 'HH:MM:SS' format
        :returns: None

        :created by : Aman
        :creation date: 20/05/2020
        :updated by :
        :last update date :
        """

        if (len(kwargs) >= 2):
            date = kwargs['date']
            time = kwargs['time']
            if date == 'Today':
                from datetime import datetime
                today = datetime.today().date()  # Return Current Date in 'YYYY/MM/DD' format
                today = str(today)
                date = today[8:10] + '/' + today[5:7] + '/' + today[0:4]  # Converting Date into 'DD/MM/YYYY' format

            logger.info("Updating Date as <b>" + date + "</b> and Time as <b>" + time + "</b> on Phone <b>"
                        + self.phone_obj.phone_obj.phone.extensionNumber + "</b>.", html=True)

            console("Updating Date as " + date + " and Time as " + time + " on Phone "
                    + self.phone_obj.phone_obj.phone.extensionNumber + ".")

            self.phone_obj.press_key('Menu')
            for i in range(5):
                self.phone_obj.press_key("ScrollLeft")

            if not self.phone_obj.verify_display_message_contents("Time and Date"):
                if not self.phone_obj.verify_display_message_contents(u"ﺦﻳﺭﺎﺘﻟا ﻭ ﺖﻗﻮﻟا"):
                    console("Time and Date not verified !!!")
                    raise Exception("Time and Date not verified !!!")
                else:
                    console("Time and Date verified !!!")
                    logger.info("Time and Date verified !!!")
            else:
                logger.info("Time and Date verified !!!")
                console("Time and Date verified !!!")

            self.phone_obj.press_key("ScrollDown")
            self.phone_obj.press_key("ScrollDown")

            if not self.phone_obj.verify_display_message_contents("Set Date and Time"):
                if not self.phone_obj.verify_display_message_contents(u"ﺖﻗﻮﻟاﻭ ﺦﻳﺭﺎﺘﻟا ﻂﺒﺿ"):
                    console("Set Date and Time not verified !!!")
                    raise Exception("Set Date and Time not verified !!!")
                else:
                    console("Set Date and Time verified !!!")
                    logger.info("Set Date and Time verified !!!")
            else:
                logger.info("Set Date and Time verified !!!")
                console("Set Date and Time verified !!!")

            self.phone_obj.press_softkey(1)

            if not self.phone_obj.verify_display_message_contents("Time and Date"):
                if not self.phone_obj.verify_display_message_contents(u"ﺦﻳﺭﺎﺘﻟا ﻭ ﺖﻗﻮﻟا"):
                    console("Time and Date not verified !!!")
                    raise Exception("Time and Date not verified !!!")
                else:
                    console("Time and Date verified !!!")
                    logger.info("Time and Date verified !!!")
            else:
                logger.info("Time and Date verified !!!")
                console("Time and Date verified !!!")

            if self.phone_obj.verify_display_message_contents("Time Server 1"):
                self.phone_obj.press_key("Enter")
            if not self.phone_obj.verify_display_message_contents(u"1 ﺖﻗﻮﻟا ﺮﻓﺮﺳ"):  # Verifying Time Server 1 in Arabic
                self.phone_obj.press_key("Enter")
            self.phone_obj.press_key("ScrollDown")
            for i in time:
                if i != ':':
                    Dial = "DialPad" + str(i)
                    self.phone_obj.press_key(Dial)
            self.phone_obj.sleep(1)
            self.phone_obj.press_key("ScrollDown")
            for i in date:
                if i != '/':
                    Dial = "DialPad" + str(i)
                    self.phone_obj.press_key(Dial)
            self.phone_obj.sleep(1)
            self.phone_obj.press_softkey(1)
        else:
            logger.error("Please check the arguments passed: %s" % kwargs)
            raise Exception("Please check the arguments passed: %s" % kwargs)
        self.phone_obj.sleep(2)

    def createfile(self, **kwargs):
        """
        This method is used to create a configuration file for desktop phones with some default configuration
        along with the passed configuration.

        Keyword Args:
            fileName: File name of the created file i.e., Aastra/Startup
            parameter: Parameter dictionary to be set in the config file.

        :returns: None
        :created by: Ramkumar. G
        :creation date:
        :last update by:
        :last update date:
        """
        fileName = kwargs['fileName']
        parameter = kwargs.get('parameter')
        try:
            filePath = os.path.join(os.path.dirname((os.path.dirname(__file__))), "configuration")
            if os.path.exists(filePath):
                import shutil
                shutil.rmtree(filePath)
            os.mkdir(os.path.join(os.path.dirname((os.path.dirname(__file__))), "configuration\\"))
            filePath = os.path.join(os.path.dirname((os.path.dirname(__file__))), "configuration\\" + fileName)

            with open(filePath, 'w+') as configFile:
                if '.xml' in fileName:
                    xmlInput = self.prettify(**parameter)
                    configFile.write(xmlInput)
                elif '.csv' in fileName:
                    number = parameter['number']
                    firstName = parameter.get('firstName', 'First')
                    lastName = parameter.get('lastName', 'last')
                    if isinstance(number, PhoneComponent):
                        number = number.phone_obj.phone_obj.phone.extensionNumber
                    csvwriter = csv.writer(configFile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                    rows = [firstName, lastName, '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '1', '1',
                            '1', number, '-1', 'V2']
                    csvwriter.writerow(rows)
                else:
                    configFile.write("$telnet enabled: Telnet for support1410!$\n")
                    configFile.write("sip register blocking: 0\n")
                    configFile.write("enable atap: 36863\n")
                    for k, v in parameter.items():
                        if isinstance(v, PhoneComponent):
                            v = v.phone_obj.phone_obj.phone.extensionNumber
                        configFile.write(k + ':' + v)
                        configFile.write('\n')
            logger.info("Successfully created " + fileName + " file.", also_console=True)
        except Exception as er:
            raise Exception("Could not create {} file!! Got exception: {}".format(fileName, er.message))

    def verifyDownloadedFile(self, **kwargs):
        """

        """
        import ast
        connection = str(kwargs.get("connection", "FTP"))
        folder = str(kwargs.get('folderName'))
        file = str(kwargs.get('fileName'))
        file = ast.literal_eval(file)
        files_tc = []
        for key, files in file.items():
            i = ast.literal_eval(files)
            for f in i:
                files_tc.append(f)
        if connection == "FTP":
            from ftplib import FTP
            ftp = FTP()
            ftp.set_debuglevel(2)
            ftp.connect(Ftpserver, FtpPort)
            ftp.login(FtpUser, FtpPass)
            a = ftp.nlst(folder)
            a = [i.split("_")[-1] for i in a]
            for tc_f in files_tc:
                if tc_f in a:
                    console(tc_f)
                    console("present")
                else:
                    logger.error(tc_f + " is not present in " + folder + " on sever")
            ftp.quit()

    def createConnection(self, **kwargs):
        """

        """
        connection = str(kwargs.get('connection', 'FTP'))
        folder = kwargs.get('folderName', '')
        if connection == "FTP":
            from ftplib import FTP
            import os
            ftp = FTP()
            ftp.set_debuglevel(2)
            ftp.connect(Ftpserver, FtpPort)
            ftp.login(FtpUser, FtpPass)

            if not folder:
                ftp.quit()

            if folder:
                if folder in ftp.nlst():
                    a = ftp.nlst(folder)
                    for f in a:
                        ftp.delete(f)
                    ftp.rmd(folder)

                ftp.mkd("/" + folder)
                ftp.cwd("/" + folder)
                ftp.quit()

        elif connection == "HTTP":
            import pysftp
            sftp = pysftp.Connection(host="10.112.123.89", username="root", password="Jafe@20_20")
            if not folder:
                sftp.close()
            sftp.cwd('/var/www/html/')
            if folder not in sftp.listdir():
                sftp.mkdir(folder)
            sftp.cwd('/var/www/html/' + folder)
            console(sftp.pwd)
            sftp.close()

        else:
            console("Passed parameter is not a valid one")

    def sendFileToServer(self, **kwargs):
        """

        :created by:
        :creation date:
        :last update by: Sharma
        :last update date: 31/08/2020
        """
        file = kwargs.get('fileName')
        folder = kwargs.get('folderName')
        connection = kwargs.get('connection')
        time.sleep(30)

        logger.info("Sending <b>{}</b> to <b>{}</b> server".format(file, connection), html=True)
        console("Sending {} to {} server".format(file, connection))

        if file.lower() == 'background image':
            configFilePath = os.path.join(os.path.dirname((os.path.dirname(__file__))), "TestFiles/")
            if self.phone_obj.phone_type in ('Mitel6920', 'Mitel6867i'):
                configFilePath += '6920.jpg'
            elif self.phone_obj.phone_type in ('Mitel6930', 'Mitel6869i'):
                configFilePath += '6930.jpg'
        else:
            configFilePath = os.path.join(os.path.dirname((os.path.dirname(__file__))), "configuration/" + file)
        if connection == "FTP":
            from ftplib import FTP
            ftp = FTP()
            ftp.set_debuglevel(2)
            ftp.connect(Ftpserver, FtpPort)
            ftp.login(FtpUser, FtpPass)
            if folder != "root":
                if folder in ftp.nlst():
                    a = ftp.nlst(folder)
                    for f in a:
                        ftp.delete(f)
                    ftp.rmd(folder)
                ftp.mkd("/" + folder)
                ftp.cwd("/" + folder)
            fp = open(configFilePath, 'rb')
            ftp.storbinary('STOR %s' % os.path.basename(configFilePath), fp, 1024)
            fp.close()
            ftp.quit()
        elif connection == "HTTP":
            cnopts = pysftp.CnOpts()
            cnopts.hostkeys = None
            with pysftp.Connection(host="10.112.123.89", username="root", password="Jafe@20_20", cnopts=cnopts) as sftp:
                sftp.cwd('/var/www/html/')
                if folder in sftp.listdir():
                    logger.warn("{0} folder is already present under path: {1}".format(folder, sftp.pwd))
                    sftp.cwd('/var/www/html/' + folder)
                    logger.warn("Deleting existing files in the folder.")
                    for i in sftp.listdir():
                        if i:
                            sftp.remove(i)
                    remoteFilePath = sftp.pwd + "/" + file
                    sftp.put(configFilePath, remoteFilePath)
                    if file not in sftp.listdir():
                        raise Exception(file + " did not move to the folder: " + folder)
                else:
                    logger.warn(folder + "is not present on the server under path: {}".format(sftp.getcwd()))
                    logger.warn("Creating folder {0} under path: {1}".format(folder, sftp.pwd))
                    sftp.chdir('/var/www/html/' + folder)

    def readServerFile(self, **kwargs):
        fileName = str(kwargs["fileName"])
        connection = str(kwargs.get("connection"))
        parameter = str(kwargs.get("parameter"))
        folder = str(kwargs.get("folder"))
        option = str(kwargs.get('option'))
        if connection == "FTP":
            from ftplib import FTP
            ftp = FTP()
            ftp.set_debuglevel(2)
            ftp.connect(Ftpserver, FtpPort)
            ftp.login(FtpUser, FtpPass)
            ftp.cwd(folder)
            a = (ftp.nlst())
            for i in a:
                if i.split("_")[-1] == fileName:
                    path = os.path.join(os.path.dirname(__file__)) + "/" + fileName
                    if os.path.exists(path):
                        os.remove(path)
                    ftp.retrbinary('RETR ' + i, open(path, 'wb').write)
                    time.sleep(5)
                    with open(path, "r") as f:
                        for j in f:
                            if parameter[-8:] in j:
                                if option == "masked":
                                    if "*" in str(j.split(":")[1]):
                                        console(str(j.split(":")[-2]) + " parameter is masked in the " + fileName)
                                    else:
                                        raise Exception(
                                            str(j.split(":")[-2]) + " parameter is not masked in the " + fileName)
                                elif option == "not masked":
                                    if not "*" in str(j.split(":")[1]):
                                        console(str(j.split(":")[-2]) + " parameter is not masked in the " + fileName)
                                    else:
                                        raise Exception(
                                            str(j.split(":")[-2]) + " parameter is masked in the " + fileName)
                                else:
                                    console(parameter + " parameter is present in the " + fileName)

            if os.path.exists(path):
                os.remove(path)
            ftp.close()

    def anacryptFile(self, **kwargs):
        file = str(kwargs["fileName"])
        password = str(kwargs.get("password"))
        option = str(kwargs.get("option"))
        import shutil
        path = "C:\TFTPBOOT"
        filePath = os.path.join(os.path.dirname((__file__)), "anacrypt.exe")
        if os.path.exists(path):
            shutil.rmtree(path)
        os.mkdir(path)
        shutil.copy(filePath, path)
        os.chdir(path)
        with open(file, 'w+') as configFile:
            configFile.write("\n")
        if option == "mac":
            os.system("anacrypt " + file + " -p " + password + " -m " + file)
        else:
            os.system("anacrypt " + file + " -p " + password + " -i")

    def verifyAnacryptFile(self, **kwargs):
        file = str(kwargs.get('fileName'))
        value = kwargs.get('value')
        option = kwargs.get('option')
        path = "C:\TFTPBOOT"
        if value != "not":
            filename = str(file[:-4] + ".tuz")
            os.chdir(path)
            file_path = os.listdir(path)
            for i in file_path:
                if option != "mac":
                    if i == filename or i == "security.tuz":
                        console(i + " is present in the folder")
                    else:
                        continue
                else:
                    console("in mac loop")
                    if i == filename:
                        console(i + " is present in the folder")
                    else:
                        continue
        else:
            os.chdir(path)
            file_path = os.listdir(path)
            filename = str(file[:-4] + ".txt")
            for item in file_path:
                if item.endswith(".txt"):
                    raise Exception("Text file is present in the folder")
            console(filename + " is not present in the folder")

    def renameAnacryptFile(self, **kwargs):
        path = "C:\TFTPBOOT"
        file = str(kwargs.get('fileName'))
        value = str(kwargs.get('value'))
        os.chdir(path)
        os.system("rename " + file + " " + value)

    def baseConfig(self, **kwargs):

        from datetime import datetime
        console(kwargs)
        Test_name = str(kwargs.get('Test_name')).split(':')[0] + str('_') + str(
            datetime.now().strftime("%Y%m%d%H%M%S"))

        path_local = str(
            str(kwargs.get('SUITE_SOURCE')).split(str(kwargs.get('SUITE_SOURCE')).split('\\')[-1])[0]).replace('\\',
                                                                                                               '/')
        return Test_name, path_local

    # def testNameCreator(self, **kwargs):
    #     """
    #     Below method setup the configuration in tinydb required for
    #     sip message verification process
    #     :param kwargs:
    #     :type kwargs: dict
    #     :key Test_name: Name of testcase in execution
    #     :key SUITE_SOURCE: path of testcase file directory
    #     :returns:
    #     """
    #
    #     db.purge()
    #     self.testCaseName, self.path_local = self.baseConfig(**kwargs)
    #     pbx = str(kwargs.get('pbx'))
    #     if pbx == 'MxOne' :
    #         self.path_server = var_pbx.path_server_mxone
    #         self.ip_addr_server = var_pbx.ip_addr_server_mxone
    #         self.server_username = var_pbx.server_username_mxone
    #         self.server_pwd = var_pbx.server_pwd_mxone
    #         self.server_root_pwd = var_pbx.root_passwd_mxone
    #
    #     elif pbx == 'Asterisk' :
    #         self.path_server = var_pbx.path_server_Asterisk
    #         self.ip_addr_server = var_pbx.ip_addr_server_Asterisk
    #         self.server_username = var_pbx.server_username_Asterisk
    #         self.server_pwd = var_pbx.server_pwd_Asterisk
    #         self.server_root_pwd = var_pbx.server_pwd_Asterisk
    #
    #     self.file_pcap = '{}.pcap'.format(self.testCaseName)
    #     self.file_json = '{}.json'.format(self.testCaseName)
    #     self.file_txt = '{}.txt'.format(self.testCaseName)
    #     self.pkt_log_file = self.path_local + self.file_txt
    #     self.pcap_file = self.path_server + self.file_pcap
    #     self.op_file = self.path_server + self.file_json
    #     self.local_pcap_download_file = self.path_local + self.file_pcap
    #     self.local_json_download_file = self.path_local + self.file_json
    #     db.insert({'testCaseName': self.testCaseName,
    #                'path_local': self.path_local,
    #                'path_server': self.path_server,
    #                'ip_addr_server': self.ip_addr_server,
    #                'server_username': self.server_username,
    #                'server_pwd': self.server_pwd,
    #                'root_pwd': self.server_root_pwd,
    #                'file_pcap': self.file_pcap,
    #                'file_json': self.file_json,
    #                'file_txt': self.file_txt,
    #                'pkt_log_with_path': self.pkt_log_file,
    #                'pcap_file': self.pcap_file,
    #                'op_file': self.op_file,
    #                'local_pcap_download_file': self.local_pcap_download_file,
    #                'local_json_download_file': self.local_json_download_file
    #                })
    #     return

    # def wiresharkOperator(self, **kwargs):
    #     """
    #     Below method capturue the network packets of
    #     sip call operations save them as pcap file in
    #     test execution m/c
    #     :param kwargs: this is used pass operand to function
    #     to start or stop tcpdump on MXone server
    #     :type kwargs: dict
    #     :key operand: start, stop
    #     :returns:
    #     """
    #
    #     import threading
    #
    #     operand = kwargs['operand']
    #     phoneObject = kwargs['phoneObj']
    #     operation = kwargs['operation']
    #     ip_addr_src = self.phone_obj.phone_obj.phone.ipAddress
    #
    #     logger.info("Value recieved from test cases are %s " % operand + " and %s " % ip_addr_src)
    #
    #     if operand == 'start':
    #         logger.info(
    #             "Below step testNameCreator function called to setup the configuration in tinydb required for tls packet verification")
    #
    #         if operation == 'sippsTls':
    #             self.testNameCreator(**kwargs)
    #             pv.call_stack.clear()
    #             func_param_dict.clear()
    #             # 'echo "Mx0n3@!2#" | sudo -S tcpdump -s 0 port 5061 and \(host 10.112.123.198 and  host 10.112.110.111\) -w test.pcap'
    #             func_param_dict.update({
    #                 'cmd': """echo '{0}'| sudo -S tcpdump -s 0 port 5061 and \(host {1} and  host {2}\) -w {3} """.format(
    #                     db.all()[0]['root_pwd'], ip_addr_src, db.all()[0]['ip_addr_server'], db.all()[0]['pcap_file']),
    #                 'ip_addr_src': ip_addr_src,
    #                 'ip_address_server': db.all()[0]['ip_addr_server'],
    #                 'username': db.all()[0]['server_username'],
    #                 "password": db.all()[0]['server_pwd'],
    #                 'op_file': db.all()[0]['file_pcap'],
    #                 'op_file_json': db.all()[0]['file_json'],
    #                 'local_pcap_download_file': db.all()[0]['local_pcap_download_file'],
    #                 'local_json_download_file': db.all()[0]['local_json_download_file'],
    #                 'file': db.all()[0]['pcap_file'],
    #                 'packet_log_file': db.all()[0]['file_txt'],
    #                 'pkt_log_with_path': db.all()[0]['pkt_log_with_path'],
    #                 'path_local': db.all()[0]['path_local'],
    #                 'server_file': db.all()[0]['op_file']})
    #             console(func_param_dict)
    #             logger.info(
    #                 "Cleaning prevoius capture files from path :[{}]".format(func_param_dict.get('path_local')))
    #             logger.info("Cleaning prevoius capture files {0} , {1} and {2}".format(
    #                 func_param_dict.get('op_file'),
    #                 func_param_dict.get('op_file_json'),
    #                 func_param_dict.get('packet_log')
    #             ))
    #
    #         elif operation == 'sip':
    #             self.testNameCreator(**kwargs)
    #             pv.call_stack.clear()
    #             func_param_dict.clear()
    #             # 'echo "Mx0n3@!2#" | sudo -S tcpdump -s 0 port 5061 and \(host 10.112.123.198 and  host 10.112.110.111\) -w test.pcap'
    #             func_param_dict.update({
    #                 'cmd': """echo '{0}'| sudo -S tcpdump -s 0 port 5060 and \(host {1} and  host {2}\) -w {3} """.format(
    #                     db.all()[0]['root_pwd'], ip_addr_src, db.all()[0]['ip_addr_server'], db.all()[0]['pcap_file']),
    #                 'ip_addr_src': ip_addr_src,
    #                 'ip_address_server': db.all()[0]['ip_addr_server'],
    #                 'username': db.all()[0]['server_username'],
    #                 "password": db.all()[0]['server_pwd'],
    #                 'op_file': db.all()[0]['file_pcap'],
    #                 'op_file_json': db.all()[0]['file_json'],
    #                 'local_pcap_download_file': db.all()[0]['local_pcap_download_file'],
    #                 'local_json_download_file': db.all()[0]['local_json_download_file'],
    #                 'file': db.all()[0]['pcap_file'],
    #                 'packet_log_file': db.all()[0]['file_txt'],
    #                 'pkt_log_with_path': db.all()[0]['pkt_log_with_path'],
    #                 'path_local': db.all()[0]['path_local'],
    #                 'server_file': db.all()[0]['op_file'],
    #                 'protocol': operation
    #
    #             })
    #             console(func_param_dict)
    #             logger.info(
    #                 "Cleaning prevoius capture files from path :[{}]".format(func_param_dict.get('path_local')))
    #             logger.info("Cleaning prevoius capture files {0} , {1} and {2}".format(
    #                 func_param_dict.get('op_file'),
    #                 func_param_dict.get('op_file_json'),
    #                 func_param_dict.get('packet_log')
    #             ))
    #
    #
    #
    #         elif operation == 'httpsTls':
    #             self.coreServerConfigCreator(**kwargs)
    #             pv.call_stack.clear()
    #             func_param_dict.clear()
    #             # 'echo "Mx0n3@!2#" | sudo -S tcpdump -s 0 port 5061 and \(host 10.112.123.198 and  host 10.112.110.111\) -w test.pcap'
    #             func_param_dict.update({
    #                 'cmd': """echo '{0}'| sudo -S tcpdump -s 0 port 443 and \(host {1} and  host {2}\) -w {3} """.format(
    #                     cb.all()[0]['root_pwd'], ip_addr_src, cb.all()[0]['ip_addr_server'], cb.all()[0]['pcap_file']),
    #                 'ip_addr_src': ip_addr_src,
    #                 'ip_address_server': cb.all()[0]['ip_addr_server'],
    #                 'username': cb.all()[0]['server_username'],
    #                 "password": cb.all()[0]['server_pwd'],
    #                 'op_file': cb.all()[0]['file_pcap'],
    #                 'op_file_json': cb.all()[0]['file_json'],
    #                 'local_pcap_download_file': cb.all()[0]['local_pcap_download_file'],
    #                 'local_json_download_file': cb.all()[0]['local_json_download_file'],
    #                 'file': cb.all()[0]['pcap_file'],
    #                 'packet_log_file': cb.all()[0]['file_txt'],
    #                 'pkt_log_with_path': cb.all()[0]['pkt_log_with_path'],
    #                 'path_local': cb.all()[0]['path_local'],
    #                 'server_file': cb.all()[0]['op_file']})
    #             console(func_param_dict)
    #             logger.info(
    #                 "Cleaning prevoius capture files from path :[{}]".format(func_param_dict.get('path_local')))
    #             logger.info("Cleaning prevoius capture files {0} , {1} and {2} {3}".format(
    #                 func_param_dict.get('op_file'),
    #                 func_param_dict.get('op_file_json'),
    #                 func_param_dict.get('packet_log'),
    #                 func_param_dict.get('file')
    #             ))
    #
    #         else:
    #             logger.info("Operation parameter missing")
    #
    #         logger.info(
    #             "SSH to Server {0} to execute the command {1} ".format(func_param_dict.get("ip_address_server"),
    #                                                                    func_param_dict.get("cmd")))
    #
    #         t1 = threading.Thread(target=pv.ssh_cmd, kwargs=func_param_dict)
    #         t1.start()
    #         time.sleep(2)
    #
    #
    #     elif operand == 'stop':
    #         """Here we are stopping tcpdump on asterisk server"""
    #
    #         if operation == 'httpsTls':
    #             func_param_dict['cmd'] = "echo '{0}' | sudo -S killall tcpdump".format(cb.all()[0]['root_pwd'])
    #         else:
    #             func_param_dict['cmd'] = "echo '{0}' | sudo -S killall tcpdump".format(db.all()[0]['root_pwd'])
    #         logger.info(
    #             "SSH to Server {0} to stop TCPDUMP command ".format(func_param_dict.get("ip_address_server")))
    #         console(pv.ssh_cmd(**func_param_dict))
    #         logger.info("Downloading the packet capture file using SCP from server {0} to local {1} ".format(
    #             func_param_dict.get('ip_address_server'), func_param_dict.get('path_local')))
    #         console(pv.scp_get(**func_param_dict))
    #
    #         logger.info("Now Converting Downloaded packet capture file from {0} to {1} and {2}".format(
    #             func_param_dict.get('op_file'),
    #             func_param_dict.get('op_file_json'),
    #             func_param_dict.get('packet_log')
    #         ))
    #         logger.info("""Here we are converting pcap file into json and text""")
    #         pv.pcap_converter(**func_param_dict)

    def tlspacket_verifer(self, **kwargs):
        packt_key = kwargs['packt_key']
        pkt_dt = kwargs['pkt_dt']
        packt_value = kwargs['packt_value']
        verification_result = list()
        for values in pkt_dt:
            try:
                res_one = values.__contains__(packt_key)
            except:
                logger.warn("NOT DOING ANYTHING HERE!!")
            if res_one:
                print "Result One in tlspacket_verifer", res_one

                try:
                    print values
                    res_two = values.__contains__(packt_value)
                except Exception as error:
                    logger.warn("NOT DOING ANYTHING HERE!!")
                if res_two:
                    print "Result two in tlspacket_verifer", res_two
                    verification_result.append(0)

                else:
                    logger.info("No matching value found ")
                    verification_result.append(1)

        if len([x for x in verification_result if (x == 0)]) == 0:
            raise Exception(packt_key + " value ({0}) is not verified ".format(packt_value))
            result = [x for x in verification_result if (x == 0)]
            del result[:]
            del verification_result[:]

            return 1

        else:
            logger.info(packt_key + " value ({0}) is not verified ".format(packt_value))
            result = [x for x in verification_result if (x == 0)]
            del result[:]
            del verification_result[:]

            return 0

    # def ServerHelloVerifier(self, **kwargs):
    #     """
    #     :param kwargs:
    #     :returns:
    #     """
    #     if kwargs['operation'] == 'httpsTls':
    #         pkt_log_with_path = cb.all()[0]['pkt_log_with_path']
    #     else:
    #         pkt_log_with_path = db.all()[0]['pkt_log_with_path']
    #     kwargs.update({'protocol': 'tls', 'inputFile': pkt_log_with_path})
    #     vverification_result = []
    #     pd = pv.Base_Packet_Extracter(**kwargs)
    #     for k, v in pd.iteritems():
    #         for values in v:
    #             try:
    #                 res_one = str(values).split(":").__contains__('Handshake_Protocol')
    #             except Exception as error:
    #                 pass
    #             if res_one:
    #                 print "Result One", res_one
    #                 try:
    #                     res_two = str(values).split(":").__contains__('Server Hello')
    #                 except Exception as error:
    #                     pass
    #                 if res_two:
    #                     print "Result two", res_two
    #                     kwargs.update({'pkt_dt': pd[k]})
    #                     vverification_result.append(0)
    #                     return self.tlspacket_verifer(**kwargs)
    #
    #
    #                 else:
    #                     logger.info("No matching value found ")
    #                     vverification_result.append(1)
    #
    #     if len([x for x in vverification_result if (x == 0)]) == 0:
    #         raise Exception("Handshake_Protocol value Client Hello is not verified ")
    #         result = [x for x in vverification_result if (x == 0)]
    #         del result[:]
    #         del vverification_result[:]
    #
    #         return 1
    #
    #     else:
    #         logger.info("Handshake_Protocol value Client Hello is not verified")
    #         result = [x for x in vverification_result if (x == 0)]
    #         del result[:]
    #         del vverification_result[:]
    #
    #         return 0
    #
    #
    # def clientHelloVerifier(self, **kwargs):
    #     """
    #     :param kwargs:
    #     :returns:
    #     """
    #     if kwargs['operation'] == 'httpsTls':
    #         pkt_log_with_path = cb.all()[0]['pkt_log_with_path']
    #     else:
    #         pkt_log_with_path = db.all()[0]['pkt_log_with_path']
    #     kwargs.update({'protocol': 'tls', 'inputFile': pkt_log_with_path})
    #     vverification_result = []
    #     pd = pv.Base_Packet_Extracter(**kwargs)
    #     for k, v in pd.iteritems():
    #         for values in v:
    #             try:
    #                 res_one = str(values).split(":").__contains__('Handshake_Protocol')
    #             except Exception as error:
    #                 pass
    #             if res_one:
    #                 print "Result One", res_one
    #                 try:
    #                     res_two = str(values).split(":").__contains__('Client Hello')
    #                 except Exception as error:
    #                     pass
    #                 if res_two:
    #                     print "Result two", res_two
    #                     kwargs.update({'pkt_dt': pd[k]})
    #                     vverification_result.append(0)
    #                     return self.tlspacket_verifer(**kwargs)
    #
    #
    #                 else:
    #                     logger.info("No matching value found ")
    #                     vverification_result.append(1)
    #
    #     if len([x for x in vverification_result if (x == 0)]) == 0:
    #         raise Exception("Handshake_Protocol value Client Hello is not verified ")
    #         result = [x for x in vverification_result if (x == 0)]
    #         del result[:]
    #         del vverification_result[:]
    #
    #         return 1
    #
    #     else:
    #         logger.info("Handshake_Protocol value Client Hello is not verified")
    #         result = [x for x in vverification_result if (x == 0)]
    #         del result[:]
    #         del vverification_result[:]
    #
    #         return 0
    #
    #
    # def httpd_confupdater(self, **kwargs):
    #     '''
    #
    #     :param kwargs:
    #     :tls:1,11,12
    #     :returns:
    #     '''
    #     import os
    #     ipfn = 'tls.conf'
    #     opfn = 'httpd-ssl.conf'
    #     ip_file = var_pbx.httpipfiletlslocal + ipfn
    #     op_file = var_pbx.httpipfiletlslocal + opfn
    #     tls = kwargs['tls']
    #     print int(tls)
    #
    #     # cmd0="echo '{0}' | rm -f  {1}".format(var_pbx.httpdpass,var_pbx.serverhttpdfile)
    #     cmd1 = 'cp -f {0} {1}'.format(opfn, var_pbx.httpdserverconfpath)
    #     cmd2 = "echo '{0}' | sudo -S chmod 777 {1}".format(var_pbx.httpdpass, var_pbx.serverhttpdfile)
    #     cmd3 = "echo '{0}' | sudo -S /opt/lampp/lampp stop".format(var_pbx.httpdpass)
    #     cmd4 = "echo '{0}' | sudo -S /opt/lampp/lampp start".format(var_pbx.httpdpass)
    #
    #     kwargs.update(
    #         {'file': op_file, 'ip_address_server': var_pbx.httpdserverIPAddress, 'username': var_pbx.httpdUsername,
    #          'password': var_pbx.httpdpass, 'cmd': cmd1})
    #
    #     if tls:
    #         if int(tls) == 1:
    #             paramOne = 'SSLProtocol TLSv1'
    #             paramTwo = 'SSLProxyProtocol TLSv1'
    #             try:
    #                 try:
    #                     os.remove(op_file)
    #                 except OSError as e:
    #                     logger.error("Error: %s : %s" % (op_file, e.strerror))
    #                     pass
    #
    #                 with open(ip_file, 'r') as ip, open(op_file, 'w') as op:
    #                     for st in ip.readlines():
    #                         if st.__contains__('hclak'):
    #                             op.write('{0}\n{1}\n'.format(paramOne, paramTwo))
    #                         else:
    #                             op.write(st)
    #                 pv.scp_put(**kwargs)
    #                 kwargs.update({'cmd': cmd1})
    #                 pv.ssh_cmd(**kwargs)
    #                 kwargs.update({'cmd': cmd2})
    #                 pv.ssh_cmd(**kwargs)
    #                 kwargs.update({'cmd': cmd3})
    #                 pv.ssh_cmd(**kwargs)
    #                 kwargs.update({'cmd': cmd4})
    #                 return pv.ssh_cmd(**kwargs)
    #
    #             except Exception as error:
    #                 print "Error", error
    #                 logger.error("Error", error)
    #                 raise Exception("Error", error)
    #                 pass
    #         elif int(tls) == 11:
    #             paramOne = 'SSLProtocol TLSv1.1'
    #             paramTwo = 'SSLProxyProtocol TLSv1.1'
    #             try:
    #                 os.remove(op_file)
    #             except OSError as e:
    #                 logger.error("Error: %s : %s" % (op_file, e.strerror))
    #                 pass
    #             try:
    #                 with open(ip_file, 'r') as ip, open(op_file, 'w') as op:
    #                     for st in ip.readlines():
    #                         if st.__contains__('hclak'):
    #                             op.write('{0}\n{1}\n'.format(paramOne, paramTwo))
    #                         else:
    #                             op.write(st)
    #                 pv.scp_put(**kwargs)
    #                 kwargs.update({'cmd': cmd1})
    #                 pv.ssh_cmd(**kwargs)
    #                 kwargs.update({'cmd': cmd2})
    #                 pv.ssh_cmd(**kwargs)
    #                 kwargs.update({'cmd': cmd3})
    #                 pv.ssh_cmd(**kwargs)
    #                 kwargs.update({'cmd': cmd4})
    #                 return pv.ssh_cmd(**kwargs)
    #
    #             except Exception as error:
    #                 print "Error", error
    #                 logger.error("Error", error)
    #                 raise Exception("Error", error)
    #                 pass
    #
    #         elif int(tls) == 12:
    #             print 'Ak'
    #             paramOne = 'SSLProtocol TLSv1.2'
    #             paramTwo = 'SSLProxyProtocol TLSv1.2'
    #             try:
    #                 os.remove(op_file)
    #             except OSError as e:
    #                 logger.error("Error: %s : %s" % (op_file, e.strerror))
    #                 pass
    #             try:
    #                 with open(ip_file, 'r') as ip, open(op_file, 'w') as op:
    #                     for st in ip.readlines():
    #                         if st.__contains__('hclak'):
    #                             op.write('{0}\n{1}\n'.format(paramOne, paramTwo))
    #                         else:
    #                             op.write(st)
    #                 pv.scp_put(**kwargs)
    #                 kwargs.update({'cmd': cmd1})
    #                 pv.ssh_cmd(**kwargs)
    #                 kwargs.update({'cmd': cmd2})
    #                 pv.ssh_cmd(**kwargs)
    #                 kwargs.update({'cmd': cmd3})
    #                 pv.ssh_cmd(**kwargs)
    #                 kwargs.update({'cmd': cmd4})
    #                 console(pv.ssh_cmd(**kwargs))
    #                 return
    #             except Exception as error:
    #                 print "Error", error
    #                 logger.error("Error", error)
    #                 raise Exception("Error", error)
    #                 pass
    #
    #     else:
    #         raise Exception("Please check the arguments passed %s" % kwargs)
    #         logger.error("Please check the arguments passed %s" % kwargs)
    #
    #
    # def httpXmlPublisher(self, **kwargs):
    #     xmlName = kwargs['xmlName']
    #     xmlfn = '{0}.xml'.format(xmlName)
    #     ip_file = var_pbx.httpdpulishxmlLocal + xmlfn
    #     file_uploadpath = var_pbx.core_server_home
    #     opfileuploadpath = file_uploadpath + xmlfn
    #     filepublishpath = var_pbx.httpdpulishxmlserver + xmlfn
    #
    #     cmd1 = "echo '{0}' | sudo -S chmod 777 {1}".format(var_pbx.httpdpass, opfileuploadpath)
    #     cmd2 = "echo '{0}' | sudo -S rm -f {1}/*.xml".format(var_pbx.httpdpass, var_pbx.httpdpulishxmlserver)
    #     cmd3 = "echo '{0}' | sudo -S cp -f {1} {2}".format(var_pbx.httpdpass, opfileuploadpath, filepublishpath)
    #     cmd4 = "echo '{0}' | sudo -S /opt/lampp/lampp stop".format(var_pbx.httpdpass)
    #     cmd5 = "echo '{0}' | sudo -S /opt/lampp/lampp start".format(var_pbx.httpdpass)
    #
    #     kwargs.update(
    #         {'file': ip_file, 'ip_address_server': var_pbx.httpdserverIPAddress, 'username': var_pbx.httpdUsername,
    #          'password': var_pbx.httpdpass, 'cmd': None})
    #
    #     try:
    #
    #         pv.scp_put(**kwargs)
    #         kwargs.update({'cmd': cmd1})
    #         pv.ssh_cmd(**kwargs)
    #         kwargs.update({'cmd': cmd2})
    #         print(pv.ssh_cmd(**kwargs))
    #         kwargs.update({'cmd': cmd3})
    #         print(pv.ssh_cmd(**kwargs))
    #         kwargs.update({'cmd': cmd4})
    #         print(pv.ssh_cmd(**kwargs))
    #         kwargs.update({'cmd': cmd5})
    #         print(pv.ssh_cmd(**kwargs))
    #
    #     except Exception as error:
    #         print "Error", error
    #         logger.error("Error", error)
    #         raise Exception("Error", error)
    #         pass
    #
    # def rtpPktVerifier(**kwargs):
    #     """
    #     Below method verify response packet header name exsistence
    #     in packet
    #    :param kwargs: verification parameters
    #    :type kwargs: dict
    #    :key packt_name: sip method name
    #    :key packt_key: sip-header
    #    :returns:
    #     """
    #     if (len(kwargs) > 1):
    #         packt_name = kwargs['packt_name']
    #         packt_key = kwargs['packt_key']
    #         packt_value_expected = kwargs['packt_value']
    #         rtpevent_verification_result = []
    #     else:
    #         raise Exception('Please provide sufficent parmeters to verify')
    #
    #     logger.info("Coreparmeter info : {0} ".format(func_param_dict))
    #     logger.info("Now Reading the json converting for verification ")
    #     rtpeventpkts = pv.Base_Packet_Extracter(**func_param_dict)
    #
    #     for rtpeventpkt in rtpeventpkts:
    #         if bool(rtpeventpkt) != False:
    #             pv.rtp_event_verifier(packt_key, packt_value_expected, logger, **rtpeventpkt)
    #             if pv.value == packt_value_expected:
    #                 logger.info("value found :{}".format(pv.value))
    #                 rtpevent_verification_result.append(0)
    #             else:
    #                 logger.info("No matching value found ")
    #                 rtpevent_verification_result.append(1)
    #
    #         else:
    #
    #             logger.info("rtpeventpkt seems empty {}".format(rtpeventpkt))
    #
    #
    #     else:
    #         logger.info("rtpeventpkt seems empty {}".format(rtpeventpkt))
    #         raise Exception(packt_name + ' RTPEVENT not found in packet')
    #
    #     if len([x for x in rtpevent_verification_result if (x == 0)]) == 0:
    #         raise Exception(
    #             packt_key + " value ({0}) is not verified in {1} of rtpevent".format(packt_value_expected, packt_name))
    #         result = [x for x in rtpevent_verification_result if (x == 0)]
    #         del result[:]
    #         del rtpevent_verification_result[:]
    #
    #         return
    #
    #     else:
    #         logger.info(
    #             packt_key + " value ({0}) is verified in {1} of rtpevent ".format(packt_value_expected, packt_name))
    #         result = [x for x in rtpevent_verification_result if (x == 0)]
    #         del result[:]
    #         del rtpevent_verification_result[:]
    #         return 0

    def hostIpAddressGetter(self, **kwargs):
        """
        Below method is used to get the IP Address of different machines.

        :param:
            :kwargs:
                :proto: Machine to get IP of

        :created by: Abhishek Khanchi
        :creation date:
        :last update by: Sharma
        :last update date: 15/06/2020
        """
        try:
            import socket
            print kwargs
            proto = kwargs['proto']
            print proto
            if proto == u'local':
                ip_address = socket.gethostbyname_ex(socket.gethostname())
                if isinstance(ip_address[-1], list):
                    return ip_address[-1][-1]
                return ip_address[-1]
            elif proto == u'tftp':
                ip_address = var_pbx.tftp_server
                # print ip_address
                return ip_address

            elif proto == u'ftp':
                ip_address = var_pbx.ftp_server
                return ip_address
            elif proto == u'http':
                ip_address = var_pbx.httpdserverIPAddress
                return ip_address
        except:
            raise Exception("something went wrong")

    # def urlCreator(self,**kwargs):
    #     print kwargs
    #     proto = kwargs['proto']
    #     ipAddress = self.hostIpAddressGetter(**kwargs)
    #     # print ipAddress
    #     if proto == u'tftp':
    #         filename = kwargs['filename']
    #         # print kwargs
    #         url = 'tftp://{0}/{1}'.format(ipAddress, filename)
    #         # print url
    #         return url
    #     if proto == u'ftp':
    #         filename = kwargs['filename']
    #         # print kwargs
    #         username = var_pbx.ftp_server_username
    #         passwd = var_pbx.ftp_server_passwd
    #         url = 'ftp://{0}:{1}@{2}/{3}'.format(username, passwd, ipAddress, filename)
    #         # print url
    #         return url
    #     if proto == u'http':
    #         filename = kwargs['filename']
    #         # print kwargs
    #
    #         url = 'http://{0}/{1}'.format(ipAddress, filename)
    #         # print url
    #         return url
    #     if proto ==u'httptls':
    #         filename = kwargs['filename']
    #         url = 'tftp://{0}/{1}'.format(ipAddress, filename)
    #         return url
    #
    #
    #     else:
    #         raise Exception("something went wrong inside urlCreator")
    #
    #
    # def cfgGenrator(self,**kwargs):
    #     try:
    #         proto = kwargs['proto']
    #         op_file = kwargs['op_file']
    #         ip_file = kwargs['ip_file']
    #         parameters = kwargs['parameters']
    #         # print kwargs
    #         try:
    #             os.remove(op_file)
    #         except OSError as e:
    #              logger.error("Error: %s : %s" % (op_file, e.strerror))
    #              pass
    #
    #         with open(ip_file, 'r') as ip, open(op_file, 'w') as op:
    #             for st in ip.readlines():
    #                 if st.__contains__('hclak'):
    #                     if parameters.has_key("DirectoryFile"):
    #                         parameters.pop("DirectoryFile")
    #                         kwargs.update({'filename': var_pbx.csvFile})
    #                         url = self.urlCreator(**kwargs)
    #                         param = "directory 1: " + url
    #                         print param
    #                         op.write('{0}\n'.format(param))
    #                     if parameters.has_key("custom_ringtone"):
    #                         parameters.pop("custom_ringtone")
    #                         kwargs.update({'filename': var_pbx.wavFile})
    #                         url = self.urlCreator(**kwargs)
    #                         param = "custom ringtone 1: " + url
    #                         print param
    #                         op.write('{0}\n'.format(param))
    #                     else:
    #                         for values in dict(parameters).values():
    #                             print values + '\n'
    #                             op.write(values + '\n')
    #
    #                 else:
    #                     op.write(st)
    #
    #     except Exception as error:
    #         print "Error", error
    #         logger.error("Error", error)
    #         raise Exception("Error", error)
    #         pass
    #
    # def phoneConfigCreator(self,**kwargs):
    #         """
    #         :param self:
    #         :param kwargs:
    #         :returns:
    #         """
    #         print kwargs
    #         proto = kwargs['servertype']
    #         configFilename = kwargs['configfilename']
    #         parameters = dict(kwargs['parameters'])
    #         ipfn = 'comm.cfg'
    #         opfn = configFilename
    #         ip_file = var_pbx.phoneConfigLocal + ipfn
    #         op_file = var_pbx.phoneConfigLocal + opfn
    #
    #         if proto == u'ftp':
    #             serverPath = var_pbx.ftp_server_root
    #             serverOpFile = var_pbx.ftp_server_root + opfn
    #             cmd0 = 'rm -f {0}'.format(serverOpFile)
    #             cmd1 = 'cp -f {0} {1}'.format(opfn, serverPath)
    #             cmd2 = "echo '{0}' | sudo -S chmod 777 {1}".format(var_pbx.httpdpass, serverOpFile)
    #             cgargs = {'proto': proto, 'ip_file': ip_file, 'op_file': op_file, 'parameters': parameters}
    #             self.cfgGenrator(**cgargs)
    #             kwargs.update(
    #                 {'file': op_file, 'ip_address_server': var_pbx.coreserverIPAddress,
    #                  'username': var_pbx.httpdUsername,
    #                  'password': var_pbx.httpdpass, 'cmd': cmd0})
    #             pv.ssh_cmd(**kwargs)
    #             pv.scp_put(**kwargs)
    #             kwargs.update({'cmd': cmd1})
    #             pv.ssh_cmd(**kwargs)
    #             kwargs.update({'cmd': cmd2})
    #             pv.ssh_cmd(**kwargs)
    #         elif proto == u'tftp':
    #             serverPath = var_pbx.tftp_path_root
    #             serverOpFile = var_pbx.tftp_path_root + opfn
    #             cgargs = {'proto': proto, 'ip_file': ip_file, 'op_file': op_file, 'parameters': parameters}
    #             self.cfgGenrator(**cgargs)
    #             cmd0 = 'rm -f {0}'.format(serverOpFile)
    #             cmd1 = 'cp -f {0} {1}'.format(opfn, serverPath)
    #             cmd2 = "echo '{0}' | sudo -S chmod 777 {1}".format(var_pbx.httpdpass, serverOpFile)
    #             kwargs.update(
    #                 {'file': op_file, 'ip_address_server': var_pbx.coreserverIPAddress,
    #                  'username': var_pbx.httpdUsername,
    #                  'password': var_pbx.httpdpass, 'cmd': cmd0})
    #             pv.ssh_cmd(**kwargs)
    #             pv.scp_put(**kwargs)
    #             kwargs.update({'cmd': cmd1})
    #             pv.ssh_cmd(**kwargs)
    #             kwargs.update({'cmd': cmd2})
    #             pv.ssh_cmd(**kwargs)
    #             return
    #         elif proto == u'http':
    #             serverPath = var_pbx.httpdpulishxmlserver
    #             serverOpFile = var_pbx.httpdpulishxmlserver + opfn
    #             cmd0 = 'rm -f {0}'.format(serverOpFile)
    #             cmd1 = 'cp -f {0} {1}'.format(opfn, serverPath)
    #             cmd2 = "echo '{0}' | sudo -S chmod 777 {1}".format(var_pbx.httpdpass, serverOpFile)
    #             cmd3 = "echo '{0}' | sudo -S /opt/lampp/lampp stop".format(var_pbx.httpdpass)
    #             cmd4 = "echo '{0}' | sudo -S /opt/lampp/lampp start".format(var_pbx.httpdpass)
    #             cgargs = {'proto': proto, 'ip_file': ip_file, 'op_file': op_file, 'parameters': parameters}
    #             self.cfgGenrator(**cgargs)
    #             kwargs.update(
    #                 {'file': op_file, 'ip_address_server': var_pbx.coreserverIPAddress,
    #                  'username': var_pbx.httpdUsername,
    #                  'password': var_pbx.httpdpass, 'cmd': cmd0})
    #             pv.ssh_cmd(**kwargs)
    #             pv.scp_put(**kwargs)
    #             kwargs.update({'cmd': cmd1})
    #             pv.ssh_cmd(**kwargs)
    #             kwargs.update({'cmd': cmd2})
    #             pv.ssh_cmd(**kwargs)
    #             kwargs.update({'cmd': cmd3})
    #             pv.ssh_cmd(**kwargs)
    #             kwargs.update({'cmd': cmd4})
    #             pv.ssh_cmd(**kwargs)
    #             return
    #         elif proto == u'httptls':
    #             serverPath = var_pbx.httpdpulishxmlserver
    #             serverOpFile = var_pbx.httpdpulishxmlserver + opfn
    #             cmd0 = 'rm -f {0}'.format(serverOpFile)
    #             cmd1 = 'cp -f {0} {1}'.format(opfn, serverPath)
    #             cmd2 = "echo '{0}' | sudo -S chmod 777 {1}".format(var_pbx.httpdpass, serverOpFile)
    #             cmd3 = "echo '{0}' | sudo -S /opt/lampp/lampp stop".format(var_pbx.httpdpass)
    #             cmd4 = "echo '{0}' | sudo -S /opt/lampp/lampp start".format(var_pbx.httpdpass)
    #             cgargs = {'proto': proto, 'ip_file': ip_file, 'op_file': op_file, 'parameters': parameters}
    #             self.cfgGenrator(**cgargs)
    #             kwargs.update(
    #                 {'file': op_file, 'ip_address_server': var_pbx.coreserverIPAddress,
    #                  'username': var_pbx.httpdUsername,
    #                  'password': var_pbx.httpdpass, 'cmd': cmd0})
    #             pv.ssh_cmd(**kwargs)
    #             pv.scp_put(**kwargs)
    #             kwargs.update({'cmd': cmd1})
    #             pv.ssh_cmd(**kwargs)
    #             kwargs.update({'cmd': cmd2})
    #             pv.ssh_cmd(**kwargs)
    #             kwargs.update({'cmd': cmd3})
    #             pv.ssh_cmd(**kwargs)
    #             kwargs.update({'cmd': cmd4})
    #             pv.ssh_cmd(**kwargs)
    #             return
    #
    # def reQPacketVerifier(self, **kwargs):
    #     """
    #     Below method request packet value verification
    #     :param kwargs: verification parameters
    #     :type kwargs: dict
    #     :key packt_name: sip method name
    #     :key packt_key: sip-header
    #     :key packt_value: packt_value_expected
    #     :returns:
    #     """
    #
    #     if (len(kwargs) > 1):
    #
    #         packt_name = kwargs['packt_name']
    #         packt_key = kwargs['packt_key']
    #         packt_value_expected = kwargs['packt_value']
    #         sip_ip_addr_src = self.phone_obj.phone_obj.phone.ipAddress
    #         # console("sip_ip_addr_src: "+ sip_ip_addr_src)
    #         extensionNumber = self.phone_obj.phone_obj.phone.extensionNumber
    #         sip_verification_result = []
    #     else:
    #         raise Exception('Please provide sufficent parmeters to verify')
    #
    #     func_param_dict.update({
    #         'sip_ip_addr_src': sip_ip_addr_src,
    #         'source_dn': extensionNumber
    #     })
    #
    #     logger.info("capture files local path :{}".format(func_param_dict.get('path_local')))
    #     logger.info("Reqeust info : {0} ".format(func_param_dict))
    #     logger.info("Now Reading the json converting for verification using info  ")
    #     # pv.Base_Packet_Extracter(**func_param_dict)
    #     # logger.info("Now iterating for Request verification")
    #
    #     if packt_name=='REGISTER':
    #         del pv.registerPktList[:]
    #         pv.Base_Packet_Extracter(**func_param_dict)
    #         console('REGISTER CONTENT')
    #         for pkt in pv.registerPktList:
    #             sipMethod = pkt['PACKET']["sip.Request-Line_tree"]["sip.Method"]
    #             if sipMethod == 'REGISTER':
    #                 pv.packet_parser(packt_key, **pkt)
    #                 if packt_value_expected=='unregister':
    #                     if str(pv.value).startswith("expires"):
    #                         if int(str(pv.value).split("=")[-1])>0:
    #                             logger.info(packt_name + "   sip method is verified in packet ")
    #                             pass
    #                 else:
    #                     if pv.value == packt_value_expected:
    #                         logger.info(packt_name + "   sip method is verified in packet ")
    #                         pass
    #         else:
    #             raise Exception(packt_name + '  sip method not found in packet')
    #
    #     elif packt_name=='SUBSCRIBE':
    #         del pv.subscribePktList[:]
    #         pv.Base_Packet_Extracter(**func_param_dict)
    #         console('SUBSCRIBE CONTENT')
    #         for pkt in pv.subscribePktList:
    #             sipMethod = pkt['PACKET']["sip.Request-Line_tree"]["sip.Method"]
    #             if sipMethod == 'SUBSCRIBE':
    #                 pv.packet_parser(packt_key, **pkt)
    #                 if packt_value_expected == 'unsubscribe':
    #                     if int(pv.value)>0:
    #                        logger.info(packt_name + "   sip method is verified in packet ")
    #                        pass
    #                 else:
    #                     if pv.value == packt_value_expected:
    #                         logger.info(packt_name + "   sip method is verified in packet ")
    #                         pass
    #         else:
    #             raise Exception(packt_name + '  sip method not found in packet')
    #     elif packt_name == 'INVITE':
    #         pv.Base_Packet_Extracter(**func_param_dict)
    #         for k, v in pv.call_stack.items():
    #
    #             if v[packt_name]['PACKET'] != None:
    #                 pv.packet_parser(packt_8key, **v[packt_name]['PACKET'])
    #
    #                 if pv.value == packt_value_expected:
    #
    #                     sip_verification_result.append(0)
    #
    #                 else:
    #                     sip_verification_result.append(1)
    #             else:
    #                 raise Exception("<b>" + packt_name + "</b>sip method not found in packet", html=True)
    #             pv.value = None
    #
    #     if len([x for x in sip_verification_result if (x == 0)]) == 0:
    #
    #         raise Exception(packt_value_expected + " is not found in sip request method " + packt_name)
    #         result = [x for x in sip_verification_result if (x == 0)]
    #         del result[:]
    #         del sip_verification_result[:]
    #         pv.call_stack.clear()
    #         del pv.call_id_ls[:]
    #
    #         return 1
    #
    #
    #     else:
    #         logger.info(packt_value_expected + " is verified in sip request method " + packt_name)
    #         result = [x for x in sip_verification_result if (x == 0)]
    #         del result[:]
    #         del sip_verification_result[:]
    #         pv.call_stack.clear()
    #         del pv.call_id_ls[:]
    #
    #         return 0
    #
    # def resPPacketVerifier(self, **kwargs):
    #     """
    #         Below method response packet value verification
    #         :param kwargs: verification parameters
    #         :type kwargs: dict
    #         :key packt_name: sip method name
    #         :key packt_key: sip-header
    #         :key packt_value: packt_value_expected of sip-header
    #         :returns:
    #     """
    #
    #     if (len(kwargs) > 1):
    #         packt_name = kwargs['packt_name']
    #         packt_key = kwargs['packt_key']
    #         packt_value_expected = kwargs['packt_value']
    #         sip_ip_addr_src = self.phone_obj.phone_obj.phone.ipAddress
    #         # console("sip_ip_addr_src: "+ sip_ip_addr_src)
    #         extensionNumber = self.phone_obj.phone_obj.phone.extensionNumber
    #         sip_verification_result = []
    #     else:
    #         raise Exception('Please provide sufficent parmeters to verify')
    #
    #     func_param_dict.update({
    #         'sip_ip_addr_src': sip_ip_addr_src,
    #         'source_dn': extensionNumber
    #     })
    #     logger.info("Response info : {0} ".format(func_param_dict))
    #     logger.info("Now Reading the json converting for verification ")
    #     pv.Base_Packet_Extracter(**func_param_dict)
    #
    #     for k, v in pv.call_stack.items():
    #         logger.info("Now iterating for response verification")
    #         if v[packt_name]['PACKET'] != None:
    #             for i in v[packt_name]['RESPONSE']:
    #                 pv.packet_parser(packt_key, **i)
    #                 if pv.value == packt_value_expected:
    #                     sip_verification_result.append(0)
    #                 else:
    #                     sip_verification_result.append(1)
    #                 pv.value = None
    #
    #         else:
    #             raise Exception(packt_name + '  sip method not found in packet')
    #     pv.value = None
    #
    #     if len([x for x in sip_verification_result if (x == 0)]) == 0:
    #         raise Exception(packt_value_expected + " is not found in sip response method " + packt_name)
    #         result = [x for x in sip_verification_result if (x == 0)]
    #         del result[:]
    #         del sip_verification_result[:]
    #         sip.call_stack.clear()
    #         del pv.call_id_ls[:]
    #         return 1
    #     else:
    #         logger.info(packt_value_expected + " is verified in sip response method " + packt_name)
    #         result = [x for x in sip_verification_result if (x == 0)]
    #         del result[:]
    #         del sip_verification_result[:]
    #         del pv.call_id_ls[:]
    #         pv.call_stack.clear()
    #         return 0
    #
    # def sipMethodNameVerifier(self, **kwargs):
    #     """
    #             Below method verify sip packet exsistence
    #             :param kwargs: verification parameters
    #             :type kwargs: dict
    #             :key packt_name: sip method name
    #             :returns:
    #     """
    #
    #     if (len(kwargs) > 0):
    #
    #         packt_name = kwargs['packt_name']
    #
    #         sip_ip_addr_src = self.phone_obj.phone_obj.phone.ipAddress
    #         # console("sip_ip_addr_src: " + sip_ip_addr_src)
    #         extensionNumber = self.phone_obj.phone_obj.phone.extensionNumber
    #
    #     else:
    #         raise Exception('Please provide sufficent parmeters to verify')
    #
    #     func_param_dict.update({
    #         'sip_ip_addr_src': sip_ip_addr_src,
    #         'source_dn': extensionNumber
    #     })
    #
    #     logger.info("capture files local path :{}".format(func_param_dict.get('path_local')))
    #     logger.info("Reqeust info : {0} ".format(func_param_dict))
    #     logger.info("Now Reading the json converting for verification using info  ")
    #
    #     logger.info("Now iterating for Request verification")
    #
    #     if packt_name=='REGISTER':
    #         del pv.registerPktList[:]
    #         pv.Base_Packet_Extracter(**func_param_dict)
    #         console('REGISTER CONTENT')
    #         console(pv.registerPktList)
    #         if len(pv.registerPktList)>0:
    #             logger.info(packt_name + "   sip method is verified in packet ")
    #             pass
    #         else:
    #             raise Exception(packt_name + '  sip method not found in packet')
    #
    #     elif packt_name=='SUBSCRIBE':
    #         console('Inside subscribe')
    #         console('SUBSCRIBE CONTENT')
    #         del pv.subscribePktList[:]
    #         pv.Base_Packet_Extracter(**func_param_dict)
    #         console(pv.subscribePktList)
    #         if len(pv.subscribePktList)>0:
    #             logger.info(packt_name + "   sip method is verified in packet ")
    #             pass
    #         else:
    #             raise Exception(packt_name + '  sip method not found in packet')
    #     elif packt_name == 'INVITE':
    #         pv.Base_Packet_Extracter(**func_param_dict)
    #         for k, v in pv.call_stack.items():
    #             if v[packt_name]['PACKET'] == None:
    #                 raise Exception(packt_name + '  sip method not found in packet')
    #             else:
    #                 logger.info(packt_name + "   sip method is verified in packet ")
    #     else:
    #          raise Exception(packt_name + '  sip method not found in packet')
    #
    # def reQheaderNameVerifier(self, **kwargs):
    #     """
    #             Below method verify request packet header name exsistence
    #             in packet
    #             :param kwargs: verification parameters
    #             :type kwargs: dict
    #             :key packt_name: sip method name
    #             :key packt_key: sip-header
    #             :returns:
    #     """
    #
    #     if (len(kwargs) > 1):
    #
    #         packt_name = kwargs['packt_name']
    #         packt_key = kwargs['packt_key']
    #         sip_ip_addr_src = self.phone_obj.phone_obj.phone.ipAddress
    #         # console("sip_ip_addr_src: " + sip_ip_addr_src)
    #         extensionNumber = self.phone_obj.phone_obj.phone.extensionNumber
    #         sip_verification_result = []
    #     else:
    #         raise Exception('Please provide sufficent parmeters to verify')
    #
    #     func_param_dict.update({
    #         'sip_ip_addr_src': sip_ip_addr_src,
    #         'source_dn': extensionNumber
    #     })
    #
    #     logger.info("capture files local path :{}".format(func_param_dict.get('path_local')))
    #     logger.info("Reqeust info : {0} ".format(func_param_dict))
    #     logger.info("Now Reading the json converting for verification using info  ")
    #     pv.Base_Packet_Extracter(**func_param_dict)
    #     logger.info("Now iterating for Request verification")
    #     pv.value = None
    #     for k, v in pv.call_stack.items():
    #         if v[packt_name]['PACKET'] != None:
    #             pv.packet_parser(packt_key, **v[packt_name]['PACKET'])
    #
    #             if pv.value:
    #
    #                 sip_verification_result.append(0)
    #
    #             else:
    #                 sip_verification_result.append(1)
    #
    #         else:
    #             raise Exception(packt_name + '  sip method not found in packet')
    #     pv.value = None
    #
    #     if len([x for x in sip_verification_result if (x == 0)]) == 0:
    #
    #         raise Exception(packt_key + "  not found in sip request header " + packt_name)
    #         result = [x for x in sip_verification_result if (x == 0)]
    #         del result[:]
    #         del sip_verification_result[:]
    #         pv.call_stack.clear()
    #         del pv.call_id_ls[:]
    #         return 1
    #
    #
    #     else:
    #         logger.info(packt_key + "  is verified in sip request header " + packt_name)
    #         result = [x for x in sip_verification_result if (x == 0)]
    #         del result[:]
    #         del sip_verification_result[:]
    #         pv.call_stack.clear()
    #         del pv.call_id_ls[:]
    #
    #         return 0
    #
    # def resPheaderNameVerifier(self, **kwargs):
    #     """
    #             Below method verify response packet header name exsistence
    #             in packet
    #             :param kwargs: verification parameters
    #             :type kwargs: dict
    #             :key packt_name: sip method name
    #             :key packt_key: sip-header
    #             :returns:
    #     """
    #
    #     if (len(kwargs) > 1):
    #         packt_name = kwargs['packt_name']
    #         packt_key = kwargs['packt_key']
    #
    #         sip_ip_addr_src = self.phone_obj.phone_obj.phone.ipAddress
    #         console("sip_ip_addr_src: " + sip_ip_addr_src)
    #         extensionNumber = self.phone_obj.phone_obj.phone.extensionNumber
    #         sip_verification_result = []
    #     else:
    #         raise Exception('Please provide sufficent parmeters to verify')
    #
    #     func_param_dict.update({
    #         'sip_ip_addr_src': sip_ip_addr_src,
    #         'source_dn': extensionNumber
    #     })
    #     logger.info("Response info : {0} ".format(func_param_dict))
    #     logger.info("Now Reading the json converting for verification ")
    #     pv.Base_Packet_Extracter(**func_param_dict)
    #     pv.value = None
    #     for k, v in pv.call_stack.items():
    #         logger.info("Now iterating for response verification")
    #         if v[packt_name]['PACKET'] != None:
    #
    #             for i in v[packt_name]['RESPONSE']:
    #                 pv.packet_parser(packt_key, **i)
    #                 if pv.value:
    #                     sip_verification_result.append(0)
    #                 else:
    #                     sip_verification_result.append(1)
    #             pv.value = None
    #
    #         else:
    #             raise Exception(packt_name + ' sip method not found in packet')
    #
    #     pv.value = None
    #
    #     if len([x for x in sip_verification_result if (x == 0)]) == 0:
    #
    #         raise Exception(packt_key + "  is not verified in sip response header " + packt_name)
    #         result = [x for x in sip_verification_result if (x == 0)]
    #         del result[:]
    #         del sip_verification_result[:]
    #         pv.call_stack.clear()
    #         del pv.call_id_ls[:]
    #         return 1
    #
    #     else:
    #
    #         logger.info(packt_key + " is verified in sip response header " + packt_name)
    #         result = [x for x in sip_verification_result if (x == 0)]
    #         del result[:]
    #         del sip_verification_result[:]
    #         del pv.call_id_ls[:]
    #         pv.call_stack.clear()

    #         return 0
    #
    # def sdp_media_attr_verfier_caller(self, **kwargs):
    #     """
    #     :param kwargs:
    #     :returns:
    #     """
    #
    #     if (len(kwargs) > 1):
    #         packt_name = kwargs['packt_name']
    #         packt_key = kwargs['packt_key']
    #         packt_value_expected = kwargs['packt_value']
    #
    #         sip_ip_addr_src = self.phone_obj.phone_obj.phone.ipAddress
    #         console("sip_ip_addr_src: " + sip_ip_addr_src)
    #         extensionNumber = self.phone_obj.phone_obj.phone.extensionNumber
    #         sip_verification_result = []
    #
    #     else:
    #         raise Exception('Please provide sufficent parmeters to verify')
    #
    #     func_param_dict.update({
    #         'sip_ip_addr_src': sip_ip_addr_src,
    #         'source_dn': extensionNumber
    #     })
    #     logger.info("Response info : {0} ".format(func_param_dict))
    #     logger.info("Now Reading the json converting for verification ")
    #
    #     pv.Base_Packet_Extracter(**func_param_dict)
    #     pv.value = None
    #     for k, v in pv.call_stack.items():
    #         if v[packt_name]['PACKET'] != None:
    #             sdp = v[packt_name]['PACKET']  # [u'sip.msg_body'][u'sdp']
    #
    #             pv.sdp_mediaAttr_verifier(packt_key, packt_value_expected, logger, **sdp)
    #
    #             if pv.value == packt_value_expected:
    #                 logger.info("value found :{}".format(pv.value))
    #                 sip_verification_result.append(0)
    #
    #
    #             else:
    #                 logger.info("No matching value found ")
    #                 sip_verification_result.append(1)
    #
    #
    #
    #         else:
    #             raise Exception(packt_name + ' sip method not found in packet')
    #
    #     if len([x for x in sip_verification_result if (x == 0)]) == 0:
    #
    #         raise Exception(
    #             packt_key + " value ({0}) is not verified in {1} of sdp".format(packt_value_expected, packt_name))
    #         result = [x for x in sip_verification_result if (x == 0)]
    #         del result[:]
    #         del sip_verification_result[:]
    #         sip.call_stack.clear()
    #         del pv.call_id_ls[:]
    #         return 1
    #
    #     else:
    #
    #         logger.info(packt_key + " value ({0}) is verified in {1} of  sdp ".format(packt_value_expected, packt_name))
    #         result = [x for x in sip_verification_result if (x == 0)]
    #         del result[:]
    #         del sip_verification_result[:]
    #         del pv.call_id_ls[:]
    #         pv.call_stack.clear()
    #
    #         return 0
    #
    #     sip.value = None

    def actionUrl(self, **kwargs):
        """
        This method is used to enter the Action URIs on the Web UI of the phone.

        :param:
            :onhookField: Onhook Field Action URI
            :offhookField: Offhook Field Action URI
            :incomingField: Incoming Field Acion URI
            :connectedField: Connected Field Action URI
            :regeventField: Register Event Field Action URI
            :disconnectedField: Disconnected Field Action URI

        :returns: None
        :created by: Aman Bhardwaj
        :creation date: 31/05/2020
        :last update by: Sharma
        :last update date: 11/09/2020
        """
        ip = self.phone_obj.phone_obj.phone.ipAddress
        pbx = kwargs['pbx']
        session = requests.Session()
        loginURL = "http://" + ip + "/sysinfo.html"

        url = "http://" + ip + "/actionURI.html"
        offhookField = kwargs.get('offhookField', '')
        incomingField = kwargs.get('incomingField', '')
        onhookField = kwargs.get('onhookField', '')
        connectedField = kwargs.get('connectedField', '')
        disconnectedField = kwargs.get('disconnectedField', '')
        regeventField = kwargs.get('regeventField', '')

        payload = {
            'offhookField': offhookField,
            'incomingField': incomingField,
            'onhookField': onhookField,
            'connectedField': connectedField,
            'disconnectedField': disconnectedField,
            'regeventField': regeventField,
        }
        auth = (userid, passcode)
        try:
            loginResponse = session.get(loginURL, auth=auth)

            for i in range(2):
                if loginResponse.status_code != 200 or 'Session Expired' in loginResponse.text:
                    console("Attempt to login failed. Trying Again !! ")
                    loginResponse = session.get(loginURL, auth=auth)

            response = session.post(url, auth=auth, data=payload, timeout=4)
            if response.status_code == 200:
                logger.info("Successfully configured Action URI on extension: "
                            + self.phone_obj.phone_obj.phone.extensionNumber, also_console=True)
            else:
                raise Exception("Could not configure Action URI on extension: "
                                + self.phone_obj.phone_obj.phone.extensionNumber + ". Got HTTP code: "
                                + str(response.status_code) + " instead of 200.")
        except ConnectionError as e:
            console("Could not connect to the Web UI of the phone. Error: ", newline=False)
            console(e.message)
        except Exception as e:
            logger.info('Error occurred while configuring top soft-keys on extension: '
                        + self.phone_obj.phone_obj.phone.extensionNumber, also_console=True)
            logger.info('ERROR:', e.message)
        finally:
            session.close()

    def actionInRedialMenu(self, **kwargs):
        """
        Below method is used to perform actions in the redial menu on the phone.

        :param:
            :kwargs:
                :key: Key to press in Redial menu

        :created by: Sharma
        :creation date:
        :last update by: Sharma
        :last update date: 08/08/2020
        """
        keyToPress = kwargs['key']
        self.phone_obj.press_key('Redial')

        if keyToPress == 'Dial':
            if self.phone_obj.phone_type in ("Mitel6910", "Mitel6865i"):
                self.phone_obj.press_key("Enter")
            else:
                self.phone_obj.press_softkey(1)
        elif keyToPress == "None":
            self.phone_obj.sleep(3)
        else:
            raise Exception("INVALID ARGUMENTS PASSED!!!!")

    def createTelnetPackets(self, **kwargs):
        """
        This method is used to create telnet connection on the passed phone.

        Keyword Args:
            phoneObj: PhoneComponent object of the phone to telnet
        :returns: None
        :created by: Sharma
        :creation date: 14/05/2020
        :last update date:
        :last update by:
        """
        import telnetlib
        phoneObj = kwargs['phoneObj']
        ipToTelnet = phoneObj.phone_obj.phone_obj.phone.ipAddress
        logger.info("Creating the telnet connection on <b>{}</b> with IP: <b>{}</b>".format(
            self.phone_obj.phone_obj.phone.ipAddress, ipToTelnet), html=True)
        console("Creating the telnet connection on {} with IP: {}".format(self.phone_obj.phone_obj.phone.ipAddress,
                                                                          ipToTelnet))

        telnetSession = telnetlib.Telnet(ipToTelnet)
        telnetSession.read_until(phoneObj.phone_obj.phone_type + " login:")
        telnetSession.write(b"root\r")

        logger.info("Closing the connection on the PhoneComponent object with IP: <b>" + ipToTelnet + "/b", html=True)
        console("Closing the connection on the PhoneComponent object with IP: " + ipToTelnet)
        telnetSession.close()

    def pcapConverter(self, **kwargs):
        """
        This method convert PCAP file using Tshark into json and text

        Below are example commands executed
            tshark -2 -R "TLS" -r Test.pcap -T json >output_TLS.json
            tshark -V -r Test.pcap > file_to_convert.txt

        :Input_File:
        :Op_file:
        :returns: Nothing
        :created by: Abhishek Khanchi
        :creation date:
        :last update by: Sharma
        :last update date: 07/08/2020
        """
        conversionType = kwargs.get('conversionType', 'text')
        inputFile = kwargs.get('local_pcap_download_file', os.path.realpath(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'Downloads\captureFile.pcap')))
        outputFile = kwargs.get('outputFile', os.path.realpath(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'Downloads\convertedFile.txt')))

        logger.info("Converting PCAP file into " + conversionType, also_console=True)
        try:
            cmd = "tshark "

            if 'filters' in kwargs:
                filters = kwargs['filters']
                if len(filters) > 1:
                    logger.warn("NOT DOING ANYTHING HERE!!")  # will add support for more filters later (if required)
                else:
                    cmd = cmd + ' -Y "{0}=={1}" '.format(filters.keys()[0], filters.values()[0])

                    # cmd = "tshark -V -r {0} -Y " + filters.keys()[0] + "==" + filters.values()[0] \
                    #       + "> {1}".format(inputFile, outputFile)

            if conversionType == 'json':
                cmd = cmd + '-2 -R tls -r "{}" -T json '.format(inputFile)
            elif conversionType == 'text':
                cmd = cmd + '-V -r "{}"'.format(inputFile)

            cmd += ' > "{}"'.format(outputFile)

            os.chdir("C:/Program Files/Wireshark")
            os.system(cmd)
            os.chdir("./")
            logger.info("Successfully converted PCAP file into " + conversionType, also_console=True)
        except Exception:
            raise Exception("Could not convert the PCAP file to text!!")

    def verifyPacketContents(self, **kwargs):
        """
        This method is used to verify the content of a given type of protocol in the
        packets captured.

        Keyword Args:
            contentToVerify: The content to verify
            protocolToVerify: The type of packet to verify i.e., HTTP, TFTP, Telnet, SIP, etc.

        :created by: Sharma
        :creation date: 29/05/2020
        :last update by: Vikhyat Sharma
        :last update date: 15/01/2021
        """
        yaml_file = yaml.load(open(os.path.join(os.path.dirname((os.path.dirname(__file__))),
                                                "Variables/WebUIDetails.yaml")), Loader=yaml.FullLoader)

        protocolEntries = yaml_file.get('Protocols')
        protocolToVerify = str(kwargs['protocolToVerify'])
        contentToVerify = str(kwargs['contentToVerify'])
        if 'SystemIP' in contentToVerify:
            contentToVerify.replace('SystemIP', self.hostIpAddressGetter(proto='local'))

        if 'phoneObj' in kwargs:
            phoneObj = kwargs['phoneObj']
            if contentToVerify.split('=')[1] == 'ipAddress':
                contentToVerify = contentToVerify.replace('ipAddress', phoneObj.phone_obj.phone_obj.phone.ipAddress)
            elif contentToVerify.split('=')[1] == 'extensionNumber':
                contentToVerify = contentToVerify.replace('extensionNumber',
                                                          phoneObj.phone_obj.phone_obj.phone.extensionNumber)

        pcapFilePath = os.path.abspath(os.path.join(os.path.dirname(os.path.dirname(__file__)),
                                                    'Downloads\\captureFile.pcap'))
        convertedFilePath = os.path.abspath(os.path.join(os.path.dirname(os.path.dirname(__file__)),
                                                         'Downloads\\convertedFile.txt'))

        self.pcapConverter(conversionType='text', local_pcap_download_file=pcapFilePath,
                           outputFile=convertedFilePath)

        logger.info("Verifying that <b>{}</b> is present under <b>{}</b> in the captured file.".format(
            contentToVerify, protocolToVerify), html=True)
        console("Verifying the {} is present under {} protocol in the captured file ".format(
            contentToVerify, protocolToVerify))

        lineIndex = -1

        fileContents = []
        with open(convertedFilePath, 'r') as convertedFile:
            fileContent = convertedFile.read().decode(encoding='utf-8')
            fileContents = fileContent.split('\n')

        if 'Call-Duration' in contentToVerify:
            callDurationFound = 0
            for line in fileContents:
                if 'Call-Duration' in line:
                    callDurationFound = 1
                    content = line.split('Duration=')
                    if 25 <= int(content[-1][:2]) <= 40:
                        lineIndex = fileContents.index(line)
                        console("Line Index: ", str(lineIndex))
                    else:
                        logger.info("Call Duration is not around 30 seconds. Actual value is: "
                                    + content[2][:2], also_console=True)
                    break
            if not callDurationFound:
                raise Exception("Call Duration is not present in the captured file.")

        else:
            lineIndex = 0
            startingIndex = 0
            nextFrameIndex = 0
            protocolFound, contentFound = False, False
            while lineIndex < len(fileContents):
                for line in fileContents[startingIndex:]:
                    lineIndex += 1
                    if protocolToVerify in line:
                        protocolFound = True
                        break
                startingIndex = lineIndex
                for line in fileContents[startingIndex:]:
                    lineIndex += 1
                    if 'Frame' in line:
                        nextFrameIndex = lineIndex
                        break
                console("Packet verifying: ")
                console("Starting Index: {} and nextFrameIndex: {}".format(startingIndex, nextFrameIndex))
                for content in fileContents[startingIndex:nextFrameIndex]:
                    if contentToVerify in content:
                        contentFound = True
                startingIndex = nextFrameIndex
            if protocolFound:
                if contentFound:
                    logger.info("Successfully verified that <b>{}</b> is present under <b>{}</b> in the captured "
                                "file.".format(contentToVerify, protocolToVerify), html=True)
                    console("Successfully verified that {} is present under {} in the captured file.".format(
                            contentToVerify, protocolToVerify))
                else:
                    raise Exception("Not able to verify that {} is present under {} in the captured file. ".format(
                                    contentToVerify, protocolToVerify))
            else:
                raise Exception("{} is not present in the captured file.".format(protocolToVerify))

    def verifyProtocolInCapturedPackets(self, **kwargs):
        """
        This method will verify the presence of given protocol packets in the packet file.
        Keyword Args:
            protocolToVerify: Protocol to verify in file, i.e., HTTP, SIP

        :returns: None
        :created by: Sharma
        :creation date: 30/05/2020
        :last update by:
        :last update date:
        """
        try:
            pcapPacketFile = os.path.abspath(os.path.join(os.path.dirname(os.path.dirname(__file__)),
                                                          'Downloads\\captureFile.pcap'))
            convertedFilePath = os.path.abspath(os.path.join(os.path.dirname(os.path.dirname(__file__)),
                                                             'Downloads\\convertedFile.txt'))

            yaml_file = yaml.load(open(os.path.join(os.path.dirname((os.path.dirname(__file__))),
                                                    "Variables\\WebUIDetails.yaml")), Loader=yaml.FullLoader)
            protocolToVerify = kwargs['protocolToVerify']
            packetsFound = 0
            packetsList = yaml_file.get('Protocols')

            self.pcapConverter(conversionType='text', local_pcap_download_file=pcapPacketFile,
                               outputFile=convertedFilePath)

            packetFile = open(os.path.abspath(os.path.join(os.path.dirname(os.path.dirname(__file__)),
                                                           'Downloads\\convertedFile.txt')))

            logger.info("Checking the capture file has {} protocol packets".format(protocolToVerify))
            for lines in packetFile.readlines():
                if protocolToVerify in lines:
                    packetsFound = 1
                    break

            if packetsFound == 1:
                console(str(packetsList.keys()[packetsList.values().index(protocolToVerify)]) +
                        " Packets are present in the packets.")
            else:
                raise Exception("No " + str(packetsList.keys()[packetsList.values().index(protocolToVerify)]) +
                                " Packets found in the captured file.")
        except ValueError as err:
            logger.error("Got Error: " + err.message)
            raise Exception("INVALID PROTOCOL ENTRY PASSED !!!")

    def verifyProtocolNotPresent(self, **kwargs):
        """
        This method verifies the packets of the passed protocol are not present in the captured file.

        Keyword Args:
            protocolToVerify: Protocol to check in the captured file

        returns: None
        created by: Vikhyat Sharma
        creation date: 06/08/2020
        last update by:
        last update date:
        """
        protocolToVerify = kwargs['protocolToVerify']
        convertedFile = os.path.realpath(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'Downloads\convertedFile.txt'))
        try:
            with open(convertedFile) as file:
                data = file.read().decode(encoding='utf-8')
                for line in data:
                    if protocolToVerify in line:
                        raise Exception("{0} packets are present in the captured file!!".format(protocolToVerify))
            logger.info("<b>{}</b> packets are not present in the captured file.", html=True)
            console("{} packets are not present in the captured file.")
        except IOError:
            if 'capturefile.pcap' not in os.listdir('../Downloads/'):
                raise Exception("Captured File is not present in Downloads sub-folder under Project-tree!!")
            else:
                raise Exception("Converted file is not present in Downloads sub-folder under Project-tree!!")

    def verify_ringer_state(self, **kwargs):
        """
        Below method is used to verify ringer state of the phone.

        :param:
            :kwargs:
                ::

        :created by: Ramkumar.G
        :creation date:
        :last update by: Sharma
        :last update date:
        """

        console(kwargs)
        ring_state = str(kwargs['ringer_state'])
        if ring_state == "Off":
            if (self.phone_obj.phone_obj.verify_ringer_state(ring_state)):
                console("Ringer state is Off")
                logger.info("Ringer state is Off")
            else:
                console("Ringer state is not Off")
                logger.info("Ringer state is not Off")
                raise Exception("Ringer state is not Off")
        else:
            RingerVolume = str(kwargs.get('ringer_volume'))
            if self.phone_obj.phone_obj.verify_ringer_state(ring_state, RingerVolume):
                console("Ringer volume " + RingerVolume + "is verified")
                logger.info("Ringer volume " + RingerVolume + "is verified")
            else:
                raise Exception("Ringer volume " + RingerVolume + " value is not matching")

    def verifyBrightnessLevel(self, **kwargs):
        """
        This method is used to verify the current brightness level of the phone with the passed level.

        Keyword Args:
            level: Brightness Level to check

        :returns: None
        :created by: Sharma
        :creation date: 29/07/2020
        :last update by:
        :last update date:
        """
        level = kwargs["level"]
        # self.phone_obj.sleep(5)    # This wait may be important for test case to work in idle state.
        if self.phone_obj.get_phone_brightness() == level:
            logger.info("Successfully verified the current brightness level as <b>" + level + "</b>.")
            console("Successfully verified the current brightness level as " + level)
        else:
            raise Exception("Could not verify the brightness level of phone as " + level + "!!! GOT " +
                            self.phone_obj.get_phone_brightness() + " instead.")

    def verifyTimeBetweenPackets(self, **kwargs):
        """
        This method is used to verify the time between the packets.

        Keyword Args:
            time: Time between the packets (in seconds)

        :returns: None
        :created by: Sharma
        :creation date: 07/08/2020
        :last update by:
        :last update date:
        """
        try:
            timeBetweenProtocols = int(kwargs['time'])
            captureFile = open(os.path.realpath(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'Downloads/convertedFile.txt')))
            frameTimes = []
            for line in captureFile.readlines():
                if "Arrival Time:" in line:
                    frameTimes.append(float(line[line.rfind(':') + 1:].strip()))
            for i in range(len(frameTimes) - 1):
                if not ((abs(frameTimes[i] - frameTimes[i + 1]) - timeBetweenProtocols) < 1):
                    raise Exception("TIME BETWEEN PROTOCOLS IS MORE THAN " + str(timeBetweenProtocols)
                                    + " FOUND PACKETS WITH DIFFERENCE OF "
                                    + str((abs(frameTimes[i] - frameTimes[i + 1]) - timeBetweenProtocols))
                                    + " IN THE FILE !!")
            logger.info("Packets have a correct time of " + str(timeBetweenProtocols) + " seconds between them.")
        except IOError:
            raise Exception("CONVERTED TEXT FILE NOT FOUND !!!")

    def verifyFileContents(self, **kwargs):
        """
        This method is used to verify the contents of the file.

        Keyword Args:
            phone: Phone Object
            fileName: File To open (This file must be in Downloads folder of the Project)
            textToCheck: Text to check in the file

        :returns: None
        :created by: Ramkumar G.
        :creation date:
        :last update by: Sharma
        :last update date: 07/09/2020
        """
        try:
            phone = str(kwargs['phone'].phone_obj.phone_obj.phone.extensionNumber)
            filename = str(kwargs['fileName'])
            filePath = os.path.join(os.path.dirname((os.path.dirname(__file__))), "Downloads/" + filename)

            if '.csv' in filename:
                with open(filePath, 'r') as csvfile:
                    csvReader = csv.reader(csvfile)
                    for row in csvReader:
                        if row[0] == phone:
                            console(phone + " number is present in the " + filename)
                        elif row[0] == phone:
                            console(" No entries are there in the " + filename)
                        else:
                            console(phone + " number is not present in the row " + filename)
            else:
                textToCheck = kwargs['textToCheck']
                filePath = os.path.realpath(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'Downloads/'+filename))
                console("File Path : ", filePath)
                fileContents = open(filePath)
                foundStatus = False
                for content in fileContents.readlines():
                    if textToCheck in content:
                        foundStatus = True
                        break

                if foundStatus:
                    logger.info(textToCheck + " is present in " + filename + " file.", also_console=True)
                else:
                    raise Exception(textToCheck + " is not present in the " + filename + " file.")
        except IOError as e:
            raise Exception("COULD NOT FOUND THE FILE SPECIFIED !!" + "\n" + e)
        except Exception as e:
            raise Exception(e)

    def createXMLFile(self, rootElement, kwargs, attr={}):
        """
        This method is used to XML File using the paramters passed.

        :returns:
        :created by: Sharma
        :creation date: 24/08/2020
        :last update by:
        :last update date:
        """
        xmlFile = open('../Configuration/AutomationXML.xml', 'w')

        from xml.etree.ElementTree import Element, SubElement
        from xml.etree import ElementTree
        from xml.dom import minidom

        rootElement = Element(rootElement)
        for parameter, value in kwargs.items():
            configurationItem = SubElement(rootElement, parameter, attrib=attr.get(parameter, {}))
            configurationItem.text = str(value)

        roughString = ElementTree.tostring(rootElement, 'utf-8')
        reparsed = minidom.parseString((roughString.replace('&lt;', '<')).replace('&gt;', '>'))
        xmlFile.write(reparsed.toprettyxml(indent="    "))

    def longPressKey(self, **kwargs):
        """
        This method is used to long press any key on the phone.

        Keyword Args:
            keyToPress: Key to long press

        :returns: None
        :created by: Ramkumar. G
        :creation date:
        :last update by:
        :last update date:
        """
        keyToPress = str(kwargs['keyToPress'])

        logger.info("Long pressing <b>{}</b> key on extension: <b>{}</b>".format(keyToPress,
                    self.phone_obj.phone_obj.phone.extensionNumber), html=True)
        console("Long pressing {} key on extension: {}".format(keyToPress,
                                                               self.phone_obj.phone_obj.phone.extensionNumber))
        self.phone_obj.long_press_key(keyToPress)

    def changeScreenSaverSettings(self, **kwargs):
        """
        This method is used to change the change the scree saver settings on the phone.

        Note: Screensaver settings cannot be changed on 6865i and 6910 models.

        :param:
            :screenSaverMode: Mode to set (Mode1-Mode3 are present by default)
            :screenSaverTimer: Idle time after which screen saver will appear

        :returns: None
        :created by: Sharma
        :creation date: 28/08/2020
        :last update by:
        :last update date:
        """
        logger.info("Moving to screen saver settings on extension: " + self.phone_obj.phone_obj.phone.extensionNumber
                    , html=True)
        console("Moving to screen saver settings on extension: " + self.phone_obj.phone_obj.phone.extensionNumber)

        self.phone_obj.press_key('Menu')
        for i in range(3):
            self.phone_obj.press_key('ScrollRight')
        if self.phone_obj.phone_type == 'Mitel6930':
            self.phone_obj.press_key('ScrollRight')
        self.phone_obj.press_key('Enter')

        if 'screenSaverMode' in kwargs:
            screenSaverMode = kwargs['screenSaverMode']
            logger.info("Setting the screen saver mode to <b>{}</b> on extension: <b>{}</b>".format(screenSaverMode
                                                                                                    ,
                                                                                                    self.phone_obj.phone_obj.phone.extensionNumber),
                        html=True)
            console("Setting the screen saver mode to {} on extension: {}".format(screenSaverMode
                                                                                  ,
                                                                                  self.phone_obj.phone_obj.phone.extensionNumber))
            for i in range(3):
                self.phone_obj.press_key('ScrollLeft')
            if screenSaverMode != 'Mode 1':
                for i in range(int(screenSaverMode[-1]) - 1):
                    self.phone_obj.press_key('ScrollRight')
            self.verifyDisplayMessageUtil(screenSaverMode)

        self.phone_obj.press_key('ScrollDown')
        if 'screenSaverTimer' in kwargs:
            screenSaverTimer = kwargs['screenSaverTimer']
            logger.info("Setting the screen saver timer to <b>{}</b> on extension: <b>{}</b>".format(screenSaverTimer
                                                                                                     ,
                                                                                                     self.phone_obj.phone_obj.phone.extensionNumber),
                        html=True)
            console("Setting thee screen saver timer to {} on extension: {}".format(screenSaverTimer
                                                                                    ,
                                                                                    self.phone_obj.phone_obj.phone.extensionNumber))
            for i in range(4):
                self.phone_obj.press_softkey(2)
            self.phone_obj.input_a_number(screenSaverTimer)

        self.phone_obj.press_softkey(1)
        self.phone_obj.press_key('GoodBye')

    def verifyScreenSaverDisplay(self, **kwargs):
        """
        This method is used to verify the screen saver details being displayed on the phone.

        Keyword Args:
            screenSaveIsSet: To check whether screen saver is set on the phone i.e., True or False
            isTimeSet: To check if Time is displayed on the screen saver i.e., True or False
            missedCallIndicator: To check if missed call indicator is present i.e., True of False
            missedCallCount: To check the missed call count i.e., 1/2/3
            screenSaverType: Screen Saver Mode set on the phone i.e., Default(0/1/2/3) or Custom


        :returns: None
        :created by: Sharma
        :creation date: 28/08/2020
        :last update by:
        :last update date:
        """
        screenSaverIsSet = kwargs.get('screenSaverIsSet', 'true')
        screenSaverDetails = self.phone_obj.get_phone_screensaver()
        extension = self.phone_obj.phone_obj.phone.extensionNumber
        if screenSaverIsSet.lower() == 'true':
            if screenSaverDetails != "No screen saver found on the phone":
                logger.info("Screen Saver is set on extension: " + extension, also_console=True)
            else:
                raise Exception("Screen Saver is not set on extension: " + extension)
        elif screenSaverIsSet.lower() == 'false':
            if screenSaverDetails == "No screen saver found on the phone":
                logger.info("Screen Saver is not set on extension: " + extension, also_console=True)
            else:
                raise Exception("Saver saver is set on extension: " + extension)

        if 'isTimeShown' in kwargs:
            isTimeShown = kwargs['isTimeShown']
            if isTimeShown.lower() == 'true':
                if 'Hour' in screenSaverDetails:
                    logger.info("Time is displayed on the screen saver of extension: " + extension, also_console=True)
                else:
                    raise Exception("Time is not displayed on the screen of extension: " + extension)
            elif isTimeShown.lower() == 'false':
                if 'Hour' not in screenSaverDetails:
                    logger.info("Time is not displayed on the screen saver of extension: " + extension,
                                also_console=True)
                else:
                    raise Exception("Time is displayed on the screen saver of extension: " + extension)
            else:
                raise Exception("INVALID ARGUMENT PASSED !!")
        if 'missedCallIndicator' in kwargs:
            missedCallIndicator = kwargs['missedCallIndicator']
            if missedCallIndicator.lower() == 'true':
                if screenSaverDetails['IsMissedCallImgVisible'] == '1':
                    logger.info("Missed Call Indicator is present on the screen saver of extension: " + extension
                                , also_console=True)
                else:
                    raise Exception(
                        "Missed Call Indicator is not present on the screen saver of extension: " + extension)
            elif missedCallIndicator.lower() == 'false':
                if screenSaverDetails['IsMissedCallImgVisible'] == '0':
                    logger.info("Missed Call Indicator is not present on the screen saver of extension: " + extension
                                , also_console=True)
                else:
                    raise Exception("Missed Call Indicator is present on the screen saver of extension: " + extension)
            else:
                raise Exception("INVALID ARGUMENT PASSED !!")
        if 'screenSaverType' in kwargs:
            screenSaverType = kwargs['screenSaverType']
            if screenSaverType.lower() == 'default':
                if screenSaverDetails['ImgIndex'] in ('0', '1', '2', '3'):
                    logger.info("Default screen saver set is on extension: " + extension, also_console=True)
                else:
                    raise Exception("Default screen saver is not set on extension: " + extension)
            elif screenSaverType.lower() == 'custom':
                if screenSaverDetails['ImgIndex'] not in ('0', '1', '2', '3'):
                    logger.info("Custom screen saver is set on extension: " + extension, also_console=True)
                else:
                    raise Exception("Custom screen saver is not set on extension: " + extension + ". Got Mode: "
                                    + screenSaverDetails['ScreenType'] + " instead.")
            else:
                raise Exception("INVALID ARGUMENTS PASSED FOR 'screenSaverType' !!")

    def isBackgroundImageSet(self, typeOfImage):
        """
        This method is used to check if custom background image is set on the phone.

        :returns: None
        :created by: Sharma
        :creation date: 31/08/2020
        :last update by:
        :last update date:
        """
        console(self.phone_obj.is_background_image_set())
        if typeOfImage == 'Custom':
            if self.phone_obj.is_background_image_set():
                logger.info("Custom Background Image is set on extension: "
                            + self.phone_obj.phone_obj.phone.extensionNumber, also_console=True)
            else:
                raise Exception("Custom Background image is not present on extension: "
                                + self.phone_obj.phone_obj.phone.extensionNumber)
        else:
            if not self.phone_obj.is_background_image_set():
                logger.info("Default Background Image is set on extension: "
                            + self.phone_obj.phone_obj.phone.extensionNumber, also_console=True)
            else:
                raise Exception("Default Background image is not present on extension: "
                                + self.phone_obj.phone_obj.phone.extensionNumber)

    def setBackgroundImage(self, **kwargs):
        """
        This method is used to set the background image on the phone.

        Keyword Args:
            server: Type of server to use
            typeOfImage: Type of Image to configure i.e., Custom or Default

        returns: None
        created by: Vikhyat Sharma
        creation date:
        last update by:
        last update date:
        """
        serverToUse = kwargs['server']
        typeOfImage = kwargs['typeOfImage']
        phoneModel = self.phone_obj.phone_type

        logger.info("Configuring " + typeOfImage + " background image on extension: "
                    + self.phone_obj.phone_obj.phone.extensionNumber, also_console=True)

        if phoneModel in ('Mitel6867i', 'Mitel6920'):
            phoneModel = '6920'
        elif phoneModel in ('Mitel6869i', 'Mitel6930'):
            phoneModel = '6930'

        if typeOfImage == 'Custom':
            if serverToUse == 'FTP':
                startupConfiguration = {
                    'background image': 'ftp://' + FtpUser + ':' + FtpPass + '@' + Ftpserver + '/BGImages/'
                                        + phoneModel + '.jpg'
                }

            elif serverToUse == 'HTTP':
                startupConfiguration = {
                    'background image': 'https://' + httpUserName + ':' + httpPassword + '@' + httpServer + '/BGImages/'
                                        + phoneModel + '.jpg'
                }
            else:
                raise Exception("INVALID SERVER {0} PASSED!!".format(serverToUse))
        elif typeOfImage == 'default':
            startupConfiguration = {}
        else:
            raise Exception("INVALID ARGUMENT PASSED FOR 'typeOfImage'.")

        self.createfile(fileName='startup.cfg', parameter=startupConfiguration)
        self.sendFileToServer(connection='FTP', fileName='startup.cfg', folderName='AutomationTesting')

        configurationDetails = {'download protocol': 'FTP', 'ftp server': Ftpserver,
                                'ftp path': 'AutomationTesting/',
                                'ftp username': FtpUser, 'ftp password': FtpPass
                                }
        self.configureXMLParameter(**configurationDetails)
        self.rebootPhone()
        self.phone_obj.sleep(10)
        logger.info("Configured " + typeOfImage + " background image on extension: "
                    + self.phone_obj.phone_obj.phone.extensionNumber, also_console=True)

    def setCustomScreenSaver(self, **kwargs):
        """

        """
        serverToUse = kwargs['server']
        screenSaverType = kwargs['saverType']
        phoneModel = self.phone_obj.phone_type

        logger.info("Configuring custom screen saver background image on extension: "
                    + self.phone_obj.phone_obj.phone.extensionNumber, also_console=True)

        if phoneModel in ('Mitel6867i', 'Mitel6920'):
            phoneModel = '6920'
        elif phoneModel in ('Mitel6869i', 'Mitel6930'):
            phoneModel = '6930'

        if screenSaverType == 'Custom':
            if serverToUse == 'FTP':
                entries = {
                    'screen saver background image': 'ftp://' + FtpUser + ':' + FtpPass + '@' + Ftpserver + '/BGImages/'
                                                     + phoneModel + '.jpg'
                }
            elif serverToUse == 'HTTP':
                entries = {
                    'screen saver background image': 'https://' + httpUserName + ':' + httpPassword + '@' + httpServer
                                                     + '/BGImages/' + phoneModel + '.jpg'
                }
        elif screenSaverType == 'default':
            entries = {}
        else:
            raise Exception("INVALID ARGUMENT PASSED FOR 'screenSaverType'.")

        self.createfile(fileName='startup.cfg', parameter=entries)
        self.sendFileToServer(connection='FTP', fileName='startup.cfg', folderName='AutomationTesting')

        configurationDetails = {'download protocol': 'FTP', 'ftp server': Ftpserver, 'ftp path': 'AutomationTesting/',
                                'ftp username': FtpUser, 'ftp password': FtpPass
                                }
        self.configureXMLParameter(**configurationDetails)
        self.rebootPhone()
        self.phone_obj.sleep(5)
        logger.info("Configured " + screenSaverType + " scree saver background image on extension: "
                    + self.phone_obj.phone_obj.phone.extensionNumber, also_console=True)

    def getFirmwareVersion(self):
        """
        This method is used to get the firmware version on the phone

        :returns: Firmware Version (String)
        :created by: Sharma
        :creation date: 14/09/2020
        :last update date:
        :last updated by:
        """
        return self.phone_obj.get_firmware_version()

    def verifyTimeZonePresent(self, **kwargs):
        """
        This method is used to verify whether the passed time zone is present in the timezone settings of the phone.

        Keyword Args:
            timeZone: Time Zone to verify
            area: Zone Area i.e., Asia/America

        :returns: None
        :created by: Vikhyat Sharma
        :creation date: 25/05/2020
        :last update by:
        :last update date:
        """

        timeZone = kwargs['timeZone']
        area = kwargs['area']

        logger.info("Verifying <b>{}</b> time zone is present under <b>{}</b> area on extension: <b>{}</b>".format(
                    timeZone, area, self.phone_obj.phone_obj.phone.extensionNumber), html=True)
        console("Verifying {} time zone is present under {} area on extension: {}".format(timeZone, area,
                self.phone_obj.phone_obj.phone.extensionNumber))
        console(self.phone_obj.get_highlighted_text_properties())
        for _ in range(7):
            self.phone_obj.press_key('ScrollUp')

        if area == 'Asia':
            self.phone_obj.press_key('ScrollDown')
        elif area == 'Atlantic':
            for _ in range(2):
                self.phone_obj.press_key('ScrollDown')
        elif area == 'Australia':
            for _ in range(3):
                self.phone_obj.press_key('ScrollDown')
        elif area == 'Europe':
            for _ in range(4):
                self.phone_obj.press_key('ScrollDown')
        elif area == 'Pacific':
            for _ in range(5):
                self.phone_obj.press_key('ScrollDown')
        elif area == 'Others':
            for _ in range(6):
                self.phone_obj.press_key('ScrollDown')
        else:
            raise Exception("INVALID AREA: " + area + " PASSED FOR TIMEZONE!!")

        self.phone_obj.press_key('ScrollRight')

        if timeZone in ('HK', 'BG'):
            for _ in range(5):
                self.phone_obj.press_key('ScrollDown')
        elif timeZone in ('IN-Kolkata', 'BB'):
            for _ in range(6):
                self.phone_obj.press_key('ScrollDown')
        else:
            raise Exception("NOT POSSIBLE TO NAVIGATE TO {} FOR NOW!!".format(timeZone))
        self.verifyHighlightedText(timeZone)

    def verifyDirectoryFormat(self, **kwargs):
        """
        This method is used to verify the format of the contacts shown in directory.

        This keywords assumes the phone is in directory.

        Keyword Args:
            pbx: Call Manager of the phone
            directoryFormat: Format of directory/Sorting basis of directory i.e., By Last/By First

        :returns: None
        :created by: Vikhyat Sharma
        :creation date: 01/12/2020
        :last update by:
        :last update date:
        """
        pbx = kwargs['pbx']
        directoryFormat = kwargs['directoryFormat']

        self.verifyDisplayMessageUtil('Directory')
        if pbx == 'MiVoice':
            if directoryFormat == 'By First':
                self.verifyDisplayMessageUtil('auto user')
            elif directoryFormat == 'By Last':
                self.verifyDisplayMessageUtil(', auto')
            else:
                raise Exception("Invalid Directory Format: " + directoryFormat + " passed!!")
        elif pbx == 'MiCloud':
            if directoryFormat == 'By First':
                self.verifyDisplayMessageUtil('Test user')
            elif directoryFormat == 'By Last':
                self.verifyDisplayMessageUtil(', Test')
            else:
                raise Exception("Invalid Directory Format: " + directoryFormat + " passed!!")
        else:
            raise Exception(pbx + " does not support sorting directory!!")

    def verifyHighlightedText(self, textToVerify):
        """
        This method is used to verify the passed text is in the highlighted text.

        Args:
            textToVerify: Highlighted Text to Verify

        :returns: None
        :created by: Vikhyat Sharma
        :creation date: 03/12/2020
        :last update by:
        :last update date:
        """

        highlightedInfo = self.phone_obj.get_highlighted_text_properties()
        highlightedText = ''

        console(highlightedInfo)
        for entry in highlightedInfo:
            if int(entry['IsHighlighted']):
                highlightedText = entry['ItemText']

        if textToVerify in highlightedText:
            logger.info("<b>" + textToVerify + "</b> is highlighted on extension: <b>"
                        + self.phone_obj.phone_obj.phone.extensionNumber + "</b>", html=True)
            console(textToVerify + " is highlighted on extension: " + self.phone_obj.phone_obj.phone.extensionNumber)
        else:
            raise Exception(textToVerify + " is not highlighted!! Got " + highlightedText + " instead.")

    def callHistoryForTelepo(self, **kwargs):
        """
        This method is used to navigate in the call history settings of Telepo Call Manager.

        param:
            self: PhoneComponent Object
        Keyword Args:
            folderName: folder to open i.e., Outgoing/ Missed/ Received
            action: action to perform i.e., Details/Dial/Delete/Quit/OffHook/Loudspeaker
        :returns: None

        :created by: Vikhyat Sharma
        :creation date: 10/11/2020
        :last update by:
        :last update date:
        """
        folderName = kwargs['folderName']
        action = kwargs['action']

        logger.info("Opening the <b>" + folderName + "</b> folder of Call History on <b>"
                    + self.phone_obj.phone_obj.phone.extensionNumber + "</b> and performing <b>" + action
                    + "</b> action.", html=True)

        console("Opening the " + folderName + " folder of Call History on "
                + self.phone_obj.phone_obj.phone.extensionNumber + " and performing " + action + " action.")

        self.phone_obj.press_key('CallersList')
        self.phone_obj.sleep(5)
        if folderName == 'Missed':
            if self.phone_obj.phone_type == 'Mitel6865i':
                self.phone_obj.press_key('ScrollDown')

            self.phone_obj.press_key('Enter')
            self.verifyDisplayMessageUtil('Missed calls')

            if self.phone_obj.phone_type == 'Mitel6865i':
                self.phone_obj.press_key('Enter')

        elif folderName == 'Received':
            if self.phone_obj.phone_type == 'Mitel6865i':
                for _ in range(2):
                    self.phone_obj.press_key('ScrollDown')
            else:
                self.phone_obj.press_key('ScrollDown')

            self.phone_obj.press_key('Enter')
            self.verifyDisplayMessageUtil('Incoming calls')

            if self.phone_obj.phone_type == 'Mitel6865i':
                self.phone_obj.press_key('Enter')

        elif folderName == 'Outgoing':
            if self.phone_obj.phone_type == 'Mitel6865i':
                for _ in range(3):
                    self.phone_obj.press_key('ScrollDown')
            else:
                for _ in range(2):
                    self.phone_obj.press_key('ScrollDown')
            self.phone_obj.press_key('Enter')
            self.verifyDisplayMessageUtil('Outbound calls')

            if self.phone_obj.phone_type == 'Mitel6865i':
                self.phone_obj.press_key('Enter')

        elif folderName == 'Clear log':
            if self.phone_obj.phone_type == 'Mitel6865i':
                for _ in range(4):
                    self.phone_obj.press_key('ScrollDown')
            else:
                for _ in range(3):
                    self.phone_obj.press_key('ScrollDown')
            self.verifyDisplayMessageUtil('Clear log')
            self.phone_obj.press_key('Enter')

            self.phone_obj.sleep(5)
            if self.phone_obj.phone_type == 'Mitel6865i':
                self.phone_obj.press_key('ScrollDown')
        else:
            raise Exception("INVALID FOLDER({}) PASSED FOR CALL HISTORY".format(folderName))
        self.phone_obj.sleep(3)

        if action == 'Details':
            logger.warn("Telepo does not support Details View of Call History entry!!")
        elif action == 'Dial':
            if self.phone_obj.phone_type == 'Mitel6865i':
                self.phone_obj.press_key('Enter')
            else:
                self.verifyDisplayMessageUtil('Select')
                self.phone_obj.press_softkey(1)
            self.waitTill(timeInSeconds=5)
        elif action == 'Quit':
            self.phone_obj.press_key('GoodBye')
        elif action == 'OffHook':
            self.phone_obj.press_key('OffHook')
        elif action == 'Loudspeaker':
            self.phone_obj.press_key('Loudspeaker')
        else:
            raise Exception("Invalid action({0}) passed for Call history for extension: {1}".format(
                action, self.phone_obj.phone_obj.phone.extensionNumber))

    def verifyLEDStateForTelepo(self, **kwargs):
        """
        This method is used to verify the LED state of softkeys on Telepo call manager registered phones.

        This method is only for programmed softkeys on Telepo phones. If the LED type is a hard key, then use the
        legacy method (verifyLedState).

        :param:
            :self: PhoneComponent object
            :ledType: Key to verify LED of e.g., BLF/Park/Pickup
            :ledMode: LED Mode to verify i.e., On/Blink/Off

        :returns: None

        :created by: Vikhyat Sharma
        :creation date: 11/11/2020
        :last updated by:
        :last update on:
        """
        if len(kwargs) >= 2:
            ledType = kwargs['ledToVerify']
            ledMode = kwargs['ledMode']

            ledType = ledType.lower()
            if ledType == 'intercom':
                if self.phone_obj.phone_type == 'Mitel6865i':
                    ledType = 'Line1'
                else:
                    ledType = 'Line3'
            elif ledType == 'blf':
                if self.phone_obj.phone_type == 'Mitel6865i':
                    ledType = 'Line2'
                else:
                    ledType = 'Line4'
            elif ledType == 'park':
                if self.phone_obj.phone_type == 'Mitel6865i':
                    ledType = 'Line3'
                else:
                    ledType = 'Line5'
            elif ledType == 'pickup':
                if self.phone_obj.phone_type == 'Mitel6865i':
                    ledType = 'Line4'
                else:
                    ledType = 'Line6'

            if self.phone_obj.phone_type == 'Mitel6940' and 'Line' in ledType:
                logger.warn("Mitel6940 set does not have Line LEDs", also_console=True)
            else:
                if self.phone_obj.verify_led_state(ledType, ledMode):
                    logger.info("LED state of <b>" + ledType + "</b> verified as <b>"
                                + ledMode + "</b> on " + self.phone_obj.phone_obj.phone.extensionNumber, html=True)
                    console("LED state of " + ledType + " verified as " + ledMode + " on "
                            + self.phone_obj.phone_obj.phone.extensionNumber)
                else:
                    raise Exception("LED state of " + ledType + " verification as " + ledMode + " failed on "
                                    + self.phone_obj.phone_obj.phone.extensionNumber)
        else:
            raise Exception("Please check the arguments passed: %s" % kwargs)

    def pressProgrammmedKeyOnTelepo(self, **kwargs):
        """
        This method is used to press the pre-configured programmed keys on phones registered with Telepo call manager.

        Keyword Args:
            keyToPress: Program key to press

        :returns: None
        :created by: Vikhyat Sharma
        :creation date: 11/11/2020
        :last update by:
        :last update date:
        """
        keyToPress = kwargs['keyToPress']
        keyToPress = keyToPress.lower()

        if keyToPress == 'intercom':
            if self.phone_obj.phone_type == 'Mitel6865i':
                keyToPress = 'ProgramKey1'
            else:
                keyToPress = 'ProgramKey3'
        elif keyToPress == 'blf':
            if self.phone_obj.phone_type == 'Mitel6865i':
                keyToPress = 'ProgramKey2'
            else:
                keyToPress = 'ProgramKey4'
        elif keyToPress == 'park':
            if self.phone_obj.phone_type == 'Mitel6865i':
                keyToPress = 'ProgramKey3'
            else:
                keyToPress = 'ProgramKey5'
        elif keyToPress == 'pickup':
            if self.phone_obj.phone_type == 'Mitel6865i':
                keyToPress = 'ProgramKey4'
            elif self.phone_obj.phone_type == 'Mitel6869i':
                keyToPress = 'ProgramKey5'
            else:
                keyToPress = 'ProgramKey6'
        elif keyToPress == 'favourites':
            if self.phone_obj.phone_type == 'Mitel6867i':
                keyToPress = 'BottomKey1'
            elif self.phone_obj.phone_type == 'Mitel6930':
                keyToPress = 'BottomKey2'
            elif self.phone_obj.phone_type == 'Mitel6865i':
                self.phone_obj.press_key('ProgramKey8')
                self.phone_obj.sleep(5)
                for _ in range(2):
                    self.phone_obj.press_key('ScrollDown')
                self.verifyDisplayMessageUtil('Favourites')
                self.phone_obj.press_key('Enter')
                self.phone_obj.sleep(5)
                self.phone_obj.press_key('ScrollDown')
                keyToPress = 'Enter'
            else:
                raise Exception("INVALID PHONE TYPE (" + self.phone_obj.phone_type + ") PASSED!!")
        else:
            raise Exception("INVALID KEY TO PRESS ({}) PASSED!!".format(keyToPress))

        logger.info("Pressing <b>{}</b> on extension: <b>{}</b>.".format(keyToPress,
                    self.phone_obj.phone_obj.phone.extensionNumber), html=True)
        console("Pressing {} on extension: {}.".format(keyToPress, self.phone_obj.phone_obj.phone.extensionNumber))
        self.phone_obj.press_key(keyToPress)

    def enterString(self, stringToEnter):
        """
        This method is used to enter a string in a input field on the phone.

        :param:
            :stringToEnter: (str) String to Enter on the phone

        :returns: None
        :created by: Vikhyat Sharma
        :creation date: 17/12/2020
        :last update by:
        :last update date:
        """

        if stringToEnter:
            logger.info("Entering '<b>{}</b>' on extension: <b>{}</b>".format(stringToEnter,
                                                                              self.phone_obj.phone_obj.phone.extensionNumber),
                        html=True)
            console(
                "Entering '{}' on extension: {}".format(stringToEnter, self.phone_obj.phone_obj.phone.extensionNumber))
            # stringToDialPadMap = {
            #     'abc': 'DialPad2',
            #     'def': 'DialPad3',
            #     'ghi': 'DialPad4',
            #     'jkl': 'DiadPad5',
            #     'mno': 'DialdPad6',
            #     'pqrs': 'DialPad7',
            #     'tuv': 'DialPad8',
            #     'wxyz': 'DialPad9',
            # }
            stringsOnDialPad = ('ABCabc2', 'DEFdef3', 'GHIghi4', 'JKLjkl5', 'MNOmno6', 'PQRSpqrs7', 'TUVtuv8',
                                'WXYZwxyz9')
            # noOfPresses = {
            #     'adgjmptw': 1,
            #     'behknqux': 2,
            #     'cfilorvy': 3,
            #     'sz': 4,
            # }
            noOfPresses = ('ADGJMPTW', 'BEHKNQUX', 'CFILORVY', 'SZ234568', 'adgjmptw79', 'behknqux', 'cfilorvy', 'sz')

            for letter in stringToEnter:
                for string in noOfPresses:
                    if letter in string:
                        presses = noOfPresses.index(string)
                        break
                for i in range(presses):
                    for string in stringsOnDialPad:
                        if letter in string:
                            dialPadKey = str(stringsOnDialPad.index(letter) + 2)
                            break
                    self.phone_obj.press_key('DialPad' + dialPadKey)
        else:
            logger.warn("Passed an empty string to enter")

    def changeEAPSettings(self, **kwargs):
        """
        This method changes the EAP settings on the phone

        :param:
            :eapType: (String) EAP Type to configure i.e., Disabled/
            :identity: (String) Identity for the EAP settings
            :password: (String) MD5 Password String

        :returns: None
        :created by: Vikhyat Sharma
        :creation date: 17/12/2020
        :last update by:
        :last update date:
        """
        eapType = kwargs['eapType']
        identity = kwargs.get('identity', '')
        password = kwargs.get('password', '')

        if self.phone_obj.phone_obj in ('Mitel6865i', 'Mitel6910'):
            logger.warn("NOT DOING ANYTHING HERE!!")
        else:
            for _ in range(2):
                self.phone_obj.press_key('ScrollLeft')
            if eapType == 'False':
                eapType = 'Disabled'
            elif eapType == 'EAP-MD5':
                self.phone_obj.press_key('ScrollRight')
            elif eapType == 'EAP-TLS':
                self.phone_obj.press_key('ScrollRight')
                self.phone_obj.press_key('ScrollRight')
            else:
                raise Exception("INVALID EAP-TYPE ({}) PASSED!!".format(eapType))

            self.phone_obj.press_key('ScrollDown')
            self.enterString(identity)
            self.phone_obj.press_key('ScrollDown')
            self.enterString(password)
            self.phone_obj.press_softkey(1)
            self.phone_obj.press_key('ScrollLeft')
            self.phone_obj.press_key('Enter')
            self.phone_obj.phone_obj.WaitTillPhoneComesOnline(300)

    def changeLLDPSettings(self, lldpStatus):
        """
        This method is used to change the LLDP settings on the phone.
        :args:
            lldpStatus:  LLDP status to apply on phone i.e., enable/disable

        :returns: None
        :created by: Vikhyat Sharma
        :creation date: 18/12/2020
        :last update by:
        :last update date:
        """
        lldpStatus = int(lldpStatus)
        self.verifyDisplayMessageUtil('LLDP')
        for _ in range(2):
            self.phone_obj.press_key('ScrollDown')

        if not lldpStatus:
            self.phone_obj.press_key('ScrollUp')

        self.phone_obj.press_key('Enter')
        if self.phone_obj.phone_type in ('Mitel6865i', 'Mitel6910'):
            raise Exception("ADD CONDITION TO RESTART THE PHONE AFTER CHANGING LLDP.")
        else:
            self.phone_obj.press_key('ScrollLeft')
            self.phone_obj.press_key('Enter')

    def directoryActionsForTelepo(self, **kwargs):
        """
        This method performs search related actions in the directory of the phone.

        Args:
            self: PhoneComponent Object of the phone to search on.
        Keyword Args:
            phoneObj: PhoneComponent object of the phone to search
            directoryAction: Action to perform i.e., default/searchOnly/searchWithDial/searchMultiple

        :returns: None
        :created by: Vikhyat Sharma
        :creation date: 17/12/2019
        :last updated by:
        :last update date:
        """
        phoneObj = kwargs['phoneObj']
        directoryAction = kwargs['directoryAction']

        if isinstance(phoneObj, PhoneComponent):
            phoneToSearch = phoneObj.phone_obj.phone_obj.phone.extensionNumber
            phoneName = phoneObj.phone_obj.phone_obj.phone.phoneName
        else:
            raise Exception("THE PASSED PHONE IS NOT A PHONECOMPONENT OBJECT!!")

        logger.info("Searching number: <b>{}</b> with name: <b>{}</b> on extension: <b>{}</b>".format(phoneToSearch,
                    phoneName, self.phone_obj.phone_obj.phone.extensionNumber))
        console("Searching number: {} with name: {} on extension: {}".format(phoneToSearch, phoneName,
                self.phone_obj.phone_obj.phone.extensionNumber))

        if self.phone_obj.phone_type == 'Mitel6865i':
            self.phone_obj.press_key('ProgramKey8')
            self.phone_obj.sleep(5)
            for _ in range(3):
                self.phone_obj.press_key('ScrollDown')
            self.phone_obj.press_key('Enter')
        else:
            self.phone_obj.press_key('Directory')

        self.phone_obj.sleep(2)
        if self.phone_obj.phone_type in ('Mitel6865i', 'Mitel6910'):
            self.verifyDisplayMessageUtil('Enter search query')
            self.enterString(phoneToSearch)
            self.phone_obj.press_key('ScrollDown')
            self.phone_obj.sleep(3)
            self.phone_obj.press_key('ScrollDown')
            self.phone_obj.press_key('ScrollDown')

        else:
            self.verifyDisplayMessage(message='Directory Search', pbx='Telepo')

            # changing the input type from ABC to 123
            self.phone_obj.press_softkey(3)
            self.phone_obj.press_softkey(3)

            self.phone_obj.input_a_number(phoneToSearch)
            if self.phone_obj.phone_type == 'Mitel6930':
                self.phone_obj.press_softkey(4)
            elif self.phone_obj.phone_type == 'Mitel6867i':
                self.phone_obj.press_softkey(4)
                self.phone_obj.sleep(2)
                self.phone_obj.press_softkey(3)
            else:
                raise Exception("ADD SUPPORT FOR SEARCHING NUMBER IN " + self.phone_obj.phone_type)
            self.phone_obj.sleep(3)
        self.verifyDisplayMessage(message='Search Result', pbx='Telepo')

        if directoryAction in ('searchWithDial', 'searchOnly'):
            self.verifyDisplayMessage(message=phoneName, pbx='Telepo')
            if directoryAction == 'searchWithDial':
                if self.phone_obj.phone_type in ('Mitel6865i', 'Mitel6910'):
                    self.phone_obj.press_key('Enter')
                else:
                    self.phone_obj.press_softkey(1)
                self.phone_obj.sleep(3)
        else:
            raise Exception("UNSUPPORTED DIRECTORY ACTION {} PASSED!!".format(directoryAction))

    def verifyConferenceDisplay(self, **kwargs):
        """
        This method is used to verify conference display on the phone.

        Keyword Args:
            numberOfParties: Number of Parties in conference
            pbx: Call Manager of the phone

        :returns: None
        :created by: Vikhyat Sharma
        :creation date: 20/12/2020
        :last update by:
        :last update date:
        """
        numberOfParties = kwargs['numberOfParties']
        pbx = kwargs['pbx']

        conferenceDisplayMsg = ''
        softkeysToVerify = ['Drop', 'Leave']

        if numberOfParties.isdigit():
            numberOfParties = int(numberOfParties)
            if self.phone_obj.phone_type in ('Mitel6865i', 'Mitel6910'):
                conferenceDisplayMsg = 'Conference({})'.format(numberOfParties - 1)
            else:
                if numberOfParties > 3:
                    softkeysToVerify.append('Show')
                    softkeysToVerify.remove('Leave')
                    conferenceDisplayMsg = 'Conferenced {} calls'.format(numberOfParties-1)

            if conferenceDisplayMsg:
                self.verifyDisplayMessageUtil(conferenceDisplayMsg)
            for keys in softkeysToVerify:
                self.verifyDisplayMessage(message=keys, pbx=pbx)
        else:
            raise Exception("INVALID NUMBER OF PARTIES PASSED!! ACCEPTS DIGITS ONLY BUT PASSED-", numberOfParties)

    def verifyToneIsPlayed(self,**kwargs):
        """
        This method is used to check speciifc tone is played on phone
        :param:
                :Type of tone to verify
        :return: None

        :created by: Mpatil
        :creation date: 30/11/2020
        :last update date:
        :last updated by:
        """
        import datetime

        toneType = kwargs['toneType']
        negativeValidation=bool(kwargs.get('negativeValidation',False))
        toneValue=None
        timeout=15
        logger.info("Verifying '"+toneType+"' tone is played on Extension : "+self.phone_obj.phone_obj.phone.extensionNumber, also_console=True)

        if toneType=='Ringing':
            toneValue=[2]
        elif toneType=='Dial':
            toneValue=[0]
        elif toneType=='CallWaiting':
            toneValue=[5,6,7,8,9]
        elif toneType=="Busy":
            toneValue = [3]
        elif toneType=="DTMF":
            toneValue = [0]
            timeout=2
        else:
            raise Exception("Invalid Tone Type Passed !!")

        endTime = datetime.datetime.now() + datetime.timedelta(seconds=timeout)
        status = False
        while True:
            currentToneValue=int(self.phone_obj.get_tone_at_phone())
            logger.info("Current tone value"+str(currentToneValue),also_console=True)
            if currentToneValue in toneValue:
                status=True
                break
            if datetime.datetime.now() >= endTime:
                break

        logger.info("Negative vlidation -"+str(negativeValidation),also_console=True)
        logger.info("Status -" + str(status), also_console=True)

        if not negativeValidation:
            if status == True:
                logger.info(toneType + " Tone is played on extension " + self.phone_obj.phone_obj.phone.extensionNumber)
            else:
                raise Exception(toneType + " Tone is Not played on extension " + self.phone_obj.phone_obj.phone.extensionNumber)
        else:
            if status == False:
                logger.info(toneType + " Tone is not plyed on extension " + self.phone_obj.phone_obj.phone.extensionNumber)
            else:
                raise Exception(toneType + " Tone is played on extension " + self.phone_obj.phone_obj.phone.extensionNumber)

    def pressDTMFKeyAndVerifyToneIsPlayed(self,**kwargs):
        """
         This method is used to check speciifc tone is played on phone
         :param:
               : Phone object on which want to verify tone
         :return: None

         :created by: Mpatil
         :creation date: 30/11/2020
         :last update date:
         :last updated by:
         """
        phoneObj = kwargs['phoneObj']
        dtmfKey = kwargs['dtmfKey']
        longPressKey = bool(kwargs.get("longPressDTMFkey",False))
        negativeValidation=bool(kwargs.get("negativeValidation",False))

        if self is phoneObj:
            if longPressKey:
                logger.info("Long Pressing DTMF key : "+dtmfKey+" on extension : "+self.phone_obj.phone_obj.phone.extensionNumber,also_console=True)
                self.longPressKey(key_to_be_pressed=dtmfKey)
            else:
                logger.info("Pressing DTMF key : " + dtmfKey + " on extension : " + self.phone_obj.phone_obj.phone.extensionNumber,also_console=True)
                self.phone_obj.press_key(dtmfKey)
            self.verifyToneIsPlayed(toneType="DTMF",negativeValidation=negativeValidation)
        else:
            if longPressKey:
                logger.info("Long Pressing DTMF key : "+dtmfKey+" on extension : "+self.phone_obj.phone_obj.phone.extensionNumber,also_console=True)
                self.longPressKey(key_to_be_pressed=dtmfKey)
            else:
                logger.info("Pressing DTMF key : " + dtmfKey + " on extension : " + self.phone_obj.phone_obj.phone.extensionNumber,also_console=True)
                self.phone_obj.press_key(dtmfKey)
            phoneObj.verifyToneIsPlayed(toneType="DTMF",negativeValidation=negativeValidation)

    def pressSoftkeyInDiagnosticSettingState(self, **kwargs):
        """
        This method presses the available softkeys in the Diagnostic settings menu option.
        :param:
            :self: PhoneComponent object
            :softKey: softkey to press i.e., Upload/Close/Backspace/Save

        :return: None
        :created by : Milind
        :creation date: 21/12/2020
        :updated by :
        :last update date :
        """

        if len(kwargs) >= 1:
            softkey = kwargs["softKey"]
            option = kwargs["option"]

            logger.info("Pressing key: <b>" + softkey + "</b> in <b> "+option+" </b> of Diagnostic settings", html=True)
            console("Pressing key: <b>" + softkey + "</b> in <b> "+option+" </b> of Diagnostic settings")

            if option == "log_upload":
                if softkey == "Upload":
                    if self.phone_obj.phone_type == "Mitel6920":
                        self.phone_obj.press_softkey(3)
                    elif self.phone_obj.phone_type == "Mitel6930":
                        self.phone_obj.press_softkey(4)
                    elif self.phone_obj.phone_type == "Mitel6910":
                        self.phone_obj.press_key("ScrollRight")

                elif softkey == "Close":
                    if self.phone_obj.phone_type == "Mitel6920":
                        self.phone_obj.press_softkey(4)
                    elif self.phone_obj.phone_type == "Mitel6930":
                        self.phone_obj.press_softkey(5)
                    elif self.phone_obj.phone_type == "Mitel6910":
                        self.phone_obj.press_key("GoodBy")
                else:
                    raise Exception("Please check the softkey passed. Softkey : " + softkey + " is not present on display.")

            elif option == "diagnostic_server":
                if softkey == "Backspace":
                    if self.phone_obj.phone_type == "Mitel6920":
                        self.phone_obj.press_softkey(1)
                    elif self.phone_obj.phone_type == "Mitel6930":
                        self.phone_obj.press_softkey(2)
                    elif self.phone_obj.phone_type == "Mitel6910":
                        self.phone_obj.press_key("ScrollLeft")
                elif softkey == "Save":
                    if self.phone_obj.phone_type == "Mitel6920":
                        self.phone_obj.press_softkey(4)
                        self.phone_obj.press_softkey(1)
                    elif self.phone_obj.phone_type == "Mitel6930":
                        self.phone_obj.press_softkey(1)
                    elif self.phone_obj.phone_type == "Mitel6910":
                        self.phone_obj.press_key("ScrollRight")

                elif softkey == "Cancel":
                    if self.phone_obj.phone_type == "Mitel6920":
                        self.phone_obj.press_softkey(4)
                        self.phone_obj.press_softkey(3)
                    elif self.phone_obj.phone_type == "Mitel6930":
                        self.phone_obj.press_softkey(5)
                    elif self.phone_obj.phone_type == "Mitel6910":
                        self.phone_obj.press_key("GoodBye")
                else:
                    raise Exception("Please check the softkey passed. Softkey : "+softkey+" is not present on display.")

        else:
            raise Exception("Please check the arguments passed: %s" % kwargs)

    def clearDiagnosticServerIp(self, **kwargs):
        """
        This method is used to clear the diagnostic server ip.
        :param:
            :self: PhoneComponent object

        :return: None
        :created by : Milind
        :creation date: 21/12/2020
        :updated by :
        :last update date :
        """
        logger.info("Removing diagnostic server ip address if already configured, from extesion : <b>"+self.phone_obj.phone_obj.phone.extensionNumber+"</b>", html=True)
        console("Removing diagnostic server ip address if already configured, from extesion : <b>" + self.phone_obj.phone_obj.phone.extensionNumber)


        for i in range(23):
            self.pressSoftkeyInDiagnosticSettingState(softKey="Backspace",option="diagnostic_server")

    def verifyMessageDisplayedOnPhone(self, **kwargs):
        """
        This method is used to verify message is displayed on phone within specidified amount of timie.
        :param:
            :self: PhoneComponent object
            :time : wait timeout in seconds
        """
        import datetime
        timeout = int(kwargs["timeInSeconds"])
        message = kwargs["message"]
        status = False

        if self.phone_obj.phone_type=="Mitel6910" and message == "Logs uploaded successfully":
            time.sleep(timeout)
            return
        waitTime = datetime.datetime.now() + datetime.timedelta(seconds=timeout)
        status = False
        while True:
            if self.phone_obj.verify_display_message_contents(message):
                status = True
                break
            if datetime.datetime.now() >= waitTime:
                break
        if status:
            logger.info("Message : <b>%s" % message + "</b> Verified on extension " + self.phone_obj.phone_obj.phone.extensionNumber,html=True)
        else:
            raise Exception("Message : %s" % message + " not verified on " + self.phone_obj.phone_type
                            + " with extension " + self.phone_obj.phone_obj.phone.extensionNumber + " and IP: "
                            + self.phone_obj.phone_obj.phone.ipAddress)

    def verifyLogFileIsDownloadedOnServer(self, **kwargs):
        """
        This method is used to verify message is displayed on phone within specidified amount of timie.
        :param:
            :self: PhoneComponent object
            :connection : To specify what type of connection i.e ftp/http/tftp
        """
        connection = str(kwargs.get('connection', 'FTP'))

        status=False
        logFileName=""
        if connection == "FTP":
            from ftplib import FTP
            import os
            ftp = FTP()
            ftp.set_debuglevel(2)
            ftp.connect(Ftpserver, FtpPort)
            ftp.login(FtpUser, FtpPass)
            filesList=ftp.nlst()
            for file in filesList:
                expectedFileExtension = 'tgz'
                fileExtension = file.split('.')
                if fileExtension[-1] == expectedFileExtension:
                    status=True
                    logFileName=file
            ftp.quit()

        elif connection == "HTTP":
            import pysftp
            sftp = pysftp.Connection(host=httpServer, username="root", password="Jafe@20_20")
        elif connection == "TFTP":
            import os
            for file in os.listdir("C:\TFTP-Root"):
                filExtension = file.split('.')
                if filExtension[-1] == "tgz":
                    status = True
                    logFileName = file

        if status:
            logger.info("Log file : "+logFileName+" is uploaded successfully on : "+connection+" Server.")
        else:
            raise Exception("Failed to upload log file to : "+connection+" Server.")

    def enterUrlPrefixInDiagnosticServerUrl(self, **kwargs):
        """
        This method is used to enter protocole in diagnostic server url.
        :param:
            :self: PhoneComponent object
            :connection : To specify what type of connection i.e http/tftp
        """
        connection = str(kwargs.get('connection', ''))
        logger.info("Entering url perefix as : "+connection.lower())
        if self.phone_obj.phone_type == "Mitel6920":
            self.phone_obj.press_softkey(3)
            self.phone_obj.press_softkey(3)
        elif self.phone_obj.phone_type == "Mitel6930":
            self.phone_obj.press_softkey(4)
            self.phone_obj.press_softkey(4)
        if connection == "HTTP":
            if self.phone_obj.phone_type in ("Mitel6920", "Mitel6930"):
                self.phone_obj.input_a_number('44')
                time.sleep(1)
                self.phone_obj.input_a_number('8')
                time.sleep(1)
                self.phone_obj.input_a_number('8')
                time.sleep(1)
                self.phone_obj.input_a_number('7')
                time.sleep(1)
                self.phone_obj.input_a_number('111')
                time.sleep(1)
                self.phone_obj.input_a_number('##')
                time.sleep(1)
                self.phone_obj.input_a_number('##')
            elif self.phone_obj.phone_type == "Mitel6910":
                self.phone_obj.input_a_number('444')
                time.sleep(1)
                self.phone_obj.input_a_number('88')
                time.sleep(1)
                self.phone_obj.input_a_number('88')
                time.sleep(1)
                self.phone_obj.input_a_number('77')
                time.sleep(1)
                self.phone_obj.input_a_number('111')
                time.sleep(1)
                self.phone_obj.input_a_number('##')
                time.sleep(1)
                self.phone_obj.input_a_number('##')

        elif connection == "TFTP":
            if self.phone_obj.phone_type in ("Mitel6920","Mitel6930"):
                self.phone_obj.input_a_number('8')
                time.sleep(1)
                self.phone_obj.input_a_number('333')
                time.sleep(1)
                self.phone_obj.input_a_number('8')
                time.sleep(1)
                self.phone_obj.input_a_number('7')
                time.sleep(1)
                self.phone_obj.input_a_number('111')
                time.sleep(1)
                self.phone_obj.input_a_number('##')
                time.sleep(1)
                self.phone_obj.input_a_number('##')
            elif self.phone_obj.phone_type == "Mitel6910":
                self.phone_obj.input_a_number('88')
                time.sleep(1)
                self.phone_obj.input_a_number('3333')
                time.sleep(1)
                self.phone_obj.input_a_number('88')
                time.sleep(1)
                self.phone_obj.input_a_number('77')
                time.sleep(1)
                self.phone_obj.input_a_number('111')
                time.sleep(1)
                self.phone_obj.input_a_number('##')
                time.sleep(1)
                self.phone_obj.input_a_number('##')

        else:
            raise Exception("Invalid Url prefix provided")

    def deleteExistingLogFileFromServer(self, **kwargs):
        """
        This method is used to enter protocole in diagnostic server url.
        :param:
            :self: PhoneComponent object
            :connection : To specify what type of connection i.e http/tftp
        """
        connection = str(kwargs.get('connection', ''))
        if connection == "FTP":
            from ftplib import FTP
            import os
            ftp = FTP()
            ftp.set_debuglevel(2)
            ftp.connect(Ftpserver, FtpPort)
            ftp.login(FtpUser, FtpPass)
            filesList=ftp.nlst()
            for file in filesList:
                expectedFileExtension = 'tgz'
                fileExtension = file.split('.')
                if fileExtension[-1] == expectedFileExtension:
                    ftp.delete(file)
            ftp.quit()

        elif connection == "TFTP":
            import os
            for file in os.listdir("C:\TFTP-Root"):
                filExtension=file.split('.')
                if filExtension[-1] == "tgz":
                    logger.info("Removing fie: " + file)
                    logFilepath = os.path.join("C:\TFTP-Root", file)
                    os.remove(logFilepath)

    def getThisMachineIp(self, **kwargs):
        """
        This method is used to get this machine ip address.
        :param:
            :self: PhoneComponent object
        """
        import socket
        hostname = socket.gethostname()
        local_ip = socket.gethostbyname(hostname)
        return local_ip

    def enterDiagnosticServerIp(self, **kwargs):
        """
        This method is used to clear the diagnostic server ip.
        :param:
            :self: PhoneComponent object

        :return: None
        :created by : Milind
        :creation date: 21/12/2020
        :updated by :
        :last update date :
        """
        serverIp=kwargs['serverIp']

        logger.info("Entering diagnostic server ip as : "+serverIp)
        for num in serverIp:
            self.phone_obj.input_a_number(num)
            time.sleep(1)

    def press_transfer(self):
        self.phone_obj.press_softkey(3)

if __name__ == "__main__":
    phone_details1 = {"phoneModel": "Mitel6930", "ipAddress": "10.211.22.240", "extensionNumber": "3001",
                      "phoneName": "3001"}
    obj1 = PhoneComponent(**phone_details1)
   # obj1.setBackgroundImage(server='HTTP', typeOfImage='Custom')
   # print(obj1.phone_obj.press_softkey('line1'))
   # obj1.phone_obj.pressHardKey(sys.modules['PhoneHandler'].HardPhone.Keys.IncreaseVolume)
    obj1.openRedialList()
    phoneObj = "User3000"
    obj1.redialNumber(phoneObj)

  #  time.sleep(30)
   # obj1.phone_obj.press_softkey(1)
   #  obj1.phone_obj.press_key("ScrollUp")
   #  time.sleep(30)
    obj1.disconnectTerminal()
