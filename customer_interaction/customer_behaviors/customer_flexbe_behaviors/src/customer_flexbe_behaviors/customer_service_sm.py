#!/usr/bin/env python
# -*- coding: utf-8 -*-
###########################################################
#               WARNING: Generated code!                  #
#              **************************                 #
# Manual changes may get lost if file is generated again. #
# Only code inside the [MANUAL] tags will be kept.        #
###########################################################

from flexbe_core import Behavior, Autonomy, OperatableStateMachine, ConcurrencyContainer, PriorityContainer, Logger
from customer_flexbe_behaviors.customer_service_clean_sm import CustomerService_CleanSM
# Additional imports can be added inside the following tags
# [MANUAL_IMPORT]

# [/MANUAL_IMPORT]


'''
Created on Thu Aug 19 2021
@author: Luis
'''
class CustomerServiceSM(Behavior):
	'''
	dual arm customer service behaviors
	'''


	def __init__(self):
		super(CustomerServiceSM, self).__init__()
		self.name = 'Customer Service'

		# parameters of this behavior
		self.add_parameter('en_sim', False)

		# references to used behaviors
		self.add_behavior(CustomerService_CleanSM, 'Customer_Service/Customer Service_Clean')

		# Additional initialization code can be added inside the following tags
		# [MANUAL_INIT]
		
		# [/MANUAL_INIT]

		# Behavior comments:



	def create(self):
		# x:725 y:300, x:444 y:420
		_state_machine = OperatableStateMachine(outcomes=['finished', 'failed'])

		# Additional creation code can be added inside the following tags
		# [MANUAL_CREATE]
		
		# [/MANUAL_CREATE]

		# x:30 y:365, x:130 y:365, x:230 y:365, x:330 y:365
		_sm_customer_service_0 = ConcurrencyContainer(outcomes=['finished', 'failed'], conditions=[
										('finished', [('Customer Service_Clean', 'finished')]),
										('failed', [('Customer Service_Clean', 'failed')])
										])

		with _sm_customer_service_0:
			# x:44 y:95
			OperatableStateMachine.add('Customer Service_Clean',
										self.use_behavior(CustomerService_CleanSM, 'Customer_Service/Customer Service_Clean'),
										transitions={'finished': 'finished', 'failed': 'failed'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit})



		with _state_machine:
			# x:221 y:108
			OperatableStateMachine.add('Customer_Service',
										_sm_customer_service_0,
										transitions={'finished': 'finished', 'failed': 'failed'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit})


		return _state_machine


	# Private functions can be added inside the following tags
	# [MANUAL_FUNC]
	
	# [/MANUAL_FUNC]
