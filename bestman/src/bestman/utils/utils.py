
from scipy.spatial.transform import Rotation as R

import numpy as np

def quat2T(qpose):
    pos = qpose[:3]
    rot_matrix = R.from_quat(qpose[3:7]).as_matrix()
    T = np.eye(4)
    T[:3, :3] = rot_matrix
    T[:3, 3] = pos
    return T

def rpy2T(pose):
    pos = pose[:3]
    rot_matrix = R.from_euler('xyz', pose[3:]).as_matrix()
    T = np.eye(4)
    T[:3, :3] = rot_matrix
    T[:3, 3] = pos
    return T


def map_sensor_to_robot(x, y, z, qx, qy, qz, qw, T_robot_init,degrees=False):

    T_sensor_relative = quat2T([x, y, z, qx, qy, qz, qw])

    T_final = T_robot_init @ T_sensor_relative
    
   
    pos_final = T_final[:3, 3]
    euler_final = R.from_matrix(T_final[:3, :3]).as_euler('xyz', degrees=degrees)
    
    return list(pos_final)+list( euler_final)







def transform_to_base_quat(x, y, z, qx, qy, qz, qw, T_base_to_local,dgrees=False):
    '''transform the pose of fastumi to robot base
        unit:m
    '''
    rotation_local = R.from_quat([qx, qy, qz, qw]).as_matrix()
    T_local = np.eye(4)
    T_local[:3, :3] = rotation_local
    T_local[:3, 3] = [x, y, z]
    
    T_base_r = np.matmul(T_local[:3, :3] , T_base_to_local[:3, :3] )
    
    x_base, y_base, z_base = T_base_to_local[:3, 3] + T_local[:3, 3]
    rotation_base = R.from_matrix(T_base_r)
    roll_base, pitch_base, yaw_base = rotation_base.as_euler('xyz', degrees=dgrees)
    return x_base, y_base, z_base,  roll_base, pitch_base, yaw_base





import numpy as np
from scipy.spatial.transform import Rotation as R

def load_trajectory(
    traj_path: str,
    clamp_path: str
) :
    '''read traj(x,y,z,qx,qy,qz,qw) and clamp width'''
    try:
        raw_clamp = np.loadtxt(clamp_path)
        raw_pose = np.loadtxt(traj_path)
        pose_timestamps = raw_pose[:,0]
        raw_pose = raw_pose[:,1:]
    except Exception as e:
        print(e)
    return raw_pose, raw_clamp, pose_timestamps

def transform_traj(raw_pose, raw_clamp, pose_timestamps, T_robot_init):
    '''unit:mm'''
    target_poses = []   
    target_clamp_widths=[]
    
    clamp_timestamps = raw_clamp[:,0]
    umi_clamp_widths = raw_clamp[:,-1]

    for i,(p, pose_ts) in enumerate(zip(raw_pose,pose_timestamps)):

        idx = np.abs(clamp_timestamps - pose_ts).argmin()
        real_width = np.clip(umi_clamp_widths[idx], 0, 88)
        target_clamp_widths.append(real_width)
        
        target_poses.append(map_sensor_to_robot(*p,T_robot_init=T_robot_init))

    return target_poses, target_clamp_widths

def transform_to_base_quat(x, y, z, qx, qy, qz, qw, T_base_to_local,dgrees=False):
    '''transform the pose of fastumi to robot base
        unit:m
    '''
    rotation_local = R.from_quat([qx, qy, qz, qw]).as_matrix()
    T_local = np.eye(4)
    T_local[:3, :3] = rotation_local
    T_local[:3, 3] = [x, y, z]
    
    T_base_r = np.matmul(T_local[:3, :3] , T_base_to_local[:3, :3] )
    
    x_base, y_base, z_base = T_base_to_local[:3, 3] + T_local[:3, 3]
    rotation_base = R.from_matrix(T_base_r)
    roll_base, pitch_base, yaw_base = rotation_base.as_euler('xyz', degrees=dgrees)
    return x_base, y_base, z_base,  roll_base, pitch_base, yaw_base






def transform_vive_to_gripper(qpos):
    """
    完整转换链：VIVE → VIVE_FLAT → XV → Gripper
    
    参数：
        qpos: list or array, [x, y, z, qx, qy, qz, qw]
    
    返回：
        list, [x, y, z, qx, qy, qz, qw] in Gripper coordinate
    """
    # 定义 VIVE 到 VIVE_FLAT 的变换
    TRANSFORMATION = np.eye(4)
    TRANSFORMATION[:3, :3] = R.from_euler('xyz', [30, 0, 0], degrees=True).as_matrix()
    
    # VIVE → VIVE_FLAT
    qpos = VIVE2VIVE_FLAT(qpos, TRANSFORMATION)
    
    # VIVE_FLAT → XV
    qpos = VIVEFLAT2XV(qpos)
    
    # XV → Gripper
    qpos = XV2Gripper(qpos)
    
    return qpos
def VIVE2VIVE_FLAT(qpos, TRANSFORMATION):
    """
    qpos : x y z qx qy qz qw
    TRANSFORMATION: VIVE iv VIVE flat
    """
    M = qpos2mat(qpos)
    M_flat = np.dot(np.dot(TRANSFORMATION, M), np.linalg.inv(TRANSFORMATION))
    return mat2qpos(M_flat)
def XV2Gripper(qpos):
    TRANSFORMATION_MAT = np.array([
        [0, 0, 1, 0],
        [-1, 0, 0, 0],
        [0, -1, 0, 0],
        [0, 0, 0, 1]
    ])
    
    cur_qpos = np.array(qpos)
    cur_mat = qpos2mat(cur_qpos)
    
    #####################################
    left_right_offset = 0.02268
    front_back_offset = 0.08745
    up_down_offset = 0.09240
    #####################################
    cur_qpos[0] -= left_right_offset
    cur_qpos[1] -= up_down_offset
    cur_qpos[2] -= front_back_offset
    
    ori = cur_mat[:3, :3]
    cur_qpos[:3] += ori[:, 0] * left_right_offset
    cur_qpos[:3] += ori[:, 1] * up_down_offset
    cur_qpos[:3] += ori[:, 2] * front_back_offset
    
    cur_mat = qpos2mat(cur_qpos)
    xv_mat_in_gripper =  np.dot(np.dot(TRANSFORMATION_MAT, cur_mat), np.linalg.inv(TRANSFORMATION_MAT))
    return mat2qpos(xv_mat_in_gripper)

def qpos2mat(qpos):
    x, y, z, qx, qy, qz, qw = qpos
    R_mat = R.from_quat([qx, qy, qz, qw]).as_matrix()
    t = np.array([x, y, z])
    M = np.eye(4)
    M[:3, :3] = R_mat
    M[:3, 3] = t
    return M

def mat2qpos(M):
    t = M[:3, 3]
    R_mat = M[:3, :3]
    qx, qy, qz, qw = R.from_matrix(R_mat).as_quat()
    return [t[0], t[1], t[2], qx, qy, qz, qw]

def VIVEFLAT2XV(qpos):
    
    TRANSFORMATION_MAT = np.array([
        [1, 0, 0, 0],
        [0, 0, 1, 0],
        [0, -1, 0, 0],
        [0, 0, 0, 1]
    ])
    
    cur_qpos = np.array(qpos)
    cur_mat = qpos2mat(cur_qpos)
    #############################
    left_right_offset = 0.02220 # original 0.02220
    front_back_offset = -0.04020 # original -0.03820
    up_down_offset = -0.01003 # original -0.01003
    #############################
    cur_qpos[0] -= left_right_offset
    cur_qpos[1] -= front_back_offset
    cur_qpos[2] += up_down_offset
    
    ori = cur_mat[:3, :3]
    cur_qpos[:3] += ori[:, 0] * left_right_offset
    cur_qpos[:3] += ori[:, 1] * front_back_offset
    cur_qpos[:3] -= ori[:, 2] * up_down_offset
    
    cur_mat = qpos2mat(cur_qpos)
    
    vive_mat_in_xv =  np.dot(np.dot(TRANSFORMATION_MAT, cur_mat), np.linalg.inv(TRANSFORMATION_MAT)) 
    return mat2qpos(vive_mat_in_xv)

# ===== Example Usage of Session Selection =====
if __name__ == "__main__":
    try:
        # Step 1: Choose multi_sessions_* root
        multi_root = select_multi_sessions_dir()
        
        # Step 2: Choose session_XXX under it
        selected_session = select_session_subdir(multi_root)
        
        print(f"\n✅ 最终选择路径：\n{selected_session}")
        # → You can now load data from selected_session (e.g., poses, timestamps)
        
    except FileNotFoundError as e:
        print(f"❌ 错误：{e}")