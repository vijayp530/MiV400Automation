import xml.etree.ElementTree as ET

#from class_utility import defaultLogFunction

def defaultLogFunction(fileName, className, strToLog):
    print(str(fileName) + "->("+ str(className) + ") :" + strToLog)
    #print(strToLog)

# ------------------------------------------#
# Class         : xmlClass                  #
# Description   : Wrapper class for Etree   #
# ------------------------------------------#
#@exception_handler
class xmlClass:
    """Wrapper class for XML"""
    def __init__(self, xmlFileName, logFunction=defaultLogFunction):
        self._xmlRoot = self._ParseXml(xmlFileName)
        self.dicChildren = dict()

    # -------------------------------------------#
    # Function      : ParseXml                   #
    # Description   : Parse the xml file using   #
    #                 ElementTree and returns    #
    #                 tree object                #
    # -------------------------------------------#
    def _ParseXml(self, xmlFileName):
        self.tree = ET.parse(xmlFileName)
        root = self.tree.getroot()
        return root

    # -------------------------------------------#
    # Function      : GetAllAttrib               #
    # Description   : Get all attrib of a node   #
    #                 and return as dictionary   #
    # -------------------------------------------#
    def GetAllAttrib(self, node, dicAttributes):
        for attrName, attrValue in node.attrib.items():
            dicAttributes[attrName] = attrValue
        return None

    # -------------------------------------------#
    # Function      : GetAllChildren             #
    # Description   : Get all children to dict   #
    #                 used for arguments         #
    # -------------------------------------------#
    def GetAllChildren(self, node, dicChildren):
        for child in node.getchildren():
            dicChildren[child.tag] = child.text
        return None
    
    # -------------------------------------------#
    # Function      : GetAllChildrenAnyDepth     #
    # Description   : Get all children till any  #
    #                 depth, to a global dict    #
    # Change List   : Modified (21-DEC-2015) to  #
    #                 to get all children        #
    # -------------------------------------------#
    def GetAllChildrenAnyDepth(self, node):
        for child in node.getchildren():
            if len(child) != 0:
                self.GetAllChildrenAnyDepth(child)
            else:
                self.dicChildren[child.tag] = child.text
        return self.dicChildren

    # -------------------------------------------#
    # Function      : FindNode                   #
    # Description   : Find the node using name   #
    # -------------------------------------------#
    def FindNode(self, Name):
        return self._xmlRoot.find(Name)

    # -------------------------------------------#
    # Function      : GetTag                     #
    # Description   : Get the node tag           #
    # -------------------------------------------#
    def GetTag(self, Node):
        return Node.tag

    # -------------------------------------------#
    # Function      : GetText                    #
    # Description   : Get the node tag           #
    # -------------------------------------------#
    def GetText(self, Node):
        return Node.text


    # -------------------------------------------#
    # Function      : GetNodeTextByName          #
    # Description   : Find the node by name and  #
    #                 Get the text of that node  #
    # -------------------------------------------#
    def GetNodeTextByName(self, Name):
        node = self.FindNode(Name)
        Text = None
        if node != None:
            Text = self.GetText(node)
        #else:
        #    Text = Name
        return Text

    def IsItNode(self, Name):
        RetFlag = True
        node = self.FindNode(Name)
        if ((Node != None) and (len(node) > 0)):
            RetFlag = False
        return RetFlag

    # -------------------------------------------#
    # Function      : TraverseChildren           #
    # Description   : Traverse the children of   #
    #                 node and execute callback  #
    # -------------------------------------------#
    def TraverseChildren(self, Node, cbFunction):
        Ret  = False
        Stop = False

        for child in Node.getchildren():
            #print("--------------- Traverse Children child ------------")
            Ret = True
            Stop = cbFunction(self, child)
            if (Stop == True):
                break
            #print("Completed execution of children")
        return Ret

    # -------------------------------------------#
    # Function      : TraverseChildrenWithName   #
    # Description   : Traverse the children of   #
    #                 node with name and execute #
    #                 the callback               #
    # -------------------------------------------#
    def TraverseChildrenWithName(self, Obj, Name, cbFunction):
        Node = Obj.FindNode(Name)
        return self.TraverseChildren(Node, cbFunction)

    def GetTagCount(self,tagName):
        return len(list(self._xmlRoot.iter(tagName)))

#scriptConfigFileName = "script_config.xml"
#if __name__ == "__main__":
#    xmlConfig = xmlClass(scriptConfigFileName)
#    print(xmlConfig)