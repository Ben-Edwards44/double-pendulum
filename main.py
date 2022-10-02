#Author: Ben-Edwards44


import pygame
import random
import pendulum


def init():
    global window

    pygame.init()
    window = pygame.display.set_mode((800, 500))
    pygame.display.set_caption("Double Pendulum Simulation")


def find_colour(total_num, current_num):
    if total_num <= 3:
        colour = [0, 0, 0]
        colour[current_num] = 255
        return tuple(colour)
    else:
        return ((current_num * 20) % 255, (current_num * 20) % 255, (current_num * 20) % 255)


def create_single(mass_upper, mass_lower, length_upper, length_lower, angle_upper, angle_lower, colour):
    global pendulums

    upper_anchor = (400, 100)
    p = pendulum.Pendulum(mass_upper, mass_lower, upper_anchor, angle_upper, angle_lower, length_upper, length_lower, 15, colour, window)
    pendulums = [p]


def vary_start_pos(num, length_upper, length_lower, mass_upper, mass_lower):
    global pendulums

    pendulums = []
    upper_anchor = (400, 100)

    for i in range(num):
        colour = find_colour(num, i)
        
        new = pendulum.Pendulum(mass_upper, mass_lower, upper_anchor, random.uniform(89.9, 90.1), random.uniform(89.9, 90.1), length_upper, length_lower, 15, colour, window)
        pendulums.append(new)


def vary_length(num, mass_upper, mass_lower, start_angle):
    global pendulums

    pendulums = []
    upper_anchor = (400, 100)

    for i in range(num):
        length_upper = random.uniform(140, 150)
        length_lower = random.uniform(65, 75)
        
        colour = find_colour(num, i)
        
        new = pendulum.Pendulum(mass_upper, mass_lower, upper_anchor, start_angle, start_angle, length_upper, length_lower, 15, colour, window)
        pendulums.append(new)


def main():
    while True:
        pygame.time.Clock().tick(60)
        window.fill((0, 0, 0))
        
        for i in pendulums:
            i.main()

        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                quit()

        pygame.display.update()


init()
#create_single(3, 2, 150, 75, 40, 30, (255, 255, 255))
vary_start_pos(3, 150, 75, 5, 5)
main()
