__author__ = 'mkr'

import os
import re
import time
import socket
import subprocess
import glob
import shutil
import redis
from celery import Celery
from billiard import current_process


app = Celery('celeryTasks', backend='redis://',broker='redis://10.163.98.21:6379/0')
app.conf.CELERY_IGNORE_RESULT = False
app.conf.CELERY_RESULT_BACKEND = 'redis://10.163.98.21:6379/0'

@app.task()
def run_cmd(*args,**kwargs):

    cmd = " ".join(args)
    print("executing command :", cmd)
    try:
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out = ""
        while p.poll() is None:
            l = p.stdout.readline()
            print(l)
            out += l
            run_cmd.update_state(
                state = 'PROGRESS',
                meta = {'PROGRESS': out}
            )
        l = p.stdout.read()
        print(l)
        out += l
        return out
    except subprocess.CalledProcessError, e:
        print('Error executing command: ', cmd)
        return str(e)

@app.task()
def get_staf_log(*args, **kwargs):
    #f = max(glob.iglob(r'C:\HCLT\vtftestpkg\vtf\shoretel-test\MHClient\reports\*'), key=os.path.getctime)
    f = r'C:\HCLT\vtftestpkg\vtf\shoretel-test\MHClient\reports\staf_server.log'
    print("staf file name##" + f)
    with open(f) as fd:
        out = fd.read()
        fd.close()
    with open (f , 'w'):
       pass
    if out == "":
        out = "STAF Server not started "
    print("staf log####"+out+"#####staf log")
    return out

@app.task()
def get_teamcity_build(*args,**kwargs):
    build = "".join(args)
    print("Teamcity Build Id:" + build)
    if os.path.exists('artifacts.zip'):
        os.remove('artifacts.zip')
    return subprocess.call([r'sh /Users/teamworkautomation/teamwork-ios-automation/test/get_build.sh ' + build],shell=True)


@app.task()
def get_robot_log(*args, **kwargs):
    #f = max(glob.iglob(r'C:\HCLT\vtftestpkg\vtf\shoretel-test\MHClient\reports\*'), key=os.path.getctime)
    f = r'/Users/teamworkautomation/teamwork-ios-automation/test/log.html'
    print("Robot logfile name##" + f)
    with open(f) as fd:
        out = fd.read()
        fd.close()
    if out == "":
        out = "Robot output log not found"
        print("Robot log####"+out+"#####Robot log")
    return out

@app.task()
def run_robot_test(*args, **kwargs):
    tcid_tag = "".join(args)
    try:
        path=r'/Users/shoretel/teamwork-ios-automation/test'
        print("starting teamwork ios test %s" % tcid_tag)
        # p = subprocess.Popen(["python", "-m", "robot", "-i", tcid_tag, "."], stdout=subprocess.PIPE, shell=True)
        p = subprocess.Popen(["python", "-m", "robot", "-i", tcid_tag, "."])
        
        # (output, err) = p.communicate()
        
        #This makes the wait possible
        p_status = str(p.wait())
        
        #This will give you the output of the command being executed
        print("Command output: " + p_status)
        print("test case execution over !!!")
        
        #Rerun if failed N times
        
        #Remote copy file to ATF Host
        return p_status
    except subprocess.CalledProcessError, e:
        print('Error executing command: ', cmd)
        return str(e)

@app.task()
def run_squish(*args, **kwargs):
    cmd = "".join(args)
    try:
        path=r'C:\P-Series-Automation\Azure\squish-4.1.0-qt46x-win32-msvc9\bin\squishserver.exe'
        cwd=r'C:\P-Series-Automation\Azure\squish-4.1.0-qt46x-win32-msvc9\bin\\'
        print("starting squish server")
        subprocess.Popen(path,stdout=None,cwd=cwd)
        print("executing test case ..",cmd)
        output = subprocess.check_output(cmd,stdin=None,stderr=subprocess.STDOUT,shell=True)
        print("test case execution over !!!")
        return output
    except subprocess.CalledProcessError, e:
        print('Error executing command: ', cmd)
        return str(e)


@app.task()
def pr(*args, **kwargs):
    print("HERE!")
    return 3
