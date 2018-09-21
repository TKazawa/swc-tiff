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
			if tmpname[-4:]=='.tif':				# modified 拡張子.swcの検出
				
				dir_filelist.append(tmpname)		# modified 拡張子.new.swcならばリストに追加
				filelist.append(file)				# modified ファイル名のみも追加
			#print file		#デバック：ファイル名の出力
			#if file[-4:]=='.swc':					# modified ファイル名の取得
			#	filelist.append(file)
		#     print file
		swclist.append([root,file])
	return swclist
	
	
def Conv3d2d(inputfile):				# 3d -> 2dコンバート用関数
	print inputfile+ '  processing...'
	tif=Image.open(inputfile)			# 画像ファイルを開く
	print tif.info						# TIFF画像の詳細情報の表示
	tif.seek(0)							# マルチページの1枚目を開く


	nx = tif.size[0]					# 画像のx,yサイズの入力
	ny = tif.size[1]

	nz=1								# 深さにおいては初期化(枚数の関係で+1)

	try:								# マルチページの情報取得
		while 1:
			tif.seek(tif.tell()+1)		# マルチページを1枚ずづ進める
			nz = nz +1 	
	except EOFError:
		pass

#nz=3 
#nx=5
#ny=4

	outimage_xy=Image.new('L',( nx, ny ))	# 出力用画像の作成 x-y
	outimage_xz=Image.new('L',( nx, nz ))	# x-z
	outimage_yz=Image.new('L',( ny,nz ))	# y-z

	tif.seek(0)									# マルチページを１枚目に
	pixeldata=np.zeros((nz,ny,nx), dtype=int)	# 出力用の配列を作成 全体
	outpixel_xy=np.zeros((ny,nx), dtype=int)	# 出力用の配列を作成 x-y
	outpixel_xz=np.zeros((nz,nx), dtype=int)	# 出力用の配列を作成 x-z
	outpixel_yz=np.zeros((nz,ny), dtype=int)	# 出力用の配列を作成 y-z
	count=0

# calculate 'x-y data'

	
	#print pixeldata
	zi=0								# z方向は初期化

	try:								# マルチページの情報取得
		while 1:	
			for yi in range(0,ny):
				for xi in range(0,nx):
					pixeldata[zi][yi][xi]=tif.getpixel ((xi,yi))
					if (pixeldata[zi][yi][xi]>outpixel_xy[yi][xi]):		# 配列のピクセル値が、保管用の配列ピクセル値より大きな場合
						
						outpixel_xy[yi][xi]=pixeldata[zi][yi][xi]		# ピクセルの値を置き換える
			tif.seek(tif.tell()+1)
			print 'step1:'+str(zi)+'/'+str(nz)							# デバッグ：途中経過表示
			zi = zi+1
	except EOFError:
		pass


#print pixeldata	#結果を出力する

# calculate 'x-z data'		/ 全体をループさせて断面配列を作成 -> 最大ピクセル数を出力する
	for yi in range(0,ny):
		for xi in range(0,nx):
			for zi in range(0,nz):
				if (pixeldata[zi][yi][xi]>outpixel_xz[zi][xi]):
					outpixel_xz[zi][xi]=pixeldata[zi][yi][xi]
		print 'step2:'+str(yi)+'/'+str(ny)							# デバッグ：途中経過表示
			

# calculate 'y-z data'	/ 全体をループさせて断面配列を作成 -> 最大ピクセル数を出力する
	for xi in range(0,nx):
		for yi in range(0,ny):
			for zi in range(0,nz):
				if (pixeldata[zi][yi][xi]>outpixel_yz[zi][yi]):
					outpixel_yz[zi][yi]=pixeldata[zi][yi][xi]
		print 'step2:'+str(xi)+'/'+str(nx)							# デバッグ：途中経過表示



	outimage_xy=Image.fromarray(np.uint8(outpixel_xy))		# 画像の変換
	outimage_xz=Image.fromarray(np.uint8(outpixel_xz))
	outimage_yz=Image.fromarray(np.uint8(outpixel_yz))
	outimage_xy.save( inputfile[:-4]+'_xy_.tiff', 'tiff' )	# 画像の保存
	outimage_xz.save( inputfile[:-4]+'_xz_.tiff', 'tiff' )	# 
	outimage_yz.save( inputfile[:-4]+'_yz_.tiff', 'tiff' )		
	


# メイン関数
def main():

# ファイルとサブディレクトリのパスを表示する
 #path = '~/shrsmb/StandardBrain'
	
	path=r'./'	 #Unix用
	#path=r'.\\' #windows用
	list=getswcfiles(path)
	#print dir_filelist		# modified デバック用
	#print filelist			# modified デバック用
	#print len(filelist)		# modified デバック用
	#print len(dir_filelist)
	
	for inputfile in dir_filelist:
		Conv3d2d(inputfile)
	

if __name__ == '__main__': main()




