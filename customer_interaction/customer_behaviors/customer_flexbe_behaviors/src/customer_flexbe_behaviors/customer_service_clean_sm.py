#!/usr/bin/env python
# -*- coding: utf-8 -*-
###########################################################
#               WARNING: Generated code!                  #
#              **************************                 #
# Manual changes may get lost if file is generated again. #
# Only code inside the [MANUAL] tags will be kept.        #
###########################################################

from flexbe_core import Behavior, Autonomy, OperatableStateMachine, ConcurrencyContainer, PriorityContainer, Logger
from customer_flexbe_behaviors.clean_task_sm import CleanTaskSM
from customer_flexbe_states.arm_state import ArmState
from customer_flexbe_states.music_state import MusicState
from customer_flexbe_states.pub_task_state import PubTaskState
# Additional imports can be added inside the following tags
# [MANUAL_IMPORT]

# [/MANUAL_IMPORT]


'''
Created on Thu Aug 19 2021
@author: Luis
'''
class CustomerService_CleanSM(Behavior):
	'''
	dual arm customer service clean task behaviors
	'''


	def __init__(self):
		super(CustomerService_CleanSM, self).__init__()
		self.name = 'Customer Service_Clean'

		# parameters of this behavior
		self.add_parameter('en_sim', False)

		# references to used behaviors
		self.add_behavior(CleanTaskSM, 'Clean Task')

		# Additional initialization code can be added inside the following tags
		# [MANUAL_INIT]
		
		# [/MANUAL_INIT]

		# Behavior comments:



	def create(self):
		# x:609 y:62, x:682 y:300
		_state_machine = OperatableStateMachine(outcomes=['finished', 'failed'])

		# Additional creation code can be added inside the following tags
		# [MANUAL_CREATE]
		
		# [/MANUAL_CREATE]

		# x:30 y:365, x:130 y:365
		_sm_start_clean_0 = OperatableStateMachine(outcomes=['finished', 'failed'])

		with _sm_start_clean_0:
			# x:45 y:149
			OperatableStateMachine.add('play_music',
										MusicState(),
										transitions={'finish': 'finished'},
										autonomy={'finish': Autonomy.Off})

			# x:305 y:150
			OperatableStateMachine.add('pub_task_state',
										PubTaskState(arm_task_state='Start Clean Task'),
										transitions={'done': 'finished'},
										autonomy={'done': Autonomy.Off})


		# x:30 y:365, x:130 y:365
		_sm_end_clean_1 = OperatableStateMachine(outcomes=['finished', 'failed'])

		with _sm_end_clean_1:
			# x:42 y:164
			OperatableStateMachine.add('stop_music',
										MusicState(),
										transitions={'finish': 'finished'},
										autonomy={'finish': Autonomy.Off})

			# x:299 y:182
			OperatableStateMachine.add('pub_task_state',
										PubTaskState(arm_task_state='End Clean Task'),
										transitions={'done': 'finished'},
										autonomy={'done': Autonomy.Off})



		with _state_machine:
			# x:102 y:49
			OperatableStateMachine.add('arm_state',
										ArmState(),
										transitions={'check_clean': 'start_clean', 'check_service': 'arm_state', 'finish': 'finished'},
										autonomy={'check_clean': Autonomy.Off, 'check_service': Autonomy.Off, 'finish': Autonomy.Off},
										remapping={'arm_state': 'arm_state'})

			# x:344 y:211
			OperatableStateMachine.add('end_clean',
										_sm_end_clean_1,
										transitions={'finished': 'arm_state', 'failed': 'failed'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit})

			# x:43 y:293
			OperatableStateMachine.add('start_clean',
										_sm_start_clean_0,
										transitions={'finished': 'Clean Task', 'failed': 'failed'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit})

			# x:127 y:423
			OperatableStateMachine.add('Clean Task',
										self.use_behavior(CleanTaskSM, 'Clean Task'),
										transitions={'finished': 'end_clean', 'failed': 'failed'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit})


		return _state_machine


	# Private functions can be added inside the following tags
	# [MANUAL_FUNC]
	
	# [/MANUAL_FUNC]
