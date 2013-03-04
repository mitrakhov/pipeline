#from dBase import *
from shotgun_api3 import Shotgun
import os


site = 'https://chimneypot.shotgunstudio.com'    
scriptName = 'dBase'
scriptKey = '729a76955455909c79f6d90262bb9fbe9186b92b'
pName = 'kievPipelineTest'
sg = Shotgun(site, scriptName, scriptKey)

lst = sg.find('HumanUser', [['updated_at', 'not_in_last', 1, 'MONTH'],['sg_status_list', 'is', 'act']], ['name', 'updated_at', 'sg_status_list'])
for i in lst:
	print "%s: %s, %s, %s"%(i['name'],i['updated_at'], i['sg_status_list'], i['id'])

killEric = sg.update('HumanUser', 62, {'sg_status_list':'dis'})


def test():
	print 'huy'    
    return sg

