import sys
import os
import socket
import time
import subprocess
import signal
import re
from optparse import OptionParser


def main(*args):
    P_Series_Dir = r'C:\P-Series-Automation\Azure\squish-4.1.0-qt46x-win32-msvc9\bin'
    SquishServerCmd = os.path.join(P_Series_Dir,r'squishserver.exe')
    SquishRunnerCmd = os.path.join(P_Series_Dir,r'squishrunner.exe')
    SquishRunnerCmd = SquishRunnerCmd + " --host localhost --testcase " + os.path.join(r'Q:\testsuites',args[1]) + " -objectmap Q:/testsuites/shared/objects.map"
    print(SquishRunnerCmd,SquishServerCmd)
    start_server_runner(SquishServerCmd,SquishRunnerCmd,P_Series_Dir)
    os.system("taskkill /F /IM eggdrop.exe")
    os.system("taskkill /F /IM squishserver.exe")
    time.sleep(5)
    os.system("taskkill /F /IM _squishrunner.exe")
    time.sleep(5)
    os.system("taskkill /F /IM _squishserver.exe")
    time.sleep(5)
    sys.exit(0)

def find_testcasename(tcfn):
    with open(os.path.join(r'C:\depot\phone\auto\shorebot\shorebot\testconfigs',tcfn),'r') as f:
        tc=f.read()
    print(tc)
    c=0
    for root,dirs,files in os.walk(r'Q:\testsuites'):
        print(dirs,c)
        c+=1
        for dir in dirs:
            if re.search(tc,dir):
                return os.path.join(root,dir)
    
def start_server_runner(serverCmd,runnerCmd,Dir):
    global server_p
    print("before execution")
    server_p = subprocess.Popen(serverCmd,stdout=None,cwd=Dir)
    print("after execution")
    time.sleep(5)
    #global runner_p
    #runner_p = subprocess.Popen(runnerCmd,cwd=Dir,stdout=None)
    ipaddress=socket.gethostbyname(socket.gethostname())
    print("ATF IP is ",ipaddress)
    print(subprocess.check_output(runnerCmd,stdin=None,stderr=subprocess.STDOUT,shell=True))
    #os.system("C:\\depot\\phone\\auto\\shorebot\\shorebot\\shorebot_server.bat")
    
    
if __name__=="__main__":
    parser = OptionParser()
    parser.add_option("-m", "--model", dest="model", type="choice",
                      choices=['p8cg','p8'],
                      help="PPhone Model : one of p8cg, p8")
    parser.add_option("-f","--file", dest="file" , type="string",
                      help="TestCaseFile")
    parser.add_option("-b","--build", dest="build" , type="string",
                      help="PPhone Build Number")

    (options, args) = parser.parse_args()
    
    main(options.model,options.file,options.build)
