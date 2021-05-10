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

set uname_index  [lsearch $fd "HQ1_UNAME"]
set uname [lindex $fd [expr $uname_index + 2]]

set pass_index  [lsearch $fd "HQ1_PASSWORD"]
set pass [lindex $fd [expr $pass_index + 2]]

#Read command args
set first_name 		[lindex $argv 1]
set workgroupName 	[lindex $argv 2]
set agentState 		[lindex $argv 3]
 
 #Initialize and run D2 command
set d2_h [::dcal::D2WebAPITool #auto]
$d2_h initialize -server $server -username $uname -password $pass

$d2_h command "workGroup" -mode "modify" -name $workgroupName -members_Selection $first_name -members_SetAgentState $agentState
