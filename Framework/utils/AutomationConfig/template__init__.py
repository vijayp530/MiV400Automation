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
import tempfile

DOWNLOADS_PATH = r'C:\Users\Administrator\Downloads'
GAPPS_BUILD_PATH = r'C:\WFDevGCAL\automation-gapps\builds'
GAPPS_PATH = r'C:\WFDevGCAL\automation-gapps\lib'

WIN_ATF_CONFIG_PATH = "C:\\ATF_ROBOT\\run\\GSuite\\configs\\"
WIN_ATF_LOG_PATH = "C:\\ATF_ROBOT\\run\\GSuite\\logs\\"
MAC_ATF_CONFIG_PATH = "populate_me"
LINUX_ATF_CONFIG_PATH = "populate_me"
OS_CONFIG_PATH = ""

auto_project_list = ['gsuite','boss','teamweb','teamios','mnm']
# mvilleda - Automation Test
class AutomationConfig(object):
    ROBOT_LIBRARY_SCOPE = 'GLOBAL'
    # ROBOT_LIBRARY_VERSION = VERSION

    def __init__(self):
        global OS_CONFIG_PATH
        
        # try:
        self._robot_runmodule_dir = BuiltIn().get_variable_value('${ROBOT_RUNMODULE_DIR}')
        if self._robot_runmodule_dir == "None":
            raise Exception("var: _robot_runmodule_dir is %s " % self._robot_runmodule_dir)
        
        logger.warn("Loading %s " % self._robot_runmodule_dir)
        # global ROBOT_RUNMODULE_DIR
        print("DEBUG: In AutomationConfig init ***")
        if _platform == "linux" or _platform == "linux2":
            # linux
            OS_CONFIG_PATH = LINUX_ATF_CONFIG_PATH
        elif _platform == "darwin":
            OS_CONFIG_PATH = MAC_ATF_CONFIG_PATH
            # OS X
        elif _platform == "win32":
            # Windows...
            OS_CONFIG_PATH = WIN_ATF_CONFIG_PATH

        logger.warn("Loading %s robot parameters from %s\\%s: STARTED" % (_platform,OS_CONFIG_PATH,self._robot_runmodule_dir))
        self.load_robot_automation_configs()
        logger.warn("Loading %s robot parameters from %s\\%s: COMPLETE" % (_platform,OS_CONFIG_PATH,self._robot_runmodule_dir))

    def load_phone_users(self):
        """
            Load Phone user attributes
            Make all users visible to robot
        """
        # self.OS_CONFIG_PATH
        self.available_phones = 0
        row_index = 0
        user_index = 0
        users_list = []
        user_dict = {}

        # TODO remove hard code path 
        logger.info("Loading phone users cfg file %s " % self.user_cfg_file)

        reader = csv.DictReader(open(self.user_cfg_file))
        for row in reader:
            for column, value in iter(row.items()):
                user_dict.setdefault(column, []).append(value)

        for is_avail in user_dict['is_available']:
            if is_avail.lower() == "true":
                self.available_phones += 1
                users_list.append(row_index)
            row_index += 1
        
        for i in users_list:
            tmp_user_dict = {}
            user_index += 1
            varname = '${user0%s}' % user_index
            
            for key in user_dict.keys():
                tmp_user_dict[key] = user_dict[key][i]

        self.create_suite_variable(varname, tmp_user_dict)
        logger.warn("Created user \"%s\" as dict %s" % (varname, tmp_user_dict))
            
    def load_robot_automation_configs(self):
        global OS_CONFIG_PATH
        auto_project = BuiltIn().get_variable_value("${AUTOMATION_PROJECT}").lower()

        logger.warn("project: %s" % auto_project)

        for project in auto_project.split(','):
            if project not in auto_project_list:

                logger.error("project \"%s\" not in automation project list %s" % (project,auto_project_list))
                sys.exit()
        if "gsuite" in auto_project:
            logger.warn("Loading GSUITE configs...")
            self.load_testbed_config()
            self.load_shoretel_users()
            self.load_google_contacts()
            is_mt = BuiltIn().get_variable_value('${is_runtype_mt}')
            if is_mt == "true":
                logger.warn("Skipping HQ2 user creation for MT run")
            else:
                self.load_shoretel_hq2_users()

    def load_testbed_config(self):
        """Load testbed attributes"""
        # Make all users visible to robot
        global OS_CONFIG_PATH
        filename = ""
        is_mt = BuiltIn().get_variable_value('${is_runtype_mt}')
        if is_mt == "true":
            filename = OS_CONFIG_PATH + self._robot_runmodule_dir + '\\mt_testbed.cfg'
        else:
            filename = OS_CONFIG_PATH + self._robot_runmodule_dir +  '\\testbed.cfg'

        logger.info("Loading testbed configuration from config file %s " % filename)
        testbedDict = {}
        numItems = 0
        with open(filename, 'r') as f:
            for line in f:
                line = line.rstrip() #removes trailing whitespace and '\n' chars

                if "=" not in line: continue #skips blanks and comments w/o =
                if line.startswith("#"): continue #skips comments which contain =

                numItems = numItems+1
                k, v = line.split("=", 1)
                # logger.warn("num %s numItems:: col %s     val %s" % (numItems,k,v))
                testbedDict[k.strip()] = v.strip()

        logger.info('testbed keys %s' % testbedDict.keys())
        numTestbeds = 1

        users_list = []
        for i in range(0, int(numTestbeds)):
            tbNum = i
            #TEMPLATE_START
            #TEMPLATE_REPLACE1
            #TEMPLATE_REPLACE2
            #TEMPLATE_END

            # logger.warn("TESTBED %s" % testbed_factory)
            testbedNum = tbNum + 1
            varname = '${testbed0%s}' % testbedNum
            BuiltIn().set_suite_variable(varname, testbed_factory)

    def load_shoretel_users(self):
        """Load shoretel user attributes"""
        # Make all users visible to robot
        global OS_CONFIG_PATH
        filename = ""
        is_mt = BuiltIn().get_variable_value('${is_runtype_mt}')
        if is_mt == "true":
            filename = OS_CONFIG_PATH + self._robot_runmodule_dir +  '\\pphone_mt_userInfo.csv'
        else:
            filename = OS_CONFIG_PATH + self._robot_runmodule_dir +  '\\pphone_st_hq1_userInfo.csv'

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
            google_password = 'google_password=%s' % userDict["google_password"][userNum]
            company = 'company=%s' % userDict["company"][userNum]
            cas_session_id = 'cas_session_id=%s' % userDict["cas_session_id"][userNum]
            hq_username = 'hq_username=%s' % userDict["hq_username"][userNum]
            hq_password = 'hq_password=%s' % userDict["hq_password"][userNum]

            user_factory = BuiltIn().create_dictionary(ip, extension, server,
                                                       phone_type, user_type, mac, first_name, middle_name,
                                                       last_name, home, work,
                                                       fax, mobile, pager,
                                                       sip_did, pri_dnis, client_password,
                                                       vm_password, sip_password, client_id,
                                                       client_email, tenant_id, robot_address,
                                                       google_password, company,cas_session_id,hq_username,hq_password)

            print("USER %s" % user_factory)
            phoneNum = userNum + 1
            if phoneNum < 10:
                varname = '${user0%s}' % phoneNum
            else:
                varname = '${user%s}' % phoneNum

            BuiltIn().set_suite_variable(varname, user_factory)
            

    def load_shoretel_hq2_users(self):
        """Load shoretel hq2 user attributes"""
        # Make all users visible to robot
        global OS_CONFIG_PATH
        filename = ""
        is_mt = BuiltIn().get_variable_value('${is_runtype_mt}')
        filename = OS_CONFIG_PATH + self._robot_runmodule_dir +  '\\pphone_st_hq2_userInfo.csv'

        logger.info("Loading hq2 users from config file %s " % filename)
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

            user_factory = BuiltIn().create_dictionary(ip, extension, server,
                                                       phone_type, user_type, mac, first_name, middle_name,
                                                       last_name, home, work,
                                                       fax, mobile, pager,
                                                       sip_did, pri_dnis, client_password,
                                                       vm_password, sip_password, client_id,
                                                       client_email, tenant_id, robot_address,
                                                       telnet_id, company)

            print("USER %s" % user_factory)
            phoneNum = userNum + 1
            if phoneNum < 10:
                varname = '${hq2_user0%s}' % phoneNum
            else:
                varname = '${hq2_user%s}' % phoneNum

            BuiltIn().set_suite_variable(varname, user_factory)

    def load_boss_users(self):
        """Load boss user attributes"""
        # Make all users visible to robot
        global OS_CONFIG_PATH
        is_mt = BuiltIn().get_variable_value('${is_runtype_mt}')
        filename = OS_CONFIG_PATH + self._robot_runmodule_dir +  '\\boss_userInfo.csv'

        logger.info("Loading boss users from config file %s " % filename)
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

            user_factory = BuiltIn().create_dictionary(ip, extension, server,
                                                       phone_type, user_type, mac, first_name, middle_name,
                                                       last_name, home, work,
                                                       fax, mobile, pager,
                                                       sip_did, pri_dnis, client_password,
                                                       vm_password, sip_password, client_id,
                                                       client_email, tenant_id, robot_address,
                                                       telnet_id, company,cas_session_id,hq_username,hq_password)

            print("boss USER %s" % user_factory)
            # if userNum > 1:
            # break
            #  TODO varname only allows ten users. Increase user num
            phoneNum = userNum + 1
            varname = '${boss0%s}' % phoneNum
            logger.warn("Creating boss user dict \"%s\"" % varname)
            BuiltIn().set_suite_variable(varname, user_factory)
            
        logger.info("boss  config loaded!")


    def load_teamweb_users(self):
        """Load teamweb user attributes"""
        pass
        # Make all users visible to robot
        global OS_CONFIG_PATH
        filename = ""
        is_mt = BuiltIn().get_variable_value('${is_runtype_mt}')
        if is_mt == "true":
            filename = OS_CONFIG_PATH + self._robot_runmodule_dir +  '\\teamweb_mt_userInfo.csv'
        else:
            filename = OS_CONFIG_PATH + self._robot_runmodule_dir +  '\\teamweb_st_userInfo.csv'

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

            user_factory = BuiltIn().create_dictionary(ip, extension, server,
                                                       phone_type, user_type, mac, first_name, middle_name,
                                                       last_name, home, work,
                                                       fax, mobile, pager,
                                                       sip_did, pri_dnis, client_password,
                                                       vm_password, sip_password, client_id,
                                                       client_email, tenant_id, robot_address,
                                                       telnet_id, company,cas_session_id,hq_username,hq_password)

            print("teamweb USER %s" % user_factory)
            # if userNum > 1:
            # break
            #  TODO varname only allows ten users. Increase user num
            phoneNum = userNum + 1
            varname = '${teamweb0%s}' % phoneNum
            logger.info("Creating teamweb user dict \"%s\"" % varname)
            BuiltIn().set_suite_variable(varname, user_factory)
        logger.info("teamweb config loaded!")


    def load_teamios_users(self):
        """Load teamios user attributes"""
        pass
        # Make all users visible to robot
        global OS_CONFIG_PATH
        filename = ""
        is_mt = BuiltIn().get_variable_value('${is_runtype_mt}')
        if is_mt == "true":
            filename = OS_CONFIG_PATH + self._robot_runmodule_dir +  '\\teamios_mt_userInfo.csv'
        else:
            filename = OS_CONFIG_PATH + self._robot_runmodule_dir +  '\\teamios_st_userInfo.csv'

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

            user_factory = BuiltIn().create_dictionary(ip, extension, server,
                                                       phone_type, user_type, mac, first_name, middle_name,
                                                       last_name, home, work,
                                                       fax, mobile, pager,
                                                       sip_did, pri_dnis, client_password,
                                                       vm_password, sip_password, client_id,
                                                       client_email, tenant_id, robot_address,
                                                       telnet_id, company,cas_session_id,hq_username,hq_password)

            print("teamios USER %s" % user_factory)
            # if userNum > 1:
            # break
            #  TODO varname only allows ten users. Increase user num
            phoneNum = userNum + 1
            varname = '${teamios0%s}' % phoneNum
            logger.info("Creating teamios user dict \"%s\"" % varname)
            BuiltIn().set_suite_variable(varname, user_factory)
            
        logger.info("teamios user config loaded!")

    def load_google_contacts(self):
        """Load Google user attributes"""
        # Make all users visible to robot
        global OS_CONFIG_PATH
        filename = ""
        is_mt = BuiltIn().get_variable_value('${is_runtype_mt}')
        if is_mt == "true":
            filename = OS_CONFIG_PATH + self._robot_runmodule_dir +  '\\google_userInfo.csv'
        else:
            filename = OS_CONFIG_PATH + self._robot_runmodule_dir +  '\\google_userInfo.csv'

        logger.info("Loading google users from config file %s " % filename)
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

        for i in range(0, int(numPhones)):
            userNum = i
            user_name = 'first_name=%s' % userDict["user_name"][userNum]
            user_type = 'user_type=%s' % userDict["user_type"][userNum]
            first_name = 'first_name=%s' % userDict["first_name"][userNum]
            middle_name = 'middle_name=%s' % userDict["middle_name"][userNum]
            last_name = 'last_name=%s' % userDict["last_name"][userNum]
            client_email = 'client_email=%s' % userDict["client_email"][userNum]
            client_password = 'client_password=%s' % userDict["client_password"][userNum]
            # server = 'server=%s' % userDict["server"][userNum]
            home = 'home=%s' % userDict["home"][userNum]
            work = 'work=%s' % userDict["work"][userNum]
            work_fax = 'work_fax=%s' % userDict["work_fax"][userNum]
            mobile = 'mobile=%s' % userDict["mobile"][userNum]
            pager = 'pager=%s' % userDict["pager"][userNum]
            tenant_id = 'tenant_id=%s' % userDict["tenant_id"][userNum]
            robot_address = 'robot_address=%s' % userDict["robot_address"][userNum]
            telnet_id = 'telnet_id=%s' % userDict["telnet_id"][userNum]
            company = 'company=%s' % userDict["company"][userNum]

            g_user_factory = BuiltIn().create_dictionary(user_type, first_name, middle_name,
                                                         last_name, home, work,
                                                         work_fax, mobile, pager,
                                                         client_password,
                                                         client_email, tenant_id, robot_address,
                                                         telnet_id, company)

            print("gUSER %s" % g_user_factory)
            phoneNum = userNum + 1
            if phoneNum < 10:
                varname = '${g_user0%s}' % phoneNum
            else:
                varname = '${g_user%s}' % phoneNum

            BuiltIn().set_suite_variable(varname, g_user_factory)

    def create_duts(self, numPhones):
        pass

    def dump_vars(self):
        """Populate testbed specific variables"""
        variables = BuiltIn().get_variables()
        print("DEBUG: variables %s" % variables)

    def process_latest_build(self):
        """Kills chrome.exe and chromedriver.exe"""
        # Copy downloaded file to builds
        path = 'C:/Users/Administrator/Downloads/'
        file = path + "Google_Apps_LatestBuild_Main_GoogleApps_6_artifacts.zip"
        dstdir = "../../builds"
        if not os.path.exists(path):
            raise Exception("path %s not found!!!!!!!" % path)
            return
        shutil.copy(file, dstdir)

    def chrome_cleanup(self):
        """Kills chrome.exe and chromedriver.exe"""
        logger.warn("DEBUG: Killing chrome.exe and chromedriver.exe")
        #TODO add switch
        for proc in psutil.process_iter():
            if proc.name() == "chrome.exe":
                proc.kill()
            if proc.name() == "chromedriver.exe":
                proc.kill()
            if proc.name() == "ShoreTel.exe":
                proc.kill()


    def archive_output(self):
        """archive all outputs to _results"""
        tcid = BuiltIn().get_variable_value('${kTest_id}')

        # if not os.path.exists('_results\\'):
        # os.makedirs('_results\\')
        # dst = '_results\\' + str(tcid) + '_log.html'
        # dst2 = '_results\\' + str(tcid) + '_report.html'
        # dst3 = '_results\\' + str(tcid) + '_output.xml'
        # print("DEBUG: archiving outputs to %s, %s, %s" % (dst, dst2, dst3))
        # shutil.copy('log.html', dst)
        # shutil.copy('report.html', dst2)
        # shutil.copy('output.xml', dst3)

    def verify_build_is_new(self, branch):
        # Check version in manifest and compare with abco_version
        with open(GAPPS_BUILD_PATH + '\\latestbuild\\manifest.json') as df:
            data = json.load(df)
        new_ver = data["version"].encode('utf-8')

        if (branch == 'dev'):
            fh_path = WIN_ATF_CONFIG_PATH + self._robot_runmodule_dir + '\\logs\\dev_version.txt'
        else:
            fh_path = WIN_ATF_CONFIG_PATH + self._robot_runmodule_dir + '\\logs\\main_version.txt'

        logger.warn("Cross referencing new build with file \"%s\"" % fh_path)
        fh = open(fh_path)
        for line in fh:
            pass
        prev_ver = line.encode('utf-8')

        prev = tuple(map(str, prev_ver.split(".")))
        new = tuple(map(str, new_ver.split(".")))
        if new <= prev:
            logger.error("Skipping ABCO run. The latest build version %s is older/same as previous run version %s" % (
                new_ver, prev_ver))
            logger.error("Manual removal of collided build in st/mt abco_version.txt will avoid skipping run...")
            logger.error("Sending email notification...TODO")
            raise Exception("ERROR")
            return 0

        return new_ver

    def build_and_update_google_suite(self, branch):
        """Copies zip extension to builds folder.
        Unzips and creates/overwrites crx file

        :return ret_val: none.
        """
        global GAPPS_PATH
        global GAPPS_BUILD_PATH
        if (branch == 'dev'):
            GAPPS_PATH = r'C:\WFDevGCAL\automation-gapps\lib'
            GAPPS_BUILD_PATH = r'C:\WFDevGCAL\automation-gapps\builds'
        else:
            GAPPS_PATH = r'C:\WebFramework\automation-gapps\lib'
            GAPPS_BUILD_PATH = r'C:\WebFramework\automation-gapps\builds'

        filelist = [f for f in os.listdir(DOWNLOADS_PATH) if f.endswith(".zip")]
        for f in filelist:
            file = DOWNLOADS_PATH + "\\" + f
            print(file)
            shutil.copy2(file, GAPPS_BUILD_PATH + '\\build.zip')

        # sleep 5 seconds
        if not os.path.exists('latestbuild\\'):
            os.makedirs('latestbuild\\')
        if (branch == 'dev'):
            os.system(
                "\"c:\\Program Files\\7-Zip\\7z.exe\" x C:\\WFDevGCAL\\automation-gapps\\builds\*.zip -oC:\\WFDevGCAL\\automation-gapps\\builds\\latestbuild")
            os.system(
                "chrome.exe --pack-extension=\"c:\\WFDevGCAL\\automation-gapps\\builds\\latestbuild\" --pack-extension-key=\"c:\\WFDevGCAL\\automation-gapps\\builds\\build_key.pem""")
        else:
            os.system(
                "\"c:\\Program Files\\7-Zip\\7z.exe\" x C:\\WebFramework\\automation-gapps\\builds\*.zip -oC:\\WebFramework\\automation-gapps\\builds\\latestbuild")
            os.system(
                "chrome.exe --pack-extension=\"c:\\WebFramework\\automation-gapps\\builds\\latestbuild\" --pack-extension-key=\"c:\\WebFramework\\automation-gapps\\builds\\build_key.pem""")

        version = self.verify_build_is_new(branch)
        if version == 0:
            logger.warn("Aborting ABCO %s build update" % branch)
            return 0

        logger.warn("Pulling build version %s" % version)
        if (branch == 'dev'):
            # append new build version into abco_version.txt
            write_path = WIN_ATF_CONFIG_PATH + self._robot_runmodule_dir + '\\logs\\dev_version.txt'
            with open(write_path, "a") as myfile:
                myfile.write(version + '\n')
        else:
            # append new build version into abco_version.txt
            write_path = WIN_ATF_CONFIG_PATH + self._robot_runmodule_dir + '\\logs\\main_version.txt'
            with open(write_path, "a") as myfile:
                myfile.write(version + '\n')

        # overwrite input config with new build
        with open('C:\NextGenArc\etc\configs\input.config', 'r') as ifh, open('input.config', 'w') as ofh:
            replace_build = "<client>%s</client>" % version
            newline = re.sub("<client>.*</client>", replace_build, ifh.read())
            ifh.close()
            ofh.write(newline)
            ofh.close()
            shutil.copy('input.config', 'C:\NextGenArc\etc\configs\input.config')

        # replace crx with c:\crx file
        fpath = 'c:\gsuite.crx'
        os.chmod(fpath, 0777)
        os.remove(fpath)
        shutil.copy2(GAPPS_BUILD_PATH + '\\latestbuild.crx', fpath)
        archive_path = 'Z:\\ROBOT\\builds_archive\\' + branch + '_gapps_' + str(version) + '.crx'
        shutil.copy2(GAPPS_BUILD_PATH + '\\latestbuild.crx', archive_path)

        if (branch == 'dev'):
            dev_crx_path = WIN_ATF_CONFIG_PATH + self._robot_runmodule_dir + '\\dev_gsuite.crx'
            shutil.copy2(GAPPS_BUILD_PATH + '\\latestbuild.crx', dev_crx_path)
        else:
            main_crx_path = WIN_ATF_CONFIG_PATH + self._robot_runmodule_dir + '\\main_gsuite.crx'
            shutil.copy2(GAPPS_BUILD_PATH + '\\latestbuild.crx', main_crx_path)

        return version

    def remove_old_downloaded_builds(self, branch):
        filelist = [f for f in os.listdir("C:\Users\Administrator\Downloads") if f.endswith(".zip")]
        for f in filelist:
            file = "C:\\Users\\Administrator\\Downloads\\" + f
            logger.warn("Removing file %s" % file)
            os.remove(file)
        if branch == "main":
            if os.path.exists('C:\\WebFramework\\automation-gapps\\builds\\latestbuild\\'):
                shutil.rmtree("C:\\WebFramework\\automation-gapps\\builds\\latestbuild\\")
        else:
            if os.path.exists('C:\\WFDevGCAL\\automation-gapps\\builds\\latestbuild\\'):
                shutil.rmtree("C:\\WFDevGCAL\\automation-gapps\\builds\\latestbuild\\")

    def create_gapp_id_url(self):
        tempdir = tempfile.gettempdir()
        
        for subdirs, dirs, files in os.walk(tempdir):
            for dir in dirs:
                if "scoped_dir" in dir:
                    # logger.warn(dir)
                    for  files in os.listdir(os.path.join(tempdir,dir)):
                        if "extension_" in files:
                            # logger.warn(files)
                            scrap, id = files.split('_')
                            break
                   
        logger.warn(id)           
        # import rpdb2; rpdb2.start_embedded_debugger('admin1')
        write_robot_dir = os.path.join(os.path.dirname(os.getcwd()),"variables")
        write_robot_filename = "AppUrl_DoNotPush.robot"
        
        robot_var = "${GSUITE_CLIENT_LOGIN_PAGE}     chrome-extension://REPLACE/foreground.html"
        robot_var = robot_var.replace("REPLACE", id)
        
        with open(os.path.join(write_robot_dir,write_robot_filename), 'w') as fh:
            fh.write("*** Variables ***\n")
            fh.write(robot_var)

