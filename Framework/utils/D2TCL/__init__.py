import os
import psutil
import shutil
import csv
import json
from sys import platform as _platform

from robot.libraries.BuiltIn import BuiltIn
from robot.libraries.Collections import Collections
from robot.api import logger

WIN_ATF_D2_PATH = "C:\\ATF_ROBOT\\Framework\\utils\\D2cmdlib\\"
MAC_ATF_D2_PATH = "populate_me"
LINUX_ATF_D2_PATH = "populate_me"

# mvilleda - Automation Test
# This library is a wrapper and workaround to 
# run D2 cmds using tcl

class D2TCL(object):
    
    ROBOT_LIBRARY_SCOPE = 'GLOBAL'
    # ROBOT_LIBRARY_VERSION = VERSION

    def __init__(self):
        self.OS_D2_PATH = ""

        if _platform == "linux" or _platform == "linux2":
            # linux
            self.OS_D2_PATH = LINUX_ATF_D2_PATH
        elif _platform == "darwin":
            self.OS_D2_PATH = MAC_ATF_D2_PATH
            # OS X
        elif _platform == "win32":
            # Windows...
            self.OS_D2_PATH = WIN_ATF_D2_PATH
		
    def run_d2_cmd(self, testbed, cmd):
        cmd = "tclsh " + self.OS_D2_PATH + cmd
        logger.warn("Running cmd \"%s\" on %s" % (cmd, testbed.HQ1_IPADDRESS))
        status = os.system( cmd )
        if status == 1:
           raise Exception("D2 cmd \"%s\" failed" % (cmd))
        logger.info("DCAL command \"%s\" PASSED" % cmd)

    def d2_enable_hq_srtp(self, user):
        """Enable HQ SRTP
        
        :return ret_val: none.
        """
        cmd = 'py_enableHq1SRTP.tcl \"%s\"' % user.server
        self.run_d2_cmd(user, cmd)
        
    def d2_modify_workgroup_membership(self, user, workgroup_name, value):
        cmd = 'py_modifyWorkgroupM.tcl \"%s\" \"%s\" \"%s\" \"%s\"' % (user.server, user.extension, workgroup_name, value)
        
        self.run_d2_cmd(user, cmd)

    def d2_modify_workgroup_agent_state(self, testbed, user, workgroup_name, option):
	
        option = option.lower()
        agentState = {'logged_in': 'Logged In', "logged_out" :  "Logged Out", "in_wrap_up": "in _wrap_up", "exit_wrap_up":  "Logged In"}

        cmd = 'py_modifyWorkgroupAgentState.tcl \"%s\" %s \"%s\" \"%s\"' % (testbed.ROBOT_MODULE_CONFIG_DIR, user.extension, workgroup_name, agentState[option])

        self.run_d2_cmd(testbed, cmd)

    def d2_modify_huntgroup_membership(self, user, huntgroup_name, value):
        cmd = 'py_modifyHuntgroupMembership.tcl \"%s\" \"%s\" \"%s\" \"%s\"' % (user.server, user.first_name, huntgroup_name, value)

        self.run_d2_cmd(user, cmd)

    def d2_modify_phone_availability_state(self, testbed, user, value):
        cmd = 'py_modifyUserAvailability.tcl \"%s\" \"%s\" \"%s\"' % (user.server, user.first_name, value)

        self.run_d2_cmd(user, cmd)

    def d2_modify_phone_access_license(self, testbed, user, value):
        cmd = 'py_modifyPhoneAccessLicense.tcl \"%s\" %s %s' % (testbed.ROBOT_MODULE_CONFIG_DIR, user.first_name, value)

        self.run_d2_cmd(testbed, cmd)
		
		
    def d2_modify_ipphone_address_map_site(self, testbed, user, site):
        lowIPAddress = user.ip
        cmd = 'py_IPPhoneAddressMap_ChangeSite.tcl local \"%s\" \"%s\"' % (lowIPAddress, site)

        self.run_d2_cmd(testbed, cmd)
		
    def d2_modify_move_phone_to_target_switch(self, testbed, user, site):
        cmd = 'py_MovePhoneToTargetSwitch.tcl local \"%s\" \"%s\"' % (user.ip, site)

        self.run_d2_cmd(testbed, cmd)

    

    