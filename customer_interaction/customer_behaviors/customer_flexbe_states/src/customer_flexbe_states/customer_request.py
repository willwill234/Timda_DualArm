#!/usr/bin/env python

import rospkg, rospy
import numpy as np
import serial 
from enum import IntEnum
from customer_interaction_msgs.srv import TimdaMode , TimdaModeResponse
from diagnostic_msgs.srv import AddDiagnostics, AddDiagnosticsResponse
from flexbe_core import EventState, Logger
from flexbe_core.proxy import ProxyServiceCaller, ProxySubscriberCached, ProxyPublisher
from std_msgs.msg import String

class Status(IntEnum):
    idle                        = 0
    ready_to_service            = 1
    ready_to_clean              = 2
    # nav_to_shelf                = 1
    # nav_to_Table1               = 2
    # nav_to_Table2               = 3
    start_clean                 = 3
    start_customer_request      = 4
    busy_on_customer_request    = 5
    busy_on_clean               = 6
    finish                      = 7


class CustomerRequest(EventState):
    '''
    Publishes a table number to robot so that it can reach the table.

    -- port_name 	string 	    which port of NodeMCU is used.
    -- baud 	    int 	    which baud of NodeMCU is used.

    <= finish 			task finish.
    <= fail				program unnormal shutdown. 

    '''

    def __init__(self, port_name, baud):
        # Declare outcomes, input_keys, and output_keys by calling the super constructor with the corresponding arguments.
        super(CustomerRequest, self).__init__(outcomes = ['finish', 'done', 'failed'])
        self.status = Status.idle
        self.list_ser = []
        self.ser = serial.Serial(port_name, baud) 
        self.__set_pubSub()
        self.wifi_module_service = 'Timda_mobile'
        self.wifi_module_client = ProxyServiceCaller({self.wifi_module_service: TimdaMode})
        self.customer_order_service = rospy.Service('customer_order', AddDiagnostics, self.adddiagnosticsresponse)
        self.timda_mobile_resp = TimdaModeResponse()
        self.timda_mobile_req = TimdaMode()
        self.order = str()
        self.order_feedback = AddDiagnosticsResponse()
        self.arm_state = String()

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
        if 'Ready to Service' in msg.data:
            self.status = Status.ready_to_service
            rospy.loginfo('Ready!')
            # msg.data = 'Processing'
            # self.__arm_task_state_pub.publish(self.arm_task_state_topic, msg)
        elif 'Ready to Clean' in msg.data:
            self.status = Status.ready_to_clean
            # rospy.loginfo('Ready!')
            # msg.data = 'Processing'
            # self.__arm_task_state_pub.publish(self.arm_task_state_topic, msg)
        elif 'Start Clean Task' in msg.data:
            self.status = Status.finish
            rospy.loginfo('Start Clean Task!')
            # msg.data = 'Processing'
            # self.__arm_task_state_pub.publish(self.arm_task_state_topic, msg)
        elif 'End Clean Task' in msg.data:
            self.status = Status.idle
            rospy.logwarn('End Clean Task')
            # msg.data = 'Processing'
            # self.__arm_task_state_pub.publish(self.arm_task_state_topic, msg)
        elif 'Start Customer Service' in msg.data:
            self.status = Status.finish
            rospy.loginfo('Start Customer Service!')
            # msg.data = 'Processing'
            # self.__arm_task_state_pub.publish(self.arm_task_state_topic, msg)
        elif 'End Customer Service' in msg.data:
            self.status = Status.idle
            rospy.logwarn('End Customer Service')
            # msg.data = 'Processing'
            # self.__arm_task_state_pub.publish(self.arm_task_state_topic, msg)
        elif 'End Pick Order' in msg.data:
            self.status = Status.busy_on_customer_request
            rospy.logwarn('Pick Order complete')
            # msg.data = 'Processing'
            # self.__arm_task_state_pub.publish(self.arm_task_state_topic, msg)
        elif 'End Release Order' in msg.data:
            self.status = Status.busy_on_customer_request
            rospy.logwarn('Release Order complete')
            # msg.data = 'Processing'
            # self.__arm_task_state_pub.publish(self.arm_task_state_topic, msg)
        # else:
        #     self.status = Status.idle
        #     rospy.logwarn('Ready to Service!')
            

    def adddiagnosticsresponse(self, request):
        self.arm_state.data = 'Ready to Service'
        self.__arm_task_state_pub.publish(self.arm_task_state_topic, self.arm_state.data)
        print(self.status)
        self.order = request.load_namespace
        self.order_feedback.success=True
        self.order_feedback.message="Recieve Order, Please Wait a minute"
        return  self.order_feedback

    def execute(self, userdata):
        if not self.wifi_module_client.is_available(self.wifi_module_service):
            return 'fail'
        if self.__arm_task_state_sub.has_msg(self.arm_task_state_topic):
            msg = self.__arm_task_state_sub.get_last_msg(self.arm_task_state_topic)
            self.__status_callback(msg)
        if self.ser.in_waiting:
            self.list_ser.append(self.ser.read(1))
        if not self.ser.in_waiting:      
            if self.status==Status.idle:
                self.arm_state.data = 'Ready to Clean'
                self.__arm_task_state_pub.publish(self.arm_task_state_topic, self.arm_state.data)    
            if len(self.list_ser) >= 3  and self.status == Status.ready_to_clean:
                if self.list_ser[0] == 's' and self.list_ser[2] == 'e':
                    print(self.list_ser)
                    table_num = str(ord(self.list_ser[1]))
                    
                    try:
                        if table_num == "1":
                            self.timda_mobile_req = "Table1"
                            self.timda_mobile_resp = self.wifi_module_client.call(self.wifi_module_service, self.timda_mobile_req)
                            self.arm_state.data = 'Start Clean Task'
                            self.__arm_task_state_pub.publish(self.arm_task_state_topic, self.arm_state.data)
                        else:
                            self.timda_mobile_req = "Table2"
                            self.timda_mobile_resp = self.wifi_module_client.call(self.wifi_module_service, self.timda_mobile_req)
                            self.arm_state.data = 'Start Clean Task'
                            self.__arm_task_state_pub.publish(self.arm_task_state_topic, self.arm_state.data)
                        print(self.timda_mobile_resp.nav_res)
                    except rospy.ServiceException as e:
                        print ("Service call failed: %s" % e)
                    
                    del self.list_ser [:]
                else:
                    del self.list_ser [:]
            elif self.status == Status.ready_to_service:
                    self.timda_mobile_req = "shelf"
                    self.timda_mobile_resp = self.wifi_module_client.call(self.wifi_module_service, self.timda_mobile_req)
                    self.arm_state.data ='Start Customer Service'
                    self.__arm_task_state_pub.publish(self.arm_task_state_topic, self.arm_state.data)
                    self.status = Status.finish
            elif self.status == Status.busy_on_customer_request:
                print(self.order)
                if 'table1' in self.order:
                    self.timda_mobile_req = "Table1"
                    self.timda_mobile_resp = self.wifi_module_client.call(self.wifi_module_service, self.timda_mobile_req)
                    self.status = Status.finish
                    self.order = ''
                elif'table2' in self.order:
                    self.timda_mobile_req = "Table2"
                    self.timda_mobile_resp = self.wifi_module_client.call(self.wifi_module_service, self.timda_mobile_req)
                    self.status = Status.finish
                    self.order = ''
        # while not rospy.is_shutdown():
        #     rospy.logwarn(self.order)
            # if self.__arm_task_state_sub.has_msg(self.arm_task_state_topic):
            #     msg = self.__arm_task_state_sub.get_last_msg(self.arm_task_state_topic)
            #     self.__status_callback(msg)

            # while self.ser.in_waiting:      
            #     self.list_ser.append(self.ser.read(1))

            # if self.status==Status.idle:
            #     self.arm_state.data = 'Ready to Clean'
            #     self.__arm_task_state_pub.publish(self.arm_task_state_topic, self.arm_state.data)    
            # if len(self.list_ser) >= 3  and self.status == Status.ready_to_clean:
            #     if self.list_ser[0] == 's' and self.list_ser[2] == 'e':
            #         print(self.list_ser)
            #         table_num = str(ord(self.list_ser[1]))
                    
            #         try:
            #             if table_num == "1":
            #                 self.timda_mobile_req = "Table1"
            #                 self.timda_mobile_resp = self.wifi_module_client.call(self.wifi_module_service, self.timda_mobile_req)
            #                 self.arm_state.data = 'Start Clean Task'
            #                 self.__arm_task_state_pub.publish(self.arm_task_state_topic, self.arm_state.data)
            #             else:
            #                 self.timda_mobile_req = "Table2"
            #                 self.timda_mobile_resp = self.wifi_module_client.call(self.wifi_module_service, self.timda_mobile_req)
            #                 self.arm_state.data = 'Start Clean Task'
            #                 self.__arm_task_state_pub.publish(self.arm_task_state_topic, self.arm_state.data)
            #             print(self.timda_mobile_resp.nav_res)
            #         except rospy.ServiceException as e:
            #             print ("Service call failed: %s" % e)
                    
            #         del self.list_ser [:]
            #     else:
            #         del self.list_ser [:]
            # elif self.status == Status.ready_to_service:
            #         self.timda_mobile_req = "shelf"
            #         self.timda_mobile_resp = self.wifi_module_client.call(self.wifi_module_service, self.timda_mobile_req)
            #         self.status = Status.finish
            # elif self.status == Status.busy_on_Customer_request:
            #     if 'table1' in self.order:
            #         self.timda_mobile_req = "Table1"
            #         self.timda_mobile_resp = self.wifi_module_client.call(self.wifi_module_service, self.timda_mobile_req)
            #         self.status = Status.finish
            #         self.order = ''
            #     elif'table2' in self.order:
            #         self.timda_mobile_req = "Table2"
            #         self.timda_mobile_resp = self.wifi_module_client.call(self.wifi_module_service, self.timda_mobile_req)
            #         self.status = Status.finish
            #         self.order = ''
            # elif 'table1' in self.order:
            #     if self.status == Status.idle:
            #         self.timda_mobile_req = "shelf"
            #         self.timda_mobile_resp = self.wifi_module_client.call(self.wifi_module_service, self.timda_mobile_req)
            #         self.status = Status.ready
            #     elif self.status == Status.busy_on_Customer_request:
            #         self.timda_mobile_req = "Table1"
            #         self.timda_mobile_resp = self.wifi_module_client.call(self.wifi_module_service, self.timda_mobile_req)
            #         self.status = Status.idle
            #         self.order = ''
            # elif 'table2' in self.order:
            #     if self.status == Status.idle:
            #         self.timda_mobile_req = "shelf"
            #         self.timda_mobile_resp = self.wifi_module_client.call(self.wifi_module_service, self.timda_mobile_req)
            #         self.status = Status.ready
            #     elif self.status == Status.busy_on_Customer_request:
            #         self.timda_mobile_req = "Table2"
            #         self.timda_mobile_resp = self.wifi_module_client.call(self.wifi_module_service, self.timda_mobile_req)
            #         self.status = Status.ready
            #         self.order = ''
                elif self.order == 'shutdown':
                    self.ser.close()
                    self.__arm_task_state_pub.publish(self.arm_task_state_topic, 'All Done!')
                    self.ser.close()
                    return 'finish'
                elif self.status == Status.finish:
                    return 'done'
            # rospy.spin()
        # self.ser.close()    
        # print('good bye!')
        # return 'finish'

    def on_enter(self, userdata):
        self.__arm_task_state_sub.remove_last_msg(self.arm_task_state_topic)
        self.status = Status.idle
