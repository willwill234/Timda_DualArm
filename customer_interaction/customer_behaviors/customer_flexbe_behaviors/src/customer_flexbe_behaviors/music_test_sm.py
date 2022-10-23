#!/usr/bin/env python
# -*- coding: utf-8 -*-
###########################################################
#               WARNING: Generated code!                  #
#              **************************                 #
# Manual changes may get lost if file is generated again. #
# Only code inside the [MANUAL] tags will be kept.        #
###########################################################

from flexbe_core import Behavior, Autonomy, OperatableStateMachine, ConcurrencyContainer, PriorityContainer, Logger
from customer_flexbe_states.music_state import MusicState
from customer_flexbe_states.pub_task_state import PubTaskState
# Additional imports can be added inside the following tags
# [MANUAL_IMPORT]

# [/MANUAL_IMPORT]


'''
Created on Sun Aug 22 2021
@author: Luis
'''
class music_testSM(Behavior):
	'''
	test music state
	'''


	def __init__(self):
		super(music_testSM, self).__init__()
		self.name = 'music_test'

		# parameters of this behavior

		# references to used behaviors

		# Additional initialization code can be added inside the following tags
		# [MANUAL_INIT]
		
		# [/MANUAL_INIT]

		# Behavior comments:



	def create(self):
		# x:629 y:51, x:311 y:378
		_state_machine = OperatableStateMachine(outcomes=['finished', 'failed'])

		# Additional creation code can be added inside the following tags
		# [MANUAL_CREATE]
		
		# [/MANUAL_CREATE]

		# x:30 y:365, x:130 y:365, x:230 y:365
		_sm_start_0 = ConcurrencyContainer(outcomes=['finished', 'failed'], conditions=[
										('finished', [('play', 'finish'), ('pub_state', 'done')])
										])

		with _sm_start_0:
			# x:25 y:137
			OperatableStateMachine.add('play',
										MusicState(),
										transitions={'finish': 'finished'},
										autonomy={'finish': Autonomy.Off})

			# x:259 y:140
			OperatableStateMachine.add('pub_state',
										PubTaskState(arm_task_state='Start Clean Task'),
										transitions={'done': 'finished'},
										autonomy={'done': Autonomy.Off})


		# x:30 y:365, x:130 y:365, x:230 y:365
		_sm_end_1 = ConcurrencyContainer(outcomes=['finished', 'failed'], conditions=[
										('finished', [('end_play', 'finish'), ('pub_state', 'done')])
										])

		with _sm_end_1:
			# x:41 y:128
			OperatableStateMachine.add('end_play',
										MusicState(),
										transitions={'finish': 'finished'},
										autonomy={'finish': Autonomy.Off})

			# x:307 y:121
			OperatableStateMachine.add('pub_state',
										PubTaskState(arm_task_state='End Clean Task'),
										transitions={'done': 'finished'},
										autonomy={'done': Autonomy.Off})



		with _state_machine:
			# x:72 y:122
			OperatableStateMachine.add('start',
										_sm_start_0,
										transitions={'finished': 'end', 'failed': 'failed'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit})

			# x:343 y:108
			OperatableStateMachine.add('end',
										_sm_end_1,
										transitions={'finished': 'finished', 'failed': 'failed'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit})


		return _state_machine


	# Private functions can be added inside the following tags
	# [MANUAL_FUNC]
	
	# [/MANUAL_FUNC]
