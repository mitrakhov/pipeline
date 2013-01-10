#
# PROPRIETARY INFORMATION.  This software is proprietary to
# Side Effects Software Inc., and is not to be reproduced,
# transmitted, or disclosed in any way without written permission.
#
# Produced by:
#       Side Effects Software Inc
#       123 Front Street West, Suite 1401
#       Toronto, Ontario
#       Canada   M5J 2M2
#       416-504-9876
#
# NAME:         mantra.py ( Python )
#
# COMMENTS:     IFD generation using SOHO
#

import time
import soho
import hou
import IFDapi
import IFDmisc
import IFDframe
import IFDgeo
import IFDsettings
import IFDhooks
from soho import SohoParm
from IFDapi import *

clockstart = time.clock()

controlParameters = {
    # The time at which the scene is being rendered
    'now'     : SohoParm('state:time', 'real',  [0], False,  key='now'),

    'main'    : SohoParm('render_viewcamera','int', [1], False, key='main'),
    'decl'    : SohoParm('declare_all_shops', 'int', [0], False, key='decl'),
    'engine'  : SohoParm('vm_renderengine',  'string', ['micropoly'],
                                            False, key='engine'),
    'vm_inheritproperties' : SohoParm('vm_inheritproperties', 'int', [0], False),
    'vm_embedvex' :SohoParm('vm_embedvex',  'int', [0], False, key='embedvex'),
}

parmlist = soho.evaluate(controlParameters)

now     = parmlist['now'].Value[0]
IFDapi.ForceEmbedVex = parmlist['embedvex'].Value[0]
decl_shops = parmlist['decl'].Value[0]

inheritedproperties = parmlist['vm_inheritproperties'].Value[0]

options = {}
if inheritedproperties:
    # Turn off object->output driver inheritance
    options['state:inheritance'] = '-rop'

    
if not soho.initialize(now, None):
    soho.error("Unable to initialize rendering module")
    
#
# Add objects to the scene, we check for parameters on the viewing
# camera.  If the parameters don't exist there, they will be picked up
# by the output driver.
#
objectSelection = {
    # Candidate object selection
    # Candidate object selection
    'vobject'     : SohoParm('vobject', 'string',       ['*'], False),
    'alights'     : SohoParm('alights', 'string',       ['*'], False),
    'vfog'        : SohoParm('vfog',    'string',       ['*'], False),

    'forceobject' : SohoParm('forceobject',     'string',       [''], False),
    'forcelights' : SohoParm('forcelights',     'string',       [''], False),
    'forcefog'    : SohoParm('forcefog',        'string',       [''], False),

    'excludeobject' : SohoParm('excludeobject', 'string',       [''], False),
    'excludelights' : SohoParm('excludelights', 'string',       [''], False),
    'excludefog'    : SohoParm('excludefog',    'string',       [''], False),

    'matte_objects'   : SohoParm('matte_objects', 'string',     [''], False),
    'phantom_objects' : SohoParm('phantom_objects', 'string',   [''], False),

    'sololight'     : SohoParm('sololight',     'string',       [''], False),
}


objparms = soho.evaluate(objectSelection, now)
stdobject = objparms['vobject'].Value[0]
stdlights = objparms['alights'].Value[0]
stdfog = objparms['vfog'].Value[0]
forceobject = objparms['forceobject'].Value[0]
forcelights = objparms['forcelights'].Value[0]
forcefog = objparms['forcefog'].Value[0]
excludeobject = objparms['excludeobject'].Value[0]
excludelights = objparms['excludelights'].Value[0]
excludefog = objparms['excludefog'].Value[0]
sololight = objparms['sololight'].Value[0]
matte_objects = objparms['matte_objects'].Value[0]
phantom_objects = objparms['phantom_objects'].Value[0]
forcelightsparm = 'forcelights'
if sololight:
    stdlights = excludelights = ''
    forcelights = sololight
    forcelightsparm = 'sololight'

# First, we add objects based on their display flags or dimmer values
soho.addObjects(now, stdobject, stdlights, stdfog, True,
    geo_parm='vobject', light_parm='alights', fog_parm='vfog')
soho.addObjects(now, forceobject, forcelights, forcefog, False,
    geo_parm='forceobject', light_parm=forcelightsparm, fog_parm='forcefog')

# Force matte & phantom objects to be visible too
if matte_objects:
    soho.addObjects(now, matte_objects, '', '', False,
	geo_parm='matte_objects', light_parm='', fog_parm='')
if phantom_objects:
    soho.addObjects(now, phantom_objects, '', '', False,
	geo_parm='phantom_objects', light_parm='', fog_parm='')
soho.removeObjects(now, excludeobject, excludelights, excludefog,
    geo_parm='excludeobject', light_parm='excludelights', fog_parm='excludefog')

    
# Lock off the objects we've selected
soho.lockObjects(now)

IFDsettings.clearLists()
IFDsettings.load(now)
IFDgeo.reset()

if inheritedproperties:
    # Output object level properties which are defined on the output driver
    ray_comment('Object properties defined on output driver')
    IFDsettings.outputObject(soho.getOutputDriver(), now)


if decl_shops:
    IFDgeo.declareAllMaterials(now, decl_shops > 1)

#
# Output objects
#
IFDframe.outputObjects(now,
    soho.objectList('objlist:instance'),
    soho.objectList('objlist:light'),
    soho.objectList('objlist:space'),
    soho.objectList('objlist:fog'),
    -1, -1)
