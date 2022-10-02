#Author: Ben-Edwards44


import pygame
import math


G = 9.81
SHOW_PATH = True


class Pendulum:
    def __init__(self, mass_upper, mass_lower, upper_anchor, theta1, theta2, length_upper, length_lower, radius, colour, window):
        self.m1 = mass_upper
        self.m2 = mass_lower
        self.upper_anchor = upper_anchor
        self.l1 = length_upper
        self.l2 = length_lower
        self.radius = radius
        self.colour = colour
        self.window = window

        self.dt = 0.1
        self.ang_vel_u = 0
        self.ang_vel_l = 0
        self.positions = []

        self.theta = theta1
        self.theta2 = theta2

    def find_angle(self, pos1, pos2):
        x = pos1[0] - pos2[0]
        y = pos1[1] - pos2[1]

        return math.atan(x / y)

    def find_pos(self, angle, length, anchor_pos):
        x = length * math.sin(angle)
        y = length * math.cos(angle)

        return (int(anchor_pos[0] + x), int(anchor_pos[1] + y))

    def force_upper(self):
        #Equations can be found here: https://www.myphysicslab.com/pendulum/double-pendulum-en.html

        numerator1 = -G * (2 * self.m1 + self.m2) * math.sin(self.theta) - self.m2 * G * math.sin(self.theta - 2 * self.theta2)
        numerator2 = 2 * math.sin(self.theta - self.theta2) * self.m2 * (self.ang_vel_l**2 * self.l2 + self.ang_vel_u**2 * self.l1 * math.cos(self.theta - self.theta2))
        numerator = numerator1 - numerator2
        denominator = self.l1 * (2 * self.m1 + self.m2 - self.m2 * math.cos(2 * self.theta - 2 * self.theta2))
        
        self.ang_vel_u += numerator / denominator * self.dt

    def force_lower(self):
        #Equations can be found here: https://www.myphysicslab.com/pendulum/double-pendulum-en.html

        numerator = 2 * math.sin(self.theta - self.theta2) * (self.ang_vel_u**2 * self.l1 * (self.m1 + self.m2) + G * (self.m1 + self.m2) * math.cos(self.theta) + self.ang_vel_l**2 * self.l2 * self.m2 * math.cos(self.theta - self.theta2))
        denominator = self.l2 * (2 * self.m1 + self.m2 - self.m2 * math.cos(2 * self.theta - 2 * self.theta2))

        self.ang_vel_l += numerator / denominator * self.dt

    def draw_pendulum(self):
        pygame.draw.circle(self.window, self.colour, self.upper_pos, self.radius)
        pygame.draw.circle(self.window, self.colour, self.lower_pos, self.radius)

        pygame.draw.line(self.window, self.colour, self.upper_anchor, self.upper_pos, 2)
        pygame.draw.line(self.window, self.colour, self.upper_pos, self.lower_pos, 2)

    def draw_path(self):
        for i, x in enumerate(self.positions):
            if i > 0:
                pygame.draw.line(self.window, self.colour, x, self.positions[i - 1], 2)

    def main(self):
        self.force_upper()
        self.force_lower()

        new_u = self.ang_vel_u * self.dt
        new_l = self.ang_vel_l * self.dt

        self.theta += new_u
        self.theta2 += new_l

        self.upper_pos = self.find_pos(self.theta, self.l1, self.upper_anchor)
        self.lower_pos = self.find_pos(self.theta2, self.l2, self.upper_pos)

        self.positions.append(self.lower_pos)

        self.draw_pendulum()

        if SHOW_PATH:
            self.draw_path()
