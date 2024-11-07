from envreward_utils import read_config
from glob import glob
import os 
from torchvision import transforms
from PIL import Image
from torch.utils.data import Dataset
import torch
from typing import Dict

CFG_PATH = "./envreward_cfg.json"
ENVREWARD_DATAPATH = "./EnvReward_Dataset/"
REWARD_JSON = "reward.json"
ACTION_JSON = "action.json"
END_IMAGE = "end_img.json"

class EnvRewardDataset(Dataset):

    def __init__(self,cfg_path=CFG_PATH,root_dir=ENVREWARD_DATAPATH,train=True):
        super(EnvRewardDataset, self).__init__()
        self.cfg_dict = read_config(cfg_path)
        self.dynamics_dir = root_dir
        self.train = train
        if self.train:
            self.dataset_dir = self.dynamics_dir+"train/"
        else:
            self.dataset_dir = self.dynamics_dir+"test/"
        

        self.img_size = self.cfg_dict["State_size"]
        self.img_channel = self.cfg_dict["State_channel"]
        if self.img_channel == 1:
            self.transform = transforms.Compose([
                transforms.Resize((self.img_size, self.img_size)),  # Resize image
                transforms.Grayscale(num_output_channels=1), # Turn RGB to Grayscale
                transforms.ToTensor(),          # Turn Image into tensor and normalize
            ])
        elif self.img_channel == 3:
            self.transform = transforms.Compose([
                transforms.Resize((self.img_size, self.img_size)),  # Resize image
                transforms.ToTensor(),          # Turn Image into tensor(HWC->CHW)
            ])
        else:
            raise ValueError("State_channel:{} is illegal! Legal value: 1(Grayscale) or 3(RGB)".format(self.img_channel))
        
        self.data_end_dict = read_config(self.dataset_dir+END_IMAGE)
        self.end_image_list = list(self.data_end_dict.values())
        
        self.total_image_list = glob(self.dataset_dir+"*.jpeg")
        
        self.order_image_list = list(set(self.total_image_list)-set(self.end_image_list))
        self.order_image_list.sort()

        self.reward_dict = read_config(self.dataset_dir+REWARD_JSON)
        self.action_dict = read_config(self.dataset_dir+ACTION_JSON)

        self.reward_list = list(self.reward_dict.values())
        self.action_list = list(self.action_dict.values())

    def __len__(self):
        # Dataset Size
        return len(self.order_image_list)
    
    def __getitem__(self, idx)->Dict[str,torch.Tensor]:
        # Get Currect Image+Action and Next Image+Reward
        image_path = self.order_image_list[idx]
        next_img_path = self.get_next_img(image_path)

        image = Image.open(image_path)
        next_image = Image.open(next_img_path)

        # If transform is not None
        if self.transform:
            image_tensor = self.transform(image)
            next_image_tensor = self.transform(next_image)

        # Get reward and action
        reward = self.reward_list[idx]
        action = self.action_list[idx]
        reward_tensor = torch.tensor(reward)
        action_tensor = torch.tensor(action)

        return {"state":image_tensor,"next_state":next_image_tensor,"reward":reward_tensor,"action":action_tensor}

    def get_next_img(self,image_path:str)->str:
        dir_name, file_name = os.path.split(image_path)
        idx_str = file_name[:-5]
        new_idx_ = int(idx_str)+1
        file_name = file_name.replace(idx_str,f"{new_idx_:07d}")
        next_img_path = os.path.join(dir_name, file_name)
        return next_img_path


if __name__ == "__main__":
    envrewardd = EnvRewardDataset()
    print(envrewardd[1]["action"])
    print(envrewardd[1]["reward"])
    import matplotlib.pyplot as plt
    for i in range(8):
        plt.subplot(2,4,i+1)
        image = Image.open(envrewardd.order_image_list[i])
        plt.imshow(image)
        plt.title(f"Index{i} State")
        plt.axis("off")
    plt.show()
    for idx in range(8):
        env_dict = envrewardd[idx]
        state = env_dict["state"]
        nstate = env_dict["next_state"]
        plt.subplot(4,4,2*idx+1)
        plt.imshow(state.permute(1, 2, 0).numpy())
        plt.axis("off")
        plt.title(f"Index{idx} State")
        plt.subplot(4,4,2*idx+2)
        plt.imshow(nstate.permute(1, 2, 0).numpy())
        plt.axis("off")
        plt.title(f"Index{idx} Next State")
    plt.show()

        
    