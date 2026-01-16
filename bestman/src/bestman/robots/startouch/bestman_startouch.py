import time
import sys
import os
from typing import Any, Dict, Optional, Union, Tuple,List

import numpy as np
from scipy.spatial.transform import Rotation as R


from bestman.robots.base_robot import BaseRobot
from .startouch_config import StartouchConfig
from ..factory import register_robot

try:
    from startouch_python_sdk import StartouchArm
except ImportError as e:
    raise ImportError(
        "Startouch SDK not available. "
        "Please ensure the .so files are present in the startouch_sdk directory. "
        f"Original error: {e}"
    ) from e
@register_robot(StartouchConfig)
class BestmanStartouch(BaseRobot):
    """
    piper 
    - move_to_joint_positions()
    - move_to_ee_pose()
    - move_gripper()
    """

    config_class = StartouchConfig

    def __init__(self, config: StartouchConfig):
        super().__init__(config)
        self.config: StartouchConfig = config
        self.arm: None
        self.cameras = {}

    @property
    def observation_features(self) -> Dict[str, Any]:
        pass

    def connect(self) -> None:
        """
        建立与 Piper 机械臂的连接
        """
        self.arm = StartouchArm(**self.config.sdk_kwargs)
        # pass
        print(f"[{self.config.id or 'startouch'}] Connected successfully.")



    def disconnect(self) -> None:
        """
        安全断开连接
        """
        self.arm.cleanup()

    def get_observation(self) -> Dict[str, Any]:
        pass

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
        pass

    @property
    def mode(self):
        pass
    
    def go_home(self):
       self.arm.go_home()
            
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
        self.arm.set_joint(joint_positions)

    def move_to_ee_pose(
        self,
        pose:Union[list,np.ndarray],
        is_radian: bool = False,
        wait: bool = False
    ):
        """
        控制末端执行器移动到目标位姿（笛卡尔空间） - 角度
        
        Args:
            pose: [x,y,z,roll,pitch,yaw]    position单位：米 
            is_radian:radian or degree
            wait: 是否阻塞等待执行完成
        """
        if pose.shape != (6,):
            raise ValueError(f"pose must be shape (6,), got {pose.shape}")
        position = pose[:3]
        rpy = pose[3:]
        self.arm.set_end_effector_pose_euler(position,rpy)

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
        if (position.shape != (3,)) or (rpy.shape != (3,)):
            raise ValueError(f"position and position must be shape (3,), position.shape : {position.shape}, rpy.shape : {rpy.shape}")
        
        self.arm.set_end_effector_pose_euler(position,rpy)
    
    def move_to_ee_pose_quat(
        self,
        position: Union[list, np.ndarray],
        orientation: Union[list, np.ndarray],
        is_radian: bool = False,
        wait: bool = False,
    ):
        if position.shape != (3,):
            raise ValueError(f"position must be shape (3,), position.shape : {position.shape}")
        
        if orientation.shape != (4,):
            raise ValueError(f"orientation must be shape (4,), position.shape : {orientation.shape}")
        
        self.arm.set_end_effector_pose_quat(position,orientation)

    def servo_to_joint_positions(
        self,
        joint_positions: Union[list, np.ndarray],
    ) -> bool:
        """实时关节伺服（模式 1，需高频调用）"""
        pass
    
    def servo_to_ee_pose(
        self,
        pose: Union[list, np.ndarray]
    ) -> bool:
        """实时笛卡尔伺服（模式 1，需高频调用）"""
        pass

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
        self.arm.setGripperPosition(command)
        

    def get_joint_positions(self) -> List[float]:
        """
        Get current joint angles.
        获取当前关节角。

        Returns:
            (N,) List in radians
        """
        return self.arm.get_joint_positions().tolist()

    def get_joint_velocities(self) -> List[float]:
        """
        Get current joint velocities.
        获取当前关节速度。

        Returns:
            (N,) List in rad/s 
        """
        return self.arm.get_joint_velocities().tolist()

   
    def get_ee_pose(self) -> Tuple[np.ndarray, np.ndarray]:
        """
        Get current end-effector pose in base coordinate frame.
        获取基坐标系下的当前末端执行器位姿。

        Returns:
            position: (3,) in meters / 位置：(3,) 米
            orientation: (3,) quaternion [roll, pitch, yaw](degree)角度
        """
        return self.get_ee_pose_euler()
    
    def get_ee_velocity(self) -> Tuple[np.ndarray, np.ndarray]:
        """
        Get current end-effector velocity in base coordinate frame.
        获取基坐标系下的当前末端执行器速度。

        Returns:
            linear_vel: (3,) in m/s / 线速度：(3,) m/s
            angular_vel: (3,) in rad/s / 角速度：(3,) rad/s
        """
        pass
   
    def get_gripper_position(self) -> float:
        """
        Get current gripper position.
        获取当前夹爪位置。

        Returns:
            Normalized value in [0.0, 1.0] (0=open, 1=closed), 
            or physical value (e.g., mm) — consistent per robot model.
            归一化值 [0.0, 1.0]（0=开，1=关），或物理单位（如 mm）——每种机器人保持一致。
        """
        return self.arm.get_gripper_position()

    def __getattr__(self, name):
        pass