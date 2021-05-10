__author__ = 'mkr'


from util import windows_machine, mac_machine
from celery.task.control import revoke
from celery.result import AsyncResult
from tasks import app
from celery.exceptions import TimeoutError

import re

class CeleryWorker():
    def __init__(self, ip, user, password, workerName, redisServer, redisPort, os='windows'):
        self.ip = ip
        self.user = user
        self.password = password
        self.workerName = workerName
        self.redisServer = redisServer
        self.redisPort = redisPort
        #self.taskFile = taskFile
        self.celery_conf_file = self.workerName+'.py'
        '''
        Modified By : Jahnavi
        Date : 25 -Apr-2016
        Desc : code to connect mac machines
        '''
        if os.upper() == "MAC":
            self.macMachine = mac_machine.MacMachine(self.ip,self.user,self.password)
        else:
            self.windowsMachine = windows_machine.WindowsMachine(self.ip,self.user,self.password)
        self.start()

    def start(self):
        #self.stop()
        if not self.is_worker_alive(self.workerName):
            print("Celery Worker ", self.workerName, " does not exist. Is celery worker started??")
            raise Exception("Celery Worker "+self.workerName+" does not exist. Is celery worker started??")
            # self.create_celery_conf()
            # self.windowsMachine.net_copy(self.celery_conf_file,r'C:\Python27\Scripts')
            # #self.windowsMachine.net_copy(self.taskFile,r'C:\Python27')
            #
            # cmd = r'cd C:\Python27\Scripts & start "celery" cmd /k Celery.exe -A ' \
            #       + self.workerName + ' worker -n  ' + self.workerName + ' -Q  ' + self.workerName + ' -l info -f ' + self.workerName + '.log'
            # self.windowsMachine.run_remote(cmd)
        else:
            print("Celery Worker ", self.workerName, " is Alive. skip starting..")

    def create_celery_conf(self):
        with open(r'util\celery_conf_template.py', 'r') as f:
            conf = f.read()
        conf = re.sub(r'\$redis_ip',self.redisServer,conf)
        conf = re.sub(r'\$redis_port',self.redisPort,conf)
        conf = re.sub(r'\$name',self.workerName, conf)
        with open(self.celery_conf_file, 'w') as f:
            f.write(conf)

    def run(self, cmd, async=False, timeout=9999999, task=None):
        if not task:
            print("Executing Celery cmd: ", cmd)
            ret = app.send_task(self.workerName+'.run_cmd', args=[cmd], kwargs={}, queue=self.workerName)
            if async:
                return ret
            else:
                try:
                    return ret.get(timeout=timeout), None
                except TimeoutError:
                    task = AsyncResult(ret.task_id)
                    # print(task.info)
                    #out = task.info['PROGRESS']
                    self.stop_task(ret.task_id)
                    # return 'TIMEOUT', out
                    return 'TIMEOUT', None
        else:
            print("Inside celery worker",[cmd])
            ret = app.send_task(self.workerName+'.'+task, args=[cmd], kwargs={}, queue=self.workerName)
            try:
                return ret.get(timeout=timeout)
            except TimeoutError:
                return None

    def stop(self):
        # print("Stoping celery worker")
        # cmd = '''taskkill /f /im celery.exe'''
        # print(cmd)
        pass
        # self.windowsMachine.run_remote(cmd)

    def __del__(self):
        self.stop()
        # del self.windowsMachine
        pass

    def is_worker_alive(self, workerName):
        #app = Celery('app',broker="redis://")
        celery_dict = app.control.inspect().stats()
        #print(celery_dict)

        for cel in celery_dict.keys() if celery_dict else []:
            if re.match('celery@'+workerName, cel):
                print("Celery worker:", workerName, "is active")
                return True
        return False

    def stop_task(self, task_id):
        try:
            revoke(task_id, terminate=True)
        except Exception:
            print("Could not revoke task {0}".format(task_id))

#cw = CeleryWorker('10.198.128.78', 'Administrator', 'shoreadmin1', 'MH_VTF78', 'mkr-t440s.shoretel.com', '6379')
#CeleryWorker('10.30.12.117','','','VTF78','10.30.12.117','6379')

# ret = tasks.run_cmd.apply_async([r'cmd /c start c:\python27\python.exe'],  queue='MH_VTF78', timeout=10, soft_timeout=20)
# ret = tasks.run_cmd.apply_async([r'cmd /c start c:\python27\python.exe'],  queue='MKR')
#     # apply_async(args=[r'cmd /c start c:\python27\python.exe'], queue='MH_VTF78', timeout=20)
# try:
#     print(ret.get(timeout=10))
# except TimeoutError:
#     print("Task Timed out")