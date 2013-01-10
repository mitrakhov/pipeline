'''
    IFDuserhooks.py
    A simple example to illustrate the IFDhooks features
'''
import traceback
from IFDapi import *
import math
import os
import re
import hou
import soho
from soho import SohoParm

ifdcodeParms = {
    'vm_ifdcode' : SohoParm('vm_ifdcode', 'string', [''], False),
}

def processInclude(filename):

    if filename:
        if filename.find(' ') >= 0:
            ray_comment('Inline include (value has spaces)')
            #soho.indent()
            print filename
            ray_comment('End of Inline include')
        else:
            try:
                fp = open(filename, 'r')
                ray_comment('Include file: %s' % filename)
                for line in fp.readlines():
                    #soho.indent()
                    sys.stdout.write(hou.expandString(line))
                ray_comment('End of include file: %s' % filename)
            except:
                ray_comment('Error processing include file: %s' % filename)
        return True
        
    return False


    
def pre_outputInstance(obj, now):
    plist = obj.evaluate(ifdcodeParms, now) 
    ifdcode = plist['vm_ifdcode']
    if ifdcode:
        return processInclude(ifdcode.Value[0])
     
    return False
    
    
    
''' List of hooks in this file '''
_HOOKS = {
    'pre_outputInstance'   : pre_outputInstance,
}

def call(name='', *args, **kwargs):
    ''' Hook callback function '''
    method = _HOOKS.get(name, None)
    if method:
        try:
            if method(*args, **kwargs):
                return True
            else:
                return False
        except Exception, err:
            ray_comment('Hook Error[%s]: %s %s' % (name, __file__, str(err)))
            ray_comment('Traceback:\n# %s\n' %
                        '\n#'.join(traceback.format_exc().split('\n')))
    return False