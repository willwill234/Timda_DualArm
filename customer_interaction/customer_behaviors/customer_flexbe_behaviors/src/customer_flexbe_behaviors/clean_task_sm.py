#!/usr/bin/env python
# -*- coding: utf-8 -*-
###########################################################
#               WARNING: Generated code!                  #
#              **************************                 #
# Manual changes may get lost if file is generated again. #
# Only code inside the [MANUAL] tags will be kept.        #
###########################################################

from flexbe_core import Behavior, Autonomy, OperatableStateMachine, ConcurrencyContainer, PriorityContainer, Logger
from customer_flexbe_behaviors.scratch_desk_left_sm import scratch_desk_leftSM
from customer_flexbe_behaviors.scratch_desk_right_sm import scratch_desk_rightSM
from customer_flexbe_behaviors.wipe_task_left_sm import wipe_task_leftSM
from customer_flexbe_behaviors.wipe_task_right_sm import wipe_task_rightSM
from customer_flexbe_states.pub_task_state import PubTaskState
# Additional imports can be added inside the following tags
# [MANUAL_IMPORT]

# [/MANUAL_IMPORT]


'''
Created on Thu Aug 19 2021
@author: Luis
'''
class CleanTaskSM(Behavior):
	'''
	dual arm clean task behaviors
	'''


	def __init__(self):
		super(CleanTaskSM, self).__init__()
		self.name = 'Clean Task'

		# parameters of this behavior
		self.add_parameter('en_sim', False)

		# references to used behaviors
		self.add_behavior(scratch_desk_leftSM, 'scratch_task/scratch_desk_left')
		self.add_behavior(scratch_desk_rightSM, 'scratch_task/scratch_desk_right')
		self.add_behavior(wipe_task_leftSM, 'wipe_task/wipe_task_left')
		self.add_behavior(wipe_task_rightSM, 'wipe_task/wipe_task_right')

		# Additional initialization code can be added inside the following tags
		# [MANUAL_INIT]
		
		# [/MANUAL_INIT]

		# Behavior comments:



	def create(self):
		# x:725 y:300, x:399 y:40
		_state_machine = OperatableStateMachine(outcomes=['finished', 'failed'])

		# Additional creation code can be added inside the following tags
		# [MANUAL_CREATE]
		
		# [/MANUAL_CREATE]

		# x:30 y:365, x:130 y:365, x:230 y:365, x:330 y:365
		_sm_wipe_task_0 = ConcurrencyContainer(outcomes=['finished', 'failed'], conditions=[
										('finished', [('wipe_task_left', 'finished'), ('wipe_task_right', 'finished')]),
										('failed', [('wipe_task_left', 'failed'), ('wipe_task_right', 'failed')])
										])

		with _sm_wipe_task_0:
			# x:50 y:102
			OperatableStateMachine.add('wipe_task_right',
										self.use_behavior(wipe_task_rightSM, 'wipe_task/wipe_task_right'),
										transitions={'finished': 'finished', 'failed': 'failed'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit})

			# x:293 y:103
			OperatableStateMachine.add('wipe_task_left',
										self.use_behavior(wipe_task_leftSM, 'wipe_task/wipe_task_left'),
										transitions={'finished': 'finished', 'failed': 'failed'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit})


		# x:30 y:365, x:130 y:365, x:230 y:365, x:330 y:365
		_sm_scratch_task_1 = ConcurrencyContainer(outcomes=['finished', 'failed'], conditions=[
										('finished', [('scratch_desk_left', 'finished'), ('scratch_desk_right', 'finished')]),
										('failed', [('scratch_desk_left', 'failed'), ('scratch_desk_right', 'failed')])
										])

		with _sm_scratch_task_1:
			# x:68 y:92
			OperatableStateMachine.add('scratch_desk_left',
										self.use_behavior(scratch_desk_leftSM, 'scratch_task/scratch_desk_left'),
										transitions={'finished': 'finished', 'failed': 'failed'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit})

			# x:321 y:88
			OperatableStateMachine.add('scratch_desk_right',
										self.use_behavior(scratch_desk_rightSM, 'scratch_task/scratch_desk_right'),
										transitions={'finished': 'finished', 'failed': 'failed'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit})



		with _state_machine:
			# x:167 y:169
			OperatableStateMachine.add('scratch_task',
										_sm_scratch_task_1,
										transitions={'finished': 'wipe_task', 'failed': 'failed'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit})

			# x:403 y:236
			OperatableStateMachine.add('wipe_task',
										_sm_wipe_task_0,
										transitions={'finished': 'pub_stask_state', 'failed': 'failed'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit})

			# x:653 y:107
			OperatableStateMachine.add('pub_stask_state',
										PubTaskState(arm_task_state='End Clean Task'),
										transitions={'done': 'finished'},
										autonomy={'done': Autonomy.Off})


		return _state_machine


	# Private functions can be added inside the following tags
	# [MANUAL_FUNC]
	
	# [/MANUAL_FUNC]
