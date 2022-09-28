import math
import sys
import os
import numpy as np


def distance(p1: tuple[float, float], p2: tuple[float, float]) -> float:
    return math.sqrt((p2[0] - p1[0]) ** 2 + (p2[1] - p1[1]) ** 2)


def law_of_cos(a: float, b: float,c: float) -> float:
    return math.acos((a ** 2 + b **2 - c**2) * (1/(2 * a * b)))

class Circle:
    def __init__(self, radius: float, x: float, y: float) -> None:
        self.__radius = radius
        self.__x = x
        self.__y = y

    @staticmethod
    def find_intersection_points(c1: 'Circle', c2: 'Circle') -> tuple[tuple[float, float], tuple[float, float]]:
        #https://math.stackexchange.com/questions/256100/how-can-i-find-the-points-at-which-two-circles-intersect
        x1 = c1.__x
        x2 = c2.__x

        y1 = c1.__y
        y2 = c2.__y

        r1 = c1.__radius
        r2 = c2.__radius

        R = distance((x1, y1), (x2, y2))
        # math.sqrt((x2 - x1) **2 + (y2 - y1) ** 2)

        p1 = np.array((x1 + x2, y1 + y2))
        p2 = np.array((x2 - x1, y2 - y1))
        p3 = np.array((y2 - y1, x1 - x2))

        s1 = (1/2)
        s2 = (r1**2 - r2**2) / (2 * R ** 2)
        s3 = (1/2) * math.sqrt((2 * (r1 ** 2 + r2 ** 2) / (R ** 2)) - (((r1 ** 2 - r2 ** 2) ** 2) / (R ** 4)) - 1)

        return ((s1 * p1) + (s2 * p2) + (s3 * p3), (s1 * p1) + (s2 * p2) - (s3 * p3))