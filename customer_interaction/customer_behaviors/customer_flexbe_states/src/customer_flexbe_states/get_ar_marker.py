#!/usr/bin/env python
import time

from numpy.lib.shape_base import get_array_prepare
import rospkg, rospy
import numpy as np
import ConfigParser
from flexbe_core import EventState, Logger
from flexbe_core.proxy import ProxyServiceCaller
from product_strategy import GetProductInfo
from enum import IntEnum

class Status(IntEnum):
    idle        = 0
    busy        = 1
    failed      = 2
    finish      = 3

class aruco_information(dict):

    def __init__(self):
        self['ids']           = [] 
        self['base_H_mrks']   = []
        self['names']         = []
        self['exps']          = []
        self['side_ids']      = []


class GetArMarker(EventState):
    """
    Publishes a pose from userdata so that it can be displayed in rviz.

    -- robot_side              string                 Robots side to move
    #> ar_marker_info          aruco_infoResponse()   See get_product_info.py

    <= done									          Calib done.
    <= fail							    	          Calib fail.

    """
    
    def __init__(self, robot_side):
        """Constructor"""
        super(GetArMarker, self).__init__(outcomes=['done', 'failed'],output_keys=['ar_marker_info'])
        self.robot_side = robot_side
        self.status = Status.idle
        self.GetProductInfo = GetProductInfo()
        self.ar_marker_res = None


    def execute(self, userdata):

        if self.status == Status.failed:
            return 'failed'
        elif self.status == Status.busy and self.ar_marker_res!= None:
            # userdata.ar_marker_info = aruco_information()
            # userdata.ar_marker_info['ids']    = self.ar_marker_res.ids
            # userdata.ar_marker_info['corner'] = self.ar_marker_res.corners
            # userdata.ar_marker_info['rvecs']  = self.ar_marker_res.rvecs
            # userdata.ar_marker_info['tvecs']  = self.ar_marker_res.tvecs
            self.status = Status.finish
            print("-----------------------------------")
            userdata.ar_marker_info = aruco_information()
            userdata.ar_marker_info['ids']         = self.ar_marker_res[0]
            userdata.ar_marker_info['base_H_mrks'] = self.ar_marker_res[1]
            userdata.ar_marker_info['names']       = self.ar_marker_res[2]
            userdata.ar_marker_info['exps']        = self.ar_marker_res[3]
            userdata.ar_marker_info['side_ids']    = self.ar_marker_res[4]
            # print(self.ar_marker_res[0])
            # print(self.ar_marker_res[1])
            # print(self.ar_marker_res[2])
            # print(self.ar_marker_res[3])
            # print(self.ar_marker_res[4])
        elif self.status == Status.finish:
            return 'done'
        else:
            # print("Unknow")
            return

    def on_enter(self, _):
        time.sleep(0.5)
        self.status = Status.busy
        # self.ar_marker_res = self.GetProductInfo.get_ar_marker(self.robot_side)
        self.ar_marker_res = self.GetProductInfo.new_get_obj_info(self.robot_side)
        