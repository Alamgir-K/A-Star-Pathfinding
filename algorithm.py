"""
This file is a part of the CSC111 final project by Alamgir Khan, Aman Rana,
Rahul Jaideep and Dhruvaa Saravanan.

This module contains the classes and functions necessary for the algorithmic and calculation part of
the visualisation tool. We implement the A* Pathfinding algorithm using a variety of heuristics
based on what the user wishes in the actual visualisation.
"""
from __future__ import annotations
from typing import Callable, Dict, List, Set, Tuple, Union
import pygame
from pygame.colordict import THECOLORS


class Vertex:
    """A vertex in the grid visualization, used to represent a node

    Instance Attributes:
        - row: The row position of the node
        - column: The column position of the node
        - x: x-coordinate of the vertex
        - y: y-coordinate of the vertex
        - color: The color of the node
        - width: The width of the node.
        - row_total: The total number of rows
        - neighbors: A list of vertices that are adjacent to this vertex
    """
    row: int
    column: int
    x: int
    y: int
    color: tuple
    width: int
    row_total: int
    neighbors: List[Vertex]

    def __init__(self, row: int, column: int, width: int, row_total: int) -> None:
        """Initialize a new vertex with the given row, column, width and row_total
        """
        self.row = row
        self.column = column
        self.x = row * width
        self.y = column * width
        self.color = THECOLORS['white']
        self.width = width
        self.row_total = row_total
        self.neighbors = []

    def get_position(self) -> Tuple[int, int]:
        """Return the row and column positions of the vertex
        """
        return self.row, self.column

    def draw_node(self, pygame_window: pygame.Surface) -> None:
        """Draw the vertex (node) on the pygame_window
        """
        pygame.draw.rect(pygame_window, self.color, (self.x, self.y, self.width, self.width))

    def check_up(self, grid: List[List[Vertex]]) -> bool:
        """
        Check if there are nodes available above
        """
        if self.row <= 0:
            return False
        elif grid[self.row - 1][self.column].color == THECOLORS['black']:
            return False

        return True

    def check_down(self, grid: List[List[Vertex]]) -> bool:
        """
        Check if there are nodes available below
        """
        if self.row >= self.row_total - 1:
            return False
        elif grid[self.row + 1][self.column].color == THECOLORS['black']:
            return False

        return True

    def check_left(self, grid: List[List[Vertex]]) -> bool:
        """
        Check if there are nodes available to the left
        """
        if self.column <= 0:
            return False
        elif grid[self.row][self.column - 1].color == THECOLORS['black']:
            return False

        return True

    def check_right(self, grid: List[List[Vertex]]) -> bool:
        """
        Check if there are nodes available to the right
        """
        if self.column >= self.row_total - 1:
            return False
        elif grid[self.row][self.column + 1].color == THECOLORS['black']:
            return False

        return True

    def check_left_up(self, grid: List[List[Vertex]]) -> bool:
        """
        Check if there are nodes available diagonally to the left and above
        """
        if self.row <= 0 or self.column <= 0:
            return False
        elif grid[self.row - 1][self.column - 1].color == THECOLORS['black']:
            return False

        return True

    def check_left_down(self, grid: List[List[Vertex]]) -> bool:
        """
        Check if there are nodes available diagonally to the left and below
        """
        if self.row >= (self.row_total - 1) or self.column <= 0:
            return False
        elif grid[self.row + 1][self.column - 1].color == THECOLORS['black']:
            return False

        return True

    def check_right_up(self, grid: List[List[Vertex]]) -> bool:
        """
        Check if there are nodes available diagonally to the right and above
        """
        if self.row <= 0 or self.column >= (self.row_total - 1):
            return False
        elif grid[self.row - 1][self.column + 1].color == THECOLORS['black']:
            return False

        return True

    def check_right_down(self, grid: List[List[Vertex]]) -> bool:
        """
        Check if there are nodes available diagonally to the right and below
        """
        if self.row >= (self.row_total - 1) or self.column >= (self.row_total - 1):
            return False
        elif grid[self.row + 1][self.column + 1].color == THECOLORS['black']:
            return False

        return True

    def update_neighbors(self, grid: List[List[Vertex]]) -> None:
        """Update the neighbors of the vertex by checking node availability
        """
        # Up
        if self.check_up(grid):
            self.neighbors.append(grid[self.row - 1][self.column])

        # Down
        if self.check_down(grid):
            self.neighbors.append(grid[self.row + 1][self.column])

        # Left
        if self.check_left(grid):
            self.neighbors.append(grid[self.row][self.column - 1])

        # Right
        if self.check_right(grid):
            self.neighbors.append(grid[self.row][self.column + 1])

        # Left-Up
        if self.check_left_up(grid):
            self.neighbors.append(grid[self.row - 1][self.column - 1])

        # Left-Down
        if self.check_left_down(grid):
            self.neighbors.append(grid[self.row + 1][self.column - 1])

        # Right-Up
        if self.check_right_up(grid):
            self.neighbors.append(grid[self.row - 1][self.column + 1])

        # Right-Down
        if self.check_right_down(grid):
            self.neighbors.append(grid[self.row + 1][self.column + 1])


def manhattan_heuristic(start_point: Tuple[int, int], end_point: Tuple[int, int]) -> float:
    """Return the distance between start_point and end_point using Manhattan distance
     (sum of the absolute differences between the two vectors)
    """
    x1, y1 = start_point
    x2, y2 = end_point
    distance = abs(x1 - x2) + abs(y1 - y2)
    return distance


def pythagorean_heuristic(start_point: Tuple[int, int], end_point: Tuple[int, int]) -> float:
    """Return the distance between start_point and end_point using the pythagorean distance
    """
    x1, y1 = start_point
    x2, y2 = end_point
    distance = (((x2 - x1) ** 2) + ((y2 - y1) ** 2)) ** 0.5
    return distance


def diagonal_distance_heuristic(start_point: Tuple[int, int], end_point: Tuple[int, int]) -> float:
    """Return the distance between start_point and end_point using the diagonal distance
    """
    d1 = 1
    d2 = 2 ** 0.5
    x1, y1 = start_point
    x2, y2 = end_point
    dx = abs(x2 - x1)
    dy = abs(y2 - y1)
    distance = d1 * (dx + dy) + (d2 - 2 * d1) * min(dx, dy)
    return distance


def make_path(origin: Dict[Vertex], current_node: Vertex) -> None:
    """Construct the path using the current_node by using the draw function until the start node is
     reached. current_node will initially be the start node but will become the end node at the end
     of the path construction.
    """
    current_node.color = THECOLORS['purple']

    while current_node in origin:
        current_node = origin[current_node]
        current_node.color = THECOLORS['green']

    current_node.color = THECOLORS['blue']


def find_lowest_cost_node(queue: Set[Tuple[Union[float, int],
                                           int, Vertex]]) -> Tuple[Union[float, int], int, Vertex]:
    """Return the item with the lowest traversal cost in queue
    """
    lowest_count_so_far = 1000000
    lowest_cost_item = None
    lowest_cost_so_far = 1000000.0

    for item in queue:
        if item[0] < lowest_cost_so_far:
            lowest_cost_so_far = item[0]
            lowest_count_so_far = item[1]
            lowest_cost_item = item
        elif item[0] == lowest_cost_so_far and item[1] < lowest_count_so_far:
            lowest_cost_so_far = item[0]
            lowest_count_so_far = item[1]
            lowest_cost_item = item

    return lowest_cost_item


def nodes_in_queue(queue: Set[Tuple[Union[float, int],
                                    int, Vertex]]) -> Set[Vertex]:
    """Return a set of all the nodes in queue
    """
    nodes = set()

    for item in queue:
        nodes.add(item[2])

    return nodes


def pathfinder(draw: Callable, grid: List[List[Vertex]], start_node: Vertex, end_node: Vertex,
               heuristic: str) -> bool:
    """Run the pathfinding algorithm and return whether or not the fastest route was found"""
    count = 0
    search_set_queue = set()
    origin = {}
    traversal_cost = {node: 1000000.0 for row in grid for node in row}
    traversal_cost[start_node] = 0
    total_cost = {node: 1000000.0 for row in grid for node in row}
    start_node_position = start_node.get_position()
    end_node_position = end_node.get_position()
    if heuristic == 'manhattan':
        total_cost[start_node] = manhattan_heuristic(start_node_position, end_node_position)
    elif heuristic == 'pythagorean':
        total_cost[start_node] = pythagorean_heuristic(start_node_position, end_node_position)
    elif heuristic == 'diagonal':
        total_cost[start_node] = diagonal_distance_heuristic(start_node_position, end_node_position)
    search_set_queue.add((total_cost[start_node], count, start_node))

    while len(search_set_queue) != 0:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        current_item = find_lowest_cost_node(search_set_queue)
        current_node = current_item[2]
        search_set_queue.discard(current_item)

        if current_node == end_node:
            make_path(origin, end_node)
            return True

        for neighbor in current_node.neighbors:
            temporary_traversal_cost = traversal_cost[current_node] + 1

            if temporary_traversal_cost < traversal_cost[neighbor]:
                origin[neighbor] = current_node
                traversal_cost[neighbor] = temporary_traversal_cost
                neighbor_position = neighbor.get_position()
                if heuristic == 'manhattan':
                    total_cost[neighbor] = temporary_traversal_cost + manhattan_heuristic(
                        neighbor_position, end_node_position)
                elif heuristic == 'pythagorean':
                    total_cost[neighbor] = temporary_traversal_cost + pythagorean_heuristic(
                        neighbor_position, end_node_position)
                elif heuristic == 'diagonal':
                    total_cost[neighbor] = temporary_traversal_cost + diagonal_distance_heuristic(
                        neighbor_position, end_node_position)

                if neighbor not in nodes_in_queue(search_set_queue):
                    count += 1
                    neighbor_total_traversal_cost = total_cost[neighbor]
                    search_set_queue.add((neighbor_total_traversal_cost, count, neighbor))
                    neighbor.color = THECOLORS['yellow']

        draw()

        if current_node != start_node:
            current_node.color = THECOLORS['red']

    return False


if __name__ == '__main__':
    import python_ta

    python_ta.check_all(config={
        'max-line-length': 100,
        'disable': ['E1136', 'R0902', 'R0912', 'R1702', 'R0914'],
        'extra-imports': ['random', 'pygame', 'pygame.colordict'],
        'generated-members': ['pygame.*']
    })

    import python_ta.contracts

    python_ta.contracts.check_all_contracts()
