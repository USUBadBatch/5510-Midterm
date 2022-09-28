from skidsteer import Skidsteer
import numpy as np
import matplotlib.pyplot as plt
from utils import distance, law_of_cos, Circle
import math


DELTA_TIME = .1 #s
CIRCLE_DIAMETER = 5 #m
SKIDSTEER_LEN = .75 #m
SKIDSTEER_WIDTH = .55 #m
CIRCLE_RADIUS = CIRCLE_DIAMETER / 2 #m
AVERAGE_VELOCITY = 8 #m/s
CIRCLE_X, CIRCLE_Y = (0,0) 



def main():

    skid = Skidsteer(SKIDSTEER_LEN, SKIDSTEER_WIDTH)
    skid.reset()


    coords: list[tuple[float, float]] = []

    coords.append((skid.get_xpos(), skid.get_ypos()))
    i = 0
    vl, vr = (0,0)
    next_pos = None

    #get to the edge
    while True:
        vl, vr = skid.calc_turning_left_clamped_velocities(AVERAGE_VELOCITY, CIRCLE_RADIUS, 1, i)


        next_pos = skid.calc_next_pos(vl, vr, DELTA_TIME)
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
    skid.increment_theta(delta_theta)
    skid.move_time(AVERAGE_VELOCITY, AVERAGE_VELOCITY, DELTA_TIME)
    coords.append((skid.get_xpos(), skid.get_ypos()))

    plt.plot([CIRCLE_X, skid.get_xpos()], [CIRCLE_Y, skid.get_ypos()], "g")


    #go around circle
    #first set initial heading to align with circle
    #should be pi / 2 + angle out our pos to the center
    a1 = math.atan(skid.get_ypos() / skid.get_xpos())
    # a1 += math.pi / 2
    # a2 = math.pi / 2
    # a2 = 0
    a_new = a1 
    skid.set_theta(a_new)


    plt.plot([skid.get_xpos(), skid.calc_next_pos(AVERAGE_VELOCITY, AVERAGE_VELOCITY, DELTA_TIME)[0]], [skid.get_ypos(),skid.calc_next_pos(AVERAGE_VELOCITY, AVERAGE_VELOCITY, DELTA_TIME)[1]], "g")

    vl, vr = skid.calc_inst_radius_velocities(AVERAGE_VELOCITY, CIRCLE_RADIUS)
    #fixme: robit circle is still offset somehow
    for i in range(int((2 * math.pi * CIRCLE_RADIUS) / (AVERAGE_VELOCITY * DELTA_TIME))):
        print(f"Skid pos: ({skid.get_xpos(): >20.15f}, {skid.get_ypos():>20.15f}), Distance from circle center: {distance((skid.get_xpos(), skid.get_ypos()), (CIRCLE_X, CIRCLE_Y)):<.15f}")
        skid.set_theta_new(vl ,vr, DELTA_TIME)
        skid.set_x_new(vl ,vr, DELTA_TIME)
        skid.set_y_new(vl ,vr, DELTA_TIME)
        # skid.move_time(vl ,vr, DELTA_TIME)
        coords.append((skid.get_xpos(), skid.get_ypos()))







    plt.plot([x for (x, y) in coords], [y for (x, y) in coords], "r")
    plt.scatter(CIRCLE_X, CIRCLE_Y, color="blue")
    circle_main = plt.Circle((CIRCLE_X, CIRCLE_Y), CIRCLE_RADIUS, color='b', fill=False)
    plt.gca().add_patch(circle_main)
    # # plt.legend(loc="upper right")
    plt.show()

main()
