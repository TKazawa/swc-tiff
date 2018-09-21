# coding: utf-8
import os, os.path # osモジュールのインポート
import sys
import numpy as np
import math

# os.listdir('パス')
# 指定したパス内の全てのファイルとディレクトリを要素とするリストを返す
#files = os.listdir('.')


argvs=sys.argv
argc=len(argvs)
#if (argc != 3): 
#	print 'Usage: # python %s minclass maxclass filename(without extension)' % argvs[0]
#	quit()

dir_filelist=[] 		#modified /ファイルリスト作成
filelist=[]				#modified /ファイルリスト作成
if argc!=1:
	fw=open(argvs[1]+'csv','w')
else:
	fw=open('countswcvol.csv','w')
	
#ヘッダ入力
fw.write(' , , count0,count1,count2,count3,count4,count5,count6,count7\n')

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
				
				if (tmpname>8)&(tmpname[-8:]=='.new.swc'):
					dir_filelist.append(tmpname)		# modified 拡張子.new.swcならばリストに追加
					filelist.append(file)				# modified ファイル名のみも追加
			#print file		#デバック：ファイル名の出力
			#if file[-4:]=='.swc':					# modified ファイル名の取得
			#	filelist.append(file)
		#     print file
		swclist.append([root,file])
	return swclist
	
	
	
# SWC内cclassファイルカウント用
def CountNewSwc(inputfile):
	
	# リスト作成
	NEURON=[]
	comment=[]
	xlist=[]
	ylist=[]
	zlist=[]
	radilist=[]
	cclasslist=[]
	parlist=[]
	regeonlist=[]
	
	imlist=[]
	lrlist=[]
	swclist=[]
	
	swchist_l=np.zeros(8 , dtype=np.float64)	#配列の作成 データ型：倍精度 / ヒストグラム計算用
	swchist_r=np.zeros(8, dtype=np.float64)
	ID=0	#modified

	IDlist=[]									# ID保持用リストの作成

	#read swc
	print inputfile								# ファイル名の出力
	f=open(inputfile)							# ファイルの読み込み
	lines=f.readlines()
	
	
	# 倍精度浮動点小数の配列の作成 /by numpy 
	xarray=np.zeros(len(lines) , dtype=np.float64)	#配列の作成 データ型：倍精度 / x座標入力用
	yarray=np.zeros(len(lines) , dtype=np.float64)	#配列の作成 データ型：倍精度 / y座標入力用
	zarray=np.zeros(len(lines) , dtype=np.float64)	#配列の作成 データ型：倍精度 / z座標入力用
	rarray=np.zeros(len(lines) , dtype=np.float64)	#配列の作成 データ型：倍精度 / 直径入力用
	count = 0 										#カウント用変数
	for line in lines:
		if (len(line)==0):							# 長さ0のデータは読み飛ばす
			continue
		elif(line=='\n'):							# 改行コードのみの行も読み飛ばす
			continue
		elif line.startswith("#"):					# コメント行は読み飛ばす
			line=line[1:-1]
			#print line
			comment.append(line)
			continue  
		data=line[:-1].split(' ')					# 半角スペースによって文字列をリストへ分割
		ID=int(data[0])
		cclass=int(data[1])
		
		xarray[count]= np.float64(data[2])	#配列にデータを入力
		yarray[count]= np.float64(data[3])
		zarray[count]= np.float64(data[4])
		rarray[count]= np.float64(data[5])
		parent= int(data[6])
		
		count =count+1
		IDlist.append(ID)
		parlist.append(parent)
	
		# 各cclassの読み込み
	
		im_cclass =int(format(cclass,'b'),2) & int('1110000',2) # (1110000)_2 をマスクとして利用し、上位3ビット(処理による付与ラベル)を取り出す
		lr_cclass =int(format(cclass,'b'),2) & int('1000',2) # (1000)_2 をマスクとして利用し、第4ビット(右か左かの判定部分)を取り出す
		swc_cclass =int(format(cclass,'b'),2) & int('111',2) # (111)_2 をマスクとして利用し、下位3ビット(元のラベル)を取り出す
		
		imlist.append(im_cclass)
		lrlist.append(lr_cclass)
		swclist.append(swc_cclass)
	
	count=0				# カウンター変数
	for pc in parlist:			# parentのリストから読み込む
		for ic in IDlist:		# IDのリストから読み込む
			if pc==ic:			# parentとIDが等しければ計算する
				xdist=xarray[ic-1]-xarray[count]
				ydist=yarray[ic-1]-yarray[count]
				zdist=zarray[ic-1]-zarray[count]
				x2dist= math.pow(xarray[ic-1]-xarray[count],2)		# x軸方向の距離を求める
				y2dist= math.pow(yarray[ic-1]-yarray[count],2)		# y軸方向の距離を求める
				z2dist= math.pow(zarray[ic-1]-zarray[count],2)		# z軸方向の距離を求める
				dist=math.sqrt(x2dist+y2dist+z2dist)
				vol=dist*rarray[count]*rarray[count]*np.float64(math.pi)
				
				#print pc,count,xarray[ic-1],xarray[count],xarray[ic-1]-xarray[count],math.pow(xarray[ic-1]-xarray[count],2), yarray[count],yarray[ic-1]-yarray[count],math.pow(yarray[ic-1]-yarray[count],2),zarray[count],zarray[ic-1]-zarray[count],math.pow(zarray[ic-1]-zarray[count],2),dist,rarray[count],vol
				#print pc,count,math.pow(yarray[ic-1]-yarray[count],2),zarray[count],zarray[ic-1]-zarray[count],math.pow(zarray[ic-1]-zarray[count],2),dist,rarray[count],vol
				
				im_tmp=imlist[count] >>4			# 右へ4ビットシフト
				
				if im_tmp>0:					# 処理による付与されたラベルが存在する場合
					if lrlist[count]==0:			# さらに左のとき
						swchist_l[im_tmp]=swchist_l[im_tmp]+vol	#ヒストグラムの計算
						print'L', im_tmp,swchist_l[im_tmp]
					else:
						swchist_r[im_tmp]=swchist_r[im_tmp]+vol	# ヒストグラムの計算
						print 'R',im_tmp,swchist_r[im_tmp]			
		count=count+1

	
	fw.write(inputfile+',L')
	for si in range(0,len(swchist_l)):
		fw.write(','+str(swchist_l[si]))
	fw.write('\n')
	fw.write(' ,R')
	
	for si in range(0,len(swchist_r)):
		fw.write(','+str(swchist_r[si]))
	fw.write('\n')
	

	
# メイン関数
def main():

# ファイルとサブディレクトリのパスを表示する
 #path = '~/shrsmb/StandardBrain'
	
	path=r'./' #/home/kazawa/LAL-imgtest'	#パスの指定
	list=getswcfiles(path)
	#print dir_filelist		# modified デバック用
	#print filelist			# modified デバック用
	#print len(filelist)		# modified デバック用
	#print len(dir_filelist)
	
	for inputfile in dir_filelist:
		CountNewSwc(inputfile)
	fw.close

if __name__ == '__main__': main()