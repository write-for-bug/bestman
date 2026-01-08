# bestman RobotConfig基类
import abc
from dataclasses import dataclass
from pathlib import Path
from typing import Literal, Dict, Any, Optional, ClassVar, List

import draccus

@dataclass(kw_only=True)
class RobotConfig(draccus.ChoiceRegistry, abc.ABC):
    """
    通用机器人配置基类
    子类通过 @draccus.register 注册，由 type 字段自动选择
    """
    # 机器人唯一标识（用于日志/校准）
    id: str | None = None
    
    # 透传给 原SDK 的参数
    sdk_kwargs: Dict[str, Any] = draccus.field(default_factory=dict)

    # 子类必须声明必需的 sdk_kwargs 键, （声明sdk包装必要的参数名）
    necessary_kwargs: ClassVar[List[str]] = []

    # 自由度
    dof: int = 6
    initial_joints: Optional[List[float]] = None
    tcp_offset: Optional[List[float]] = None

    def __post_init__(self):
        '''kwargs checking'''
        missing_kwargs = set(self.necessary_kwargs) - set(self.sdk_kwargs.keys())
        if missing_kwargs:
            raise ValueError(
                f"Missing required sdk_kwargs for {self.type}: {sorted(missing_kwargs)}. "
                f"Required: {self.necessary_kwargs}, Got: {list(self.sdk_kwargs.keys())}"
            )
        if len(self.initial_joints)!=self.dof:
            raise ValueError(
                f"initial_joints needs to be length {self.dof}, got {len(self.initial_joints)}"
            )

        if hasattr(self, "cameras") and self.cameras:
            for _, config in self.cameras.items():
                for attr in ["width", "height", "fps"]:
                    if getattr(config, attr) is None:
                        raise ValueError(
                            f"Specifying '{attr}' is required for the camera to be used in a robot"
                        )
        if hasattr(self, "gripper") and self.gripper:
            # TODO
            pass

    @property
    def type(self) -> str:
        """返回注册时的名称（如 'xarm'）"""
        return self.get_choice_name(self.__class__)