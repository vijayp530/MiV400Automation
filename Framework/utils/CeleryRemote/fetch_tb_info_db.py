__author__ = 'UKumar'

import sys
import re
from string import ascii_uppercase
from dbHandler import dbHandler
from fetch_testbed_info import FetchTestbedInfo

class FetchTbInfoDatabase:
    """
    classdocs
    """

    def __init__(self, input, logger):
        """
        Constructor
        """
        self.input = input
        self.logger = logger
        self.logger.debug('Begin')
        self.dbObj = dbHandler()
        self.logger.debug('End')

    def fetch_mh_st_info(self):
        tb_info = dict()
        #tb_info_db = self.select(tb_name)
        pid = self.dbObj.get_project_id(self.input['project'])
        query1 = 'SELECT id FROM rodexecute_testbed WHERE name='+"'"+self.input['testbed_name']+"' and ownedby='"+self.input['user']+"' and project_id='"+str(pid)+"' and type='"+self.input['testbed']['type']+"'"
        # query1 = 'SELECT id FROM rodexecute_testbed WHERE name='+"'"+self.input['testbed_name']+"' and ownedby='"+self.input['user']+"' and project='"+self.input['project']+"' and type='"+self.input['testbed']['type']+"'"
        print("query1 :", query1)
        tb_id = self.dbObj.execute_select_query(query1)
        print("id:", tb_id[0][0])
        print("id is ", int(str(tb_id).lstrip("(").rstrip("L,)")))
        hqQuery = 'SELECT ip, app_user, app_password, os_user, os_password FROM rodexecute_device WHERE name=\'HQ\' and testbed_id='+str(tb_id[0][0])
        print(hqQuery)
        hqInfo = self.dbObj.execute_select_query(hqQuery)
        print("hq info: ", hqInfo)

        tb_info['SITE1_SERVER_ADDR'] = str(hqInfo[0][0])
        tb_info['SITE1_USERNAME'] = str(hqInfo[0][1])
        tb_info['SITE1_PASSWORD'] = str(hqInfo[0][2])
        tb_info['OS_USERNAME'] = str(hqInfo[0][3])
        tb_info['OS_PASSWORD'] = str(hqInfo[0][4])

        phoneQuery = 'SELECT mac FROM rodexecute_device WHERE name=\'IPPhone\' and testbed_id='+str(tb_id[0][0])
        phonemac = self.dbObj.execute_select_query(phoneQuery)
        print(phonemac)
        i = 1
        for mac in phonemac:
            tb_info['PHONE'+str(i)+'_MAC_ADDR'] = mac[0]
            i = i+1
        print(tb_info)
        return tb_info

    def fetch_mh_mt_info(self, tb_info):
        # query1 = 'SELECT id FROM rodexecute_testbed WHERE name='+"'"+self.input['testbed_name']+"' and ownedby='"+self.input['user']+"' and project='"+self.input['project']+"' and type='"+self.input['testbed']['type']+"'"
        pid = self.dbObj.get_project_id(self.input['project'])
        query1 = 'SELECT id FROM rodexecute_testbed WHERE name='+"'"+self.input['testbed_name']+"' and ownedby='"+self.input['user']+"' and project_id='"+str(pid)+"' and type='"+self.input['testbed']['type']+"'"
        print("query1 :", query1)
        tb_id = self.dbObj.execute_select_query(query1)
        print("id:", tb_id[0][0])

        hqQuery = 'SELECT ip, app_user, app_password, os_user, os_password FROM rodexecute_device WHERE name=\'HQ\' and testbed_id='+str(tb_id[0][0])
        print(hqQuery)
        hqInfo = self.dbObj.execute_select_query(hqQuery)
        print("hq info: ", hqInfo)

        tb_info['SITE1_SERVER_ADDR'] = str(hqInfo[0][0])
        tb_info['MT_D2_SERVER_IP'] = str(hqInfo[0][0])
        tb_info['MT_D2_LOGINNAME'] = str(hqInfo[0][1])
        tb_info['MT_D2_LOGINPASSWORD'] = str(hqInfo[0][2])
        tb_info['OS_USERNAME'] = str(hqInfo[0][3])
        tb_info['OS_PASSWORD'] = str(hqInfo[0][4])
        print(tb_info)

        switchQuery = 'SELECT name, ip, type, mac FROM rodexecute_device WHERE type=\'SG-vPhone\' and testbed_id='+str(tb_id[0][0])
        switches = self.dbObj.execute_select_query(switchQuery)
        print(switches)
        i = 1
        for switch in switches:
            tb_info['SETUP'+str(i)+'_SITE'+str(i)+'_SWITCH'+str(i)+'_NAME'] = switch[0]
            tb_info['SETUP'+str(i)+'_SITE'+str(i)+'_SWITCH'+str(i)+'_ADDR'] = switch[1]
            tb_info['SETUP'+str(i)+'_SITE'+str(i)+'_SWITCH'+str(i)+'_TYPE'] = switch[2]
            tb_info['SETUP'+str(i)+'_SITE'+str(i)+'_SWITCH'+str(i)+'_MAC'] = switch[3]
            i = i+1
        tenantQuery = 'SELECT name, tenant_id, prefix FROM rodexecute_tenants WHERE testbed_id='+str(tb_id[0][0])
        tenants = self.dbObj.execute_select_query(tenantQuery)
        print("tenant: ", tenants)
        tb_info['MT_DEFAULT_TENANT_NAME'] = tenants[0][0]
        tb_info['MT_DEFAULT_TENANT_ID'] = tenants[0][1]
        tb_info['MT_DEFAULT_TENANT_PREFIX'] = tenants[0][2]
        testInfo = self.dbObj.execute_select_query('SELECT * FROM rodexecute_manhattantestdata WHERE testbed_id='+str(tb_id[0][0]))
        tb_info['MT_ABC_AUTHENTICATION_URL'] = testInfo[0][1]
        tb_info['REVERSE_PROXY_IP_FOR_HOST'] = testInfo[0][2]
        #print(tb_info)
        return tb_info

    def fetch_mb_st_info(self, tb_info):
        usrmac_info = dict()
        pid = self.dbObj.get_project_id(self.input['project'])
        query1 = 'SELECT id FROM rodexecute_testbed WHERE name='+"'"+self.input['testbed_name']+"' and ownedby='"+self.input['user']+"' and project_id='"+str(pid)+"' and type='"+self.input['testbed']['type']+"'"
        # query1 = 'SELECT id FROM rodexecute_testbed WHERE name='+"'"+self.input['testbed_name']+"' and ownedby='"+self.input['user']+"' and project='"+self.input['project']+"' and type='"+self.input['testbed']['type']+"'"
        print("query1 :", query1)
        tb_id = self.dbObj.execute_select_query(query1)
        print("id:", tb_id[0][0])

        hqQuery = 'SELECT ip, app_user, app_password, os_user, os_password FROM rodexecute_device WHERE (name=\'HQ\' OR name=\'SMR\') and testbed_id='+str(tb_id[0][0])
        print(hqQuery)
        hqInfo = self.dbObj.execute_select_query(hqQuery)
        print("hq info: ", hqInfo)

        tb_info['SITE1_SERVER_ADDR'] = str(hqInfo[0][0])
        tb_info['SITE1_USERNAME'] = str(hqInfo[0][1])
        tb_info['SITE1_PASSWORD'] = str(hqInfo[0][2])
        tb_info['OS_USERNAME'] = str(hqInfo[0][3])
        tb_info['OS_PASSWORD'] = str(hqInfo[0][4])

        tb_info['SMR_IP_ADDR'] = str(hqInfo[1][0])
        tb_info['SMR_USERNAME'] = str(hqInfo[1][1])
        tb_info['SMR_PASSWORD'] = str(hqInfo[1][2])


        mDeviceQuery = 'SELECT port, plateform_name, plateform_version, name, udid, ios_udid, password ' \
                       'FROM rodexecute_mobilitydevices WHERE testbed_id='+str(tb_id[0][0])
        mobilityDevices = self.dbObj.execute_select_query(mDeviceQuery)
        print(mobilityDevices)
        i = 1
        for device in mobilityDevices:
            tb_info['DEVICE'+str(i)+'_PORT'] = device[0]
            tb_info['DEVICE'+str(i)+'_PLATFORM_NAME'] = device[1]
            tb_info['DEVICE'+str(i)+'_PLATFORM_VERSION'] = device[2]
            tb_info['DEVICE'+str(i)+'_NAME'] = device[3]
            tb_info['DEVICE'+str(i)+'_UDID'] = device[4]
            tb_info['DEVICE'+str(i)+'_PASSWORD'] = device[6]
        tb_info['DEVICE1_iOS_UDID'] = mobilityDevices[0][5]

        mbTestDataQuery = 'SELECT * FROM rodexecute_mobilitytestdata WHERE testbed_id='+str(tb_id[0][0])
        mbTestData = self.dbObj.execute_select_query(mbTestDataQuery)
        tb_info['APP_PKG'] = mbTestData[0][1]
        tb_info['APP_ACTIVITY'] = mbTestData[0][2]
        tb_info['APP_LOCATION'] = mbTestData[0][3]
        tb_info['NEW_COMMAND_TIMEOUT'] = mbTestData[0][4]
        phoneType = self.dbObj.execute_select_query('SELECT type FROM rodexecute_device WHERE name=\'IPPhone\' and testbed_id='+str(tb_id[0][0]))[0][0]

        mbUsersQuery = 'SELECT * FROM rodexecute_usernames WHERE testbed_id='+str(tb_id[0][0])
        mbUsers = self.dbObj.execute_select_query(mbUsersQuery)
        print(mbUsers)
        i = 1
        noOfUsers = len(mbUsers)
        for ch in ascii_uppercase:
            tb_info['USER_'+ch+'_NAME'] = mbUsers[i-1][1]
            tb_info['USER_'+ch+'_FULLNAME'] = mbUsers[i-1][2]+"#"+mbUsers[i-1][3]
            tb_info['USER_'+ch+'_EXTENSION'] = mbUsers[i-1][4]
            tb_info['PPHONE_0'+str(i)+'_ADDR'] = str(mbUsers[i-1][6])  # for converting None to string None
            usrmac_info['USER'+str(i)+'_FIRSTNAME'] = mbUsers[i-1][2]
            usrmac_info['USER'+str(i)+'_LASTNAME'] = mbUsers[i-1][3]
            usrmac_info['USER'+str(i)+'_EXTENSION'] = mbUsers[i-1][4]
            usrmac_info['USER'+str(i)+'_DID'] = str(mbUsers[i-1][5])
            #usrmac_info['PPHONE_0'+str(i)+'_ADDR'] = str(mbUsers[i-1][7])
            usrmac_info['USER'+str(i)+'_MAC'] = re.sub('\-', '', str(mbUsers[i-1][7]))
            if i == noOfUsers:
                break
            i += 1
        usrmac_info['NUMBER_OF_USERS'] = len(mbUsers)
        usrmac_info['PHONE_TYPE'] = str(phoneType)
        #print(tb_info)
        #print(usrmac_info)

        return tb_info, usrmac_info

    def fetch_pbx_mt_info(self, tb_info):
        usrmac_info = dict()
        bco_config_info = dict()
        pid = self.dbObj.get_project_id(self.input['project'])
        query1 = 'SELECT id FROM rodexecute_testbed WHERE name='+"'"+self.input['testbed_name']+"' and ownedby='"+self.input['user']+"' and project_id='"+str(pid)+"' and type='"+self.input['testbed']['type']+"'"
        # query1 = 'SELECT id FROM rodexecute_testbed WHERE name='+"'"+self.input['testbed_name']+"' and ownedby='"+self.input['user']+"' and project='"+self.input['project']+"' and type='"+self.input['testbed']['type']+"'"
        print("query1 :", query1)
        tb_id = self.dbObj.execute_select_query(query1)
        print("id:", tb_id)

        hqQuery = 'SELECT ip, app_user, app_password, os_user, os_password FROM rodexecute_device WHERE name=\'HQ\' and testbed_id='+str(tb_id[0][0])
        print(hqQuery)
        hqInfo = self.dbObj.execute_select_query(hqQuery)
        print("hq info: ", hqInfo)

        tb_info['SITE1_SERVER_ADDR'] = str(hqInfo[0][0])
        tb_info['MT_D2_SERVER_IP'] = str(hqInfo[0][0])
        tb_info['MT_D2_LOGINNAME'] = str(hqInfo[0][1])
        tb_info['MT_D2_LOGINPASSWORD'] = str(hqInfo[0][2])
        tb_info['OS_USERNAME'] = str(hqInfo[0][3])
        tb_info['OS_PASSWORD'] = str(hqInfo[0][4])
        #print(tb_info)

        switchQuery = 'SELECT name, ip, type, mac FROM rodexecute_device WHERE type=\'SG-vPhone\' and testbed_id='+str(tb_id[0][0])
        switches = self.dbObj.execute_select_query(switchQuery)

        i = 1
        for switch in switches:
            tb_info['SETUP'+str(i)+'_SITE'+str(i)+'_SWITCH'+str(i)+'_NAME'] = switch[0]
            bco_config_info['SITE1_SWITCH'+str(i)+'_NAME'] = switch[0]
            tb_info['SETUP'+str(i)+'_SITE'+str(i)+'_SWITCH'+str(i)+'_ADDR'] = switch[1]
            tb_info['SETUP'+str(i)+'_SITE'+str(i)+'_SWITCH'+str(i)+'_TYPE'] = switch[2]
            tb_info['SETUP'+str(i)+'_SITE'+str(i)+'_SWITCH'+str(i)+'_MAC'] = switch[3]
            i = i+1
        tenantQuery = 'SELECT name, tenant_id, prefix FROM rodexecute_tenants WHERE testbed_id='+str(tb_id[0][0])
        tenants = self.dbObj.execute_select_query(tenantQuery)
        tb_info['MT_DEFAULT_TENANT_NAME'] = tenants[0][0]
        tb_info['MT_DEFAULT_TENANT_ID'] = tenants[0][1]
        tb_info['MT_DEFAULT_TENANT_PREFIX'] = tenants[0][2]
        testInfo = self.dbObj.execute_select_query('SELECT * FROM rodexecute_pbxtestdata WHERE testbed_id='+str(tb_id[0][0]))

        tb_info['MT_ABC_AUTHENTICATION_URL'] = testInfo[0][1]
        tb_info['REVERSE_PROXY_IP_FOR_HOST'] = testInfo[0][2]

        bco_config_info['PRI_DID_RANGE'] = testInfo[0][3]


        pbxUsersQuery = 'SELECT * FROM rodexecute_usernames WHERE testbed_id='+str(tb_id[0][0])
        pbxUsers = self.dbObj.execute_select_query(pbxUsersQuery)

        noOfUsers = len(pbxUsers)
        for i in range(1, noOfUsers+1):
            tb_info['USER'+str(i)+'_NAME'] = pbxUsers[i-1][2]
            tb_info['PPHONE_0'+str(i)+'_ADDR'] = str(pbxUsers[i-1][6])  # for converting None to string None
            bco_config_info['PPHONE_0'+str(i)+'_ADDR'] = str(pbxUsers[i-1][6])
            usrmac_info['USER'+str(i)+'_FIRSTNAME'] = pbxUsers[i-1][2]
            usrmac_info['USER'+str(i)+'_LASTNAME'] = pbxUsers[i-1][3]
            usrmac_info['USER'+str(i)+'_EXTENSION'] = pbxUsers[i-1][4]
            usrmac_info['USER'+str(i)+'_DID'] = str(pbxUsers[i-1][5])
            usrmac_info['USER'+str(i)+'_MAC'] = re.sub('\-', '', str(pbxUsers[i-1][7]))
            # if i == noOfUsers:
            #     break
            # i += 1
        usrmac_info['NUMBER_OF_USERS'] = len(pbxUsers)
        phoneType = self.dbObj.execute_select_query('SELECT type FROM rodexecute_device WHERE name=\'IPPhone\' and testbed_id='+str(tb_id[0][0]))[0][0]
        usrmac_info['PHONE_TYPE'] = str(phoneType)

        ldvsswitchQuery = 'SELECT name FROM rodexecute_device WHERE type=\'SG-LinuxDVS\' and testbed_id='+str(tb_id[0][0])
        ldvsSwitches = self.dbObj.execute_select_query(ldvsswitchQuery)

        i = 1
        for ldvsSwitch in ldvsSwitches:
            bco_config_info['BCO_LINUXDVS_SWITCH'+str(i)+'_NAME'] = ldvsSwitch[0]
            i = i+1
        bco_config_info['HQ_LOGIN_NAME'] = tb_info['MT_D2_LOGINNAME']
        bco_config_info['MT_HQ_SERVER'] = tb_info['MT_D2_LOGINNAME']
        bco_config_info['REVERSE_PROXY_IP'] = tb_info['MT_ABC_AUTHENTICATION_URL']
        bco_config_info['BCO_PPHONE_SITE1_SERVER_ADDR'] = tb_info['MT_D2_SERVER_IP']

        #print(tb_info)
        return tb_info, usrmac_info, bco_config_info

    def fetch_mnm_st_info(self):
        tb_info = dict()
        usrmac_info = dict()
        #tb_info_db = self.select(tb_name)
        pid = self.dbObj.get_project_id(self.input['project'])
        query1 = 'SELECT id FROM rodexecute_testbed WHERE name='+"'"+self.input['testbed_name']+"' and ownedby='"+self.input['user']+"' and project_id='"+str(pid)+"' and type='"+self.input['testbed']['type']+"'"
        print("query1 :", query1)

        tb_id = self.dbObj.execute_select_query(query1)
        print("id:", tb_id[0][0])

        hqQuery = 'SELECT ip, app_user, app_password, os_user, os_password FROM rodexecute_device WHERE name=\'HQ\' and testbed_id='+str(tb_id[0][0])
        print(hqQuery)
        hqInfo = self.dbObj.execute_select_query(hqQuery)
        print("hq info: ", hqInfo)

        tb_info['SITE1_SERVER_ADDR'] = str(hqInfo[0][0])
        tb_info['SITE1_USERNAME'] = str(hqInfo[0][1])
        tb_info['SITE1_PASSWORD'] = str(hqInfo[0][2])
        tb_info['OS_USERNAME'] = str(hqInfo[0][3])
        tb_info['OS_PASSWORD'] = str(hqInfo[0][4])


        ''' fetch user info and add to dict'''
        mnmUsersQuery = 'SELECT * FROM rodexecute_usernames WHERE testbed_id='+str(tb_id[0][0])
        mnmUsers = self.dbObj.execute_select_query(mnmUsersQuery)
        print(mnmUsers)
        noOfUsers = len(mnmUsers)

        for i in range(1, noOfUsers+1):
            tb_info['USER'+str(i)+'_NAME'] = mnmUsers[i-1][2]
            tb_info['PPHONE_0'+str(i)+'_ADDR'] = str(mnmUsers[i-1][6])  # for converting None to string None
            usrmac_info['USER'+str(i)+'_FIRSTNAME'] = mnmUsers[i-1][2]
            usrmac_info['USER'+str(i)+'_LASTNAME'] = mnmUsers[i-1][3]
            usrmac_info['USER'+str(i)+'_EXTENSION'] = mnmUsers[i-1][4]
            usrmac_info['USER'+str(i)+'_DID'] = str(mnmUsers[i-1][5])
            usrmac_info['USER'+str(i)+'_MAC'] = re.sub('\-', '', str(mnmUsers[i-1][7]))

        usrmac_info['NUMBER_OF_USERS'] = len(mnmUsers)
        phoneType = self.dbObj.execute_select_query('SELECT type FROM rodexecute_device WHERE name=\'IPPhone\' and testbed_id='+str(tb_id[0][0]))[0][0]
        usrmac_info['PHONE_TYPE'] = str(phoneType)

        '''fetch testdata and insert into dict'''
        mnmTestDataQuery = 'SELECT * FROM rodexecute_mnmtestdata WHERE testbed_id='+str(tb_id[0][0])
        #print("data query: ", mnmTestDataQuery)
        mnmTestData = self.dbObj.execute_select_query(mnmTestDataQuery)
        print(mnmTestData)
        for i in range(len(mnmTestData)):
            c = i+1
            tb_info['Off_System_Extensions'+str(c)] = mnmTestData[i-1][1]
            print(tb_info['Off_System_Extensions'+str(c)])

        ''' fetch switch info and insert into tb_info'''
        switchQuery = 'SELECT name, ip, type, mac FROM rodexecute_device WHERE type=\'SG-vPhone\' and testbed_id='+str(tb_id[0][0])
        print(switchQuery)
        switches = self.dbObj.execute_select_query(switchQuery)
        print(switches)
        i = 1
        for switch in switches:
            tb_info['SETUP'+str(i)+'_SITE'+str(i)+'_SWITCH'+str(i)+'_NAME'] = switch[0]
            tb_info['SETUP'+str(i)+'_SITE'+str(i)+'_SWITCH'+str(i)+'_ADDR'] = switch[1]
            tb_info['SETUP'+str(i)+'_SITE'+str(i)+'_SWITCH'+str(i)+'_TYPE'] = switch[2]
            tb_info['SETUP'+str(i)+'_SITE'+str(i)+'_SWITCH'+str(i)+'_MAC'] = switch[3]
            i = i+1

        #print("TB INFO IS : ", tb_info)
        #print("USERMAC INFO ", usrmac_info)
        return tb_info , usrmac_info

    def fetch_mnm_mt_info(self, tb_info):
        '''
        :return: will return mnm project test info from mysqql db
        '''
        usrmac_info = dict()
        #tb_info_db = self.select(tb_name)
        pid = self.dbObj.get_project_id(self.input['project'])
        query1 = 'SELECT id FROM rodexecute_testbed WHERE name='+"'"+self.input['testbed_name']+"' and ownedby='"+self.input['user']+"' and project_id='"+str(pid)+"' and type='"+self.input['testbed']['type']+"'"
        # query1 = 'SELECT id FROM rodexecute_testbed WHERE name='+"'"+self.input['testbed_name']+"' and ownedby='"+self.input['user']+"' and project='"+self.input['project']+"' and type='"+self.input['testbed']['type']+"'"
        print("query1 :", query1)

        tb_id = self.dbObj.execute_select_query(query1)
        print("id:", tb_id[0][0])

        hqQuery = 'SELECT ip, app_user, app_password, os_user, os_password FROM rodexecute_device WHERE name=\'HQ\' and testbed_id='+str(tb_id[0][0])
        print(hqQuery)
        hqInfo = self.dbObj.execute_select_query(hqQuery)
        print("hq info: ", hqInfo)

        tb_info['SITE1_SERVER_ADDR'] = str(hqInfo[0][0])
        tb_info['MT_D2_SERVER_IP'] = str(hqInfo[0][0])
        tb_info['MT_D2_LOGINNAME'] = str(hqInfo[0][1])
        tb_info['MT_D2_LOGINPASSWORD'] = str(hqInfo[0][2])
        tb_info['OS_USERNAME'] = str(hqInfo[0][3])
        tb_info['OS_PASSWORD'] = str(hqInfo[0][4])

        ''' fetch user info and add to dict'''
        mnmUsersQuery = 'SELECT * FROM rodexecute_usernames WHERE testbed_id='+str(tb_id[0][0])
        mnmUsers = self.dbObj.execute_select_query(mnmUsersQuery)
        print(mnmUsers)
        noOfUsers = len(mnmUsers)
        for i in range(1, noOfUsers+1):
            tb_info['USER'+str(i)+'_NAME'] = mnmUsers[i-1][2]
            tb_info['PPHONE_0'+str(i)+'_ADDR'] = str(mnmUsers[i-1][6])  # for converting None to string None
            usrmac_info['USER'+str(i)+'_FIRSTNAME'] = mnmUsers[i-1][2]
            usrmac_info['USER'+str(i)+'_LASTNAME'] = mnmUsers[i-1][3]
            usrmac_info['USER'+str(i)+'_EXTENSION'] = mnmUsers[i-1][4]
            usrmac_info['USER'+str(i)+'_DID'] = str(mnmUsers[i-1][5])
            usrmac_info['USER'+str(i)+'_MAC'] = re.sub('\-', '', str(mnmUsers[i-1][7]))

        usrmac_info['NUMBER_OF_USERS'] = len(mnmUsers)
        phoneType = self.dbObj.execute_select_query('SELECT type FROM rodexecute_device WHERE name=\'IPPhone\' and testbed_id='+str(tb_id[0][0]))[0][0]
        usrmac_info['PHONE_TYPE'] = str(phoneType)

        '''fetch testdata and insert into dict'''
        mnmTestDataQuery = 'SELECT * FROM rodexecute_mnmtestdata WHERE testbed_id='+str(tb_id[0][0])
        print("data query: ", mnmTestDataQuery)
        mnmTestData = self.dbObj.execute_select_query(mnmTestDataQuery)
        #print(mnmTestData)

        tb_info['MT_ABC_AUTHENTICATION_URL'] = mnmTestData[0][2]
        tb_info['REVERSE_PROXY_IP_FOR_HOST'] = mnmTestData[0][3]

        ''' fetch switch info and insert into tb_info'''
        switchQuery = 'SELECT name, ip, type, mac FROM rodexecute_device WHERE type=\'SG-vPhone\' and testbed_id='+str(tb_id[0][0])
        print(switchQuery)
        switches = self.dbObj.execute_select_query(switchQuery)
        print(switches)
        i = 1
        for switch in switches:
            tb_info['SETUP'+str(i)+'_SITE'+str(i)+'_SWITCH'+str(i)+'_NAME'] = switch[0]
            tb_info['SETUP'+str(i)+'_SITE'+str(i)+'_SWITCH'+str(i)+'_ADDR'] = switch[1]
            tb_info['SETUP'+str(i)+'_SITE'+str(i)+'_SWITCH'+str(i)+'_TYPE'] = switch[2]
            tb_info['SETUP'+str(i)+'_SITE'+str(i)+'_SWITCH'+str(i)+'_MAC'] = switch[3]
            i = i+1

        ''' fetch tenant info and insert into tb_info dict'''
        tenantQuery = 'SELECT name, tenant_id, prefix FROM rodexecute_tenants WHERE testbed_id='+str(tb_id[0][0])
        tenants = self.dbObj.execute_select_query(tenantQuery)
        tb_info['MT_DEFAULT_TENANT_NAME'] = tenants[0][0]
        tb_info['MT_DEFAULT_TENANT_ID'] = tenants[0][1]
        tb_info['MT_DEFAULT_TENANT_PREFIX'] = tenants[0][2]

        print(tb_info, usrmac_info)
        return tb_info, usrmac_info

    def select(self, tbname):
        row = (1, u'mh-st_10.198.166.44', u'10.198.166.44', u'admin', u'changeme', u'0.0.0.0,1.1.1.1,2.2.2.2')
        return row

if __name__ == '__main__':
    ftb = FetchTbInfoDatabase()
    ftb.fetch_mh_st_info("ok")
