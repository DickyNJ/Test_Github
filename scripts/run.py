#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
# sys.path.append('/home/jetson/CodeSpace/catkin_ws/devel/lib/python2.7/dist-packages/')
import rospy
from arm_car import Arm_car

rospy.init_node('arm_car2', anonymous=False)
rate = rospy.Rate(10) 

arm_car_2 = Arm_car()

while not rospy.is_shutdown():
    rate.sleep()
    
