#!/usr/bin/env python
#coding=utf-8  
import time,pygame,threading,os,json  
volume = 0.50000000  
statelist = [0,0]  

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


#Music Playing  
with open('index.list','r') as index:  
    filelist = json.loads(index.read())  
    print(filelist)  
lens = len(filelist)  
filePlaying = 0  
pygame.mixer.init()  
track = pygame.mixer.music.load(filelist[filePlaying])  #歌曲讀取
pygame.mixer.music.set_volume(volume)  #音量預設
pygame.mixer.music.play()  #音樂播放
pause=1  
####   main function  ####
# 播放狀態
def playpause():  
    global pause  #全域變數
    while True:
        try:  
            if pause == 0:  
                print('pause music')  
                pygame.mixer.music.pause()  
                pause=1  
            else:  
                print('resume music')  
                pygame.mixer.music.unpause()  
                pause=0  
            break  
        except:
            print("error")

# def playpause():  
#     global pause  #全域變數
#     while True:  
#         while GPIO.event_detected(pinPlay):  #觸發事件偵測
#             while GPIO.event_detected(pinPlay) == 0:  
#                 if pause == 0:  
#                     print('pause music')  
#                     pygame.mixer.music.pause()  
#                     pause=1  
#                 else:  
#                     print('resume music')  
#                     pygame.mixer.music.unpause()  
#                     pause=0  
#                 break  
#             time.sleep(1)  
#         time.sleep(1)  
  
# # 音量調整功能
def volume():  
        global volume   #全域變數
        volume = 0.5  
        while True:  
            i=0  
            # for pinSingle in pinVolume:  
            #     statelist[i] = GPIO.event_detected(pinSingle)  #觸發事件偵測
            #     i=i+1  
        #    print('Volume keys state',statelist)  
            if statelist[0]==True:   #音量調大觸發事件偵測
                print('volume up')  
                volume = volume + 0.1  
                if volume > 1.0:  
                    volume = 1.0  
                print('volume value:',volume)  
            if statelist[1]==True:  #音量調小觸發事件偵測
                print('volume down')  
                volume = volume - 0.1  
                if volume < 0.0:  
                    volume = 0.0  
                print('volume value:',str(round(volume*10)))  #round浮點數的四捨五入值
            pygame.mixer.music.set_volume(volume)  
            time.sleep(0.5)  
  
#  歌曲切換功能
def switch():  
    global filePlaying,track,pause  #全域變數
    while True:  
        filePlayingchk = filePlaying  
        if pygame.mixer.music.get_busy() == 0 :  # 判斷是否在播放音樂,本功能為歌曲播放完至下首
            filePlaying = filePlaying + 1  
        # else:  
        #     if GPIO.event_detected(pinNext) == 1  :  #下一首觸發事件偵測
        #         while GPIO.event_detected(pinNext) == 0:  #彈跳
        #             filePlaying = filePlaying + 1  
        #             break  
        #     if GPIO.event_detected(pinPrev) == 1  :  #上一首大觸發事件偵測
        #         while GPIO.event_detected(pinPrev) == 0:  #彈跳
        #             filePlaying = filePlaying - 1  
        #             break  
        if filePlaying < 0:  
            filePlaying = lens -1  
        elif filePlaying > lens -1:  
            filePlaying = 0  
        if filePlayingchk != filePlaying :  
            track = pygame.mixer.music.load(filelist[filePlaying])  
            pygame.mixer.music.play()  # 播放
            pause = 0  
            print(filePlaying + 1,filelist[filePlaying])  #輸出歌名
        time.sleep(0.5)  
#Muti-threads  多執行緒宣告
threads=[]  
t1 = threading.Thread(target=playpause)  
threads.append(t1)  
t2 = threading.Thread(target=volume)  
threads.append(t2)  
t3 = threading.Thread(target=switch)  
threads.append(t3)  
  
print('Wait......')  
print(filePlaying + 1,filelist[filePlaying])  
if __name__ == '__main__':  
    for t in threads:  
        t.setDaemon(True)  
        t.start()  
    t.join()  

## pygame 功能列表
# pygame.init() 進行全部模組的初始化，
# pygame.mixer.init() 或者只初始化音訊部分
# pygame.mixer.music.load(‘xx.mp3’) 使用檔名作為引數載入音樂 ,音樂可以是ogg、mp3等格式。載入的音樂不會全部放到內容中，而是以流的形式播放的，即在播放的時候才會一點點從檔案中讀取。
# pygame.mixer.music.play()播放載入的音樂。該函式立即返回，音樂播放在後臺進行。
# play方法還可以使用兩個引數
# pygame.mixer.music.play(loops=0, start=0.0) loops和start分別代表重複的次數和開始播放的位置。
# pygame.mixer.music.stop() 停止播放，
# pygame.mixer.music.pause() 暫停播放。
# pygame.mixer.music.unpause() 取消暫停。
# pygame.mixer.music.fadeout(time) 用來進行淡出，在time毫秒的時間內音量由初始值漸變為0，最後停止播放。
# pygame.mixer.music.set_volume(value) 來設定播放的音量，音量value的範圍為0.0到1.0。
# pygame.mixer.music.get_busy() 判斷是否在播放音樂,返回1為正在播放。
# pygame.mixer.music.set_endevent(pygame.USEREVENT 1) 在音樂播放完成時，用事件的方式通知使用者程式，設定當音樂播放完成時傳送pygame.USEREVENT 1事件給使用者程式。
# pygame.mixer.music.queue(filename) 使用指定下一個要播放的音樂檔案，當前的音樂播放完成後自動開始播放指定的下一個。一次只能指定一個等待播放的音樂檔案。