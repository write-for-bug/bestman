# 绕tcp中心旋转
from bestman.robots.xarm import XArmConfig
from bestman.robots.xarm import BestmanXarm
from bestman.robots import make_robot_from_config
import time
# Xarm配置对象
config = XArmConfig(
    id="my_xarm",
    dof=7,  
    initial_joints=[0., 0., 0., 0., -180., 90., -180.],
    tcp_offset=[0., 0., 174.435, 0., 0., 0.],  #单位：mm
    sdk_kwargs={"port":"192.168.1.235","is_radian":False}
)
robot:BestmanXarm = BestmanXarm(config)
# or
# robot = make_robot_from_config(config)
rpy_offset_list = [[0,0,0],[0,20,0],[20,0,0],[0,0,20]
              ,[0,-20,0],[-20,0,0],[0,0,-20]]
try:
    robot.connect()
    robot.go_home()
    pose = robot.get_ee_pose()
    position = pose[:3].copy()
    init_rpy = pose[3:6].copy()
    i = 0
    while(True):
        rpy = [a+b for a,b in zip(init_rpy,rpy_offset_list[i])]
        ee_pos = robot.move_to_ee_pose_rpy(position=position,rpy=rpy,wait=True)
        i=(i+1)%len(rpy_offset_list)

except KeyboardInterrupt:
    print("keyboard exit")
except Exception as e:
    print(e)
finally:
    robot.go_home()
    robot.disconnect()