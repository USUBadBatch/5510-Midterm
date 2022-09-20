from skidsteer import Skidsteer
import numpy as np
import matplotlib.pyplot as plt
import math
from Point import Point


DELTA_TIME = .1
DIAMETER = 5 # in meters
SKIDSTEER_LEN = .75 # in meters
SKIDSTEER_WIDTH = .55 # still in meters
RADIUS = DIAMETER / 2

# this is the maximum distance that the center of the robot 
# can get from the center of the circle. Anything more than this
# and the robot is outside the circle.
MAX_DIST = (DIAMETER / 2) - (SKIDSTEER_LEN / 2)
CALIBRATED_RADIUS = math.sqrt(RADIUS**2 - ((SKIDSTEER_WIDTH / 2) ** 2)) - (SKIDSTEER_LEN / 2)
print(CALIBRATED_RADIUS)
DEBUG_FILE = open("out.txt",encoding="utf-8", mode="w+")





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



def recordBoundedCoords(skid: Skidsteer, coords: list[tuple[Point, Point, Point, Point]]) -> tuple[Point, Point, Point, Point]:
    length = skid.get_length()
    width = skid.get_width()

    points = (
        Point(
            skid.get_xpos() - (width / 2),
            skid.get_ypos() + (length / 2)
        ),
        Point(
            skid.get_xpos() + (width / 2),
            skid.get_ypos() + (length / 2)
        ),
        Point(
            skid.get_xpos() - (width / 2),
            skid.get_ypos() - (length / 2)
        ),
        Point(
            skid.get_xpos() + (width / 2),
            skid.get_ypos() - (length / 2)
        )
    )

    coords.append(points)

    return points


def main():

    skid = Skidsteer(SKIDSTEER_LEN, SKIDSTEER_WIDTH)
    skid.reset()

    coords: list[tuple[Point, Point, Point, Point]] = []

    for degree in range(360):
        #go forward
        skid.move_distance(8, 8, .1, CALIBRATED_RADIUS)
        pos = recordBoundedCoords(skid, coords)
        DEBUG_FILE.write(f"Front ({skid.get_xpos()}, {skid.get_ypos()})\n")
        # DEBUG_FILE.write(f"Front Left: {pos[0]}, Front Right: {pos[1]}, Rear Left: {pos[2]}, Rear Right: {pos[3]}\n")

        #go backwards
        skid.move_distance(-8, -8, .1, CALIBRATED_RADIUS)
        # print(f"Back ({skid.get_xpos()}, {skid.get_ypos()})")

        #turn left 1 degree
        skid.turn(-1, 1, math.radians(1))





    plt.plot([fl.x for (fl, fr, rl, rr) in coords], [fl.y for (fl, fr, rl, rr) in coords], "r", label="fl")
    # plt.plot([fr.x for (fl, fr, rl, rr) in coords], [fr.y for (fl, fr, rl, rr) in coords], "g", label="fr")
    # plt.plot([rl.x for (fl, fr, rl, rr) in coords], [rl.y for (fl, fr, rl, rr) in coords], "b", label="rl")
    # plt.plot([rr.x for (fl, fr, rl, rr) in coords], [rr.y for (fl, fr, rl, rr) in coords], "y", label="rr")


    plt.legend(loc="upper right")
    plt.show()

main()
