# servo_circular_pose_demo.py
from bestman.robots.xarm import XArmConfig, BestmanXarm
import time
import numpy as np

# === 配置 ===
config = XArmConfig(
    id="my_xarm",
    dof=7,
    initial_joints=[0., 0., 0., 0., -180., 90., -180.],
    tcp_offset=[0., 0., 174.435, 0., 0., 0.],  # mm
    sdk_kwargs={"port": "192.168.1.235", "is_radian": False}
)

robot = BestmanXarm(config)

# === 圆周参数 ===
FREQ = 200          # 控制频率
TOTAL_TIME = 10.0    # 秒
CIRCLE_AXIS = 'z'   # 绕工具坐标系的 x/y/z 轴旋转
AMPLITUDE_DEG = 15  # 最大偏转角度（度）
CIRCLE_FPS = 0.5    # 圆周频率（Hz），即每秒画多少圈

try:
    robot.connect()
    print("Going to home...")
    robot.go_home()

    # 获取当前末端位姿（作为圆心）
    pose = robot.get_ee_pose()  # [x, y, z, roll, pitch, yaw] in degrees if is_radian=False
    center_pos = pose[:3].copy()
    base_rpy = np.array(pose[3:6])  # base orientation

    print(f"Circle center: {center_pos}, base RPY: {base_rpy}")

    # 切换到伺服模式
    robot.arm.set_mode(1)  # servo mode
    time.sleep(0.2)

    dt = 1.0 / FREQ
    steps = int(TOTAL_TIME * FREQ)
    t_start = time.perf_counter()

    for i in range(steps):
        t = i * dt
        # 计算当前旋转角度（弧度）
        theta = 2 * np.pi * CIRCLE_FPS * t
        offset_deg = AMPLITUDE_DEG * np.sin(theta)

        # 构建绕指定轴的偏移
        rpy_offset = np.zeros(3)
        if CIRCLE_AXIS == 'x':
            rpy_offset[0] = offset_deg
        elif CIRCLE_AXIS == 'y':
            rpy_offset[1] = offset_deg
        elif CIRCLE_AXIS == 'z':
            rpy_offset[2] = offset_deg
        else:
            raise ValueError("CIRCLE_AXIS must be 'x', 'y', or 'z'")

        # 目标姿态 = 基础姿态 + 偏移
        target_rpy = base_rpy + rpy_offset
        target_pose = np.concatenate([center_pos, target_rpy])

        # 发送伺服指令（注意：xArm SDK 的 set_servo_cartesian 默认使用与初始化相同的单位）
        # robot.arm.set_servo_cartesian(target_pose.tolist())
        print(target_rpy)
        # 精确 timing
        elapsed = time.perf_counter() - t_start
        sleep_time = (i + 1) * dt - elapsed
        if sleep_time > 0:
            time.sleep(sleep_time)

    print("Circle motion finished.")

except KeyboardInterrupt:
    print("Keyboard interrupt received.")
except Exception as e:
    print(f"Error: {e}")
finally:
    # 安全回退
    robot.arm.set_mode(0)  # 回到位置模式
    robot.arm.set_state(0)
    time.sleep(0.1)
    robot.go_home()
    robot.disconnect()