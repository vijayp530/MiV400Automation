import sys
import os

configDict={}
class ShoretelIPBX_parser():
    def __init__(self):
        pass
    def parse_shoretelIPBX(self):

        #This will open the shoretelIPBX config file and read the contenent in dict format.
        datalist=open(r'C:\\HCLT\\vtftestpkg\\vtf\\TAF\\conf\\VTFSystem.cfg').readlines()
        #datalist.remove('\n')
        for data in datalist:
            if data.startswith("#") or data=="\n":
                continue
            data=data.split()
            if len(data)==1:
                configDict[data[0].lower()]="None"
            else:
                configDict[data[0].lower()]=data[1]
        return configDict




if __name__ == "__main__":
    obj=ShoretelIPBX_parser()
    obj.parse_shoretelIPBX()
