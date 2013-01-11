def hqsubmit():
	cmd = """afsubmitter -m nuke -o "-F %s-%s " -f "%s" -g afanasy"""
	path_script = nuke.root().name()
	os.system(cmd%(int(nuke.animationStart()),int(nuke.animationEnd()),path_script))
	#print nuke.animationStart()
	# Result: 397.0
	#print nuke.animationEnd()
	# Result: 482.0
	#print nuke.root().name()
	# Result: /mnt/karramba/test_zzz/film/sequences/XXX/shots/X01/comp/hqtest.nk
