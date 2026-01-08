# position:[x,y,z] rpy[roll,pitch,yaw]控制
from bestman.robots.xarm import XArmConfig
from bestman.robots.xarm import BestmanXarm
from bestman.robots import make_robot_from_config
import time
# Xarm配置对象
config = XArmConfig(
    id="my_xarm",
    dof=7,
    initial_joints=[0., 0., 0., 0., -180., 90., -180.],
    tcp_offset=[0,0,0,0,0,0],
    sdk_kwargs={"port":"192.168.1.235","is_radian":False}
)

robot:BestmanXarm = BestmanXarm(config)
# or
# robot = make_robot_from_config(config)
position_list = [[0.225 , 0 , 0.14  ],#原位
             
            [0.275 , 0 , 0.14  ],#x轴运动5cm
            [0.225 , 0 , 0.14  ],#回原位

            [0.225 , 0.05 , 0.14  ],#y轴运动5cm
            [0.225 , 0 , 0.14  ],#回原位

            [0.225 , 0 , 0.19  ],#z轴运动5cm
            [0.225 , 0 , 0.14  ],#回原位

            ]
rpy_list = [[90, -90, 90]]*len(position_list)
try:
    robot.connect()
    robot.go_home()
    i = 0
    while(True):
        position = position_list[i]
        rpy = rpy_list[i]
        ee_pos = robot.move_to_ee_pose_rpy(position=position,rpy=rpy,wait=True)
        i=(i+1)%len(position_list)
except KeyboardInterrupt:
    print("keyboard exit")
except Exception as e:
    print(e)
finally:
    robot.go_home()
    robot.disconnect()