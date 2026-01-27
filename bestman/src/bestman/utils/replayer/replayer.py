import numpy as np
import os
from ..file_utils import select_multi_sessions_dir,select_session_subdir
from ..utils import map_sensor_to_robot
import time
class TrajReplayer:
    def __init__(self,robot=None):
        self.robot = robot

    def load_data(self,data_root):
        dir1 = select_multi_sessions_dir(data_root)#选择multisessions
        selected_session = select_session_subdir(dir1)#选择session
        clamp_path = os.path.join(selected_session,"Clamp_Data","clamp_data_tum.txt")    #"./session_001/Clamp_Data/clamp_data_tum.txt"
        traj_path = os.path.join(selected_session,"Merged_Trajectory","merged_trajectory.txt")#"./session_001/Merged_Trajectory/merged_trajectory.txt"\
       
        try:
            self.raw_clamp = np.loadtxt(clamp_path)
            self.raw_pose = np.loadtxt(traj_path)
            self.pose_timestamps = self.raw_pose[:,0]
            self.raw_pose = self.raw_pose[:,1:]
        except Exception as e:
            print(e)

    def transform_traj(self,T_robot_init):
        self.target_pose = []   
        self.target_clamp_width=[]
        
        clamp_timestamps = self.raw_clamp[:,0]
        umi_clamp_widths = self.raw_clamp[:,-1]

        for i,(p, pose_ts) in enumerate(zip(self.raw_pose,self.pose_timestamps)):

            idx = np.abs(clamp_timestamps - pose_ts).argmin()
            real_width = np.clip(umi_clamp_widths[idx], 0, 88)
            self.target_clamp_width.append(real_width)
            
            self.target_pose.append(map_sensor_to_robot(*p,T_robot_init=T_robot_init))


    

    def replay(self,interval=1,speed_rate=1.0):
        if not hasattr(self,"raw_pose"):
            raise ValueError("call load_data fisrt")
        if not hasattr(self,"target_pose"):
            raise ValueError("call transform_traj fisrt")
        
        if  not hasattr(self,"target_clamp_width") or self.target_clamp_width is None :
            print("clamp miss, replay traj only")
        
        # 1. 下采样
        sampled_indices = slice(0, None, interval)
        sampled_timestamps = self.pose_timestamps[sampled_indices]
        sampled_pose = self.target_pose[sampled_indices]
        sampled_clamp = self.target_clamp_width[sampled_indices]

        # 2. 转为相对时间并应用速率
        # 这里的 timestamps 是每一帧应该被执行的“理想时刻”
        timestamps = (sampled_timestamps - sampled_timestamps[0]) / speed_rate
        
        start_time = time.time()
        total_points = len(sampled_pose)
        
        print(f"开始同步轨迹复现: {total_points} 个点, 预计时长: {timestamps[-1]/speed_rate:.2f} 秒")

        inter_w = sampled_clamp[0]

        for i in range(total_points):
            # 计算当前点应该在什么时候执行
            target_execution_time = timestamps[i]
            
            # 计算当前实际已经过去了多久
            actual_elapsed = time.time() - start_time
            
            # 需要等待的差值
            wait_time = target_execution_time - actual_elapsed
            
            if wait_time > 0:
                time.sleep(wait_time)
            elif wait_time < -0.01:
                # 如果实际耗时已经超过了目标时刻，说明落后于时间表
                print(f"[WARN]: 滞后于时间轴 {abs(wait_time):.3f}s (Point {i})")

            # if i % 20 == 0:
            #     inter_w = sampled_clamp[i]

            # 同步执行机器人指令
            # 注意：如果 self._robot_sdk 内部非常耗时，会直接影响下一帧的准时性
            # self._robot_sdk(sampled_pose[i], inter_w)
            self.robot.servo_to_ee_pose(sampled_pose[i])
        print("轨迹复现完成")

