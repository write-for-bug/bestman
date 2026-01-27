from dataclasses import dataclass
import draccus
import time
import numpy as np
import math

from bestman.robots.startouch import StartouchConfig
from bestman.robots.startouch import BestmanStartouch
from bestman.robots import make_robot_from_config  # 通用工厂函数（推荐使用）

# ==================== Piper 配置 ====================
# 方式1：直接手动创建配置（推荐用于快速测试）
config = StartouchConfig(
    id="startouch",                                  
    dof=6,                                          
    initial_joints=[0.0, 0.0, 0.0, 0.0, 0.0, 0.0],                          
    sdk_kwargs={
        "can_port": "can0"
    }
)


robot = BestmanStartouch(config)

# or
# robot = make_robot_from_config(config)

try:
    robot.connect()
    robot.go_home()
    time.sleep(2)  
    
    print("Starting cyclic joint motion...")

    while(True):
        robot.move_gripper(1)
        time.sleep(1.0)
        robot.move_gripper(0.5)
        print("get_gripper_position:", robot.get_gripper_position())
        time.sleep(1)
        robot.move_gripper(0)
        time.sleep(1)

except KeyboardInterrupt:
    print("keyboard exit")
except Exception as e:
    print(e)
finally:
    robot.go_home()
    # robot.disconnect()