###############################################################################
## Module: config_parser
## File name: config_parser.py
## Description: configuration class to parse config file and store values in form of Dictionary
##
##
##  -----------------------------------------------------------------------
##  Modification log:
##
##  Date        Engineer    Description
##  ---------   ---------   ---------     
##  14-AUG-14    VHA        Module Created
###############################################################################
import re
import os

class ConfigParser:
    """ ConfigParser class is used to read configuration files. """

    def __init__(self, filename=None, rtool=None):
        
        """ 1 map and 1 list is used to maintain an ordered map"""
        self.config_map={}
        self.config_key_list=[]
        self.rtool = rtool
        if filename != None:
            try:		
                fileobj = open(filename, "r")
                other_value_line_count=0
                for line in fileobj:
                    if '=' in line: 
                        list = line.split('=')
                        if len(list) >= 2:
                            # Remove \n and leading and trailing spaces from value and then save
                            value = list[1].split('\n')[0].strip()
                            list[0] = list[0].strip()

                            self.config_map[str(list[0]).strip()] = value
                            self.config_key_list.append(list[0])
                    else:
                        key = 'other_value_line_count_' + str(other_value_line_count)
                        other_value_line_count = other_value_line_count + 1
                        self.config_map[key] = line
                        self.config_key_list.append(key)
                fileobj.close()	
                                
            except IOError:
                msg = "ConfigManager: Unable to open file: " + filename
                print(msg) 
                raise Exception
                        
    def __str__(self):
        	
        ret_str = ""
        for key in self.config_key_list:
                value = self.config_map[key]
    #		print(" * * * * kay=", key, " value =",  value)
                if re.search("other_value_line_count", key):
                        ret_str = ret_str + str(value)
                else:
                        ret_str = ret_str + str(key) + '=' + str(value) + '\n'
        #print(ret_str)
        return ret_str

    def __getitem__(self,key):
        if key in list(self.config_map.keys()):
                return self.config_map[key]
        else:
                return None

    def __setitem__(self, key, value):
        self.config_map[key] = str(value).strip()
        if not key in self.config_key_list: self.config_key_list.append(key)

    def remove(self, key):
        value = None
        if key in self.config.key_list:
                value = self.config_map[key]
                self.config_key_list.remove(key)
                del self.config_map[key]

    def update_dictionary(self, param_dict):
        for key in param_dict.keys():
            self.config_map[key]=param_dict[key]
        #print(self.config_map['$mdn_post'],param_dict['$mdn_post'])
        
    def write(self, fileobj):
        fileobj.write(str(self))
	
if __name__ == "__main__":
    confManager = ConfigManager("../config/STAF.conf")
    print((confManager.config_map))
    


