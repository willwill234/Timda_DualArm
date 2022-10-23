from flexbe_core.proxy import ProxySubscriberCached, ProxyPublisher
import rospy
from enum import IntEnum
from flexbe_core import EventState
from std_msgs.msg import String

class Status(IntEnum):
    idle             = 0
    busy_on_clean    = 1
    busy_on_service    = 2
    failed_to_arrive = 3
    finish           = 4


class ArmState(EventState):
    '''
    Wait for timda_mobile to Goal.

    -- en_sim					bool			Use real robot or Gazebo

    <= done 									Robot move done.
    <= failed 									Robot move failed.
    '''
    
    def __init__(self):
        '''
        Constructor
        '''
        super(ArmState, self).__init__(outcomes=['check_clean', 'check_service', 'finish'],output_keys=['arm_state'])

        self.status = Status.idle
        self.__set_pubSub()

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
        if 'Start Clean Task' in msg.data:
            self.status = Status.busy_on_clean
        elif 'Start Customer Service' in msg.data:
            self.status = Status.busy_on_service
        elif 'All Done!' in msg.data:
            self.status = Status.finish


    
    def execute(self, userdata):
        '''
        Execute this state
        '''
        if self.__arm_task_state_sub.has_msg(self.arm_task_state_topic):
            msg = self.__arm_task_state_sub.get_last_msg(self.arm_task_state_topic)
            userdata.arm_state = String()
            userdata.arm_state.data = msg
            self.__status_callback(msg)

        if self.status == Status.busy_on_clean:
            return 'check_clean'
        elif self.status == Status.busy_on_service:
            return 'check_service'
        elif self.status == Status.finish:
            return 'finish'

    def on_enter(self, userdata):
        self.status = Status.idle
        self.__arm_task_state_sub.remove_last_msg(self.arm_task_state_topic)

        

