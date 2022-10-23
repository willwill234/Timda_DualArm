#!/usr/bin/env python
# -*- coding: utf-8 -*-
###########################################################
#               WARNING: Generated code!                  #
#              **************************                 #
# Manual changes may get lost if file is generated again. #
# Only code inside the [MANUAL] tags will be kept.        #
###########################################################

from flexbe_core import Behavior, Autonomy, OperatableStateMachine, ConcurrencyContainer, PriorityContainer, Logger
from customer_flexbe_behaviors.close_drawer_2_sm import close_drawer_2SM
from customer_flexbe_states.arm_state import ArmState
# Additional imports can be added inside the following tags
# [MANUAL_IMPORT]

# [/MANUAL_IMPORT]


'''
Created on Thu Aug 19 2021
@author: Luis
'''
class CustomerService_orderSM(Behavior):
	'''
	dual arm customer service order task behaviors
	'''


	def __init__(self):
		super(CustomerService_orderSM, self).__init__()
		self.name = 'Customer Service_order'

		# parameters of this behavior
		self.add_parameter('en_sim', False)

		# references to used behaviors
		self.add_behavior(close_drawer_2SM, 'close_drawer_2')

		# Additional initialization code can be added inside the following tags
		# [MANUAL_INIT]
		
		# [/MANUAL_INIT]

		# Behavior comments:



	def create(self):
		# x:725 y:300, x:684 y:79
		_state_machine = OperatableStateMachine(outcomes=['finished', 'failed'])

		# Additional creation code can be added inside the following tags
		# [MANUAL_CREATE]
		
		# [/MANUAL_CREATE]


		with _state_machine:
			# x:141 y:115
			OperatableStateMachine.add('arm_state',
										ArmState(),
										transitions={'check_clean': 'arm_state', 'check_service': 'close_drawer_2', 'finish': 'finished'},
										autonomy={'check_clean': Autonomy.Off, 'check_service': Autonomy.Off, 'finish': Autonomy.Off})

			# x:390 y:317
			OperatableStateMachine.add('close_drawer_2',
										self.use_behavior(close_drawer_2SM, 'close_drawer_2'),
										transitions={'finished': 'arm_state', 'failed': 'failed'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit})


		return _state_machine


	# Private functions can be added inside the following tags
	# [MANUAL_FUNC]
	
	# [/MANUAL_FUNC]
