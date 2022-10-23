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
# Additional imports can be added inside the following tags
# [MANUAL_IMPORT]

# [/MANUAL_IMPORT]


'''
Created on Wed Aug 26 2021
@author: Luis
'''
class test_arSM(Behavior):
	'''
	example for test ar_marker
	'''


	def __init__(self):
		super(test_arSM, self).__init__()
		self.name = 'test_ar'

		# parameters of this behavior
		self.add_parameter('en_sim', True)
		self.add_parameter('default_speed', 100)

		# references to used behaviors

		# Additional initialization code can be added inside the following tags
		# [MANUAL_INIT]
		
		# [/MANUAL_INIT]

		# Behavior comments:



	def create(self):
		# x:555 y:136, x:139 y:258
		_state_machine = OperatableStateMachine(outcomes=['finished', 'failed'])

		# Additional creation code can be added inside the following tags
		# [MANUAL_CREATE]
		
		# [/MANUAL_CREATE]


		with _state_machine:
			# x:59 y:67
			OperatableStateMachine.add('get_ar_marker',
										GetArMarker(robot_side='right'),
										transitions={'done': 'tran_to _arm_base', 'failed': 'failed'},
										autonomy={'done': Autonomy.Off, 'failed': Autonomy.Off},
										remapping={'ar_marker_info': 'ar_marker_info'})

			# x:370 y:242
			OperatableStateMachine.add('tran_to _arm_base',
										ReciveAndTransToArm(robot_side='right', speed=self.default_speed, en_sim=self.en_sim),
										transitions={'done': 'finished', 'finish': 'finished'},
										autonomy={'done': Autonomy.Off, 'finish': Autonomy.Off},
										remapping={'ar_marker_info': 'ar_marker_info', 'robot_cmd': 'robot_cmd'})


		return _state_machine


	# Private functions can be added inside the following tags
	# [MANUAL_FUNC]
	
	# [/MANUAL_FUNC]
