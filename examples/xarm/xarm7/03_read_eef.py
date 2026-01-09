from bestman.robots.xarm import XArmConfig,BestmanXarm

import time
# Xarm配置对象
config = XArmConfig(
    id="my_xarm",
    dof=7,
    initial_joints=[0., 0., 0., 0., -180., 90., -180.],
    # tcp_offset=[0,0,174.435,0,0,0],
    tcp_offset=[0,0,0,0,0,0],
    sdk_kwargs={"port":"192.168.1.235","is_radian":False}
)


robot:BestmanXarm = BestmanXarm(config)
# or
# from bestman.robots import make_robot_from_config
# robot = make_robot_from_config(config)
try:
    robot.connect()
    robot.go_home()
    while(True):
        ee_pos = robot.get_ee_pose()
        print("End-Effector Pos : ", " ".join(f"{x:8.3f}" for x in ee_pos))
        print("-" * 60)
        time.sleep(0.01)
except KeyboardInterrupt:
    print("keyboard exit")
finally:
    robot.disconnect()