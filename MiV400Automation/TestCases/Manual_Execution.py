import os

Commands = [
             "robot -v dut:PhoneA -v pbx:Manual  --listener ..\lib\MyListner.py  Manual_Execution_File.robot",

             ##uncomment below one line if you want to execute only failed test cases of above DUT
             # "robot -v dut:PhoneA -v pbx:Manual  --listener ..\lib\MyListner.py --rerunfailed output.xml Manual_Execution_File.robot",

             ##uncomment below lines if you want to run for different DUT's
             # "robot -v dut:PhoneB -v pbx:Manual  --listener ..\lib\MyListner.py  Manual_Execution_File.robot",
             # "robot -v dut:PhoneB -v pbx:Manual  --listener ..\lib\MyListner.py --rerunfailed output.xml Manual_Execution_File.robot",
             # "robot -v dut:PhoneC -v pbx:Manual  --listener ..\lib\MyListner.py  Manual_Execution_File.robot",
             # "robot -v dut:PhoneC -v pbx:Manual  --listener ..\lib\MyListner.py --rerunfailed output.xml Manual_Execution_File.robot",
             # "robot -v dut:PhoneD -v pbx:Manual  --listener ..\lib\MyListner.py  Manual_Execution_File.robot",
             # "robot -v dut:PhoneD -v pbx:Manual  --listener ..\lib\MyListner.py --rerunfailed output.xml Manual_Execution_File.robot"
            ]

for i in range(2): # increase the range 2 to your desired value
	for key in Commands:
		os.system(key)



