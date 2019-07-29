from abaqus import *
from abaqusConstants import *

import numpy
from math import sqrt
# create edge set

bdp = [0,0,5]
# beam section direct point

Mdb()
model1 = mdb.Model(name='Model-1')
part1 = model1.Part(name='Part-1')

p0 = [0.,0.,0.]

p1 = [1.,0.,1.]
p2 = [sqrt(2)/2.,sqrt(2)/2.,1.]
p3 = [0.,1.,1.]
p4 = [-sqrt(2)/2.,sqrt(2)/2.,1.]
p5 = [-1.,0.,1.]
p6 = [-sqrt(2)/2.,-sqrt(2)/2.,1.]

part1.DatumPointByCoordinate(coords=(p0[0],p0[1],p0[2]))

part1.DatumPointByCoordinate(coords=(p1[0],p1[1],p1[2]))
part1.DatumPointByCoordinate(coords=(p2[0],p2[1],p2[2]))
part1.DatumPointByCoordinate(coords=(p3[0],p3[1],p3[2]))
part1.DatumPointByCoordinate(coords=(p4[0],p4[1],p4[2]))
part1.DatumPointByCoordinate(coords=(p5[0],p5[1],p5[2]))
part1.DatumPointByCoordinate(coords=(p6[0],p6[1],p6[2]))

d=part1.datums

for i in range(2,8):
	part1.WirePolyLine(points=((d[1],d[i]),))
	
print 'lines finished'

e=part1.edges
v=part1.vertices
enum=len(e)

model1.Material(name='steel')
model1.materials['steel'].Density(table=((7850,),))
model1.materials['steel'].Elastic(table=((200000000000,.3),))
model1.RectangularProfile(name='pipe1',a=0.01,b=0.05)
model1.BeamSection(name='Pipe-1',integration=DURING_ANALYSIS,profile='pipe1',material='steel')

regionSection=part1.Set(edges=e,name='Set-section')
part1.SectionAssignment(region=regionSection,sectionName='Pipe-1')

import part

for i in range(enum):
	thisedge = e[i]
	poe = thisedge.pointOn
	# poe = point on edge
	poe = poe[0]
	bsv2 = []
	# bsv2 = beam section vector2
	for j in range(3):
		bsv2.append(bdp[j]-poe[j])
	vedge = thisedge.getVertices()
	v1=v[vedge[0]]
	v2=v[vedge[1]]
	v1=v1.pointOn
	v2=v2.pointOn
	v1=v1[0]
	v2=v2[0]
	bsv3 = []
	# bsv3 = beam section vector3
	for k in range(3):
		bsv3.append(v1[k]-v2[k])
	bsv2 = numpy.array(bsv2)
	bsv3 = numpy.array(bsv3)
	bsv = numpy.cross(bsv2,bsv3)
	ee=[]
	ee.append(thisedge)
	earray = part.EdgeArray(ee)
	esetname = 'edgeset-'+str(i+1)
	eset = part1.Set(edges=earray,name=esetname)
	part1.assignBeamSectionOrientation(region=eset,method=N1_COSINES,n1=bsv)
	
	
print 'finish'