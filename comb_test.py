# coding: utf-8
import os, os.path # osモジュールのインポート
import Image
import sys
import numpy as np # numpyモジュールのインポート

# os.listdir('パス')
# 指定したパス内の全てのファイルとディレクトリを要素とするリストを返す
#files = os.listdir('.')

dir_filelist=[] #modified /ファイルリスト作成
filelist=[]		#modified /ファイルリスト作成

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
			if tmpname[-4:]=='.swc':				# modified 拡張子.swcの検出
				
				if (tmpname>8)&(tmpname[-8:]!='.new.swc'):
					dir_filelist.append(tmpname)		# modified 拡張子.swcならばリストに追加
			
			#print file		#デバック：ファイル名の出力
			#if file[-4:]=='.swc':					# modified ファイル名の取得
			#	filelist.append(file)
		#     print file
		swclist.append([root,file])
	return swclist
	
# プログラム実行関数	
def imgid(inputfile):

	print inputfile
	tif=Image.open("LALallLRforV3D.tif")	#ファイル読み込み

	# リスト作成
	NEURON=[]
	comment=[]
	xlist=[]
	ylist=[]
	zlist=[]
	xstrlist=[]
	ystrlist=[]
	zstrlist=[]
	radilist=[]
	radistrlist=[]
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
			#print line
			comment.append(line)
			continue  
	        data=line[:-1].split(' ')
	        print data[0] #for debug
                ID=int(data[0])
		cclass=int(data[1])
		x =  np.float64(data[2]) 
		y =  np.float64(data[3]) 
		z =  np.float64(data[4])
		radi =  np.float64(data[5])
		parent= int(data[6])
#identify regeon
# 実空間スケール -> ピクセルスケールへ変換
		regx=int(round((x-1.0)/2.0))		#modified /1引いた値を２で割って丸める -> 整数化
		regy=int(round((y-1.0)/2.0))		#modified
		regz=int(round((z-1.0)/2.0))		#modified
	#print ID,x,y,z,regx,regy,regz	#デバック modified
		tif.seek(0)
		tif.seek(regz)
    
		tmpimg=tif.load() #modified  tmpimg=tif.load
		label=tif.getpixel((regx,regy))
    
#    print parent
#    print cclass
	#print ID,regx,regy,regz,label  #modified
		xstrlist.append(data[2])
		ystrlist.append(data[3])
		zstrlist.append(data[4])
		radistrlist.append(data[5])
		
		xlist.append(x)
		ylist.append(y)
		zlist.append(z)
		radilist.append(radi)
		cclasslist.append(cclass)	
		parlist.append(parent)
	#modified cclass値の決定
	# 上位１ビットは空白
	# 次1ビットは検出した値
	# 次1ビットは左右判定 (右ならば+8してある)
	# 下位3ビットは元のラベル
	
		tmplabel=label			# デバック用値
		label = label-(128+64+32+16+8)			# 検出したlabelを3ビットに落とす (0の場合は無視)
		label = label*16							# 16(2^4)をかけて4ビット分ビットシフト
		if (regx>=256):							# x座標が256以上の場合
			label= label+8						# 8(2^3)の位に右か左かを検出
		if (label<0):							# 対応する座標点が見つからなかった場合、つまりlabelが0以下の場合 
			label=0								# ラベルの値を０にする
								
		label = label + cclass					# ラベルにもとのラベルの値を足す（下位3ビットにもとの値を足す）

		regeonlist.append(label)
		#print ID,x,y,z,regx,regy,regz,cclass,tmplabel,label,format(label,'b') #modified
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
		f.writelines([str(xstrlist[i])," ",str(ystrlist[i])," ",str(zstrlist[i])," "])
		f.writelines([str(radistrlist[i])," ",str(parlist[i]),"\n"])
	f.close

	print regeonlist

	
# メイン関数
def main():

# ファイルとサブディレクトリのパスを表示する
 #path = '~/shrsmb/StandardBrain'
	
	path=r'./'	#パスの指定
	list=getswcfiles(path)
	#print dir_filelist		# modified デバック用
	print filelist			# modified デバック用
	#print len(filelist)		# modified デバック用
	#print len(dir_filelist)
	
	for inputfile in dir_filelist:		# リストを読み込み実施関数へ
		imgid(inputfile)
	

if __name__ == '__main__': main()


#print root
#print dirs
#print file
