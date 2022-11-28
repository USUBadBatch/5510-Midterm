import torch
from model import PolicyNN
from os.path import exists
import os

class Agent(object):
    def __init__(self, env, load_exist):
        self.device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
        self.load_exist = load_exist
        
        PATH = f'{os.getcwd()}/policy_cnn.pt'
        self.model = PolicyNN(env.observation_space.shape[0]).to(self.device)
        if exists(PATH) and load_exist:
            self.model.load_state_dict(torch.load(PATH))
        
        self.optimizer = torch.optim.Adam(self.model.parameters(), lr=3e-3)
        
    def act(self, state):
        state = torch.from_numpy(state).unsqueeze(0).to(self.device)
        probs = self.model(state).cpu()
        cat_dist = torch.distributions.Categorical(probs)
        action = cat_dist.sample()
        
        return action.item(), cat_dist.log_prob(action)
    