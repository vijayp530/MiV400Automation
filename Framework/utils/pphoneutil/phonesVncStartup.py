from subprocess import Popen
import sys
import os
import csv

def print_usage():
	print('''***ERROR*** Incorrect cmd usage. Must pass two args ie. pphoneVncStartup.bat <auto_project> <config_module>''' )

if len(sys.argv) < 3:
	print_usage()
	sys.exit(1)
	
config_project = sys.argv[1]
config_module = sys.argv[2]

WIN_ATF_CONFIG_PATH = os.path.join("C:\\","ATF_ROBOT","run")
OS_CONFIG_PATH = os.path.join(WIN_ATF_CONFIG_PATH,config_project,"configs",config_module,'pphone_st_hq1_userInfo.csv')

fname = OS_CONFIG_PATH 

print("Reading pphone ips from path \"%s\"" % fname)
with open(fname) as f_in:
	lines = (line.rstrip() for line in f_in)
	lines = list(line for line in lines if line)  # Non-blank lines in a list
numPhones = -1
for line in lines:
	numPhones += 1

reader = csv.DictReader(open(fname))
userDict = {}
for row in reader:
	for column, value in row.iteritems():
		userDict.setdefault(column, []).append(value)

for userNum in range(0,3):
	ip = userDict["ip"][userNum]
	cmd = 'pphonevnc.bat ' + ip
	print("Running cmd %s" % cmd)
	os.system(cmd)