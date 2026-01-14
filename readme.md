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
    camera:CameraConfig = None,#future后续也许添加摄像头配置
    gripper:GripperConfig = None,#future
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
robot= BestmanPiper(config)
```

连接

```
robot.connect()
```





🔧 Startouch 

目前startouch仅在python310下提供动态链接库，其他版本链接库后续会放进来

实例化机器人配置类：

```
from bestman.robots.startouch import StarTouchConfig
config = StarTouchConfig(
    id="my_startouch",
    dof=6,
    initial_joints=[0., 0., 0., 0., 0., 0.],
    tcp_offset=[0., 0., 0., 0., 0., 0.],
    sdk_kwargs={"port":"can0"}#透传给原SDK的参数，不同机械臂的sdk_kwargs会有区别，参数不对会通过内部的necessary_kwargs报出错误并提示sdk需要的参数
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

  



# 接口说明

### 初始化相关类

RobotConfig类

```
config = XArmConfig(
    id="my_xarm",#名字，后续用于debug
    dof=7,#自由度
    initial_joints=[0., 0., 0., 0., -180., 90., -180.],#初始化关节，home关节
    tcp_offset=[0., 0., 0., 0., 0., 0.],# 配置tool point center 通常默认法兰中心
    sdk_kwargs={"port":"192.168.1.235","is_radian":False}#透传给原SDK的参数
)
```

使用config类初始化机器人实例

```
# 使用具体基类初始化
robot= BestmanXarm(config)
# 通过工厂函数初始化
# from bestman.robots import make_robot_from_config
# robot = make_robot_from_config(config)
```

### 生命周期管理

```
robot_instance.connect()	#统一连接接口
robot_instance.disconnect() #断开连接以及释放相关硬件资源
```



### 状态观测接口

```
robot_instance.get_joint_positions()#返回关节状态(6,)或者(7,) List[float]，后续增加单位配置功能
robot_instance.get_ee_pose()#返回tcp姿态(6,)List[float]
robot_instance.get_gripper_position()#返回夹爪状态

robot_instance.get_joint_velocities()#返回关节速度
```

### 控制接口

> 目前仅支持位置控制和伺服务控制两种模式

- #### 位置控制接口

  > 低频使用（1-10Hz），可选择阻塞或非阻塞调用，任务间转移或初始化时使用

  ```
  #关节位置控制[j1,j2,j3,j4,j5,j6...]
  robot_instance.move_to_joint_positions(joint_positions,radians=False,wait=True)
  
  #末端位置控制 pose=[x(m),y(m),z(m),roll,pitch,yaw] (deg or rad)
  robot_instance.move_to_ee_pose(pose, is_radian=False, wait=False)
  
  #末端位置控制 position=[x(m),y(m),z(m)],rpy=[roll,pitch,yaw]
  move_to_ee_pose_rpy(position, rpy, is_radian=False, wait=False)
  
  #末端位置控制 position=[x(m),y(m),z(m)], orientation=[x,y,z,w]适配umi数据格式
  move_to_ee_pose_quat(position, orientation, wait=False)
  ```

  

- #### 伺服控制接口

  > 必须高频调用（>=30Hz）,实时性要求高的场景下使用

  ```
  #关节伺服控制[j1,j2,j3,j4,j5,j6...]
  robot_instance.servo_to_joint_positions(joint_positions,radians=False,wait=True)
  
  #末端伺服控制 pose=[x(m),y(m),z(m),roll,pitch,yaw] (deg or rad)
  robot_instance.servo_to_ee_pose(pose, is_radian=False, wait=False)
  
  #末端伺服控制 position=[x(m),y(m),z(m)],rpy=[roll,pitch,yaw]
  robot_instance.servo_to_ee_pose_rpy(position, rpy, is_radian=False, wait=False)
  
  #末端伺服控制 position=[x(m),y(m),z(m)], orientation=[x,y,z,w]适配umi数据格式
  robot_instance.servo_to_ee_pose_quat(position, orientation, wait=False)
  ```





📌 版本兼容性说明  
本项目不严格地测试于 Python 3.10



目前支持的wrapper：XArm6、XArm7、StarTouch

