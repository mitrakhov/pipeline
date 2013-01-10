from cexceptions import *


class ReloadRendersPanel( nukescripts.PythonPanel ):
    def __init__( self, node_read, renders_vers ):
		nukescripts.PythonPanel.__init__( self, 'Reload Renders', 'tfx.ReloadRenders')
		# CREATE KNOBS
		self.nodesChoice = nuke.Enumeration_Knob( 'renders', 'Source render versions', renders_vers[2])
		self.node = node_read
		self.s_dir = renders_vers[0]
		self.e_dir = renders_vers[1]
		# ADD KNOBS
		self.addKnob( self.nodesChoice )
       
    def knobChanged( self, knob ):
        dir_files = self.s_dir+os.sep+knob.value()+os.sep+self.e_dir
        files = os.listdir(dir_files)
        files.sort()
        start_file = files[0].split('.')
        name_file = dir_files + os.sep + start_file[0]
        start = int(start_file[1])
        end = int(files[-1].split('.')[1])
        label = "%s.%%0%sd.%s %s-%s"%(name_file, len(start_file[1]), start_file[2], start,end)
        self.node.knob('file').fromUserText(label)

def fillReads():
	read_node = nuke.selectedNode()
	if not read_node.Class() == 'Read': raise Exception('Must select a read node!')
	import sys,os,popen2
	sys.path.append('/usr/pipeline/lib')
	from nukescripts import pyQtAppUtils, utils
	import filesys
	import pipe
	reload(filesys)
	reload(pipe)
	asset_obj = pipe.Projects().GetAssetByInfo(nuke.root().name())
	if not asset_obj: raise Exception('Script not in projects')
	obj_data = asset_obj.GetShot()
	if not obj_data: obj_data = asset_obj.GetSequence()
	if not obj_data: raise Exception('Data path not found')
	#obj_data.RefreshRenderLatest()
	#renders_data = obj_data.GetDataRenderLatest()
	meta_knob = read_node.metadata()
	renders_data = filesys.GetAllRenderVersions(meta_knob['input/filename'])
	#print renders_data
	ReloadRendersPanel(read_node, renders_data).showModalDialog()