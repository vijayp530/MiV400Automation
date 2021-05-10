import os
import sys
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("project", help="gsuite, tww, or boss")
parser.add_argument("run_module", help="config module")
parser.add_argument("st_or_mt", help="ST or MT run")
args = parser.parse_args()

project = args.project
run_module = args.run_module
OS_CONFIG_PATH = os.path.join("C:\\", "ATF_ROBOT", "run",project, "configs", run_module)

#check mt or st
testbed_filename = 'testbed.cfg'
if 'mt' in args.st_or_mt:
    testbed_filename = "mt_" + testbed_filename

folder_path = os.path.dirname(os.path.abspath(__file__))

infile = os.path.join(folder_path,'template__init__.py')
outfile = os.path.join(folder_path,'__init__.py')

filename = os.path.join(OS_CONFIG_PATH, testbed_filename)

print("Loading testbed configuration from config file %s " % filename)

testbedDict = {}
numItems = 0
tb_args = ""
factory_args = ""
factory_start = "testbed_factory = BuiltIn().create_dictionary("
factory_end = ")"

with open(filename, 'r') as f:
	for line in f:
		line = line.rstrip() #removes trailing whitespace and '\n' chars

		if "=" not in line: continue #skips blanks and comments w/o =
		if line.startswith("#"): continue #skips comments which contain =

		numItems = numItems+1
		k, v = line.split("=", 1)
		# logger.warn("num %s numItems:: col %s     val %s" % (numItems,k,v))
		#testbedDict[k.strip()] = v.strip()
		k = k.rstrip()
		factory_args = factory_args + k + ","
		
		bla = "    Log    ${testbed01." + k + "}    WARN"
		tb_args = tb_args + k + " = '" + k + "=%s' % testbedDict[\"" + k + "\"]\n            "   
		print(bla)
		# testbed_name = 'testbed_name=%s' % testbedDict["testbed_name"]
        # COMPLETE_IMAGE_LIST = 'COMPLETE_IMAGE_LIST=%s' % testbedDict["COMPLETE_IMAGE_LIST"]
		
factory_args = factory_args.rstrip(",")
factory = factory_start + factory_args + factory_end

# Read in the file
with open(infile, 'r') as file :
  filedata = file.read()

# Replace the target string
filedata = filedata.replace('#TEMPLATE_REPLACE1', tb_args)
filedata = filedata.replace('#TEMPLATE_REPLACE2', factory)

# Write the file out again
with open(outfile, 'w') as file:
  file.write(filedata)
  print("Writing file %s complete!"%outfile)
  