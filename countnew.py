# coding: utf-8
import os, os.path # osモジュールのインポート
import sys

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
	fw=open('countswc.csv','w')
	
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
	
	swchist_l=[0]*8
	swchist_r=[0]*8
	ID=0	#modified

	#read swc
	print inputfile
	f=open(inputfile)
	lines=f.readlines()
	for line in lines:
		if (len(line)==0):
			continue
		elif(line=='\n'):
			continue
		elif line.startswith("#"):
			line=line[1:-1]
			#print line
			comment.append(line)
			continue  
		data=line[:-1].split(' ')
		ID=int(data[0])

		# 各cclassの読み込み
		cclass=int(data[1])					#整数型で読み込み
		im_cclass =int(format(cclass,'b'),2) & int('1110000',2) # (1110000)_2 をマスクとして利用し、上位3ビット(処理による付与ラベル)を取り出す
		lr_cclass =int(format(cclass,'b'),2) & int('1000',2) # (1000)_2 をマスクとして利用し、第4ビット(右か左かの判定部分)を取り出す
		swc_cclass =int(format(cclass,'b'),2) & int('111',2) # (111)_2 をマスクとして利用し、下位3ビット(元のラベル)を取り出す
		
		imlist.append(im_cclass)
		lrlist.append(lr_cclass)
		swclist.append(swc_cclass)
		
	
		#print im_cclass, lr_cclass
		
		
		#print ID,cclass,format(cclass,'b'), format(im_cclass,'b'),format(lr_cclass,'b'),format(swc_cclass,'b')
	
	
	for si in range(0,len(imlist)):
		im_tmp=imlist[si] >>4			# 右へ4ビットシフト
		#print im_tmp,imlist[si]
		if im_tmp>0:					# 処理による付与されたラベルが存在する場合
			#print im_tmp
			if lrlist[si]==0:				# 右か左かの判定 (0のとき左)
				swchist_l[im_tmp]=swchist_l[im_tmp]+1
			else:
			
				swchist_r[im_tmp]=swchist_r[im_tmp]+1
	
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
	
	path=r'./' #/home/kazawa/LAL-imgtest'	#パスのｓ亭
	list=getswcfiles(path)
	#print dir_filelist		# modified デバック用
	#print filelist			# modified デバック用
	#print len(filelist)		# modified デバック用
	#print len(dir_filelist)
	
	for inputfile in dir_filelist:
		CountNewSwc(inputfile)
	fw.close

if __name__ == '__main__': main()