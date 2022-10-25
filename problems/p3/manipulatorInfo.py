from math import sin, cos

class ManipulatorInfo:
    def __init__(
            self, 
            lengths, 
            angles, 
            cost=None, 
            parent_manipulator=None,
            distance_covered=0,
        ):
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

        self.__cost_val = cost
        self.__parent_position = parent_manipulator
        self.__distanceTraveled = distance_covered

    def calculatePos(self, d1, d2, d3, d6, theta1, theta4, theta5):
        x = cos(theta1) * cos(theta4) * sin(theta5) * d6 - sin(theta1) * cos(theta5) * d6 - sin(theta1) * d3
        y = sin(theta1) * cos(theta4) * sin(theta5) * d6 + cos(theta1) * cos(theta5) * d6 + cos(theta1) * d3
        z = -1 * sin(theta4) * sin(theta5) * d6 + d1 + d2

        return x, y, z

    def getEndEffectorPosition(self):
        return self.__endEffectorPosX, self.__endEffectorPosY, self.__endEffectorPosZ

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

    def getCost(self):
        return self.__cost_val

    def setCost(self, new_cost):
        self.__cost_val = new_cost

    def getParent(self):
        return self.__parent_position

    def getDistance(self):
        return self.__distanceTraveled