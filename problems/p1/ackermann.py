import math



class Ackermann:
    def __init__(self, length_between_axles: float, width: float) -> None:
        self.__length = length_between_axles
        self.__width = width

        self.__x_pos = 0
        self.__y_pos = 0

        #theta in rad
        self.__theta = 0


    def calc_delta_x(self, velocity) -> float:
        return -velocity * math.sin(self.__theta)

    def calc_delta_y(self, velocity: float) -> float:
        return velocity * math.cos(self.__theta)

    def calc_delta_theta(self, velocity: float, alpha: float) -> float:
        return velocity / self.__length * math.tan(alpha)

    def calc_x_new(self, velocity: float, dt: float) -> float:
        "Calculates and returns the new x position"
        return self.__x_pos + self.calc_delta_x(velocity) * dt

    def calc_y_new(self, velocity: float, dt: float) -> float:
        "Calculatess and returns the new y position"
        return self.__y_pos + self.calc_delta_y(velocity) * dt

    def calc_theta_new(self, velocity: float, alpha: float, dt: float) -> float:
        "Calculates and returns the new theta"
        return self.__theta + self.calc_delta_theta(velocity, alpha) * dt

    def set_x_new(self, velocity: float, dt: float) -> float:
        "Calculates then sets the current instances new x_pos then returns the new x position"
        x_new = self.calc_x_new(velocity, dt)
        self.__x_pos = x_new
        return self.__x_pos

    def set_y_new(self, velocity: float, dt: float) -> float:
        "Calculates then sets the current instances new y_pos then returns the new y position"
        y_new = self.calc_y_new(velocity, dt)
        self.__y_pos = y_new
        return self.__y_pos

    def set_theta_new(self, velocity: float, alpha: float, dt: float) -> float:
        "Calculates then sets the current instances new theta then returns the new theta"
        theta_new = self.calc_theta_new(velocity, alpha, dt)
        self.__theta = theta_new
        return self.__theta

    def calc_inst_radius_dist(self, velocity: float, alpha: float) -> float:
        "Calculates and returns the instantaneous turning radius"
        return velocity / self.calc_delta_theta(velocity, alpha)

    def calc_alpha_for_inst_turning_raidus(self, radius: float) -> float:
        return math.atan(self.__length / radius)

    def reset(self, x_pos: float = 0, y_pos: float = 0, theta: float = 0, alpha: float = 0) -> None:
        "Resets the skidsteers position"
        self.__x_pos = x_pos
        self.__y_pos = y_pos
        self.__theta = theta

    
    def clone(self) -> 'Ackermann':
        tmp = Ackermann(self.__length, self.__width)
        tmp.__x_pos = self.__x_pos
        tmp.__y_pos = self.__y_pos
        tmp.__theta = self.__theta
        return tmp

    def get_xpos(self) -> float:
        return self.__x_pos

    def get_ypos(self) -> float:
        return self.__y_pos

    def get_theta(self) -> float:
        return self.__theta

    def get_alpha(self) -> float:
        return self.__alpha

    def set_xpos(self, x_pos):
        self.__x_pos = x_pos

    def set_ypos(self, y_pos):
        self.__y_pos = y_pos

    def set_theta(self, theta):
        self.__theta = theta
    
    def set_alpha(self, alpha):
        self.__alpha = alpha

    def increment_theta(self, delta_theta):
        self.__theta += delta_theta

    def get_length(self) -> float:
        return self.__length

    def get_width(self) -> float:
        return self.__width

    def calc_next_pos(self, velocity: float, alpha: float, dt: float):
        tmp = self.clone()
        tmp.set_theta_new(velocity, alpha, dt)
        tmp.set_x_new(velocity, dt)
        tmp.set_y_new(velocity, dt)

        return (tmp.__x_pos, tmp.__y_pos, tmp.__theta, dt)

    def move(self, velocity: float, alpha: float, dt: float):
        self.set_theta_new(velocity, alpha, dt)
        self.set_x_new(velocity, dt)
        self.set_y_new(velocity, dt)

        return (self.__x_pos, self.__y_pos, self.__theta, dt)

    def __repr__(self) -> str:
        return f"Position: {self.__x_pos, self.__y_pos}, Theta : {self.__theta}"