n = nuke.selectedNode()
x = 800
y = 600

coord = []
sphList = []
mrgList = []
l = 0
ll = 0
h = []

for i in range(x):
	for j in range(y):
		alpha = nuke.sample(n, 'alpha', i, j)
		if alpha != 0:
			r = [nuke.sample(n, 'red', i, j),nuke.sample(n, 'green', i, j),nuke.sample(n, 'blue', i, j)]
			coord.append(r)

g = nuke.createNode('Group')

g.begin()

for c in coord[::10]:
	
	if l == 1000 or len(coord) == ll:
		sphList.append(h)
		h = []
		l = 0
	
	else:
		a = nuke.createNode('Sphere', 'inpanel=False')
		a['translate'].setValue(c)
		a['rows'].setValue(2)
		a['columns'].setValue(2)
		a['uniform_scale'].setExpression('Group1.SPHScale', 0)
		a.setInput(0, None)
		h.append(a)
		
	l += 1
	ll += 1

for n in sphList:
	m = nuke.createNode('MergeGeo')
	mrgList.append(m)
	for s in zip(n, range(len(n))):
		m.setInput(s[1], s[0])

m = nuke.createNode('MergeGeo')

for mrg in zip(mrgList, range(len(mrgList))):
	m.setInput(mrg[1], mrg[0])

o = nuke.createNode('Output')


g.addKnob(nuke.Tab_Knob('SphScale', 'Scaling'))
g.addKnob(nuke.Double_Knob('SPHScale', 'Scaling'))
g['SPHScale'].setValue(0.5)
g.end()	
	
	
