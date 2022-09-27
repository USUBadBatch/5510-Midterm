from os import access
from skidsteer import Skidsteer
import numpy as np
import matplotlib.pyplot as plt
import math


DELTA_TIME = .1
CIRCLE_DIAMETER = 5 # in meters
SKIDSTEER_LEN = .75 # in meters
SKIDSTEER_WIDTH = .55 # still in meters
CIRCLE_RADIUS = CIRCLE_DIAMETER / 2



def main():

    skid = Skidsteer(SKIDSTEER_LEN, SKIDSTEER_WIDTH)
    skid.reset()


    coords: list[tuple[float, float]] = []
    (v_l, v_r) = skid.calc_inst_radius_velocities(8, CIRCLE_RADIUS)

    print(f"V_l: {v_l}, V_r: {v_r}, Desired Radius: {CIRCLE_RADIUS}, Actual Radius: {skid.calc_inst_radius_dist(v_l, v_r)}, stuff: {(v_l + v_r) / 2}")


    for i in range(1, int(5 / DELTA_TIME)):
        coords.append((skid.get_xpos(), skid.get_ypos()))
        (v_l, v_r) = skid.calc_turning_left_clamped_velocities(8, CIRCLE_RADIUS, 5, DELTA_TIME * i)
        skid.move_time(v_l, v_r, DELTA_TIME)


    for _ in range(50):
        coords.append((skid.get_xpos(), skid.get_ypos()))
        (v_l, v_r) = skid.calc_turning_left_clamped_velocities(8, CIRCLE_RADIUS, 1, 1)
        skid.move_time(v_l, v_r, DELTA_TIME)
        




    plt.plot([x for (x, y) in coords], [y for (x, y) in coords], "r")
    # # plt.legend(loc="upper right")
    plt.show()

main()
