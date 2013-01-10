"""
def ffffilenameFix(s):
	if os.name == "posix":
#		print 'Applying path mapping: windows --> linux'
		s = s.replace('//karramba/work/', '/mnt/karramba/', 1)
		s = s.replace('//karramba/Work/', '/mnt/karramba/', 1)
		s = s.replace('//Karramba/work/', '/mnt/karramba/', 1)
		s = s.replace('//Karramba/Work/', '/mnt/karramba/', 1)
		s = s.replace('//bigboy/d/', '/mnt/bigboy/', 1)
		s = s.replace('//bigboy/D/', '/mnt/bigboy/', 1)
		s = s.replace('//Bigboy/d/', '/mnt/bigboy/', 1)
		s = s.replace('//Bigboy/D/', '/mnt/bigboy/', 1)
		s = s.replace('K:/', '/mnt/karramba/', 1)
		s = s.replace('k:/', '/mnt/karramba/', 1)
		s = s.replace('W:/Work/', '/mnt/bigboy/', 1)
		s = s.replace('w:/Work/', '/mnt/bigboy/', 1)
		s = s.replace('W:/work/', '/mnt/bigboy/', 1)
		s = s.replace('w:/work/', '/mnt/bigboy/', 1)
		s = s.replace('D:/', '/mnt/disk/', 1)
		s = s.replace('d:/', '/mnt/disk/', 1)

	else:
#		print 'Applying path mapping for Windows'
		s = s.replace('/mnt/karramba/', '//karramba/work/', 1)
		s = s.replace('/mnt/bigboy/', '//bigboy/D/Work/', 1)
		s = s.replace('K:/', '//karramba/work/', 1)
		s = s.replace('k:/', '//karramba/work/', 1)
		s = s.replace('W:/', '//bigboy/D/Work/', 1)
		s = s.replace('w:/', '//bigboy/D/Work/', 1)
		s = s.replace('/mnt/disk/', 'D:/', 1)
		s = s.replace('H:/', '//karramba/work/Huggies/_src/', 1)
	return s
"""
