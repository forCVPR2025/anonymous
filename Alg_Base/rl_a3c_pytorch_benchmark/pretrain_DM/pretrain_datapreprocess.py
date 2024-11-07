from pretrain_utils import read_config,dump_json
import json
import os
import glob

PRETRAIN_ROOT="./"
ORIGIN_DATAPATH="./OriginDataset/"
EPISODE_PREFIX = "episode"

DATA_VOLUME = ORIGIN_DATAPATH+"data_volume.json"
CFG_PATH="./pretrain_cfg.json"


class DataPreprocessing():
    def __init__(self,mode,cfg_path=CFG_PATH,ori_datapath=ORIGIN_DATAPATH,episode_prefix=EPISODE_PREFIX) -> None:
        self.cfg = read_config(cfg_path)
        self.cfg_dict = self.cfg[mode]
        self.evo_step = self.cfg_dict["Evolution_step"]
        self.ori_datapath = ori_datapath
        self.episode_prefix = episode_prefix

    def read_json(self,json_path:str):
        with open(json_path, 'r') as json_file:
            data_dict = json.load(json_file)
        img_list = list(data_dict.keys())
        del img_list[-self.evo_step:]
        label_list = list(data_dict.values())
        return img_list,label_list
    
    def Acquire_full_label(self,img_list:list,label_list:list):
        full_label_list = []
        for idx in range(len(img_list)):
            idx_label = []
            for i in range(idx,idx+self.evo_step):
                idx_label.append(label_list[i])
            full_label_list.append(idx_label)
        return full_label_list
    
    def data_preprocess(self):
        episode_list = glob.glob(self.ori_datapath+"*/")
        for episode in episode_list:
            if self.episode_prefix in episode:
                json_path_src = episode+"Direction_label_src.json"
                json_path_dst = episode+"Direction_label.json"
                img_list,label_list = self.read_json(json_path_src)
                full_label_list = self.Acquire_full_label(img_list,label_list)
                Direction_label_dict = dict(zip(img_list,full_label_list))
                if os.path.exists(json_path_dst):
                    os.unlink(json_path_dst)
                dump_json(Direction_label_dict,json_path_dst)
            else:
                continue

    
            
if __name__ == "__main__":
    data_p = DataPreprocessing(mode = "Head_backbone")
    data_p.data_preprocess()
    # label_df = pd.read_csv("C:\\Users\\20669\\Desktop\\test.csv",sep=',',header='infer')
    # n_list = list(label_df["name"])
    # l_list = list(label_df["label"])
    # print(dict(zip(n_list,l_list)))
