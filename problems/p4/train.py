import torch
from tqdm import tqdm
from torch.utils.tensorboard import SummaryWriter

from model import DQN
from cartpole import CartPoleEnv

env = CartPoleEnv(cart_mass=0.2, pole_mass=4.0, pole_length=1.0)
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

def main():
    pass

main()
