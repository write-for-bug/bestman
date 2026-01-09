# pose:[x,y,z,roll,pitch,yaw]直接控制
from bestman.robots.xarm import XArmConfig
from bestman.robots.xarm import BestmanXarm
from bestman.robots import make_robot_from_config
import time
# Xarm配置对象
config = XArmConfig(
    id="my_xarm",
    dof=7,  
    initial_joints=[0., 0., 0., 0., -180., 90., -180.],
    tcp_offset=[0., 0., 0., 0., 0., 0.],
    sdk_kwargs={"port":"192.168.1.235","is_radian":False}
)
robot:BestmanXarm = BestmanXarm(config)
# or
# robot = make_robot_from_config(config)
pose_list = [[0.225 , 0 , 0.14  , 90  ,-90 , 90],#原位
             
            [0.275 , 0 , 0.14  , 90  ,-90 , 90],#x轴运动5cm
            [0.225 , 0 , 0.14  , 90  ,-90 , 90],#回原位

            [0.225 , 0.05 , 0.14  , 90  ,-90 , 90],#y轴运动5cm
            [0.225 , 0 , 0.14  , 90  ,-90 , 90],#回原位

            [0.225 , 0 , 0.19  , 90  ,-90 , 90],#z轴运动5cm
            [0.225 , 0 , 0.14  , 90  ,-90 , 90],#回原位

            [0.225 , 0 , 0.14  , 100  ,-90 , 90],#绕x轴正转10度
            [0.225 , 0 , 0.14  , 90  ,-90 , 90],#回原位

            [0.225 , 0 , 0.14  , 90  ,-80 , 90],#绕y轴正转10度
            [0.225 , 0 , 0.14  , 90  ,-90 , 90],#回原位

            [0.225 , 0 , 0.14  , 90  ,-90 , 100],#绕z轴正转10度
            [0.225 , 0 , 0.14  , 90  ,-90 , 90],#回原位
            ]
try:
    robot.connect()
    robot.go_home()
    
    i = 0
    while(True):
        ee_pos = robot.move_to_ee_pose(pose_list[i],wait=True)
        i=(i+1)%len(pose_list)

except KeyboardInterrupt:
    print("keyboard exit")
except Exception as e:
    print(e)
finally:
    robot.go_home()
    robot.disconnect()