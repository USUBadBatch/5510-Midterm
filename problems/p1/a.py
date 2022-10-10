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
    coords2: list[tuple[float, float]] = []

    coords.append((skid.get_xpos(), skid.get_ypos()))
    coords2.append((skid.get_xpos(), skid.get_ypos()))
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
        coords2.append((skid.get_xpos(), skid.get_ypos()))
        i += DELTA_TIME

    #calc point on circle
    next_point: tuple[float, float] = (next_pos[0], next_pos[1])
    curr_point: tuple[float, float] = (skid.get_xpos(), skid.get_ypos())

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
    coords2.append((skid.get_xpos(), skid.get_ypos()))

    plt.plot([CIRCLE_X, skid.get_xpos()], [CIRCLE_Y, skid.get_ypos()], "g")
    v1 = np.array((skid.get_xpos() - CIRCLE_X, skid.get_ypos() - CIRCLE_Y))
    print(f"Vec1: {v1}")


    #go around circle
    #first set initial heading to align with circle
    a_new = math.atan(skid.get_ypos() / skid.get_xpos())
    print(f"Angle(rad): {a_new}, Pi / 2: {math.pi / 2}, root(2) / 2: {math.sqrt(2) / 2}, root(3) / 2: {math.sqrt(3) / 2} ")
    skid.set_theta(a_new)

    next_pos = skid.calc_next_pos(AVERAGE_VELOCITY, AVERAGE_VELOCITY, DELTA_TIME)
    next_x, next_y = (next_pos[0], next_pos[1])


    plt.plot([skid.get_xpos(), next_x], [skid.get_ypos(), next_y], "g")

    v2 = np.array((next_x - skid.get_xpos(), next_y - skid.get_ypos()))
    print(f"Vec2: {v2}")
    print(f"Vec1 dot Vec2: {np.dot(v1,v2)}")

    vl, vr = skid.calc_inst_radius_velocities(AVERAGE_VELOCITY, CIRCLE_RADIUS)
    print(f"Vl: {vl}, Vr:{vr}, Avg: {(vl + vr) / 2}")
    print(f"Inst rad: {skid.calc_inst_radius_dist(vl, vr)}")


    tmp1 = skid.clone()
    tmp2 = skid.clone()

    dtheta = skid.calc_delta_theta(vl ,vr, DELTA_TIME)
    skid.increment_theta(-dtheta / 2)

    #fixme: robit circle is still offset somehow
    for i in range(int((2 * math.pi * CIRCLE_RADIUS) / (AVERAGE_VELOCITY * DELTA_TIME)) + 1):
        print(f"Skid pos: ({skid.get_xpos(): >20.15f}, {skid.get_ypos():>20.15f}), Distance from circle center: {distance((skid.get_xpos(), skid.get_ypos()), (CIRCLE_X, CIRCLE_Y)):<.15f}")
        
        skid.set_theta_new(vl ,vr, DELTA_TIME)
        skid.set_x_new(vl ,vr, DELTA_TIME)
        skid.set_y_new(vl ,vr, DELTA_TIME)
        coords.append((skid.get_xpos(), skid.get_ypos()))

        
        # print(f"Skid pos: ({tmp1.get_xpos(): >20.15f}, {tmp1.get_ypos():>20.15f}), Distance from circle center: {distance((tmp1.get_xpos(), tmp1.get_ypos()), (CIRCLE_X, CIRCLE_Y)):<.15f}")
        # tmp1.set_x_new(vl ,vr, DELTA_TIME)
        # tmp1.set_y_new(vl ,vr, DELTA_TIME)
        # tmp1.set_theta_new(vl ,vr, DELTA_TIME)
        # coords2.append((tmp1.get_xpos(), tmp1.get_ypos()))








    plt.plot([x for (x, y) in coords], [y for (x, y) in coords], color="red")
    # plt.plot([x for (x, y) in coords2], [y for (x, y) in coords2], color="orange")
    plt.scatter(CIRCLE_X, CIRCLE_Y, color="blue")
    circle_main = plt.Circle((CIRCLE_X, CIRCLE_Y), CIRCLE_RADIUS, color='b', fill=False)  # type: ignore
    plt.gca().add_patch(circle_main)
    # # plt.legend(loc="upper right")
    plt.gca().set_aspect("equal")
    plt.show()

main()
