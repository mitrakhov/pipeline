import nuke,os,re
from cexceptions import *
import filesys
import cdebug
mdebug = cdebug.cdebug()

def condensing_is(folder_path,name):
	"""Return dictionary
	@todo: do over re.pattern. Get together ones
	"""
	dct = {}	
	imseqs = filesys.ImageSequences(folder_path).get_sequences()
	for imseq in imseqs:
		range = imseq.getRange()
		user_text = '%s%s%s%s%%0%sd.%s %s-%s'%(imseq.getPath(),os.sep,imseq.getFileName(),imseq.getSep(),imseq.getLengthOfPadding(),imseq.getExt(),range[0],range[1])
		name_sq = imseq.getFileName() + "_"		
		dct[name_sq] = user_text
	
	lst = os.listdir(folder_path)
	lst_d = filter(lambda x: os.path.isdir(folder_path + os.sep + x), lst)
	for o in lst_d:
		dct.update(condensing_is(folder_path + os.sep + o,name+'_'+o))
	return dct
	
	
	lst = os.listdir(folder_path)
	lst_f = filter(lambda x: not os.path.isdir(folder_path + os.sep + x), lst)
	if lst_f: 
		num_src = 1
		while lst_f:
			name_sq = str('__' + name + '_' + str(num_src) + '__').upper()
			path_sq = str(str(num_src) + '/' + name).upper()
			name_fl = lst_f[0]
			srch = pat.search(name_fl)
			index = 2
			if not srch:
				pat = re.compile('^(\d{1,10})\.(.*)')
				index = 1
				srch = pat.search(name_fl)
			
			if not srch: 
				mdebug(srch,lst_f) 
				break
				
			name_fl = name_fl[:srch.start(index)]
			lst = os.listdir(folder_path)
			
			name_ln = len(name_fl)
			sequence_fl = filter(lambda x: x[:name_ln] == name_fl, lst_f)
			lst_f = filter(lambda x: not x in sequence_fl, lst_f)
			if len(sequence_fl) < 2: continue
			sequence_num = map(lambda x: int(pat.search(x).group(index)), sequence_fl)
			sequence_num.sort()
			dct[name_sq] = '%s%s%s%%0%sd.%s %s-%s'%(folder_path,os.sep,name_fl,len(srch.group(index)),srch.group(index+1),sequence_num[0],sequence_num[-1])
			num_src += 1

	lst_d = filter(lambda x: os.path.isdir(folder_path + os.sep + x), lst)
	for o in lst_d:
		dct.update(condensing_is(folder_path + os.sep + o,name+'_'+o))
	return dct

def load_src():
	import pipe
	asset_obj = pipe.Projects().GetAssetByInfo(nuke.root().name())
	if not asset_obj: return
	shot_obj = asset_obj.GetShot()
	if not shot_obj: raise Exception('Shot not found')
	src_path = shot_obj.GetSrcPath()
	sequences = condensing_is(src_path,'src')
	if not sequences: nuke.message("There aren't files in folder SRC")
	filenameSearch = "Load"
	enumerationPulldownp = "None " + ' '.join(sequences.keys()) 
	p = nuke.Panel("Presets selection")
	p.addEnumerationPulldown("SRC to load:", enumerationPulldownp)
	p.addButton("Cancel") 
	p.addButton("Load")
	
	result = p.show()
	enumVal = p.value("SRC to load:")
	if enumVal == 'None': return
	#nuke.message(sequences[enumVal])
	n = nuke.toNode(enumVal)
	if not n: 
		n = nuke.createNode('Read', inpanel=False)
		n.setName(enumVal)
	n.knob('file').fromUserText(sequences[enumVal])
	
	
	
