import os
import shutil
import time

ORIDATASET_PATH = "./OriginDataset/"
VIDEO_PATH = "../../../Webots_Simulation/traffic_project/droneVideos/"
VIDEO_PREFIX = "DRONE"
EPISODE_PREFIX = "episode"
MIN_EPISODE_LEN = 2000

def Generate_Video2Ori(ori_dataset=ORIDATASET_PATH,video_path=VIDEO_PATH,episode_prefix=EPISODE_PREFIX,video_prefix=VIDEO_PREFIX,min_episode_len=MIN_EPISODE_LEN):
    ## if exists data in OriginDataset dir rm the dirs
    print("<------ Generating Drone videos to Origin Dataset ------>")
    start_t = time.time()
    episode_list = os.listdir(ori_dataset)
    for episode_name in episode_list:
        if episode_prefix in episode_name:
            shutil.rmtree(ori_dataset+episode_name)

    video_folders = os.listdir(video_path)
    video_folder_list = []
    for folder_name in video_folders:
        if video_prefix in folder_name:
            video_folder_list.append(folder_name)

    episode_idx = 0
    # get total num of episode
    total_episode = 0
    for folder_name in video_folder_list:
        folder_path = video_path+folder_name
        drone_episode_list = os.listdir(folder_path)
        for idx in range(len(drone_episode_list)):
            episode_path = folder_path+"/"+drone_episode_list[idx]
            if len(os.listdir(episode_path)) > min_episode_len:
                total_episode += 1

    for folder_name in video_folder_list:
        folder_path = video_path+folder_name
        drone_episode_list = os.listdir(folder_path)
        for idx in range(len(drone_episode_list)):
            episode_path = folder_path+"/"+drone_episode_list[idx]
            episode_path_dst = ori_dataset+"episode{}".format(episode_idx)
            ## Judge whether the folder is empty
            if len(os.listdir(episode_path)) > min_episode_len:
                shutil.copytree(episode_path,episode_path_dst)
                os.rename(episode_path_dst+"/mark.json",episode_path_dst+"/Direction_label_src.json")
                episode_idx += 1
                print(f"Finish Generating Episode: {episode_idx}/{total_episode}")
    print(f"<------ Finish Generating Drone videos to Origin Dataset Time Comsume:{time.time()-start_t} ------>\n")

if __name__ == "__main__":
    Generate_Video2Ori()