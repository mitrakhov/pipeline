proc tvco {} {	
	global env
	global WIN32
	
	set tempPath ""
	if {$WIN32} {
		set tempPath $env(TEMP)
	} else {
		set tempPath "/tmp"
	}
	
	catch { exec "/usr/pipeline/bin/browser" "-m" "nuke" } result
	#set result [ string range $result 1 end ]
	puts $result
	catch { exec "/usr/pipeline/bin/vco" "/film/sequences/SQ01/shots/sh01/comp/compose/compose.nk" "-v" "1" "-p" "gala_spring" "-V" "-m" "gala_spring,469"  } resultvco
	#catch { exec "/usr/pipeline/bin/vco" $result } resultvco
	puts $resultvco 
		
}