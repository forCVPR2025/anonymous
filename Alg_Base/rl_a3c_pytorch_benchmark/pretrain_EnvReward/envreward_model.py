import torch
import torch.nn as nn
from torch.utils.tensorboard import SummaryWriter

class EnvRewardModel(nn.Module):
    def __init__(self, input_shape, actions_dim):
        super(EnvRewardModel, self).__init__()

        # 共享的卷积层
        self.encoder = nn.Sequential(
            nn.Conv2d(input_shape[0], 32, 5, stride=2, padding=2),
            nn.ReLU(),
            nn.Conv2d(32, 32, 5, stride=2, padding=1),
            nn.ReLU(),
            nn.Conv2d(32, 64, 4, stride=2, padding=1),
            nn.ReLU(),
            nn.Conv2d(64, 64, 3, stride=2, padding=1),
            nn.ReLU()
        )

        # 计算卷积层输出的大小
        def conv2d_output_size(size, kernel_size=3, stride=2,padding=1):
            return (size - kernel_size+2*padding) // stride + 1
        
        l1_out = conv2d_output_size(input_shape[1],5,2,2)
        l2_out = conv2d_output_size(l1_out,5,2,1)
        l3_out = conv2d_output_size(l2_out,4,2,1)
        self.l4_out = conv2d_output_size(l3_out,3,2,1)

        
        decoder_input_size = self.l4_out * self.l4_out * 64 + actions_dim

        # Reshpe 
        self.env_fc = nn.Sequential(
            nn.Linear(decoder_input_size, self.l4_out * self.l4_out * 64),
            nn.ReLU(),
        )

        self.decoder = nn.Sequential(
            nn.ConvTranspose2d(64, 64, 4, stride=2, padding=1),
            nn.ReLU(),
            nn.ConvTranspose2d(64, 32, 4, stride=2, padding=1),
            nn.ReLU(),
            nn.ConvTranspose2d(32, 32, 4, stride=2, padding=0),
            nn.ReLU(),
            nn.ConvTranspose2d(32, input_shape[0], 4, stride=2, padding=1),
            nn.ReLU(),
        )

        def trans_conv2d_output_size(size, kernel_size=3, stride=2,padding=1):
            return (size-1)*stride-2*padding+kernel_size

        t1_out = trans_conv2d_output_size(self.l4_out,4,2,1)
        t2_out = trans_conv2d_output_size(t1_out,4,2,1)
        t3_out = trans_conv2d_output_size(t2_out,4,2,0)
        self.t4_out = trans_conv2d_output_size(t3_out,4,2,1)
        
        assert self.t4_out == input_shape[1]

        # Reward model
        self.reward_fc = nn.Sequential(
            nn.Linear(decoder_input_size, 128),
            nn.ReLU(),
            nn.Linear(128, 1)  # 输出奖励
        )

    def forward(self, state, action):
        x = self.encoder(state)
        x = x.view(x.size(0), -1)
        x = torch.cat((x, action), dim=1)

        decode_in = self.env_fc(x)
        decode_in = decode_in.view(-1, 64, self.l4_out, self.l4_out)
        next_state_pred = self.decoder(decode_in)
        reward_pred = self.reward_fc(x)

        return next_state_pred, reward_pred

def visualize_model():
    sample_state = torch.randn(1, 3, 84, 84)
    sample_action = torch.randn(1, 7)
    model = EnvRewardModel(input_shape=(3,84,84),actions_dim=7)
    writer = SummaryWriter('./runs/experiment')
    writer.add_graph(model, (sample_state,sample_action))
    writer.close()


if __name__ == "__main__":
    visualize_model()
    