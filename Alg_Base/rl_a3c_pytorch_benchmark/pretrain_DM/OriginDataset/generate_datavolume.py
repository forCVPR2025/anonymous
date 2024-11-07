import os
import json
import time

ORIDATASET_PATH = "./OriginDataset/"
EPISODE_PREFIX = "episode"

def Generate_Ori2DataVolume(oridata_path=ORIDATASET_PATH,episode_prefix=EPISODE_PREFIX):
    print("<------ Generating Data Volume ------>")
    start_t = time.time()
    data_volume_dict = {}

    num_episode = 0
    oridata_list = os.listdir(oridata_path)
    for episode_name in oridata_list:
        if episode_prefix in episode_name:
            num_episode += 1

    for episode_idx in range(num_episode):
        file_list = os.listdir(oridata_path+episode_prefix+str(episode_idx))
        num_img = len(file_list)-1
        data_volume_dict[episode_prefix+str(episode_idx)] = num_img


    json_path = oridata_path+"data_volume.json"
    if os.path.exists(json_path):
        os.unlink(json_path)
    with open(json_path, 'w') as json_file:
        json.dump(data_volume_dict, json_file)
    print(f"<------ Finish Generating Data Volume Time Comsume:{time.time()-start_t} ------>\n")

if __name__ == "__main__":
    Generate_Ori2DataVolume()