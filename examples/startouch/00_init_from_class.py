#!/usr/bin/env python3

import sys
import os


from bestman.robots.startouch import StartouchConfig,BestmanStartouch

# ==================== Startouch 配置 ====================
config = StartouchConfig(
    id="startouch",                                  
    dof=6,                                          
    initial_joints=[0.0, 0.0, 0.0, 0.0, 0.0, 0.0],                          
    sdk_kwargs={
        "can_port": "can0" 
    }
)

robot:BestmanStartouch = BestmanStartouch(config)
# 推荐使用通用工厂函数初始化
# from bestman.robots import make_robot_from_config  
# robot = make_robot_from_config(config)

try:
    robot.connect()      
    robot.go_home()     
    import time
    print("Home motion completed. Waiting 5 seconds...")
    time.sleep(5)
except Exception as e:
    print(e)

finally:
    robot.disconnect()   # 安全断开（失能机械臂）

