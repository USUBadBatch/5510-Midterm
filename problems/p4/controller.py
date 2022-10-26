import os
import sys

import math
import gym

# Sets the environment for the video driver based on the OS to render the environment graphic
if sys.platform == 'win32':
	os.environ['SDL_VIDEODRIVER'] = 'windib'
elif sys.platform == 'linux' or sys.platform == 'linux2':
    os.environ['SDL_VIDEODRIVER'] = 'dummy'

# env = CartPoleEnv(cart_mass=4.0, pole_mass=0.2, pole_length=1.0)
env = gym.make('CartPole-v1', render_mode='human')
env.cart_mass = 4.0
env.pole_mass = 0.2
env.length = 1.0 / 2
env.force_mag = 6.0
env.theta_threshold_radians = 24 * 2 * math.pi / 360

class CartPoleController():
    def __init__(self, env):
        self.__env = env
        self.__observation, _ = self.__env.reset()
        
    def __get_action(self):
        return 0 if self.__observation[1] > 0 else 1
    
    def next_step(self):
        self.__observation, _, terminated, truncated, _ = self.__env.step(self.__get_action())
        
        if terminated or truncated:
            self.__observation, _ = self.__env.reset()
            
            
controller = CartPoleController(env)

for _ in range(1000):
    env.render()
    controller.next_step()
    
env.close()
