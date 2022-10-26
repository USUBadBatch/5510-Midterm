from torch import nn

class PolicyNN(nn.Module):
    def __init__(self, observation_space, action_space):
        super(PolicyNN, self).__init__()
        self.layer1 = nn.Linear(observation_space, 16)
        self.layer2 = nn.Linear(16, 2)

    def forward(self, x):
        x = self.layer1(x)                      # 4 -> 16
        x = self.layer2(x)                      # 16 -> 2
        x = nn.functional.softmax(x, dim=1)     # get probabilities of output
        
        return x