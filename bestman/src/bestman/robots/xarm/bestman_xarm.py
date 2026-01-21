# bestman/robots/xarm6.py
from typing import Any, Dict, Optional, Union, Tuple,List

import numpy as np

from bestman.robots.base_robot import BaseRobot
from .xarm_config import XArmConfig
from ..factory import register_robot

try:
    from xarm.wrapper import XArmAPI
except ImportError:
    raise ImportError(
        "XArm SDK not installed. Please install via: "
        "pip install bestman[xarm]"
    )

@register_robot(XArmConfig)
class BestmanXarm(BaseRobot):
    """
    xArm6 
    - move_to_joint_positions()
    - move_to_ee_pose()
    - move_gripper()
    """

    config_class = XArmConfig

    def __init__(self, config: XArmConfig):
        super().__init__(config)
        self.config: XArmConfig = config
        self.arm: Optional[XArmAPI] = None
        self.cameras = {}

    @property
    def observation_features(self) -> Dict[str, Any]:
        pass
        # obs = {
        #     "joint_pos": (self.config.dof,),
        #     "joint_vel": (self.config.dof,),
        #     "eef_pos": (6,),#x,y,z,roll,pitch,yaw
        #     "eef_vel": (6,),#vx,vy,vz,vr,vp,vy
        #     "gripper_pos": float,
        # }
        # for cam_name in self.config.cameras:
        #     cam_cfg = self.config.cameras[cam_name]
        #     obs[f"image_{cam_name}"] = (cam_cfg.height, cam_cfg.width, 3)
        # return obs

    def connect(self) -> None:
        sdk_kwargs = self.config.sdk_kwargs.copy()

        self.arm = XArmAPI(**sdk_kwargs)
        try:
            self.arm.clean_warn()
            self.arm.clean_error()
            if hasattr(self.config,"tcp_offset") and self.config.tcp_offset is not None:
                self.arm.set_tcp_offset(self.config.tcp_offset,wait=True)
            self.arm.motion_enable(True)
            self.arm.set_mode(0)    #速度位置模式
        except Exception as e:
            if self.arm:
                self.arm.disconnect()
            self.arm = None  # 确保清理
            raise ConnectionError(f"Failed to connect to xArm: {e}") from e
        
        print(f"[{self.config.id or 'xarm6'}] Connected successfully.")
        if hasattr(self.config,"gripper") and self.config.gripper is not None:
            # gripper initialize
            pass
            # self.gripper = XArmGripper(self.arm)
            # self.gripper.connect()

        if hasattr(self.config,"cameras"):
            for name, cam_cfg in self.config.cameras.items():
                pass# maybe TODO
                # self.cameras[name] = get_camera(cam_cfg)



    def disconnect(self) -> None:
        if self.arm:
            self.arm.disconnect()
        for cam in self.cameras.values():
            cam.release()
        print(f"[{self.config.id or 'xarm6'}] Disconnected.")

    def get_observation(self) -> Dict[str, Any]:
        pass
        # angles = self.arm.get_servo_angle()[1]
        # velocities = self.arm.get_joint_states()[1][1]
        # gripper_pos = self.gripper.get_position() if self.gripper else 0.0

        # obs = {
        #     "joint_positions": np.array(angles[: self.config.dof], dtype=np.float32),
        #     "joint_velocities": np.array(velocities[: self.config.dof], dtype=np.float32),
        #     "gripper_position": float(gripper_pos),
        # }

        # for name, cam in self.cameras.items():
        #     ret, frame = cam.read()
        #     if ret:
        #         obs[f"image_{name}"] = frame[..., ::-1]  # BGR -> RGB
        #     else:
        #         cfg = self.config.cameras[name]
        #         obs[f"image_{name}"] = np.zeros(
        #             (cfg.height, cfg.width, 3), dtype=np.uint8
        #         )
        # return obs
    def action_features(self) -> Dict[str, Any]:
        """
        Declare the structure of action commands.
        声明动作指令的结构。

        Example / 示例:
        {
            "joint_targets": (6,),     # Target joint angles in radians / 目标关节角（弧度）
            "gripper_command": float   # Gripper command, normalized [0,1] / 夹爪指令（归一化）
        }
        """
        pass
    # ======== 独立控制接口 ========
    def set_mode(self, mode):
        '''
        Parameters:
        _mode=
            0: position control mode
            1: servo motion mode
            2: joint teaching mode (invalid)
            3: cartesian teaching
            4: joint velocity control mode
            5: cartesian velocity control mode
            6: joint online trajectory planningmode
            7: cartesian online trajectory planning
        Notes:
            https://github.com/xArm-Developer/xArm-Python-SDK/blob/master/doc/api/xarm_api.md#mode
        '''
        self.arm.set_mode(mode)
        # self.arm.motion_enable(True)
        self.arm.set_state(0)#每次更换机械臂运动模式都要切换机械臂运动状态

    @property
    def mode(self):
        return self.arm.mode
    
    def go_home(self):
        self.set_mode(0)
        if hasattr(self.config, "initial_joints") and self.config.initial_joints is not None:
            self.move_to_joint_positions(self.config.initial_joints, wait=True)
        else:
            ValueError("initial joint not defined in config")
            
    def move_to_joint_positions(
        self,
        joint_positions: Union[list, np.ndarray],
        is_radian: bool = False,
        wait: bool = True,
    ) -> bool:
        """
        控制机械臂移动到目标关节角度（单位：弧度）
        
        Args:
            joint_positions: 目标关节角，长度必须等于 config.dof
            blocking: 是否阻塞等待执行完成
            is_radian: 是否使用弧度制
        """
        if self.mode != 0:
            self.set_mode(0)
        if len(joint_positions) != self.config.dof:
            raise ValueError(
                f"Expected joint_positions shape ({self.config.dof},), got {joint_positions.shape}"
            )
        code = self.arm.set_servo_angle(
            angle=joint_positions,
            is_radian=is_radian,
            wait=wait,
        )
        return code == 0  

    def move_to_ee_pose(
        self,
        pose:Union[list,np.ndarray],
        is_radian: bool = False,
        wait: bool = False
    ):
        """
        控制末端执行器移动到目标位姿（笛卡尔空间）
        
        Args:
            pose: [x,y,z,roll,pitch,yaw]    position单位：米 
            is_radian:radian or degree
            wait: 是否阻塞等待执行完成
        """
        if self.mode != 0:
            self.set_mode(0)
        if len(pose) != 6:
            raise ValueError(f"pose must be (3,), got {pose.shape}")

        code = self.arm.set_position(
            x = pose[0]*1000, y = pose[1]*1000, z = pose[2]*1000,
            roll = pose[3], pitch = pose[4], yaw = pose[5],
            is_radian=is_radian,
            wait=wait,
        )
        return code == 0

    def move_to_ee_pose_rpy(
        self,
        position: Union[list, np.ndarray],
        rpy: Union[list, np.ndarray],
        is_radian: bool = False,
        wait: bool = False,
    ) -> bool:
        """
        控制末端执行器移动到目标位姿（笛卡尔空间）
        
        Args:
            position: [x, y, z]（单位：米）
            rpy: [roll, pitch, yaw](radian or degree)
            wait: 是否阻塞等待执行完成
        """
        if self.mode != 0:
            self.set_mode(0)

        if len(position) != 3:
            raise ValueError(f"position must be (3,), got {position.shape}")
        if len(rpy) != 3:
            raise ValueError(f"rpy must be (3,) , got {rpy.shape}")

        
        code = self.arm.set_position(
            x = position[0]*1000, y = position[1]*1000, z = position[2]*1000,
            roll = rpy[0], pitch = rpy[1], yaw = rpy[2],
            is_radian=is_radian,
            wait=wait,
        )
        return code == 0
    
    def move_to_ee_pose_quat(
        self,
        position: Union[list, np.ndarray],
        orientation: Union[list, np.ndarray],
        is_radian: bool = False,
        wait: bool = False,
    ):
        raise NotImplementedError("coming")

    def servo_to_joint_positions(
        self,
        joint_positions: Union[list, np.ndarray],
    ) -> bool:
        """实时关节伺服（模式 1，需高频调用）"""
        if self.mode != 1:
            raise ValueError(f"current mode:{self.mode}, call set_mode(1) first")
            # self.arm.set_mode(1)
        return self.arm.set_servo_angle_j(angles=joint_positions,is_radian=False) == 0
    
    def servo_to_ee_pose(
        self,
        pose: Union[list, np.ndarray]
    ) -> bool:
        """实时笛卡尔伺服（模式 1，需高频调用）"""
        if self.mode != 1:
            raise ValueError(f"current mode:{self.mode}, call set_mode(1) first")
            
        self.arm.set_servo_cartesian(mvpose=pose,is_radian=False)
    
    def servo_to_ee_pose_rpy(
        self,
        position: Union[list, np.ndarray],
        rpy: Union[list, np.ndarray],
    ) -> bool:
        raise NotImplementedError()
    
    def servo_to_ee_pose_quat(
        self,
        position: Union[list, np.ndarray],
        orientation: Union[list, np.ndarray],
    ) -> bool:
        raise NotImplementedError()
    
    def move_gripper(self, command: float) -> bool:
        """
        控制夹爪开合
        
        Args:
            command: 夹爪指令（0.0~1.0 或具体单位，取决于 GripperInterface 实现）
        """
        if self.gripper is None:
            raise RuntimeError("Gripper not initialized")
        try:
            self.gripper.move(command)
            return True
        except Exception as e:
            print(f"Gripper error: {e}")
            return False
        

    def get_joint_positions(self) -> List[float]:
        """
        Get current joint angles.
        获取当前关节角。

        Returns:
            (N,) List in radians
        """
        return self.arm.get_servo_angles()

    def get_joint_velocities(self) -> List[float]:
        """
        Get current joint velocities.
        获取当前关节速度。

        Returns:
            (N,) List in rad/s 
        """
        return self.arm.realtime_joint_speeds

   
    def get_ee_pose(self) -> Tuple[np.ndarray, np.ndarray]:
        """
        Get current end-effector pose in base coordinate frame.
        获取基坐标系下的当前末端执行器位姿。

        Returns:
            position: (3,) in meters / 位置：(3,) 米
            orientation: (4,) quaternion [x, y, z, w] / 姿态：(4,) 四元数 [x, y, z, w]
        """
        position = self.arm.position    
        position[:3] = [x/1000 for x in position[:3]]
        return position

    
    def get_ee_velocity(self) -> Tuple[np.ndarray, np.ndarray]:
        """
        Get current end-effector velocity in base coordinate frame.
        获取基坐标系下的当前末端执行器速度。

        Returns:
            linear_vel: (3,) in m/s / 线速度：(3,) m/s
            angular_vel: (3,) in rad/s / 角速度：(3,) rad/s
        """
        raise NotImplementedError("SDK only offers scalar")
        return self.arm.realtime_tcp_speed
   
   
    def get_gripper_position(self) -> float:
        """
        Get current gripper position.
        获取当前夹爪位置。

        Returns:
            Normalized value in [0.0, 1.0] (0=open, 1=closed), 
            or physical value (e.g., mm) — consistent per robot model.
            归一化值 [0.0, 1.0]（0=开，1=关），或物理单位（如 mm）——每种机器人保持一致。
        """
        pass

    def __getattr__(self, name):
        return getattr(self.arm, name)