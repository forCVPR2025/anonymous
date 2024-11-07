import torch
from torchvision import models
import numpy as np
from pretrain_utils import Acquire_need_statedict,norm_col_init
import torch.nn.functional as F

WEIGHT_PATH_DICT = {
    "resnet18":"resnet18-5c106cde.pth",
    "resnet34":"resnet34-333f7ec4.pth",
}

PRETRAIN_DIR = "./pretrain_weight/"

class ResNet18Dynamics(torch.nn.Module):
    def __init__(self,cfg_dict:dict)->None:
        super(ResNet18Dynamics,self).__init__()
        raise NotImplementedError("Please Implement it yourself if needed!")
    def forward(self,input):
        raise NotImplementedError("Please Implement forward function yourself if needed!")
class ResNet33Dynamics(torch.nn.Module):
    def __init__(self,cfg_dict:dict)->None:
        super(ResNet33Dynamics,self).__init__()
        raise NotImplementedError("Please Implement it yourself if needed!")
    def forward(self,input):
        raise NotImplementedError("Please Implement forward function yourself if needed!")
    
class E2ECNNLSTM(torch.nn.Module):
    def __init__(self,cfg_dict:dict)->None:
        super(E2ECNNLSTM,self).__init__()
        self.conv1 = torch.nn.Conv2d(cfg_dict["State_channel"]*cfg_dict["State_Buffer"], 16, 8, stride=4)
        self.conv2 = torch.nn.Conv2d(16, 32, 4, stride=2)
        
        # Get ConvNet Output size
        self.input_shape = cfg_dict["State_size"]
        conv1_outdim = int((self.input_shape-8)/4)+1
        conv2_outdim = int((conv1_outdim-4)/2)+1
        self.conv_outdim = conv2_outdim

        self.fc_hidden = self.fc_hidden = cfg_dict["Hidden_dim"][0]
        self.output_dim = cfg_dict["Action_dim"]
        self.fcn1 = torch.nn.Linear(32*self.conv_outdim*self.conv_outdim,self.fc_hidden)
        self.fcn2 = torch.nn.Linear(self.fc_hidden,self.output_dim)

        ## Initialize model weight
        relu_gain = torch.nn.init.calculate_gain("relu")
        self.conv1.weight.data.mul_(relu_gain)
        self.conv1.bias.data.fill_(0)
        self.conv2.weight.data.mul_(relu_gain)
        self.conv2.bias.data.fill_(0)
        ## Initial weights of fully connected layer
        self.fcn1.bias.data.fill_(0)
        self.fcn1.weight.data = norm_col_init(self.fcn1.weight.data,1.0)
        self.fcn2.bias.data.fill_(0)
        self.fcn2.weight.data = norm_col_init(self.fcn2.weight.data,1.0)
        ## set model to train mode
        self.train()

    def forward(self,input):
        x = F.relu(self.conv1(input))
        x = F.relu(self.conv2(x))
        x = x.view(x.size(0), -1)
        x = F.relu(self.fcn1(x))
        x = self.fcn2(x)        
        return F.softmax(x, dim=1)

class CNNLSTM(torch.nn.Module):
    def __init__(self,cfg_dict:dict)->None:
        super(CNNLSTM,self).__init__()
        self.conv1 = torch.nn.Conv2d(cfg_dict["State_channel"]*cfg_dict["State_Buffer"], 32, 5, stride=1, padding=2)
        self.conv2 = torch.nn.Conv2d(32, 32, 5, stride=1, padding=1)
        self.conv3 = torch.nn.Conv2d(32, 64, 4, stride=1, padding=1)
        self.conv4 = torch.nn.Conv2d(64, 64, 3, stride=1, padding=1)
        # Get ConvNet Output size
        self.input_shape = cfg_dict["State_size"]
        conv1_outdim = int(self.input_shape/2)
        conv2_outdim = int((conv1_outdim-2)/2)
        conv3_outdim = int((conv2_outdim-1)/2)
        conv4_outdim = int(conv3_outdim/2)
        self.conv_outdim = conv4_outdim

        # Fully connected layer
        self.fc_hidden = cfg_dict["Hidden_dim"][0]
        self.output_dim = cfg_dict["Action_dim"]
        self.fcn1 = torch.nn.Linear(64*self.conv_outdim*self.conv_outdim,self.fc_hidden)
        self.fcn2 = torch.nn.Linear(self.fc_hidden,self.output_dim)
        
        ## Initialize model weight
        relu_gain = torch.nn.init.calculate_gain("relu")
        self.conv1.weight.data.mul_(relu_gain)
        self.conv1.bias.data.fill_(0)
        self.conv2.weight.data.mul_(relu_gain)
        self.conv2.bias.data.fill_(0)
        self.conv3.weight.data.mul_(relu_gain)
        self.conv3.bias.data.fill_(0)
        self.conv4.weight.data.mul_(relu_gain)
        self.conv4.bias.data.fill_(0)
        ## Initialize model bias weight
        self.fcn1.bias.data.fill_(0)
        self.fcn1.weight.data = norm_col_init(self.fcn1.weight.data,1.0)
        self.fcn2.bias.data.fill_(0)
        self.fcn2.weight.data = norm_col_init(self.fcn2.weight.data,1.0)

        self.train()
    def forward(self,input):
        x = F.relu(F.max_pool2d(self.conv1(input), 2, 2))
        x = F.relu(F.max_pool2d(self.conv2(x), 2, 2))
        x = F.relu(F.max_pool2d(self.conv3(x), 2, 2))
        x = F.relu(F.max_pool2d(self.conv4(x), 2, 2))
        x = x.view(x.size(0), -1)
        x = F.relu(self.fcn1(x))
        x = self.fcn2(x)        
        return F.softmax(x, dim=1)



if __name__ == "__main__":
    from torchsummary import summary
    from pretrain_utils import read_config
    cfg = read_config("./pretrain_cfg.json")
    cfg_dict = cfg["Head_backbone"]
    if cfg_dict["Model_Type"] == "Self_train":
        model = CNNLSTM(cfg_dict)
    elif cfg_dict["Model_Type"] == "E2E":
        model = E2ECNNLSTM(cfg_dict)
    summary(model.cuda(),input_size=(30,84,84))



