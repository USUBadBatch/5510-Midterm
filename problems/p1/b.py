import math
from utils import distance, Circle, law_of_cos
import matplotlib.pyplot as plt
import numpy as np

from ackermann import Ackermann


DELTA_TIME = .1 #s
CIRCLE_DIAMETER = 5 #m
ACKERMANN_LEN = .75 #m
ACKERMANN_WIDTH = .55 #m
CIRCLE_RADIUS = CIRCLE_DIAMETER / 2 #m
AVERAGE_VELOCITY = 8 #m/s
CIRCLE_X, CIRCLE_Y = (0,0) 


def main():
    global DELTA_TIME
    car = Ackermann(ACKERMANN_LEN, ACKERMANN_WIDTH)
    car.reset()

    coords: list[tuple[float, float]] = []
    coords.append((car.get_xpos(), car.get_ypos()))
    print(car)

    car.move(AVERAGE_VELOCITY, 0, DELTA_TIME)
    coords.append((car.get_xpos(), car.get_ypos()))
    print(car)
    
    
    next_pos = None
    count = 0
    alpha = 0
    while True:
        alpha: float = (math.pi / 2.5) - (DELTA_TIME * count)
        print(f"alpha: {(math.pi / 2.5) - (DELTA_TIME * count)}")


        count += 1
        next_pos = car.calc_next_pos(AVERAGE_VELOCITY, alpha, DELTA_TIME)

        if distance((next_pos[0], next_pos[1]), (CIRCLE_X, CIRCLE_Y)) > CIRCLE_RADIUS:
            break
        else:
            car.move(AVERAGE_VELOCITY, alpha, DELTA_TIME)
            print(car)

        coords.append((car.get_xpos(), car.get_ypos()))

    next_point = (next_pos[0], next_pos[1])
    curr_point = (car.get_xpos(), car.get_ypos())

    circle_cur = plt.Circle((curr_point), .8, fill=False) #type: ignore



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
    car.increment_theta(delta_theta + car.calc_delta_theta(AVERAGE_VELOCITY, alpha) * DELTA_TIME)

    car.move(AVERAGE_VELOCITY, 0, DELTA_TIME)
    coords.append((car.get_xpos(), car.get_ypos()))


    #todo: set heading
    #todo: fix this is broken
    a_new = math.atan(car.get_ypos() / car.get_xpos()) + math.pi
    a_old = car.get_theta()
    a_new1 = (a_new - a_old) / 2
    car.increment_theta(a_new1)



    alpha = car.calc_alpha_for_inst_turning_raidus(2.5)
    for i in range(int((2 * math.pi * CIRCLE_RADIUS) / (AVERAGE_VELOCITY * DELTA_TIME)) + 1):
        car.move(AVERAGE_VELOCITY, alpha, DELTA_TIME)


        coords.append((car.get_xpos(), car.get_ypos()))


    plt.plot([x for (x, y) in coords], [y for (x, y) in coords], color="red")
    plt.scatter(CIRCLE_X, CIRCLE_Y, color="blue")
    circle_main = plt.Circle((CIRCLE_X, CIRCLE_Y), CIRCLE_RADIUS, color='b', fill=False)  # type: ignore
    plt.gca().add_patch(circle_main)
    plt.gca().add_patch(circle_cur)
    plt.gca().set_aspect("equal")
    plt.show()



main()