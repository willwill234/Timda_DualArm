from flexbe_core.proxy import ProxySubscriberCached, ProxyPublisher 
# from strategy.msg import TimdaMobileStatus
import rospy
from enum import IntEnum
from flexbe_core import EventState
import time,pygame,threading,os,json
from rospy.core import rospyinfo  
from std_msgs.msg import String


class Status(IntEnum):
    idle                        = 0
    start_clean                 = 1
    start_customer_request      = 2
    play_music                  = 3
    busy_on_customer_request    = 4
    busy_on_clean               = 5
    end_music                   = 6
    finish                      = 7


class MusicState(EventState):
    '''
    Choose music to play.

    <= done 									Robot move done.
    <= failed 									Robot move failed.
    '''
    
    def __init__(self):
        '''
        Constructor
        '''
        super(MusicState, self).__init__(outcomes=['finish'])

        self.volume = 0.50000000
        self.status = Status.idle
        self.__set_pubSub()
        # self.pause = 0
        self.statelist = [0,0]
        self.lens = 0  
        self.status = Status.idle
        self.filelist = []
        self.filePlaying = 0

        
    def __set_pubSub(self):
        self.arm_task_state_topic = '/arm_task_state'
        self.__arm_task_state_sub = ProxySubscriberCached({
            self.arm_task_state_topic:
            String})

        self.arm_task_state_topic = '/arm_task_state'
        self.__arm_task_state_pub = ProxyPublisher({
            self.arm_task_state_topic:
            String})

    def __status_callback(self, msg):
        if 'Start Clean Task' in msg.data and self.status != Status.play_music :
            self.status = Status.start_clean
            self.filePlaying = 1
            pygame.mixer.music.load(self.filelist[self.filePlaying])
            pygame.mixer.music.play()
            self.status = Status.play_music
            time.sleep(2)
            pygame.mixer.music.stop()
            self.filePlaying = 3
            pygame.mixer.music.load(self.filelist[self.filePlaying])
            pygame.mixer.music.play()
            rospy.loginfo('Music Playing!')
        elif 'End Clean Task' in msg.data:
            self.status = Status.end_music
            self.filePlaying = 2
            pygame.mixer.music.load(self.filelist[self.filePlaying])
            pygame.mixer.music.play()
            time.sleep(2)
            rospy.logwarn('Music Stop')
        elif 'Start Customer Service' in msg.data and self.status != Status.start_customer_request:
            self.status = Status.start_customer_request
            self.filePlaying = 1
            pygame.mixer.music.load(self.filelist[self.filePlaying])
            pygame.mixer.music.play()
            self.status = Status.play_music
            time.sleep(2)
            pygame.mixer.music.stop()
            self.filePlaying = 3
            pygame.mixer.music.load(self.filelist[self.filePlaying])
            pygame.mixer.music.play()
            rospy.loginfo('Music Playing!')
        elif 'End Customer Service' in msg.data:
            self.status = Status.end_music
            self.filePlaying = 0
            pygame.mixer.music.load(self.filelist[self.filePlaying])
            pygame.mixer.music.play()
            time.sleep(2)
            rospy.logwarn('Music Stop')
        elif 'All Done!' in msg.data:
            self.status = Status.finish
        else:
            rospy.logwarn('Music Playing!')


    def scan_music(self):
        path = os.path.abspath(os.path.join(os.path.dirname(__file__),os.path.pardir))+'/music/'
        dirs = os.listdir(path)  
        support = ['.mp3','.ogg']   
        for file in dirs:  
            filename = os.path.splitext(file)  
            if filename[-1] in support:  
                self.filelist.append(path + file)  
                print(file)
        with open('index.list', 'w') as index:  
            index.write(json.dumps(self.filelist))



    def execute(self, userdata):
        '''
        Execute this state
        '''
        if self.__arm_task_state_sub.has_msg(self.arm_task_state_topic):
            # if 'Start' in str(userdata.arm_state.data):
            #     self.__arm_task_state_pub.publish(self.arm_task_state_topic, userdata.arm_state.data)
            msg = self.__arm_task_state_sub.get_last_msg(self.arm_task_state_topic)
            print(msg)
            self.__status_callback(msg)
        # if self.status == Status.play_music:
        #     return 'finish'
        # elif self.status == Status.end_music:
        #     pygame.mixer.music.stop()
        #     return 'finish'
        # elif self.status == Status.finish:
        #     pygame.mixer.music.stop()
        #     return 'finish'
        # # if self.status == Status.finish:
        # # 	pygame.mixer.music.stop()
        # # 	return 'finish'
        # # elif self.status == Status.end_music:
        # # 	pygame.mixer.music.stop()
        # # 	return 'done'
        if self.status == Status.play_music:
            return 'finish'
        elif self.status == Status.end_music:
            pygame.mixer.music.stop()
            return 'finish'

    def on_enter(self, userdata):
        time.sleep(1)
        # self.__arm_task_state_sub.remove_last_msg(self.arm_task_state_topic)
        self.status = Status.idle
        # self.scan_music()
        with open('index.list','r') as index:  
            self.filelist = json.loads(index.read())  
            print(self.filelist)  
        self.lens = len(self.filelist)  
        self.filePlaying = 0  
        pygame.mixer.init()  
        self.track = pygame.mixer.music.load(self.filelist[self.filePlaying])  
        pygame.mixer.music.set_volume(self.volume)  

        print('Wait......')  
        

        
