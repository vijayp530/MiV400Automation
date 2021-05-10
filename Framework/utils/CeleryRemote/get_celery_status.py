__author__ = 'mkr'

import re

from celery import Celery

def is_worker_alive(self, workerName):
    app = Celery('app',broker="redis://")
    celery_dict = app.control.inspect().stats()
    # print(celery_dict.keys())

    for cel in celery_dict.keys() if celery_dict else []:
        if re.match('celery@'+workerName, cel):
            print("Celery worker:",workerName,"is active")
            return True
    return False

def start_worker(self,ipaddr,userId='administrator',password='shoreadmin1'):

        self.s = winrm.Session(ipaddr, auth=(userId, password))

        celery_data = ""
        with open(r'c:\python27\scripts\tasks.py','r') as f:
            celery_data = f.read()
        self.s.run_cmd()

#if __name__ == '__main__':
#    print(is_worker_alive('','vha_manhattan_tb1-MHCLIENT1'))
