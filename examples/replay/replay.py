#!/usr/bin/env python3

import sys
import os
from bestman.robots.startouch import StartouchConfig
from bestman.utils import select_multi_sessions_dir,select_session_subdir
from bestman.utils import load_trajectory,rpy2T,transform_traj
from bestman.robots import make_robot_from_config 
from bestman.utils import TrajReplayer

DATA_ROOT='/media/ark/B2D6-285E'

# ==================== Startouch 配置 ====================
config = StartouchConfig(
    id="startouch",     # 多臂debug以及logger用                   
    dof=6,                                          
    initial_joints=[0.0, 0.0, 0.0, 0.0, 0.0, 0.0],         #home_关节                 
    sdk_kwargs={
        "can_port": "can0" #透传至原sdk的参数
    }
)
robot = make_robot_from_config(config)
replayer = TrajReplayer(robot=robot)
replayer.load_data(DATA_ROOT)

try:
    robot.connect()      
    robot.go_home()

    pose = robot.get_ee_pose()#[x,y,z,r,p,y](m,rad)
    T_robot_init = rpy2T(pose)
   
    replayer.transform_traj(T_robot_init=T_robot_init)
    
    replayer.replay(speed_rate=1.0)



except Exception as e:
    print(e)

finally:
    robot.disconnect()   # 安全断开（失能机械臂）

