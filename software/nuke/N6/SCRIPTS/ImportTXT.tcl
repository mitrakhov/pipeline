# Import Nuke ASCII format

proc ImportTXT {txt_file} {
	if {[catch {set file [open $txt_file RDONLY]} err]} {
		puts "Error $err"
		return 0
	}
	set data [read $file]
	close $file
	set data [split $data "\n"]
	
	# Cleanup data
	set tmp_data {}
	foreach line $data {if {$line!=""} {lappend tmp_data $line}}
	set data $tmp_data
	
	# Check if the first column is a frames column
	set framesExists [isFramesColumnExists $data]
	# Get a number of columns
	set columns [expr [numColumns $data]-$framesExists]
	
	switch $columns {
		"1" {
			# Create Position node for situation when x and y are placed on different files 
			set pos_node [stack 0]
			set xy [string index [file tail $txt_file] end-4]
			if {$xy=="x"} {set yx "y"} else {set yx "x"}

			if {![exists $pos_node] || [class $pos_node]!="Position" || [expression $pos_node.translate.$xy.animated]} {
				push 0
				Position -New
				set pos_node [stack 0]
				knob $pos_node.label [file tail $txt_file]
			} else {
				knob $pos_node.label "[knob $pos_node.label]\n[file tail $txt_file]"
			}
			
			set frame [knob root.first_frame]
			foreach line $data {
				if {$framesExists} {set _frame [lindex $line 0]} else {set _frame $frame}
				setkey $pos_node.translate.$xy $_frame [lindex $line [expr $framesExists]]
				incr frame
			}
		}
		
		"2" {
			# Create Position node
			push 0
			Position -New
			set pos_node [stack 0]
			
			set frame [knob root.first_frame]
			foreach line $data {
				if {$framesExists} {set _frame [lindex $line 0]} else {set _frame $frame}
				setkey $pos_node.translate.x $_frame [lindex $line [expr $framesExists]]
				setkey $pos_node.translate.y $_frame [lindex $line [expr 1+$framesExists]]
				incr frame
			}
			knob $pos_node.label [file tail $txt_file]
		}
		
		"3" {
			# Create Axis node
			push 0
			Axis -New
			set axis_node [stack 0]
			
			set frame [knob root.first_frame]
			foreach line $data {
				if {$framesExists} {set _frame [lindex $line 0]} else {set _frame $frame}
				setkey $axis_node.translate.x $_frame [lindex $line [expr $framesExists]]
				setkey $axis_node.translate.y $_frame [lindex $line [expr 1+$framesExists]]
				setkey $axis_node.translate.z $_frame [lindex $line [expr 2+$framesExists]]
				incr frame
			}
			knob $axis_node.label [file tail $txt_file]
		}
	}
	return 1
}




# Is the first column is a frames column?
proc isFramesColumnExists {data} {
	set first 1
	set old_value 0
	foreach line $data {
		if {!$first} {
			if {[lindex $line 0] - $old_value != 1} {return 0}
		}
		set first 0
		set old_value [lindex $line 0]
		if {$old_value - int($old_value ) != 0} {return 0}
	}
	
	return 1
}




# How many columns? 
proc numColumns {data} {
	set line [lindex $data 0]
	return [llength $line]
}