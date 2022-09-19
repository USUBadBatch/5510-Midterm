from skidsteer import Skidsteer
import numpy as np
import matplotlib.pyplot as plt
import math


DELTA_TIME = .1
CIRCLE_DIAMETER = 5 # in meters
SKIDSTEER_LEN = .75 # in meters
SKIDSTEER_WIDTH = .55 # still in meters

skidsteer = Skidsteer(SKIDSTEER_LEN, SKIDSTEER_WIDTH)
coords: list[tuple[float, float, float]] = []

def get_v_left(elapsed_time: float):
    return min(14, max(.5, 10*elapsed_time))

def get_dist(x:float, y: float):
    return math.sqrt(x*x + y*y)


for t in range(int(1/DELTA_TIME)):
    coords.append((skidsteer.get_xpos(), skidsteer.get_ypos(), skidsteer.get_theta()))
    if get_dist(skidsteer.get_xpos, skidsteer.get_ypos) > (CIRCLE_DIAMETER / 2) - (SKIDSTEER_WIDTH / 2):
        break
    skidsteer.move(get_v_left(t), 16, DELTA_TIME)

plt.plot([x for (x,y,t) in coords], [y for (x,y,t) in coords])
plt.xlabel("X")
plt.ylabel("Y")
plt.title("Trajectory of Robit in Cartesian Plane")
plt.show()