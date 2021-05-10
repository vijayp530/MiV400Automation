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
set ext 	[lindex $argv 1]
set workgroupName 	[lindex $argv 2]
set bool 	[lindex $argv 3]

#Initialize and run D2 command
set d2_h [::dcal::D2WebAPITool #auto]
$d2_h initialize -server $server -username $uname -password $pass

if {$bool == "true"} {
    $d2_h command "workgroup" -mode "modify" -name $workgroupName -members_Selection $ext -members_Add
    # ModifyWorkGroupAgentState $phone "logged out"
} else {
    $d2_h command "workgroup" -mode "modify" -name $workgroupName -members_Selection $ext -members_Remove
}
         