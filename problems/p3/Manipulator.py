from importlib.resources import path
from math import sqrt
from random import random
from manipulatorInfo import ManipulatorInfo

class Manipulator:
    def __init__(self, lengths, angles, accepted_error=.1, monte_carlo_num_iterations=100_000):
        self.__manipulator_position = ManipulatorInfo(lengths, angles)

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

            d1, d2, d3, d6 = self.__manipulator_position.getLengths()
            theta1, theta4, theta5, theta6 = self.__manipulator_position.getAngles()

            # pos_new_d1 = self.__d1 + temp_d1
            possible_manipulator_position = ManipulatorInfo(
                lengths=(
                    d1, # d1 is set and won't change
                    max(0, d2 + temp_d2),
                    max(0, d3 + temp_d3),
                    max(0, d6 + temp_d6),
                ), 
                angles=(
                    theta1 + temp_theta1,
                    theta4 + temp_theta4,
                    theta5 + temp_theta5,
                    theta6 + temp_theta6,
                )
            )

            temp_error = self.calculateDistanceOfTwoPoints(
                target_point, 
                possible_manipulator_position.getEndEffectorPosition()
            )
            if temp_error < curr_error:
                # d1 is set
                # self.__d1 = pos_new_d1 
                self.__manipulator_position = possible_manipulator_position

                curr_error = temp_error

        return i - 1

    def getDistancesAndAngels(self):
        return self.__manipulator_position.getLengths(), self.__manipulator_position.getAngles()

    def calculateEndEffectorError(self, target_point):
        return self.calculateDistanceOfTwoPoints(
            target_point, 
            self.__manipulator_position.getEndEffectorPosition()
        )

    def calculateDistanceOfTwoPoints(self, point1, point2):
        diff_x = point1[0] - point2[0]
        diff_y = point1[1] - point2[1]
        diff_z = point1[2] - point2[2]

        return sqrt((diff_x * diff_x) + (diff_y * diff_y) + (diff_z * diff_z))

    def moveToShortest(self, targ_x:float, targ_y:float, targ_z:float):
        target_point = (targ_x, targ_y, targ_z)
        q = Queue()
        mani_x, mani_y, mani_z = self.__manipulator_position.getEndEffectorPosition()
        curr_point:Point = Point(x=mani_x, y=mani_y, z=mani_z, cost_from_start=0, cost_to_end=self.calculateDistanceOfTwoPoints(target_point, (mani_x, mani_y, mani_z)))
        movements = [-self.__accepted_error, 0, self.__accepted_error]
        while curr_point.getCostToEnd() > self.__accepted_error:
            # print(f"Current Point to Final {curr_point.getCostToEnd()}")
            for move_x in movements:
                for move_y in movements:
                    for move_z in movements:
                        if move_x == 0 and move_y and move_z: continue
                        x = curr_point.x + move_x
                        y = curr_point.y + move_y
                        z = curr_point.z + move_z
                        dist_from_start = self.calculateDistanceOfTwoPoints((x,y,z), curr_point.getXYZ())
                        dist_to_end = self.calculateDistanceOfTwoPoints(target_point, (x,y,z))
                        q.enqueue(Point(x, y, z, parent_point=curr_point, cost_from_start=dist_from_start, cost_to_end=dist_to_end))

            curr_point = q.dequeue()

        # print(f"Current Point has heuristic of {curr_point.totEstCost()}")
        # print(f"Current Point has length of {curr_point.getCostToEnd()}")

        path_list = []
        while not curr_point == None:
            x, y, z = curr_point.getXYZ()
            path_list.append({
                "x": x, 
                "y": y, 
                "z": z, 
                "dist_to_end": curr_point.getCostToEnd(),
            })
            curr_point = curr_point.getParent()

        path_list.reverse()
        for point in path_list:
            self.moveTo(point["x"], point['y'], point['z'])
            (d1, d2, d3, d6), (theta1, theta4, theta5, theta6) = self.getDistancesAndAngels()
            point["d1"] = d1
            point["d2"] = d2
            point["d3"] = d3
            point["d6"] = d6
            point["theta1"] = theta1
            point["theta4"] = theta4
            point["theta5"] = theta5
            point["theta6"] = theta6

        return path_list

    def getPos(self):
        return self.__manipulator_position.getEndEffectorPosition()



class Queue:
    """
    A* algorithm's queue
    """
    def __init__(self):
        self.__queue = []

    def enqueue(self, element):
        idx = len(self.__queue)
        for i, el in enumerate(self.__queue):
            if element < el:
                idx = i
                break

        self.__queue.insert(idx, element)

    def dequeue(self):
        return self.__queue.pop(0)

    def __len__(self):
        return len(self.__queue)

    def __str__(self):
        msg = ''
        for i, point in enumerate(self.__queue):
            msg += f"{i}: {point}\n"

        return msg


class Point:
    decrimentor = .95
    def __init__(self,
        x, 
        y, 
        z, 
        parent_point=None, 
        cost_from_start=None, 
        cost_to_end=None
    ):
        self.x = x
        self.y = y
        self.z = z
        self.__parent_point = parent_point
        self.__cost_from_start = cost_from_start
        self.__cost_to_end = cost_to_end

    def getXYZ(self):
        return (self.x, self.y, self.z)

    def getParent(self):
        return self.__parent_point

    def totEstCost(self):
        dec = Point.decrimentor
        val = self.__cost_from_start + (2 * dec + 3) * self.__cost_to_end
        return val

    def __lt__(self, point):
        Point.decrimentor *= .95
        return self.totEstCost() < point.totEstCost()

    def getCostToEnd(self):
        return self.__cost_to_end

    def __str__(self):
        return f"x: {self.x}, y: {self.y}, z: {self.z}, cost: {self.totEstCost()}"


