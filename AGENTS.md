# BestMan AGENTS.md

本文件为 AI 编码代理（如 opencode）提供项目指导，确保代码符合项目规范。

---

## 构建和测试命令

### 完整 QA 流程
```bash
cd bestman
just qa
```
运行：代码格式化 → Lint 检查并修复 → 导入排序 → 类型检查 → 完整测试套件

### 测试命令

**运行所有测试：**
```bash
just test
```

**运行单个测试：**
```bash
just test tests/test_bestman.py::test_function
just test tests/ -k "test_name_pattern"
```

**在调试器中运行测试：**
```bash
just pdb tests/test_bestman.py::test_function
```

**多版本测试：**
```bash
just testall
```

**覆盖率测试：**
```bash
just coverage
```

### Lint 和格式化命令

**格式化代码（Ruff）：**
```bash
ruff format .
```

**Lint 检查并自动修复：**
```bash
ruff check . --fix
```

**导入排序（isort）：**
```bash
ruff check --select I --fix .
```

**类型检查（Typer/ty）：**
```bash
ty check .
```

---

## 代码风格指南

### 格式化规则
- **缩进**：4 个空格（Python 文件）
- **行长度限制**：120 字符
- **文件编码**：UTF-8
- **行结束符**：LF（Unix 风格）
- **尾随空格**：禁止
- **文件末尾**：必须有换行符

### 导入顺序
```python
# 1. 标准库
import abc
from typing import Any, Dict, Optional

# 2. 第三方库
import numpy as np
from scipy.spatial.transform import Rotation as R

# 3. 本地导入（从 bestman 包开始）
from bestman.robots.base_robot import BaseRobot
from .config import RobotConfig
```

### 命名约定
- **类名**：PascalCase（如 `BaseRobot`, `XArmConfig`）
- **函数/方法**：snake_case（如 `get_joint_positions`, `move_to_ee_pose`）
- **变量**：snake_case（如 `joint_positions`, `tcp_offset`）
- **常量**：UPPER_SNAKE_CASE（如 `MAX_VELOCITY`）
- **私有成员**：前导下划线（如 `_ROBOT_REGISTRY`, `__post_init__`）

### 类型注解
- **必须使用**：所有公共 API
- **常用类型**：
  - `np.ndarray` - NumPy 数组
  - `Union[list, np.ndarray]` - 可接受的多种类型
  - `Optional[T]` - 可选值
  - `Tuple[np.ndarray, np.ndarray]` - 多返回值
  - `Dict[str, Any]` - 字典
  - `ClassVar[List[str]]` - 类变量

### 文档字符串
- **风格**：Google 风格
- **语言**：中英文双语（英文为主，中文注释关键概念）
- **格式**：Triple-quotes（三引号）
- **必须包含**：
  - 函数/类用途描述
  - Args（参数说明，含类型和单位）
  - Returns（返回值说明）
  - Raises（可能的异常）

### 错误处理
```python
try:
    # 原始 SDK 导入
    from xarm.wrapper import XArmAPI
except ImportError:
    raise ImportError(
        "XArm SDK not installed. Please install via: "
        "pip install bestman[xarm]"
    )

# 配置验证
missing_kwargs = set(self.necessary_kwargs) - set(self.sdk_kwargs.keys())
if missing_kwargs:
    raise ValueError(
        f"Missing required sdk_kwargs for {self.type}: {sorted(missing_kwargs)}. "
        f"Required: {self.necessary_kwargs}, Got: {list(self.sdk_kwargs.keys())}"
    )

# 连接失败处理
try:
    self.arm.connect()
except Exception as e:
    if self.arm:
        self.arm.disconnect()
    self.arm = None
    raise ConnectionError(f"Failed to connect to robot: {e}") from e
```

### 抽象基类模式
```python
import abc
from abc import ABC

class BaseRobot(abc.ABC):
    @abc.abstractmethod
    def connect(self) -> None:
        pass

    @abc.abstractmethod
    def disconnect(self) -> None:
        pass
```

### 工厂模式注册
```python
# 使用装饰器注册
@register_robot(XArmConfig)
class BestmanXarm(BaseRobot):
    config_class = XArmConfig

# Draccus 注册
@RobotConfig.register_subclass("xarm")
@dataclass(kw_only=True)
class XArmConfig(RobotConfig):
    pass
```

### 数据类配置
```python
from dataclasses import dataclass, field

@dataclass(kw_only=True)
class RobotConfig:
    id: str | None = None
    dof: int = 6
    sdk_kwargs: Dict[str, Any] = field(default_factory=dict)
    necessary_kwargs: ClassVar[List[str]] = []

    def __post_init__(self):
        # 验证逻辑
        pass
```

### 单位约定
- **位置**：米
- **角度**：弧度（默认），某些接口支持角度
- **速度**：m/s 或 rad/s
- **时间**：秒
- **夹爪**：归一化 [0.0, 1.0]（0=开，1=关）或物理单位（mm）

### 生命周期管理
```python
# 推荐：使用 try-finally
robot = BestmanXarm(config)
try:
    robot.connect()
    robot.go_home()
finally:
    robot.disconnect()

# 或使用上下文管理器
with BestmanXarm(config) as robot:
    robot.go_home()
```

### 测试要求
- 使用 `pytest` 框架
- 测试文件命名：`test_*.py`
- 测试函数命名：`test_*`
- 使用 fixtures 进行测试设置
- 测试应验证边界条件和错误情况

### 项目依赖管理
- **包管理器**：`uv`
- **Python 版本**：≥3.8（主要在 3.10、3.12、3.13 测试）
- **安装命令**：`pip install -e .`
- **开发依赖**：`pip install -e ".[test]"`

### 关键依赖
- `typer` - CLI 框架
- `draccus` - 配置管理
- `numpy` - 数值计算
- `scipy` - 科学计算
- `pytest` - 测试框架
- `ruff` - Lint 和格式化
- `ty` - 类型检查

### 代码组织结构
```
bestman/
├── src/bestman/
│   ├── __init__.py          # 核心导出
│   ├── robots/               # 机器人实现
│   │   ├── base_robot.py     # 抽象基类
│   │   ├── config.py         # 配置基类
│   │   ├── factory.py        # 工厂函数
│   │   └── [robot_type]/     # 具体实现
│   ├── camera/               # 摄像头支持（未来）
│   └── gripper/              # 夹爪支持（未来）
├── tests/                    # 测试文件
└── examples/                 # 使用示例
```

### 调试建议
- 在测试失败时使用 `just pdb` 进入调试器
- 检查 `bestman.robots.factory._ROBOT_REGISTRY` 确认注册状态
- 使用 `print` 语句记录连接和运动状态
- 验证 `sdk_kwargs` 参数传递给底层 SDK

### 注意事项
1. **连接管理**：始终在 finally 块或上下文管理器中调用 `disconnect()`
2. **模式切换**：调用运动控制前确保机械臂模式正确（0=位置控制，1=伺服控制）
3. **单位一致性**：注意底层 SDK 可能使用不同单位（如 XArm 毫米 vs 本项目米）
4. **高频伺服**：伺服控制必须以高频（≥30Hz）调用以维持稳定性
5. **类型检查**：代码修改后务必运行 `ty check .` 确保类型正确
