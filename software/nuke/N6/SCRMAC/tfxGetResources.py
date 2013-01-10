import sys
sys.path.append('/usr/pipeline/lib')
import browser
import filesys

def GetResources():
	asset_obj = pipe.Projects().GetAssetByInfo(nuke.root().name())
	if not asset_obj: raise Exception('Script is not belong pipeline')
	proj_name = asset_obj.GetProject()
	# getParent()
	# type, db_id
	proc = subprocess.Popen('browser -c resources -a %s'%asset_obj.db_id,  shell=True, stdout=subprocess.PIPE, )
	stdout_value = proc.communicate()[0].strip()
	if stdout_value == 'cancel': return None
	imseq = filesys.ImageSequence(stdout_value)
	
	range = imseq.getRange()
	user_text = '%s%s%s%s%%0%sd.%s %s-%s'%(imseq.getPath(),os.sep,imseq.getFileName(),imseq.getSep(),imseq.getLengthOfPadding(),imseq.getExt(),range[0],range[1])
	
	name_node = '__%s__'%imseq.getFileName().upper().replace('.','_')
	
	n = nuke.toNode(name_node)
	if not n: 
		n = nuke.createNode('Read', inpanel=False)
		n.setName(name_node)
	n.knob('file').fromUserText(user_text)
	
	