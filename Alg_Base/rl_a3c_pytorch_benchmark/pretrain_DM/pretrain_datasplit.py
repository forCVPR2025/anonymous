from pretrain_utils import read_config,dump_json
import os
import random
import glob
import shutil
import time

PRETRAIN_ROOT="./"
ORIGIN_DATAPATH="./OriginDataset/"
DATA_VOLUME = ORIGIN_DATAPATH+"data_volume.json"
CFG_PATH="./pretrain_cfg.json"
DYNAMICS_DATAPATH = "./DynamicsDataset/"

class DynamicsDataSplit():
    def __init__(self,mode,data_volume=DATA_VOLUME,cfg_path=CFG_PATH,oridata_path=ORIGIN_DATAPATH) -> None:
        self.oridata_path = oridata_path
        self.volume_dict = read_config(data_volume)
        self.cfg = read_config(cfg_path)
        self.cfg_dict = self.cfg[mode]
        self.bs = self.cfg_dict["Episode_size"]
        self.statebuf = self.cfg_dict["State_Buffer"]
        self.datavolome = self.Acquire_datavolume()

        ### Get train index and test index
        self.train_idx,self.test_idx = self.Acquire_Index()

        ### make 3 dir: base/train/test
        self.base_dir = DYNAMICS_DATAPATH+"Batch{Episode_size}State{State_Buffer}".format(Episode_size=self.bs,State_Buffer=self.statebuf)
        self.train_dir = self.base_dir+"/train/"
        self.test_dir = self.base_dir+"/test/"
        if not os.path.exists(self.base_dir):
            os.makedirs(self.base_dir)
        else:
            shutil.rmtree(self.base_dir)
            time.sleep(1)
            os.makedirs(self.base_dir)
        if not os.path.exists(self.train_dir):
            os.makedirs(self.train_dir)
        if not os.path.exists(self.test_dir):
            os.makedirs(self.test_dir)

    def Acquire_datavolume(self):
        datavolume = 0
        for key in self.volume_dict.keys():
            episode_len = int(self.volume_dict[key]/self.bs)
            datavolume += episode_len
        return datavolume
    
    def Acquire_Index(self):
        idx_list = list(range(self.datavolome))
        train_volume = int(self.cfg_dict["TrainSplit"]*self.datavolome)
        random.shuffle(idx_list)
        
        train_idx = idx_list[:train_volume]
        test_idx = idx_list[train_volume:]
        return train_idx,test_idx
    
    def Split_data(self):
        print("<------ Begin Data Split ------>")
        start_t = time.time()
        ### extract episode data from 
        episode_pathlib = glob.glob(self.oridata_path+"*/")
        episode_pathlib.sort()
        split_idx = 0
        episode_idx = 0
        for episode in episode_pathlib:
            episode_idx += 1
            img_lib = glob.glob(episode+"*.jpeg")
            img_lib.sort() # make sure the img list is in order
            split_idx_single = 0
            ### Split image
            while (split_idx_single+1)*self.bs < len(img_lib):
                curr_split_img = img_lib[split_idx_single*self.bs:(split_idx_single+1)*self.bs]
                if split_idx in self.train_idx:
                    curr_split_path = self.train_dir+"episode{train_idx}".format(train_idx=split_idx)
                    json_path = self.train_dir+"episode{train_idx}".format(train_idx=split_idx)+"/Direction_label.json"
                else:
                    curr_split_path = self.test_dir+"episode{test_idx}".format(test_idx=split_idx)
                    json_path = self.test_dir+"episode{test_idx}".format(test_idx=split_idx)+"/Direction_label.json"

                os.makedirs(curr_split_path)
                for img_path in curr_split_img:
                    shutil.copy(img_path,curr_split_path)
            
                ### Split label
                label_idx_list = list(range(split_idx_single*self.bs,(split_idx_single+1)*self.bs))
                label_json = episode+"Direction_label_src.json"
                label_dict = read_config(label_json)
                curr_label_dict = {}
                
                for index in label_idx_list:
                    label_key = str(index).zfill(6)
                    label_value = label_dict[label_key]
                    curr_label_dict[label_key]=label_value
                
                dump_json(curr_label_dict,json_path)
                # print(split_idx_single)
                # print(split_idx)
                split_idx_single += 1
                split_idx += 1
                print(f"Finish Generating Episode: {episode_idx}/{len(episode_pathlib)} Split: {split_idx_single}/{int(len(img_lib)/self.bs)}")
        print(f"<------ Finish Data Split Time Comsume:{time.time()-start_t} ------>\n")

    # Check the correctness of the data
    def Check_split(self):
        print("<------ Begin Checking Data Split ------>")
        start_t = time.time()
        train_ls = glob.glob(self.train_dir+"*/")
        test_ls = glob.glob(self.test_dir+"*/")
        train_ls.sort()
        test_ls.sort()
        for train_dir_name in train_ls:
            num_img = len(glob.glob(train_dir_name+"*.jpeg"))
            num_json = len(glob.glob(train_dir_name+"*.json"))
            print("train_dir: {} contains {} images and {} json file".format(train_dir_name,num_img,num_json)) 
        for test_dir_name in test_ls:
            num_img_t = len(glob.glob(test_dir_name+"*.jpeg"))
            num_json_t = len(glob.glob(test_dir_name+"*.json"))
            print("train_dir: {} contains {} images and {} json file".format(test_dir_name,num_img_t,num_json_t))
        print("Number of train episode is {}".format(len(train_ls)))
        print("Number of test episode is {}".format(len(test_ls)))
        print(f"<------ Finish Checking Data Split Time Comsume:{time.time()-start_t} ------>\n")



if __name__ == "__main__":
    # print(glob.glob("*/"))
    datasplit = DynamicsDataSplit(mode="Head_backbone")
    datasplit.Split_data()
    datasplit.Check_split()
