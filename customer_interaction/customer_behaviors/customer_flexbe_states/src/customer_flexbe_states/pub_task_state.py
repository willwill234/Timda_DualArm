#!/usr/bin/env python

import rospy
import tf,time
from flexbe_core import EventState
from flexbe_core.proxy import ProxyPublisher, ProxySubscriberCached

from std_msgs.msg import String
from enum import IntEnum

class Status(IntEnum):
	idle        = 0
	busy        = 1
	finish      = 2

class PubTaskState(EventState):
	'''
	Publish the task state 
    -- arm_task_state           string          Robots task state

	<= done 									Robot move done.
	<= failed 									Robot move failed.
	'''


	def __init__(self, arm_task_state):
		'''
		Constructor
		'''
		super(PubTaskState, self).__init__(outcomes=['done'])

		self.arm_task_state = arm_task_state
		self.status = Status.idle
		self.__set_pubSub()

	def __set_pubSub(self):
		self.arm_task_state_topic = '/arm_task_state'
		self.__arm_task_state_pub = ProxyPublisher({
		    self.arm_task_state_topic:
		    String})



	def pub_task_state(self):
		msg = self.arm_task_state
		if 'Start' and 'Clean' in msg:
			self.status = Status.finish
			self.__arm_task_state_pub.publish(self.arm_task_state_topic, msg)
		elif 'End' and 'Clean' in msg:
			self.status = Status.finish
			self.__arm_task_state_pub.publish(self.arm_task_state_topic, msg)
		elif 'Start' and 'Customer Service' in msg:
			self.status = Status.finish
			self.__arm_task_state_pub.publish(self.arm_task_state_topic, msg)
		elif 'End' and 'Customer Service' in msg:
			self.status = Status.finish
			self.__arm_task_state_pub.publish(self.arm_task_state_topic, msg)
		elif 'End' and 'Pick Order' in msg:
			self.status = Status.finish
			self.__arm_task_state_pub.publish(self.arm_task_state_topic, msg)
		elif 'End' and 'Realease Order' in msg:
			self.status = Status.finish
			self.__arm_task_state_pub.publish(self.arm_task_state_topic, msg)
		# elif 'Start' and 'Customer Service' in msg:
		# 	self.status = Status.finish
		# 	self.__arm_task_state_pub.publish(self.arm_task_state_topic, msg)
		# elif 'Start' and 'Customer Service' in msg:
		# 	self.status = Status.finish
		# 	self.__arm_task_state_pub.publish(self.arm_task_state_topic, msg)
		else:
			self.status = Status.finish

	def execute(self, userdata):
		self.pub_task_state()
		'''
		Execute this state
		'''
		if self.status == Status.finish:
			return 'done'


	def on_enter(self, userdata):
		time.sleep(0.2)
		self.status = Status.idle
		self.pub_task_state()
		
