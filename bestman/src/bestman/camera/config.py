# bestman RobotConfig基类
import abc
from dataclasses import dataclass
from pathlib import Path
from typing import Literal, Dict, Any, Optional, ClassVar, List

import draccus

@dataclass(kw_only=True)
class CameraConfig(draccus.ChoiceRegistry, abc.ABC):
    """
    camera配置基类
    """
    # 机器人唯一标识（用于日志/校准）
    id: str | None = None
    height: int = None
    width: int = None
    fps: int = None

    # 透传给 原SDK 的参数
    sdk_kwargs: Dict[str, Any] = draccus.field(default_factory=dict)
    # 子类必须声明必需的 sdk_kwargs 键, （声明原sdk必要的参数名）
    necessary_kwargs: ClassVar[List[str]] = []

    # 自由度
    dof: int = 6



    @property
    def type(self) -> str:
        """返回注册时的名称（如 'realsense'）"""
        return self.get_choice_name(self.__class__)