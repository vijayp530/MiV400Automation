#User todo - Must create env variable "set VTFHOME C:\HCLT\ vtftestpkg\vtf\"
set ::env(VTFHOME) [file join C:/ HCLT vtftestpkg vtf]
set vtfhome [file join C:/ HCLT vtftestpkg vtf]

lappend auto_path [file join $vtfhome shoretel-test DCAL]
lappend auto_path [file join $vtfhome shoretel-test DCAL d2webapi]

package require Itcl 3.3
source ${vtfhome}/shoretel-test/DCAL/src/pkg.itcl
package require dcal 1.0
package require dcald2webapi 1.0