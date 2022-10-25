from Manipulator import Manipulator
from math import sqrt

def main():
    # Angles are measured in degrees
    theta1 = 0
    theta4 = -90
    theta5 = 90
    theta6 = 40

    # distances are measured in meters
    d1 = .6
    d2 = .2
    d3 = .3
    d6 = .2
    
    targ_x = 1.2
    targ_y = .8
    targ_z = .5

    starting_lengths = (d1, d2, d3, d6)
    starting_angles = (theta1, theta4, theta5, theta6)

    m = Manipulator(lengths=starting_lengths, angles=starting_angles)
    path = m.moveToShortest(1.2, .8, .5)
    end_lengths, end_angels = m.getDistancesAndAngels()

    # for point in path:
    #     print(f"\nx -> {point['x']}\ny -> {point['y']}\nz -> {point['z']}")
    
    print(
f"""

The final angles and distances for the shortest traveled distance are as follows:

DISTANCES:
    d1 is of length {end_lengths[0]}
    d2 is of length {end_lengths[1]}
    d3 is of length {end_lengths[2]}
    d6 is of length {end_lengths[3]}

ANGLES:
    theta 1 is {end_angels[0]} degrees
    theta 4 is {end_angels[1]} degrees
    theta 5 is {end_angels[2]} degrees
    theta 6 is {end_angels[3]} degrees

FINAL POSITION:
    x is {path[-1]['x']}
    y is {path[-1]['y']}
    z is {path[-1]['z']}
    
Which is {sqrt((targ_x - path[-1]['x'])**2 + (targ_y - path[-1]['y'])**2 + (targ_z - path[-1]['z'])**2)} meters from the target.

"""
)

main()