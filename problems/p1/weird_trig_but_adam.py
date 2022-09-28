import math
import numpy as np


Circle = lambda radius, x0, y0 : {"radius": radius, "x0" : x0, "y0" : y0}

def points(c1params, c2params):
    
    x1 = c1params["x0"]
    x2 = c2params["x0"]

    y1 = c1params["y0"]
    y2 = c2params["y0"]

    r1 = c1params["radius"]
    r2 = c2params["radius"]

    R = math.sqrt((x2 - x1) **2 + (y2 - y1) ** 2)

    p1 = np.array((x1 + x2, y1 + y2))
    p2 = np.array((x2 - x1, y2 - y1))
    p3 = np.array((y2 - y1, x1 - x2))

    s1 = (1/2)
    s2 = (r1**2 - r2**2) / (2 * R ** 2)
    s3 = (1/2) * math.sqrt((2 * (r1 ** 2 + r2 ** 2) / (R ** 2)) - (((r1 ** 2 - r2 ** 2) ** 2) / (R ** 4)) - 1)

    return ((s1 * p1) + (s2 * p2) + (s3 * p3), (s1 * p1) + (s2 * p2) - (s3 * p3))

print(points(Circle(2.5, 0, 0), Circle(.8, -.6, 2.4)))