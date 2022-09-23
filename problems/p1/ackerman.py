import math



class Ackerman:
    def __init__(self, length: float, width: float) -> None:
        self.__length = length
        self.__width = width

        self.__x_pos = 0
        self.__y_pos = 0

        #theta in rad
        self.__theta = 0

    
    def calc_x_new(self, v_left: float, v_right: float, dt: float) -> float:
        "Calculates and returns the new x position"
        return self.__x_pos - (.5 * (v_left + v_right) * math.sin(self.__theta) * dt)

    def calc_y_new(self, v_left: float, v_right: float, dt: float) -> float:
        "Calculatess and returns the new y position"
        return self.__y_pos + (.5 * (v_left + v_right) * math.cos(self.__theta) * dt)

    def calc_theta_new(self, v_left: float, v_right: float, dt: float) -> float:
        "Calculates and returns the new theta"
        return self.__theta + ((1/self.__width) * (v_right - v_left) * dt)

    def calc_inst_radius_dist(self, v_left: float, v_right: float) -> float:
        "Calculates and returns the instantaneous turning radius"
        return (self.__width / 2) * ((v_right + v_left)/(v_right - v_left))

    def calc_inst_radius_velocities_ratio(self, radius: float) -> float:
        "Returns the ration of V_r/V_l"

        return (1 + ((2 * radius) / self.__width)) / (-1 + ((2 * radius) / self.__width))

    def calc_inst_radius_velocitites(self, avg_velocity: float, radius: float) -> tuple[float, float]:
        "Returns (v_l, v_r)"

        ratio = self.calc_inst_radius_velocities_ratio(radius)
        v_l = (-4/self.get_width()) + ((8 * radius) / (self.get_width() ** 2))
        v_r = v_l * ratio

        return (v_l, v_r)



    def set_x_new(self, v_left: float, v_right: float, dt: float) -> float:
        "Calculates then sets the current instances new x_pos then returns the new x position"
        x_new = self.calc_x_new(v_left, v_right, dt)
        self.__x_pos = x_new
        return self.__x_pos

    def set_y_new(self, v_left: float, v_right: float, dt: float) -> float:
        "Calculates then sets the current instances new y_pos then returns the new y position"
        y_new = self.calc_y_new(v_left, v_right, dt)
        self.__y_pos = y_new
        return self.__y_pos

    def set_theta_new(self, v_left: float, v_right: float, dt: float) -> float:
        "Calculates then sets the current instances new theta then returns the new theta"
        theta_new = self.calc_theta_new(v_left, v_right, dt)
        self.__theta = theta_new
        return self.__theta

    def reset(self, x_pos: float = 0, y_pos: float = 0, theta: float = 0) -> None:
        "Resets the skidsteers position"
        self.__x_pos = x_pos
        self.__y_pos = y_pos
        self.__theta = theta

    def calculate_turn_time(self, v_left: float, v_right: float, desired_relative_angle_radians: float) -> float:
        return desired_relative_angle_radians * self.__width / (v_right - v_left)

    def move_time(self, v_left: float, v_right: float, dt: float) -> tuple[float, float, float, float]:
        "Returns (xpos, ypos, theta, dt)"
        self.set_x_new(v_left, v_right, dt)
        self.set_y_new(v_left, v_right, dt)
        self.set_theta_new(v_left, v_right, dt)

        return (self.__x_pos, self.__y_pos, self.__theta, dt)

    def move_distance(self, v_left: float, v_right: float, dt: float, distance: float) -> tuple[float, float, float, float]:
        whole_iters = int(abs(distance / ((v_left + v_right) / 2 * dt)))
        remainder_iter = distance % (v_left + v_right) / 2 * dt
        last_pos = None

        for _ in range(int(whole_iters)):
            last_post = self.move_time(v_left, v_right, dt)

        last_pos = self.move_time(v_left, v_right, )

        return last_pos

    def turn(self, v_left: float, v_right: float, desired_relative_angle_radians: float) -> tuple[float, float, float, float]:
        "Returns (xpos, ypos, theta, dt)"
        turn_time = self.calculate_turn_time(v_left, v_right, desired_relative_angle_radians)

        self.set_x_new(v_left, v_right, turn_time)
        self.set_y_new(v_left, v_right, turn_time)
        self.set_theta_new(v_left, v_right, turn_time)

        return (self.__x_pos, self.__y_pos, self.__theta, turn_time)


    def get_xpos(self) -> float:
        return self.__x_pos

    def get_ypos(self) -> float:
        return self.__y_pos

    def get_theta(self) -> float:
        return self.__theta

    def get_angular_velocity(self) -> float:
        pass

    def get_length(self) -> float:
        return self.__length

    def get_width(self) -> float:
        return self.__width

    def __repr__(self) -> str:
        return f"Position: ({self.__x_pos, self.__y_pos}), Theta Dot: {self.__theta}"