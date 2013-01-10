def MochaImportCornerPin():

  """ Automatically creates cornerpin node using *.txt files from Mocha
      written by Anton Mitrakhov """

  # gets input files
#  import pipe
  start_path = '/mnt/karramba/'
#  asset_obj = None
#  try:
#   asset_obj = pipe.Projects().GetAssetByInfo(nuke.root().name())
#  except:
#  	print "Bla"
#  if asset_obj:
#  	 start_path = asset_obj.GetDataPath() + os.sep + 'tracks' + os.sep
  input = nuke.getFilename("Select Mocha *.txt file to import", "*_Tracker?.txt")
  if input == None: return
  
  # parses input folder
  path = "/".join(input.split("/")[:-1])
  fname =  input.split("/")[-1].split("Tracker")[0]
  mask = fname + "Tracker"
  labelname = fname.rstrip("_")
  tracklist = os.listdir(path)
  
  # makes list of "yours" trackers from input folder
  flist = [path + "/" + x for x in tracklist if x[:len(mask)] == mask]
  flist.sort()
  if len(flist) !=4:
    nuke.message("Not a proper Mocha data")
    return
  
  # creates output tracker node
  cp = nuke.createNode("CornerPin2D") 
  cp.knob("label").setValue(labelname)
  cp.addKnob(nuke.Tab_Knob("RefTab", 'Reference "From" frame'))
  cp.addKnob(nuke.Int_Knob("RefFrame", "ReferenceFrame"))
  cp.addKnob(nuke.PyScript_Knob("sf", "Set to current frame"))
  cp.knob('sf').setCommand("nuke.selectedNode().knob('RefFrame').setValue(nuke.frame())")
  n = 1
  
  # sets values for node knobs
  for file in flist:
    xraw = []
    yraw = []
    tracker = open(file, "r")
    for line in tracker:
      xraw.append(line.split(" ")[0])
      yraw.append(line.split(" ")[1].rstrip("\n"))   
    trackx = "{curve i x"+ str(nuke.animationStart()) +" "+ " ".join(xraw) +"}"
    tracky = "{curve i x"+ str(nuke.animationStart()) +" "+ " ".join(yraw) +"}"
    track = trackx + " " + tracky
    
    cp.knob("to%s"%n).fromScript(track)    
    cp.knob("from%s"%n).fromScript("{to%s(RefFrame)} {to%s(RefFrame)}"%(n,n))

    n+=1
  
  

    
