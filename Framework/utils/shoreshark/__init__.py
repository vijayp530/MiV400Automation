import psutil
import sys
import re
import json
import subprocess
import time
from sys import platform as _platform
import fileinput

from robot.api import logger


WIN_TSHARK_PATH = 'C:\\Program Files\\Wireshark\\'
MAC_TSHARK_PATH = 'populate me'
LINUX_TSHARK_PATH = 'populate me'

sys.path.append(WIN_TSHARK_PATH)

  
class shoreshark(object):
    ROBOT_LIBRARY_SCOPE = 'GLOBAL'

    # ROBOT_LIBRARY_VERSION = VERSION

    def __init__(self):

        if _platform == "linux" or _platform == "linux2":
            # linux
            TSHARK_PATH = LINUX_TSHARK_PATH
        elif _platform == "darwin":
            TSHARK_PATH = MAC_TSHARK_PATH
            # OS X
        elif _platform == "win32":
            # Windows...
            TSHARK_PATH = WIN_TSHARK_PATH

        self.tshark_path = TSHARK_PATH
        #default to interface 1
        self.interface = 1
        self.post_dict = []

        
    def tshark_start_capture(self, cap_filter, outfile):
        logger.info("Preparing to start pkt capture with filter \"%s\" at file %s" % (cap_filter, outfile))
         
        subprocess.Popen(["python", "tshark_start.py", cap_filter , outfile])
        time.sleep(5)

    def tshark_stop_capture(self):
        ps_tsharkwin = "tshark.exe"
        ps_tshark = "tshark"

        time.sleep(2)
        for proc in psutil.process_iter():
            # check whether the process name matches
            if proc.name() == ps_tsharkwin:
                proc.kill()
            if proc.name() == ps_tshark:
                proc.kill()

    def tshark_filter_http_post(self, infile, dst_ip):
        read_filter = " -R \"ip.dst== "+ dst_ip + " && http.request.method == POST\" "
        cap_infile = " -nr " + infile + " "
        only_show = " -O http "
        format_of_output = " -T fields "
        field_to_print(= " -e text ")
        output_redirect = " > gsuite_cap.txt "
        
        # if has_two_pass_analysis is "true":
        two_pass = " -2 "

        tshark_cmd = "tshark " + read_filter + two_pass
        tshark_cmd = tshark_cmd  + cap_infile + only_show
        tshark_cmd = tshark_cmd  + format_of_output + field_to_print(+ output_redirect)
         
        print("filtering cas pkt capture with cmd: \"%s\"" % tshark_cmd)
    
        subprocess.check_call(tshark_cmd, shell="True")
        self.clean_pkt_output()
        
        
    def clean_pkt_output(self):
        for line in fileinput.input(r'gsuite_cap.txt', inplace = True):
            match = re.search(r'\{(.*?)\}',line).group(1)
            print("{" + match + "}")
        f = open("gsuite_cap.txt","r")
        lines = f.readlines()
        f.close()
        f = open("cap_tmp.txt",'w')
        for line in lines:
            if "make-call" in line:
                f.write(line)
        f.close()
        with open('cap_tmp.txt', 'r') as handle:
            json_data = [json.loads(line) for line in handle]
            logger.warn(json_data)
        self.post_dict  = json_data
        logger.warn(self.post_dict)


    def print_post_dict(self):
        print(self.post_dict)


    def clear_post_dict(self):
        self.post_dict = []

    def tshark_verify_cas_make_call_to_number(self, num):
         dict_len = len(self.post_dict)
         match = 0
         for i in range (0,dict_len):
             # logger.warn("dict  %s" % self.post_dict[i])
             # logger.warn("dict  %s" % self.post_dict[i]['dest'])
             if self.post_dict[i]["dest"] == num:
                 print("Match in dict array index %s val: %s" % (i, self.post_dict[i]["dest"]))
                 match = 1
                 break
         if match == 0:
             raise Exception("Num %s was not found in dict %s" % (num, self.post_dict))

    def tshark_verify_cas_make_no_call(self):
        dict_len = len(self.post_dict)
        if dict_len == 0:
            print("No number was dialed.")


    def decrypt_cas_packets(self, read_filter,has_two_pass_analysis):
        # TODO remove hard coded values
        read_filter = " -R \"ip.dst==10.23.197.249 && tcp.port==5448\" "
        premaster = " -o ssl.keylog_file:C:\ATF_ROBOT\premaster.txt "
        cap_infile = " -nr gsuite.pcap "
        decode_as = " -d tcp.port==" + self.decode_port + ",ssl "
        only_show = " -O http "
        format_of_output = " -T fields "
        field_to_print(= " -e text ")
        output_redirect = " > gsuite_cap.txt "
        
        # if has_two_pass_analysis is "true":
        two_pass = " -2 "

        tshark_cmd = "tshark " + read_filter + premaster + two_pass
        tshark_cmd = tshark_cmd  + cap_infile + decode_as + only_show
        tshark_cmd = tshark_cmd  + format_of_output + field_to_print(+ output_redirect)
         
        print("Decrypting cas pkt capture with cmd: \"%s\"" % tshark_cmd)
    
        subprocess.call(tshark_cmd, shell="True")
        
        # print(result      )
        
        