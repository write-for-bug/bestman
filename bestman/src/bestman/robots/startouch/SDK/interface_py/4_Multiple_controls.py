#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
多种控制方法,带规划的时间默认是2s
注意:没有透传方法,函数后加入raw是透传方法,直接移动到目标位置,没有规划，小心
"""
from startouchclass import SingleArm
from startouchclass import *
import time
import numpy as np
import math


pos = np.array([0.3, 0.02, 0.205], dtype=float)
euler1 = np.array([math.radians(30.0), 0.0, 0.0], dtype=float)  # x转30度
euler2 = np.array([0.0, 0.5235987756, 0.0], dtype=float)        # y转30度
quat1 = np.array([0.9659258262890683, 0.25881904510252074, 0.0, 0.0]) # wxyz格式
quat2 = euler_to_quaternion(euler2[0],euler2[1],euler2[2])      # startouchclass内置转换函数

q = [0.127373,0.633809,0.161993,0.471817,0.127375,0.523513]

tf = 2
# 创建机械臂连接  连接接口为"can0"
arm_controller = SingleArm(can_interface_ = "can0")

# 欧拉角规划 x
arm_controller.set_end_effector_pose_euler(pos,euler1,tf)
time.sleep(2.0)
arm_controller.go_home()
time.sleep(2)

# 欧拉角规划 y
arm_controller.set_end_effector_pose_euler(pos,euler2)
time.sleep(2.0)
arm_controller.go_home()
time.sleep(2)

# 四元数规划 x
arm_controller.set_end_effector_pose_quat(pos,quat1)
time.sleep(2.0)
arm_controller.go_home()
time.sleep(2)

# 四元数规划 y
arm_controller.set_end_effector_pose_quat(pos,quat2)
time.sleep(2.0)
arm_controller.go_home()
time.sleep(2)

# 直接关节角度，位置同[pos,euler1]
arm_controller.set_joint(q)
time.sleep(2.0)
arm_controller.go_home()
time.sleep(2)


arm_controller.cleanup()


