"""
Created BY: Abhishek khanchi
EmployeeID: 51810668
packet verifier

"""
import paramiko
from scp import SCPClient
# import

call_id_ls=[]
call_stack={}
sip_packets=[]
subscribePktList=[]
registerPktList=[]
value=None

def fileCleaner(**kwargs):
    import os
    import glob
    print(os.getcwd())
    path_local=kwargs['path_local']
    file_to_deleted=['pcap','json','txt','png']
    for i  in file_to_deleted:
        for filename in glob.glob('{0}/*.{1}'.format(path_local,i)):
            print(filename)
            os.unlink(filename)



def pcap_converter(**kwargs):
    """
    This Method convert PCAP file using
    TsharK into json and text
    :Input_File:
    :Op_file:
    :return: Nothing
    """
    """Inside pcap_to_json_converter"""
    import os
    import shutil
    from pprint import pprint
    Input_File=kwargs['local_pcap_download_file']
    Op_file=kwargs['local_json_download_file']
    op_txt_log=kwargs['pkt_log_with_path']
    protocol=kwargs['protocol']
    # op_txt_csv=kwargs['pkt_csv_with_path']


    """
      Below are example commands executed
       tshark -2 -R "TLS" -r Test.pcap -T json >output_TLS.json
       tshark -V -r Test.pcap > file_to_convert.txt"""
    if protocol=='tls':
        cmd1 = """tshark  -2 -R "tls" -r {0} -T json >{1}""".format(Input_File,Op_file)

        cmd2 = """tshark -V -r {0} > {1}""".format(Input_File,op_txt_log)

    elif protocol=='rtp':
        cmd1 = """tshark  -2 -R "rtp" -r {0} -T json >{1}""".format(Input_File, Op_file)

        cmd2 = """tshark -V -r {0} > {1}""".format(Input_File, op_txt_log)

    elif protocol=='sip':
        cmd1 = """tshark  -2 -R "sip" -r {0} -T json >{1}""".format(Input_File, Op_file)

        cmd2 = """tshark -V -r {0} > {1}""".format(Input_File, op_txt_log)

    # cmd3= """tshark  -2 -R "tls" -r {0} -T csv >{1}""".format(Input_File,op_txt_csv)
    ls=[cmd1,cmd2]
    for i in ls:
        #print i
        os.system(i)
    sip_logs  = open(op_txt_log,'r').readlines()
    pprint(sip_logs)

    return

def ssh_cmd(**kwargs):
    """Runs cmd via ssh on phone

    :param cmd: ssh cmd
    :type cmd: type str
    :return ret_val: ssh cmd result
    """
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        ip_address = kwargs['ip_address_server']
        username = kwargs['username']
        password = kwargs["password"]
        cmd=kwargs['cmd']

        ssh.connect(ip_address, username=username,password=password)
    except (paramiko.BadHostKeyException, paramiko.AuthenticationException,
            paramiko.SSHException):
        ssh.close()

        raise Exception("SSH connection failed!! IP, uname, or passwd is incorrect")
        return


    stdin, stdout, stderr = ssh.exec_command(cmd, get_pty=True)
    result = stdout.readlines()

    if ssh:
        ssh.close()
    return result



def scp_get(**kwargs):
    """Runs cmd via ssh on phone

    :param cmd: ssh cmd
    :type cmd: type str
    :return ret_val: ssh cmd result
    """
    ip_address = kwargs['ip_address_server']
    username = kwargs['username']
    password = kwargs["password"]
    file = kwargs['file']
    print("SCP getting %s " % file)
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(ip_address, username=username, password=password)
    with SCPClient(ssh.get_transport()) as scp:

            scp.get(file)
    if ssh:
        ssh.close()

def scp_put(**kwargs):
    """Runs cmd via ssh on phone

    :param cmd: ssh cmd
    :type cmd: type str
    :return ret_val: ssh cmd result
    """
    ip_address = kwargs['ip_address_server']
    username = kwargs['username']
    password = kwargs["password"]
    file = kwargs['file']
    print("SCP putting %s " % file)
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(ip_address, username=username, password=password)
    with SCPClient(ssh.get_transport()) as scp:

            try:
                scp.put(file)
            except:
                raise Exception("An error occured with scp.put(%s) " % file)

    if ssh:
        ssh.close()
def tls_packet_extractor(**kwargs):
    """
    :param kwargs:
    inputfile: packet

    :return:
    """
    import re
    proto_buf_tls={}
    count=0
    inputfile=kwargs['inputFile']
    with open(inputfile, 'r') as infile:
         copy = False
         for line in infile:
             if re.match("Transport Layer Security", line):
                        count+=1
                        proto_buf_tls.update({count:[]})
                        copy = True
             elif re.match("Frame", line):
                        copy = False
             elif copy:

                  inputs=line.rstrip().lstrip().split(':')
                  strlist=[x.rstrip().lstrip().replace(' ', '_') for x in inputs]
                  strlist.pop()
                  strlist.append(line.rstrip().lstrip().split(':')[-1].lstrip().rstrip())
                  stri = ':'.join(strlist)
                  proto_buf_tls[count].append(stri)
    return proto_buf_tls

def ipChecker(ipaddrstr):
            """
            Description
            This check ipv4 address availibility in text and return  the count of ip_address found
            :param kwargs: string containing ipaddress
            :return: len_ipls
            """
            #print "Inside ipChecker"
            from re import findall
            ip = ipaddrstr
            len_ipls = len(findall(r"\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b", ip))
            return len_ipls



def packet_parser(key,**kwargs):
    """
    Below method is sip packet parser and
    and extractor of sip-header value
    :param kwargs: sip dict
    :type kwargs: dict
    :return None:
    """

    key_new=key.replace('.','_')

    for k,v in kwargs.items():

        if isinstance(v,dict):
                packet_parser(key_new,**v)
        elif isinstance(v,list):
            for d in v:
                packet_parser(key_new,**d)
        else:

            key_json= k.replace('.','_')

            if key_json.lower() == str(key_new.lower()):

                global value
                value=v
                # print value
                break
            else:
                pass

def Base_Packet_Extracter(**kwargs):

    protocol=kwargs['protocol']
    if protocol=='sip':
        Base_Packet_Extracter_Sip(**kwargs)
    elif protocol=='tls':
         ret_dict=tls_packet_extractor(**kwargs)
         return ret_dict
    elif protocol=='rtpevent':
         retlist=rtpevent_packet_extractor(**kwargs)
         return retlist


def rtpevent_packet_extractor(**kwargs):
        """
        Below method extract invite method of sip call from json
        and append to datastructure call_stack
        :param kwargs(dict):
        :key local_json_download_file: json converted by PCAP_converter method
        :key source_dn: source phone dn
        :return: rtpeventdictlist
        """
        import json
        ipfile=kwargs['local_json_download_file']
        json1_file = open(ipfile)
        json1_str = json1_file.read()
        json1_data = json.loads(json1_str)
        # call_stack.clear()
        rtpeventdictlist = []

        for i in range(len(json1_data)):
            rtpeventdict = json1_data[i]['_source']['layers']['rtpevent']
            rtpeventdictlist.append(rtpeventdict)
            # rtp_mediaAttr_verifier(key, exval, ** rtpeventdict)
        return rtpeventdictlist

def Base_Packet_Extracter_Sip(**kwargs):
    """
    Below method extract invite method of sip call from json
    and append to datastructure call_stack
    :param kwargs(dict):
    :key sip_ip_addr_src: source phone ip address
    :key ip_address_server: Asterisk server IP address
    :key local_json_download_file: json converted by PCAP_converter method
    :key source_dn: source phone dn
    :return: restPacketextractor method
    """
    import ipaddress
    import json
    sip_ip_addr_src = kwargs['ip_addr_src']
    ip_address_server=kwargs['ip_address_server']
    local_json_download=kwargs['local_json_download_file']

    source_dn =kwargs['source_dn']
    src_ip_addr=ipaddress.ip_address(sip_ip_addr_src)
    dst_ip_addr=ipaddress.ip_address(ip_address_server)
    json1_file = open(local_json_download)
    json1_str = json1_file.read()
    json1_data = json.loads(json1_str)
    call_stack.clear()

    for i in range(len(json1_data)):
        sip_packet = json1_data[i]['_source']['layers']['sip']
        packet_parser(key="sip.Method", **sip_packet)
        pkt_sip_Method = value
        # print "sip method : {0} ".format(pkt_sip_Method)
        if pkt_sip_Method == 'INVITE':

            pkt_src_ipaddr=json1_data[i]['_source']['layers']['ip']["ip.src"]
            pkt_dst_ipaddr = json1_data[i]['_source']['layers']['ip']["ip.dst"]
            if ipChecker(pkt_src_ipaddr)>0:
                if ipChecker(pkt_dst_ipaddr)>0 :
                    pkt_src_ipaddr_fin=ipaddress.ip_address(pkt_src_ipaddr)
                    pkt_dst_ipaddr_fin = ipaddress.ip_address(pkt_dst_ipaddr)

                    if pkt_src_ipaddr_fin==src_ip_addr and pkt_dst_ipaddr_fin==dst_ip_addr:
                        packet_parser(key="sip.from.user", **sip_packet)
                        packet_user_dn = value

                        if source_dn==packet_user_dn:
                               packet_parser(key='sip.Call-ID', **sip_packet)
                               call_id = value

                               packet_parser(key='sip.CSeq.method', **sip_packet)
                               CSeq = value


                               if call_id_ls.__contains__(str(call_id)):
                                   pass
                               else:

                                  call_id_ls.append(str(call_id))

                               call_stack.update({str(call_id):{'INVITE':{'PACKET':json1_data[i]['_source']['layers']['sip'], 'RESPONSE':[]},
                                                                          'ACK': {'PACKET': None, 'RESPONSE': []},
                                                                          'BYE': {'PACKET': None, 'RESPONSE': []},
                                                                          'CANCEL': {'PACKET': None, 'RESPONSE': []},
                                                                          'OPTIONS': {'PACKET': None, 'RESPONSE': []},
                                                                          'PRACK': {'PACKET': None, 'RESPONSE': []},
                                                                          'NOTIFY': {'PACKET': None, 'RESPONSE': []},
                                                                          'PUBLISH': {'PACKET': None, 'RESPONSE': []},
                                                                          'INFO': {'PACKET': None, 'RESPONSE': []},
                                                                          'REFER': {'PACKET': None, 'RESPONSE': []},
                                                                          'MESSAGE': {'PACKET': None, 'RESPONSE': []},
                                                                          'UPDATE': {'PACKET': None, 'RESPONSE': []}

                                                                                    }})
                else:
                    pass
            else:
                raise Exception("NO Source IP address found in packet")
                pass
        if pkt_sip_Method == 'SUBSCRIBE':
             # print 'SUBSCRIBE'
             pkt_src_ipaddr = json1_data[i]['_source']['layers']['ip']["ip.src"]
             pkt_dst_ipaddr = json1_data[i]['_source']['layers']['ip']["ip.dst"]
             if ipChecker(pkt_src_ipaddr) > 0:
                if ipChecker(pkt_dst_ipaddr) > 0:
                    pkt_src_ipaddr_fin = ipaddress.ip_address(pkt_src_ipaddr)
                    pkt_dst_ipaddr_fin = ipaddress.ip_address(pkt_dst_ipaddr)
                    if pkt_src_ipaddr_fin == src_ip_addr and pkt_dst_ipaddr_fin == dst_ip_addr:
                        packet_parser(key="sip.from.user", **sip_packet)
                        packet_user_dn = value
                        if source_dn == packet_user_dn:

                              subscribePktList.append({'PACKET':json1_data[i]['_source']['layers']['sip']})
                              # print "abhishek khanchi SUBSCRIBE"
                else:
                     pass
             else:
                  raise Exception("NO Source IP address found in packet")
                  pass
        if pkt_sip_Method == 'REGISTER':
             pkt_src_ipaddr = json1_data[i]['_source']['layers']['ip']["ip.src"]
             pkt_dst_ipaddr = json1_data[i]['_source']['layers']['ip']["ip.dst"]
             if ipChecker(pkt_src_ipaddr) > 0:
                if ipChecker(pkt_dst_ipaddr) > 0:
                    pkt_src_ipaddr_fin = ipaddress.ip_address(pkt_src_ipaddr)
                    pkt_dst_ipaddr_fin = ipaddress.ip_address(pkt_dst_ipaddr)
                    if pkt_src_ipaddr_fin == src_ip_addr and pkt_dst_ipaddr_fin == dst_ip_addr:
                        packet_parser(key="sip.from.user", **sip_packet)
                        packet_user_dn = value
                        if source_dn == packet_user_dn:
                              registerPktList.append({'PACKET':json1_data[i]['_source']['layers']['sip']})



                else:
                     pass
             else:
                  raise Exception("NO Source IP address found in packet")
                  pass
    else:
        json1_file.close()
        return restPacketextractor(**kwargs)

def restPacketextractor(**kwargs):
    """
    Below method extract all other sip methods of sip call from json
    and append to datastructure call_stack

    :param kwargs(dict):
    :key local_json_download_file: json converted by PCAP_converter method
    :return: response_appender method
    """
    import json

    packetappended = 0
    local_json_download = kwargs['local_json_download_file']
    json1_file = open(local_json_download)
    json1_str = json1_file.read()
    json1_data = json.loads(json1_str)
    for key in call_id_ls:
        for i in range(len(json1_data)):
            sip_packet = json1_data[i]['_source']['layers']['sip']
            packet_parser(key="sip.Call-ID", **sip_packet)
            Call_ID_JSON = value
            packet_parser(key="sip.Method", **sip_packet)
            CSeq_JSON = value

            if Call_ID_JSON ==key:
                #print CSeq_JSON
                if CSeq_JSON=='UPDATE':

                    call_stack[key][CSeq_JSON]['PACKET']=sip_packet
                    packetappended += 1
                    #print 'Packet appended current is {0} {1}'.format(CSeq_JSON,packetappended)

                elif CSeq_JSON == 'ACK':
                    call_stack[key][CSeq_JSON]['PACKET'] = sip_packet
                    packetappended += 1
                    #print 'Packet appended current is {0} {1}'.format(CSeq_JSON, packetappended)

                elif CSeq_JSON=='BYE':
                    call_stack[key][CSeq_JSON]['PACKET'] = sip_packet
                    packetappended += 1
                    #print 'Packet appended current is {0} {1}'.format(CSeq_JSON, packetappended)

                elif CSeq_JSON=='ACK':
                    call_stack[key][CSeq_JSON]['PACKET'] = sip_packet
                    packetappended += 1
                    #print 'Packet appended current is {0} {1}'.format(CSeq_JSON, packetappended)


                elif CSeq_JSON=='OPTIONS':
                    call_stack[key][CSeq_JSON]['PACKET'] = sip_packet
                    packetappended += 1
                    #print 'Packet appended current is {0} {1}'.format(CSeq_JSON, packetappended)

                elif CSeq_JSON=='REGISTER':
                    call_stack[key][CSeq_JSON]['PACKET'] = sip_packet
                    packetappended += 1
                    #print 'Packet appended current is {0} {1}'.format(CSeq_JSON, packetappended)

                elif CSeq_JSON=='CANCEL':
                    call_stack[key][CSeq_JSON]['PACKET'] = sip_packet
                    packetappended += 1
                    #print 'Packet appended current is {0} {1}'.format(CSeq_JSON, packetappended)

                elif CSeq_JSON=='PRACK':
                    call_stack[key][CSeq_JSON]['PACKET'] = sip_packet
                    packetappended += 1
                    #print 'Packet appended current is {0} {1}'.format(CSeq_JSON, packetappended)

                elif CSeq_JSON=='SUBSCRIBE':
                    call_stack[key][CSeq_JSON]['PACKET'] = sip_packet
                    packetappended += 1
                    #print 'Packet appended current is {0} {1}'.format(CSeq_JSON, packetappended)


                elif CSeq_JSON=='NOTIFY':
                    call_stack[key][CSeq_JSON]['PACKET'] = sip_packet
                    packetappended += 1
                    #print 'Packet appended current is {0} {1}'.format(CSeq_JSON, packetappended)

                elif CSeq_JSON =='PUBLISH':
                    call_stack[key][CSeq_JSON]['PACKET'] = sip_packet
                    packetappended += 1
                    #print 'Packet appended current is {0} {1}'.format(CSeq_JSON, packetappended)

                elif CSeq_JSON=='INFO':
                    call_stack[key][CSeq_JSON]['PACKET'] = sip_packet
                    packetappended += 1
                    #print 'Packet appended current is {0} {1}'.format(CSeq_JSON, packetappended)

                elif CSeq_JSON=='REFER':
                    call_stack[key][CSeq_JSON]['PACKET'] = sip_packet
                    packetappended += 1
                    #print 'Packet appended current is {0} {1}'.format(CSeq_JSON, packetappended)

                elif CSeq_JSON=='MESSAGE':
                    call_stack[key][CSeq_JSON]['PACKET'] = sip_packet
                    #print 'Packet appended current is {0} {1}'.format(CSeq_JSON, packetappended)
                    packetappended += 1
    # print "packet Added {}".format(packetappended)
    return response_appender(**kwargs)

def response_appender(**kwargs):
    """
        Below method extracts responses of all sip method from json and
        append to datastructure call_stack
        :param kwargs(dict):
        :key local_json_download_file: json converted by PCAP_converter method
        :return:
    """
    # print "Inside response_appender"
    import json
    responseadded=0
    local_json_download = kwargs['local_json_download_file']
    json1_file = open(local_json_download)
    json1_str = json1_file.read()
    json1_data = json.loads(json1_str)
    for key in call_id_ls:
        for i in range(len(json1_data)):
            sip_packet = json1_data[i]['_source']['layers']['sip']
            packet_parser(key="sip.Status-Code", **sip_packet)
            Status_Code = value
            packet_parser(key="sip.Call-ID", **sip_packet)
            Call_ID_JSON = value
            packet_parser(key="sip.CSeq.method", **sip_packet)
            CSeq_JSON = value
            if Status_Code :
                # composite_key=str(Call_ID_JSON) + str(CSeq_JSON)
                if Call_ID_JSON == key:
                    if CSeq_JSON == 'INVITE':
                        call_stack[key][CSeq_JSON]['RESPONSE'].append(sip_packet)
                        responseadded += 1
                        #print 'RESPONSE appended current is {0} {1}'.format(CSeq_JSON, responseadded)
                    elif CSeq_JSON == 'ACK':
                        call_stack[key][CSeq_JSON]['RESPONSE'].append(sip_packet)
                        responseadded += 1
                        #print 'RESPONSE appended current is {0} {1}'.format(CSeq_JSON, responseadded)
                    elif CSeq_JSON == 'UPDATE':
                        call_stack[key][CSeq_JSON]['RESPONSE'].append(sip_packet)
                        responseadded += 1
                        #print 'RESPONSE appended current is {0} {1}'.format(CSeq_JSON, responseadded)

                    elif CSeq_JSON == 'BYE':
                        call_stack[key][CSeq_JSON]['RESPONSE'].append(sip_packet)
                        responseadded += 1
                        #print 'RESPONSE appended current is {0} {1}'.format(CSeq_JSON, responseadded)

                    elif CSeq_JSON == 'OPTIONS':
                        call_stack[key][CSeq_JSON]['RESPONSE'].append(sip_packet)

                        responseadded += 1
                        #print 'RESPONSE appended current is {0} {1}'.format(CSeq_JSON, responseadded)

                    elif CSeq_JSON == 'REGISTER':
                        call_stack[key][CSeq_JSON]['RESPONSE'].append(sip_packet)
                        responseadded += 1
                        #print 'RESPONSE appended current is {0} {1}'.format(CSeq_JSON, responseadded)

                    elif CSeq_JSON == 'CANCEL':
                        call_stack[key][CSeq_JSON]['RESPONSE'].append(sip_packet)
                        responseadded += 1
                        #print 'RESPONSE appended current is {0} {1}'.format(CSeq_JSON, responseadded)

                    elif CSeq_JSON == 'PRACK':
                        call_stack[key][CSeq_JSON]['RESPONSE'].append(sip_packet)
                        responseadded += 1
                        #print 'RESPONSE appended current is {0} {1}'.format(CSeq_JSON, responseadded)

                    elif CSeq_JSON == 'SUBSCRIBE':
                        call_stack[key][CSeq_JSON]['RESPONSE'].append(sip_packet)
                        responseadded += 1
                        #print 'RESPONSE appended current is {0} {1}'.format(CSeq_JSON, responseadded)

                    elif CSeq_JSON == 'NOTIFY':
                        call_stack[key][CSeq_JSON]['RESPONSE'].append(sip_packet)
                        responseadded += 1

                    elif CSeq_JSON == 'PUBLISH':
                        call_stack[key][CSeq_JSON]['RESPONSE'].append(sip_packet)
                        responseadded += 1
                        #print 'RESPONSE appended current is {0} {1}'.format(CSeq_JSON, responseadded)

                    elif CSeq_JSON == 'INFO':
                        call_stack[key][CSeq_JSON]['RESPONSE'].append(sip_packet)
                        responseadded += 1
                        #print 'RESPONSE appended current is {0} {1}'.format(CSeq_JSON, responseadded)

                    elif CSeq_JSON == 'REFER':
                        call_stack[key][CSeq_JSON]['RESPONSE'].append(sip_packet)
                        responseadded += 1
                        #print 'RESPONSE appended current is {0} {1}'.format(CSeq_JSON, responseadded)

                    elif CSeq_JSON == 'MESSAGE':
                        call_stack[key][CSeq_JSON]['RESPONSE'].append(sip_packet)
                        responseadded += 1
                        #print 'RESPONSE appended current is {0} {1}'.format(CSeq_JSON, responseadded)

def sdp_mediaAttr_verifier(key, exval, log, **sdp):
        """
        :param key:
        :param kwargs:
        :return:
        """

        key_new = key.replace('.', '_').replace('-', '_')

        for k, v in dict(sdp).items():
            # log.info("k: {0}".format(k))
            if isinstance(v, dict):
                sdp_mediaAttr_verifier(key_new, exval, log, **v)
            elif isinstance(v, list):
                for d in v:
                    sdp_mediaAttr_verifier(key_new, exval, log, **d)
            else:
                key_json = None
                key_json = k.replace('.', '_').replace('-', '_')
                # log.info("k: {0}    Key_json : {1}, expected_key : {2}".format(k,key_json,key_new))
                if key_json.lower() == str(key_new.lower()):
                    log.info("Key matched {}".format(key_json))
                    if v.lower() == str(exval).lower():
                        # log.info("{0} Expected value found {1}".format(key, v))
                        globals()['value'] = v
                        break
                    else:
                        # log.info("Key :{0} UnExpected value found {1}".format(key_json, v))
                        pass
                else:
                    # log.info("UnExpected Key found {0} ".format(key_json))
                    pass

    # print "Response Added {}".format(responseadded)
def rtp_event_verifier(key, exval,log, **rtpevent):
    """
    :param key:
    :param kwargs:
    :return:
    """
    key_new = key.replace('.', '_').replace('-', '_')

    for k, v in dict(rtpevent).items():
        log.info("k: {0}".format(k))
        if isinstance(v, dict):
            rtp_event_verifier(key_new, exval, **v)
        elif isinstance(v, list):
            for d in v:
                rtp_event_verifier(key_new, exval, **d)
        else:
            key_json = None
            key_json = k.replace('.', '_').replace('-', '_')
            # log.info("k: {0}    Key_json : {1}, expected_key : {2}".format(k,key_json,key_new))
            if key_json.lower() == str(key_new.lower()):
                # log.info("Key matched {}".format(key_json))
                if v.lower() == str(exval).lower():

                    # log.info("{0} Expected value found {1}".format(key, v))
                    globals()['value'] = v
                    break
                else:
                    # log.info("Key :{0} UnExpected value found {1}".format(key_json, v))
                    pass
            else:
                # log.info("UnExpected Key found {0} ".format(key_json))
                pass
def flowDiagram():
    pass




# logger.info("Now iterating for Request verification")

# pprint(call_stack.keys())
# for k, v in call_stack.items():
#     print "Key====",k
#     print "$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$"
#     print "Value===",v
#     print "##################################################\n"
# pprint(subscribePktList)
# Base_Packet_Extracter_Sip(**kwargs)
# from pprint import pprint
# pprint(call_stack)
# def sip_phase_one(**kwargs):
#     """
#     :param kwargs:
#     :return:
#     """
#     import threading
#     ip_addr_src = kwargs['sip_ip_addr_src']
#     ip_addr_dst = kwargs['sip_ip_addr_dst']
#     ip_addr_sip_server=kwargs['sip_ip_addr_dst']
#
#
#     ssh_cmd_dict = {
#         'cmd': """cd /root/pcap_download;rm -rf *.pcap;tcpdump -nqt -s 0 -A \(host {0} and  host {1}\) and port 5060 -w {2}""".format(
#             ip_addr_src,ip_addr_sip_server,pcap_file),
#         'ip_address': '10.112.123.89', 'username': "root", "password": "default"
#         }
#     from pprint import pprint
#     t1 = threading.Thread(target=ssh_cmd, kwargs=ssh_cmd_dict)
#     t1.start()
# def sip_phase_final(**kwargs):
#     pass

# def packet_verifier(**kwargs):
#
#     ip_addr_src = kwargs['sip_ip_addr_src']
#     ip_addr_dst = kwargs['sip_ip_addr_dst']
#     # ip_addrstr = u'10.112.123.196', u"10.112.123.89"
#
#     import threading
#     ssh_cmd_dict = {
#         'cmd': """cd /root/pcap_download;rm -rf *.pcap;tcpdump -nqt -s 0 -A \(host 10.112.123.196 and  host 10.112.123.89\) and port 5060 -w {0}""".format(
#             pcap_file),
#         'ip_address': '10.112.123.89', 'username': "root", "password": "default"
#         }
#     from pprint import pprint
#     t1 = threading.Thread(target=ssh_cmd, kwargs=ssh_cmd_dict)
#     t1.start()
#     #
#     from PhoneComponent import PhoneComponent
#     params_one = {"phoneModel": "Mitel6930", "ipAddress": "10.112.123.196", "extensionNumber": "4165142514",
#                   "phoneName": "Test1", "hq_rsa": "hq.rsa"}
#     params_two = {"phoneModel": "Mitel6920", "ipAddress": "10.112.123.202", "extensionNumber": "4165142515",
#                   "phoneName": "Test2", "hq_rsa": "hq.rsa"}
#
#     pha = PhoneComponent(**params_one)
#     phb = PhoneComponent(**params_two)
#     kwargs = {'phoneObj': phb, 'dialingMode': 'Loudspeaker','answerMode':'Loudspeaker'}
#     pha.makeCall(**kwargs)
#     phb.answerCall(**kwargs)
#
#     phb.disconnectTerminal()
#     import time
#     time.sleep(5)
#     ssh_cmd_dict['cmd'] = "killall tcpdump"
#     print(ssh_cmd_dict)
#     pprint(ssh_cmd(**ssh_cmd_dict))
#     t1.join()
#     print scp_get("""/root/pcap_download/{}""".format(pcap_file))
#     kwargs={'Input_File':pcap_file,"Op_file":op_file}
#     pcap_converter(**kwargs)
#     key=u"sip.from.user"
#     Base_Packet_Extracter()
#     for k,v in call_stack.iteritems():
#         sip_packet_parser(key,**v['INVITE'])
#         if value==u'4165142514':
#             print value
#             print 'pass'
#         else:
#             print 'FAIL'



# packet_verifier()
# for key in call_stack.keys():
#     print key
#     for j in call_stack[key].keys():
#         print j
#         print call_stack[key][j]['PACKET']
#         print j
#         print "RESPONSE"
#         print call_stack[key][j]['RESPONSE']
    # if dict(call_stack['8a0db7cd4cbe4fbe'][i])!=None:
    #     print i
# call_id__invite_extracrter()
# print "Prince"

# print (call_stack['b6f1dab981d2fa8c'][0]['UPDATE']['PACKET'])
# for pac in call_stack['b6f1dab981d2fa8c']:
#     for i in range(13):
#         print pac[i]
#     print 'Ak kks'

# test()b6f1dab981d2fa8c1287255901
# print call_id_ls
# print call_stack
# print call_stack['b6f1dab981d2fa8c1287255901']
# for sub_packet in call_stack['b6f1dab981d2fa8c1287255901']:
#     print len(sub_packet['response'])
# import threading
# ssh_cmd_dict={'cmd':"""cd /root/pcap_download;rm -rf *.pcap;tcpdump -n -s 0 port 5060 or udp portrange 10000-20000 -vvv -w {0}""".format(pcap_file),
#          'ip_address':'10.112.123.89','username':"root","password":"default"
#          }
# from pprint import pprint
# t1 = threading.Thread(target=ssh_cmd,kwargs=ssh_cmd_dict)
# t1.start()
#
#
# from time import sleep
# sleep(30)
# ssh_cmd_dict['cmd']="killall tcpdump"
# print(ssh_cmd_dict)
# pprint(ssh_cmd(**ssh_cmd_dict))
# t1.join()
# print scp_get("""/root/pcap_download/{}""".format(pcap_file))
# kwargs={'Input_File':pcap_file,"Op_file":op_file}
# SIP_packet_extracter(**kwargs)
# from PhoneComponent import PhoneComponent
# params_one= {"phoneModel": "Mitel6865i", "ipAddress": "10.112.123.72", "extensionNumber": "4165142513", "phoneName": "yo1","ssh_password":None}
# params_two= {"phoneModel": "Mitel6867i", "ipAddress": "10.112.123.171", "extensionNumber": "4165142512", "phoneName": "yo2","ssh_password":None}
# # params_three= {"phoneModel": "Mitel6910", "ipAddress": "10.112.123.18", "extensionNumber": "4043", "phoneName": "yo3",
# #            "hq_rsa": "hq_rsa"}
# pha=PhoneComponent(**params_one)
# # phb=PhoneComponent(**params_two)

# kwargs= {
#         'ip_address':u"10.112.123.120",
#         'username':'admin',
#         # 'phone_hq_rsa':'C:/Asterisk_three/hq_rsa'
#         'phone_hq_rsa':'C:/Asterisk_three/Robo_SVN/Framework/phone_wrappers/rsa_keys/hq_rsa'
#                      }
# switchOnWebui(**kwargs)

# kwargs = {'ip_address_server':'10.112.110.111','username':"mxone_admin",'password':'Mxone@456','file':'tls.pcap'}
# scp_get(**kwargs)
# from scapy.all import *
# a = " "
#os.system("tshark  -T fields  -e frame.time -e  data.data -w Eavesdrop_Data.pcap > Eavesdrop_Data.txt -F pcap -c 1000")
#I commented out the t-shark so i could just reuse the same data

# data = "0001_20200225121725.pcap"
# a = rdpcap(data)
# sessions = a.sessions()
# for session in sessions:
#     http_payload = ""
#     for packet in sessions[session]:
#         print packet.show()