#!/usr/bin/env python
# -*- coding: utf-8 -*-
###########################################################
#               WARNING: Generated code!                  #
#              **************************                 #
# Manual changes may get lost if file is generated again. #
# Only code inside the [MANUAL] tags will be kept.        #
###########################################################

from flexbe_core import Behavior, Autonomy, OperatableStateMachine, ConcurrencyContainer, PriorityContainer, Logger
from customer_flexbe_states.customer_request import CustomerRequest
from flexbe_states.wait_state import WaitState
# Additional imports can be added inside the following tags
# [MANUAL_IMPORT]

# [/MANUAL_IMPORT]


'''
Created on Fri Aug 27 2021
@author: Luis
'''
class customer_requestSM(Behavior):
	'''
	example for test service bell
	'''


	def __init__(self):
		super(customer_requestSM, self).__init__()
		self.name = 'customer_request'

		# parameters of this behavior

		# references to used behaviors

		# Additional initialization code can be added inside the following tags
		# [MANUAL_INIT]
		
		# [/MANUAL_INIT]

		# Behavior comments:



	def create(self):
		# x:30 y:365, x:130 y:365
		_state_machine = OperatableStateMachine(outcomes=['finished', 'failed'])

		# Additional creation code can be added inside the following tags
		# [MANUAL_CREATE]
		
		# [/MANUAL_CREATE]


		with _state_machine:
			# x:144 y:84
			OperatableStateMachine.add('customer_req',
										CustomerRequest(port_name='/dev/ttyUSB0', baud=115200),
										transitions={'finish': 'finished', 'done': 'wait_state', 'failed': 'failed'},
										autonomy={'finish': Autonomy.Off, 'done': Autonomy.Off, 'failed': Autonomy.Off})

			# x:334 y:74
			OperatableStateMachine.add('wait_state',
										WaitState(wait_time=0.1),
										transitions={'done': 'customer_req'},
										autonomy={'done': Autonomy.Off})


		return _state_machine


	# Private functions can be added inside the following tags
	# [MANUAL_FUNC]
	
	# [/MANUAL_FUNC]
