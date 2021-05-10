__author__ = 'Jahnavi'
'''This module will handle with phone to capture phone logs'''


from util import config_updater
from util import usermac_parser
class PhoneHandler():
    def __init__(self,input,vtfExecutors,project,pattern,logger):
        self.pattern=pattern
        self.ipbxconf=config_updater.ConfigUpdater(input,vtfExecutors,logger)
        self.usermac=usermac_parser.UserMacParser(project,pattern,logger)
        self.logger=logger

    def get_phone_ip(self):
        '''

        :return:will return the phone user and its ip
        '''
       # self.logger.debug("Begin")
        userDict=self.usermac.parse_mac(self.pattern)
        ipbxDict=self.ipbxconf.parse_config_dat(r'C:\HCLT\vtftestpkg\vtf\TAF\conf\shoretelIPBXConfig.dat')
        #print("user mac ",userDict)
        #print("ipbx ",ipbxDict)
        user_ip_dict={}
        for user,details in userDict.items():
            #print(user)
            #print(details["CallManagerSwitch"])
            if details["CallManagerSwitch"].lower() in ipbxDict.keys():
                #print(ipbxDict[details["CallManagerSwitch"].lower()])
                user_ip_dict.__setitem__(user,ipbxDict[details["CallManagerSwitch"].lower()])
        print(user_ip_dict)

    def phone_login(self):
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(remoteHost, username=username, password=password)







phObj=PhoneHandler("input","vtf","pbx","user_psp2","logger")
phObj.get_phone_ip()

