
import os
import subprocess
import re
import paramiko
import socket, traceback, sys , time
from paramikoe import SSHClientInteraction

def get_mac(ip):
    if not ip:
        return 0
    os.system('ping {0}'.format(ip))
    try :
        out = subprocess.check_output('arp -a | findstr {0}'.format(ip),shell=True)
    except subprocess.CalledProcessError :
        return 0
    if not out:
        return 0
    mac = out.strip().rstrip().split()[1]
    if not re.search('^([0-9A-Fa-f]{2}[-]){5}([0-9A-Fa-f]{2})$',mac):
        return 0
    return mac
 

def fetch_and_save_switch_mac_to_sysCfg(configParams):
    '''
    Author: mkr
    To fetch and save the switches mac address to system.cfg
    '''
    found = 1
    with open("C:\\HCLT\\Arc\\ConfigFiles\\System.cfg",'a') as f:
        for sw,ip in zip(
            ('vphone_mac','vtrunk_mac','vucb_mac','ldvs_mac'),
            (configParams['vphone_ip'],configParams['vtrunk_ip'],configParams['vucb_ip'],configParams['ldvs_ip'])
            ):
            mac=get_mac(ip)
            if mac:
                f.write(sw+'='+mac+'\n')
            else :
                found = 0
    return found
                

def fetch_and_save_build_to_buildCfg(configParams):
    '''
    Author: mkr
    To fetch and save the build number to build.cfg
    '''
    found = 1
    with open("C:\\HCLT\\Arc\\ConfigFiles\\Build.cfg",'a') as f:
        match = re.search(".*\\\\([\d\.]+)$",configParams['build_drive_folder'])
        if match:
            f.write('\nbuild='+match.group(1)+'\n')
        else:
            found = 0
    return found        
    
def set_hq_ip_in_vswitches(vswitches, hq_ip):
    '''
    Author: mkr
    To update hq ip in vswitches
    '''

    client = paramiko.SSHClient()
    client.load_system_host_keys()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    for device in vswitches:
        try:
            #ssh.connect(ip, port, user, password, timeout=time_out)
            client.connect(hostname=device['IP'], username=device['USER'], password=device['PASSWORD'])
            interact = SSHClientInteraction(client, display=True)
            print("Ssh to {0} Success!! ".format(ip))
        except paramiko.AuthenticationException:
            print("Unable to ssh {0}, Authentication problem !".format(ip))
            return 0
        except socket.error, e:
            print("Unable to ssh {0}, Communication problem !".format(ip))
            return 0
        
        interact.expect('.+')
        interact.send('su')
        interact.expect('.+')
        interact.send('ShoreTel')
        interact.expect('.+#\s*')
        interact.send('stcli')
        interact.expect('.+>\s*')
        interact.send('3')
        interact.expect('.+>\s*')
        interact.send('4')
        interact.expect('.+>\s*')
        interact.send('10.198.128.93')
        interact.expect('.+>\s*')
        interact.send('0')
        interact.expect('.+>\s*')
        interact.send('0')
        interact.expect('.+>\s*')
        interact.send('y')
        interact.expect('.+#\s*')
        interact.send('> /etc/ubootenv/cntrlsrv')
        client.close()
        return 1

def upgrade_vswitches(vswitches, hq_ip):
    '''
    Author: mkr
    To upgrade vswitches build
    '''

    client = paramiko.SSHClient()
    client.load_system_host_keys()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    for device in vswitches:
        try:
            #ssh.connect(ip, port, user, password, timeout=time_out)
            client.connect(hostname=device['IP'], username=device['USER'], password=device['PASSWORD'])
            interact = SSHClientInteraction(client, display=True)
            print("Ssh to {0} Success!! ".format(ip))
        except paramiko.AuthenticationException:
            print("Unable to ssh {0}, Authentication problem !".format(ip))
            return 0
        except socket.error, e:
            print("Unable to ssh {0}, Communication problem !".format(ip))
            return 0
        
        interact.expect('.+')
        interact.send('su')
        interact.expect('.+')
        interact.send('ShoreTel')
        interact.expect('.+#\s*')
        interact.send('upgrade 1')
        interact.expect('.+')
        return 1
        
def create_dest_dict(cmdList):
    maincommandlist = []
    subdict = {}
    linecount = 0
    isthread = False
    for cmd in cmdList:
        cmd=cmd.split()
        if isthread == False:
            if re.search(r'thread', cmd[0].lower()):
                linecount = int(cmd[1])
                isthread = True
            else:
                #not a thread create dictionary and append to main list
                subdict[cmd[0]]=[" ".join(cmd[1:])]
                maincommandlist.append(subdict)
                subdict={}
        else:
            #add line to dict
            if cmd[0] in subdict.keys():
                subdict[cmd[0]].append(" ".join(cmd[1:]))
            else:
                subdict[cmd[0]]=[" ".join(cmd[1:])]
            linecount = linecount - 1
            if linecount == 0:
                #add the sub dictionary to list
                maincommandlist.append(subdict)
                isthread = False
                subdict={}

    return maincommandlist