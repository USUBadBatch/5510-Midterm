from cProfile import label
import matplotlib.pyplot as plt
import numpy as np
import math
from utils import distance, Circle, law_of_cos
from ackermann import Ackermann


def f_euler_x(series: int, velocity: float, theta: float, dt: float):
    k = series - 1
    v = velocity

    if k <= 0:
        return 0

    return f_euler_x(k ,v, theta, dt) - v * math.sin(theta) * dt

def f_euler_y(series: int, velocity: float, theta: float, dt: float):
    k = series - 1
    v = velocity

    if k <= 0:
        return 0

    return f_euler_y(k ,v, theta, dt) + v * math.cos(theta) * dt


def main(dt):

    DELTA_TIME = dt #s
    CIRCLE_DIAMETER = 5 #m
    ACKERMANN_LEN = .75 #m
    ACKERMANN_WIDTH = .55 #m
    CIRCLE_RADIUS = CIRCLE_DIAMETER / 2 #m
    AVERAGE_VELOCITY = 8 #m/s
    CIRCLE_X, CIRCLE_Y = (0,0) 


    car = Ackermann(ACKERMANN_LEN, ACKERMANN_WIDTH)
    car.reset()

    x_error: list[float] = []
    y_error: list[float] = []

    coords: list[tuple[float, float]] = []
    coords.append((car.get_xpos(), car.get_ypos()))
    x_error.append(f_euler_x(1, AVERAGE_VELOCITY, car.get_theta(), DELTA_TIME))
    y_error.append(f_euler_y(1, AVERAGE_VELOCITY, car.get_theta(), DELTA_TIME))

    car.move(AVERAGE_VELOCITY, 0, DELTA_TIME)
    coords.append((car.get_xpos(), car.get_ypos()))
    x_error.append(f_euler_x(2, AVERAGE_VELOCITY, car.get_theta(), DELTA_TIME))
    y_error.append(f_euler_y(2, AVERAGE_VELOCITY, car.get_theta(), DELTA_TIME))
    
    
    next_pos = None
    count = 0
    alpha = 0
    while True:
        alpha: float = (math.pi / 2.5) - (DELTA_TIME * count)

        count += 1
        next_pos = car.calc_next_pos(AVERAGE_VELOCITY, alpha, DELTA_TIME)

        if distance((next_pos[0], next_pos[1]), (CIRCLE_X, CIRCLE_Y)) > CIRCLE_RADIUS:
            break
        else:
            car.move(AVERAGE_VELOCITY, alpha, DELTA_TIME)

        coords.append((car.get_xpos(), car.get_ypos()))
        x_error.append(f_euler_x(count + 2, AVERAGE_VELOCITY, car.get_theta(), DELTA_TIME))
        y_error.append(f_euler_y(count + 2, AVERAGE_VELOCITY, car.get_theta(), DELTA_TIME))

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
    car.increment_theta(delta_theta + car.calc_delta_theta(AVERAGE_VELOCITY, alpha) * DELTA_TIME)

    car.move(AVERAGE_VELOCITY, 0, DELTA_TIME)
    coords.append((car.get_xpos(), car.get_ypos()))
    x_error.append(f_euler_x(count + 3, AVERAGE_VELOCITY, car.get_theta(), DELTA_TIME))
    y_error.append(f_euler_y(count + 3, AVERAGE_VELOCITY, car.get_theta(), DELTA_TIME))


    alpha = car.calc_alpha_for_inst_turning_raidus(2.5)
    a_new = math.atan(car.get_ypos() / car.get_xpos()) 
    if a_new > 0:
        a_new -= math.pi

    a_new += math.pi    
    car.set_theta(a_new)
    car.increment_theta((-car.calc_delta_theta(AVERAGE_VELOCITY, alpha) *DELTA_TIME) / 2)

    alpha = car.calc_alpha_for_inst_turning_raidus(2.5)
    for i in range(int((2 * math.pi * CIRCLE_RADIUS) / (AVERAGE_VELOCITY * DELTA_TIME)) + 1):
        car.move(AVERAGE_VELOCITY, alpha, DELTA_TIME)

        coords.append((car.get_xpos(), car.get_ypos()))
        x_error.append(f_euler_x(count + 4 + i, AVERAGE_VELOCITY, car.get_theta(), DELTA_TIME))
        y_error.append(f_euler_y(count + 4 + i, AVERAGE_VELOCITY, car.get_theta(), DELTA_TIME))


    distances = [distance((x_error[i], y_error[i]) , (coords[i][0], coords[i][1])) for i in range(len(x_error))]


    return [i for i in range(len(x_error))], distances, [sum(distances[:i + 1]) for i in range(len(x_error))]



d1, e1, se1 = main(1)
d2, e2, se2 = main(.1)
d3, e3, se3 = main(.01)

fig, (plt1, plt2, plt3) = plt.subplots(1, 3)

# Σ
plt1.plot(d1, e1, label="Error")
plt1.plot(d1, se1, label="Σ Error")
plt1.set_title("Error for dt=1")
plt1.set_xlabel("Timestep")
plt1.set_ylabel("Error (m)")

plt2.plot(d2, e2, label="Error")
plt2.plot(d2, se2, label="Σ Error")
plt2.set_title("Error for dt=.1")
plt2.set_xlabel("Timestep")
plt2.set_ylabel("Error (m)")

plt3.plot(d3, e3, label="Error")
plt3.plot(d3, se3, label="Σ Error")
plt3.set_title("Error for dt=.01")
plt3.set_xlabel("Timestep")
plt3.set_ylabel("Error (m)")

plt.show()
