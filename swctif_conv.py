# coding: utf-8
import os, os.path # osモジュールのインポート
import sys

# swcファイルをFiji/ ImageJ とプラグインNeuroRegisterを用いてマルチページtifへと変更するプログラム

dir_filelist=[]
filelist=[]

fijidir=r'/home/kazawa/Fiji.app/ImageJ-linux32'		# Fiji/ImageJの指定
localdir=r'/home/kazawa/sakamoto/'					# カレントディレクトリの指定


f=open('swc_tif.ijm','w')			# マクロ用ファイルの作成

argvs=sys.argv
argc=len(argvs)
if (argc != 7): 
	print 'Usage: # python %s imagewidth imageheight imagedepth pixelwidth pixelheight pixeldepth' % argvs[0]
	quit()

WIDTH=argvs[1]
HEIGHT=argvs[2]
DEPTH=argvs[3]
PWIDTH=argvs[4]
PHEIGHT=argvs[5]
PDEPTH=argvs[6]
	

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
				
				#if (tmpname>8)&(tmpname[-8:]=='.new.swc'):
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
	
	#SWCFILE = localdir+inputfile.replace('.\\\\','')	#windows
	SWCFILE = localdir+inputfile.replace('./','')		#unix
	#tmp = inputfile.replace('.\\\\','')					#windows
	tmp = inputfile.replace('./','')					#unix
	TIFFILE = localdir+tmp[:-4]+'.tif'
	str1='run(\"SWC Tools\", \"open=SWCFILE imagewidth=WIDTH imageheight=HEIGHT imagedepth=DEPTH pixelwidth=PWIDTH pixelheight=PHEIGHT pixeldepth=PDEPTH\");'
	str2='saveAs(\"Tiff\", \"TIFFILE\");'
	str3='close();'
	str1 = str1.replace('SWCFILE',SWCFILE) 
	str1 = str1.replace('PWIDTH',str(PWIDTH)) 
	str1 = str1.replace('PHEIGHT',str(PHEIGHT)) 
	str1 = str1.replace('PDEPTH',str(PDEPTH)) 
	str1 = str1.replace('WIDTH',str(WIDTH)) 
	str1 = str1.replace('HEIGHT',str(HEIGHT)) 
	str1 = str1.replace('DEPTH',str(DEPTH)) 
	str1 = str1.replace('\\','\\\\')					# windows用
	str2 = str2.replace('TIFFILE',TIFFILE) 
	str2 = str2.replace('\\','\\\\')					# windows用
	
	
	#print str1
	#print str2
	#print str3
	print SWCFILE
	
	f.write(str1)
	f.write('\n')
	f.write(str2)
	f.write('\n')
	f.write(str3)
	f.write('\n')
	
	
	
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
		CountNewSwc(inputfile)
	
	f.write('run(\"Quit\");')
	f.close()
	
	command = fijidir +' swc_tif.ijm'			#fiji による実行
	os.system(command)

if __name__ == '__main__': main()




