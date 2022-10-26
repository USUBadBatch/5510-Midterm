import gym
import numpy as np

from torch.utils.tensorboard import SummaryWriter
import torch

from agent import Agent

writer = SummaryWriter()

epochs = 50
log_iter = 10

env = gym.make("CartPole-v1", render_mode="human")

agent = Agent(env)
learning = []

for i in range(epochs):
    steps = 0
    done = False
    state, _ = env.reset()
    
    cumulative_rewards = 0
    action_probs = []

    while not done:
        steps += 1
        
        action, action_prob = agent.act(state)
        action_probs.append(action_prob)

        state, reward, done, *_ = env.step(action)
        cumulative_rewards += reward
        
    policy_loss = torch.cat([-log_prob * cumulative_rewards for log_prob in action_probs]).sum()
    
    agent.optimizer.zero_grad()
    policy_loss.backward()
    agent.optimizer.step()
    
    learning.append(steps)
    if i % log_iter == 0:
        print(f"Iteration: {i} | Moving-Average Steps: {np.mean(learning[-log_iter:]):.4f}")
        