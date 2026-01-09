🚀 安装 Bestman 及机器人 SDK

✅ 要求：Python ≥ 3.10

- 创建 Conda 环境（推荐）

  ```
  conda create -n bestman python=3.10 -y
  conda activate bestman

- 安装 bestman 主包（可编辑模式）

```
cd ./bestman
pip install -e .
```

- 按需安装机器人驱动支持

🔧 XArm 支持（UFACTORY）

``` 
pip install bestman[xarm]
```

运行示例：

```
# 在项目根目录下运行
python ./examples/xarm/xarm7/00_init_from_class.py
python ./examples/xarm/xarm7/00_init_from_factory.py

更多示例见 ./examples/xarm/xarm7
```

实例化机器人配置类：

```
from bestman.robots.xarm import XArmConfig
config = XArmConfig(
    id="my_xarm",
    dof=7,
    initial_joints=[0., 0., 0., 0., -180., 90., -180.],
    tcp_offset=[0., 0., 0., 0., 0., 0.],
    sdk_kwargs={"port":"192.168.1.235","is_radian":False}#透传给原SDK的参数
)
```

通过工厂函数初始化

```
from bestman.robots import RobotConfig,make_robot_from_config
robot = make_robot_from_config(config)
```

通过机器人实例初始化：

```
from bestman.robots.xarm import BestmanXarm
robot= BestmanXarm(config)
```

连接

```
robot.connect()
```



🔧 Piper 机械臂支持（AgileX Robotics）

```
pip install bestman[piper]
```

实例化机器人配置类：

```
from bestman.robots.piper import PiperConfig
config = PiperConfig(
    id="my_piper",
    dof=6,
    initial_joints=[0., 0., 0., 0., 0., 0.],
    tcp_offset=[0., 0., 0., 0., 0., 0.],
    sdk_kwargs={"can_port":"can0"}#透传给原SDK的参数
)
```

通过工厂函数初始化

```
from bestman.robots import RobotConfig,make_robot_from_config
robot = make_robot_from_config(config)
```

通过机器人实例初始化：

```
from bestman.robots.piper import BestmanPiper
robot= BestmanXarm(config)
```

连接

```
robot.connect()
```





🔧 Startouch 

```
pip install bestman[startouch]
```

实例化机器人配置类：

```
from bestman.robots.xarm import StarTouchConfig
config = StarTouchConfig(
    id="my_startouch",
    dof=6,
    initial_joints=[0., 0., 0., 0., 0., 0.],
    tcp_offset=[0., 0., 0., 0., 0., 0.],
    sdk_kwargs={"port":"can0"}#透传给原SDK的参数
)
```

通过工厂函数初始化

```
from bestman.robots import RobotConfig,make_robot_from_config
robot = make_robot_from_config(config)
```

通过机器人实例初始化：

```
from bestman.robots.startouch import BestmanStarTouch
robot= BestmanStarTouch(config)
```

连接

```
robot.connect()
```





- 验证安装

```
cd examples
python -c "import bestman; print(bestman.version)"
```



💡 提示

- 所有可选依赖均通过 extras_require 定义，避免不必要的包安装。

- 若遇网络问题，可添加 -i https://pypi.tuna.tsinghua.edu.cn/simple 使用国内镜像。

    



📌 版本兼容性说明  
本项目不严格地测试于 Python 3.10。



目前只有XArm7的wrapper

