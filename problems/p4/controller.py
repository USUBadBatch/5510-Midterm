import os
import sys

# Sets the environment for the video driver based on the OS to render the environment graphic
if sys.platform == 'win32':
	os.environ['SDL_VIDEODRIVER'] = 'windib'
elif sys.platform == 'linux' or sys.platform == 'linux2':
    os.environ['SDL_VIDEODRIVER'] = 'dummy'

class CartPoleController():
    def __init__(self, env):
        self.__env = env
        self.__observation, _ = self.__env.reset()
        
    def __get_action(self):
        return 0 if self.__observation[1] < 0 else 1
    
    def next_step(self):
        self.__observation, _, terminated, truncated, _ = self.__env.step(self.__get_action())
        
        if terminated or truncated:
            self.__observation, _ = self.__env.reset()
