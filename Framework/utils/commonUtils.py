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

class CommonUtils:
    """ CommonUtils class is used to do some common functions """
    def replace_delimiter(self, params, delimiter):
        '''takes params as dict and one delimiter,replaces delimeter with space
	    and return the dict'''
        for key, value in params.items():
            if "#" in  params[key]:
                params[key]=params[key].replace(delimiter, " ")
        return params
    def get_value_if_present_in_dict(self, params, key):
        '''searches key in dict if present return the values else None as string'''
        if key in params:
            return params[key]
        else:
            return "None"
#######################

 