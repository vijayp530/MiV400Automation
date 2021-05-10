'''
Created on Nov 30, 2015

@author: UKumar
'''
import os, re, sys, collections
import shutil
from class_xml import xmlClass
from usermac_parser import UserMacParser
from ipbx_updater import ShoretelIPBXUpdater
from highball_testbed_info_generator import GenerateHighballTestbedInfo
from windows_machine import WindowsMachine, create_file
from file_handler import FileHandler
from system_db_handler import SystemDBHandler
from config_reader import ConfigReader
from fetch_testbed_info import FetchTestbedInfo
from fetch_tb_info_db import FetchTbInfoDatabase


class PrivateTestbed():
    '''
    classdocs
    '''

    def __init__(self, gConf, input, logger):
        '''
        Constructor
        '''
        self.gConf = gConf
        self.logger = logger
        self.input = input
        self.logger.debug("Begin")
        self.configReader = ConfigReader(self.logger)
        self.rod_server_info = self.configReader.get_rod_server_info(self.gConf)
        self.remoteDir = self.rod_server_info['XML_FILE_DIR']
        self.localDir = self.configReader.get_local_xml_path(self.gConf)
        self.systemdbPath = self.configReader.get_systemdb_path(self.gConf)
        print("self.localDir: ",self.localDir)
        print("Project is : ", self.input['project'])

        self.fileObj = FileHandler()
        print("Start", self.input['testbed']['type'])
        if self.input['setup_type'].lower() == 'private':
            self.fetchFromDb = FetchTbInfoDatabase(self.input, self.logger)

            #self.get_testbed_info_file()
            #sys.exit(0)
            self.xmlObj = xmlClass(self.localDir+"private\\"+self.get_gold_file_name())
            if self.input['project'].lower() != 'cosmo-pseries':
                #self.xmlObj = xmlClass(self.localDir+self.get_gold_file_name())
                self.testbedInfoDict = self.parse_testbed_xml(self.input['testbed']['type'])

                tempdict = dict()
                self.xmlObj.GetAllAttrib(self.xmlObj.FindNode('SHORETELIPBX'), tempdict)
                self.shoretelIPBXPath = tempdict["PATH"]+"\shoretelIPBXConfig.dat"
                self.xmlObj.GetAllAttrib(self.xmlObj.FindNode('USRMAC'), tempdict)
                self.usrmacPath = tempdict["PATH"]+"\usrmacFile.dat"

                if self.input['project'].lower() == 'cosmo-pbx':
                    self.xmlObj.GetAllAttrib(self.xmlObj.FindNode('BCO'), tempdict)
                    self.bcoConfigPath = tempdict["PATH"]+"\BCOConfig.dat"

                self.ipbxupdate = ShoretelIPBXUpdater(self.shoretelIPBXPath, self.logger)
                self.highballTBInfo = GenerateHighballTestbedInfo(self.logger)
                self.usermacParser = UserMacParser(input['project'], self.usrmacPath, self.logger)

                self.backup_conf_files(self.shoretelIPBXPath, self.usrmacPath)
                print("Backup done")

            def func_not_found():
                print("No Function Found, Please Check the Name!")

            projectType = re.sub(r'\-', '_', self.input['project'].lower())
            projectType = re.sub(r'\&', 'n', projectType)
            updater_func = getattr(self, projectType+"_updater", func_not_found)
            updater_func()
            print("End")
        else:
            self.logger.debug("You selected Default option!")
        self.logger.debug("End")

    def copy_cert_files(self):
        self.logger.debug("Begin")
        if self.input['testbed']['type'] == "MT":
            print("inside add pre")
            self.fileObj.copy_certificate_files(self.testbedInfoDict['MT_D2_SERVER_IP'], self.testbedInfoDict['OS_USERNAME'], self.testbedInfoDict['OS_PASSWORD'], self.input)
            self.fileObj.add_reverse_proxy(self.testbedInfoDict)
        self.logger.debug("End")

    def get_gold_file_name(self):
        self.logger.debug("Begin")
        gold_file_name_dict = {"manhattan":"manhattan_private_tbGold.xml",
                               "highball":"highball_private_tbGold.xml",
                               "mobility":"mobility_private_tbGold.xml",
                               "cosmo-pbx":"pbx_private_tbGold.xml",
                               "cosmo-pseries":"pseries_private_tbGold.xml",
                               "m&m":"mnm_private_tbGold.xml"
                               }
        self.logger.debug("End")
        return gold_file_name_dict[self.input['project'].lower()]


    '''def get_testbed_info_file(self):
        """
        """
        self.logger.info("Retrieving testbed info file from server...")
        self.fileObj.sftp_xml_file(self.rod_server_info['IP'], self.rod_server_info['USER'],
                                   self.rod_server_info['PASSWORD'], self.localDir,
                                   self.input['testbed_info_xml'], self.remoteDir
                                  )
        if self.input['project'].lower() == "cosmo-pseries" and self.input['new_atf'] == True:
            self.fileObj.sftp_xml_file(self.rod_server_info['IP'], self.rod_server_info['USER'],
                                       self.rod_server_info['PASSWORD'], self.localDir,
                                       self.input['atf_xml'], self.remoteDir
                                      )
        self.logger.info("File Retrieved")'''

    def backup_conf_files(self, shoretelIPBXPath, usrmacPath):
        """ Takes backup of files for default setup
        """
        self.logger.debug("Begin")
        self.copy_file(shoretelIPBXPath, self.localDir+"default\ShoretelIPBXConfig.dat")
        self.copy_file(usrmacPath, self.localDir+"default\usrmacFile.dat")
        self.logger.debug("End")

    def replace_conf_files(self):
        """ replaces the conf files with backup ones
        """
        self.logger.debug("Begin")
        if self.input['setup_type'].lower() == 'private':
            if self.input['project'].lower() == "cosmo-pseries":
                self.copy_file(self.localDir+"default\system.db", self.systemdbPath+"system.db")
                self.copy_file(self.localDir+"default\system.db.runtime", self.systemdbPath+"system.db.runtime")
                self.logger.info("Replacement of database files done")
            else:
                self.copy_file(self.localDir+"default\ShoretelIPBXConfig.dat", self.shoretelIPBXPath)
                self.copy_file(self.localDir+"default\usrmacFile.dat", self.usrmacPath)
                if self.input['project'].lower() == "cosmo-pbx":
                    self.copy_file(self.localDir+"default\BCOConfig.dat", self.bcoConfigPath)
                self.logger.info("Replacement of config files done")
        else:
            self.logger.info("Choice is default, replacement of config files not required.")
        self.logger.debug("End")

    def copy_file(self, src, dst):
        """Copies from src to dst
        src and dst are source and destination file paths
        Ex : src = "C:\\Users\\ukumar\\Desktop\\tmp\\NextGenArc\\ngnarc.py"
             dst = "C:\\Users\\ukumar\\Desktop\\NextGenArc\\ngnarc.py"
        """
        self.logger.debug("Copy Initiated")
        shutil.copy2(src, dst)
        self.logger.debug("Copy Completed")

    def parse_testbed_xml(self, tbType):
        """
        Author : Uttam
        returns configuration parameters from testbed config file
        """
        self.logger.debug("Begin")
        tbInfo = dict()
        if tbType == "ST":
            tbInfo = self.xmlObj.GetAllChildrenAnyDepth(self.xmlObj.FindNode("./SHORETELIPBX/ST"))
        else:
            tbInfo = self.xmlObj.GetAllChildrenAnyDepth(self.xmlObj.FindNode("./SHORETELIPBX/MT"))
            if self.input['project'].lower() == 'cosmo-pbx':
                tbInfo = self.xmlObj.GetAllChildrenAnyDepth(self.xmlObj.FindNode("./BCO"))
        self.logger.debug(tbInfo)
        self.logger.debug("End")
        return tbInfo

    def manhattan_updater(self):
        '''Updates ShoretelIPBXConfig.dat and usramcfile.dat file for Manhattan
        '''
        self.logger.info("Updating ShoretelIPBXConfig.dat file for Manhattan")
        #testbedInfoDict = self.parse_testbed_xml(self.input['testbed']['type'])
        print("testbed info dict is : ", self.testbedInfoDict)

        if self.input['testbed']['type'] == "MT":
            print("inside MT")
            self.testbedInfoDict = self.fetchFromDb.fetch_mh_mt_info(self.testbedInfoDict)
            self.testbedInfoDict['MT_D2_DOMAIN'] = self.testbedInfoDict['MT_D2_LOGINNAME'].split("@")[1]
            self.copy_cert_files()
        else:
            self.testbedInfoDict = self.fetchFromDb.fetch_mh_st_info()
            fetchFromHQ = FetchTestbedInfo(self.testbedInfoDict['SITE1_SERVER_ADDR'], self.testbedInfoDict['SITE1_USERNAME'], self.testbedInfoDict['SITE1_PASSWORD'])
            self.testbedInfoDict = fetchFromHQ.fetch_testbed_info_manhattn(self.testbedInfoDict)
            print("info is : ", self.testbedInfoDict)
        ipbxDict = self.ipbxupdate.create_ipbx_dict()
        self.ipbxupdate.update_ipbx_file(ipbxDict, self.testbedInfoDict)
        self.logger.info("Updating files Done.")

    def highball_updater(self):
        '''Updates ShoretelIPBXConfig.dat and usramcfile.dat file for Highball
        '''
        self.logger.info("Updating ShoretelIPBXConfig.dat and usrmacFile.dat file for Highball")
        testbedInfoHighballDict = self.highballTBInfo.get_testbed_info_highball(self.testbedInfoDict, self.input['testbed']['type'])

        ipbxDict = self.ipbxupdate.create_ipbx_dict()
        self.ipbxupdate.update_ipbx_file(ipbxDict, testbedInfoHighballDict)
        usrmacInfoToUpdate = self.usermacParser.get_usrmac_info_toupdate(self.xmlObj)
        self.usermacParser.update_usrmac_file(usrmacInfoToUpdate)
        self.logger.info("Updating Done.")
        
    def mobility_updater(self):
        '''Updates ShoretelIPBXConfig.dat and usramcfile.dat file for Mobility
        '''
        self.logger.info("Updating ShoretelIPBXConfig.dat and usrmacFile.dat file for Mobilbity")

        if self.input['testbed']['type'] == "MT":
            print("inside MT")
        else:
            self.testbedInfoDict, usrmacInfoDict = self.fetchFromDb.fetch_mb_st_info(self.testbedInfoDict)
            fetchFromHQ = FetchTestbedInfo(self.testbedInfoDict['SITE1_SERVER_ADDR'], self.testbedInfoDict['SITE1_USERNAME'], self.testbedInfoDict['SITE1_PASSWORD'])
            self.testbedInfoDict = fetchFromHQ.fetch_testbed_info_mobility(self.testbedInfoDict)
            self.testbedInfoDict['SERVER_ADDRESS'] = self.testbedInfoDict['SMR_IP_ADDR']
            #print("info is : ", self.testbedInfoDict)
            #print("usr mac info  is : ", usrmacInfoToUpdate)
        ipbxDict = self.ipbxupdate.create_ipbx_dict()
        self.ipbxupdate.update_ipbx_file(ipbxDict, self.testbedInfoDict)
        usrmacInfoToUpdate = self.usermacParser.get_usrmac_info_toupdate(self.testbedInfoDict, usrmacInfoDict)
        self.usermacParser.update_usrmac_file(usrmacInfoToUpdate)
        self.logger.info("Updating Done.")
        
    def cosmo_pseries_updater(self):
        '''Updates ShoretelIPBXConfig.dat and usramcfile.dat file for PSeries
        '''
        self.logger.info("Updating system.db file for PSeries")
        self.copy_file(self.systemdbPath+"system.db", self.localDir+"default\system.db")
        self.copy_file(self.systemdbPath+"system.db.runtime", self.localDir+"default\system.db.runtime")
        sysDBHandler = SystemDBHandler(self.input, self.xmlObj, self.systemdbPath, self.logger)
        sysDBHandler.handle_system_db()
        
        if os.path.exists(self.systemdbPath+"system.db.runtime"):
            os.remove(self.systemdbPath+"system.db.runtime")
        shutil.copy2(self.systemdbPath+"system.db", self.systemdbPath+"system.db.runtime")
        os.system(r'Q:\scripts\squishAutConfig.pl')
        self.logger.info("Updating system.db Done.")
        
    def cosmo_pbx_updater(self):
        '''Updates ShoretelIPBXConfig.dat and usramcfile.dat file for PBX
        '''
        self.logger.info("Updating ShoretelIPBXConfig.dat and usrmacFile.dat file for PBX")
        #testbedInfoDict = self.parse_testbed_xml(self.input['testbed']['type'])
        #print("testbed info dict is : ", self.testbedInfoDict)

        if self.input['testbed']['type'] == "MT":
            print("inside MT")
            self.testbedInfoDict, usrmac_info, bco_config_info = self.fetchFromDb.fetch_pbx_mt_info(self.testbedInfoDict)
            self.copy_cert_files()
        else:
            print("No ST info")

        ipbxDict = self.ipbxupdate.create_ipbx_dict()
        self.ipbxupdate.update_ipbx_file(ipbxDict, self.testbedInfoDict)
        usrmacInfoToUpdate = self.usermacParser.get_usrmac_info_toupdate(self.testbedInfoDict, usrmac_info)
        self.usermacParser.update_usrmac_file(usrmacInfoToUpdate)
        self.ipbxupdate.update_bco_cgf(self.bcoConfigPath, bco_config_info)
        self.logger.info("Updating files Done.")

    def mnm_updater(self):
        '''Updates ShoretelIPBXConfig.dat and usramcfile.dat file for MnM
        '''
        self.logger.info("Updating ShoretelIPBXConfig.dat file for MnM")

        usrmacInfoDict = dict()
        print(self.testbedInfoDict)
        if self.input['testbed']['type'] == "MT":
            self.testbedInfoDict, usrmacInfoDict= self.fetchFromDb.fetch_mnm_mt_info(self.testbedInfoDict)
            self.copy_cert_files()
        else:
            self.testbedInfoDict, usrmacInfoDict = self.fetchFromDb.fetch_mnm_st_info()

        ipbxDict = self.ipbxupdate.create_ipbx_dict()
        self.ipbxupdate.update_ipbx_file(ipbxDict, self.testbedInfoDict)
        # for MnM updation, of usrmacFile.dat is not required right now
        #usrmacInfoToUpdate = self.usermacParser.get_usrmac_info_toupdate(self.testbedInfoDict, usrmacInfoDict)
        #self.usermacParser.update_usrmac_file(usrmacInfoToUpdate)
        self.logger.info("Updating files Done.")

        
if __name__ == "__main__":
    input = {"testbed":{"name":"cosmo_pseries_tb1", "type":"MT", "hq_ip":"10.198.107.18"}, "action":"execute", "suite":"REGRESSION",
             "project":"Cosmo-PSeries", "setup_type":"Private", "testbed_name":"PseriesMttbUttam"}

    s = PrivateTestbed(None, input, None)
    #s = PrivateTestbed(None, None)
    #s.parse_mapping_xml("ST")
    #s.parse_input_xml_manhattan("C:\NextGenArc\etc\configs\manhattan_private_tb.xml", "MT")



    # def fetch_info_from_hq_manhattan(self, testbedInfo):
    #     print(testbedInfo["SITE1_SERVER_ADDR"], testbedInfo["HQ_USERNAME_REMOTE_CONNECT"], testbedInfo["HQ_PASSWORD_REMOTE_CONNECT"])
    #     remote_path = 'c:\\'
    #     ST = collections.OrderedDict()
    #     MT = collections.OrderedDict()
    #     ST = {'select SwitchName from switches':['SETUP1_SITE1_SWITCH1_NAME'],'select SwitchName from switches':['SETUP1_SITE1_SWITCH2_NAME'], 'select SwitchName from switches':['SETUP1_SITE1_SWITCH3_NAME']}
    #     ##MT = {'select TenantPrefix from tenantprefixes where TenantID='+testbedInfo['MT_SYSTEM_TENANT_ID']:['MT_DEFAULT_TENANT_PREFIX'],'select TenantName from tenants where TenantID='+testbedInfo['MT_SYSTEM_TENANT_ID']:['MT_DEFAULT_TENANT_NAME']}
    #     text = ''
    #     delimiter_for_query_result = "\nselect '' as '';\n"
    #     for k in ST if self.input['testbed']['type']=='ST' else MT:
    #         text+=k+';'+delimiter_for_query_result
    #     print(text)
    #     wd = os.getcwd()
    #     script_local_path = os.path.join(wd, 'script.sql')
    #     create_file(script_local_path, text)
    #
    #     hq_wmi = WindowsMachine(testbedInfo["SITE1_SERVER_ADDR"], testbedInfo["HQ_USERNAME_REMOTE_CONNECT"], testbedInfo["HQ_PASSWORD_REMOTE_CONNECT"])
    #     hq_wmi.net_copy(script_local_path, remote_path)
    #     hq_wmi.run_remote('''"C:\Program Files (x86)\Shoreline Communications\ShoreWare Server\MySQLConfig\MySQL Server\\bin\mysql.exe" -uroot -pshorewaredba shoreware < c:\script.sql ''')
    #     print("output file is : ", wd+"\util\\"+hq_wmi.out+'.out')
    #     hq_wmi.net_copy_back('C:\\'+hq_wmi.out+'.out',wd+"\util\\"+hq_wmi.out+'.out')
    #     hq_wmi.net_delete('C:\\'+hq_wmi.out+'.out')
    #     ##hq_wmi.net_copy_back('C:\\'++'.out',wd+hq_wmi.out+'.out')
