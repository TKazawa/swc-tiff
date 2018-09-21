#!/usr/bin/python
# coding: utf-8
import Image
import numpy as np # numpyモジュールのインポート
import os




dir_filelist=[]
filelist=[]


# ファイル名取得用関数

def getswcfiles(path):
	swclist=[]
	#dirlist=[]
	for root, dirs, files in os.walk(path):
#(root,dirs,files)=os.walk(path)
		for file in files:
		#   if file[-3:]==r'.py': 
		#    if file[-4:] == r".swc":
			#print os.path.join(root, file)
			tmpname =os.path.join(root, file)		# modifiedディレクトリ名+ファイル名の一時確保
			if tmpname[-8:]=='.new.swc':				# modified 拡張子.swcの検出
				
				dir_filelist.append(tmpname)		# modified 拡張子.new.swcならばリストに追加
				filelist.append(file)				# modified ファイル名のみも追加
			#print file		#デバック：ファイル名の出力
			#if file[-4:]=='.swc':					# modified ファイル名の取得
			#	filelist.append(file)
		#     print file
		swclist.append([root,file])
	return swclist

	


# メイン関数
def main():

# ファイルとサブディレクトリのパスを表示する
 #path = '~/shrsmb/StandardBrain'
	
	path=r'./'	 #Unix用
	#path=r'.\\' #windows用
	list=getswcfiles(path)
	print dir_filelist		# modified デバック用
	#print filelist			# modified デバック用
	#print len(filelist)		# modified デバック用
	#print len(dir_filelist)
	
#	for inputfile in dir_filelist:
#		Conv3d2d(inputfile)
	

if __name__ == '__main__': main()




