#coding=utf-8  
import os,json  
  
#指定掃描的歌曲目錄，生成index.list  
# path = '~/Desktop/music/'  
path = os.path.abspath((os.path.dirname(__file__)))+'/' 
dirs = os.listdir(path)  
support = ['.mp3','.ogg']  #可用此兩種格式音樂
filelist = []  
for file in dirs:  
    filename = os.path.splitext(file)  
    if filename[-1] in support:  
        filelist.append(path + file)  
        print(file)  
with open('index.list', 'w') as index:  
    index.write(json.dumps(filelist))  