from glob import glob
from typing import Dict,Tuple
import os
import shutil
from envreward_utils import dump_json,read_config
import numpy as np

ORI_DATAPATH = "../../../Webots_Simulation/traffic_project/droneVideos/"
ENVREWARD_DATAPATH = "./EnvReward_Dataset/"
DRONE_PREFIX = "DRONE"
EPISODE_PREFIX = "episode"
CFG_PATH = "./envreward_cfg.json"
REWARD_JSON = "reward.json"
ACTION_JSON = "action.json"

"""
    Get data volume of dataset sample from simulator
    Input:
        path(str): path of origin data from simulator
    Output:
        data_volume_dict: dictation of drone and episode(e.g: Dict("Drone0",Dict("episode0",666)) )
"""
def get_datavolume(mode:str,path = ORI_DATAPATH)->Dict[str,Dict[str,int]]:
    data_volume_dict = {}
    drone_list = glob(path+DRONE_PREFIX+"*/")
    drone_num = len(drone_list)
    if mode.lower() == "train":
        for drone_idx in range(drone_num-1):
            drone_volume = {}
            droneidx_path = path+DRONE_PREFIX+str(drone_idx)+"/"
            episode_len = len(glob(droneidx_path+EPISODE_PREFIX+"*/"))
            for episode_idx in range(episode_len):
                episodeidx_path = droneidx_path+EPISODE_PREFIX+f"{episode_idx}/"
                episode_volume = len(glob(episodeidx_path+"*.jpeg"))
                drone_volume[EPISODE_PREFIX+f"{episode_idx}"] = episode_volume
            data_volume_dict[DRONE_PREFIX+str(drone_idx)] = drone_volume
    elif mode.lower() == "test":
        drone_volume = {}
        droneidx_path = path+DRONE_PREFIX+str(drone_num-1)+"/"
        episode_len = len(glob(droneidx_path+EPISODE_PREFIX+"*/"))
        for episode_idx in range(episode_len):
            episodeidx_path = droneidx_path+EPISODE_PREFIX+f"{episode_idx}/"
            episode_volume = len(glob(episodeidx_path+"*.jpeg"))
            drone_volume[EPISODE_PREFIX+f"{episode_idx}"] = episode_volume
        data_volume_dict[DRONE_PREFIX+str(drone_num-1)] = drone_volume
    else:
        raise AttributeError(f"Mode:{mode} is illegal! Legal ones: train and test")
    return data_volume_dict

def get_total_idx(data_volume_dict:Dict[str,Dict[str,int]],dronevolume:Dict[str,int],drone_idx:int,episode_idx:int,img_idx:int)->Tuple[str, bool]:
    real_idx = 0
    final_flag = False
    for drone_id in range(drone_idx):
        real_idx += dronevolume[DRONE_PREFIX+str(drone_id)]
    for episode_id in range(episode_idx):
        real_idx += data_volume_dict[DRONE_PREFIX+str(drone_idx)][EPISODE_PREFIX+str(episode_id)]
    if img_idx >= data_volume_dict[DRONE_PREFIX+str(drone_idx)][EPISODE_PREFIX+str(episode_idx)]:
        raise IndexError(f"Image Index Out of range! Index:{img_idx} while episode volume:{data_volume_dict[DRONE_PREFIX+str(drone_idx)][EPISODE_PREFIX+str(episode_idx)]}")
    real_idx += img_idx
    if img_idx == data_volume_dict[DRONE_PREFIX+str(drone_idx)][EPISODE_PREFIX+str(episode_idx)]-1:
        final_flag = True
    return f"{real_idx:07d}",final_flag

def get_test_idx(data_volume_dict:Dict[str,Dict[str,int]],episode_idx:int,img_idx:int)->Tuple[str, bool]:
    real_idx = 0
    final_flag = False
    drone_str = list(data_volume_dict.keys())[0]
    for episode_id in range(episode_idx):
        real_idx += data_volume_dict[drone_str][EPISODE_PREFIX+str(episode_id)]
    if img_idx >= data_volume_dict[drone_str][EPISODE_PREFIX+str(episode_idx)]:
        raise IndexError(f"Image Index Out of range! Index:{img_idx} while episode volume:{data_volume_dict[drone_str][EPISODE_PREFIX+str(episode_idx)]}")
    real_idx += img_idx
    if img_idx == data_volume_dict[drone_str][EPISODE_PREFIX+str(episode_idx)]-1:
        final_flag = True
    return f"{real_idx:07d}",final_flag

def generate_dataset(dronevolume:Dict[str,int],datavolume_dict:Dict[str,Dict[str,int]],num_classes:int,mode:str):
    end_img_dict = {}
    reward_dict = {}
    action_dict = {}
    for drone_name in dronevolume.keys():
        drone_idx = int(drone_name.replace(DRONE_PREFIX,""))
        for episode_name in datavolume_dict[drone_name].keys():
            episode_idx = int(episode_name.replace(EPISODE_PREFIX,""))
            image_path_list = glob(ORI_DATAPATH+DRONE_PREFIX+str(drone_idx)+"/"+EPISODE_PREFIX+str(episode_idx)+"/*.jpeg")
            image_list = [os.path.basename(f) for f in image_path_list]
            ra_json_path = ORI_DATAPATH+DRONE_PREFIX+str(drone_idx)+"/"+EPISODE_PREFIX+str(episode_idx)+"/mark.json"
            reward_action_json = read_config(ra_json_path)
            for idx,img_name in enumerate(image_list):
                image_idx = int(img_name.replace(".jpeg", ""))
                if mode.lower() == "train":
                    real_idx_str,final_flag = get_total_idx(datavolume_dict,dronevolume,drone_idx,episode_idx,image_idx)
                elif mode.lower() == "test":
                    real_idx_str,final_flag = get_test_idx(datavolume_dict,episode_idx,image_idx)
                else:
                    raise AttributeError(f"Mode:{mode} is illegal! Legal ones: train and test") 
                if final_flag:
                    end_img_dict[DRONE_PREFIX+str(drone_idx)+"_"+EPISODE_PREFIX+str(episode_idx)]=ENVREWARD_DATAPATH+mode+"/"+real_idx_str+".jpeg"
                else:
                    reward_action_l = reward_action_json[f"{image_idx:06d}"] # [reward,action]
                    # reward_dict[real_idx_str] = reward_action_l[0]
                    # action_dict[real_idx_str] = value2onehot(num_classes,int(reward_action_l[1]))
                    reward_dict[real_idx_str] = reward_action_l
                    action_dict[real_idx_str] = value2onehot(num_classes,0)
                
                src_path = image_path_list[idx]
                dst_path = ENVREWARD_DATAPATH+mode+"/"+real_idx_str+".jpeg"
                if not os.path.exists(ENVREWARD_DATAPATH):
                    os.makedirs(ENVREWARD_DATAPATH)
                if not os.path.exists(ENVREWARD_DATAPATH+mode):
                    os.makedirs(ENVREWARD_DATAPATH+mode)
                shutil.copy(src_path,dst_path)

    sorted_reward_dict = dict(sorted(reward_dict.items()))
    sorted_action_dict = dict(sorted(action_dict.items()))
    json_path = ENVREWARD_DATAPATH+mode+"/end_img.json"
    reward_json_path = ENVREWARD_DATAPATH+mode+"/"+REWARD_JSON
    action_json_path = ENVREWARD_DATAPATH+mode+"/"+ACTION_JSON
    dump_json(end_img_dict,json_path)
    dump_json(sorted_reward_dict,reward_json_path)
    dump_json(sorted_action_dict,action_json_path)
    
def value2onehot(num_classes:int,value:int):
    one_hot = list(np.zeros(num_classes))
    one_hot[value] = 1.0
    return one_hot

def del_currfile(mode:str):
    ### Delete Current exists dataset
    if os.path.exists(ENVREWARD_DATAPATH+mode.lower()+"/"):
        jpeg_files = glob(os.path.join(ENVREWARD_DATAPATH+mode.lower()+"/", "*.jpeg"))
        # Check if dataset exists
        if jpeg_files:
            for file in jpeg_files:
                os.remove(file)
        json_files = glob(os.path.join(ENVREWARD_DATAPATH+mode.lower()+"/", "*.json"))
        if json_files:
            for j_file in json_files:
                os.remove(j_file)

def main(mode:str):
    datavolume_dict = get_datavolume(mode=mode)
    dronevolume = {}
    for key in datavolume_dict.keys():
        dronevolume[key] = sum(datavolume_dict[key].values())
    del_currfile(mode=mode)
    cfg_dict = read_config(CFG_PATH)
    num_classes = cfg_dict["Action_dim"]
    generate_dataset(dronevolume,datavolume_dict,num_classes,mode=mode)


if __name__ == "__main__":
    main("train")
    main("test")



    
    