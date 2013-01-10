from cexceptions import *
import sys	
import subprocess
from nukescripts import pyQtAppUtils, utils
sys.path.append('/usr/pipeline/lib')
import os, filesys, app, pipe

def cvci():
	
	try:
		comment = 'test check in'
		nuke.scriptSave() 
		proc = subprocess.Popen('comments -m maya -c good',  shell=True, stdout=subprocess.PIPE, )
		stdout_value = proc.communicate()[0]
		if stdout_value != None:
			comment = stdout_value #r.readlines()[0]
		lst_comments = comment.split('\t')
		isGood = False
		if len(lst_comments) > 1:
			if lst_comments[1].strip('\n') == 'g':
				isGood = True
			comment = lst_comments[0]
		asset_obj = pipe.Projects().GetAssetByInfo(nuke.root().name())
		asset_obj.CheckIn(comment, isGood)
	except:
		exctype, value = sys.exc_info()[:2]
		raise Exception("Unexpected error: %s" % value)