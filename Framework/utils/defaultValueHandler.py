###############################################################################
## Module: confMgr
## File name: confMgr.py
## Description: configuration manager to associate stream & Rotating file handlers
##
##
##  -----------------------------------------------------------------------
##  Modification log:
##
##  Date        Engineer    Description
##  ---------   ---------   ---------     
##  14-AUG-14    VHA        Module Created
###############################################################################

# Constants for the framework begin ----
#CONFIG_FILE_NAME = '../config/STAF.conf'

#-------------
#import sys

#sys.path.append('../Defaultvalue')
from config_parser import ConfigParser
class defaultValueHandler:
    def __init__(self, FILE_NAME):
        self.feature_obj = ConfigParser(FILE_NAME)

    def getConfigKeyList(self):
        return self.feature_obj.config_key_list

    def getConfigMap(self):        
        return self.feature_obj.config_map

    def setConfigMap(self, new_dict):
        self.feature_obj.update_dictionary(new_dict)

'''        
if __name__ == "__main__":
    filepath = "..//Defaulvalue"+param+".txt"
    Handler = defaultValueHandler("..\\Defaultvalue\\tenants_general.txt")
    
    print((Handler.getConfigMap()))
    #print((confMgr.getConfigMap()["FILE_LOG_LEVEL"]))
'''

