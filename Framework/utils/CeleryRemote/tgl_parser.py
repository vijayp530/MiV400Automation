__author__ = 'mkr'

from class_xml import xmlClass
import re
import os
import sys
from collections import defaultdict


class TGLParser:
    def __init__(self, tgl_file=None):
        if tgl_file:
            self.xmlObj = xmlClass(tgl_file)

    def get_group_count(self):
        return self.xmlObj.GetTagCount('group')

    def get_test_count(self):
        return self.xmlObj.GetTagCount('test')

    def get_all_groups(self):
        ret = []
        for group in self.xmlObj._xmlRoot.iter('group'):
            ret.append(group.find('name').text)
        return ret

    def get_all_tests(self):
        ret = []
        for test in self.xmlObj._xmlRoot.iter('test'):
            ret.append(test.find('name').text)
        return ret

    def get_all_groups_tests(self):
        ret = {}
        for group in self.xmlObj._xmlRoot.iter('group'):
            tests = []
            for test in group.iter('test'):
                tests.append(test.find('name').text)
            ret[group.find('name').text] = tests
        return ret

    def get_package_name(self):
        return self.xmlObj.GetNodeTextByName('name')
    
    def create_tgl(self, pkgName, groupName, testName, tglTemplate, tglFile):
        '''
        Author : Vinay
        tgl_parser(): create tgl file for each test case
        parameters: None        
        '''
        with open(tglTemplate,'r') as content_file:
            content = content_file.read()
        #substituting package, Group & test script name  
        testcaseTgl = re.sub("\$testScript", testName, re.sub("\$groupName", groupName,re.sub("\$pkgName", pkgName, content)))
        with open(tglFile, 'w') as script_file:
            script_file.write(testcaseTgl)

    def parse_failed_tc_file(self,tcFile):
        f=open(tcFile,'r')
        lines = f.readlines()
        lines[:] = [line.rstrip('\n') for line in lines]
        lines = filter(None, lines)
        print(lines)
        #sys.exit()
        lines.sort()
        f.close()
        #f = open(tcFile, 'w')
        #f.writelines(lines)
        #f.close()
        return lines

    def create_failed_tgl(self,tcFile,tglPath,tglTemplate,tcTemplate):
        '''author : UBS'''
        lines=self.parse_failed_tc_file(tcFile)
        print("lines are ",lines)
        (pkg,grp,TC_Name,tc_id)=('','','','')
        self.remove_tgl_files(tglPath)
        for line in lines:
            #line.strip()
            print(lines)
            tcInfo = line.split(',')
            #print(tcInfo)
            (curr_pkg,curr_grp)=(pkg,grp)
            (pkg,grp,tcName,tc_id)=tcInfo
            self.TGL_Content=''
            if curr_pkg != pkg:
                 #newTGL_content=New_TGL(pkg,grp,TC_Name)
                 tglFile=pkg+'_'+grp+'.tgl'
                 print"1", tglFile
                 tglFile=os.path.join(tglPath,tglFile)
                 self.create_tgl(pkg,grp,tcName,tglTemplate,tglFile)
            elif curr_grp != grp:
                #newTGL_content=New_TGL(pkg,grp,TC_Name)
                tglFile=pkg+'_'+grp+'.tgl'
                tglFile=os.path.join(tglPath,tglFile)
                self.create_tgl(pkg,grp,tcName,tglTemplate,tglFile)
            else:
                tglFile=pkg+'_'+grp+'.tgl'
                tglFile=os.path.join(tglPath,tglFile)
                if tcName != None or tcName != '':
                    self.append_TC(tcName,tcTemplate,tglFile)

                #TGL_Content=''

    def remove_tgl_files(self,tglPath):
        ''' will remove the already existing failed test case tgl files from directory'''
        fileList=os.listdir(tglPath)
        for file in fileList:
            os.remove(tglPath+"\\"+file)


    def append_TC(self, TC_Name, TCTemplate, tglFile):
        '''author : UBS'''
    #Appending Test case template for main TGL file
    #Final_TGL_Path=os.path.join(TGL_Path,TGLFile_name)
        with open(tglFile,'r') as f:
            self.TGL_Content = f.read()
        with open(TCTemplate,'r') as append_file:
            self.append_content = append_file.read()
            #self.new_content=re.sub(r'<test>(.*)</test>',self.append_content,self.TGL_Content)
            self.new_content = re.sub(r'(.*)</group>',self.append_content,self.TGL_Content)
        self.final_data = re.sub("\$testScript", TC_Name, self.new_content)
        with open(tglFile,'w') as Final_TGL:
            Final_TGL.write(self.final_data)

    # def get_failed_testcase_list(self,tcFile):
    #     '''
    #     author : jahnavi
    #     :return: this will return list of test cases with group name
    #     '''
    #     pkgDict=defaultdict(list)
    #     failedDict=defaultdict(list)
    #     with open(tcFile) as ftcFile:
    #         tcInfo=ftcFile.readlines()
    #     for tc in tcInfo:
    #         tc=tc.strip()
    #         tcdata=tc.split(",")
    #         tcdata=[c for c in tcdata if c != '']
    #         pkgName=tcdata[0]
    #         grpName=tcdata[1]
    #         tcName=tcdata[2]
    #         failedDict[grpName].append(tcName)
    #         pkgDict[pkgName].append(grpName)
    #     failedDict=dict(failedDict)
    #     pkgDict=dict(pkgDict)
    #     return pkgDict ,failedDict
    #
    # def create_failed_tgl(self,tcFile,tglTemplate):
    #     '''
    #     will create the tgl file with failed test cases
    #     '''
    #
    #     pkgDict=(self.get_failed_testcase_list(tcFile))[0]
    #     tcDict=(self.get_failed_testcase_list(tcFile))[1]
    #    # print(pkgDict)
    #     for pkg in pkgDict.keys():
    #         print(pkg)
    #         for grp in set(pkgDict[pkg]):
    #             if grp in tcDict.keys():
    #                 print(grp)
    #                 with open(tglTemplate,'r') as content_file:
    #                     content = content_file.read()
    #                     #substituting package, Group & test script name
    #                 testcaseTgl = re.sub("\$pkgName", pkg, content)
    #                 with open(os.path.join(r'C:\NextGenArc\etc\tmp\Failed_TGL',grp+"_failed"+pkg+".tgl"),'w') as Final_TGL1:
    #                     Final_TGL1.write(testcaseTgl)
    #





        

#tgp = TGLParser(r'C:\NextGenArc\etc\tmp\Highball_bco.tgl')
#tgp.remove_tgl_files(r'C:\NextGenArc\etc\tmp\Failed_TGL')
#tgp.create_failed_tgl(r'C:\NextGenArc\etc\tmp\Failed_TC\150805032510064000Failed_TC.txt',r'C:\NextGenArc\etc\tmp\Failed_TGL',r'C:\NextGenArc\etc\templates\template.tgl',r'C:\NextGenArc\etc\templates\Test_Case_Append_Template.tgl')
#print((tgp.get_failed_testcase_list(r'C:\NextGenArc\etc\tmp\Failed_TC\150731034309188000Failed_TC.txt'))[1])
#tgp.create_failed_tgl(r'C:\NextGenArc\etc\tmp\Failed_TC\150731034309188000Failed_TC.txt',r'C:\NextGenArc\etc\templates\template.tgl')
# print(tgp.get_group_count())
# print(tgp.get_test_count())
# print(tgp.get_all_tests())
# print(tgp.get_all_groups_tests())
