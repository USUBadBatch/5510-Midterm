from math import sin, cos, sqrt
from random import random

class Manipulator:
    def __init__(self, lengths, angles, accepted_error=.1, monte_carlo_num_iterations=100_000):
        self.__d1 = lengths[0]
        self.__d2 = lengths[1]
        self.__d3 = lengths[2]
        self.__d6 = lengths[3]

        self.__theta1 = angles[0]
        self.__theta4 = angles[1]
        self.__theta5 = angles[2]
        self.__theta6 = angles[3]

        x, y, z = self.calculatePos(
            self.__d1, 
            self.__d2, 
            self.__d3, 
            self.__d6, 
            self.__theta1, 
            self.__theta4, 
            self.__theta5
        )

        self.__endEffectorPosX = x
        self.__endEffectorPosY = y
        self.__endEffectorPosZ = z

        self.__num_monte_carlo_iterations = monte_carlo_num_iterations
        self.__accepted_error = accepted_error

    """
    Description:
    Moves the manipulator to the sepcified location.

    Input:
    targ_x: float = target x coordinate
    targ_y: float = target y coordinate
    targ_z: float = target z coordinate

    Output:
    iterations: int = number of iterations it took to find acceptable point
    """
    def moveTo(self, targ_x:float, targ_y:float, targ_z:float):
        target_point = (targ_x, targ_y, targ_z)
        curr_error = self.calculateEndEffectorError(target_point)

        for i in range(self.__num_monte_carlo_iterations):
            if curr_error < self.__accepted_error:
                break

            # subtracting half of the multiplier allows for negative values
            # d1 doesn't need to change
            # temp_d1 = (random() * 2) - 1
            temp_d2 = (random() * 2) - 1
            temp_d3 = (random() * 2) - 1
            temp_d6 = (random() * 2) - 1
            temp_theta1 = (random() * 20) - 10
            temp_theta4 = (random() * 20) - 10
            temp_theta5 = (random() * 20) - 10
            temp_theta6 = (random() * 20) - 10

            # pos_new_d1 = self.__d1 + temp_d1
            pos_new_d1 = self.__d1 # d1 is set and won't change
            pos_new_d2 = self.__d2 + temp_d2
            pos_new_d3 = self.__d3 + temp_d3
            pos_new_d6 = self.__d6 + temp_d6
            pos_new_theta1 = self.__theta1 + temp_theta1
            pos_new_theta4 = self.__theta4 + temp_theta4
            pos_new_theta5 = self.__theta5 + temp_theta5
            pos_new_theta6 = self.__theta6 + temp_theta6

            temp_position = self.calculatePos(
                pos_new_d1, 
                pos_new_d2, 
                pos_new_d3, 
                pos_new_d6,
                pos_new_theta1,
                pos_new_theta4,
                pos_new_theta5,
            )
            temp_error = self.calculateDistanceOfTwoPoints(target_point, temp_position)
            if temp_error < curr_error:
                # d1 is set
                # self.__d1 = pos_new_d1 
                self.__d2 = pos_new_d2
                self.__d3 = pos_new_d3
                self.__d6 = pos_new_d6
                self.__theta1 = pos_new_theta1
                self.__theta4 = pos_new_theta4
                self.__theta5 = pos_new_theta5
                self.__theta6 = pos_new_theta6

                curr_error = temp_error

        return i - 1

    def getLengths(self):
        return (
            self.__d1,
            self.__d2,
            self.__d3,
            self.__d6,
        )

    def getAngles(self):
        return (
            self.__theta1,
            self.__theta4,
            self.__theta5,
            self.__theta6,
        )

    def getDistancesAndAngels(self):
        return self.getLengths(), self.getAngles()

    def calculatePos(self, d1, d2, d3, d6, theta1, theta4, theta5):
        x = cos(theta1) * cos(theta4) * sin(theta5) * d6 - sin(theta1) * cos(theta5) * d6 - sin(theta1) * d3
        y = sin(theta1) * cos(theta4) * sin(theta5) * d6 + cos(theta1) * cos(theta5) * d6 + cos(theta1) * d3
        z = -1 * sin(theta4) * sin(theta5) * d6 + d1 + d2

        return x, y, z

    def calculateEndEffectorError(self, target_point):
        point2 = (self.__endEffectorPosX, self.__endEffectorPosY, self.__endEffectorPosZ)

        return self.calculateDistanceOfTwoPoints(target_point, point2)

    def calculateDistanceOfTwoPoints(self, point1, point2):
        diff_x = point1[0] - point2[0]
        diff_y = point1[1] - point2[1]
        diff_z = point1[2] - point2[2]

        return sqrt((diff_x * diff_x) + (diff_y * diff_y) + (diff_z * diff_z))

