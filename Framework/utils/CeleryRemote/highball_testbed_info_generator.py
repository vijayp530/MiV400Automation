'''
Created on Dec 09, 2015

@author: UKumar
'''

import sys
from class_xml import xmlClass


class GenerateHighballTestbedInfo:
    """
    classdocs
    """

    def __init__(self, logger):
        '''
        Constructor
        '''
        self.logger = logger

    '''
    def xml_reader(self, fileName):
        """
        """
        with open(fileName) as fd:
            dictObj = xmltodict.parse(fd.read())
        dictObj = json.loads(json.dumps(dictObj))
        return dictObj
    '''

    def get_testbed_info_highball(self, inputDict, tbType):
        """
        """
        highball_tb_dict = {}

        #tbDict = self.xml_reader("C:\NextGenArc\etc\configs\hb_ST_tb5.config") #inputxml)
        #xobj = xmlClass(r'C:\NextGenArc\xmlFiles\private\hb_MT_tb5.xml')

        #inputDict = xobj.GetAllChildrenAnyDepth(xobj.FindNode("./SHORETELIPBX/MT"))

        if tbType == "ST":
            highball_tb_dict = self.highball_st_parser(inputDict)
        else:
            highball_tb_dict = self.highball_mt_parser(inputDict)
        self.logger.debug(highball_tb_dict)
        return highball_tb_dict

    def highball_st_parser(self, tbDict):
        """
        """
        tmpHBDict = tbDict
        regAgentInfo = self.get_reg_agent_info(tbDict)
        tmpHBDict.update(regAgentInfo)
        regGroupInfo = self.get_reg_group_info(tbDict)
        tmpHBDict.update(regGroupInfo)
        regServiceInfo = self.get_reg_service_info(tbDict)
        tmpHBDict.update(regServiceInfo)
        self.logger.debug(tmpHBDict)
        return tmpHBDict

    def highball_mt_parser(self, tbDict):
        """
        """
        tmpHBDict = tbDict
        supInfo = self.get_sup_pwd_info(tbDict)
        tmpHBDict.update(supInfo)
        tenantSupInfo = self.get_tenant_sup_pwd_info(tbDict)
        tmpHBDict.update(tenantSupInfo)
        mtBcoAgentInfo = self.get_mt_bco_agent_info(tbDict)
        tmpHBDict.update(mtBcoAgentInfo)
        tmpHBDict["BCO_SUP_PWD"] = 'changeme'
        self.logger.debug(tmpHBDict)
        return tmpHBDict

    def get_reg_agent_info(self, tbDict):
        tmpDict = dict()
        iterations = int(tbDict["ST_REG_AGENTS_COUNT"])
        for i in range(1, iterations+1):
            tmpDict["ST_REG_AGENT"+str(i)+"_NAME"] = tbDict["ST_REG_AGENTS_NAME_PREFIX"]+str(i)
            tmpDict["ST_REG_AGENT"+str(i)+"_FULLNAME"] = tbDict["ST_REG_AGENTS_FULLNAME_PREFIX"]+str(i)
            tmpDict["ST_REG_AGENT"+str(i)+"_UNAME"] = tbDict["ST_REG_AGENTS_USERNAME_PREFIX"]+str(i)
            tmpDict["ST_REG_AGENT"+str(i)+"_PWD"] = 'changeme'
            tmpDict["ST_REG_AGENT"+str(i)+"_ID"] = tbDict["ST_REG_AGENTS_ID_PREFIX"]+str(i)
        return tmpDict

    def get_reg_group_info(self, tbDict):
        tmpDict = dict()
        for i in range(1, int(tbDict["ST_REGRESSION_GROUPS_COUNT"])+1):
            tmpDict["ST_REG"+str(i)+"_GROUP"] = "ST_WA_Grp"+str(i)
        return tmpDict

    def get_reg_service_info(self, tbDict):
        tmpDict = dict()
        tmpDict["ST_REG_SERVICE"] = "ST_WA_Srv1"
        for i in range(2, int(tbDict["ST_REGRESSION_SERVICES_COUNT"])+1):
            tmpDict["ST_REG_SERVICE"+str(i)] = "ST_WA_Srv"+str(i)
        #print(tmpDict)
        return tmpDict

    def get_sup_pwd_info(self, tbDict):
        tmpDict = dict()
        tmpDict["HB_GLOBAL_SUPERVISOR_PWD"] = 'changeme'
        tmpDict["HB_SUPERVISOR_PWD"] = 'changeme'
        return tmpDict

    def get_tenant_sup_pwd_info(self, tbDict):
        tmpDict = dict()
        numberDict = {"1":"ONE", "2":"TWO", "3":"THREE", "4":"FOUR", "5":"FIVE",
                      "6":"SIX", "7":"SEVEN", "8":"EIGHT", "9":"NINE"}

        iterations = int(tbDict["TENANT_SUPERVISORS_COUNT"])
        for i in range(1, iterations+1):
            tmpDict["HB_TENANT_"+numberDict[str(i)]+"_SUPERVISOR1_PWD"] = 'changeme'

        tmpDict["HB_TENANT_USER3_SUPERVISOR1_PWD"] = 'changeme'
        tmpDict["HB_TENANT_USER3_SUPERVISOR2_PWD"] = 'changeme'
        return tmpDict

    def get_mt_bco_agent_info(self, tbDict):
        tmpDict = dict()
        tmpDict["BCO_AGENT_NAME"] = tbDict["BCO_AGENTS_NAME_PREFIX"]+str(1)
        tmpDict["BCO_AGENT_UNAME"] = tbDict["BCO_AGENTS_NAME_PREFIX"]+str(1)+"@mt.com"
        tmpDict["BCO_AGENT_PWD"] = 'changeme'
        #tmpDict["BCO_AGENT_ID"] = tbDict["TESTBED"]["MT_BCO_AGENTS"]["BCO_AGENT_ID"]
        iterations = int(tbDict["BCO_AGENTS_COUNT"])
        for i in range(1, iterations):
            tmpDict["BCO_AGENT"+str(i)+"_NAME"] = tbDict["BCO_AGENTS_NAME_PREFIX"]+str(i+1)
            tmpDict["BCO_AGENT"+str(i)+"_UNAME"] = tbDict["BCO_AGENTS_NAME_PREFIX"]+str(i+1)+"@mt.com"
            tmpDict["BCO_AGENT"+str(i)+"_PWD"] = 'changeme'
        #print(tmpDict)
        return tmpDict

    '''
    def get_hq_info_st(self, tbDict):
        tmpDict = dict()
        tmpDict["SITE1_SERVER_ADDR"] = tbDict["TESTBED"]["SHORETELIPBX"]["SITE1_SERVER_ADDR"]["#text"]
        tmpDict["SITE1_USERNAME"] = tbDict["TESTBED"]["SHORETELIPBX"]["SITE1_USERNAME"]["#text"]
        tmpDict["SITE1_PASSWORD"] = tbDict["TESTBED"]["SHORETELIPBX"]["SITE1_PASSWORD"]["#text"]
        tmpDict["SITE2_SERVER_ADDR"] = tbDict["TESTBED"]["SHORETELIPBX"]["SITE2_SERVER_ADDR"]["#text"]
        tmpDict["SITE2_USERNAME"] = tbDict["TESTBED"]["SHORETELIPBX"]["SITE2_USERNAME"]["#text"]
        tmpDict["SITE2_PASSWORD"] = tbDict["TESTBED"]["SHORETELIPBX"]["SITE2_PASSWORD"]["#text"]
        return tmpDict

    def get_hq_info_mt(self, tbDict):
        tmpDict = dict()
        tmpDict["SITE1_SERVER_ADDR"] = tbDict["TESTBED"]["SHORETELIPBX"]["SITE1_SERVER_ADDR"]["#text"]
        tmpDict["MT_D2_LOGINNAME"] = tbDict["TESTBED"]["SHORETELIPBX"]["MT_D2_LOGINNAME"]["#text"]
        tmpDict["MT_D2_LOGINPASSWORD"] = tbDict["TESTBED"]["SHORETELIPBX"]["MT_D2_LOGINPASSWORD"]["#text"]
        tmpDict["SITE2_SERVER_ADDR"] = tbDict["TESTBED"]["SHORETELIPBX"]["SITE2_SERVER_ADDR"]["#text"]
        #tmpDict["SITE2_USERNAME"] = tbDict["TESTBED"]["SHORETELIPBX"]["SITE2_USERNAME"]["#text"]
        #tmpDict["SITE2_PASSWORD"] = tbDict["TESTBED"]["SHORETELIPBX"]["SITE2_PASSWORD"]["#text"]
        return tmpDict

    def get_phone_info(self, tbDict):
        tmpDict = dict()
        for i in range(1, len(tbDict["TESTBED"]["SHORETELIPBX"]["PHONES"].keys())):
            tmpDict["PPHONE_0"+str(i)+"_ADDR"] = tbDict["TESTBED"]["SHORETELIPBX"]["PHONES"]["PPHONE_0"+str(i)+"_ADDR"]
        #print(tmpDict)
        return tmpDict

    def get_ip_port_info(self, tbDict):
        tmpDict = dict()
        tmpDict["ST_HIGHBALL_IP_URL"] = tbDict["TESTBED"]["SHORETELIPBX"]["ST_HIGHBALL_IP_URL"]["#text"]
        tmpDict["ST_HIGHBALL_PORT_URL"] = tbDict["TESTBED"]["SHORETELIPBX"]["ST_HIGHBALL_PORT_URL"]["#text"]
        tmpDict["ST_WEBAGENT_IP_URL"] = tbDict["TESTBED"]["SHORETELIPBX"]["ST_WEBAGENT_IP_URL"]["#text"]
        tmpDict["ST_WEBAGENT_PORT_URL"] = tbDict["TESTBED"]["SHORETELIPBX"]["ST_WEBAGENT_PORT_URL"]["#text"]
        tmpDict["ST_WEBAGENT_PORT2_URL"] = tbDict["TESTBED"]["SHORETELIPBX"]["ST_WEBAGENT_PORT2_URL"]["#text"]
        #print(tmpDict)
        return tmpDict

    def get_webagent_sup_info(self, tbDict):
        tmpDict = dict()
        tmpDict["ST_REG_SUP_COS_NAME"] = tbDict["TESTBED"]["SHORETELIPBX"]["ST_REG_SUP_COS_NAME"]["#text"]
        tmpDict["ST_REG_SUP_NAME"] = tbDict["TESTBED"]["SHORETELIPBX"]["ST_REG_SUP_NAME"]["#text"]
        tmpDict["ST_REG_SUP_UNAME"] = tbDict["TESTBED"]["SHORETELIPBX"]["ST_REG_SUP_UNAME"]["#text"]
        tmpDict["ST_REG_SUP_PWD"] = 'changeme'
        #print(tmpDict)
        return tbDict

    def get_reg_irn_info(self, tbDict):
        tmpDict =dict()
        #print(len(tbDict["TESTBED"]["ST_REGRESSION_IRNS"].keys()))
        for i in range(1, len(tbDict["TESTBED"]["SHORETELIPBX"]["ST_REGRESSION_IRNS"].keys())):
            tmpDict["ST_REG_IRN"+str(i)] = tbDict["TESTBED"]["SHORETELIPBX"]["ST_REGRESSION_IRNS"]["ST_REG_IRN"+str(i)]
        #print(tmpDict)
        return tmpDict

    def get_tenant_info(self, tbDict):
        tmpDict = dict()
        numberDict = {"1":"ONE", "2":"TWO", "3":"THREE", "4":"FOUR", "5":"FIVE",
                      "6":"SIX", "7":"SEVEN", "8":"EIGHT", "9":"NINE"}
        iterations = len(tbDict["TESTBED"]["SHORETELIPBX"]["TENANTS"].keys()) - 5
        for i in range(1, iterations):
            tmpDict["HB_TENANT_"+numberDict[str(i)]] = tbDict["TESTBED"]["SHORETELIPBX"]["TENANTS"]["HB_TENANT_"+numberDict[str(i)]]["#text"]

        tmpDict["DEFAULT_TENANT_NAME"] = tbDict["TESTBED"]["SHORETELIPBX"]["TENANTS"]["DEFAULT_TENANT_NAME"]["#text"]
        tmpDict["DEFAULT_TENANT_ID"] = tbDict["TESTBED"]["SHORETELIPBX"]["TENANTS"]["DEFAULT_TENANT_ID"]["#text"]
        tmpDict["DEFAULT_TENANT_PREFIX"] = tbDict["TESTBED"]["SHORETELIPBX"]["TENANTS"]["DEFAULT_TENANT_PREFIX"]["#text"]
        tmpDict["MT_SYSTEM_TENANT_ID"] = tbDict["TESTBED"]["SHORETELIPBX"]["TENANTS"]["MT_SYSTEM_TENANT_ID"]["#text"]
        tmpDict["MT_SYSTEM_TENANT_SITE_NAME"] = tbDict["TESTBED"]["SHORETELIPBX"]["TENANTS"]["MT_SYSTEM_TENANT_SITE_NAME"]["#text"]
        #print(tmpDict)
        return tmpDict

    def get_bco_sup_info(self, tbDict):
        tmpDict = dict()
        tmpDict["BCO_SUP_COS_NAME"] = tbDict["TESTBED"]["SHORETELIPBX"]["BCO_SUPERVISOR"]["BCO_SUP_COS_NAME"]["#text"]
        tmpDict["BCO_SUP_NAME"] = tbDict["TESTBED"]["SHORETELIPBX"]["BCO_SUPERVISOR"]["BCO_SUP_NAME"]["#text"]
        tmpDict["BCO_SUP_UNAME"] = tbDict["TESTBED"]["SHORETELIPBX"]["BCO_SUPERVISOR"]["BCO_SUP_UNAME"]["#text"]
        tmpDict["BCO_SUP_PWD"] = 'changeme'
        print(tmpDict)
        return tmpDict

    def get_mt_irn(self, tbDict):
        tmpDict = dict()
        for i in range(1, len(tbDict["TESTBED"]["SHORETELIPBX"]["MT_IRNS"]["BCO_IRNS"].keys())):
            tmpDict["BCO_IRN"+str(i)] = tbDict["TESTBED"]["SHORETELIPBX"]["MT_IRNS"]["BCO_IRNS"]["BCO_IRN"+str(i)]
        for i in range(1, len(tbDict["TESTBED"]["SHORETELIPBX"]["MT_IRNS"]["IRNS"].keys())):
            tmpDict["IRN_0"+str(i)] = tbDict["TESTBED"]["SHORETELIPBX"]["MT_IRNS"]["IRNS"]["IRN_0"+str(i)]
        #print(tmpDict)
        return tmpDict

    def get_port(self, tbDict):
        tmpDict = dict()
        for i in range(1, len(tbDict["TESTBED"]["SHORETELIPBX"]["PORTS"].keys())):
            tmpDict["PORT"+str(i)] = tbDict["TESTBED"]["SHORETELIPBX"]["PORTS"]["PORT"+str(i)]
        #print(tmpDict)
        return tmpDict
    '''









if __name__ == "__main__":
    s = GenerateHighballTestbedInfo(None)
    s.get_testbed_info_highball(None, "MT")
    #s.parse_input_xml("vha_manhattan_tb5")