#!/usr/bin/env python
import time
import cv2
from numpy.lib.shape_base import get_array_prepare
import rospkg, rospy
import numpy as np
import ConfigParser
from flexbe_core import EventState, Logger
from arm_control import Command, ArmTask, DualArmTask
from product_strategy import GetProductInfo
from flexbe_core.proxy import ProxyServiceCaller
# from hand_eye.srv import eye2base, eye2baseResponse
# from detect_aruco_pose_dual_cam.srv import aruco_info, aruco_infoResponse
from math import radians, degrees, sin, acos, pi, cos
from enum import IntEnum

class Status(IntEnum):
    idle        = 0
    failed      = 1
    busy        = 2
    finish      = 3


class ReciveAndTransToArm(EventState):
    """
    Publishes a pose from userdata so that it can be displayed in rviz.

    -- robot_name              string          Robots name to move

    <= done									   Calib done.
    <= fail							    	   Calib fail.

    """
    
    def __init__(self, robot_side, speed, en_sim):
        """Constructor"""
        super(ReciveAndTransToArm, self).__init__(outcomes=['done', 'finish'],
                                                  input_keys=['ar_marker_info'],
                                                  output_keys=['robot_cmd'])
        self.robot_side = robot_side
        self.default_speed = speed
        self.en_sim = en_sim
        self.id_num = 0
        self.status = Status.idle
        self.side_id = None
        self.ids = None
        self.object_name = None
        self.base_H_mrks = None
        self.roll = 0.0
        self.GetProductInfo = GetProductInfo()
        self.DualArmTask = DualArmTask(self.robot_side, self.en_sim)
        self.pos = None
        self.vector = None
        self.sucang = None


    def execute(self, userdata):

        if self.status == Status.idle:
            self.id_num = np.size(userdata.ar_marker_info['ids'])
            self.ids = userdata.ar_marker_info['ids']
            self.base_H_mrks = userdata.ar_marker_info['base_H_mrks']
            self.base_H_mrks = self.base_H_mrks.reshape(int(np.size(self.base_H_mrks)/16), 4, 4)[0]
            print(self.base_H_mrks)
            self.object_name = userdata.ar_marker_info['names']
            self.expired = userdata.ar_marker_info['exps']
            self.side_id = userdata.ar_marker_info['side_ids']
            
            
            self.vector = self.base_H_mrks[0:3, 2]
            print(self.vector)
            self.status = Status.busy
            self.sucang, self.roll = self.DualArmTask.suc2vector(self.vector, [0, 1.57, 0])

        elif self.status == Status.failed:
            return 'failed'

        elif self.id_num == 0:
            return 'finish'

        else:
            userdata.robot_cmd = Command()
            userdata.robot_cmd['mode'] = 'line'
            userdata.robot_cmd['speed'] = self.default_speed
            userdata.robot_cmd['pos'] = self.base_H_mrks[0:3, 3]
            userdata.robot_cmd['euler'] = [self.roll, 90, 0.0]
            userdata.robot_cmd['phi'] = 0
            print("++++++++++++++++++++++++++++++++")
            print(userdata.robot_cmd['mode'])
            print(userdata.robot_cmd['speed'])
            print(userdata.robot_cmd['pos'])
            print(userdata.robot_cmd['euler'])
            print(userdata.robot_cmd['phi'])
            self.id_num =self.id_num -1
            return 'done'

            
    def on_enter(self, userdata):
        print('start_transform_to_arm_base')
        

    
