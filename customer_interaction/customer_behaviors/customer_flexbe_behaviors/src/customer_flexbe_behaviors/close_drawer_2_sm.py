#!/usr/bin/env python
# -*- coding: utf-8 -*-
###########################################################
#               WARNING: Generated code!                  #
#              **************************                 #
# Manual changes may get lost if file is generated again. #
# Only code inside the [MANUAL] tags will be kept.        #
###########################################################

from flexbe_core import Behavior, Autonomy, OperatableStateMachine, ConcurrencyContainer, PriorityContainer, Logger
from dual_arm_flexbe_states.fixed_joint_move import FixedJointMoveState
from dual_arm_flexbe_states.fixed_pose_move import FixedPoseMoveState
from dual_arm_flexbe_states.init_robot import InitRobotState
from dual_arm_flexbe_states.robotiq_2f_gripper_state import Robotiq2FGripperState
# Additional imports can be added inside the following tags
# [MANUAL_IMPORT]

# [/MANUAL_IMPORT]


'''
Created on Mon Aug 23 2021
@author: Luis
'''
class close_drawer_2SM(Behavior):
	'''
	example for dual  arm to close drawer level2
	'''


	def __init__(self):
		super(close_drawer_2SM, self).__init__()
		self.name = 'close_drawer_2'

		# parameters of this behavior
		self.add_parameter('robot_name', 'right_arm')
		self.add_parameter('en_sim', False)
		self.add_parameter('default_speed', 20)

		# references to used behaviors

		# Additional initialization code can be added inside the following tags
		# [MANUAL_INIT]
		
		# [/MANUAL_INIT]

		# Behavior comments:



	def create(self):
		# x:889 y:300, x:326 y:41
		_state_machine = OperatableStateMachine(outcomes=['finished', 'failed'])

		# Additional creation code can be added inside the following tags
		# [MANUAL_CREATE]
		
		# [/MANUAL_CREATE]


		with _state_machine:
			# x:33 y:41
			OperatableStateMachine.add('init_right_arm',
										InitRobotState(robot_name='right_arm', en_sim=self.en_sim, speed=self.default_speed),
										transitions={'done': 'right_gripper_reset', 'failed': 'failed'},
										autonomy={'done': Autonomy.Off, 'failed': Autonomy.Off})

			# x:682 y:26
			OperatableStateMachine.add('back_home',
										FixedJointMoveState(robot_name='right_arm', en_sim=self.en_sim, speed=self.default_speed, slide_pos=0, joints=[0, 0, 0, 0, 0, 0 ,0]),
										transitions={'done': 'finished', 'failed': 'failed'},
										autonomy={'done': Autonomy.Off, 'failed': Autonomy.Off})

			# x:502 y:294
			OperatableStateMachine.add('grab_drawer',
										Robotiq2FGripperState(robot_name='right_arm', en_sim=self.en_sim, gripper_cmd=140),
										transitions={'done': 'pull_drawer'},
										autonomy={'done': Autonomy.Off})

			# x:30 y:249
			OperatableStateMachine.add('initial',
										FixedJointMoveState(robot_name=self.robot_name, en_sim=self.en_sim, speed=self.default_speed, slide_pos=0, joints=[0.0, -68.75, 0.0, 107.14, 0.0, -49.85, 0.0]),
										transitions={'done': 'prepare_pose', 'failed': 'failed'},
										autonomy={'done': Autonomy.Off, 'failed': Autonomy.Off})

			# x:268 y:307
			OperatableStateMachine.add('prepare_pose',
										FixedPoseMoveState(robot_name=self.robot_name, en_sim=self.en_sim, mode='p2p', speed=self.default_speed, pos=[0.5, -0.126, -0.685], euler=[48.0, 90.0, 0.0], phi=0),
										transitions={'done': 'arrive_drawer', 'failed': 'failed'},
										autonomy={'done': Autonomy.Off, 'failed': Autonomy.Off})

			# x:503 y:217
			OperatableStateMachine.add('pull_drawer',
										FixedPoseMoveState(robot_name=self.robot_name, en_sim=self.en_sim, mode='line', speed=self.default_speed, pos=[0.5, -0.216, -0.685], euler=[48.0, 90.0, 0.0], phi=0),
										transitions={'done': 'right_gripper_open', 'failed': 'failed'},
										autonomy={'done': Autonomy.Off, 'failed': Autonomy.Off})

			# x:28 y:173
			OperatableStateMachine.add('right_gripper_active',
										Robotiq2FGripperState(robot_name='right_arm', en_sim=self.en_sim, gripper_cmd='active'),
										transitions={'done': 'initial'},
										autonomy={'done': Autonomy.Off})

			# x:497 y:136
			OperatableStateMachine.add('right_gripper_open',
										Robotiq2FGripperState(robot_name='right_arm', en_sim=self.en_sim, gripper_cmd='open'),
										transitions={'done': 'safety_back'},
										autonomy={'done': Autonomy.Off})

			# x:29 y:108
			OperatableStateMachine.add('right_gripper_reset',
										Robotiq2FGripperState(robot_name='right_arm', en_sim=self.en_sim, gripper_cmd='reset'),
										transitions={'done': 'right_gripper_active'},
										autonomy={'done': Autonomy.Off})

			# x:684 y:236
			OperatableStateMachine.add('safety_back',
										FixedPoseMoveState(robot_name='right_arm', en_sim=self.en_sim, mode='line', speed=self.default_speed, pos=[0.4, -0.216, -0.685], euler=[48.0, 90.0, 0.0], phi=0),
										transitions={'done': 'safety_back_home', 'failed': 'failed'},
										autonomy={'done': Autonomy.Off, 'failed': Autonomy.Off})

			# x:684 y:124
			OperatableStateMachine.add('safety_back_home',
										FixedJointMoveState(robot_name='right_arm', en_sim=self.en_sim, speed=self.default_speed, slide_pos=-0.1, joints=[25.87, -36.32, 0.00, 142.23, -65.00, -96.87, -14.38]),
										transitions={'done': 'back_home', 'failed': 'failed'},
										autonomy={'done': Autonomy.Off, 'failed': Autonomy.Off})

			# x:497 y:374
			OperatableStateMachine.add('arrive_drawer',
										FixedPoseMoveState(robot_name=self.robot_name, en_sim=self.en_sim, mode='line', speed=self.default_speed, pos=[0.7, -0.216, -0.685], euler=[48.0, 90.0, 0.0], phi=0),
										transitions={'done': 'grab_drawer', 'failed': 'failed'},
										autonomy={'done': Autonomy.Off, 'failed': Autonomy.Off})


		return _state_machine


	# Private functions can be added inside the following tags
	# [MANUAL_FUNC]
	
	# [/MANUAL_FUNC]
