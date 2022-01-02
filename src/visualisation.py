"""
This file is a part of the CSC111 final project by Alamgir Khan, Aman Rana,
Rahul Jaideep and Dhruvaa Saravanan.

This module contains the classes and functions necessary for the visualisation of our algorithm. We
utilise pygame and combine our implementation of our pathfinding algorithm to randomly generate
pygame mazes and find the shortest path between 2 points.
"""
from typing import List
from random import randint, choice
import pygame
from pygame.colordict import THECOLORS
from algorithm import Vertex, pathfinder

ROWS = 90


def create_random_grid(num_rows: int, grid_width: int) -> List[List[Vertex]]:
    """Initialize and return a grid of grid_width with num_rows
    """
    grid = []
    node_width = grid_width // num_rows

    for row in range(num_rows):
        grid.append([])
        for column in range(num_rows):
            node = Vertex(row, column, node_width, num_rows)
            if choice([True, False]):
                node.color = THECOLORS['black']
            grid[row].append(node)

    return grid


def draw_gridlines(pygame_window: pygame.Surface, num_rows: int, grid_width: int) -> None:
    """Draw gridlines on pygame_window corresponding to num_rows and grid_width
    """
    node_width = grid_width // num_rows

    for row in range(num_rows):
        row_to_draw = row * node_width
        pygame.draw.line(pygame_window, THECOLORS['grey'], (0, row_to_draw), (grid_width,
                                                                              row_to_draw))

        for column in range(num_rows):
            column_to_draw = column * node_width
            pygame.draw.line(pygame_window, THECOLORS['grey'], (column_to_draw, 0),
                             (column_to_draw, grid_width))


def draw_grid(pygame_window: pygame.Surface, grid: List[List[Vertex]],
              num_rows: int, grid_width: int) -> None:
    """Draw a complete grid on pygame_window corresponding to the input grid,
    num_rows and grid_width
    """
    pygame_window.fill(THECOLORS['white'])  # fills screen with one color

    for row in grid:
        for node in row:
            node.draw_node(pygame_window)

    draw_gridlines(pygame_window, num_rows, grid_width)
    pygame.display.update()


def clear_paths(grid: List[List[Vertex]]) -> None:
    """
    Reset the colors of all the nodes in the current grid that are red, yellow or green
    """
    for row in range(len(grid)):
        for column in range(len(grid)):
            if grid[row][column].color == THECOLORS['red'] or \
                    grid[row][column].color == THECOLORS['yellow'] or \
                    grid[row][column].color == THECOLORS['green']:
                grid[row][column].color = THECOLORS['white']


def run_visualization(pygame_window: pygame.Surface, grid_width: int) -> None:
    """Run a visualization of the pathfinding algorithm
    """
    grid = create_random_grid(ROWS, grid_width)

    start_position = grid[randint(0, ROWS - 1)][randint(0, ROWS - 1)]
    end_position = grid[randint(0, ROWS - 1)][randint(0, ROWS - 1)]
    start_position.color = THECOLORS['blue']
    end_position.color = THECOLORS['purple']
    running = True

    while running:
        draw_grid(pygame_window, grid, ROWS, grid_width)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_m:
                    for row in grid:
                        for node in row:
                            node.update_neighbors(grid)

                    pathfinder(lambda: draw_grid(pygame_window, grid, ROWS, grid_width),
                               grid, start_position, end_position, 'manhattan')

                elif event.key == pygame.K_p:
                    for row in grid:
                        for node in row:
                            node.update_neighbors(grid)

                    pathfinder(lambda: draw_grid(pygame_window,
                                                 grid, ROWS, grid_width),
                               grid, start_position, end_position, 'pythagorean')

                elif event.key == pygame.K_d:
                    for row in grid:
                        for node in row:
                            node.update_neighbors(grid)

                    pathfinder(lambda: draw_grid(pygame_window,
                                                 grid, ROWS, grid_width),
                               grid, start_position, end_position, 'diagonal')

                elif event.key == pygame.K_c:
                    clear_paths(grid)

                elif event.key == pygame.K_r:
                    grid = create_random_grid(ROWS, grid_width)
                    start_position = grid[randint(0, ROWS - 1)][randint(0, ROWS - 1)]
                    end_position = grid[randint(0, ROWS - 1)][randint(0, ROWS - 1)]
                    start_position.color = THECOLORS['blue']
                    end_position.color = THECOLORS['purple']

    pygame.quit()


if __name__ == '__main__':
    import python_ta

    python_ta.check_all(config={
        'max-line-length': 100,
        'disable': ['E1136', 'R0902', 'R0912', 'R1702', 'R0914'],
        'extra-imports': ['random', 'pygame', 'pygame.colordict', 'algorithm'],
        'generated-members': ['pygame.*']
    })

    import python_ta.contracts

    python_ta.contracts.check_all_contracts()
