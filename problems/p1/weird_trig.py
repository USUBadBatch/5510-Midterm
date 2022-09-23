import math
import matplotlib.pyplot as plt

# Constants
RADIUS = 2.5
WANTED_DIST = 0.8
X_0 = -0.6
Y_0 = 2.4
C_1 = (X_0**2 + Y_0**2 - WANTED_DIST**2 - RADIUS**2) / (2 * X_0)

def quadratic(a, b, c):
    return (-b + math.sqrt(b**2 - (4 * a * c))) / (2 * a), (-b - math.sqrt(b**2 - (4 * a * c))) / (2 * a)

def x_1(y_1):
    return -(Y_0 / X_0) * y_1 + C_1

def dist(x1, y1, x2, y2):
    return math.sqrt((x2 - x1)**2 + (y2 - y1)**2)

def onCircle(x, y, radius):
    print(math.sqrt(x**2 + y**2))
    return math.sqrt(x**2 + y**2) == radius

def main():
    a = (Y_0**2 + X_0**2) / (X_0**2)
    b = -(2 * Y_0) / X_0
    c = C_1 - RADIUS**2
    soln1_y1, soln2_y1 = quadratic(a, b, c)
    
    soln1 = (x_1(soln1_y1), soln1_y1)
    soln2 = (x_1(soln2_y1), soln2_y1)
    
    # print(onCircle(soln1[0], soln1[1], RADIUS))
    # print(onCircle(soln2[0], soln2[1], RADIUS))
        
    print(f"The point {soln1} is {'on' if onCircle(soln1[0], soln1[1], RADIUS) else 'not on'} the cirlce")
    print(f"The point {soln2} is {'on' if onCircle(soln2[0], soln2[1], RADIUS) else 'not on'} the cirlce")
    
    


main()
