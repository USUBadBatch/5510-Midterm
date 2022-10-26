import torch
from model import PolicyNN

class Agent(object):
    def __init__(self, env):
        self.device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
        self.model = PolicyNN(env.observation_space.shape[0], env.action_space.n).to(self.device)
        self.optimizer = torch.optim.Adam(self.model.parameters(), lr=3e-3)
        
    def act(self, state):
        state = torch.from_numpy(state).unsqueeze(0).to(self.device)
        probs = self.model(state).cpu()
        cat_dist = torch.distributions.Categorical(probs)
        action = cat_dist.sample()
        
        return action.item(), cat_dist.log_prob(action)