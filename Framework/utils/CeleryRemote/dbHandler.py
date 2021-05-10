import MySQLdb
from datetime import datetime
class dbHandler:
    
    def __init__(self,host='10.198.159.12',user='root',password='rodphase2',dbname='cc_roddb2'):
        self.host = host
        self.user = user
        self.password = password
        self.dbname = dbname
        self.handle = MySQLdb.connect(self.host,self.user,self.password,self.dbname)
        self.handle.autocommit(True)
        self.cursor = self.handle.cursor()

    # def connectdb(self):
    #     try:
    #         self.handle = MySQLdb.connect(self.host,self.user,self.password,self.dbname)
    #     except MySQLdb.Error:
    #         print(MySQLdb.Error)
    #         self.handle = None
    #     return self.handle

    def set_run_id(self,runid):
        self.runid = runid

    def execute_select_query(self,query):
        if self.handle.open:
            pass
        else:
            print(("inside else####"))
            self.handle = MySQLdb.connect(self.host,self.user,self.password,self.dbname)
            self.handle.autocommit(True)
            self.cursor = self.handle.cursor()
        self.cursor.execute(query)
        return self.cursor.fetchall()
        #return self.cursor.lastrowid
        
    def execute_insert_query(self,query):
        if self.handle.open:
            pass
        else:
            self.handle = MySQLdb.connect(self.host,self.user,self.password,self.dbname)
            self.handle.autocommit(True)
            self.cursor = self.handle.cursor()
        self.cursor.execute(query)
        #return self.cursor.fetchall()
        return self.cursor.lastrowid

    def get_prepare_query(self,table,value):
        #print("SELECT id from "+table +" " +"where name='%s'" % value)
        return "SELECT id from "+table +" " +"where name='%s'" % value
        
    def get_project_id(self,projectname):
        query = "SELECT id FROM rodexecute_project WHERE name = '{0}'".format(projectname)
        print(query)
        data = self.execute_select_query(query)
        if not data:
            return 0
        else:
            return data[0][0]
            
    def get_testcase_id(self,testcasename):
        query = "SELECT id FROM rodexecute_testcase WHERE name = '{0}'".format(testcasename)
        print(query)
        data = self.execute_select_query(query)
        if not data:
            return 0
        else:
            return data[0][0]

    def get_testcase_tcid(self,testcasename):
        query = "SELECT tcid FROM rodexecute_testcase WHERE name = '{0}'".format(testcasename)
        print(query)
        data = self.execute_select_query(query)
        if not data:
            return 0
        else:
            return data[0][0]

    def get_suite_id(self,suitename):
        query = "SELECT id FROM rodexecute_testsuite WHERE name = '{0}'".format(suitename)
        data = self.execute_select_query(query)
        if not data:
            return 0
        else:
            return data[0][0]
            
    def get_testbed_id(self,testbed_name):
        query = "SELECT id FROM rodexecute_testbed WHERE name = '{0}'".format(testbed_name)
        print(query)
        data = self.execute_select_query(query)
        if not data:
            return 0
        else:
            return data[0][0]
     
    def get_build_id(self,buildno, pid):
        query = "SELECT id FROM rodexecute_build WHERE number = '{0}' and project_id = {1}" .format(buildno,pid)
        print(query)
        data = self.execute_select_query(query)
        if not data:
            return 0
        else:
            return data[0][0] 

    def get_testexecutionstate_id(self,statename):
        query = "SELECT id FROM rodexecute_testexecutionstate WHERE name = '{0}'".format(statename)
        print(query)
        data = self.execute_select_query(query)
        if not data:
            return 0
        else:
            return data[0][0] 
          
    def get_testcasestatus_id(self,statusname):
        query = "SELECT id FROM rodexecute_testcasestatus WHERE name = '{0}'".format(statusname)
        print(query)
        data = self.execute_select_query(query)
        if not data:
            return 0
        else:
            return data[0][0] 
            
    tglDict = {'gname1':['gname1_TestCase1','gname1_TestCase2','gname1_TestCase3','gname1_TestCase4'],'gname2':['gname2_TestCase1','gname2_TestCase2','gname2_TestCase3','gname2_TestCase4']}   
    
    def get_running_tc_ids(self,eid):
        tc_state_id = self.get_testcasestatus_id('Running')
        query = "SELECT testcase_id from rodash_testresult WHERE testexecution_id = '{0}' and status_id = '{1}'".format(eid,tc_state_id)
        print(query)
        data = self.execute_select_query(query)
        if not data:
            return 0
        else:
                return [row[0] for row in data]
    
    def insert_test_info(self,pid,sid,tglDict):
        print("inside : insert_test_info")
        print(tglDict)
        for gname in tglDict['groupList']:
            gid = self.insert_test_group(pid,sid,gname,"")
            if not gid:
                print("Error inserting testgroup %s into database" % gname)
                return 0
            for tc in tglDict["testList"][gname]:
                tcid = tc.split('_')[-1]
                if not tcid:
                    print("Could not fetch testcase id from testcase %s" % tc)
                    return 0
                if not self.insert_test_case(gid,tcid,tc,""):
                    print("Error inserting testcase %s into database" %tc)
                    return 0
        return 1

    def insert_test_info2(self,pid,sid,tglDict):
        print("inside : insert_test_info")
        print(tglDict)
        for tc,val in tglDict.items():
            gname = val[1]
            gid = self.insert_test_group(pid,sid,gname,"")
            if not gid:
                print("Error inserting testgroup %s into database" % gname)
                return 0
            tcid = tc.split('_')[-1]
            if not tcid:
                print("Could not fetch testcase id from testcase %s" % tc)
                return 0
            if not self.insert_test_case(gid,tcid,tc,""):
                print("Error inserting testcase %s into database" %tc)
                return 0
        return 1

        # for gname in tglDict['groupList']:
        #     gid = self.insert_test_group(pid,sid,gname,"")
        #     if not gid:
        #         print("Error inserting testgroup %s into database" % gname)
        #         return 0
        #     for tc in tglDict["testList"][gname]:
        #         tcid = tc.split('_')[-1]
        #         if not tcid:
        #             print("Could not fetch testcase id from testcase %s" % tc)
        #             return 0
        #         if not self.insert_test_case(gid,tcid,tc,""):
        #             print("Error inserting testcase %s into database" %tc)
        #             return 0
        # return 1

    def insert_test_group(self,pid,sid,gname,gdesc):
        query = "SELECT id FROM rodexecute_testgroup WHERE name = '{0}'".format(gname)
        self.cursor.execute(query)
        data = self.cursor.fetchall()
        if data:
            gid = data[0][0]
        else:
            gid = 0
        
        #test group does not exist, insert        
        if not gid:
            query = "INSERT INTO rodexecute_testgroup (name,description,project_id) values('{0}','{1}',{2})".format(gname,gdesc,pid)
            print(self.cursor.execute(query))
            gid = self.cursor.lastrowid
        
        query = "SELECT id FROM rodexecute_testgroup_testsuites WHERE testgroup_id = {0} AND testsuite_id = {1}".format(gid,sid)
        self.cursor.execute(query)
        data = self.cursor.fetchall()
        if data:
            tgsid = data[0][0]
        else:
            tgsid = 0
            
        #testgroup is not related to testsuite, relate
        if not tgsid:
            #relate testgroup and  testsuite
            query = "INSERT INTO rodexecute_testgroup_testsuites (testgroup_id,testsuite_id) values({0},{1})".format(gid,sid)
            print(self.cursor.execute(query))
            print(self.cursor.lastrowid)
        
        return gid
        
        
    def insert_test_case(self,gid,tcid,tcname,tdesc):
        query = "SELECT id FROM rodexecute_testcase WHERE name = '{0}'".format(tcname)
        self.cursor.execute(query)
        data = self.cursor.fetchall()
        if data:
            tid = data[0][0]
        else:
            tid = 0
        #test case does not exist, insert
        if not tid:
            query = "INSERT INTO rodexecute_testcase (tcid,name,description,testgroup_id) values('{0}','{1}','{2}',{3})".format(tcid,tcname,tdesc,gid)
            print(self.cursor.execute(query))
            tid =  self.cursor.lastrowid
        
        return tid
        
    def insert_test_execution(self,pid,sid,bid,sbid,eby,tbid,stateid,paramid):
        print("inside : insert_test_execution")
        #query = "INSERT INTO rodexecute_testexecution (project_id,testsuite_id,primarybuild_id,secondarybuild_id,executedby,testbed_id,state_id,createtime,starttime) values({0},{1},{2},{3},'{4}',{5},{6},'{7}','{8}')".format(pid,sid,bid,sbid,eby,tbid,stateid,datetime.now(),datetime.now())
        query = "INSERT INTO rodexecute_testexecution (project_id,testsuite_id,primarybuild_id,secondarybuild_id,executedby,testbed_id,state_id,createtime,starttime,paramid_id) values({0},{1},{2},{3},'{4}',{5},{6},'{7}','{8}','{9}')".format(pid,sid,bid,sbid,eby,tbid,stateid,datetime.now(),datetime.now(),paramid)
        print(self.cursor.execute(query))
        teid =  self.cursor.lastrowid
        return teid
    
    def insert_testbed(self,name,desc,ownedby):
        query = "INSERT INTO rodexecute_testbed (name,description,ownedby) values('{0}','{1}','{2}')".format(name,desc,ownedby)
        print(self.cursor.execute(query))
        tbid =  self.cursor.lastrowid
        return tbid
        
    def insert_build(self,number,desc,pid):
        query = "INSERT INTO rodexecute_build (number,description,project_id) values('{0}','{1}',{2})".format(number,desc,pid)
        print(self.cursor.execute(query))
        bid =  self.cursor.lastrowid
        return bid
    
    def insert_test_result(self,teid,tcid,statusid):
        query = "INSERT INTO rodexecute_testresult (testcase_id,testexecution_id,createtime,status_id) values({0},{1},'{2}',{3})".format(tcid,teid,datetime.now(),statusid)
        print(self.cursor.execute(query))
        trid =  self.cursor.lastrowid
        return trid
    
    def update_test_execution_end(self,teid,stateid):
        query = "UPDATE rodexecute_testexecution SET state_id={0},endtime='{1}' WHERE id = {2}".format(stateid,datetime.now(),teid)
        print(query)
        print(self.cursor.execute(query))
        teid =  self.cursor.lastrowid
        return teid

    def update_test_execution_runid(self,teid):
        query = "UPDATE rodexecute_testexecution SET run_id={0} WHERE id = {1}".format(self.runid,teid)
        print(query)
        print(self.cursor.execute(query))
        teid =  self.cursor.lastrowid
        return teid
    
    def update_test_result_start(self,teid,tcid,statusid,item_id):
        query = "UPDATE rodexecute_testresult SET status_id={0}, starttime='{1}',item_id={2} WHERE testcase_id = {3} AND testexecution_id = {4}".format(statusid,datetime.now(),item_id,tcid,teid)
        print(query,)
        print(self.cursor.execute(query))
        trid =  self.cursor.lastrowid
        return trid
    
    def update_test_result_end(self,teid,tcid,statusid):
        query = "UPDATE rodexecute_testresult SET status_id={0}, endtime='{1}' WHERE testcase_id = {2} AND testexecution_id = {3}".format(statusid,datetime.now(),tcid,teid)
        print(query,)
        print(self.cursor.execute(query))
        trid =  self.cursor.lastrowid
        return trid
        
#DBHandler("10.198.159.12","root","rodphase2","roddb2").execute_select_query()
# mydbhandler = dbHandler("10.198.159.12","root","rodphase2","roddb2")
#mydbhandler = dbHandler("localhost","root","Myl@1990","roddb2")
# mydbhandler.connectdb()
#mydbhandler.execute_insert_query("insert into rodexecute_project(name,description) values('Manhattan',''),('Mobility',''),('Highball','')")
#mydbhandler.execute_insert_query("insert into rodexecute_testsuite(name,description) values('BCO',''),('Regression','')")
# mydbhandler.execute_insert_query("insert into rodexecute_testbed(name,description,ownedby) values('mkr_manhattan_tb1','This is Mylaris Testbed for Manhattan','Mylari')")

#mydbhandler.insert_test_group(1,1,'group2','group1 description')
#print(mydbhandler.get_project_id('mobility'))
