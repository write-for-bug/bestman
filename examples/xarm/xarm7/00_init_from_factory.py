import draccus
from bestman.robots import RobotConfig,make_robot_from_config
import os
from dataclasses import asdict
def main():
    # 获取config path
    script_path = os.path.abspath(__file__)
    script_dir = os.path.dirname(script_path)
    config_path = os.path.join(script_dir,"xarm7_config.yaml")
    config = draccus.parse(RobotConfig, config_path=config_path)
    
    # or
    # from bestman.robots.xarm import XArmConfig
    # config = XArmConfig(
    #     id="my_xarm",
    #     dof=7,
    #     initial_joints=[0., 0., 0., 0., -180., 90., -180.],
    #     tcp_offset=[0., 0., 0., 0., 0., 0.],
    #     sdk_kwargs={"port":"192.168.1.235","is_radian":False}#透传给原SDK的参数
    # )
    
   
    # initial robot instance in a unified way
    robot = make_robot_from_config(config)
    
    try:
        robot.connect()
        robot.go_home()
        robot.disconnect()
    except Exception as e:
        print(e)
if __name__ == "__main__":
    main()