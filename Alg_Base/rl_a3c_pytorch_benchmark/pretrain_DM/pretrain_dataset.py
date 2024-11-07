import glob
import os
import json
from PIL import Image
import numpy as np
from pretrain_utils import read_config
import random
import copy
from torchvision import transforms
import torch
from torch.utils.data import DataLoader
import math

ORIGIN_DATAPATH="./OriginDataset/"
DYNAMICS_DATAPATH = "./DynamicsDataset/"
CFG_PATH="./pretrain_cfg.json"

class DynamicsDataset(object):
    r"""`DynamicsDataset`_ Datasets.
    
    Args:
        mode (string): training mode
        cfg_path (string): path of pretrain_cfg.json
        root_dir (string): path of DynamicsDataset
        train: whether the dataset is trained or not

    """

    def __init__(self,mode,cfg_path=CFG_PATH,root_dir=DYNAMICS_DATAPATH,train=True,shuffle=True):
        super(DynamicsDataset, self).__init__()
        self.cfg = read_config(cfg_path)
        self.cfg_dict = self.cfg[mode]
        self.bs = self.cfg_dict["Episode_size"]
        self.statebuf = self.cfg_dict["State_Buffer"]
        self.dynamics_dir = root_dir+"Batch{Episode_size}State{State_Buffer}/".format(Episode_size=self.bs,State_Buffer=self.statebuf)
        self.train = train
        if self.train:
            self.dataset_dir = self.dynamics_dir+"train/"
        else:
            self.dataset_dir = self.dynamics_dir+"test/"
        
        self.dataset_prefix = "episode"
        self.dataset_path_list = sorted(glob.glob(
            os.path.join(self.dataset_dir, '*/')))

        if shuffle:
            random.shuffle(self.dataset_path_list)

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


    ### get image and label for a sequence(data of one batch)
    def __getitem__(self, index):
        r"""        
        Args:
            index (integer or string): Index of a sequence.
        
        Returns:
            tuple: (img_files, anno), where ``img_files`` is a list of
                file names and ``anno`` is a N x 4 (rectangles) numpy array.
        """
        
        if index < 0 or index >= len(self.dataset_path_list):
            raise Exception('Index:{} is illegal.'.format(index))
        
        # print(f"Curr_idx:{index} Curr_episode:{self.dataset_path_list[index]}")

        img_files = sorted(glob.glob(
            os.path.join(self.dataset_path_list[index], '*.jpeg')))

        if self.statebuf > 1:
            total_img_list = self.imglist2statebuf(img_files)
        else:
            total_img_list = img_files
        anno_path = self.dataset_path_list[index]+"Direction_label.json"
        with open(anno_path, 'r') as f:
            label_res = json.load(f)
        label_list = list(label_res.values())
        if len(label_list) == 1:
            label_list = sum(label_list, [])

        ## Get Image tensor and label tensor
        label_tensor = torch.tensor(label_list,dtype=torch.float32)
        img_PIL_dict = self.imgpath2PIL(img_files)
        full_state_tensor = self.imglist2tensor(total_img_list,img_PIL_dict)

        return full_state_tensor, label_tensor
    ### Return number of sequence in dataset
    def __len__(self):
        return len(self.dataset_path_list)
    
    ### turn img list to state buffer style
    def imglist2statebuf(self,img_list:list)->list:
        total_img_list = []
        single_img_list = [img_list[0]]*self.statebuf
        for img_path in img_list:
            single_img_list.append(img_path)
            del single_img_list[0]
            total_img_list.append(copy.deepcopy(single_img_list))
        return total_img_list
    
    def imgpath2PIL(self,path_list_single:list)->dict:
        img_PIL_dict = {}
        for img_path in path_list_single:
            img_PIL_dict[img_path] = copy.deepcopy(Image.open(img_path))
        return img_PIL_dict

    ### Path list to tensor
    def imglist2tensor(self,path_list:list,img_PIL_dict:dict)->torch.Tensor:
        full_state_list = []
        for statebuf in path_list:
            statetensor_list = []
            for img_path in statebuf:
                image = img_PIL_dict[img_path]
                image_tensor = self.transform(image)
                statetensor_list.append(copy.deepcopy(image_tensor))
            statetensor = torch.stack(statetensor_list,dim=0) # shape:(10*3,84,84)
            new_shape_tuple = (statetensor.shape[0]*statetensor.shape[1], statetensor.shape[2], statetensor.shape[3])
            statetensor = torch.reshape(statetensor, new_shape_tuple)
            full_state_list.append(copy.deepcopy(statetensor))
        full_state_tensor = torch.stack(full_state_list,dim=0)
        return full_state_tensor

class DynamicsDatasetSample(object):
    r"""`DynamicsDataset`_ Datasets.
    
    Args:
        mode (string): training mode
        cfg_path (string): path of pretrain_cfg.json
        root_dir (string): path of DynamicsDataset
        train: whether the dataset is trained or not

    """

    def __init__(self,mode,cfg_path=CFG_PATH,root_dir=DYNAMICS_DATAPATH,train=True):
        super(DynamicsDatasetSample, self).__init__()
        self.cfg = read_config(cfg_path)
        self.cfg_dict = self.cfg[mode]
        self.bs = self.cfg_dict["Episode_size"]
        self.statebuf = self.cfg_dict["State_Buffer"]
        self.dynamics_dir = root_dir+"Batch{Episode_size}State{State_Buffer}/".format(Episode_size=self.bs,State_Buffer=self.statebuf)
        self.train = train
        if self.train:
            self.dataset_dir = self.dynamics_dir+"train/"
        else:
            self.dataset_dir = self.dynamics_dir+"test/"
        
        self.dataset_prefix = "episode"
        self.dataset_path_list = sorted(glob.glob(
            os.path.join(self.dataset_dir, '*/')))

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


    ### get image and label for a sequence(data of one sample)
    def __getitem__(self, index):
        r"""        
        Args:
            index (integer or string): Index of a sequence.
        
        Returns:
            tuple: (img_files, anno), where ``img_files`` is a list of
                file names and ``anno`` is a N x 4 (rectangles) numpy array.
        """
        
        if index < 0 or index >= len(self.dataset_path_list)*self.bs:
            raise Exception('Index:{} is illegal.'.format(index))
        
        batch_index = math.floor(index/self.bs)
        episode_idx = index%self.bs
        
        # print(f"Curr_idx:{index} Curr_episode:{self.dataset_path_list[index]}")

        img_files_path = sorted(glob.glob(
            os.path.join(self.dataset_path_list[batch_index], '*.jpeg')))


        single_img_list = self.imglist2statebuf(img_files_path,episode_idx)
        # print(f"batch_index: {batch_index} episode_idx: {episode_idx} len(img_files_path)= {len(img_files_path)} len(single_img_list)= {len(single_img_list)}")
        anno_path = self.dataset_path_list[batch_index]+"Direction_label.json"

        with open(anno_path, 'r') as f:
            label_res = json.load(f)
        label_list = list(label_res.values())
        if len(label_list) == 1:
            label_list = sum(label_list, [])

        label = label_list[episode_idx]

        ## Get Image tensor and label tensor
        label_tensor = torch.tensor(label,dtype=torch.float32)
        sample_state_tensor = self.imgpath2Tensor(single_img_list)

        return sample_state_tensor, label_tensor
    ### Return number of sequence in dataset
    def __len__(self):
        return len(self.dataset_path_list)*self.bs
    
    ### turn img list to state buffer style
    def imglist2statebuf(self,img_list:list,episode_idx:int)->list:
        single_img_list = []
        if episode_idx < self.statebuf-1:
            single_img_list = [img_list[0]]*self.statebuf
            for img_path in img_list[:episode_idx+1]:
                single_img_list.append(img_path)
                del single_img_list[0]
        else:
            for img_path in img_list[episode_idx+1-self.statebuf:episode_idx+1]:
                single_img_list.append(img_path)
        return single_img_list
    
    def imgpath2Tensor(self,path_list_single:list)->dict:
        img_tensor_list = []
        for img_path in path_list_single:
            img_tensor = self.transform(copy.deepcopy(Image.open(img_path)))
            img_tensor_list.append(img_tensor)
        img_tensor_sample = torch.stack(img_tensor_list,dim=0)
        # import matplotlib.pyplot as plt
        # for i in range(img_tensor_sample.shape[0]):
        #     img_np = img_tensor_sample[i].permute(1, 2, 0).numpy()
        #     plt.imshow(img_np)
        #     plt.axis('off')  # 隐藏坐标轴
        #     plt.show()
        new_shape_tuple = (img_tensor_sample.shape[0]*img_tensor_sample.shape[1], img_tensor_sample.shape[2], img_tensor_sample.shape[3])
        img_tensor_sample = torch.reshape(img_tensor_sample, new_shape_tuple)
        
        return img_tensor_sample

    
class DynamicsDataLoader(object):
    def __init__(self,mode:str,dataset:DynamicsDataset,cfg_path=CFG_PATH,root_path=DYNAMICS_DATAPATH) -> None:
        self.cfg = read_config(cfg_path)
        self.cfg_dict = self.cfg[mode]
        self.State_Buffer = self.cfg_dict["State_Buffer"]
        self.Episode_size = self.cfg_dict["Episode_size"]
        self.root_path = root_path
        self.dataset = dataset
        if self.dataset.train:
            self.set_dir = self.root_path+f"Batch{self.Episode_size}State{self.State_Buffer}/train"
        else:
            self.set_dir = self.root_path+f"Batch{self.Episode_size}State{self.State_Buffer}/test"
        self.batch_volume = self.GetBatch_volume(set_dir=self.set_dir)
    """
        Return how many batch in trainset
    """
    def GetBatch_volume(self,set_dir)->int:
        batch_list = os.listdir(set_dir)
        return len(batch_list)
    
    ## You can also get num_batch with len() function
    def __len__(self):
        return self.batch_volume

    def __iter__(self):
        self.curr_idx = 0
        return self
    
    def __next__(self):
        if self.curr_idx >= self.batch_volume:
            raise StopIteration
        else:
            full_state_tensor, label_tensor = self.dataset[self.curr_idx]
            self.curr_idx += 1
            return full_state_tensor, label_tensor
    
if __name__ == "__main__":
    # ddateset = DynamicsDataset(mode="Head_backbone",train=False)
    # ddloader = DynamicsDataLoader(mode="Head_backbone",dataset=ddateset)
    ddateset = DynamicsDatasetSample(mode="Head_backbone",train=True)
    ddloader = DataLoader(ddateset,batch_size=256,shuffle=True,num_workers=16)
    # data,label = ddateset[256]
    # print(data.shape)
    # print(label.shape)
    
    
    import time
    start_t = time.time()
    for img_batch,label_batch in ddloader:
        print(f"image batch shape {img_batch.shape}")
        print(f"label batch shape {label_batch.shape}")
    print(f"Total Time Consumption is {time.time()-start_t}")
    sample_tensor = ddateset[1][1]

