#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
重定位测试
"""
from startouchclass import SingleArm
import time
import numpy as np


pos = np.array([0.3, 0.02, 0.205], dtype=float)
euler = np.array([0.0, 0.0, 0.0], dtype=float)
# 创建机械臂连接  连接接口为"can0"
arm_controller = SingleArm(can_interface_ = "can0")

arm_controller.set_end_effector_pose_euler(pos,euler)
time.sleep(2.0)
arm_controller.go_home()
time.sleep(2)

arm_controller.set_end_effector_pose_euler(pos,euler)
time.sleep(2.0)
arm_controller.go_home()
time.sleep(2)

arm_controller.cleanup()


