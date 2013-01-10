#
# ImportTrackData 2007-08 demOOn.k@gmail.com
# ver 0.2
#
# Support PfTrackrack and SynthEyes (custom exporters needed)
# Support versons
# Thanx DenizZ
#

proc ImportTrackData {track_file} {
#	set fTrack [open $track_file RDONLY] 
	if {[catch {set fTrack [open $track_file RDONLY]} err]} {
		puts "Error $err"
		return 0
	}
	set data [read $fTrack]
	close $fTrack
	set data [split $data "\n"]
	set last_name {}

	foreach i $data {
#is it name of tracker?
		if [string first \" $i]==0 {
			if [info exists cur_node] {
				knob $cur_node.translate [list $x_values $y_values]
			}
			set x_values "curve"
			set y_values "curve"
			set i [string trim $i "\""]
			set _name [split [file tail $track_file] "."]
			set _name "[lindex $_name 0]_[lindex $_name 1]_[string trimleft $i Tracker]_v"
			for {set j 1} {$j<10000} {incr j} {
				set name ${_name}${j}
				if {![exists $name]} {break}
			}
			push 0
			Position {}
			set cur_node [stack 0]
			# replace space whith "_"
			set name [regsub -all " " $name "_"]
			knob $cur_node.name $name

		}
# is a right string?
		set nums [split $i]
		if {[llength $nums] == 4} {
			set cur_frame [lindex $nums 0]
			set cur_x [lindex $nums 1]
			set cur_y [lindex $nums 2]
			set cur_vis [lindex $nums 3]
			lappend x_values "x$cur_frame" $cur_x
			lappend y_values "x$cur_frame" $cur_y
		}
	}
# Setup for last node
	if [info exists cur_node] {
		knob $cur_node.translate [list $x_values $y_values]
		knob $cur_node.selected true
	}
	return 1
}
