from dataclasses import dataclass

from bestman.robots import (
    RobotConfig,
    make_robot_from_config,
    )
from bestman.robots.xarm import BestmanXarm,XArmConfig
import time
# 两种方法初始化config
# import draccus
# config = draccus.parse(RobotConfig, config_path="./configs/xarm7_config.yaml")

config = XArmConfig(
    id="my_xarm",
    dof=7,
    initial_joints=[0., 0., 0., 0., -180., 90., -180.],
    tcp_offset=[0,0,0,0,0,0],
    sdk_kwargs={"port":"192.168.1.235","is_radian":False}
)
robot:BestmanXarm = make_robot_from_config(config)


j_list = [[0., 0., 0., 0., -180., 90., -180.],
          [33.5, 9.8, 19.3, 16.3, -127.6, 88.3, -187.5],
          [12.7,-33.2,33.4,15.7,-121.9,48.3,-204],
          [-28.6,-11.5,38.4,25.9,-168.3,54.3,-180]]

i = 0
try:
    robot.connect()
    robot.go_home()
   
    # joint control loop
    while(True):
        robot.move_to_joint_positions(j_list[i],is_radian=False,wait=True)
        time.sleep(1)
        i=(i+1)%len(j_list)
except KeyboardInterrupt:
    print("keyboard exit")
finally:
    robot.go_home()
    robot.disconnect()

