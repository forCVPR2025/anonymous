import json
from collections import OrderedDict
import copy
from torchvision import models
import torch
import re
import os
from datetime import datetime
from glob import glob

def read_config(file_path:str)->dict:
    """Read JSON config."""
    json_object = json.load(open(file_path, 'r'))
    return json_object

def dump_json(data:dict,json_path:str)->None:
    with open(json_path, 'w') as f:
        json.dump(data, f)

def judge_state_dict(key:str,cfg_dict:dict)->bool:
    sub_str3 = key[:3]
    sub_str5 = key[:5]
    sub_str6 = key[:6]
    Backbone = cfg_dict["Backbone"]
    if sub_str3 in Backbone or sub_str5 in Backbone or sub_str6 in Backbone:
        return True
    else:
        return False
    
def Acquire_need_statedict(pretrained_dict:OrderedDict,cfg_dict:dict)->OrderedDict:
    pretrained_dict_need = copy.deepcopy(pretrained_dict)
    for key in pretrained_dict.keys():
        if judge_state_dict(key.title(),cfg_dict):
            pass
        else:
            pretrained_dict_need.pop(key.title().lower())
    pretrained_dict_need2 = copy.deepcopy(pretrained_dict_need)
    for key_need in pretrained_dict_need.keys():
        key_need2 = "backbone."+key_need
        pretrained_dict_need2[key_need2] = pretrained_dict_need[key_need]
        pretrained_dict_need2.pop(key_need)
        # print(key_need)
    return pretrained_dict_need2


def norm_col_init(weights, std=1.0):
    x = torch.randn(weights.size())
    x *= std / torch.sqrt((x**2).sum(1, keepdim=True))
    return x

def get_epoch_date(weight_name:str):
    """
        Example legal weight_name:
            weight_name = "weight_10_2024-07-31-16-20-00.pth"
    """

    # re pattern,to match epoch and time
    pattern = r"weight_(\d+)_(.+)\.pth"

    # re.match to match pattern in weight name
    match = re.match(pattern, weight_name)

    if match:
        epoch = match.group(1)
        time = match.group(2)
        return epoch,time
    else:
        raise ValueError(f"weight_name:{weight_name} is illegal! Legal form: weight_$Epoch_$Date")


def save_weight(args,model:torch.nn.Module,Epoch:int):
    weight_path = args.weight_dir
    if not os.path.exists(args.weight_dir):
        os.makedirs(args.weight_dir)
    if not os.path.exists(weight_path):
        os.makedirs(weight_path)
    
    now = datetime.now()
    formatted_time = now.strftime("%Y-%m-%d-%H-%M-%S")
    weight_path += f"/weight_{Epoch}_{formatted_time}.pth"

    torch.save(model.state_dict(),weight_path)
    print(f"Saving checkpoint to {weight_path}")

def get_newest_path(args)->str:
    weight_dir = args.weight_dir + "/"
    target_list = glob(weight_dir+"*.pth")
    date_epoch_dict = {}
    for weight_path in target_list:
        epoch,date = get_epoch_date(weight_path.split('/')[-1])
        date_epoch_dict[date] = epoch
    max_date = max(list(date_epoch_dict.keys()))
    max_epoch = date_epoch_dict[max_date]
    target_path = weight_dir+f"weight_{max_epoch}_{max_date}.pth"
    print(f"Loading weight: {target_path}")
    return target_path

if __name__ == "__main__":
    pass
