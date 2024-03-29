#!/usr/bin/env python
# -*- coding: utf-8 -*-
import rospy
import os
import yaml
from arm_status_msgs.msg import ArmStatus
from arm_work_msgs.msg import ArmWork
from arm_base import Arm_base
from errorAnalyzer import ErrorAnalyzer

#

class Arm_car(Arm_base):
    def __init__(self, num_judgments=5,
                 depth=210, Arm_Location = (0, 0, 0), wucha = 1,
                 error_range = 12, wait_time = 12):
        super(Arm_car,self).__init__(depth, Arm_Location, wucha, error_range, wait_time)
        self._ID = self._config_data["ID"]
        self._num_judgments = int(self._config_data["num_judgments"]) # 子类自己的参数  车是4
        #self._analyzer = ErrorAnalyzer(self._error_range, self._num_judgments)  # 生成误差分析对象 num_judgments,车是4，四角固定是15
        self._analyzer = ErrorAnalyzer(self._error_range, self._num_judgments,self._error_range_width)  # 生成误差分析对象 num_judgments,车是4，四角固定是15
        self._work = ''
        self._job = '' # Ros传过来的消息，告诉我们这是什么任务。
        # self._example_flag = False
	self._msg = ArmStatus()
        self._msg.status = False # 机械臂的状态初始化为False
        # 消息的注册
        self.pub_arm_status = rospy.Publisher('arm_status', ArmStatus, queue_size=1)
        # 消息的订阅
        self.sub_arm_work = rospy.Subscriber('arm_work', ArmWork, self.call_back)
        rospy.loginfo("arm_car_"+ str(self._ID) +" is completed")

    def call_back(self, msg):
        rospy.loginfo(" arm_car_" + str(self._ID) + "has been in call_back")
        if self._ID == msg.arm_id:
            rospy.loginfo("arm_car_"+ str(self._ID) +": id is right, call back has been called")
            # 获取消息的内容
            self._work = msg.work
            self._job = msg.job
            self.set_color_information(msg.color) # 设置夹取的颜色信息

            # 执行相应的命令，pick / drop任意一个干完就发一次消息
            if self._work == 'pick':
                self.Arm_pick()
                self.sender()  # ros返回消息
                self.reset()  # 重置信息
                rospy.loginfo("arm_car_"+ str(self._ID) +": flag has been changed True")
                # self._example_flag = True
            
            elif self._work == 'drop':
                self.Arm_drop()
                self.sender()  # ros返回消息
                self.reset()  # 重置信息
                rospy.loginfo("arm_car_"+ str(self._ID) +": flag has been changed True")
                # self._example_flag = True
                

    # 程序执行完毕后，一些必要的信息必须重置为开始状态
    def reset(self):
        self._color_information = None
        self._flag = False
        self._flag_error = False
        self._angle = None
        # self._armStatic_status = False
        self._work = ''
        self._job = ''
        self._color_information = None

    # 机械臂夹取完毕后，返回消息，
    def sender(self):
        self._msg.arm_id = self._ID
        self._msg.status = True
        self._msg.job = self._job

        # 发送消息
        self.pub_arm_status.publish(self._msg)
        rospy.loginfo("arm_car_"+ str(self._ID) +": pub_arm_status has been pubulished")

    def Arm_pick(self):
        # 开始识别识别，返回角度
        self._angle = self.recognize_angle(self._analyzer)
        # 夹取
        self.execute_car_pick()
        rospy.loginfo("arm_car_"+ str(self._ID) +":pick is completed")

    def Arm_drop(self):
        # 放置
        self.execute_car_place()
        rospy.loginfo("arm_car_"+ str(self._ID) +":drop is completed")

    # 小车机械臂的夹取函数
    def execute_car_pick(self):
         # 旋转
        if abs(self._angle) <= 90:
            self._wucha = -(90- abs(self._angle)) / self._offset_real_right * self._offset_change
            self.control_Arm(1, 90 - self._angle, False, self._wucha)
        elif abs(self._angle) > 90:
            self._wucha = (abs(self._angle) -90) / self._offset_real_left * self._offset_change
            self.control_Arm(1, 90 - abs(self._angle), True, self._wucha)
        rospy.sleep(.5)

        # 准备夹取
        # 1、先伸直
        angle_id_1 = self._Arm.Arm_serial_servo_read(1)  # 读取第一舵机的角度
        rospy.sleep(1)
        # angle_id_2 = 60 # 放7.5厘米的盒子
        angle_id_2 = 38 # 物块放在地上，应该是38
        angle_id_4 = 70 # 物块放在地上还是盒子上都是70
        p_move_1 = [angle_id_1, angle_id_2, 0, angle_id_4, 90]
        self.arm_move(p_move_1, 1500)# 机械臂伸直
        rospy.sleep(2)
        
        # 夹取
        self.arm_clamp_block(1)  # 夹取
        rospy.sleep(1)
        # 回归到等待位置
        self.arm_move(self._p_mould, 1000)  # 回到指定位置

    # 小车机械臂的放置函数，参数是举例的，具体的参数需要根据实际情况进行修改
    def execute_car_place(self):
        angle_id_1 = self._Arm.Arm_serial_servo_read(1)  # 读取第一舵机的角度
        rospy.sleep(1)
        angle_id_2 = 40
        angle_id_4 = 70
        p_move_1 = [angle_id_1, angle_id_2, 0, angle_id_4, 90]
        self.arm_move(p_move_1, 1500)# 机械臂伸直
        rospy.sleep(2)
        
        self.arm_clamp_block(0)  # 松开夹子
        rospy.sleep(1)
        self.arm_move(self._p_mould, 1500)
        rospy.sleep(1)
