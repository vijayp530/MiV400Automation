source [file join [file dirname [info script]] d2_common.tcl]

#Read testbed config values into vars
set MODULE_CONFIG_DIR 	[lindex $argv 0]
set configDir  "c:\\ATF_ROBOT\\run\\${MODULE_CONFIG_DIR}\\"
set configPath  "${configDir}\\testbed.cfg"
set fp [open $configPath r]
set fd [read $fp]
close $fp

set server_index  [lsearch $fd "HQ1_IPADDRESS"]
set server [lindex $fd [expr $server_index + 2]]
# puts $server_index
# puts $server

set uname_index  [lsearch $fd "\${testbed_username}"]
set uname [lindex $fd [expr $uname_index + 1]]

set pass_index  [lsearch $fd "\${testbed_password}"]
set pass [lindex $fd [expr $pass_index + 1]]

#Read command args
set first_name 		[lindex $argv 1]
set huntgroupName 	[lindex $argv 2]
set action 			[lindex $argv 3]

#Initialize and run D2 command 
set d2_h [::dcal::D2WebAPITool #auto]
$d2_h initialize -server $server -username $uname -password $pass

set action [string tolower $action]
array set fields {
	add     members_Add
	remove  members_Remove
}
set action $fields($action)

##
# This function modifies the hunt group membership
#
# @param server Specify the server IP
# @param first_name specify the hunt group user 
# @param huntgroupName Specify the huntgroup user
# @param action Specify the action to be taken
#

# $d2_h command "huntgroup" -mode "Modify" -name "gApp_HuntGroup" -extension 5556 -members_Selection "4001" -members_Add true
$d2_h command "huntgroup"  -mode "Modify" -name $huntgroupName -members_Selection $first_name -$action true
