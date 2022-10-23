#!/usr/bin/env python
# -*- coding: utf-8 -*-
###########################################################
#               WARNING: Generated code!                  #
#              **************************                 #
# Manual changes may get lost if file is generated again. #
# Only code inside the [MANUAL] tags will be kept.        #
###########################################################

from flexbe_core import Behavior, Autonomy, OperatableStateMachine, ConcurrencyContainer, PriorityContainer, Logger
from customer_flexbe_states.get_ar_marker import GetArMarker
from customer_flexbe_states.recive_and_trans_to_arm import ReciveAndTransToArm
from dual_arm_flexbe_states.IK_move import IKMoveState as dual_arm_flexbe_states__IKMoveState
from dual_arm_flexbe_states.fixed_pose_move import FixedPoseMoveState
from dual_arm_flexbe_states.init_robot import InitRobotState
# Additional imports can be added inside the following tags
# [MANUAL_IMPORT]

# [/MANUAL_IMPORT]


'''
Created on Wed Aug 25 2021
@author: Luis
'''
class test_ar_markerSM(Behavior):
	'''
	example for test ar_marker
	'''


	def __init__(self):
		super(test_ar_markerSM, self).__init__()
		self.name = 'test_ar_marker'

		# parameters of this behavior
		self.add_parameter('en_sim', True)
		self.add_parameter('default_speed', 100)

		# references to used behaviors

		# Additional initialization code can be added inside the following tags
		# [MANUAL_INIT]
		
		# [/MANUAL_INIT]

		# Behavior comments:



	def create(self):
		# x:555 y:136, x:290 y:28
		_state_machine = OperatableStateMachine(outcomes=['finished', 'failed'])

		# Additional creation code can be added inside the following tags
		# [MANUAL_CREATE]
		
		# [/MANUAL_CREATE]


		with _state_machine:
			# x:52 y:64
			OperatableStateMachine.add('init_robot',
										InitRobotState(robot_name='right_arm', en_sim=self.en_sim, speed=self.default_speed),
										transitions={'done': 'init_to_perpare', 'failed': 'failed'},
										autonomy={'done': Autonomy.Off, 'failed': Autonomy.Off})

			# x:36 y:206
			OperatableStateMachine.add('init_to_perpare',
										FixedPoseMoveState(robot_name='right_arm', en_sim=self.en_sim, mode='p2p', speed=self.default_speed, pos=[0.38, -0.2, -0.1], euler=[0.0 ,65.0 ,0.0], phi=0),
										transitions={'done': 'get_ar_marker', 'failed': 'failed'},
										autonomy={'done': Autonomy.Off, 'failed': Autonomy.Off})

			# x:332 y:294
			OperatableStateMachine.add('move_to_object',
										dual_arm_flexbe_states__IKMoveState(robot_name='right_arm', en_sim=self.en_sim, speed=self.default_speed),
										transitions={'done': 'trans_to_arm_base', 'failed': 'failed'},
										autonomy={'done': Autonomy.Off, 'failed': Autonomy.Off},
										remapping={'robot_cmd': 'robot_cmd'})

			# x:444 y:28
			OperatableStateMachine.add('trans_to_arm_base',
										ReciveAndTransToArm(robot_side='right', speed=self.default_speed, en_sim=self.en_sim),
										transitions={'done': 'move_to_object', 'finish': 'finished'},
										autonomy={'done': Autonomy.Off, 'finish': Autonomy.Off},
										remapping={'ar_marker_info': 'ar_marker_info', 'robot_cmd': 'robot_cmd'})

			# x:35 y:329
			OperatableStateMachine.add('get_ar_marker',
										GetArMarker(robot_side='right'),
										transitions={'done': 'trans_to_arm_base', 'failed': 'failed'},
										autonomy={'done': Autonomy.Off, 'failed': Autonomy.Off},
										remapping={'ar_marker_info': 'ar_marker_info'})


		return _state_machine


	# Private functions can be added inside the following tags
	# [MANUAL_FUNC]
	
	# [/MANUAL_FUNC]
