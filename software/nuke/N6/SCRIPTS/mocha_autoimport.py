def MochaImport():

  """ Automatically creates tracker node using *.txt files from Mocha
      written by Anton Mitrakhov """

  # gets input files
#  import pipe
#  asset_obj = None
#  start_path = '/mnt/karramba/'
#  try:
#  	asset_obj = pipe.Projects().GetAssetByInfo(nuke.root().name())
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
  tk = nuke.createNode("Tracker3")
  tk.knob("transform").setValue("match-move")
  tk.knob("label").setValue(labelname)
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
    tk.knob("track%s"%n).fromScript(track)
    tk.knob("enable%s"%n).setValue(True)
    tk.knob("use_for%s"%n).setValue("T R")

    n+=1
  
  

    
