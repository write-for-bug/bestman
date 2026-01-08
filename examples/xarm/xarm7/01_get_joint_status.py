from bestman.robots.xarm import XArmConfig
from bestman.robots.xarm import BestmanXarm
from bestman.robots import make_robot_from_config
import time

# Xarm配置对象
config = XArmConfig(
    id="my_xarm",
    dof=7,
    initial_joints=[0., 0., 0., 0., -180., 90., -180.],
    sdk_kwargs={"port":"192.168.1.235","is_radian":False}
)


robot:BestmanXarm = BestmanXarm(config)
# or
# robot = make_robot_from_config(config)
try:
    robot.connect()
    robot.go_home()
    #http://192.168.1.235:18333/control?lang=en&channel=prod
    while(True):
        joints = robot.get_joint_positions()
        joints_vel = robot.get_joint_velocities()
        print("Joint Pos : ", " ".join(f"{x:8.3f}" for x in joints))
        print("Joint Vel: ", " ".join(f"{v:8.3f}" for v in joints_vel))
        print("-" * 60)
        time.sleep(0.01)
except KeyboardInterrupt:
    print("key board exit")
finally:
    robot.disconnect()