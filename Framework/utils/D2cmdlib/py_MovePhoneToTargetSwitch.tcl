source [file join [file dirname [info script]] d2_common.tcl]

#Read testbed config values into vars
set MODULE_CONFIG_DIR 	[lindex $argv 0]
set phoneIP 	[lindex $argv 1]
set targetSite 	[lindex $argv 2]
set configDir  "c:\\ATF_ROBOT\\run\\GSuite\\configs\\${MODULE_CONFIG_DIR}"
append configPath  ${configDir} {\testbed.cfg}
set fp [open $configPath r]
set fd [read $fp]
close $fp

set server_index  [lsearch $fd "HQ1_IPADDRESS"]
set server [lindex $fd [expr $server_index + 2]]

set uname_index  [lsearch $fd "HQ1_UNAME"]
set uname [lindex $fd [expr $uname_index + 2]]

set pass_index  [lsearch $fd "HQ1_PASSWORD"]
set pass [lindex $fd [expr $pass_index + 2]]

#Initialize and run D2 command  
set myTool [::dcal::D2WebAPITool #auto]
$myTool initialize -server $server -username $uname -password $pass

set site	[lindex $argv 1]
$myTool command "telephone" -mode "Modify" -ipAddress ${phoneIP} -targetSwitch ${targetSite}