from celery import Celery
from billiard import current_process
from billiard.exceptions import TimeLimitExceeded
import subprocess
# from celery.exceptions import SoftTimeLimitExceeded, TimeLimitExceeded
# import redis

app = Celery('tasks', backend='redis://', broker='redis://localhost:6379/0')
app.conf.CELERY_IGNORE_RESULT = False
app.conf.CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'

@app.task
def run_cmd(cmd):
    # redis_instance = redis.Redis()
    print("executing command :", cmd)
    try:
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        #p = subprocess.Popen('ping 10.198.128.78',stdout=subprocess.PIPE,stderr=subprocess.PIPE)
        output = p.communicate()
        p.terminate()
        #myname = getName()
        #print(myname)
        return 'DONE', output

    except subprocess.CalledProcessError, e:
        #print("finally")
        #redis_instance.publish(myname,'QUIT')
        print('Error executing command: ',cmd , str(e))
        return 'ERROR', str(e)

@app.task
def getName():
    p = current_process()
    print(p)
    return p.initargs[1].split('@')[1]