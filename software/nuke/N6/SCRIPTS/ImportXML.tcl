# Import Quantel CornerPin Data XML File (generated from Mocha)

proc ImportXML {xml_file} {
	if {[catch {set file [open $xml_file RDONLY]} err]} {
		puts "Error $err"
		return 0
	}
	set data [read $file]
	close $file
	set data [split $data "\n"]
	
	if {[lindex $data 0]!="<CornerPinInfoDoc>"} {return 0}
	
	
	# Parse XML file
	set tmp_data {}
	set xform_data {}
	set is_FrameNumber 0
	set is_bottomleftx 0
	set is_bottomlefty 0
	set is_bottomrightx 0
	set is_bottomrighty 0
	set is_topleftx 0
	set is_toplefty 0
	set is_toprightx 0
	set is_toprighty 0
	
	foreach line $data {
		if {[string first "<FrameNumber>" $line]>=0 && !$is_FrameNumber} {set is_FrameNumber 1; continue}
		if {[string first "<bottomleftx>" $line]>=0 && !$is_bottomleftx} {set is_bottomleftx 1; continue}
		if {[string first "<bottomlefty>" $line]>=0 && !$is_bottomlefty} {set is_bottomlefty 1; continue}
		if {[string first "<bottomrightx>" $line]>=0 && !$is_bottomrightx} {set is_bottomrightx 1; continue}
		if {[string first "<bottomrighty>" $line]>=0 && !$is_bottomrighty} {set is_bottomrighty 1; continue}
		if {[string first "<topleftx>" $line]>=0 && !$is_topleftx} {set is_topleftx 1; continue}
		if {[string first "<toplefty>" $line]>=0 && !$is_toplefty} {set is_toplefty 1; continue}
		if {[string first "<toprightx>" $line]>=0 && !$is_toprightx} {set is_toprightx 1; continue}
		if {[string first "<toprighty>" $line]>=0 && !$is_toprighty} {set is_toprighty 1; continue}
		
		if {$is_FrameNumber} {lappend tmp_data [expr [lindex $line end]+1]; set is_FrameNumber 0; continue}
		if {$is_bottomleftx} {lappend tmp_data [lindex $line end]; set is_bottomleftx 0; continue}
		if {$is_bottomlefty} {lappend tmp_data [lindex $line end]; set is_bottomlefty 0; continue}
		if {$is_bottomrightx} {lappend tmp_data [lindex $line end]; set is_bottomrightx 0; continue}
		if {$is_bottomrighty} {lappend tmp_data [lindex $line end]; set is_bottomrighty 0; continue}
		if {$is_topleftx} {lappend tmp_data [lindex $line end]; set is_topleftx 0; continue}
		if {$is_toplefty} {lappend tmp_data [lindex $line end]; set is_toplefty 0; continue}
		if {$is_toprightx} {lappend tmp_data [lindex $line end]; set is_toprightx 0; continue}
		if {$is_toprighty} {lappend tmp_data [lindex $line end]; set is_toprighty 0; lappend xform_data $tmp_data; set tmp_data {}}
	}
	
	
	# Create Corner Pin node
	CornerPin2D -New
	set cornerpin [stack 0]
	
	# Create Animation
	foreach line $xform_data {
		setkey $cornerpin.to1.x [lindex $line 0] [expr [value $cornerpin.width]*[lindex $line 1]]
		setkey $cornerpin.to1.y [lindex $line 0] [expr [value $cornerpin.height]*[lindex $line 2]]
		setkey $cornerpin.to2.x [lindex $line 0] [expr [value $cornerpin.width]*[lindex $line 3]]
		setkey $cornerpin.to2.y [lindex $line 0] [expr [value $cornerpin.height]*[lindex $line 4]]
		setkey $cornerpin.to3.x [lindex $line 0] [expr [value $cornerpin.width]*[lindex $line 7]]
		setkey $cornerpin.to3.y [lindex $line 0] [expr [value $cornerpin.height]*[lindex $line 8]]
		setkey $cornerpin.to4.x [lindex $line 0] [expr [value $cornerpin.width]*[lindex $line 5]]
		setkey $cornerpin.to4.y [lindex $line 0] [expr [value $cornerpin.height]*[lindex $line 6]]
	}
	knob $cornerpin.label [file tail $xml_file]
	
	return 1
}