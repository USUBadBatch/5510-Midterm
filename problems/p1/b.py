import math
from utils import distance
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

    car.move(AVERAGE_VELOCITY, math.pi / 4, DELTA_TIME)
    coords.append((car.get_xpos(), car.get_ypos()))

    car.move(AVERAGE_VELOCITY, math.pi / 5, DELTA_TIME)
    coords.append((car.get_xpos(), car.get_ypos()))

    car.move(AVERAGE_VELOCITY, math.pi / 6, DELTA_TIME)
    coords.append((car.get_xpos(), car.get_ypos()))

    car.move(AVERAGE_VELOCITY, math.pi / 7, DELTA_TIME)
    coords.append((car.get_xpos(), car.get_ypos()))
    
    car.move(AVERAGE_VELOCITY, math.pi / 8, DELTA_TIME)
    coords.append((car.get_xpos(), car.get_ypos()))





    

    plt.plot([x for (x, y) in coords], [y for (x, y) in coords], color="red")
    # plt.plot([x for (x, y) in coords2], [y for (x, y) in coords2], color="orange")
    plt.scatter(CIRCLE_X, CIRCLE_Y, color="blue")
    circle_main = plt.Circle((CIRCLE_X, CIRCLE_Y), CIRCLE_RADIUS, color='b', fill=False)
    plt.gca().add_patch(circle_main)
    # # plt.legend(loc="upper right")
    plt.gca().set_aspect("equal")
    plt.show()


main()