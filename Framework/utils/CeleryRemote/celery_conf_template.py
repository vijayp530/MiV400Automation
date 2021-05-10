__author__ = 'mkr'

import os
import time
import socket
import subprocess
import glob
import shutil
import redis
from celery import Celery
from billiard import current_process


app = Celery('$name', backend='redis://',broker='redis://$redis_ip:$redis_port/0')
app.conf.CELERY_IGNORE_RESULT = False
app.conf.CELERY_RESULT_BACKEND = 'redis://$redis_ip:$redis_port/0'

#@app.task()
# def run_cmd(*args,**kwargs):
#
#     cmd = " ".join(args)
#     print("executing command :", cmd)
#     try:
#         p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
#         out = ""
#         while p.poll() is None:
#             l = p.stdout.readline()
#             print(l)
#             out += l
#             # run_cmd.update_state(
#             #     state = 'PROGRESS',
#             #     meta = {'PROGRESS': out}
#             # )
#         l = p.stdout.read()
#         print(l)
#         out += l
#         return out
#     except subprocess.CalledProcessError, e:
#         print('Error executing command: ', cmd)
#         return str(e)

@app.task()
def run_cmd(*args,**kwargs):

    cmd = " ".join(args)
    #redis_instance = redis.Redis(host='10.30.', port=6379, db=0)
    print("executing command :",cmd)
    try:
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        #p = subprocess.Popen('ping 10.198.128.78',stdout=subprocess.PIPE,stderr=subprocess.PIPE)
        output = p.communicate()

        #myname = getName()
        #print(myname)
        return output

    except subprocess.CalledProcessError, e:
        #print("finally")
        #redis_instance.publish(myname,'QUIT')
        print('Error executing command: ', cmd)
        return str(e)

@app.task()
def get_staf_log(*args, **kwargs):
    f = max(glob.iglob(r'C:\HCLT\vtftestpkg\vtf\shoretel-test\MHClient\reports\*'), key=os.path.getctime)
    with open(f) as fd:
        out = fd.read()
    return out

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
def purge_temp(*args, **kwargs):
    dir = os.environ['TEMP']
    pattern = '^nw[_0-9]*$'
    print("Purging directory tree - {0}/{1}".format(dir,pattern))
    for f in os.listdir(dir):
        if re.search(pattern, f):
            print("removing {0}".format(os.path.join(dir, f)))
            try:
                shutil.rmtree(os.path.join(dir, f))
            except Exception:
                pass