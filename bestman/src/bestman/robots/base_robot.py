import abc
from typing import Any, Dict, Union, Tuple, List
import numpy as np

from .config import RobotConfig


class BaseRobot(abc.ABC):
    """
    Universal robot hardware abstraction interface.
    通用机器人硬件抽象接口。

    This class defines a standardized API for:
    - State observation (joints, EE pose, gripper)
    - Position control (planned point-to-point motion)
    - Servo control (real-time high-frequency command streaming)

    该类目前实现的标准化的 API：
    - 状态观测（关节、末端位姿、夹爪）
    - 位置控制（带规划的点到点运动）
    - 伺服控制（实时高频指令流）

    Basic interface summary / 基本接口概览:
    - Lifecycle:          connect(), disconnect()
    - State reading:      get_joint_positions(), get_ee_pose(), get_gripper_position(), etc.
    - Position control:   move_to_joint_positions(), move_to_ee_pose_rpy(), move_to_ee_pose_quat()
    - Servo control:      servo_to_joint_positions(), servo_to_ee_pose_rpy(), servo_to_ee_pose_quat()
    - Utility:            go_home()

    基础接口包括：
    - 生命周期管理:      connect(), disconnect()
    - 状态读取:         get_joint_positions(), get_ee_pose(), get_gripper_position() 等
    - 位置控制:         move_to_joint_positions(), move_to_ee_pose_rpy(), move_to_ee_pose_quat()
    - 伺服控制:         servo_to_joint_positions(), servo_to_ee_pose_rpy(), servo_to_ee_pose_quat()
    - 工具方法:         go_home()
    """

    config_class: type[RobotConfig]

    def __init__(self, config: RobotConfig):
        self.config = config

    # ======== Inference Related / 推理相关 ========
    @property
    @abc.abstractmethod
    def observation_features(self) -> Dict[str, Any]:
        """
        Declare the structure and shape of observation data.
        声明观测数据的结构与形状。

        Returns:
            A dictionary mapping feature names to their expected shapes or types.
            返回一个字典，键为特征名，值为其预期形状或类型。

        Example:
        {
            "joint_pos": (6,),        # Joint angles in radians / 关节角（弧度）
            "joint_vel": (6,),        # Joint velocities in rad/s / 关节速度（rad/s）
            "eef_pos": (7,),          # EE pose as [x, y, z, qx, qy, qz, qw] / 末端位姿（四元数）
            "eef_vel": (6,),          # EE velocity [vx, vy, vz, wx, wy, wz] / 末端速度
            "gripper_position": float,# Normalized [0.0, 1.0] (0=open, 1=closed) / 归一化夹爪位置
            "image_hand": (480, 640, 3)# RGB image array / RGB 图像数组
        }
        """
        pass

    @property
    @abc.abstractmethod
    def action_features(self) -> Dict[str, Any]:
        """
        Declare the structure and shape of action commands.
        声明动作指令的结构与形状。

        Returns:
            A dictionary mapping action names to their expected shapes or types.
            返回一个字典，键为动作名，值为其预期形状或类型。

        Example:
        {
            "joint_targets": (6,),     # Target joint angles in radians / 目标关节角（弧度）
            "gripper_command": float   # Gripper command, normalized [0.0, 1.0] / 夹爪指令（归一化）
        }
        """
        pass

    @abc.abstractmethod
    def get_observation(self) -> Dict[str, Any]:
        """
        Retrieve a full observation dictionary matching `observation_features`.
        获取与 `observation_features` 定义完全匹配的完整观测字典。

        Returns:
            Dict[str, Any]: Observation data with keys and shapes as declared.
            返回包含声明键和形状的观测数据字典。
        """
        pass

    # ======== Lifecycle / 生命周期 ========
    @abc.abstractmethod
    def connect(self) -> None:
        """
        Establish a connection to the physical robot hardware.
        建立与物理机器人硬件的连接。

        Raises:
            ConnectionError: If connection fails.
            连接失败时抛出 ConnectionError。
        """
        pass

    @abc.abstractmethod
    def disconnect(self) -> None:
        """
        Safely disconnect from the robot and release all resources.
        安全断开与机器人的连接并释放所有相关硬件资源。

        Note:
            Should be called in a `finally` block or context manager.
            应在 `finally` 块或上下文管理器中调用。
        """
        pass

    # ======== Read State Interface / 状态读取接口 ========
    @abc.abstractmethod
    def get_joint_positions(self) -> np.ndarray:
        """
        Get current joint angles in radians.
        获取当前关节角（弧度制）。

        Returns:
            np.ndarray: Shape (N,), where N is the number of degrees of freedom.
            返回形状为 (N,) 的 NumPy 数组，N 为自由度数。
        """
        pass

    @abc.abstractmethod
    def get_joint_velocities(self) -> np.ndarray:
        """
        Get current joint angular velocities in rad/s.
        获取当前关节角速度（单位：rad/s）。

        Returns:
            np.ndarray: Shape (N,), angular velocities in rad/s.
            返回形状为 (N,) 的角速度数组（rad/s）。
        """
        pass

    @abc.abstractmethod
    def get_ee_pose(self) -> np.ndarray:
        """
        Get current end-effector pose in the base coordinate frame.
        获取基坐标系下的当前末端执行器位姿。

        Returns:
            np.ndarray: Shape (6,), [x, y, z, roll, pitch, yaw] in meters and radians.
            返回形状为 (6,) 的数组：[x, y, z, roll, pitch, yaw]（米 + 弧度）。
        """
        pass

    @abc.abstractmethod
    def get_ee_velocity(self) -> Tuple[np.ndarray, np.ndarray]:
        """
        Get current end-effector linear and angular velocity in base frame.
        获取基坐标系下的当前末端执行器线速度与角速度。

        Returns:
            Tuple[np.ndarray, np.ndarray]:
                - linear_vel: (3,) in m/s
                - angular_vel: (3,) in rad/s
        """
        pass

    @abc.abstractmethod
    def get_gripper_position(self) -> float:
        """
        Get current gripper position.
        获取当前夹爪位置。

        Returns:
            float: Normalized value in [0.0, 1.0], where 0.0 = fully open, 1.0 = fully closed.
                   或物理单位（如 mm），但需在同型号机器人中保持一致。
            返回归一化值 [0.0, 1.0]（0.0=全开，1.0=全闭），
            或物理单位（如 mm），但同一机器人型号需保持一致。
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
        Perform planned point-to-point joint motion.
        执行带内部轨迹规划的点到点关节运动。

        Args:
            joint_positions: Target joint angles in radians, shape (N,).
                             目标关节角（弧度），形状 (N,)。
            wait: If True, block until motion completes. Default: False.
                  若为 True，则阻塞等待运动完成。默认：False。

        Returns:
            bool: True if motion was successfully initiated.
        """
        pass

    @abc.abstractmethod
    def move_to_ee_pose(
        self,
        pose: Union[list, np.ndarray],
        is_radian: bool = False,
        wait: bool = False
    ) -> bool:
        """
        Perform planned Cartesian motion to a target pose.
        执行带规划的笛卡尔空间运动至目标位姿。

        Args:
            pose: Target pose as [x, y, z, roll, pitch, yaw]. Units depend on `is_radian`.
                  目标位姿 [x, y, z, roll, pitch, yaw]，单位由 `is_radian` 决定。
            is_radian: If True, orientation is in radians; else in degrees. Default: False.
                       若为 True，姿态用弧度；否则用角度。默认：False。
            wait: Block until motion completes if True. Default: False.
                  若为 True，阻塞等待运动完成。默认：False。

        Returns:
            bool: True if motion was successfully initiated.
                  成功启动运动则返回 True。
        """
        pass

    @abc.abstractmethod
    def move_to_ee_pose_rpy(
        self,
        position: Union[List[float], np.ndarray],
        rpy: Union[List[float], np.ndarray],
        is_radian: bool = False,
        wait: bool = False,
    ) -> bool:
        """
        Perform planned Cartesian motion using position and RPY orientation.
        使用位置和 RPY 姿态执行带规划的笛卡尔空间运动。

        Args:
            position: Target position [x, y, z] in meters (base frame).
                      目标位置 [x, y, z]（米，基坐标系）。
            rpy: Target orientation [roll, pitch, yaw].
                 目标姿态 [roll, pitch, yaw]。
            is_radian: If True, RPY is in radians; else in degrees. Default: False.
                       若为 True，RPY 用弧度；否则用角度。默认：False。
            wait: Block until motion completes if True. Default: False.
                  若为 True，阻塞等待运动完成。默认：False。

        Returns:
            bool: True if motion was successfully initiated.
                  成功启动运动则返回 True。
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
        Perform planned Cartesian motion using position and quaternion orientation.
        使用位置和四元数姿态执行带规划的笛卡尔空间运动。

        Args:
            position: Target position [x, y, z] in meters (base frame).
                      目标位置 [x, y, z]（米，基坐标系）。
            orientation: Target orientation as [x, y, z, w] quaternion.
                         目标四元数姿态 [x, y, z, w]。
            wait: Block until motion completes if True. Default: False.
                  若为 True，阻塞等待运动完成。默认：False。

        Returns:
            bool: True if motion was successfully initiated.
                  成功启动运动则返回 True。
        """
        pass

    # ======== Servo Control (Mode 1) / 伺服控制（模式 1） ========
    @abc.abstractmethod
    def servo_to_joint_positions(
        self,
        joint_positions: Union[list, np.ndarray],
    ) -> bool:
        """
        Send real-time joint angle command for high-frequency servo control.
        发送实时关节角指令，用于高频伺服控制。

        Note:
            Must be called at high frequency (e.g., 100–500 Hz) to maintain stability.
            必须以高频（如 100–500 Hz）调用以维持稳定性。

        Args:
            joint_positions: Target joint angles in radians, shape (N,).
                             目标关节角（弧度），形状 (N,)。

        Returns:
            bool: True if command was accepted by the driver.
                  指令被驱动器接受则返回 True。
        """
        pass

    @abc.abstractmethod
    def servo_to_ee_pose(
        self,
        pose: Union[list, np.ndarray]
    ) -> bool:
        """
        Send real-time Cartesian pose command for high-frequency servo control.
        发送实时笛卡尔位姿指令，用于高频伺服控制。

        Note:
            Must be called at high frequency (e.g., 100–500 Hz).
            必须以高频（如 100–500 Hz）调用。

        Args:
            pose: Target pose [x, y, z, roll, pitch, yaw] in meters and radians.
                  目标位姿 [x, y, z, roll, pitch, yaw]（米 + 弧度）。

        Returns:
            bool: True if command was accepted.
                  指令被接受则返回 True。
        """
        pass

    @abc.abstractmethod
    def servo_to_ee_pose_rpy(
        self,
        position: Union[list, np.ndarray],
        rpy: Union[list, np.ndarray]
    ) -> bool:
        """
        Send real-time Cartesian command using position and RPY orientation.
        使用位置和 RPY 姿态发送实时笛卡尔指令。

        Note:
            Angles must be in **radians**.
            姿态角度必须使用 **弧度**。

        Args:
            position: Target position [x, y, z] in meters.
                      目标位置 [x, y, z]（米）。
            rpy: Target orientation [roll, pitch, yaw] in radians.
                 目标姿态 [roll, pitch, yaw]（弧度）。

        Returns:
            bool: True if command was accepted.
                  指令被接受则返回 True。
        """
        pass

    @abc.abstractmethod
    def servo_to_ee_pose_quat(
        self,
        position: Union[list, np.ndarray],
        orientation: Union[list, np.ndarray]
    ) -> bool:
        """
        Send real-time Cartesian command using position and quaternion orientation.
        使用位置和四元数姿态发送实时笛卡尔指令。

        Args:
            position: Target position [x, y, z] in meters.
                      目标位置 [x, y, z]（米）。
            orientation: Target orientation as [x, y, z, w] quaternion.
                         目标四元数 [x, y, z, w]。

        Returns:
            bool: True if command was accepted.
                  指令被接受则返回 True。
        """
        pass

    @abc.abstractmethod
    def go_home(self) -> bool:
        """
        Move the robot to its predefined home configuration.
        将机器人移动到预定义的“回家”位姿。

        Returns:
            bool: True if motion was successfully initiated.
                  成功启动运动则返回 True。
        """
        pass