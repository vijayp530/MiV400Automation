__author__ = 'mkr'

import os
import threading

TEMP_PATHS = [r'C:\Users\administrator\AppData\Local\Temp']
MH_APP_TEMP_FOLDER_PATTERN = '^nw[_0-9]*$'

def copy_build(clients, srcDir, srcUser, srcPassword, dstDir):
    # print(clients)
    print('##################*************UBS*****************#################')
    #for testbed in clients.keys():
    #    for client in clients[testbed]:
    #        map_drive(client, srcDir, srcUser, srcPassword)
    #        copy(client, srcDir, dstDir)
    threads1=[]
    threads2=[]
    for testbed in clients.keys():
        for client in clients[testbed]:
            #print(client)
            #print(clients[testbed])
            threads1.append(threading.Thread(target=map_drive, args=(client, srcDir, srcUser, srcPassword)))
            threads2.append(threading.Thread(target=copy, args=(client, srcDir, dstDir)))
    #print(threads1)
    #print(threads2)
    for (t1,t2) in zip(threads1,threads2):
        t1.start()
        t2.start()
    for (t1,t2) in zip(threads1,threads2):
        t1.join()
        t2.join()

    #for testbed in clients.keys():
    #    for client in clients[testbed]:
    #        threads2.append(threading.Thread(target=copy, args=(client, srcDir, dstDir)))
    #for t in threads2:
	#    t.start()
    #for t in threads2:
	#    t.join()
    print('##################*************UBS***************#################')

def map_drive(client, srcDir, srcUser, srcPassword):
    #print("Mapping network location {0} on client {1}".format(srcDir, client.workerName))
    cmd = "net use x: /delete /yes"
    client.run(cmd)
    cmd = "net use x: " + srcDir + " " + srcPassword + " /USER:" + srcUser
    client.run(cmd)

def copy(client, srcDir, dstDir):
    print("Copying Build from {0} to {1} on client {2}".format(srcDir, dstDir, client.workerName))
    cmd = "cmd /c xcopy " + os.path.join(srcDir, 'win') + " " + dstDir + " /e /y"

    client.run(cmd)

def clear_temp_folder(clients):
        print("Cleaning up temp folder(s) in clients")
        threads = [threading.Thread(target=client.run, kwargs={'cmd': None, 'task': 'purge_temp'}) for client in clients]
        print('##################*************UBS clear_temp_folder UBS*****************#################')
        print(threads)
        for t in threads:
            t.start()
        for t in threads:
            t.join()