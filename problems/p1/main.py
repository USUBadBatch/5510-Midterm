from skidsteer import Skidsteer
import numpy as np
import matplotlib.pyplot as plt
import math


DELTA_TIME = .1
CIRCLE_DIAMETER = 5 # in meters
SKIDSTEER_LEN = .75 # in meters
SKIDSTEER_WIDTH = .55 # still in meters

# this is the maximum distance that the center of the robot 
# can get from the center of the circle. Anything more than this
# and the robot is outside the circle.
max_dist = (CIRCLE_DIAMETER / 2) - (SKIDSTEER_WIDTH / 2)

skidsteer = Skidsteer(SKIDSTEER_LEN, SKIDSTEER_WIDTH)
coords: list[tuple[float, float, float]] = []

def get_v_left(elapsed_time: float):
    return min(12, 2*elapsed_time)

def get_dist(x:float, y: float):
    return math.sqrt(x*x + y*y)

'''
Variables needed:
total_time = time duration 
time_coeff = time coefficient
max_v_left = maximum speed of left
V_RIGHT = constant velocity of right tread
'''
# TODO look at Archimedean spiral 

for t in range(0, 100):
    x_pos = skidsteer.get_xpos()
    y_pos = skidsteer.get_ypos()
    if get_dist(x_pos, y_pos) > max_dist:
        print("Too far!")
        break
    coords.append((x_pos, y_pos, skidsteer.get_theta()))
    skidsteer.move(get_v_left(t/10)*.1, 16*.1, DELTA_TIME)
    

plt.plot([x for (x,y,t) in coords], [y for (x,y,t) in coords])
plt.xlabel("X")
plt.ylabel("Y")
plt.title("Trajectory of Robit in Cartesian Plane")
plt.show()