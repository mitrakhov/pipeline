def cnew():
	import sys,os,popen2
	import cdebug	
	import  subprocess
	from nukescripts import pyQtAppUtils, utils
	mdebug = cdebug.cdebug()
	mdebug(sys.path)
	sys.path.append('/usr/pipeline/lib')
	#import nasset
	import pipe, filesys
	proc = subprocess.Popen('nasset -m nuke',  shell=True, stdout=subprocess.PIPE, )
	result = proc.communicate()[0]
	#result = nasset.browse('nuke')
	if result == 'cancel': return
	obj = filesys.get_options(result,'m:t:d:c:')
	file_path = obj[1][0]
	proj_name = obj[1][1]
	tmp_path_file = os.path.join(filesys.USER_HOME,file_path)
	
	nuke.scriptSave(tmp_path_file)
	
	descr =  obj[0]['-d']
	tags = obj[0]['-t']
	modes =  obj[0]['-m'].split(',')
	
	type_name = modes[0]
	seq_name = modes[1]
	shot_name = modes[2]
	#print proj_name,tmp_path_file,descr,tags
	
	new_obj = pipe.Pipe().AddAsset(proj_name,tmp_path_file,descr,tags,filesys.COMP,sname=seq_name,shname=shot_name)
	script_path = new_obj.CheckOut('l')
	
	if len(modes) == 4:
		new_obj.setDependency(modes[3])
	
	if os.path.exists(script_path):
		os.system('sync')
		nuke.scriptOpen(script_path)
