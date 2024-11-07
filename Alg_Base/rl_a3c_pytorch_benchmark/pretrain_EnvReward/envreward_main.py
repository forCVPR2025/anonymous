import torch
from torch.utils.tensorboard import SummaryWriter
import os
import sys
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_dir)
from envreward_model import EnvRewardModel
from envreward_utils import read_config,get_newest_path,save_weight
import argparse
import torch.nn as nn
from tqdm import tqdm
from torch.utils.data import DataLoader
from envreward_dataset import EnvRewardDataset
import warnings

parser = argparse.ArgumentParser(description="EnvRewardModel")
"""
    Argument that we need to config：
        --Epoch
        --gpu-ids
        --env-config
        --seed
        --tensorboard-logger
        --tensorboard-logdir
        --log-interval
"""

parser.add_argument(
    "-E",
    "--Epoch",
    type=int,
    default=100,
    help="Number epochs",
)

parser.add_argument(
    "-bs",
    "--batch-size",
    type=int,
    default=1024,
    help="Batch size of dataloader"
)

parser.add_argument(
    "-evc", "--env-config",
    default="./envreward_cfg.json",
    help="pretrain Dynamics Model info (default: pretrain_cfg.json)")

parser.add_argument(
    "-s", "--seed", type=int, default=1, help="random seed (default: 1)"
)

parser.add_argument(
    "-tl",
    "--tensorboard-logger",
    type=bool,
    default=True,
    help="Creates tensorboard logger to view model weights and biases, and monitor test agent reward progress",
)

parser.add_argument(
    "-tldir",
    "--tensorboard-logdir",
    type=str,
    default="./runs/experiment",
    help="dir of tensorboard logger",
)

parser.add_argument(
    "-login",
    "--log-interval",
    type=int,
    default=2,
    help="How many iteration do we log loss",
)

parser.add_argument(
    "-l",
    "--load",
    type=bool,
    default=False,
    help="Whether load pretrain weight or not",
)


parser.add_argument(
    "-wd",
    "--weight-dir",
    type=str,
    default="./trained_models/",
    help="directory of train weight",
)

parser.add_argument(
    "-si",
    "--save-interval",
    type=int,
    default=10,
    help="How many epoch do we save a model",
)


def train(args:argparse.Namespace,cfg:dict):
    ### device
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"Using device: {device}")
    ### tensorboard logger
    if args.tensorboard_logger:
        writer = SummaryWriter(args.tensorboard_logdir)

    ### start train config
    model = EnvRewardModel(input_shape=(cfg["State_channel"],cfg["State_size"],cfg["State_size"]),actions_dim=cfg["Action_dim"])
    if args.load: # If need to load pretrain params,load the newest params in default
        if not os.path.exists(args.weight_dir):
            raise FileNotFoundError(f"Directory:{args.weight_dir} does not exist")
        load_path = get_newest_path(args)
        model.load_state_dict(torch.load(load_path))
    model.to(device)
    model.train()

    optimizer = torch.optim.Adam(model.parameters(), lr=1e-3)
    train_dataset = EnvRewardDataset(train=True)
    train_dl = DataLoader(train_dataset,batch_size=args.batch_size,shuffle=True,num_workers=16)
    for epoch in tqdm(range(args.Epoch),desc="Train Epochs"):
        running_loss = 0.0
        running_env_loss = 0.0
        running_reward_loss = 0.0

        for i,train_data in tqdm(enumerate(train_dl),desc=f"Train Iteration {len(train_dl)}",leave=False):
            state = train_data["state"].to(device)
            true_next_state = train_data["next_state"].to(device)
            true_reward = train_data["reward"].to(device)
            action = train_data["action"].to(device)

            optimizer.zero_grad()
            next_state_pred, reward_pred = model(state,action)
            total_loss,env_loss,reward_loss = compute_loss(next_state_pred, true_next_state, reward_pred, true_reward)
            total_loss.backward()
            optimizer.step()

            running_loss += total_loss.item()
            running_env_loss += env_loss.item()
            running_reward_loss += reward_loss.item()

            if (i+1) % args.log_interval == 0 and args.tensorboard_logger:
                writer.add_scalar('training total loss', running_loss / args.log_interval, epoch * len(train_dl) + i)
                writer.add_scalar('training env loss', running_env_loss / args.log_interval, epoch * len(train_dl) + i)
                writer.add_scalar('training reward loss', running_reward_loss / args.log_interval, epoch * len(train_dl) + i)
                running_loss = 0.0
                running_env_loss = 0.0
                running_reward_loss = 0.0
            
        if (epoch+1) % args.save_interval == 0:
            save_weight(args,model,epoch+1)
    print("Finish Training")
    save_weight(args,model,args.Epoch)

def test(args:argparse.Namespace,cfg:dict):
    ### get device
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model = EnvRewardModel(input_shape=(cfg["State_channel"],cfg["State_size"],cfg["State_size"]),actions_dim=cfg["Action_dim"])
    model.to(device)
    model.eval()

    ### Load model weight
    if not os.path.exists(args.weight_dir):
        raise FileNotFoundError(f"Directory:{args.weight_dir} does not exist. Cannot Init Model weight!")
    load_path = get_newest_path(args)
    model.load_state_dict(torch.load(load_path))

    ### test set and loader
    test_dataset = EnvRewardDataset(train=False)
    test_dl = DataLoader(test_dataset,batch_size=args.batch_size,shuffle=False,num_workers=8)
    
    ### start test
    total_loss = 0.0 # loss sum
    total_env_loss = 0.0
    total_reward_loss = 0.0
    with torch.no_grad():
        for _,test_data in tqdm(enumerate(test_dl),desc=f"Test Iteration {len(test_dl)}"):
            state = test_data["state"].to(device)
            true_next_state = test_data["next_state"].to(device)
            true_reward = test_data["reward"].to(device)
            action = test_data["action"].to(device)
            
            # Feed forward
            next_state_pred, reward_pred = model(state,action)
            t_loss,env_loss,reward_loss = compute_loss(next_state_pred, true_next_state, reward_pred, true_reward)
            
            # Total loss
            total_loss += t_loss.item()
            total_env_loss += env_loss.item()
            total_reward_loss += reward_loss.item()

    # calculate average loss and accuracy
    average_total_loss = total_loss / len(test_dl) ## Average loss of batch
    average_env_loss = total_env_loss / len(test_dl)
    average_reward_loss = total_reward_loss / len(test_dl)

    print(f"Average Total Loss: {average_total_loss:.4f}")
    print(f"Average Env Loss: {average_env_loss:.4f}")
    print(f"Average Reward Loss: {average_reward_loss:.4f}")

def compute_loss(pred_next_state:torch.Tensor, true_next_state:torch.Tensor, pred_reward:torch.Tensor, true_reward:torch.Tensor):
    env_fn = nn.MSELoss()
    reward_fc = nn.MSELoss()
    
    # loss for env head
    env_loss = env_fn(pred_next_state, true_next_state)
    
    # loss for reward head
    pred_reward2d = pred_reward
    true_reward2d = true_reward.unsqueeze(1)
    if true_reward2d.dtype == torch.int64:
        warnings.warn("Dtype of true_reward is torch.int64 which tends to be torch.float32! ",UserWarning)
        true_reward2d = true_reward2d.to(dtype=torch.float32)
    reward_loss = reward_fc(pred_reward2d, true_reward2d)
    
    # Combine loss
    total_loss = env_loss + reward_loss
    return total_loss,env_loss,reward_loss

if __name__ == "__main__":
    args = parser.parse_args()
    cfg = read_config(args.env_config)
    train(args,cfg)
    test(args,cfg)