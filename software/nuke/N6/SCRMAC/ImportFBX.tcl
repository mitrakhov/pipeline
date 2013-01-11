# ImportFBX v1.2
# 2009 Ali, www.2d3d.by
# Import FBX scene with (nodes and connections)

#################################################################################################################
# ImportFBX proc
#################################################################################################################
proc ImportFBX {fbx_file} {
	set fbx_ver 1
	set all_new_nodes {}
	
	if {[catch {set fbx [open $fbx_file RDONLY]} err]} {
		puts "Error $err"
		return 0
	}
	set data [read $fbx]
	close $fbx
	set data [split $data "\n"]
	
####### Start Parsing Section ####################################################################################

	## Parse Objects Section ####################################################################################
	set begin 0
	set objects {}
	foreach line $data {
		if {[string first "Objects:" $line]==0} {set begin 1; continue}

		if {[string first "    Model:" $line]==0} {
			set tmp_line [string range $line 11 end-1]
			set tmp_line [regsub -all "\"" $tmp_line ""]
			set tmp_line [regsub -all "Model::" $tmp_line ""]
			set tmp_line [regsub -all " " $tmp_line ""]
			
			set tmp_line [split $tmp_line ","]
			lappend objects $tmp_line
		}
		if {$begin==1 && [string first "\}" $line]==0} {set begin 0; break}
	}
	#puts $objects

	
	## Parse Connections Section ################################################################################
	set begin 0
	set connections {}
	foreach line $data {
		if {[string first "Connections:" $line]==0} {set begin 1; continue}

		if {[string first "    Connect:" $line]==0} {
			set tmp_line [string range $line 13 end-1]
			set tmp_line [regsub -all "\"" $tmp_line ""]
			set tmp_line [regsub -all "Model::" $tmp_line ""]
			
			# Filter unknown nodes
			if {[string first ":" $tmp_line]<0} {
			
				set tmp_line [regsub -all " " $tmp_line ""]
				set tmp_line [split $tmp_line ","]
				set tmp_line [lrange $tmp_line 1 end]
			
				lappend connections $tmp_line
			}
		}
		if {$begin==1 && [string first "\}" $line]==0} {set begin 0; break}
	}
	#puts $connections
	
	
	## Parse Takes Section ######################################################################################
	set begin 0
	set takes {}
	foreach line $data {
		if {[string first "Takes:" $line]==0} {set begin 1; continue}

		if {[string first "    Take:" $line]==0} {
			set tmp_line [string range $line 10 end-1]
			set tmp_line [regsub -all "\"" $tmp_line ""]
			set tmp_line [regsub -all " " $tmp_line ""]
			if {$tmp_line==""} {set tmp_line "Default"}
			lappend takes $tmp_line
		}
		if {$begin==1 && [string first "\}" $line]==0} {set begin 0; break}
	}
	if {[lindex $takes 0]!="Default"} {set takes [linsert $takes 0 "Default"]}
	#puts $takes
	
	
####### End Parsing Section #####################################################################################

	## Collect Objects Lists ####################################################################################
	set nulls_list {}
	set meshes_list {}
	set cameras_list {"Producer Perspective" "Producer Top" "Producer Bottom" "Producer Front" "Producer Back" "Producer Right" "Producer Left"}
	set lights_list {}
	foreach obj $objects {
		switch -glob -- [lindex $obj 1] {
			
			"Mesh" {lappend meshes_list [lindex $obj 0]}
			
			"Camera" {lappend cameras_list [lindex $obj 0]}
			
			"Light" {lappend lights_list [lindex $obj 0]}
		}
		if {[lindex $obj 1] == "Mesh" || [lindex $obj 1] == "Null" } {lappend nulls_list [lindex $obj 0]}
	}

	## Set Version ##############################################################################################
	set fbx_ver [get_fbx_ver $objects $fbx_file $fbx_ver]
	
	## Create Nodes #############################################################################################
	set cur_take_id 1
	if {[llength $takes]==0} {set cur_take_id 0}
	
	foreach obj $objects {
		push 0
		catch {foreach node [selected_nodes] {knob $node.selected 0}}
		
		set name "[lindex $obj 0]_v$fbx_ver"
		
		switch -glob -- [lindex $obj 1] {
			"Null" {
				set cur_node_id [lsearch $nulls_list [lindex $obj 0]]
				
				Axis2 -New \
				name $name \
				file $fbx_file \
				read_from_file 1 \
				fbx_take_name "{$cur_take_id} $takes" \
				fbx_node_name "{$cur_node_id} $nulls_list" \
				name $name \
				
				set node [stack 0]
				lappend all_new_nodes $node
			}
			
			"Mesh" {
				set cur_node_id [lsearch $nulls_list [lindex $obj 0]]
				
				Axis2 -New \
				name $name \
				file $fbx_file \
				read_from_file 1 \
				fbx_take_name "{$cur_take_id} $takes" \
				fbx_node_name "{$cur_node_id} $nulls_list" \
				disable 1 \
				
				set node [stack 0]
				lappend all_new_nodes $node
			}
			
			"Camera" {
				set cur_node_id [lsearch $cameras_list [lindex $obj 0]]
				
				Camera2 -New \
				name $name \
				file $fbx_file \
				read_from_file 1 \
				fbx_take_name "{$cur_take_id} $takes" \
				fbx_node_name "{$cur_node_id} $cameras_list" \
				
				set node [stack 0]
				lappend all_new_nodes $node
			}
			
			"Light" {
				set cur_node_id [lsearch $lights_list [lindex $obj 0]]
				
				Light2 -New \
				name $name \
				file $fbx_file \
				read_from_file 1 \
				fbx_take_name "{$cur_take_id} $takes" \
				fbx_node_name "{$cur_node_id} $lights_list" \
				
				set node [stack 0]
				lappend all_new_nodes $node
			}
		}
	}
	
	
	## Connect Nodes ############################################################################################
	set scene_input 0
	foreach connect $connections {
		set name0 "0"
		set name1 "0"
		catch {foreach node [selected_nodes] {knob $node.selected 0}}
		
		if {[lindex $connect 0]!="Scene"} {set name0 "[lindex $connect 0]_v$fbx_ver"}
		if {[lindex $connect 1]!="Scene"} {set name1 "[lindex $connect 1]_v$fbx_ver"}

		# Create and Connect Geometry
		if {[knob $name0.disable]} {
			push 0
			set cur_node_id [lsearch $meshes_list [lindex $connect 0]]
			
			## Start Building of ReadGeo Group ##################################################################
			Group {
				addUserKnob {20 ReadGeo}
				addUserKnob {6 read_from_file l "read from file" -STARTLINE}
				read_from_file 1
				addUserKnob {41 file T ReadGeo1.file}
				addUserKnob {22 reload -STARTLINE T "nuke.toNode(\"this.ReadGeo1\").knob(\"reload\").execute()\n"}
				addUserKnob {41 fbx_take_name l "take name" T ReadGeo1.fbx_take_name}
				addUserKnob {41 fbx_node_name l "node name" T ReadGeo1.fbx_node_name}
				addUserKnob {41 frame_rate l "frame rate" T ReadGeo1.frame_rate}
				addUserKnob {41 use_frame_rate l "use frame rate" -STARTLINE T ReadGeo1.use_frame_rate}
				addUserKnob {41 all_objects l "all objects" T ReadGeo1.all_objects}
				addUserKnob {41 read_on_each_frame l "read on each frame" -STARTLINE T ReadGeo1.read_on_each_frame}
				addUserKnob {26 ""}
				addUserKnob {41 display T ReadGeo1.display}
				addUserKnob {41 selectable -STARTLINE T ReadGeo1.selectable}
				addUserKnob {41 render_mode l render T ReadGeo1.render_mode}
				addUserKnob {26 ""}
				addUserKnob {41 transform T ReadGeo1.transform}
				addUserKnob {41 import_chan l "import chan file" T ReadGeo1.import_chan}
				addUserKnob {41 export_chan l "export chan file" -STARTLINE T ReadGeo1.export_chan}
				addUserKnob {41 xform_order l "transform order" T ReadGeo1.xform_order}
				addUserKnob {41 rot_order l "rotation order" T ReadGeo1.rot_order}
				addUserKnob {41 translate T ReadGeo1.translate}
				addUserKnob {41 rotate T ReadGeo1.rotate}
				addUserKnob {41 scaling l scale T ReadGeo1.scaling}
				addUserKnob {41 uniform_scale l "uniform scale" T ReadGeo1.uniform_scale}
				addUserKnob {41 pivot T ReadGeo1.pivot}
			}
			Input {
				inputs 0
				name look
				number 1
			}
			set N1eba27d0 [stack 0]
			Input {
				inputs 0
				name axis
			}
			set N1eba96d0 [stack 0]
			push $N1eba27d0
			push $N1eba96d0
			Input {
				inputs 0
				name img
				number 2
			}
			ReadGeo2 {
				read_from_file {{parent.read_from_file i}}
				read_texture_w_coord false
				name ReadGeo1
				selected false
			}
			TransformGeo {
				inputs 3
				selectable false
				transform_normals true
				name xform
			}
			Output {
				name Output1
			}
			end_group
			## End Building of ReadGeo Group ##################################################################
			
			set geo_node [stack 0]
			knob $geo_node.name "_[lindex $connect 0]_v$fbx_ver"
			knob $geo_node.file $fbx_file
			knob $geo_node.fbx_take_name "{$cur_take_id} $takes"
			knob $geo_node.fbx_node_name "{$cur_node_id} $meshes_list"
			
			input $geo_node 0 $name1
			lappend all_new_nodes $geo_node
			knob $geo_node.selected 0
		}
		
		if {$name1!="0" && [knob $name1.disable]} {knob $name1.disable 0}
		input $name0 0 $name1
	}
	
	catch {foreach node [selected_nodes] {knob $node.selected 0}}
	
	## Delete unused Axis nodes
	set tmp {}
	foreach node $all_new_nodes {
		if {[class $node] == "Axis2" && [value $node.disable]} {knob $node.selected 1} else {lappend tmp $node}
	}
	catch {node_delete}
	set all_new_nodes $tmp
	
	## Select All Created Nodes ################################################################################
	foreach node $all_new_nodes {knob $node.selected 1}

	## Layout All Selected Nodes ################################################################################
	if [catch {eval [concat autoplace [selected_nodes]]}] {return 0}
	
	return 1
}

#################################################################################################################
# Set New Version proc
#################################################################################################################
proc get_fbx_ver {objects fbx_file fbx_ver} {
	
	foreach obj $objects {
		set name "[lindex $obj 0]_v$fbx_ver"
		set _name "_[lindex $obj 0]_v$fbx_ver"
		if {[exists $name] || [exists $_name]} {
			incr fbx_ver
			get_fbx_ver $objects $fbx_file $fbx_ver
		}
	}
	return $fbx_ver
}