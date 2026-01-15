"""BestManRobotics - Unified Python wrapper for robotic arm SDKs."""

__author__ = """ark"""
__email__ = 'zlj15058114997@gmail.com'
__version__ = '0.1.0'

# 核心API导出
from bestman.robots import BaseRobot, RobotConfig, make_robot_from_config

__all__ = [
    "BaseRobot",
    "RobotConfig",
    "make_robot_from_config",
]
