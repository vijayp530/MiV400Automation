import os
import re

class ConfigUpdater():
    
    def __init__(self,input,vtfExecutors,logger):
        
       self.vtfExecutors=vtfExecutors
       self.logger = logger
       self.input=input
       
    def update_dat_files(self):
        '''get the config.dat files from VTF machines modify with the specified values'''
        
        self.source_file={"shoretelipbx":r'C:\HCLT\vtftestpkg\vtf\TAF\conf\shoretelIPBXConfig.dat',
                   "bcoConfig":r'C:\HCLT\vtftestpkg\vtf\TAF\conf\BCOConfig.dat'
                   }
        
        for vtf in self.vtfExecutors:
            lconf1 = os.path.join(r'etc\tmp', vtf.Worker.workerName, 'shoretelIPBXConfig.dat')
            if not os.path.exists(os.path.dirname(lconf1)):
                os.makedirs(os.path.dirname(lconf1))
            lconf2 = os.path.join(r'etc\tmp', vtf.Worker.workerName, 'BCOConfig.dat')
            if not os.path.exists(os.path.dirname(lconf2)):
                os.makedirs(os.path.dirname(lconf2))
            self.recieve_file={"shoretelipbx": lconf1,
                           "bcoConfig":lconf2}
            
            self.logger.debug("copying config files to temp dir")
            vtf.Worker.windowsMachine.net_copy_back(self.source_file["shoretelipbx"], self.recieve_file["shoretelipbx"])
            vtf.Worker.windowsMachine.net_copy_back(self.source_file["bcoConfig"],self.recieve_file["bcoConfig"] )
            self.logger.debug("copied config files to temp dir")
            
            self.logger.debug("Converting .dat file as dict")
            self.ipbxDict=self.parse_config_dat(self.recieve_file["shoretelipbx"])
            self.logger.debug(self.ipbxDict)
            self.bcoDict=self.parse_config_dat(self.recieve_file["bcoConfig"])
            self.logger.debug(self.bcoDict)
            self.logger.debug("update the input values into dat file")
            
            configDatList = self.update_values_configDatDict(self.ipbxDict, self.bcoDict)
            self.convert_datDict_to_shotelIPBX(configDatList, self.recieve_file["shoretelipbx"])
            self.convert_datDict_to_bcoConfig(configDatList, self.recieve_file["bcoConfig"])
            self.logger.debug("updated the input values in dat file successfully")
            
            vtf.Worker.windowsMachine.net_copy(r'etc\tmp\\' + vtf.Worker.workerName + '\\shoretelIPBXConfig.dat',os.path.dirname(self.source_file["shoretelipbx"]))
            vtf.Worker.windowsMachine.net_copy(r'etc\tmp\\' + vtf.Worker.workerName + '\\BCOConfig.dat',os.path.dirname(self.source_file["bcoConfig"]))
            self.logger.debug("update_dat_files successful")
   
    def parse_config_dat(self,conFile):
        '''will parse the given config.dat file into dict
        ex: it parses shoretelIPBXconfig.dat,vtfconfig.dat and bco.dat to dict
        '''
        datFile=open(conFile,'r')
        configDat=datFile.readlines()
        datDict={}
        for param in configDat:
            if param.find('#')==-1:
                if param !=" ":
                    data=re.sub('\s+',' ',param)
                    #data = param.strip()
                    #print(data)
                    paramList=data.split()
                    #paramList=re.split(r'\t+',param)
                    #paramList=re.split(r'\s+',' ',param)
                    if paramList !=[]:
                        if len(paramList)==1:
                        #if paramList[1]=="":
                            datDict.__setitem__(paramList[0].lower(),"none")
                        else:
                            #datDict.__setitem__((paramList[0].lower()).strip(),paramList[1].rstrip("\n"))
                            datDict.__setitem__(paramList[0].lower()," ".join(paramList[1:]))
                            #print(paramList[0].lower()," ".join(paramList[1:]))
        #print(datDict)
        return datDict
    
    def update_values_configDatDict(self,ipbxConfig,bcoConfig):
        '''
        Author : Jahnavi
        update_values_configDatDict: will update the system.cfg values to respective keys in .dat dicts
        '''
        paramDict=self.create_param_dict()
        # configDatList={}
        for (param, configDict) in paramDict.items():
           # print(self.input)
           # print(dir(self.input))
            if param in self.input['testbed'].keys():
                if "ipbxConfig" in configDict.keys():
                    if configDict["ipbxConfig"] in ipbxConfig.keys():
                        ipbxConfig[configDict["ipbxConfig"]]=self.input['testbed'][param]
                if "bcoConfig" in configDict.keys():
                    if configDict["bcoConfig"] in bcoConfig.keys():
                        bcoConfig[configDict["bcoConfig"]]=self.input['testbed'][param]
        configDatList={"ipbx":ipbxConfig,"bco":bcoConfig}
        return configDatList
        # return ipbxConfig, bcoConfig
    
    def convert_datDict_to_shotelIPBX(self,configDatList,ipbxFile):
       '''
       Author : Jahnavi
       convert_datDict_to_shotelIPBX -will write Ipbx dict to shoretelIPBX.dat file. 
       '''
       # configDatList=self.update_values_configDatDict(ipbxConfig,bcoConfig)
       paramList=[]
       #print(configDatList["ipbx"])
       for key , value in configDatList["ipbx"].items():
           #print(key,value)
           paramList.append(key.upper()+"\t\t\t"+value+" \n")
       #print("##########paramslist",paramList)
       with open(ipbxFile, 'w') as f:
           f.writelines(paramList)
    
    def convert_datDict_to_bcoConfig(self,configDatList,bcoCfg):
        '''
        Author:  Jahnavi
        convert_datDict_to_bcoConfig () - will write bcoConfig dict to Bcoconfig.dat file
        '''
        # configDatList=self.update_values_configDatDict(ipbxConfig,bcoConfig)
        paramList=[]
       # print(configDatList["bco"])
        for key , value in configDatList["bco"].items():
           #print(key,value)
           paramList.append(key.upper()+"\t\t\t"+value+" \n")
        #print("##########paramslist",paramList)
        with open(bcoCfg, 'w') as f:
           f.writelines(paramList)
    


    def create_param_dict(self):
        paramDict={'hq_ip':{"ipbxConfig":"site1_server_addr","bcoConfig":"bco_pphone_site1_server_addr","vtfConfig":"setup1_site1_server_addr"},
                   'ldvs_ip':{"bcoConfig":"bco_linuxdvs_server_ip"},
                   'ldvs_mac':{"bcoConfig":"bco_linuxdvs_server_mac"},
                   'ldvs_user_ip':{"bcoConfig":"bco_linuxdvs_user_ip"},
                   'vphone_ip':{"bcoConfig":"bco_vswitch_phone_ip"},
                   'vphone_mac':{"bcoConfig":"bco_vswitch_phone_mac"},
                   'vtrunk_ip':{"bcoConfig":"bco_vswitch_trunk_ip"},
                   'vtrunk_mac':{"bcoConfig":"bco_vswitch_trunk_mac"},
                   'vucb_ip':{"bcoConfig":"bco_vswitch_ucb_ip"},
                   'vucb_mac':{"bcoConfig":"bco_vswitch_ucb_mac"},
                   'vucb_conf_ext':{"bcoConfig":"BCO_UCB_CONF_EXT"},
                   'hq_user_ip':{"bcoConfig":"bco_vswitch_user_ip"},
                   "dvs_ip":{"ipbxConfig":"site2_server_addr"}
                   }
        #print(paramList.values())
        return paramDict