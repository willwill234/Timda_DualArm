#!/usr/bin/env python

import rospy
import moveit_commander
from moveit_msgs.msg import MoveItErrorCodes
from visp_hand2eye_calibration.msg import TransformArray
from math import pi, radians
from std_msgs.msg import String
from geometry_msgs.msg import Transform
from moveit_commander.conversions import pose_to_list
import tf
# from tf import transformations
from visp_hand2eye_calibration.msg import TransformArray
from tf.transformations import quaternion_from_euler, euler_from_quaternion
from flexbe_core import EventState, Logger
import numpy as np
from flexbe_core.proxy import ProxyActionClient
from geometry_msgs.msg import PointStamped
from moveit_msgs.msg import MoveGroupAction, MoveGroupGoal, Constraints, JointConstraint, MoveItErrorCodes ,MoveGroupActionResult
# from control_msgs.msg import FollowJointTrajectoryGoal, FollowJointTrajectoryAction, JointTrajectoryControllerState, FollowJointTrajectoryResult

'''
Created on 15.06.2015

@author: Philipp Schillinger
'''
class GenerateHandEyePoint(EventState):
	"""
	Output a fixed pose to move.

	<= done									   points has been created.
	<= fail									   create points fail.

	"""


	def __init__(self, base_link, tip_link, move_distance, group_name, reference_frame, cam_x, cam_y, cam_z , axis):
		'''
		Constructor
		'''
		self.move_distance = float(move_distance)
		self.base_link = base_link
		self.tip_link = tip_link
		self.tf_listener = tf.TransformListener()
		# self.tool_h_base = TransformArray()
		# self.times = int(times)
		self.points_x = []
		self.points_y = []
		self.points_z = []
		self.points_qw = []
		self.points_qx = []
		self.points_qy = []
		self.points_qz = []
		self.First_charuco_array = []
		self._group_name = group_name
		self._reference_frame = reference_frame
		self._move_group = moveit_commander.MoveGroupCommander(self._group_name)
		self._result = MoveItErrorCodes.FAILURE
		self._move_group.set_pose_reference_frame(self._reference_frame)
		self._end_effector_link = self._move_group.get_end_effector_link()
		self._current_pose = self._move_group.get_current_pose()
		self._origin_euler  = [0, 0, 0]
		self.base_rotation_x = 1
		self.base_rotation_y = 1
		self.base_rotation_z = 1
		self._axis = axis
		self.cam_axis_x = cam_x
		self.cam_axis_y = cam_y
		self.cam_axis_z = cam_z
		self.pan_vector = np.arange(1.0, 5.0).reshape(4,1)
		self.pan_martix = np.arange(1.0, 5.0).reshape(4,1)

	def execute(self, userdata):
		'''
		Execute this state
		'''
		try:
			(tool_trans_base, tool_rot_base) = self.tf_listener.lookupTransform(self.tip_link, self.base_link, rospy.Time(0))
		except (tf.LookupException, tf.ConnectivityException, tf.ExtrapolationException):
			rospy.logwarn('lookupTransform for robot failed!, ' + self.base_link + ', ' + self.tip_link)
			return
		print(tool_trans_base)
		print(tool_rot_base)
		tooltrans = tf.transformations.translation_matrix(tool_trans_base)
		toolrot = tf.transformations.quaternion_matrix(tool_rot_base)
		tool_h_base = np.matmul(tooltrans, toolrot)
		# print(tooltrans)
		# print(toolrot)
		# print(tool_h_base)
		# trans = Transform()
		# trans.translation.x = tool_trans_base[0]
		# trans.translation.y = tool_trans_base[1]
		# trans.translation.z = tool_trans_base[2]
		# trans.rotation.x = tool_rot_base[0]
		# trans.rotation.y = tool_rot_base[1]
		# trans.rotation.z = tool_rot_base[2]
		# trans.rotation.w = tool_rot_base[3]
		# self.tool_h_base.transforms.append(trans)
		self._current_pose = self._move_group.get_current_pose()

	



def callback(data):
	#rospy.loginfo(rospy.get_caller_id() + "I heard %s", data.result.planned_trajectory.joint_trajectory.points.positions)
	rospy.loginfo(rospy.get_caller_id() + "I heard %s", data.result.planned_trajectory.multi_dof_joint_trajectory.points)
	
def listener():

	# In ROS, nodes are uniquely named. If two nodes with the same
	# name are launched, the previous one is kicked off. The
	# anonymous=True flag means that rospy will choose a unique
	# name for our 'listener' node so that multiple listeners can
	# run simultaneously.
	rospy.init_node('listener', anonymous=True)

	rospy.Subscriber("move_group/result", MoveGroupActionResult, callback)

	# spin() simply keeps python from exiting until this node is stopped
	rospy.spin()




if __name__ == '__main__':
	start = GenerateHandEyePoint()
	start.execute()
	#position = rospy.Subscriber("move_group/result", MoveGroupActionResult, callback)
	#listener()
	#print("%s",position)




		

