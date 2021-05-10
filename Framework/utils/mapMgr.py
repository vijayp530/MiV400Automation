"""
Map files manager class
"""
__author__ = "Vinay HA"

import os
from map_parser import mapParser


class mapMgr:
    '''
        mapMgr parsers all the map file inside map directory and converts them into dictionary
    '''
    objRepository = {}
    objRepoList = []
    @staticmethod
    def create_maplist(component = "ManhattanComponent"):
        try:
            # Listing all the file in the map directory
            # creating the map directory path
            mapdirectory = None
            filelist = []
            base_path = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
            if "Manhattan".lower() in component.lower():
                mapdirectory = os.path.join(base_path,"automation-manhattan","ManhattanLibrary","map",component)
            elif "BOSS".lower() in component.lower():
                mapdirectory = os.path.join(base_path,"automation-boss","map",component)
            elif "PBX".lower() in component.lower():
                mapdirectory = os.path.join(base_path, "automation-pbx", "map", component)
            elif "Teamwork".lower() in component.lower() and "android" not in component.lower() and "ios" not in component.lower():
                mapdirectory = os.path.join(base_path,"automation-tww","map",component)
            elif "MnM".lower() in component.lower():
                mapdirectory = os.path.join(base_path,"automation-mnm","map",component)
            elif "gsuite" in component.lower():
                mapdirectory = os.path.join(os.path.dirname(os.getcwd()),'map',component)  
            elif "AndroidTeamworkComponent".lower() in component.lower():
                mapdirectory = os.path.join(base_path, "android teamwork automation", "map", component)
            else:
                raise Exception("Component %s is not supported!" % component)
                
            if isinstance(component, str):
                if os.path.isdir(mapdirectory):
                    print("Map directory for <%s> is <%s>"%(component, mapdirectory))
                else:
                    raise AssertionError("<%s> Directory not found for <%s>" %(mapdirectory, component))

            for dirname, dirnames, filenames in os.walk(mapdirectory):
                filelist.extend([os.path.join(dirname, filename) for filename in filenames])
                 
            for file in filelist:
                # Parsing all the map file one by one and updating objRepository dictionary
                map_obj = mapParser(file)
                mapMgr.objRepository.update(map_obj.map_dict)
                mapMgr.objRepoList.append(map_obj.map_key_list)
        except:
            return False
        
    # Method to get objList
    @staticmethod
    def getMapKeyList():
        return mapMgr.objRepoList

    # Method to get objDictionary
    @staticmethod
    def getMapDict():        
        return mapMgr.objRepository

    # Method to get element from objRepository
    @staticmethod
    def __getitem__(key):
        if key in list(mapMgr.objRepository.keys()):
            return mapMgr.objRepository[key]
        else:
            return None


if __name__ == "__main__":
    mapMgr.create_maplist()
    print((mapMgr.__getitem__('Login_Password')))
    print((mapMgr.getMapDict()['Login1_Password']))
