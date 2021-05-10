import os
from robot.libraries.BuiltIn import BuiltIn
from robot.libraries.Collections import Collections
from robot.api import logger
import psutil
import shutil
import csv
from os import listdir, rmdir, remove
import json
import sys
import re
from sys import platform as _platform
from robot.api.logger import console

OS_CONFIG_PATH = ""

class CSVReader(object):
    ROBOT_LIBRARY_SCOPE = 'TEST CASE'

    def __init__(self, csv_file_name, project_folder_name=None):
        global OS_CONFIG_PATH        
        logger.warn("Entering INIT")
        # self._robot_runmodule_dir = r"..\..\Configuration"
        # self.load_configuration_parameters()
        if os.path.isfile(csv_file_name):
            self.load_shoretel_users(csv_file_name)
        else:
            self.load_shoretel_users(csv_file_name, project_folder_name)

    def load_robot_automation_configs(self, auto_project = "TwW"):
        global OS_CONFIG_PATH
        auto_project = BuiltIn().get_variable_value("${AUTOMATION_PROJECT}")

        if auto_project == "GSuite":
            self.load_testbed_config()
            self.load_google_contacts()
            is_mt = BuiltIn().get_variable_value('${is_runtype_mt}')
            if is_mt == "true":
                console("Skipping HQ2 user creation for MT run")
            else:
                self.load_shoretel_hq2_users()
        else:
            logger.error("Automation project %s was not found in %s\\%s" % (auto_project, OS_CONFIG_PATH,self._robot_runmodule_dir))


    def load_shoretel_users(self, csv_file_name, project_folder_name=None):
        """Load shoretel user attributes"""
        # Make all users visible to robot
        global OS_CONFIG_PATH        
        filename = csv_file_name
        # filename = OS_CONFIG_PATH + self._robot_runmodule_dir +  '\\configuration.csv'        ## in connect client used this location
        if project_folder_name:
            filename = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), project_folder_name, "Variables", csv_file_name)
        
        logger.info("Loading hq users from config file %s " % filename)
        with open(filename) as f_in:
            lines = (line.rstrip() for line in f_in)
            lines = list(line for line in lines if line)  # Non-blank lines in a list
        numPhones = -1
        for line in lines:
            numPhones += 1
            print(numPhones)
        reader = csv.DictReader(open(filename))
        userDict = {}
        for row in reader:
            for column, value in row.iteritems():
                userDict.setdefault(column, []).append(value)

        users_list = []
        for i in range(0, int(numPhones)):
            userNum = i
            user_name = 'first_name=%s' % userDict["user_name"][userNum]
            user_type = 'user_type=%s' % userDict["user_type"][userNum]
            first_name = 'first_name=%s' % userDict["first_name"][userNum]
            middle_name = 'middle_name=%s' % userDict["middle_name"][userNum]
            last_name = 'last_name=%s' % userDict["last_name"][userNum]
            extension = 'extension=%s' % userDict["extension"][userNum]
            client_id = 'client_id=%s' % userDict["client_id"][userNum]
            client_email = 'client_email=%s' % userDict["client_email"][userNum]
            client_password = 'client_password=%s' % userDict["client_password"][userNum]
            ip = 'ip=%s' % userDict["ip"][userNum]
            mac = 'mac=%s' % userDict["mac"][userNum]
            phone_type = 'phone_type=%s' % userDict["phone_model"][userNum]
            server = 'server=%s' % userDict["server"][userNum]
            home = 'home=%s' % userDict["home"][userNum]
            work = 'work=%s' % userDict["work"][userNum]
            fax = 'fax=%s' % userDict["fax"][userNum]
            mobile = 'mobile=%s' % userDict["mobile"][userNum]
            pager = 'pager=%s' % userDict["pager"][userNum]
            sip_did = 'sip_did=%s' % userDict["sip_trunk_did"][userNum]
            pri_dnis = 'pri_dnis=%s' % userDict["pri_trunk_dnis"][userNum]
            vm_password = 'vm_password=%s' % userDict["vm_password"][userNum]
            sip_password = 'sip_password=%s' % userDict["sip_password"][userNum]
            tenant_id = 'tenant_id=%s' % userDict["tenant_id"][userNum]
            robot_address = 'robot_address=%s' % userDict["robot_address"][userNum]
            telnet_id = 'telnet_id=%s' % userDict["telnet_id"][userNum]
            company = 'company=%s' % userDict["company"][userNum]
            cas_session_id = 'cas_session_id=%s' % userDict["cas_session_id"][userNum]
            hq_username = 'hq_username=%s' % userDict["hq_username"][userNum]
            hq_password = 'hq_password=%s' % userDict["hq_password"][userNum]
            client_link = 'client_link=%s' % userDict["client_link"][userNum]
            user_factory = BuiltIn().create_dictionary(ip, extension, server,
                                                       phone_type, user_type, mac, first_name, middle_name,
                                                       last_name, home, work,
                                                       fax, mobile, pager,
                                                       sip_did, pri_dnis, client_password,
                                                       vm_password, sip_password, client_id,
                                                       client_email, tenant_id, robot_address,
                                                       telnet_id, company,cas_session_id,hq_username,hq_password,client_link)

            print("USER %s" % user_factory)
            phoneNum = userNum + 1
            varname = '${user0%s}' % phoneNum
            BuiltIn().set_global_variable(varname, user_factory)
            
            if "none" not in phone_type:
                pass
        
    def load_configuration_parameters(self):
        """Load configuration parameters"""
        # Make all users visible to robot
        global OS_CONFIG_PATH
        filename = ""
        filename = OS_CONFIG_PATH + self._robot_runmodule_dir + '\\configuration.csv'

        logger.info("Loading configuration from config file %s " % filename)
        with open(filename) as f_in:
            lines = (line.rstrip() for line in f_in)
            lines = list(line for line in lines if line)  # Non-blank lines in a list
        numPhones = -1
        for line in lines:
            numPhones += 1
            print(numPhones)

        reader = csv.DictReader(open(filename))
        userDict = {}
        for row in reader:
            for column, value in row.iteritems():
                userDict.setdefault(column, []).append(value)

        users_list = []       
        user_provision = 'user_provision=%s' % userDict["user_provision"][0]
        parallel_execution = 'parallel_execution=%s' % userDict["parallel_execution"][0]

        user_factory = BuiltIn().create_dictionary(user_provision, parallel_execution)

        print("USER %s" % user_factory)
        varname = '${conf}'
        BuiltIn().set_suite_variable(varname, user_factory)
