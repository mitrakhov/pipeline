def AutoProxy():    
    input=nuke.selectedNodes("Read")
    n=0
    for node in input:

      
      #creates output path
      path=node.knob ("file").getValue()
      npicture=path.split("/")[-1].rsplit(".", 1)[0]+".jpg"
      ppath="/".join(path.split("/")[0:-1])+"/proxy"
      if not os.path.exists(ppath):
        os.mkdir(ppath)
      outpath=ppath+"/"+npicture
      
      #creates render range
      outfirst=node.knob ("first").getValue()
      outlast=node.knob ("last").getValue()
      
      #creates write output
      output=nuke.createNode ("Write")
      nname=output.knob ("name")
      oname="Write"+"_"+str(n)
      nname.setValue (oname)
      opath=output.knob ("file")
      opath.setValue (outpath)
      output.setInput (0, node) 
      quality=output.knob ("_jpeg_quality")
      quality.setValue(1)
      nuke.render (oname, start=int(outfirst), end=int(outlast), incr=1)
      n+=1
