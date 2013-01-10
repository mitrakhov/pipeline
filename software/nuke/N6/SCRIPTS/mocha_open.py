import sys, os, re
from cexceptions import *

TEMPLATE="/usr/pipeline/software/nuke/SCRIPTS/template_project.mocha"

class buff(object):
	def __init__(self,file_name,parent=None):
		self.__keys = []
		self.__dict = {}
		self._my_buffer = buffer
		self._file_name = file_name
		fl = open(self._file_name,'r')
		self._my_buffer = fl.read()
		fl.close()
		
	def values(self):
		return [self.__dict[key] for key in self.__keys]

	def keys(self):
		return self.__keys[:]
	
	def __setitem__(self, key, item): 
		m = re.search(key+'(.*)$',self._my_buffer,re.MULTILINE)
		if m and m.groups() > 0:
			self._my_buffer = self._my_buffer[0:m.start(1)] +'='+ str(item) + self._my_buffer[m.end(1):len(self._my_buffer)]
		
	def __getitem__(self, key):
		pat = re.compile(key+'=(.*)$',re.MULTILINE)
		sitem = pat.search(self._my_buffer)
		if sitem:
			self.__dict[key] = sitem.group(1)
		return self.__dict[key]
	
	def replace(self,old_value,new_value):
		self._my_buffer = self._my_buffer.replace(old_value,new_value)

	def save(self,new_name=None):
		filename= new_name
		if not filename: filename = self._file_name
		fl = open(filename,'w')
		fl.write(str(self._my_buffer))
		fl.close()
		
	def __str__(self):
		return self._my_buffer
	

	
def mocha_open():
	n = nuke.selectedNode()
	if not n.Class() == 'Read': raise Exception('Must select a read node!')
	frmt = n.knob('format').value()
	frrg = n.frameRange()
	first = int(frrg.first())
	last = int(frrg.last())
	
	import pipe, filesys
	asset_obj = pipe.Projects().GetAssetByInfo(nuke.root().name())
	if not asset_obj: return
	shot_obj = asset_obj.GetShot()
	if not shot_obj: raise Exception('Shot not found')
	
	start_path = asset_obj.GetDataPath() + os.sep + 'tracks' + os.sep
	
	
	file_v = n.knob('file').value()
	ext = file_v.split('.')[-1]
	new_path = file_v.rsplit(os.sep,1)[0] + os.sep

	ims = filesys.ImageSequence(new_path)
	
	files = [x for x in os.listdir(new_path) if x[-(len(ext)):] == ext]
	
	new_len_files = last - first # + 1
	new_name = ims.getName()# + ims.getSep() #'.'.join(files[0].split('.')[:-2])
	
	conf_file = filesys.USER_HOME + os.sep + '.config/Imagineer Systems Ltd/Mocha 1 Linux.conf'
	if not os.path.exists(conf_file): 
		raise Exception("Default config file not found: " ','.join(os.listdir(filesys.USER_HOME + os.sep + '.config/Imagineer Systems Ltd')))
	
	cls_config = buff(conf_file)
	cls_config["LastSaveTrackingDataFolder"] = start_path
	cls_config["AbsoluteOutputDirectory"] = '/tmp//MoTemp'
	cls_config["LastTrackingExportFormat"] = 9
	
	cls_config.save()
	
	cls_buffer = buff(TEMPLATE)
	
	old_name = cls_buffer["Core.ClipPrefix.value"][:-1]
	
	cls_buffer["Core.ClipLength.value"] = new_len_files + 1
	cls_buffer["Core.ClipDirectory.value"] = new_path
	cls_buffer["ProjectOutputDirectory.value"] = '/tmp//MoTemp'
	cls_buffer["Core.MaximumIndex.value"] = last
	cls_buffer["Core.MinimumIndex.value"] = first
	cls_buffer["UseAbsoluteOutputDirectory.value"] = 1
	cls_buffer["Core.FrameWidth.value"] = frmt.width()
	cls_buffer["Core.FrameHeight.value"] = frmt.height()
	cls_buffer["Core.ClipSuffix.value"] = '.'+ext
	cls_buffer["Core.ClipPrefix.value"] = new_name + ims.getSep()
	cls_buffer["PlaybackOutPoint.value"] = new_len_files#last-1
	cls_buffer["Core.IndexWidth.value"] = ims.getLengthOfPadding()
	cls_buffer["Core.FirstFrameOffset.value"] = 1
	
	""" How about this:
	.Core.FrameRate.value=24                                                                                                                                                                                                               
	.Core.MasterTimelineClipID.value=0                                                                                                                                                                                                     
	.Core.FirstFrameOffset.value=1                                                                                                                                                                                                         
	.Core.FilmType.value=HD                                                                                                                                                                                                                
	.Core.FilmBackWidth.value=16                                                                                                                                                                                                           
	.Core.FilmBackHeight.value=9                                                                                                                                                                                                           
	.Core.FilmWidth1.value=1920                                                                                                                                                                                                            
	.Core.FilmWidth2.value=1280                                                                                                                                                                                                            
	.Core.FilmWidth3.value=640                                                                                                                                                                                                             
	.Core.FilmHeight1.value=1080                                                                                                                                                                                                           
	.Core.FilmHeight2.value=720                                                                                                                                                                                                            
	.Core.FilmHeight3.value=480                                                                                                                                                                                                            
	.Core.AspectRatio.value=1.77778                                                                                                                                                                                                        
	.Core.PixelAspectRatio.value=1
	?????????????     
	""" 
	cls_buffer.replace(old_name, new_name)
	os.system('mkdir /tmp/MoTemp')
	cls_buffer.save('/tmp/MoTemp/new.mocha')
	os.system('/mnt/opt/mocha/mocha /tmp/MoTemp/new.mocha ')