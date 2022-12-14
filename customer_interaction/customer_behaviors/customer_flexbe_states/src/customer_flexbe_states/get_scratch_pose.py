#!/usr/bin/env python

from flexbe_core import EventState, Logger
from arm_control import Command

right_c_pose = [[[-0.16, -0.1920, -0.50500],  [-44.024, 0.005, 4.498], 0],
                [[ 0.50, -0.0263, -0.50500],  [46.024, 20.005, 4.998], 0],
                [[ 0.50, -0.0263, -0.62500],  [46.024, 20.005, 4.998], 0],
                [[ 0.20, -0.0263, -0.62500],  [46.024, 20.005, 4.998], 0],
                [[ 0.60, -0.2000, -0.50500],  [46.024, 20.005, 4.998], 0],
                [[ 0.60, -0.2000, -0.62500],  [46.024, 20.005, 4.998], 0],
                [[ 0.20, -0.2000, -0.62500],  [46.024, 20.005, 4.998], 0],
                [[ 0.20, -0.2063, -0.50500],  [46.024, 20.005, 4.998], 0]]
left_c_pose = [[[-0.255, 0.3363, -0.50500],   [-45.0, 0.0, 0.0], 0],
                [[-0.25, 0.3563, -0.50500],   [-45.0, 20.0, 0.0], 0],
                [[ 0.50, 0.2000, -0.56500],  [-45.0, 20.0, 0.0], 0],
                [[ 0.50, 0.2000, -0.62500],  [-45.0, 20.0, 0.0], 0],
                [[ 0.20, 0.2000, -0.62500],  [-45.0, 20.0, 0.0], 0],
                [[ 0.50, 0.0500, -0.50500], [-45.0, 20.0, 0.0], 0],
                [[ 0.50, 0.0500, -0.62500], [-45.0, 20.0, 0.0], 0],
                [[ 0.20, 0.0500, -0.62500], [-45.0, 20.0, 0.0], 0],
                [[ 0.20, 0.3300, -0.62500], [-45.0, 0.0, 0.0], 0],
                [[-0.255, 0.3363, -0.5050],  [-45.0, 0.0, 0.0], 0]]
c_pose = {'left_arm' :left_c_pose,
          'right_arm': right_c_pose}

class GetScratchPose(EventState):
	"""
	Publishes a pose from userdata so that it can be execute.

	-- robot_name              string          Robots name to move

	#> robot_cmd               command(dict)   See arm_task.py

	<= done									   Pose has been published.
	<= finish								   Task finished

	"""
	
	def __init__(self, robot_name):
		"""Constructor"""
		super(GetScratchPose, self).__init__(outcomes=['done', 'finish'], output_keys=['robot_cmd'])
		self.robot_name = robot_name
		self.move_mode = 'line'
		self.total_pose = len(c_pose[self.robot_name])
		self.pose_indx = 0

	def execute(self, userdata):
		if self.pose_indx == self.total_pose:
			return 'finish'
		else:
			userdata.robot_cmd = Command()
			userdata.robot_cmd['mode'] = 'line'
			userdata.robot_cmd['speed'] = 50
			userdata.robot_cmd['pos'] = c_pose[self.robot_name][self.pose_indx][0]
			userdata.robot_cmd['euler'] = c_pose[self.robot_name][self.pose_indx][1]
			userdata.robot_cmd['phi'] = c_pose[self.robot_name][self.pose_indx][2]
			return 'done'
	
	def on_enter(self, userdata):
		self.pose_indx += 1
			
