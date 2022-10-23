#!/usr/bin/env python

from turtle import position
import rospy
import numpy as np
import moveit_commander
from moveit_msgs.msg import MoveItErrorCodes
from math import pi, radians
from std_msgs.msg import String
import geometry_msgs.msg
from moveit_commander.conversions import pose_to_list
from tf import transformations as tf


from flexbe_core import EventState, Logger

from flexbe_core.proxy import ProxyActionClient

from moveit_msgs.msg import MoveGroupAction, MoveGroupGoal, Constraints, JointConstraint, MoveItErrorCodes
# from control_msgs.msg import FollowJointTrajectoryGoal, FollowJointTrajectoryAction, JointTrajectoryControllerState, FollowJointTrajectoryResult

'''
Created on 15.06.2015

@author: Philipp Schillinger
'''

class MoveitToJointExecuteState(EventState):
	'''
	Move robot by planned trajectory.

	-- group_name         string      move group name

	># joint_trajectory             JointTrajectory  planned trajectory

	<= done 						Robot move done.
	<= failed 						Robot move failed.
	<= collision 				    Robot during collision.
	'''


	def __init__(self, group_name,reference_frame, action_topic = '/move_group'):
		'''
		Constructor
		'''
		super(MoveitToJointExecuteState, self).__init__(outcomes=['done', 'collision'],
											input_keys=['joint_config'],
											output_keys=['result_compute'])
		# group_name = ""
		self._group_name = group_name
		self._reference_frame = reference_frame
		self._move_group = moveit_commander.MoveGroupCommander(self._group_name)
		self._result = MoveItErrorCodes.FAILURE
		self._move_group.set_pose_reference_frame(self._reference_frame)
		self._end_effector_link = self._move_group.get_end_effector_link()
		self._move_group.set_end_effector_link(self._end_effector_link)
		self._move_group.set_max_acceleration_scaling_factor(0.1)
		self._move_group.set_max_velocity_scaling_factor(0.1)
		self._action_topic = action_topic
		self._trajectory_constraints = MoveGroupAction('move_group/result',position)
		self._client  = ProxyActionClient({self._action_topic: MoveGroupAction})
		self.points_num  = 0
		self.execute_num = 0
		self._execute_times = 0

	def stop(self):
		pass

	def execute(self, userdata):
		'''
		Execute this state
		'''
		print("")
		print("==================================================================")
		print(self._result)
		print("==================================================================")
		print("")
		self.points_num = np.size(userdata.hand_eye_points['x'])
		pose_goal = geometry_msgs.msg.Pose()
		pose_goal.position.x    = userdata.hand_eye_points['x'][self.execute_num]
		pose_goal.position.y    = userdata.hand_eye_points['y'][self.execute_num]   
		pose_goal.position.z    = userdata.hand_eye_points['z'][self.execute_num]
		pose_goal.orientation.x = userdata.hand_eye_points['qx'][self.execute_num]
		pose_goal.orientation.y = userdata.hand_eye_points['qy'][self.execute_num]
		pose_goal.orientation.z = userdata.hand_eye_points['qz'][self.execute_num]
		pose_goal.orientation.w = userdata.hand_eye_points['qw'][self.execute_num]
		# raw_input()
		self._move_group.set_pose_target(pose_goal, self._end_effector_link)
		self._result = self._move_group.go(wait=True)
		self._move_group.stop()
		self._move_group.clear_pose_targets()
		userdata.result_compute = self._execute_times >= self.points_num-1	

		if userdata.result_compute:
			pose_goal.position.x    = userdata.hand_eye_points['x'][0]
			pose_goal.position.y    = userdata.hand_eye_points['y'][0]   
			pose_goal.position.z    = userdata.hand_eye_points['z'][0]
			pose_goal.orientation.x = userdata.hand_eye_points['qx'][0]
			pose_goal.orientation.y = userdata.hand_eye_points['qy'][0]
			pose_goal.orientation.z = userdata.hand_eye_points['qz'][0]
			pose_goal.orientation.w = userdata.hand_eye_points['qw'][0]
			self._move_group.set_pose_target(pose_goal, self._end_effector_link)
			self._result = self._move_group.go(wait=True)
			self._move_group.stop()
			self._move_group.clear_pose_targets()
		if self._result == MoveItErrorCodes.SUCCESS:
			self.execute_num += 1
			return 'done'
			
		elif self._result == MoveItErrorCodes.MOTION_PLAN_INVALIDATED_BY_ENVIRONMENT_CHANGE:
			return 'collision'
		# else:
		# 	return 'failed'

	def on_enter(self, userdata):
		print("%f",self.trajectory_constraints)
		self._execute_times += 1
		pass

	def on_stop(self):
		pass

	def on_pause(self):
		pass

	def on_resume(self, userdata):
		self.on_enter(userdata)
