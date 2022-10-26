import torch
from tqdm import tqdm
from torch.utils.tensorboard import SummaryWriter

from collections import namedtuple
from itertools import count
import gym

from model import DQN
# from cartpole import CartPoleEnv
import utils

def optimize_model(memory, batch_size, transition, device, policy_net, target_net, gamma, optimizer):
    if len(memory) < memory.sample(batch_size):
        return
    
    transitions = memory.sample(batch_size)
    batch = transition(*zip(*transitions))

    mask = torch.tensor(tuple(map(lambda x: x is not None, batch.next_state)), device=device, dtype=torch.bool)
    next_states = torch.cat([x for x in batch.next_state if x is not None])

    state = torch.cat(batch.state)
    action = torch.cat(batch.action)
    reward = torch.cat(batch.reward)

    state_action_values = policy_net(state).gather(1, action)
    
    next_state_values = torch.zeros(batch_size, device=device)
    next_state_values[mask] = target_net(next_states).max(1)[0].detach()
    
    expected_state_action_values = (next_state_values * gamma) + reward
    
    criterion = torch.nn.Smooth1Loss()
    loss = criterion(state_action_values, expected_state_action_values.unsqueeze(1))

    optimizer.zero_grad()
    loss.backward()
    for param in policy_net.parameters():
        param.grad.data.clamp_(-1, 1)    
    optimizer.step()

def main():
    # env = CartPoleEnv(cart_mass=4.0, pole_mass=0.2, pole_length=1.0)
    if gym.__version__ < '0.26':
        env = gym.make('CartPole-v0', new_step_api=True, render_mode='single_rgb_array').unwrapped
    else:
        env = gym.make('CartPole-v0', render_mode='rgb_array').unwrapped

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    
    BATCH_SIZE = 128
    GAMMA = 0.999
    TARGET_UPDATE = 10
    
    Transition = namedtuple('Transition', ('state', 'action', 'next_state', 'reward'))
    
    init_screen = utils.get_screen(env)
    _, _, screen_height, screen_width = init_screen.shape
    
    num_actions = env.action_space.n
    
    policy_net = DQN(screen_height, screen_width, num_actions).to(device)
    target_net = DQN(screen_height, screen_width, num_actions).to(device)
    target_net.load_state_dict(policy_net.state_dict())
    target_net.eval()
    
    optimizer = torch.optim.RMSprop(policy_net.parameters())
    memory = utils.ReplayMemory(10000)
    
    args = {
        "memory" : memory, 
        "batch_size" : BATCH_SIZE, 
        "transition" : Transition, 
        "device" : device, 
        "policy_net" : policy_net, 
        "target_net" : target_net, 
        "gamma" : GAMMA, 
        "optimizer" : optimizer
        }
    
    steps_done = 0
    
    epochs = 50
    for i in tqdm(range(epochs)):
        env.reset()
        last_screen = utils.get_screen(env)
        current_screen = utils.get_screen(env)
        state = current_screen - last_screen
        
        for _ in count():
            action = utils.select_action(state, steps_done, policy_net, num_actions)
            _, reward, done, _, _ = env.step(action.item())
            reward = torch.tensor([reward], device=device)

            last_screen = current_screen
            current_screen = utils.get_screen(env)
            
            if not done:
                next_state = current_screen - last_screen
            else:
                next_state = None
                
            memory.push(state, action, next_state, reward)
            
            state = next_state 
            
            optimize_model(**args)
            if done:
                break
            
        if i % TARGET_UPDATE == 0:
            target_net.load_state_dict(policy_net.state_dict())

main()
