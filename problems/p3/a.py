from Manipulator import Manipulator

def main():
    # Angles are measured in degrees
    theta1 = -90
    theta4 = -90
    theta5 = 90
    theta6 = 40

    # distances are measured in meters
    d1 = .6
    d2 = .5
    d3 = 1
    d6 = .2

    starting_lengths = (d1, d2, d3, d6)
    starting_angles = (theta1, theta4, theta5, theta6)

    m = Manipulator(lengths=starting_lengths, angles=starting_angles)
    iterations = m.moveTo(1.2, .8, .5)
    end_lengths, end_angels = m.getDistancesAndAngels()

    print(
f"""

The final angles and distances are as follows:

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

Results were found in {iterations} Monte Carlo iterations
"""
)

main()