
from scipy.spatial.transform import Rotation as R
import numpy as np
# from rawbestman
def compensate_tcp_for_gripper(x, y, z, quaternion, distance):
    """
    根据夹爪开合引起的沿末端Z轴位移，补偿工具中心点（TCP）位置。
    
    适用于非平动夹爪（如平行夹爪）：夹爪开合时，实际抓取点会沿末端Z轴移动。
    此函数将原始位姿沿局部-Z方向平移 `distance`，得到真实TCP位姿。
    
    Args:
        x, y, z: 当前末端位置（世界坐标系）
        quaternion: 当前末端姿态（[x, y, z, w]）
        distance: 沿末端局部Z轴的补偿距离（正值表示向物体靠近）
    
    Returns:
        新的 (x, y, z, quaternion)
    """
    rotation = R.from_quat(quaternion)
    rotation_matrix = rotation.as_matrix()
    z_axis = rotation_matrix[:, 2]        # 局部Z轴方向（朝向物体）
    new_position = np.array([x, y, z]) - distance * z_axis
    return new_position[0], new_position[1], new_position[2], quaternion


def pose_to_euler(pose):
    '''
    Convert robot pose from a list [x, y, z, qw, qx, qy, qz] to [x, y, z] and Euler angles.
    
    Parameters:
    pose: list of 7 floats - [x, y, z, qw, qx, qy, qz]
    
    Returns:
    tuple: (x, y, z, roll, pitch, yaw) where (x, y, z) is the position and (roll, pitch, yaw) are the Euler angles in radians.
    '''
    x, y, z, qw, qx, qy, qz = pose
    r = R.from_quat([qx, qy, qz, qw])  # Reordering to match scipy's [qx, qy, qz, qw]
    roll, pitch, yaw = r.as_euler('xyz', degrees=False)
    return [x, y, z, roll, pitch, yaw]

def euler_to_pose(self, position_euler):
    '''
    Convert robot pose from [x, y, z, roll, pitch, yaw] to [x, y, z, qw, qx, qy, qz].
    
    Parameters:
    position_euler: list of 6 floats - [x, y, z, roll, pitch, yaw]
    
    Returns:
    list: [x, y, z, qw, qx, qy, qz]
    '''
    x, y, z, roll, pitch, yaw = position_euler
    r = R.from_euler('xyz', [roll, pitch, yaw], degrees=False)
    qx, qy, qz, qw = r.as_quat()  # Getting [qx, qy, qz, qw] from scipy
    return [x, y, z, qw, qx, qy, qz]  # Reordering to match [qw, qx, qy, qz]
    