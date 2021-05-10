'''
Created on Nov 30, 2015

@author: UKumar
'''
import sys


class ShoretelIPBXUpdater:
    """
    classdocs
    """

    def __init__(self, ipbxFilePath, logger):
        """
        Constructor
        """
        self.ipbxFilePath = ipbxFilePath
        self.logger = logger
        
    def create_ipbx_dict(self):
        """creates a dictionary of parameters of shoretelIPBX file
        """
        try:
            self.logger.debug('Begin')
            ipbxdict = {}
            fObj = open(self.ipbxFilePath, 'r')
            paramsList = fObj.readlines()
            fObj.close()
            for line in paramsList:
                if line.startswith("#") or "\n" == line:
                    continue
                param = line.split()
                if len(param) == 2:
                    ipbxdict[param[0]] = param[1]
                else:
                    ipbxdict[param[0]] = ""
            self.logger.debug(ipbxdict)
            self.logger.debug('End')
            return ipbxdict
        except Exception as e:
            raise e

    def update_ipbx_file(self, ipbxDict, updatedDict):
        """ Updates shoretelIPBX file with new values
        """
        try:
            self.logger.debug('Begin')
            self.logger.info("Updating shoretelIPBXConfig.dat file.")
            fObj = open(self.ipbxFilePath, 'w')
            for key in updatedDict.keys():
                if key in ipbxDict.keys():
                    del ipbxDict[key]
                line = key+"\t\t\t"+updatedDict[key]+"\n"
                fObj.write(line)

            for key in ipbxDict.keys():
                line = key+"\t\t\t"+ipbxDict[key]+"\n"
                fObj.write(line)
            fObj.close()
            self.logger.info("Updating Done.")
        except Exception as e:
            raise e

    def update_bco_cgf(self, bcoConfigPath, testbedInfoDict):
        """creates a dictionary of parameters of BCConfig.dat file
        """
        try:
            self.logger.debug('Begin')
            #testbedInfoDict = xmlObj.GetAllChildrenAnyDepth(xmlObj.FindNode("./BCO"))
            bcocfgDict = {}
            fObj = open(bcoConfigPath, 'r')
            paramsList = fObj.readlines()
            fObj.close()
            for line in paramsList:
                if line.startswith("#") or "\n" == line:
                    continue
                param = line.split()
                if len(param) == 2:
                    bcocfgDict[param[0]] = param[1]
                else:
                    bcocfgDict[param[0]] = ""
            fObj = open(bcoConfigPath, 'w')
            for key in testbedInfoDict.keys():
                if key in bcocfgDict.keys():
                    del bcocfgDict[key]
                line = key+"\t\t\t\t"+testbedInfoDict[key]+"\n"
                fObj.write(line)

            for key in bcocfgDict.keys():
                line = key+"\t\t\t\t"+bcocfgDict[key]+"\n"
                fObj.write(line)
            fObj.close()
            self.logger.debug(bcocfgDict)
            self.logger.debug('End')
        except Exception as e:
            raise e



if __name__ == "__main__":
    print("hello")
    ss = ShoretelIPBXUpdater()
    d = ss.create_ipbx_dict()
    #d = ss.update_ipbx_file()
    for key, values in d.items():
        print(key, values)
    #print(d["OB_TYPE"]i)
