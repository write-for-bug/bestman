#!/usr/bin/env python3

import sys
import os

# so_dir = "/home/lumos/bestman/bestman/src/bestman/robots/startouch"
# sys.path.append(so_dir)
# 调试：列出so_dir下的文件，确认.so存在
# print("so目录下的文件：", os.listdir(so_dir))

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

finally:
    robot.disconnect()   # 安全断开（失能机械臂）

print("Piper test completed.")