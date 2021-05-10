__author__ = 'Jdhulipalla'

'''
This Module will parse the usermac file and get the user info
Change List : get_usrmac_info_toupdate() and update_usrmac_file() functions added by Uttam ()
'''

from util import config_reader
from class_xml import xmlClass
import os
import re, sys


class UserMacParser():

    def __init__(self, project, usermacPath, logger):
        macdir = r'C:\HCLT\vtftestpkg\vtf\shoretel-test\IPBX-testsuites\test'
        #self.macfile = open(os.path.join(macdir,'usrmacFile.dat')).readlines()
        self.macfile = open(usermacPath).readlines()

        #self.pattern = pattern
        self.project = project
        self.usermacPath = usermacPath
        #self.logger = logger

    def get_user_pattern(self):
        '''
        :return: will return the user pattern based on project
        '''
        #self.logger.debug("Begin")
        patternDict={"pbx":"USER_PSP",
                     "highball":"USER_PSP"}

        if not patternDict[self.project]==self.pattern:
            self.parse_mac(self.pattern)
            return
        self.parse_mac(patternDict[self.project])
        #self.logger.debug("END")

    def parse_mac(self,pattern):
        '''
        :param pattern:
        :return: will parse the user mac file based on user pattern
        '''
        #print(self.macfile)
        #self.logger.debug("Begin")
        userDict={}
        for data in self.macfile:
            if re.search(pattern.upper(),data):
                data=data.split()
                userDict.__setitem__(data[0],dict)
                print("User data is : ", userDict)
                userDict[data[0]]={"MACAddress":data[2],
                                   "LastName":data[1],
                                   "Model":data[3],
                                   "CallManagerSwitch":data[4],
                                   "Extn":data[5],
                                   "SIPTrunkDID":data[6],
                                   "PRITrunkDNIS":data[7],
                                   "UserId":data[9],
                                   "Userpwd":data[10]
                                   }
        #self.logger.debug("END")
        return userDict
    '''
    def parse_usrmac_file(self, patternList):
        """
        """
        print(patternList)
        self.userDict = {}
        self.macfile = [line for line in self.macfile if not line.startswith("#")]
        for pattern in patternList:
            for data in self.macfile:
                if re.search(pattern.upper(),data):
                    data = data.split()
                    self.userDict.__setitem__(data[0],dict)
                    self.userDict[data[0]]={"FirstName":data[0],
                                       "LastName":data[1],
                                       "MACAddress":data[2],
                                       "Model":data[3],
                                       "CallManagerSwitch":data[4],
                                       "Extn":data[5],
                                       "SIPTrunkDID":data[6],
                                       "PRITrunkDNIS":data[7],
                                       "ClientID":data[8],
                                       "Comments":data[9],
                                       "Password":data[10]
                                    }
        #print(userDict)
        #self.logger.debug("END")
        return self.userDict
    '''
    def get_usrmac_info_toupdate(self, tb_info, usrmac_info):
        """
        """
        for key, value in usrmac_info.items():
            if value == 'None':
                usrmac_info[key] = 'NULL'
        if 'PHONE_TYPE' not in usrmac_info.keys():
            usrmac_info['PHONE_TYPE'] = "NULL"

        self.usrmacUpdateDict = dict()
        numberOfUsers = usrmac_info['NUMBER_OF_USERS']
        print("no of users ", numberOfUsers)
        for i in range(1, numberOfUsers+1):
            tempDict = dict()
            tempDict["FirstName"] = usrmac_info['USER'+str(i)+'_FIRSTNAME']
            tempDict["LastName"] = usrmac_info['USER'+str(i)+'_LASTNAME']
            tempDict["MACAddress"] = usrmac_info['USER'+str(i)+'_MAC']
            tempDict["Model"] = usrmac_info['PHONE_TYPE']
            tempDict["CallManagerSwitch"] = 'PPHONE_0'+str(i)+'_ADDR'
            tempDict["Extn"] = usrmac_info['USER'+str(i)+'_EXTENSION']
            tempDict["SIPTrunkDID"] = usrmac_info['USER'+str(i)+'_DID'].rstrip("+1")
            tempDict["PRITrunkDNIS"] = usrmac_info['USER'+str(i)+'_DID'].rstrip("+")
            tempDict["ClientID"] = '10UHQSW13'
            tempDict["Password"] = '10UHQSW13'

            self.usrmacUpdateDict[usrmac_info['USER'+str(i)+'_FIRSTNAME']] = tempDict

        print("usrmac dict ", self.usrmacUpdateDict)
        return self.usrmacUpdateDict

    def update_usrmac_file(self, usrmacInfoToUpdate):
        #print(self.usrmacUpdateDict)
        for fname in usrmacInfoToUpdate.keys():
            for line in self.macfile:
                if fname in line:
                    self.macfile.remove(line)
                    break

        for key, value in usrmacInfoToUpdate.items():
            line = value["FirstName"]+"   "+value["LastName"]+"   "+value["MACAddress"]+"   "+value["Model"]+\
                   "   "+value["CallManagerSwitch"]+"   "+value["Extn"]+"   "+value["SIPTrunkDID"]+\
                   "   "+value["PRITrunkDNIS"]+"   "+value["Extn"]+"   "+value["ClientID"]+"   "+value["Password"]
            self.macfile.append(line)

        fObj = open(self.usermacPath, "w")
        for line in self.macfile:
            fObj.write(line+"\n")
        fObj.close()




if __name__ == "__main__":
    macobj = UserMacParser("mobility", r'C:\HCLT\vtftestpkg\vtf\shoretel-test\IPBX-testsuites\test\usrmacFile.dat', None)
    macobj.get_usrmac_info_toupdate(None)
    ##l = macobj.create_usrmac_dict()
    ##macobj.parse_mac_file(l)
    #macobj.parse_mac("user_psp2")
    ##macobj.update_usrmac()