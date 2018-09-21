#! /usr/bin/python
# coding: utf-8
#init
import Image
import sys
argvs=sys.argv
argc=len(argvs)
if (argc != 2): 
	print 'Usage: # python %s filename' % argvs[0]
	quit()
inputfile = argvs[1]
tif=Image.open("LALallLRforFiji.tif")

NEURON=[]
comment=[]
xlist=[]
ylist=[]
zlist=[]
radilist=[]
cclasslist=[]
parlist=[]
regeonlist=[]
ID=0	#modified

#read swc
f=open(inputfile)
lines=f.readlines()
for line in lines:
	if (len(line)==0):
		continue
	elif line.startswith("#"):
		line=line[1:-1]
		print line
		comment.append(line)
		continue  
	data=line[:-1].split(' ')
	ID=int(data[0])
	cclass=int(data[1])
	x = float(data[2]) 
	y = float(data[3]) 
	z = float(data[4])
	radi = float(data[5])
	parent= int(data[6])
#identify regeon
# ����ԃX�P�[�� -> �s�N�Z���X�P�[���֕ϊ�
	regx=int(round((x-1)/2))		#modified
	regy=int(round((y-1)/2))		#modified
	regz=int(round((z-1)/2))		#modified
	#print ID,x,y,z,regx,regy,regz	#�f�o�b�N modified
	tif.seek(0)
	tif.seek(regz)
    
	tmpimg=tif.load() #modified  tmpimg=tif.load
	label=tif.getpixel((regx,regy))
    
#    print parent
#    print cclass
	#print ID,regx,regy,regz,label  #modified
	
	xlist.append(x)
	ylist.append(y)
	zlist.append(z)
	radilist.append(radi)
	cclasslist.append(cclass)
	parlist.append(parent)
	#modified cclass�l�̌���
	tmplabel=label			# �f�o�b�N�p�l
	label=label-128			# label����128�������l�ɕύX
	if (regx>=256):			# x���W��256�ȏ�̏ꍇ
		label= label+64		# 64�𑫂�
	if (label<0):		# �Ή�������W�_��������Ȃ������ꍇlabel��0�ȉ��̏ꍇ -> ���Ƃ��Ƃ�cclass��Ԃ�
		label=cclass

	regeonlist.append(label)
	print ID,x,y,z,regx,regy,regz,cclass,tmplabel,label #modified
f.close
##testof new-write

f=open(inputfile[0:-3]+'new.swc','w')
for come in comment:
	f.write('#')
	f.write(come)
	f.write('\n')
f.write('\n')
for i in range(0,ID):
	f.writelines([str(i+1)," ",str(regeonlist[i])," "])		# modified:  str(cclasslist[i])," "] -> str(regeonlist[i]),","]
	f.writelines([str(xlist[i])," ",str(ylist[i])," ",str(zlist[i])," "])
	f.writelines([str(radilist[i])," ",str(parlist[i]),"\n"])
f.close

print regeonlist


#process image
#debug print tif.size
[xsize,ysize]=tif.size
#print xsize,ysize
#tif.show()
#print tif.info
#tif.seek(1)
#z=0
#try:
# while 1:
#  tif.seek(tif.tell()+1)
  #print tif.size
#  z=z+1
#  print z
#  tmppx=tif.load
#  label=tmppx[10,10]
#  for i in range(1,xsize):
#   for j in range(1,ysize):
#     label=tmppx(i,j)
#     label=tif.getpixel((i,j)) 
#     if label!=0: 
#      print label


#except EOFError:
# pass

