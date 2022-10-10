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
    car = Ackermann(ACKERMANN_LEN, ACKERMANN_WIDTH)
    car.reset()

    coords: list[tuple[float, float]] = []
    coords.append((car.get_xpos(), car.get_ypos()))
    car.move(AVERAGE_VELOCITY, 0, DELTA_TIME)
    coords.append((car.get_xpos(), car.get_ypos()))

    next_pos = None

    count = 3
    while True:
        alpha = math.pi / count
        # print(f"alpha: {math.pi / count}")
        count += 1
        next_pos = car.calc_next_pos(AVERAGE_VELOCITY, alpha, DELTA_TIME)

        if distance((next_pos[0], next_pos[1]), (CIRCLE_X, CIRCLE_Y)) > CIRCLE_RADIUS:
            break
        else:
            car.move(AVERAGE_VELOCITY, alpha, DELTA_TIME)
        coords.append((car.get_xpos(), car.get_ypos()))

    next_point = (next_pos[0], next_pos[1])
    curr_point = (car.get_xpos(), car.get_ypos())
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
    # car.increment_theta(delta_theta)
    # car.move(AVERAGE_VELOCITY, delta_theta, DELTA_TIME)
    # coords.append((car.get_xpos(), car.get_ypos()))
    plt.scatter(*solution, color="blue")
    plt.plot([curr_point[0], next_point[0]], [curr_point[1], next_point[1]], color="green")
    dx = 0.8 * math.cos(car.get_theta() + math.pi)
    dy = 0.8 * math.sin(car.get_theta() + math.pi)
    print(f"Theta: {car.get_theta()}\nDelta Theta: {delta_theta}\nDelta X: {dx}\nDelta Y: {dy}")
    plt.plot([curr_point[0], curr_point[0] - dx], [curr_point[1], curr_point[1] + dy], color="green")

    

    plt.plot([x for (x, y) in coords], [y for (x, y) in coords], color="red")
    # plt.plot([x for (x, y) in coords2], [y for (x, y) in coords2], color="orange")
    plt.scatter(CIRCLE_X, CIRCLE_Y, color="blue")
    circle_main = plt.Circle((CIRCLE_X, CIRCLE_Y), CIRCLE_RADIUS, color='b', fill=False)  # type: ignore
    plt.gca().add_patch(circle_main)
    # # plt.legend(loc="upper right")
    plt.gca().set_aspect("equal")
    plt.show()


main()