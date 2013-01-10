# 2009 Edited by Ali, www.2d3d.by

# Copyright (c) 2007 The Foundry Visionmongers Ltd.  All Rights Reserved.

# This function is called when the user drag'n'drops or pastes
# anything that looks like a filename on the main window.


proc drop {text} {
  
  puts "\ndrop from: $text"
  foreach f [split $text "\r\n"] {

    set f [string trim $f]

    if {$f=={}} continue
    # strip the Linux 'file:' prefix
    if [string match "file:*" $f] {
      set f [string range $f 5 end]
    }
    # strip Linux '///' to '/'
    if [string match "///*" $f] {
      set f [string range $f 2 end]
    }
    #set f [filename_fix $f]
    if [file isdirectory $f] {
      
      # recursively load folders
      if {![catch {set dirs [glob -directory $f -type d *]} err]} {
        foreach dir $dirs {
           drop $dir
        }
      }
      
      # load all images in this directory
      set ff [filename_list -compress $f]

      # filter compressed list (uncompress files with extensions: mov, avi, ...)
      set ff [filter_compressed_list $f $ff]

      # drop nodes
      foreach t $ff {

        set fullname [file dirname $f/.]/$t
        #set fullname $f/$t
        if ![file isdirectory $fullname] {
          drop_node $fullname
        }
      }
    } else {
      drop_node $f
    }
  }
}




########################################################################################################################
proc filter_compressed_list {dir compressed_list} {

  set file_list {}

  foreach f $compressed_list {
   
    set name_tmp [split_filename $f]
    set name [lindex $name_tmp 0]
    set range [lindex $name_tmp 1]

    # uncompress filenames with extensions avi, mov, chan, ...
    if {[string first % $name] >= 0 && [regexp {.\.((avi)|(mov)|(r3d)|(autosave)|(nk)|(chan)|(3dt)|(2dt)|(txt)|(fbx)|(xml)|(ssf))$} [string tolower $name]]} {

      set first [lindex [split $range "-"] 0]
      set last [lindex [split $range "-"] 1]
      if {$first==""} {set first 0; set last 0}

      for {set i $first} {$i <= $last} {incr i} {
        set file_name [format $name $i]
        if {[file exist $dir/$file_name]} { lappend file_list $file_name }
      }

    } else {
      lappend file_list $f
    }
  }

  return $file_list
}




########################################################################################################################
proc drop_node {f} {

  #set f [string tolower $f]
  set ext [file extension [lindex [split_filename $f] 0]]

  catch {foreach node [selected_nodes] {knob $node.selected 0}}
  
  set ext [string tolower $ext]
  switch $ext {
  
    ".nk" - 
    ".nk3" - 
    ".nk4" - 
    ".nk~" - 
    ".nuke" - 
    ".nuke3" - 
    ".nuke4" - 
    ".autosave" {
      push 0
      source $f
    } 
 
    ".2dt" - 
    ".3dt" {
      push 0
      if {[ImportTrackData $f]} {
        puts " pasting track data file: $f"
      } else {
        puts " ignoring track data file: $f"
      }
    } 
    
    ".ssf" {
      # import Shake Rotoshape
      push 0
      if {[ImportSSF $f]} {
        puts " pasting bezier shape file: $f"
      } else {
        puts " ignoring bezier shape file: $f"
      }
    }
    
    ".chan" {
      push 0
      if [testChan $f] {
        Camera -New
        set newNode [stack 0]
        puts " pasting camera chan file: $f"
      } else {
        push 0
        Axis {}
        set newNode [stack 0]
        puts " pasting axis chan file: $f"
      }
      in $newNode {import_chan_file $f}
    }
    
    ".xml" {
      # import Quantel Corner Pin Data XML file (generated from Mocha)
      push 0
      if {[ImportXML $f]} {
        puts " pasting corner pin data file: $f"
      } else {
        puts " ignoring corner pin data file: $f"
      }
    }
    
    ".txt" {
      # import ascii file (various types)
      if {[ImportTXT $f]} {
        puts " pasting ascii file: $f"
      } else {
        puts " ignoring ascii file: $f"
      }
      
    }
    
    ".obj" {
      push 0
      if [catch {ReadGeo2 -New file $f}] {
        puts " ignoring geo file: $f"
      } else {
        knob [stack 0].read_texture_w_coord 0
        puts " pasting geo file: $f"
      }
    }
    
    ".fbx" {
      push 0
      if {[ImportFBX $f]} {
        puts " pasting fbx scene file: $f"
      } else {
        puts " ignoring fbx scene file: $f"
      }
      
    }
    
    default {
      push 0
      if [catch {Read -New file $f}] {
        puts " ignoring image file: $f"
      } elseif [errCheck [stack 0]] {
        puts " ignoring image file: $f"
      } else {
        puts " pasting image file: $f"
      }
    }
  }
}




############################################################################################
# split filename to list: {{name} {range}}
proc split_filename {f} {
  if {[llength $f]==1} {return $f}

  # remove "(XXXX missing)" warning
  set f_tmp [string range $f 0 [expr [string last "(" $f]-1]]
  if {$f_tmp!=""} {set f $f_tmp}
  
  # remove ",step"
  set f_tmp1 [string range $f 0 [expr [string last "," $f]-1]]
  if {$f_tmp1!=""} {set f $f_tmp1}
  
  # if frame range not exist return {{name} -}
  if {[string last "-" [lindex $f end]]<0} {return [list $f "-"]}
  
  # if frame range exist return {{name} {range}}
  set name [lrange $f 0 end-1]
  set range [lrange $f end-1 end]
  
  return [list $name $range]
}




############################################################################################
proc errCheck {node} {
  
  catch {set pr [knob $node.premultiplied];knob $node.premultiplied [expr !$pr]}
  
  if [expression $node.error] {delete $node; return 1}
  
  catch {knob $node.premultiplied $pr}
  
  return 0

}



############################################################################################
proc testChan {inputfile} {

  if {[catch {set file [open $inputfile RDONLY]} err]} {
    puts "Error $err"
  }
  set chan [read $file]
  close $file
  
  while {[gets $chan line] >= 0} {
    if {[llength $line] < 4} continue
    if {[llength $line] >= 8} {
      return 1
    } elseif {[llength $line] <= 7} {
      return 0
    }
  }
}

