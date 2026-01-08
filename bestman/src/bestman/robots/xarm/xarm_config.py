# bestman/config/xarm_config.py
from dataclasses import dataclass, field
from typing import Optional, Dict, Any, List, ClassVar

import draccus

from ..config import RobotConfig  

try:
    from bestman.camera.config import CameraConfig
    from bestman.gripper.config import GripperConfig  
except ImportError as e:
    print("CameraConfig GripperConfig not implemented yes")
@RobotConfig.register_subclass("xarm")
@dataclass(kw_only=True)
class XArmConfig(RobotConfig):  
    """
    xArm 系列机器人配置（支持 xArm6, xArm7 等）
    通过 draccus 自动注册为 type='xarm'
    """
    # ========== 运动参数 ==========
    dof: int = 6               # 默认 6 自由度（可覆盖为 7）

    # ========== 外设配置 ==========TODO
    # cameras: Optional[CameraConfig] = field(default_factory=dict)
    # gripper: Optional[GripperConfig] = None
    gripper = True

    # ========== SDK 透传参数 ==========
    sdk_kwargs: Dict[str, Any] = field(default_factory=dict)

    # ========== SDK 必要参数 通信接口检查 ==========
    necessary_kwargs: ClassVar[List[str]] = ["port"]

    # ========== 初始化参数 ==========
    initial_joints: Optional[List[float]] = None
    tcp_offset: Optional[List[float]] = None
    def __post_init__(self):
        super().__post_init__()
        