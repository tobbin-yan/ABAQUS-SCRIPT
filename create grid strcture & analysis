from abaqus import *
from abaqusConstants import *
import numpy

Mdb()
model1=mdb.Model(name='Model-1')
part1=model1.Part(name='Part-1')

#l1=10
#l2=10
#h=1

m=(('L1','10'),('L2','10'),('H','1'),('UL',"1"))
l1,l2,h,ul=getInputs(fields=m,label='Input the size',dialogTitle='Parameters')

l1=int(l1)
l2=int(l2)
h=float(h)
ul=float(ul)

pt=0
nloc=[]
un=numpy.zeros(shape=(l1,l2))
dn=numpy.zeros(shape=(l1-1,l2-1))

for i in range (0,l1):
	for j in range (0,l2):
		part1.DatumPointByCoordinate(coords=(float(i)*ul,float(j)*ul,0.0))
		pt=pt+1
		nloc.append([float(i)*ul,float(j)*ul,0.0])
		un[i,j]=pt

print 'up node'
print un

for i in range (0,l1-1):
	for j in range (0,l2-1):
		part1.DatumPointByCoordinate(coords=(float(i)*ul+0.5*ul,float(j)*ul+0.5*ul,float(h*-1)))
		pt=pt+1
		nloc.append([float(i)*ul+0.5*ul,float(j)*ul+0.5*ul,float(h*-1)])
		dn[i,j]=pt
		
print 'down node'
print dn

d=part1.datums

#

for i in range (0,l1):
	for j in range (0,l2-1):
		part1.WirePolyLine(points=((d[int(un[i,j])],d[int(un[i,j+1])]),))
		
for i in range (0,l1-1):
	for j in range (0,l2):
		part1.WirePolyLine(points=((d[int(un[i,j])],d[int(un[i+1,j])]),))
		
for i in range (0,l1-1):
	for j in range (0,l2-2):
		part1.WirePolyLine(points=((d[int(dn[i,j])],d[int(dn[i,j+1])]),))
		
for i in range (0,l1-2):
	for j in range (0,l2-1):
		part1.WirePolyLine(points=((d[int(dn[i,j])],d[int(dn[i+1,j])]),))

#

for i in range (0,l1-1):
	for j in range (0,l2-1):
		part1.WirePolyLine(points=((d[int(dn[i,j])],d[int(un[i,j])]),))
		part1.WirePolyLine(points=((d[int(dn[i,j])],d[int(un[i,j+1])]),))
		part1.WirePolyLine(points=((d[int(dn[i,j])],d[int(un[i+1,j])]),))
		part1.WirePolyLine(points=((d[int(dn[i,j])],d[int(un[i+1,j+1])]),))

print 'geo finished'
#	material & section	
		
		
model1.Material(name='steel')
model1.materials['steel'].Density(table=((7850,),))
model1.materials['steel'].Elastic(table=((200000000000,.3),))
model1.PipeProfile(name='pipe1',r=0.02,t=0.01)
model1.BeamSection(name='Pipe-1',integration=DURING_ANALYSIS,profile='pipe1',material='steel')

# section & assign

e=part1.edges
regionSection=part1.Set(edges=e,name='Set-section')
part1.SectionAssignment(region=regionSection,sectionName='Pipe-1')
part1.assignBeamSectionOrientation(region=regionSection,method=N1_COSINES,n1=(0.0,10.0,100.0))
ass=model1.rootAssembly
ass.Instance(name='wj-1',part=part1,dependent=ON)

print 'material & section finished'
# step

step1=model1.StaticStep(name='Step-1', previous='Initial')
step1.setValues(timePeriod=1.0, initialInc=0.01, minInc=2e-05, maxInc=0.1)

# mesh

import mesh

part1.seedPart(size=10,deviationFactor=0.1,minSizeFactor=0.1)
elemType1=mesh.ElemType(elemCode=B31,elemLibrary=STANDARD)
e=part1.edges
regionMesh=part1.Set(edges=e,name='Set-mesh')
part1.setElementType(regions=regionMesh,elemTypes=(elemType1,))
part1.generateMesh()

print 'step & mesh finished'
# load

v=ass.instances['wj-1'].vertices
vbc1=v.findAt(((1.5*ul,1.5*ul,-h),))
regionBC1=ass.Set(vertices=vbc1,name='Set-bc1')
model1.PinnedBC(name='BC-1',createStepName='Initial',region=regionBC1)

vbc2=v.findAt((((float(l1-2)-0.5)*ul,(float(l2-2)-0.5)*ul,-h),))
regionBC2=ass.Set(vertices=vbc2,name='Set-bc2')
model1.PinnedBC(name='BC-2',createStepName='Initial',region=regionBC2)

vbc3=v.findAt((((float(l1-2)-0.5)*ul,1.5*ul,-h),))
regionBC3=ass.Set(vertices=vbc3,name='Set-bc3')
model1.PinnedBC(name='BC-3',createStepName='Initial',region=regionBC3)

vbc4=v.findAt(((1.5*ul,(float(l2-2)-0.5)*ul,-h),))
regionBC4=ass.Set(vertices=vbc4,name='Set-bc4')
model1.PinnedBC(name='BC-4',createStepName='Initial',region=regionBC4)

e=ass.edges
model1.Gravity(name='Load-1', createStepName='Step-1',comp3=-9.8,)

print 'load & boundary finished'
# job

job1=mdb.Job(name='Job-1',model='Model-1',)
print 'start analysis'
job1.submit(consistencyChecking=OFF)
