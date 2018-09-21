#! /usr/bin/python
# coding: utf-8
#init
import Image
import sys
outpath=r'/home/kazawa/'
argvs=sys.argv
argc=len(argvs)
if (argc != 2): 
	print 'Usage: # python %s filename' % argvs[0]
	quit()
input = argvs[1]
if input[-4:]=='.swc':	
	if input[-8]=='.new.swc':
		basename==input[1:-9]
        else:
		basename==input[1::-5]+'.new'
else:
	basename==input

print basename

a=input(' continue ? (y or else) > ')
if a!='y':
	quit()
 
# shutil.copyfile(file1,file2)
# shutils.copyfile(file3,file4)

