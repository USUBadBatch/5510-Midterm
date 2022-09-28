from skidsteer import Skidsteer
import numpy as np
import matplotlib.pyplot as plt
from utils import distance, law_of_cos, Circle
import math


DELTA_TIME = .1
CIRCLE_DIAMETER = 5 # in meters
SKIDSTEER_LEN = .75 # in meters
SKIDSTEER_WIDTH = .55 # still in meters
CIRCLE_RADIUS = CIRCLE_DIAMETER / 2
AVERAGE_VELOCITY = 8
CIRCLE_X, CIRCLE_Y = (0,0)







def main():

    skid = Skidsteer(SKIDSTEER_LEN, SKIDSTEER_WIDTH)
    # skid.reset(x_pos = -.6, y_pos = 2.3)
    skid.reset()


    coords: list[tuple[float, float]] = []

    coords.append((skid.get_xpos(), skid.get_ypos()))
    i = 0
    vl, vr = (0,0)
    next_pos = None

    #get to the edge
    while True:
        vl, vr = skid.calc_turning_left_clamped_velocities(AVERAGE_VELOCITY, CIRCLE_RADIUS, 1, i)


        next_pos = skid.get_next_pos(vl, vr, DELTA_TIME)
        if distance((next_pos[0], next_pos[1]), (CIRCLE_X, CIRCLE_Y)) > CIRCLE_RADIUS:
            break
        else:
            skid.move_time(vl, vr, DELTA_TIME)

        coords.append((skid.get_xpos(), skid.get_ypos()))
        i += DELTA_TIME

    #calc point on circle
    next_point = (next_pos[0], next_pos[1])
    curr_point = (skid.get_xpos(), skid.get_ypos())

    possible_solutions = Circle.find_intersection_points(Circle(CIRCLE_RADIUS, CIRCLE_X, CIRCLE_Y), Circle(AVERAGE_VELOCITY * DELTA_TIME, curr_point[0], curr_point[1]))
    ps1_distance = distance(next_point, possible_solutions[0])
    ps2_distance = distance(next_point, possible_solutions[1])

    solution = None
    if ps1_distance < ps2_distance:
        solution = possible_solutions[0]
    else:
        solution = possible_solutions[1]

    #use law of cos to find new delta theta
    delta_theta = law_of_cos(distance(curr_point, next_point), distance(curr_point, solution), distance(solution, next_point))

    #move to edge of circle
    skid.incriment_theta(delta_theta)
    skid.move_time(AVERAGE_VELOCITY, AVERAGE_VELOCITY, DELTA_TIME)
    coords.append((skid.get_xpos(), skid.get_ypos()))

    print(f"Skid pos: ({skid.get_xpos(), skid.get_ypos()}), Distance from circle center: {distance((skid.get_xpos(), skid.get_ypos()), (CIRCLE_X, CIRCLE_Y))}")


    #go around circle
    #fixme: this do be broken
    for i in range(int((2 * math.pi * CIRCLE_RADIUS) / (AVERAGE_VELOCITY * DELTA_TIME))):
        vl, vr = skid.calc_inst_radius_velocities(AVERAGE_VELOCITY, CIRCLE_RADIUS)
        skid.move_time(vl ,vr, DELTA_TIME)
        coords.append((skid.get_xpos(), skid.get_ypos()))
        print(f"Skid pos: ({skid.get_xpos(), skid.get_ypos()}), Distance from circle center: {distance((skid.get_xpos(), skid.get_ypos()), (CIRCLE_X, CIRCLE_Y))}")







    plt.plot([x for (x, y) in coords], [y for (x, y) in coords], "r")
    # # plt.legend(loc="upper right")
    plt.show()

main()
