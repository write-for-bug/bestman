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
pose = [0.225 , 0 , 0.14  , 90  ,-90 , 90]#原位
             
 
try:
    robot.connect()
    robot.go_home()
    #切换为伺服模式
    robot.set_mode(1)
    time.sleep(0.5)
    i = 0
    while(True):
       print("robot mode:",robot.mode)
       robot.servo_to_ee_pose(pose)
       time.sleep(0.2)
       

except KeyboardInterrupt:
    print("keyboard exit")
except Exception as e:
    print(e)
finally:
    robot.go_home()
    robot.disconnect()