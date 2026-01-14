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
        "can_port": "can0",     
        "judge_flag": True    
    }
)


robot = BestmanStartouch(config)

# or
# robot = make_robot_from_config(config)

pos = np.array([0.3, 0.02, 0.205], dtype=float)
euler1 = np.array([math.radians(30.0), 0.0, 0.0], dtype=float)  # x转30度
euler2 = np.array([0.0, 0.5235987756, 0.0], dtype=float)        # y转30度
quat1 = np.array([0.9659258262890683, 0.25881904510252074, 0.0, 0.0]) 
pose_6d = np.concatenate([pos, euler2])

try:
    robot.connect()
    robot.go_home()
    time.sleep(2)  
    
    print("Starting cyclic joint motion...")

    while(True):
        robot.move_to_ee_pose_rpy(pos , euler1)
        time.sleep(2.0)
        robot.go_home()
        time.sleep(2)
        robot.move_to_ee_pose_quat(pos , quat1)
        time.sleep(2)
        robot.move_to_ee_pose(pose_6d)
        print("get_joint_positions:" , robot.get_joint_positions())
        print("get_joint_velocities:" , robot.get_joint_velocities())
        time.sleep(2)

except KeyboardInterrupt:
    print("keyboard exit")
except Exception as e:
    print(e)
finally:
    robot.go_home()
    # robot.disconnect()