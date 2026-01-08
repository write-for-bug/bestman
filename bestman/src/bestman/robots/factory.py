# bestman/robots/__init__.py

from typing import Type,Dict
from .config import RobotConfig
from .base_robot import BaseRobot

# 全局注册表
_ROBOT_REGISTRY: Dict[Type[RobotConfig], Type[BaseRobot]] = {}

def register_robot(config_cls: Type[RobotConfig]):
    """用于自动注册 RobotConfig → Robot 的映射"""
    def wrapper(robot_cls: Type[BaseRobot]):
        _ROBOT_REGISTRY[config_cls] = robot_cls
        return robot_cls
    return wrapper



def make_robot_from_config(config: RobotConfig) -> BaseRobot:
    """
    根据 RobotConfig 自动创建对应的机器人实例。
    """
    if not hasattr(config, "type"):
        raise ValueError(
            f"Config {type(config).__name__} must define 'type' "
            "to specify the robot implementation."
        )
    robot_class = _ROBOT_REGISTRY.get(type(config))
    if robot_class is None:
        raise ValueError(
            f"Unsupported robot config type: {type(config).__name__}. "
            f"Available: {[cls.__name__ for cls in _ROBOT_REGISTRY.keys()]}"
        )
    
    # 返回BestMan封装实例
    return robot_class(config)