import math


class Skidsteer:
    def __init__(self, length: float, width: float) -> None:
        #length in mm
        self.__length = length
        #width in mm
        self.__width = width

        self.__x_pos = 0
        self.__y_pos = 0
        #theta dot in rad
        self.__theta_dot = 0

    
    def __calc_x_new(self, v_left: float, v_right: float, dt: float) -> float:
        return self.__x_pos - (.5 * (v_left + v_right) * math.sin(self.__theta_dot) * dt)

    def __calc_y_new(self, v_left: float, v_right: float, dt: float) -> float:
        return self.__y_pos - (.5 * (v_left + v_right) * math.cos(self.__theta_dot) * dt)

    def __calc_theta_new(self, v_left: float, v_right: float, dt: float) -> float:
        return self.__theta_dot + ((1/self.__width) * (v_right - v_left) * dt)

    def __calc_inst_radius(self, v_left: float, v_right: float) -> float:
        return (self.__width / 2) * ((v_right + v_left)/(v_right - v_left))

    def __repr__(self) -> str:
        return f"Position: ({self.__x_pos, self.__y_pos}), Theta Dot: {self.__theta_dot}"