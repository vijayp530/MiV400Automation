# -*- coding: utf-8 -*-
__author__ = 'Sandeep Koluguri'

import requests
import re
import xml.etree.ElementTree as ET
from xml.etree.ElementTree import XML, fromstring, tostring
    
class ALMSession:
    def __init__(self,user,password,url,auth,logger):
        try:
            self.logger = logger
            self.logger.debug("BEGIN")
            self.__headers = {"Accept":"application/xml",
                              "Content-Type":"application/xml",
                              "KeepAlive":"true",
                              "Cookie": None}
            self.__user_pass = (user,password)
            self.Open(url,auth)
            self.logger.debug("END")
        except:
            self.logger.error(u"Exception while creating ALMSession "+self.__headers+self.__h)
            
    def Open(self,url,auth):
        '''
            will open the QC with auth user name and password
        '''
        self.logger.debug("BEGIN")
        self.__auth = url+auth
        req = requests.get(self.__auth, auth=self.__user_pass)
        if req.status_code is 200:
            self.__headers["Cookie"] = req.headers['set-cookie']
            self.logger.info(self.__headers["Cookie"])
            return 0
        else:
            self.logger.error(u"Open ALM session"+req.status_code+req.reason+u'AUTH URL:'+self.__auth+u'HEADERS:'+self.__headers)
            return int(req.status_code)

    def __queryFeatureAttr__(self, baseUrl, baseProject, keyword_list, project_type):
        '''
            will execute query for user given features to get tc
        '''
        self.logger.debug("BEGIN")
        if baseProject=="Highball":
            self.__query = baseUrl + "ContactCenter/tests?query={user-06[" + baseProject +"];user-03[\'"
	elif baseProject=="Cosmo-PBX":
	    self.__query = baseUrl + "ShoreTel/tests?query={user-05[PBX];user-06[\'"
        else:
            self.__query = baseUrl + "ShoreTel/tests?query={user-05[" + baseProject +"];user-06[\'"
        result = self.__query
        for arg in keyword_list:
                result += arg + "\' OR \'"
        result = re.match(r'(.*) OR \'$', result, re.M|re.I)
        result = result.group(1)
        result += ']}&page-size=2000'
        self.logger.info("Debug Sandeep:"+result)
        self.logger.debug("END")
        return result

    def __queryPriorityAttr__(self,baseUrl, baseProject, keyword_list, project_type):
        '''
            will execute query for user given priority to get tc
        '''
        self.logger.debug("BEGIN")
        keyword_dict = {'P1': '1 - High', 'P2': '2 - Med', 'P3': '3 - Low', 'P4' : '4 - Obsolete in Cosmo'};
        result = self.get_query_url(baseUrl,baseProject, project_type)
        for arg in keyword_list:
                result += keyword_dict[arg.upper()] + "\') OR (\'"
        result = re.match(r'^(.*) OR \(\'$', result, re.M|re.I)
        result = result.group(1)
        result += ']}&page-size=2000'
        self.logger.debug("END")
        return result

    def get_query_url(self,baseUrl,baseProject, project_type):
        '''
            will return the query url based on given project
        '''
        self.logger.debug("BEGIN")
        if baseProject=="Highball":
            if (project_type == 'MT'):
                self.__query = baseUrl +"ContactCenter/tests?query={user-06["+ baseProject +"];user-12['Scripted'];user-04[(\'"
            else:
                self.__query = baseUrl +"ContactCenter/tests?query={user-06["+ baseProject +"];user-11['Scripted'];user-04[(\'"
        elif baseProject=="Cosmo-PBX":
            if (project_type == 'MT'):
                self.__query = baseUrl +"ShoreTel/tests?query={user-05[PBX];user-18['Scripted'];user-01[(\'"
            else:
                self.__query = baseUrl +"ShoreTel/tests?query={user-05[PBX];user-02['Scripted'];user-01[(\'"
        elif baseProject=="Manhattan":
            if (project_type == 'MT'):
                self.__query = baseUrl +"ShoreTel/tests?query={user-05["+ baseProject +"];user-18['Done'];user-01[(\'"
            else:
                self.__query = baseUrl +"ShoreTel/tests?query={user-05["+ baseProject +"];user-02['Done'];user-01[(\'"
        else:
            if (project_type == 'MT'):
                self.__query = baseUrl +"ShoreTel/tests?query={user-05["+ baseProject +"];user-18['Scripted'];user-01[(\'"
            else:
                self.__query = baseUrl +"ShoreTel/tests?query={user-05["+ baseProject +"];user-02['Scripted'];user-01[(\'"
        self.logger.debug("END")
        return self.__query
    

    def Query(self, object, baseUrl, baseProject, execution_suite, keyword_list, project_type):
        '''
            will excute query on QC for given keywords
        '''
        if self.__headers["Cookie"] is not None:
            if execution_suite == 'FEATURE':
                req = requests.get(object.__queryFeatureAttr__(baseUrl, baseProject, keyword_list, project_type), headers=self.__headers, auth=self.__user_pass)
            elif execution_suite == 'PRIORITY':
                req = requests.get(object.__queryPriorityAttr__(baseUrl, baseProject, keyword_list, project_type), headers=self.__headers, auth=self.__user_pass)
            if req.status_code == 200:
                return self.successQuery(req,baseProject,object)
            elif req.status_code == 500:
                return self.ErrorQuery(req,baseProject,object)
            else:
                return int(req.status_code), None
        else:
            return 1, None

    def successQuery(self,req,baseProject,object):
        '''
            will return xml based on query result
        '''
        self.logger.debug("BEGIN")
        res = []
        result = req.content
        res=object.getXML(baseProject,result)
        self.logger.debug("END")
        return res
        
    def ErrorQuery(self,req,baseProject,object):
        '''
            will return exception xml 
        '''
        try:
            self.logger.debug("BEGIN")
            if isinstance(req.text, unicode):
                exceptionxml = ET.fromstring(req.text.encode('utf8','ignore'))
            else:
                exceptionxml = ET.fromstring(req.text)
            return exceptionxml
        except ET.ParseError:
            return int(req.status_code), None

    def parse_xml(self, obj, dict):
        almxml = ET.fromstring(obj)
        if almxml.__dict__.has_key("TotalResults") and almxml.attrib["TotalResults"] == 0:
            return
        
    def getXML(self,baseProject,result):
        '''
            will return the xml with tc cases
        '''
        try:
            root = ET.fromstring(result)
            if baseProject == "Highball":
                xmlstring=self.create_tc_xml(result, root, 30, 38, 19, 18)
            else:
                xmlstring=self.create_tc_xml(result, root, 29, 41, 28, 21)
            xmlstring = xmlstring.replace('1 - High','P1').replace('2 - Med','P2').replace('3 - Low','P3').replace('4 - Obsolete in Cosmo','P4')
            myxml = fromstring(xmlstring)
            self.logger.info("+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++\n"+xmlstring)
            return  myxml
        except:
            self.logger.error('Something went wrong! Can\'t tell what?')
            return 1, None# quit Python

    def create_tc_xml(self, result, root, id_no, path_no, keyword_no, priority_no):
        '''
            will create an XML with the resultnat test cases
        '''
        xmlstring = '<xml>'
        count = 0
        for child in root:
            id = root [count][0][id_no][0].text
            path = root[count][0][path_no][0].text
            keywordSpecific = root[count][0][keyword_no][0].text
            priority = root[count][0][priority_no][0].text
            if path is not None:
                xmlstring=self.add_tc_xml(result, count, xmlstring,path,keywordSpecific,priority)
            else:
                print("count : ",count,"\tid : ", id, "\tpath : ", path, "== no path ==")
            count = count + 1
        xmlstring += '</xml>'
        return xmlstring

    def add_tc_xml(self, result, count, xmlstring, path, keywordSpecific, priority):
        ''' will add test cases to xml'''
        if result is not None:
            res = re.match(r'^.*test\\\\(.*)$', path, re.M|re.I)
            if res is not None:
                mypath = res.group(1)
                mypathArr =  mypath.split('\\\\')
                if len(mypathArr) == 3:
                    xmlstring += '<test name="'+ mypathArr[-1] + '"><suite>' + mypathArr[-3] + '</suite><group>'+ mypathArr[-2] +'</group><feature>' + keywordSpecific + '</feature><priority>' + priority + '</priority></test>'
                elif len(mypathArr) == 4:
                    underscore = '_'
                    conc = mypathArr[-4] + underscore + mypathArr[-3]
                    xmlstring += '<test name="'+ mypathArr[-1] + '"><suite>' + conc + '</suite><group>'+ mypathArr[-2] +\
                         '</group><feature>' + keywordSpecific + '</feature><priority>' + \
                         priority + '</priority></test>'
                else:
                    print("count : ",count,"\tid : ", id, "\tpath : ", path, "== not including. wrong path ==")
        return xmlstring


