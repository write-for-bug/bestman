from bestman.robots.xarm import XArmConfig
from bestman.robots.xarm import BestmanXarm

def main():
    # Xarm配置对象
    config = XArmConfig(
        id="my_xarm",
        dof=7,
        initial_joints=[0., 0., 0., 0., -180., 90., -180.],
        tcp_offset=[0., 0., 0., 0., 0., 0.],
        sdk_kwargs={"port":"192.168.1.235","is_radian":False}#透传给原SDK的参数
    )

    # Xarm实例
    robot= BestmanXarm(config)
    # or from factory
    # from bestman.robots import make_robot_from_config
    # robot = make_robot_from_config(config)
    try:
        robot.connect()
        robot.go_home()
        robot.disconnect()
    except Exception as e:
        print(e)
if __name__ == "__main__":
    main()
