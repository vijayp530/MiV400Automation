###############################################################################
## Module         :    SystemDBHandler
## File name      :    system_db_handler.py
## Description    :    This class contains operations on system.db for PSeries
##
## -----------------------------------------------------------------------
## Modification log:
##
## Date        Engineer              Description
## ---------   ---------      -----------------------
## 07 OCT 2015  UKumar             Initial Version
###############################################################################

import os, sys
import shutil
import re
from class_xml import xmlClass
from file_handler import FileHandler
from sqlite_db_handler import SQLiteDBHandler
from fetch_tb_info_db import FetchTbInfoDatabase
from dbHandler import dbHandler
from config_reader import ConfigReader
from class_xml import xmlClass

class SystemDBHandler(object):
    '''
    This class performs operations on system.db 
    '''

    def __init__(self, input, xmlObj, systemdb_path, logger):
        '''
        Constructor
        '''
        self.logger = logger
        self.xmlObj = xmlObj
        self.input = input
        self.logger.debug('Begin')
        self.systemdb = systemdb_path+"system.db"
        self.fileObj = FileHandler()
        self.sqlite = SQLiteDBHandler(self.logger)
        self.fetchFromDb = FetchTbInfoDatabase(self.input, self.logger)
        self.configReader = ConfigReader(self.logger)
        self.dbObj = dbHandler()
        self.hq_info = dict()
        self.logger.debug('End')

    def handle_system_db(self):
        """Calls all the functions required to update system.db
        """
        try:
            self.logger.debug('Begin')
            pid = self.dbObj.get_project_id(self.input['project'])
            query1 = 'SELECT id FROM rodexecute_testbed WHERE name='+"'"+self.input['testbed_name']+"' and ownedby='"+self.input['user']+"' and project_id='"+str(pid)+"' and type='"+self.input['testbed']['type']+"'"
            
            self.tb_id = self.dbObj.execute_select_query(query1)
            
            hqQuery = 'SELECT ip, app_user, app_password, os_user, os_password FROM rodexecute_device WHERE name=\'HQ\' and testbed_id='+str(self.tb_id[0][0])
            #print(hqQuery)
            hqInfo = self.dbObj.execute_select_query(hqQuery)
            #print("hq info: ", hqInfo)
            self.hq_info['hq_ip'] = str(hqInfo[0][0])
            self.hq_info['hq_username'] = str(hqInfo[0][1])
            self.hq_info['hq_password'] = str(hqInfo[0][2])
            self.hq_info['hq_username_rdc'] = str(hqInfo[0][3])
            self.hq_info['hq_password_rdc'] = str(hqInfo[0][4])
            if self.input['testbed']['type'] == 'MT':
                self.fileObj.copy_certificate_files(self.hq_info['hq_ip'], self.hq_info['hq_username_rdc'], self.hq_info['hq_password_rdc'], self.input)

            self.insert_user_info()
            self.verify_site_info()
            self.verify_switch_info()
            self.update_env_info()
            self.update_phone_assignment()
            self.insert_server_info()
            self.update_network_info()
            self.logger.debug('End')
        except Exception as e:
            self.logger.error("Error occured!")
            raise

    def copy_db_file_local(self):
        """
        Copies database file from remote machine to local machine
        """
        self.wm.net_copy_back(r'C:\Users\Administrator\Desktop\Uttam_backup\system.db', r'D:\Shoretel\RoD\system.db')
        
    def upload_db_file_remote(self):
        """
        Copies database file back to remote machine
        """
        self.wm.net_copy(r'D:\Shoretel\RoD\system.db', r'C:\Users\Administrator\Desktop\Uttam_backup')
        print("done")

    def user_info_handler(self):
        """
        Reads user information from Gold file and from database for insertion in users table
        """
        self.logger.debug('Begin')
        #self.sqlite.create_connection(r'Q:\testsuites\shared\testdata\system.db')
        self.sqlite.create_connection(self.systemdb)
        self.logger.debug('Delete all entries in system.db phones table')
        self.sqlite.delete_query('DELETE FROM phones')
        self.logger.debug('Delete all entries in system.db users table')
        self.sqlite.delete_query('DELETE FROM users')
        users = self.sqlite.select_query('select * from users')
        self.sqlite.close_connection()
        self.userInfo = dict()
        self.xmlObj.GetAllChildren(self.xmlObj.FindNode("./USER_INFORMATION"), self.userInfo)

        tenantQuery = 'SELECT name, tenant_id, prefix FROM rodexecute_tenants WHERE testbed_id='+str(self.tb_id[0][0])
        tenants = self.dbObj.execute_select_query(tenantQuery)
        self.userInfo["tenant_name"] = tenants[0][0]
        self.userInfo["tenantid"] = tenants[0][1]
        self.userInfo["tenant_prefix"] = tenants[0][2]

        phoneType = self.dbObj.execute_select_query('SELECT type FROM rodexecute_device WHERE name=\'IPPhone\' and testbed_id='+str(self.tb_id[0][0]))[0][0]
        self.userInfo["phone_type"] = str(phoneType)

        usersQuery = 'SELECT * FROM rodexecute_usernames WHERE testbed_id='+str(self.tb_id[0][0])

        users = self.dbObj.execute_select_query(usersQuery)
        self.userInfo['NUMBER_OF_USERS'] = len(users)
        self.userInfo['switch_name'] = self.dbObj.execute_select_query('SELECT makeme_switch  FROM rodexecute_pseriestestdata where testbed_id = {0}'.format(self.tb_id[0][0]))[0][0]

        noOfUsers = len(users)
        for i in range(1, noOfUsers+1):
            rawdid = users[i-1][5]
            #print("rawdid: ", rawdid)
            did = rawdid[0:2]+" ("+rawdid[2:5]+") "+rawdid[5:8]+"-"+rawdid[8:]
            tmpDict = {"fname":users[i-1][2], "lname":users[i-1][3], "extn":users[i-1][4], "sip_trunk_did":did, "mailbox_server":"NULL", "phone_ip":users[i-1][6], "phone_mac":re.sub('-','',users[i-1][7])}
            self.userInfo["user"+str(i)] = tmpDict
        self.logger.debug('End')

    def generate_contact_number_from_prefix(self):
        """
        Generates different contact numbers for user from prefix
        """
        self.logger.debug('Begin')
        numberOfUsers = self.userInfo['NUMBER_OF_USERS']
        self.userInfo["contact_number_prefix"] = r'+1 (408)'

        for i in range(1, numberOfUsers+1):
            self.userInfo["user"+str(i)]['home'] = self.userInfo["contact_number_prefix"]+" 111-"+self.userInfo["user"+str(i)]['extn']
            self.userInfo["user"+str(i)]['business'] = self.userInfo["contact_number_prefix"]+" 112-"+self.userInfo["user"+str(i)]['extn']
            self.userInfo["user"+str(i)]['fax'] = self.userInfo["contact_number_prefix"]+" 113-"+self.userInfo["user"+str(i)]['extn']
            self.userInfo["user"+str(i)]['mobile'] = self.userInfo["contact_number_prefix"]+" 114-"+self.userInfo["user"+str(i)]['extn']
            self.userInfo["user"+str(i)]['pager'] = self.userInfo["contact_number_prefix"]+" 115-"+self.userInfo["user"+str(i)]['extn']
            self.userInfo["user"+str(i)]['pritrunkdnis'] = self.userInfo["contact_number_prefix"]+" 116-"+self.userInfo["user"+str(i)]['extn']
        #print("users : ", self.userInfo)

        self.logger.debug("User data generated from prefix.")
        self.logger.debug('End')

    def insert_one_user(self, user, update=False):
        """ Inserts single user and phone in users and phones table respectively
        """
        self.logger.debug('Begin')
        for i in range(1, self.userInfo['NUMBER_OF_USERS']+1):
            if self.userInfo['user'+str(i)]['fname'] == user:
                user = 'user'+str(i)
                break

        query = [self.userInfo[user]['fname'], self.userInfo[user]['lname'], self.userInfo[user]['extn'], self.userInfo[user]['home'],
                 self.userInfo[user]['business'], self.userInfo[user]['fax'], self.userInfo[user]['mobile'], self.userInfo[user]['pager'],
                 self.userInfo[user]["sip_trunk_did"], self.userInfo[user]["pritrunkdnis"],
                 self.userInfo["comments"], self.userInfo["vm_password"], self.userInfo["type"],
                 self.userInfo["client_password"], self.userInfo["sip_password"],
                 self.userInfo[user]["mailbox_server"],
                 self.userInfo["tenantid"], self.userInfo["tenant_prefix"]
                ]

        phone_query = [
                self.userInfo[user]['extn'],
                self.userInfo[user]['phone_ip'],
                self.userInfo["phone_type"].upper(),
                'TRUE', #available
                self.userInfo["switch_name"],
                self.userInfo[user]['fname'].lower(), #self.firstNameList[i-1],
                'cisco_switch_1', #self.userInfo["network_switch"],
                self.userInfo[user]['phone_mac']
                ]

        self.logger.info(query)
        self.logger.info(phone_query)
        try:
            #if update:
            #    self.sqlite.execute_query('delete from users where first_name = "{0}"'.format(self.userInfo[user]['fname']))
            self.sqlite.insert_query("users", tuple(query))
            self.logger.info("One row inserted in users table")
        except Exception as e:
            self.logger.error("Error : Unable to insert user.")
            raise e

        try:
            #if update:
            #    self.sqlite.execute_query('delete from users where first_name = "{0}"'.format(self.userInfo[user]['fname']))
            self.sqlite.insert_query("phones", tuple(phone_query))
            self.logger.info("One row inserted in phones table")
        except Exception as e:
            self.logger.error("Error : Unable to insert phone.")
            raise e
        self.logger.debug('End')

    def insert_user_info(self):
        """
        Inserts user's information in users table
        """
        self.logger.debug('Begin')
        self.user_info_handler()
        self.generate_contact_number_from_prefix()
        try:
            #self.sqlite.create_connection(r'Q:\testsuites\shared\testdata\system.db')
            self.sqlite.create_connection(self.systemdb)
            for user in self.userInfo.keys():
                if re.match('user\d+',user):
                    self.insert_one_user(user)
            self.sqlite.close_connection()
            self.logger.debug('End')
        except Exception as e:
            self.logger.error(e)
            raise e

    def phone_assignment_handler(self):
        """
        Reads information related to phone assignment from database
        """
        self.logger.debug('Begin')
        sQuery = "SELECT phone_type, available FROM phones WHERE user_extension IN ("
        for ext in self.extensionList:
            sQuery = sQuery+ext+", "
        sQuery = sQuery.rstrip(', ')+")"
        self.logger.debug(sQuery)
        #print(sQuery)
        #self.sqlite.create_connection(r'Q:\testsuites\shared\testdata\system.db')
        self.sqlite.create_connection(self.systemdb)
        self.result = self.sqlite.select_query(sQuery)
        
        self.sqlite.close_connection()
        self.typeList = []
        self.enabledList = []
        self.phoneName = ['dut', 'phone1', 'phone2', 'phone3', 'phon4', 'phone5',
                          'phone6', 'phone7', 'phone8', 'phone9', 'phone10'
                          ]
        for row in self.result:
            self.typeList.append(row[0])
            self.enabledList.append(row[1])
        self.logger.debug('End')
        
    def update_phone_assignment(self):
        """
        Updates phone_assignments table
        """
        self.logger.debug('Begin')
        # self.phone_assignment_handler()
        try:
            #self.sqlite.create_connection(r'Q:\testsuites\shared\testdata\system.db')
            self.sqlite.create_connection(self.systemdb)
            
            phoneType = self.dbObj.execute_select_query('SELECT type FROM rodexecute_device WHERE name=\'IPPhone\' and testbed_id='+str(self.tb_id[0][0]))[0][0]
            site_name = self.dbObj.execute_select_query('SELECT name FROM rodexecute_sites WHERE testbed_id='+str(self.tb_id[0][0]))[0][0]

            query = 'update phone_assignments set type="{0}", enabled="{1}", site="{2}" where id in (1,2,3,4)'.format(str(phoneType),'TRUE',str(site_name))
            self.sqlite.execute_query(query)
            self.sqlite.db_connection.commit()
            self.sqlite.close_connection()
            self.logger.debug('End')
        except Exception:
            self.logger.error("Error : Not able to update phone_assignments table")
            raise

    def verify_new_testbed(self):
        """
        Verifies whether the testbed(ATF machine) is new or old one
        if new it will inserts site info, switch info, server info
        and updates env table
        """
        try:
            if self.input['new_atf'] == True:
                return "new_testbed"
            else:
                return "old_testbed"
        except Exception as e:
            self.logger.error("Not able to verify testbed.")
            raise e
        
    def site_info_handler(self):
        """
        Reads site information from database
        """
        try:
            self.logger.debug('Begin')
            self.siteInfo = dict()
            siteQuery = 'SELECT name FROM rodexecute_sites WHERE testbed_id='+str(self.tb_id[0][0])
            input_site = self.dbObj.execute_select_query(siteQuery)
            self.siteNames = []
            for site in input_site[0]:
                self.siteNames.append(str(site))
            self.logger.debug('End')
            return self.siteNames
        except Exception as e:
            self.logger.error("Error : Unable to fetch site info.")
            raise e
    
    def verify_site_info(self):
        """
        Verifies that sites which we want to insert, already exist in the databse or not
        if not then call insert_one_site method
        """
        try:
            self.logger.debug('Begin')
            sitesToInsert = self.site_info_handler()
            #get list of sites from sys.db
            #self.sqlite.create_connection(r'Q:\testsuites\shared\testdata\system.db')
            self.sqlite.create_connection(self.systemdb)
            selectQuerySite = "SELECT site_name from sites"
            existingSitesTuple = self.sqlite.select_query(selectQuerySite)
            #print("existing sites : ", existingSitesTuple)
            
            existingSites = []
            for existingSite in existingSitesTuple:
                existingSites.append(', '.join(map(str, existingSite)))
            #print("after conversion 1: , ", existingSites)
            
            for site in sitesToInsert:
                if site in existingSites:
                    self.update_one_site(site)
                else:
                    self.insert_one_site(site)
            self.sqlite.close_connection()
            self.logger.debug('End')
        except Exception as e:
            self.logger.error("Error : Unable to verify site info.")
            raise e
        
    def insert_site_info(self):
        """
        Inserts multiple sites in sites table
        """
        try:
            self.logger.debug('Begin')
            sitenames = self.site_info_handler()
            #self.sqlite.create_connection(r'Q:\testsuites\shared\testdata\system.db')
            self.sqlite.create_connection(self.systemdb)
            for site in sitenames:
                self.insert_one_site(site)
            self.sqlite.close_connection()
            self.logger.debug('End')
        except Exception as e:
            self.logger.error("Error : Unable to insert multiple sites")
            raise e
        
    def insert_one_site(self, site):
        """ Inserts one site in sites table
        """
        query = [site,  self.hq_info['hq_ip'],self.hq_info['hq_username'],self.hq_info['hq_password'],None]
        self.logger.info(query)
        try:
            self.sqlite.insert_query("sites", tuple(query))
            self.logger.info("One row inserted in sites table")
        except Exception as e:
            self.logger.error("Error : Unable to insert site.")
            raise e

    def update_one_site(self, site):
        """ Updates one site in sites table
        """
        query = "UPDATE sites SET hq_ip='"+self.hq_info['hq_ip']+"', hq_username='"+self.hq_info['hq_username']+\
                "', hq_password='"+self.hq_info['hq_password']+"' WHERE site_name='"+site+"'"
        self.logger.info(query)
        try:
            self.sqlite.update_query(query)
            self.logger.info("site updated")
        except Exception as e:
            self.logger.error("Error : Unable to update site.")
            raise e
            
    def switch_info_handler(self):
        """
        Reads switch information from database and creates a dictionary
        """
        self.logger.debug('Begin')
        self.switchInfo = dict()
        #self.sites = self.site_info_handler
        query ="SELECT name,ip, mac,type,site FROM rodexecute_device WHERE testbed_id="+str(self.tb_id[0][0])+" and type='SG-vPhone'"
        self.input_switches = self.dbObj.execute_select_query(query)

        i = 1
        # for switch in input_switches:
        for s in self.input_switches:
            self.switchInfo["switch"+str(i)] = dict()
            self.switchInfo["switch"+str(i)]["switch_name"] = str(s[0])
            self.switchInfo["switch"+str(i)]["switch_ip"] = str(s[1])
            self.switchInfo["switch"+str(i)]["switch_mac"] = re.sub('-','',str(s[2]))
            self.switchInfo["switch"+str(i)]["switch_type"] = str(s[3])
            self.switchInfo["switch"+str(i)]["site_name"] = str(s[4])
            i = i+1
        self.logger.debug('End')

    def verify_switch_info(self):
        """
        Verifies that switches which we want to insert, already exist in the database or not
        if not then call insert_one_switch method
        """
        try:
            self.logger.debug('Begin')
            self.switch_info_handler()
            #self.sqlite.create_connection(r'Q:\testsuites\shared\testdata\system.db')
            self.sqlite.create_connection(self.systemdb)
            selectQuerySwitch = "SELECT switch_name from switches"
            existingSwitchesTuple = self.sqlite.select_query(selectQuerySwitch)
            #print("existing switches : ", existingSwitchesTuple)
            self.logger.debug(existingSwitchesTuple)

            existingSwitches = []
            for existingSwitch in existingSwitchesTuple:
                existingSwitches.append(', '.join(map(str, existingSwitch)))
            #print("after conversion 1: , ", existingSwitches)
            switchIndex = 1
            for switch in self.input_switches:
                if switch[0] in existingSwitches:
                    self.insert_one_switch(switchIndex, update=True)
                    switchIndex += 1
                    self.logger.info("Switch already exists.")
                else:
                    self.insert_one_switch(switchIndex)
                    switchIndex += 1

            self.sqlite.close_connection()
            self.logger.debug('End')
        except Exception as e:
            self.logger.error("Error : Unable to verify switch info.")
            raise e

    def insert_one_switch(self, i, update=False):
        """ Inserts one switch in switches table
        """
        query = [self.switchInfo["switch"+str(i)]["switch_name"], self.switchInfo["switch"+str(i)]["switch_ip"],
                 self.switchInfo["switch"+str(i)]["site_name"], self.switchInfo["switch"+str(i)]["switch_type"],
                 self.switchInfo["switch"+str(i)]["switch_mac"]
                ]
        self.logger.info(query)
        try:
            if update:
                self.sqlite.delete_query('delete from switches where switch_name="{0}"'.format(self.switchInfo["switch"+str(i)]["switch_name"]))
            self.sqlite.insert_query("switches", tuple(query))
            self.logger.info("One switch inserted")
        except Exception as e:
            self.logger.error("Error : Unable to insert one switch.")
            raise e
        
    def server_info_handler(self):
        """
        Reads server information from database and creates a dictionary
        """
        self.logger.debug('Begin')
        self.serverInfo = dict()
        self.numberOfServers = 1

        query1 = 'SELECT baa, aa, vm, vmlogin, acs, ucb FROM rodexecute_pseriestestdata WHERE testbed_id={0}'.format(str(self.tb_id[0][0]))
        info = self.dbObj.execute_select_query(query1)
        #self.sqlite.create_connection(r'Q:\testsuites\shared\testdata\system.db')
        self.sqlite.create_connection(self.systemdb)
        query2 = "SELECT globalaa, globalvm, globalvmlogin, globalacs, globalucb from servers where server_name='hq1'"
        globalInfo = self.sqlite.select_query(query2)
        self.sqlite.close_connection()

        # self.serverInfo["default_server"] = info[0][]
        # print(self.serverInfo["default_server"])
        
        for i in range(1, self.numberOfServers+1):
            server = "server"+str(i)
            self.serverInfo[server] = dict()
            self.serverInfo[server]['server_name'] = self.siteNames[0]
            self.serverInfo[server]['globalaa'] = str(globalInfo[0][0])
            self.serverInfo[server]['globalvm'] = str(globalInfo[0][1])
            self.serverInfo[server]['globalvmlogin'] = str(globalInfo[0][2])
            self.serverInfo[server]['globalacs'] = str(globalInfo[0][3])
            self.serverInfo[server]['globalucb'] = str(globalInfo[0][4])
            self.serverInfo[server]['baa'] = info[0][0]
            self.serverInfo[server]['aa'] = info[0][1]
            self.serverInfo[server]['vm'] = info[0][2]
            self.serverInfo[server]['vmlogin'] = info[0][3]
            self.serverInfo[server]['acs'] = info[0][4]
            self.serverInfo[server]['ucb'] = info[0][5]
        self.logger.debug('End')
        
    '''def update_server_info(self):
        """
        Updates default server's (hq1) information in servers table
        """
        self.server_info_handler()
        query = "UPDATE servers SET globalaa='"+self.serverInfo["default_server"]["globalaa"]+"', globalvm='"\
                +self.serverInfo["default_server"]["globalvm"]+"', globalvmlogin='"\
                +self.serverInfo["default_server"]["globalvmlogin"]+"', globalacs='"\
                +self.serverInfo["default_server"]["globalacs"]+"', globalucb='"\
                +self.serverInfo["default_server"]["globalucb"]+"', baa='"+self.serverInfo["default_server"]["baa"]+"', aa='"\
                +self.serverInfo["default_server"]["aa"]+"', vm='"+self.serverInfo["default_server"]["vm"]+"', vmlogin='"\
                +self.serverInfo["default_server"]["vmlogin"]+"', acs='"+self.serverInfo["default_server"]["acs"]+"', nightbell='"\
                +self.serverInfo["default_server"]["nightbell"]+"', overheadpage='"\
                +self.serverInfo["default_server"]["overheadpage"]+"', ucb='"\
                +self.serverInfo["default_server"]["ucb"]+"', sysconf='"+self.serverInfo["default_server"]["sysconf"]+\
                "' WHERE server_name='hq1'"
        
        #print("Query is : ", query)
        try:
            self.sqlite.create_connection(r'Q:\testsuites\shared\testdata\system.db')
            self.sqlite.update_query(query)
            self.logger.info("Server information updated.")
            self.sqlite.close_connection()
        except Exception as e:
            self.logger.error("Error : Unable to update server information")
            raise e'''

    def verify_server_exists(self):
        """Verifies that server which we want to insert, already exists or not
        """
        try:
            self.logger.debug('Begin')
            #self.sqlite.create_connection(r'Q:\testsuites\shared\testdata\system.db')
            self.sqlite.create_connection(self.systemdb)
            query = "SELECT server_name from servers"
            existingServersTuple = self.sqlite.select_query(query)

            existingServers = []
            for existingServer in existingServersTuple:
                existingServers.append(', '.join(map(str, existingServer)))

            server = self.siteNames[0]
            if server in existingServers:
                deleteQuery = "DELETE FROM servers WHERE server_name='"+server+"'"
                self.sqlite.delete_query(deleteQuery)
                self.logger.debug(server+" deleted.")
            else:
                self.logger.info(server+" does not exist.")
            self.sqlite.close_connection()
            self.logger.debug('End')
        except Exception as e:
            self.logger.error("Error : Unable to verify existing server")
            raise e
        
    def insert_server_info(self):
        """
        Inserts server information in servers table
        """
        self.server_info_handler()
        self.verify_server_exists()
        try:
            #self.sqlite.create_connection(r'Q:\testsuites\shared\testdata\system.db')
            self.sqlite.create_connection(self.systemdb)
            for i in range(0, self.numberOfServers):
                insertQuery = [self.serverInfo["server"+str(i+1)]["server_name"], self.serverInfo["server"+str(i+1)]["globalaa"],
                         self.serverInfo["server"+str(i+1)]["globalvm"], self.serverInfo["server"+str(i+1)]["globalvmlogin"],
                         self.serverInfo["server"+str(i+1)]["globalacs"], self.serverInfo["server"+str(i+1)]["globalucb"],
                         self.serverInfo["server"+str(i+1)]["baa"], self.serverInfo["server"+str(i+1)]["aa"],
                         self.serverInfo["server"+str(i+1)]["vm"], self.serverInfo["server"+str(i+1)]["vmlogin"],
                         self.serverInfo["server"+str(i+1)]["acs"],
                         #self.serverInfo["server"+str(i+1)]["nightbell"],
                         'NULL',
                         #self.serverInfo["server"+str(i+1)]["overheadpage"],
                         'NULL',
                         self.serverInfo["server"+str(i+1)]["ucb"],
                         #self.serverInfo["server"+str(i+1)]["sysconf"],
                         'NULL'
                         ] 
                          
                self.logger.info(insertQuery)
                self.sqlite.insert_query("servers", tuple(insertQuery))
                self.logger.info("Server information inserted.")
            self.sqlite.close_connection()
        except Exception as e:
            self.logger.error("Error : Unable to insert server information")
            raise e
            
    def env_info_handler(self):
        """
        Reads env table related data from database
        """
        self.logger.debug('Begin')
        self.envInfo = dict()
        #self.xmlClassObj.GetAllChildren(self.xmlClassObj.FindNode("./ENV_INFORMATION"), self.envInfo)
        query1 = 'SELECT check_sanity, sanity_notifytarget, makeme_switch, enable_dcal, mt_fqdn,' \
                 ' enable_multitenant, enable_backup FROM rodexecute_pseriestestdata WHERE testbed_id={0}'.format(str(self.tb_id[0][0]))
        #print("query1 :", query1)
        info = self.dbObj.execute_select_query(query1)

        self.envInfo['check_sanity'] = info[0][0]
        self.envInfo['sanity_notifytarget'] = info[0][1]
        self.envInfo['makeme_switch'] = info[0][2]
        self.envInfo['enable_dcal'] = info[0][3]
        self.envInfo['mt_fqdn'] = info[0][4]
        self.envInfo['enable_multitenant'] = info[0][5]
        self.envInfo['enable_backup'] = info[0][6]
        self.envInfo['dcal_login'] = self.hq_info['hq_username']
        self.envInfo['dcal_password'] = self.hq_info['hq_password']
        self.logger.debug('End')
        
    def update_env_info(self):
        """
        Updates env table
        """
        self.logger.debug('Begin')
        self.env_info_handler()
        try:
            #self.sqlite.create_connection(r'Q:\testsuites\shared\testdata\system.db')
            self.sqlite.create_connection(self.systemdb)
            for k, v in self.envInfo.items():
                query = "UPDATE env SET value='"+v+"' WHERE key='"+k+"'"
                self.sqlite.update_query(query)
                self.logger.info("Row updated in env table")
            self.sqlite.close_connection()
            self.logger.debug('End')
        except Exception as e:
            self.logger.error("Error : Unable to update env table.")
            raise e
        
    def network_info_handler(self):
        """
        Reads networks table related data from database
        """
        self.logger.debug('Begin')
        self.networkInfo = dict()
        query1 = 'SELECT sbc_ip FROM rodexecute_pseriestestdata WHERE testbed_id={0}'.format(str(self.tb_id[0][0]))
        #print("query1 :", query1)
        info = self.dbObj.execute_select_query(query1)
        self.networkInfo['sbc_ip'] = info[0][0]
        self.logger.debug('End')
        
    def update_network_info(self):
        """
        Updates networks table
        """
        self.logger.debug('Begin')
        self.network_info_handler()
        try:
            #self.sqlite.create_connection(r'Q:\testsuites\shared\testdata\system.db')
            self.sqlite.create_connection(self.systemdb)
            for k, v in self.networkInfo.items():
                query = "UPDATE networks SET network_switch_ip='"+v+"' WHERE network_switch_name='"+k+"'"
                #print(query)
                self.sqlite.update_query(query)
                self.logger.info("Row updated in networks table")
            self.sqlite.close_connection()
            self.logger.debug('End')
        except Exception as e:
            self.logger.error("Error : Unable to update networks table.")
            raise e


            
            
            

if __name__ == "__main__":
    from util import logger, class_xml
    logger = logger.get_logger('TestLog.log', 'DEBUG')
    #obj_sys = SystemDBHandler('UsersInfo.xml',None,logger)
    input = {'testbed_name' : 'PseriesMttbUttam', 'user' : 'UKumar', 'project':'Cosmo-PSeries', 'testbed': {'type','MT'}};
    obj_sys = SystemDBHandler(input,r'C:\NextGenArc\xmlFiles\private\pseries_private_tbGold.xml',logger)
    #obj_sys.user_info_handler()
    #obj_sys.insert_user1800_info()
    #obj_sys.insert_phone_info()
    #obj_sys.update_phone_assignment()
    #obj_sys.check_inserted_info()
    #obj_sys.get_sip_trunk_did()
    #obj_sys.verify_new_testbed()
    #obj_sys.site_info_handler()
    #obj_sys.update_network_info()
    #obj_sys.verify_site_info()
    #obj_sys.insert_site_info()
    obj_sys.site_info_handler()
    #obj_sys.handle_system_db()
    #obj_sys.copy_certificate_files()
