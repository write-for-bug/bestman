import abc
from typing import Any, Dict, Union, Tuple, List
import numpy as np

from .config import RobotConfig

class BaseRobot(abc.ABC):
    """
    Universal robot hardware abstraction interface.
    通用机器人硬件抽象接口。
    """
    config_class: type[RobotConfig]

    def __init__(self, config: RobotConfig):
        self.config = config

    # ======== Inference Related / 推理相关 ========
    @property
    @abc.abstractmethod
    def observation_features(self) -> Dict[str, Any]:
        """
        Declare the structure of observation data.
        声明观测数据的结构。

        Example / 示例:
        {
            "joint_pos": (6,),        # Joint angles in radians / 关节角（弧度）
            "joint_vel": (6,),        # Joint velocities in rad/s / 关节速度（rad/s）
            "eef_pos": (7,),          # EE pose [x,y,z,qx,qy,qz,qw] / 末端位姿
            "eef_vel": (6,),          # EE velocity [vx,vy,vz,wx,wy,wz] / 末端速度
            "gripper_position": float, # Normalized [0,1] / 归一化夹爪位置
            "image_hand": (480, 640, 3) # RGB image / RGB 图像
        }
        """
        pass

    @property
    @abc.abstractmethod
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
    @abc.abstractmethod
    def get_observation(self) -> Dict[str, Any]:
        """
        Retrieve a full observation dictionary as defined in `observation_features`.
        获取符合 `observation_features` 定义的完整观测字典。
        """
        pass

    # ======== Lifecycle / 生命周期 ========
    @abc.abstractmethod
    def connect(self) -> None:
        """
        Establish connection to the robot hardware.
        廻立与机器人硬件的连接。
        """
        pass

    @abc.abstractmethod
    def disconnect(self) -> None:
        """
        Safely disconnect and release all hardware resources.
        安全断开连接并释放所有硬件资源。
        """
        pass



    # ======== Read State Interface / 状态读取接口 ========
    @abc.abstractmethod
    def get_joint_positions(self) -> np.ndarray:
        """
        Get current joint angles.
        获取当前关节角。

        Returns:
            (N,) numpy array in radians / (N,) 弧度制 numpy 数组
        """
        pass

    @abc.abstractmethod
    def get_joint_velocities(self) -> np.ndarray:
        """
        Get current joint velocities.
        获取当前关节速度。

        Returns:
            (N,) numpy array in rad/s / (N,) 单位 rad/s 的 numpy 数组
        """
        pass

    @abc.abstractmethod
    def get_ee_pose(self) -> Tuple[np.ndarray, np.ndarray]:
        """
        Get current end-effector pose in base coordinate frame.
        获取基坐标系下的当前末端执行器位姿。

        Returns:
            pose: (6,) in meters /  米,
        """
        pass

    @abc.abstractmethod
    def get_ee_velocity(self) -> Tuple[np.ndarray, np.ndarray]:
        """
        Get current end-effector velocity in base coordinate frame.
        获取基坐标系下的当前末端执行器速度。

        Returns:
            linear_vel: (3,) in m/s / 线速度：(3,) m/s
            angular_vel: (3,) in rad/s / 角速度：(3,) rad/s
        """
        pass

    @abc.abstractmethod
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

    # ======== Position Control (Mode 0) / 位置控制（模式 0） ========
    @abc.abstractmethod
    def move_to_joint_positions(
        self,
        joint_positions: Union[list, np.ndarray],
        wait: bool = False,
    ) -> bool:
        """
        Perform point-to-point joint motion with internal trajectory planning.
        执行带内部轨迹规划的点到点关节运动。

        Args:
            joint_positions: (N,) target angles in radians / (N,) 目标关节角（弧度）
            wait: Block until motion completes if True / 若为 True，阻塞等待运动完成

        Returns:
            True if successful / 成功返回 True
        """
        pass

    @abc.abstractmethod
    def move_to_ee_pose(
        self,
        pose:Union[list,np.ndarray],
        is_radian: bool = False,
        wait: bool = False
    ):
        pass

    @abc.abstractmethod
    def move_to_ee_pose_rpy(
        self,
        position: Union[List[float], np.ndarray],
        rpy: Union[List[float], np.ndarray],
        is_radian: bool,
        wait: bool = False,
    ) -> bool:
        """
        Perform point-to-point Cartesian motion.
        执行点到点笛卡尔空间运动。

        Args:
            position: (3,) target position in meters (base frame) / (3,) 目标位置（米，基坐标系）
            rpy: (4,) target rpy [roll, pitch, yaw] 
            wait: Block until motion completes if True / 若为 True，阻塞等待运动完成

        Returns:
            True if successful / 成功返回 True
        """
        pass

    @abc.abstractmethod
    def move_to_ee_pose_quat(
        self,
        position: Union[List[float], np.ndarray],
        orientation: Union[List[float], np.ndarray],
        wait: bool = False,
    ) -> bool:
        """
        Perform point-to-point Cartesian motion.
        执行点到点笛卡尔空间运动。

        Args:
            position: (3,) target position in meters (base frame) / (3,) 目标位置（米，基坐标系）
            orientation: (4,) target quaternion [x, y, z, w] / (4,) 目标四元数 [x, y, z, w]
            wait: Block until motion completes if True / 若为 True，阻塞等待运动完成

        Returns:
            True if successful / 成功返回 True
        """
        pass

    # ======== Servo Control (Mode 1) / 伺服控制（模式 1） ========
    @abc.abstractmethod
    def servo_to_joint_positions(
        self,
        joint_positions: Union[list, np.ndarray],
    ) -> bool:
        """
        Real-time joint servo control. Must be called at high frequency (e.g., 100 Hz).
        实时关节伺服控制。必须以高频调用（例如 100 Hz）。

        Args:
            joint_positions: (N,) target angles in radians / (N,) 目标关节角（弧度）

        Returns:
            True if command accepted / 指令被接受则返回 True
        """
        pass

    @abc.abstractmethod
    def servo_to_ee_pose(
        self,
        position: Union[list, np.ndarray],
        orientation: Union[list, np.ndarray],
    ) -> bool:
        """
        Real-time Cartesian servo control. Must be called at high frequency (e.g., 100 Hz).
        实时笛卡尔伺服控制。必须以高频调用（例如 100 Hz）。

        Args:
            position: (3,) target position in meters (base frame) / (3,) 目标位置（米，基坐标系）
            orientation: (4,) target quaternion [x, y, z, w] / (4,) 目标四元数 [x, y, z, w]

        Returns:
            True if command accepted / 指令被接受则返回 True
        """
        pass

    @abc.abstractmethod
    def go_home(
        self,
    ) -> bool:
        """
        我要回家
        """
        pass