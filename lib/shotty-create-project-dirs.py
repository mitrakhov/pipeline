#!/usr/bin/env python
import os
import slumber
from optparse import OptionParser


parser = OptionParser()

parser.add_option('--project', dest = 'project', default = None, help = 'project')
parser.add_option('--sequence', dest = 'sequence', default = None, help = 'sequence')

(options, args) = parser.parse_args()


api = slumber.API("http://chimney.shotty.cc/api/v1/", auth=("shotty", "chimney"))


shots = api.shot.get(project__slug=options.project, scene__name=options.sequence)


print 'Total %i shots in project' % (shots['meta']['total_count'])


for shot in shots['objects']:

  scene = shot['scene']['name'].upper()
	shot_name = ('%s_%s') % (scene, shot['name'])
	print shot_name


	pwd = os.getcwd()
	paths = []
	dirs = ['dailies',
			 'hires',
			 'animation',
			 'tracking/proxy',
			 'scripts/nk',
			 'images/img',
			 'images/render',
			 'images/refs',
			 'images/tex',
			 '3d/houdini',
			 '3d/maya']
	for i in dirs:
		paths.append(os.path.join(pwd, scene, shot['name'], i))
		
	for item in paths:
		if not os.path.exists(item):
			os.makedirs(item)

