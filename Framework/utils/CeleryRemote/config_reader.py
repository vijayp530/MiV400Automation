__author__ = 'mkr'

import os
import socket
from xml.etree.ElementTree import Element

class ConfigReader:
    def __init__(self, logger):
        self.logger = logger
        self.logger.debug("Begin")
        # nothing to do here
        self.logger.debug("End")
        
    def get_qc_info(self, conf):
        self.logger.debug("Begin")
        info = dict()
        qc=conf.FindNode("QC")
        if qc is None:
            self.logger.error("QC info not found in config")
        else:
            info={
                "USER":qc.find('USER').text,
                "PASSWORD":qc.find('PASSWORD').text,
                "URL":qc.find('URL').text,
                "AUTH":qc.find('AUTH').text,
                "BASE_URL":qc.find('BASE_URL').text
            }
        self.logger.info("QC info is "+str(info))
        self.logger.debug("End")
        return info

    def get_action_module(self, conf, action):
        self.logger.debug("Begin")
        self.logger.info("Get module for action "+action.upper())
        module_ = None
        for item in conf._xmlRoot.findall("ACTION"):
            self.logger.debug("ITEM: "+item.attrib['name'])
            if item.attrib['name'] == action.upper():
                module_ = item.find('MODULE').text
                self.logger.debug("Action Module is :"+ module_)
        self.logger.debug("End")
        return module_

    def get_action_class(self, conf, action):
        self.logger.debug("Begin")
        class_ = None
        for item in conf._xmlRoot.findall("ACTION"):
            if item.attrib['name'] == action.upper():
                class_ = item.find('CLASS').text
                self.logger.debug("Action Class is :"+ class_)
        self.logger.debug("End")
        return class_

    def get_project_action_module(self, conf, project, action):
        module_ = None
        for item in conf._xmlRoot.findall("PROJECT"):
            if item.attrib['name'].lower() == project.lower():
                try:
                    module_ = item.find('MODULE').find(action.upper()).text
                    self.logger.debug("Action Module is :"+ module_)
                except Exception:
                    self.logger.error("Project Action Module info not found in config.!")
        self.logger.debug("End")
        return module_

    def get_project_action_class(self, conf, project, action):
        self.logger.debug("Begin")
        class_ = None
        for item in conf._xmlRoot.findall("PROJECT"):
            if item.attrib['name'].lower() == project.lower():
                try:
                    class_ = item.find('CLASS').find(action.upper()).text
                    self.logger.debug("Action Class is :"+ class_)
                except Exception:
                    self.logger.error("Project Action Class info not found in config.!")
        self.logger.debug("End")
        return class_

    def get_project_action_config(self, conf, project, action):
        self.logger.debug("Begin")
        config_ = None
        for item in conf._xmlRoot.findall("PROJECT"):
            if item.attrib['name'].lower() == project.lower():
                try:
                    config_ = item.find('CONFIG').find(action.upper()).text
                    self.logger.debug("Action Config is :"+ config_)
                except Exception:
                    self.logger.error("Project Action Config info not found in config.!")
        self.logger.debug("End")
        return config_

    def get_project_client(self,project):
        clientDict={"manhattan":"MHClient Build",
                    "highball":"CCD Build",
                    "cosmo-pseries":"Phone Build",
                    "cosmo-pbx":"Phone Build",
                    "mobility":"SMC Client Build",
                    "m&m": "HQ Build",
                    "wb.2-pbx": "Phone Build"}
        return clientDict[project.lower()]

    def get_client_build_no(self,project,build):
        if project.lower() =="manhattan":
            buildpath=build.split("\\")
            return buildpath[-1]
        return build

    def get_redis_server_info(self,conf):
        self.logger.debug("Begin")
        redis = conf.FindNode('REDIS')
        if redis is None:
            self.logger.error("Redis info not found in config.!")
            return None
        self.logger.debug("End")
        return redis.find('IP').text, redis.find('PORT').text

    def get_reporter_local_dir(self, conf):
        self.logger.debug("Begin")
        reporter = conf.FindNode('REPORTER')
        if reporter is None:
            self.logger.error("Reporter Local Directory info not found in config.!")
            return None
        self.logger.debug("End")
        return reporter.find('LOCALDIR').text

    def get_reporter_info(self, conf):
        self.logger.debug("Begin")
        info = dict()
        reporter = conf.FindNode('REPORTER')
        if reporter is None:
            self.logger.error("Reporter info not found in config.!")
        else:
            info = {
                "LOCALDIR": reporter.find('LOCALDIR').text,
                "REMOTEDIR": reporter.find('REMOTEDIR').text,
                "IP": reporter.find('IP').text,
                "USER": reporter.find('USER').text,
                "PASSWORD": reporter.find('PASSWORD').text,
                "TEMPLATEPATH": reporter.find('TEMPLATE').find('TEMPLATEPATH').text,
                "URL": reporter.find('URL').text
            }
        self.logger.info("Reporter info is "+str(info))
        self.logger.debug("End")
        return info
    
    def get_rod_server_info(self, conf):
        self.logger.debug("Begin")
        info = dict()
        rod_server = conf.FindNode('ROD_SERVER')
        if rod_server is None:
            self.logger.error("RoD Server info not found in config.!")
        else:
            info = {
                "IP": rod_server.find('IP').text,
                "USER": rod_server.find('USER').text,
                "PASSWORD": rod_server.find('PASSWORD').text,
                "XML_FILE_DIR": rod_server.find('XML_FILE_DIR').text
            }
        self.logger.info("RoD Server info is "+str(info))
        self.logger.debug("End")
        return info

    def get_reporter_template(self, conf, action):
        self.logger.debug("Begin")
        template = None
        reporter = conf.FindNode('REPORTER')
        if reporter is None:
            self.logger.error("Reporter info not found in config.!")
        else:
            template = reporter.find('TEMPLATE').find(action.upper()).text
            self.logger.info("Reporter Template is "+template)
        self.logger.debug("End")
        return template

    def get_database_info(self, conf):
        self.logger.debug("Begin")
        info = dict()
        reporter = conf.FindNode('DATABASE')
        if reporter is None:
            self.logger.error("Database info not found in config.!")
        else:
            info = {
                "IP": reporter.find('IP').text,
                "PORT": reporter.find('PORT').text,
                "USER": reporter.find('USER').text,
                "PASSWORD": reporter.find('PASSWORD').text,
                "DBNAME": reporter.find('DBNAME').text,
                "TYPE": reporter.find('TYPE').text
            }
        self.logger.debug("End")
        return info

    # def get_vtf_info_back(self, conf):
    #     self.logger.debug("Begin")
    #     vtf_info = dict()
    #     vtf = conf.FindNode('VTF')
    #     if vtf is None:
    #         self.logger.error("VTF info not found in Config.!")
    #     else:
    #         vtf_info['name'] = vtf.attrib['name']
    #         vtf_info['CONFIG'] = vtf.text
    #         self.logger.debug("End")
    #     return vtf_info

    def get_vtf_info(self, conf):
        self.logger.debug("Begin")
        vtf_info = []
        for vtf in conf._xmlRoot.iter('VTF'):
            vtf_info.append(
                {
                    'NAME': vtf.attrib['name'],
                    'CONFIG': vtf.text
                }
            )
        if vtf_info is None:
            self.logger.error("VTF info not found in Config.!")
        self.logger.debug("End")
        return vtf_info

    def get_root_path(self, conf):
        self.logger.debug("Begin")
        rootpath = conf.FindNode('ROOTPATH')
        if rootpath is None:
            self.logger.error("Rootpath info not found in config.!")
        else:
            rootpath = rootpath.text
            self.logger.debug("Rootpath is "+rootpath)
        self.logger.debug("End")
        return rootpath

    def get_command_file(self, conf, suite):
        self.logger.debug("Begin")
        commands = conf.FindNode('COMMANDS')
        if commands is None:
            self.logger.error("Commands info not found in config.!")
        else:
            commands = commands.find(suite.upper()).text
            self.logger.debug("Commands file for suite="+suite.upper()+" is "+commands)
        self.logger.debug("End")
        return commands

    def get_config_path(self, conf):
        self.logger.debug("Begin")
        confpath = None
        rootpath = self.get_root_path(conf)
        if rootpath is None:
            self.logger.error("Rootpath info not found in config.!")
        else:
            confpath = os.path.join(
                rootpath,
                r'etc\configs'
            )
            self.logger.debug("ConfigPath is "+confpath)
        self.logger.debug("End")
        return confpath

    def get_commands_path(self, conf):
        self.logger.debug("Begin")
        commandpath = None
        rootpath = self.get_root_path(conf)
        if rootpath is None:
            self.logger.error("Rootpath info not found in config.!")
        else:
            commandpath = os.path.join(
                rootpath,
                r'etc\commands'
            )
            self.logger.debug("Commands path is "+commandpath)
        self.logger.debug("End")
        return commandpath

    def get_run_id(self, conf):
        self.logger.debug("Begin")
        run_id = conf.FindNode('RUNID')
        if run_id is None:
            self.logger.error("Run ID info is not present in config.!")
        else:
            run_id = run_id.text
            self.logger.debug("Run ID is: "+run_id)
        self.logger.debug("End")
        return run_id

    def get_run_user(self, conf):
        self.logger.debug("Begin")
        run_user = conf.FindNode('RUNUSER')
        if run_user is None:
            self.logger.error("Run user info is not present in config.!")
        else:
            run_user = run_user.text
            self.logger.debug("Run user is: "+run_user)
        self.logger.debug("End")
        return run_user

    def set_run_id(self, conf, id):
        self.logger.debug("Begin")
        conf._xmlRoot.append(Element("RUNID"))
        conf.FindNode('RUNID').text = id
        self.logger.debug("End")

    def set_run_user(self, conf, user):
        self.logger.debug("Begin")
        conf._xmlRoot.append(Element("RUNUSER"))
        conf.FindNode('RUNUSER').text = user
        self.logger.debug("End")

    def get_emailer_info(self, conf):
        self.logger.debug("Begin")
        info = dict()
        emailer = conf.FindNode('EMAIL')
        if emailer is None:
            self.logger.error("Email info not found in config.!")
        else:
            info = {
                "SERVER": emailer.find('SERVER').text,
                "FROM": emailer.find('FROM').text,
                "PASSWORD":emailer.find('PASSWORD').text,
                "TO": emailer.find('TO').text,
            }
        self.logger.debug("End")
        return info

    def get_temp_path(self, conf):
        self.logger.debug("Begin")
        temppath = conf.FindNode('TEMPPATH')
        if temppath is None:
            self.logger.error("Temp path info is not present in config.!")
        else:
            temppath = temppath.text
            self.logger.debug("Temp path is: "+temppath)
        self.logger.debug("End")
        return temppath

    def get_device(self, conf, type_):
        self.logger.debug("Begin")
        devices = conf._xmlRoot.findall('DEVICE')
        type_devices = []
        if devices is None:
            self.logger.error("No Device info found in the config.!")
        else:
            for device in devices:
                if device.find('TYPE').text == type_:
                    d_dict = {'NAME': device.get('NAME')}
                    d_dict.update({node.tag: node.text for node in device.iter()})
                    type_devices.append(d_dict)
        self.logger.info("Devices of type:" + type_ + str(type_devices))
        self.logger.debug("End")
        return type_devices

    def get_hubnode_ports(self, conf):
        self.logger.debug("Begin")
        ports = conf.FindNode('HUBNODEPORT')
        if ports is None:
            self.logger.error("No hub node port info found in the config.!")
        else:
            ports = [port.text for port in ports.getchildren()]
        self.logger.info("hub node ports:" + str(ports))
        self.logger.debug("End")
        return ports

    def get_setup_name(self):
        """
        This method will return rod setup name st or mt from team city agent
        """
        file=(open(r'C:\BuildAgent\conf\buildAgent.properties')).readlines()
        for line in file:
            if "name=" in line:
                agent=line.split("=")
                agent_name=agent[1].split('_')
                return agent_name[0]

    def get_ipaddress(self):
        '''
        This will return the ip address of current machine
        '''
        return socket.gethostbyname(socket.gethostname())

    def get_failed_flag(self,conf):
        '''
        will return the implicit and explicit failed flag value from project specific executor file
        '''
        dict={}
        imp_flag=conf.FindNode("IMP_FAILED_RUN").text
        exp_flag=conf.FindNode("EXP_FAILED_RUN").text
        dict.__setitem__("IMP_FAILED_RUN",imp_flag)
        dict.__setitem__("EXP_FAILED_RUN",exp_flag)
        return dict

    def get_shorebotdir(self,conf):
        '''
        Author : Jahnavi
        This will return shoreboat dir path
        '''
        shoreboatdir=conf.FindNode("TESTCASE_DIR").text
        return shoreboatdir

    def get_shorebot_log_path(self,conf):
        '''
        Author : Jahnavi
        This will return shoreboat dir path
        '''
        shoreboatdir=conf.FindNode("LOG_PATH").text
        return shoreboatdir

    def get_project_timeout(self,conf):
        '''
        Author : Jahnavi
        This will return project max timeout value for each test case
        '''
        timeout=conf.FindNode("TIMEOUT").text
        return timeout

    def get_tgldir_path(self,conf):
        '''
        Author : Jahnavi
        :return: will return tgl dir path
        '''
        tgldir=conf.FindNode("TGL_DIR").text
        return tgldir

    def get_vtfcli_path(self , conf):
        '''
        Author : Jahnavi
        :return : will return vtf cli path
        '''
        vtf_cli=conf.FindNode("VTF_CLI_PATH").text
        return vtf_cli

    def get_pseries_dir(self,conf):
        '''
        :return: will return pseries dir location
        '''
        pseries_dir=conf.FindNode("PSERIES_DIR").text
        return pseries_dir

    def get_qdrive_testsuite_path(self,conf):
        '''
        :return: will return the Q-DRIVE testsuite path
        '''

        q_testsuite=conf.FindNode("Q_TESTSUITE_DIR").text
        return q_testsuite

    def get_systemdb_path(self,conf):
        '''
        :return: will return path of system.db
        '''
        self.logger.debug("Begin")
        systemdbPath = conf.FindNode("SYSTEMDB_DIR").text
        self.logger.debug("End")
        return systemdbPath
    
    def get_local_xml_path(self, conf):
        self.logger.debug("Begin")
        localDir = conf.FindNode('XML_FILE_LOCAL_DIR')
        if localDir is None:
            self.logger.error("localDir info not found in config.!")
        else:
            localDir = localDir.text
            self.logger.debug("localDir is "+localDir)
        self.logger.debug("End")
        return localDir


if __name__ == '__main__':
     from util import logger, class_xml
     logger = logger.get_logger('TestLog.log', 'DEBUG')
    # cr = ConfigReader(logger)
     #cr.get_failed_flag(r'..\etc\configs\MH_EXECUTE.CONFIG')
     #cr.get_ipaddress()


#     cr.get_client_build_no("manhattan",r'\\10.17.1.56\builds\212.4000.1501.0')
     #cf = class_xml.xmlClass(r'..\etc\configs\PSERIES_EXECUTE.CONFIG')
     #cr.get_shorebotdir(cf)
     #cr.get_failed_flag(cf)
#     print(cr.get_device(cf, 'MHCLIENT'))
