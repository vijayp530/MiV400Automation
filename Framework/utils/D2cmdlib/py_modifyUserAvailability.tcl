source [file join [file dirname [info script]] d2_common.tcl]

#Read testbed config values into vars
set RUN_MODULE 	[lindex $argv 0]
set configDir  "c:\\ATF_ROBOT\\run\\GSuite\\configs\\${RUN_MODULE}\\"
set configPath  "${configDir}testbedConfig.robot"
set fp  [open $configPath r]
set fd [read $fp]

set uname_index  [lsearch $fd "\${testbed_username}"]
set uname [lindex $fd [expr $uname_index + 1]]

set pass_index  [lsearch $fd "\${testbed_password}"]
set pass [lindex $fd [expr $pass_index + 1]]

#Read command args
set server 	[lindex $argv 0]
set first_name 	[lindex $argv 1]
set option 	[lindex $argv 2]

#Initialize and run D2 command
set d2_h [::dcal::D2WebAPITool #auto]
$d2_h initialize -server $server -username $uname -password $pass

set l_option [string tolower $option]
array set states {"available" "Available" "in_a_meeting" "In A Meeting" "out_of_office" "Out Of Office" "do_not_disturb" "Do Not Disturb" "vacation" "Vacation" "custom" "Custom"}
set option $states($l_option)
puts "Server: $server"
puts "name: $first_name"
puts "L Option: $l_option"
puts "Option: $option"

$d2_h command "user" -mode "modify" -firstName "${first_name}" -currentCallHandlingMode "${option}"