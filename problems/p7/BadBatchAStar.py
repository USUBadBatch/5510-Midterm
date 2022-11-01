"""

A* grid planning

author: Atsushi Sakai(@Atsushi_twi)
        Nikos Kanargias (nkana@tee.gr)

See Wikipedia article (https://en.wikipedia.org/wiki/A*_search_algorithm)

"""

import math

import matplotlib.pyplot as plt

show_animation = False


class AStarQueue:
    def __init__(self):
        self.__queue = []
        self.__idx = 0

    def enqueue(self, element):
        idx = len(self.__queue)
        for i, el in enumerate(self.__queue):
            if element < el:
                idx = i
                break

        self.__queue.insert(idx, element)

    def dequeue(self):
        return self.__queue.pop(0)

    def bounty_hunter(self, target_id):
        for el in self.__queue:
            if target_id == el:
                return el

        return None

    def __len__(self):
        return len(self.__queue)

    def __next__(self):
        if self.__idx >= len(self.__queue):
            self.__idx = 0
            raise StopIteration
        else: 
            el = self.__queue[self.__idx]
            self.__idx += 1
            return el

    def __iter__(self):
        return self


class AStarPlanner:

    def __init__(self, ox, oy, resolution, rr):
        """
        Initialize grid map for a star planning

        ox: x position list of Obstacles [m]
        oy: y position list of Obstacles [m]
        resolution: grid resolution [m]
        rr: robot radius[m]
        """

        self.resolution = resolution
        self.rr = rr
        self.min_x, self.min_y = 0, 0
        self.max_x, self.max_y = 0, 0
        self.obstacle_map = None
        self.x_width, self.y_width = 0, 0
        self.motion = self.get_motion_model()
        self.calc_obstacle_map(ox, oy)

    class Node:
        def __init__(self, x, y, cost, dist, parent):
            self.x = x  # index of grid
            self.y = y  # index of grid
            self.cost = cost
            self.parent = parent
            self.dist = dist

        def __str__(self):
            return str(self.x) + "," + str(self.y) + "," + str(
                self.cost) + "," + str(self.parent_index)

        def __lt__(self, other):
            return self.cost + self.dist < other.cost + other.dist

        def __eq__(self, other):
            if type(other) == int: return True
            return self.x == other.x and self.y == other.y

    def planning(self, sx, sy, gx, gy):
        """
        A star path search
        """

        goal_node = self.Node(self.calc_xy_index(gx, self.min_x),
                               self.calc_xy_index(gy, self.min_y), 
                               0.0,
                               0,
                               -1)
                               
        start_node = self.Node(self.calc_xy_index(sx, self.min_x),
                               self.calc_xy_index(sy, self.min_y), 
                               0.0,
                               self.distToFinal(self.calc_xy_index(sx, self.min_x), self.calc_xy_index(sy, self.min_y), goal_node),
                               -1)

        open_set, closed_set = AStarQueue(), []
        open_set.enqueue(start_node)

        while 1:
            if len(open_set) == 0:
                print("Open set is empty..")
                break

            current = open_set.dequeue()

            if show_animation:  # pragma: no cover
                plt.plot(self.calc_grid_position(current.x, self.min_x),
                         self.calc_grid_position(current.y, self.min_y), "xc")
                # for stopping simulation with the esc key.
                plt.gcf().canvas.mpl_connect('key_release_event',
                                             lambda event: [exit(
                                                 0) if event.key == 'escape' else None])
                if len(closed_set) % 10 == 0:
                    plt.pause(0.001)

            if current == goal_node:
                print("Found goal")
                goal_node.parent = current.parent
                goal_node.cost = current.cost
                break

            # Add it to the closed set
            closed_set.append(current)

            # expand_grid search grid based on motion model
            for i, _ in enumerate(self.motion):
                temp_x = current.x + self.motion[i][0]
                temp_y = current.y + self.motion[i][1]
                node = self.Node(temp_x,
                                 temp_y,
                                 current.cost + self.motion[i][2],
                                 self.distToFinal(temp_x, temp_y, goal_node), 
                                 current)

                # If the node is not safe, do nothing
                if not self.verify_node(node):
                    continue

                if node in closed_set:
                    continue

                if node not in open_set:
                    open_set.enqueue(node) # discovered a new node
                else:
                    if node < open_set.bounty_hunter(node):
                        # This path is the best until now. record it
                        open_set.bounty_hunter(node).cost = node.cost
                        open_set.bounty_hunter(node).parent = node.parent

        rx, ry = self.calc_final_path(start_node, goal_node)

        return rx, ry

    def calc_final_path(self, start_node, goal_node):
        # generate final course
        rx, ry = [self.calc_grid_position(goal_node.x, self.min_x)], [
            self.calc_grid_position(goal_node.y, self.min_y)]
        n = goal_node.parent
        while not (n.x == start_node.x and n.y == start_node.y) :
            rx.append(self.calc_grid_position(n.x, self.min_x))
            ry.append(self.calc_grid_position(n.y, self.min_y))
            n = n.parent

        return rx, ry

    @staticmethod
    def distToFinal(node_x, node_y, goal):
        w = 1.2  # weight of heuristic
        d = w * math.hypot((goal.x - node_x), (goal.y - node_y))
        return d

    def calc_grid_position(self, index, min_position):
        """
        calc grid position

        :param index:
        :param min_position:
        :return:
        """
        pos = index * self.resolution + min_position
        return pos

    def calc_xy_index(self, position, min_pos):
        return round((position - min_pos) / self.resolution)

    def calc_grid_index(self, node):
        return (node.y - self.min_y) * self.x_width + (node.x - self.min_x)

    def verify_node(self, node):
        px = self.calc_grid_position(node.x, self.min_x)
        py = self.calc_grid_position(node.y, self.min_y)

        if px < self.min_x:
            return False
        elif py < self.min_y:
            return False
        elif px >= self.max_x:
            return False
        elif py >= self.max_y:
            return False

        # collision check
        if self.obstacle_map[node.x][node.y]:
            return False

        return True

    def calc_obstacle_map(self, ox, oy):

        self.min_x = round(min(ox))
        self.min_y = round(min(oy))
        self.max_x = round(max(ox))
        self.max_y = round(max(oy))

        self.x_width = round((self.max_x - self.min_x) / self.resolution)
        self.y_width = round((self.max_y - self.min_y) / self.resolution)

        # obstacle map generation
        self.obstacle_map = [[False for _ in range(self.y_width)]
                             for _ in range(self.x_width)]
        for ix in range(self.x_width):
            x = self.calc_grid_position(ix, self.min_x)
            for iy in range(self.y_width):
                y = self.calc_grid_position(iy, self.min_y)
                for iox, ioy in zip(ox, oy):
                    d = math.hypot(iox - x, ioy - y)
                    if d <= self.rr:
                        self.obstacle_map[ix][iy] = True
                        break

    @staticmethod
    def get_motion_model():
        # dx, dy, cost
        motion = [[1, 0, 1],
                  [0, 1, 1],
                  [-1, 0, 1],
                  [0, -1, 1],
                  [-1, -1, math.sqrt(2)],
                  [-1, 1, math.sqrt(2)],
                  [1, -1, math.sqrt(2)],
                  [1, 1, math.sqrt(2)]]

        return motion


def main():
    print(__file__ + " start!!")

    # start and goal position
    sx = 10.0  # [m]
    sy = 10.0  # [m]
    gx = 50.0  # [m]
    gy = 50.0  # [m]
    grid_size = 2.0  # [m]
    robot_radius = 1.0  # [m]

    # set obstacle positions
    ox, oy = [], []
    for i in range(-10, 60):
        ox.append(i)
        oy.append(-10.0)
    for i in range(-10, 60):
        ox.append(60.0)
        oy.append(i)
    for i in range(-10, 61):
        ox.append(i)
        oy.append(60.0)
    for i in range(-10, 61):
        ox.append(-10.0)
        oy.append(i)
    for i in range(-10, 40):
        ox.append(20.0)
        oy.append(i)
    for i in range(0, 40):
        ox.append(40.0)
        oy.append(60.0 - i)

    if show_animation:  # pragma: no cover
        plt.plot(ox, oy, ".k")
        plt.plot(sx, sy, "og")
        plt.plot(gx, gy, "xb")
        plt.grid(True)
        plt.axis("equal")

    a_star = AStarPlanner(ox, oy, grid_size, robot_radius)
    rx, ry = a_star.planning(sx, sy, gx, gy)

    if show_animation:  # pragma: no cover
        plt.plot(rx, ry, "-r")
        plt.pause(0.001)
        plt.show()


if __name__ == '__main__':
    main()
