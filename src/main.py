"""
This file is a part of the CSC111 final project by Alamgir Khan, Aman Rana,
Rahul Jaideep and Dhruvaa Saravanan.

This program runs a visualisation tool to calculate and visualise the shortest path between 2
randomly generated points on a randomly generated maze. It does so be using various heuristics and
highlights the path it has found between the points in green.
"""

import visualisation
import pygame

WIDTH = 900

if __name__ == '__main__':
    WINDOW = pygame.display.set_mode((WIDTH, WIDTH))  # Creating pygame window of WIDTH * WIDTH
    pygame.display.set_caption(
        "CSC111 Final Project: Pathfinding Visualization")  # Adding caption for pygame window
    visualisation.run_visualization(WINDOW, WIDTH)
