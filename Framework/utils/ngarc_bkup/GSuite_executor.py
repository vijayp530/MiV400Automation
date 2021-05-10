import xml.etree.ElementTree as ET
from datetime import datetime
import os
import sys
import re
import time
import datetime
import json
import subprocess
import shutil
from util import celery_worker, config_reader, file_handler, class_xml


class GSuiteExecutor():
    def __init__(self, gConf, input, reporter, logger):
        self.gConf = gConf
        self.input = input
        self.reporter = reporter
        self.logger = logger
        self.run_types = {'st_bco': 'gsuite_st_bco_done.txt', 'mt_bco': 'gsuite_mt_bco_done.txt', 'st_reg': 'gsuite_st_regr_done.txt', 'mt_regr': 'gsuite_mt_regr_done.txt', 'st_bco_pom':'st_bco_pom.txt', 'st_regr_pom':'st_regr_pom.txt',}
        self.configReader = config_reader.ConfigReader(self.logger)
        self.conf_file = os.path.join(
            self.configReader.get_config_path(self.gConf),
            self.configReader.get_project_action_config(self.gConf,self.input['project'],self.input['action'])
        )
        self.conf = class_xml.xmlClass(self.conf_file)
        
        self.runset_path = self.configReader.get_gsuite_runset_path(self.conf)
        self.configs_path = self.configReader.get_gsuite_configs_path(self.conf)
        self.backup_log_path = self.configReader.get_gsuite_backup_log_path(self.conf)
        self.test_rerun_count = self.configReader.get_gsuite_test_rerun_count(self.conf)
        
        
    def cleanup_on_timeout(self,*args , **kwargs):
        pass
    
    def cleanup(self):
        pass
        
    def do(self):
        self.logger.debug("Begin")
        
        the_run_type, run_module = str(self.input['run_type']).split(":")
        if "pom" in the_run_type:
            type = "pom"
        else:
            type = None
            
        self.branch = self.input['branch'].lower()
        
        self.build_path = self.configReader.get_gsuite_build_path(self.conf, self.branch)
        self.test_path = self.configReader.get_gsuite_test_path(self.conf, self.branch, type)

        self.build_version = self.get_build_version()
        self.print_run_info()

        self.logfile = "log_" + run_module + ".html"
        cmd_add = self.build_robot_cli_additions(run_module, self.logfile)
        
        tcid_file = os.path.join(self.runset_path,self.run_types[the_run_type])
        tcids_list = self.get_tcids_from_file(tcid_file)
      
        pdir = os.getcwd()
        os.chdir(self.test_path)
        # Run google deauthorize script
        os.system("python -m robot Google_Authorization_Flow\\tc_AuthorizationGoogleForTheFirstTime.robot")
        os.chdir(pdir)

        tcdict = {}
        for tc in tcids_list:
            tcdict[tc] = ['dummy_pkg_gapps','dummy_grp_gapps']
        
        #insert test cases not inserted before
        if not self.reporter.dbHandler.insert_test_info2(self.reporter.pid, self.reporter.sid,
                                                            tcdict):
            print("Error inserting test info to database, Exiting..")
        # insert all test cases to db and set status as not-executed
        self.initialize_test_result2(tcids_list)
        self.start_id = self.reporter.add_items(tcids_list)

        print(self.start_id)
        print('*') * 77
        runid = self.reporter.initialize()
        print(runid)
        for tc in tcids_list:
            # before starting execution of test case set its status to executing
            print("*** TCID %s id %s" % (tc,self.start_id))
            self.reporter.notify(self.reporter.dbHandler,'BEGIN', self.start_id, tc, 'Executing', None)
            
            os.chdir(self.test_path)
            tcid = "tc-" + tc
            cmd = "python -m robot " + cmd_add + " --include " + tcid + " ." 
            
            #Run cmd LOOP times as long as the test fails
            for loop_i in range(0, int(self.test_rerun_count)):
                print("**** DEBUG *** Kicking off %s run with cmd \"%s\" on following test: %s" % (self.input['run_type'],cmd,tcid))
                print("******Attempt Number %s" % (loop_i))
                os.system(cmd)

                # write logic to parse log/output to find status of test case
                status = self._backup_logs(tcid,  run_module)
                print("***** status: %s"%  status)
                if status == "PASS":
                    break;
                
            # assign test case log to log variable
            # fh = open("output.xml",'r')
            fh = open(self.logfile,'r')
            print("####READING LOGFILE")
            log = fh.read()
            print("#### LOGFILE READ")
            fh.close()
            os.chdir(pdir)
            self.reporter.notify(self.reporter.dbHandler,'END', self.start_id, tc, status, log)
            self.start_id+=1
        os.chdir(pdir)
        # Update test execution state to completed
        self.create_fail_summary(run_module)
        self.update_test_execution_end()
        runid = self.reporter.finalize()
        self.purge_temp()
        self.logger.debug("End")
        
    def update_test_execution_end(self):
        self.logger.debug("Begin")
        self.stateid = self.reporter.dbHandler.get_testexecutionstate_id('Completed')
        self.reporter.dbHandler.update_test_execution_end(self.reporter.teid, self.stateid)
        self.logger.debug("End")
     
    def  print_run_info(self):

        print("***DEBUG*** Kicking off gSuite ABCO run type %s on build %s" %  (self.input['run_type'], self.build_version))
        print("***DEBUG*** branch type is : ", self.branch)
        print("***DEBUG*** GAPPS_BUILD_PATH is : ", self.build_path)
        print("***DEBUG*** GSUITE_TEST_PATH is : ", self.test_path)
        time.sleep(10)
      
    def get_tcids_from_file(self, filename):
        tcids_list = []
        with open(filename) as f:
            for line in f:
                tcids_list.append(line.strip())    
        return tcids_list        
     
    def build_robot_cli_additions(self, run_module, logfile):
        cmd_add = ""
        cmd_add_ismt = ""
                
        cmd_add_crxpath = " --variable CRX_PATH:C:\\ATF_ROBOT\\run\\GSuite\\configs\\" +  run_module
        if self.branch == "dev":
            cmd_add_crxpath = cmd_add_crxpath + "\\dev_gsuite.crx "
        else:
            cmd_add_crxpath = cmd_add_crxpath+ "\\main_gsuite.crx "
        
        if self.input['run_type'] == "mt_bco":
            cmd_add_ismt = " --variable is_runtype_mt:true"
        
        cmd_add = cmd_add_crxpath + cmd_add_ismt +  " --variable ROBOT_RUNMODULE_DIR:" + run_module
        
        xmlfile = "out_"  + run_module + ".xml"       
        reportfile = "report_" + run_module + ".html"
        cmd_add = cmd_add +  " -o " + xmlfile
        cmd_add = cmd_add + " --log " + logfile
        cmd_add = cmd_add +  " --report " + reportfile
        
        return cmd_add

    def create_fail_summary(self, run_module):
        fw = open('Error_Summary.txt','w')
        fw.write("*** FAILED TESTS ***")
        the_run_type, run_module = str(self.input['run_type']).split(":")
        foldername = self.input['build']['client']  + "_" + self.input['branch'].lower() + "_" + the_run_type + "_" + self.input['build']['hq']
		
        total_fails = 0
        total_test = 0
        total_skip = 0

        FAIL_PREFIX = "\t * "
        backup_logspath = os.path.join(self.backup_log_path, run_module,foldername)
        fw.write("\n Building summary of %s \n" % backup_logspath)
        for filename in os.listdir(backup_logspath):
            if not filename.endswith(".xml"): continue

            fullname = os.path.join(backup_logspath,filename)
            total_test += 1

            tree = ET.parse(fullname)
            root = tree.getroot()

            # Find Errors
            found_error = False
            kw_index = 0
            msgs = []
            keyword = ''
            status_fail = ''
            for suite in root.iter('suite'):
                if suite.find('test') is not None:
                    for kw in tree.findall('./suite/suite/suite/test/kw'):
                        kw_index += 1
                        status = kw.find('status').get('status')
                        if "FAIL" in status:
                            found_error = True
                            # print(kw.get('name'))
                            status_fail = suite.find('test').find('status').text
                            xpath = "./suite/suite/suite/test/kw[{}]/kw".format(kw_index)
                            if len(tree.findall(xpath)) == 0:
                                keyword = kw.get('name')
                                for msg in kw.findall('msg'):
                                    msgs.append(FAIL_PREFIX + msg.text)

                                break
                            else: 
                                for innerkw in tree.findall(xpath):
                                    # print(innerkw.get('name'))
                                    status = innerkw.find('status').get('status')
                                    if "FAIL" in status:
                                        # import pdb; pdb.set_trace()
                                        # print(innerkw.get('name'))
                                        keyword = innerkw.get('name')
                                        for msg in innerkw.findall('msg'):
                                            # print(msg.text)
                                            msgs.append(FAIL_PREFIX + msg.text)

                                break
            
            if found_error == False:
                # print('NEXT!')
                total_skip += 1
                continue
                    

            # Find test path
            for suite in root.iter('suite'):
                srcpath = suite.get('source')
                if ".robot" in srcpath:
                    # print(srcpath)
                    break

            # Find Tags
            tags = []
            for stat in root.iter('statistics'):
                # import pdb; pdb.set_trace()
                for tag in stat.find('tag'):
                    tags.append(tag.text)
            
            tags = ' | '.join(tags)
            failures = '\n'.join(msgs)
            # print(srcpath)
            # print(tags)
            # print("*** FAIL INFO ***\n %s" %failures)

            total_fails += 1
            fw.write(srcpath + '\n')
            fw.write(tags + '\n')
            fw.write(keyword + '\n')
            fw.write(failures.encode("utf-8") + '\n')
            if status_fail.encode("utf-8") not in failures.encode("utf-8"):
                fw.write("STATUS FAIL: %s \n\n" % status_fail.encode("utf-8"))
        # print("total fails: %s" % total_fails)
        # print("total skip: %s" % total_skip)
        # print("total test: %s" % total_test)
        fw.close()

      
    def _backup_logs(self, tcid, run_module):
        the_run_type, run_module = str(self.input['run_type']).split(":")
        foldername = self.input['build']['client']  + "_" + self.input['branch'].lower() + "_" + the_run_type + "_" + self.input['build']['hq']
        results_path = os.path.join(self.configs_path,run_module,"logs",foldername)

        
        ts =  str(time.time()).split(".")[0]
        out_log = "log_" + run_module + ".html"
        out_report = "report_" + run_module + ".html"
        out_ouput = "out_" +  run_module + ".xml"
        
        backup_logspath = os.path.join(self.backup_log_path, run_module,foldername)
        if not os.path.exists(results_path):
            os.makedirs(results_path)
        if not os.path.exists(backup_logspath):
            os.makedirs(backup_logspath)

        dst  = os.path.join(results_path, str(tcid) + ts + '_log.html')
        dst2  = os.path.join(results_path, str(tcid) + ts + '_report.html')
        dst3  = os.path.join(results_path, str(tcid) + ts + '_output.html')
               
        print("DEBUG: archiving outputs to %s, %s, %s" % (dst, dst2, dst3))
        shutil.copy(out_log, dst)
        shutil.copy(out_report, dst2)
        shutil.copy(out_ouput, dst3)
      
        dst4 = os.path.join(backup_logspath,str(tcid) + '_output.xml')
        shutil.copy(out_ouput, dst4)
      
        et_path = dst3
        tree = ET.parse(et_path)
        root = tree.getroot()
        r = root.find("./statistics/suite")
        if r is not None:
            l = list(r.iter("stat"))
            print(l[2].attrib)
            result = l[2].attrib["fail"]
            print("result %s" % result)
            # set status variable as status of test case after execution
            #available status - pass,fail,scripterror,timeout, unknown
            if result == "0":
                status = 'PASS' 
            else:
                 status = 'FAIL'
        else:
             status = 'SCRIPTERROR'
         
        return status
            
    def initialize_test_result2(self, tclist):
        self.status_id = self.reporter.dbHandler.get_testcasestatus_id('Not Executed')
        for tc in tclist:
            tid = self.reporter.dbHandler.get_testcase_id(tc)
            self.reporter.dbHandler.insert_test_result(self.reporter.teid, tid, self.status_id)

                
    def get_build_version(self):
        # Check version in manifest and compare with abco_version
        with open(self.build_path + '\\latestbuild\\manifest.json') as df:
            data = json.load(df)
        new_ver =  data["version"].encode('utf-8')
        
        return new_ver

    def update_run_path(self):
        if(self.input['branch'] == 'dev' ):
            self.build_path = r'C:\WFDevGCAL\automation-gapps\builds'
            self.test_path = r'C:\WFDevGCAL\automation-gapps\testcases'
        else:
            self.build_path = r'C:\WebFramework\automation-gapps\builds'
            self.test_path = r'C:\WebFramework\automation-gapps\testcases'


    def purge_temp(self, *args, **kwargs):
        dir = os.environ['TEMP']
        pattern = '^scoped_dir[_0-9]*$'
        print("Purging directory tree - {0}/{1}".format(dir,pattern))
        for f in os.listdir(dir):
            if re.search(pattern, f):
                print("removing {0}".format(os.path.join(dir, f)))
                try:
                    shutil.rmtree(os.path.join(dir, f))
                except Exception:
                    pass