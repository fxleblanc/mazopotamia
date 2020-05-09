import sys
import numpy as np
from convert_to_maze import convert_to_maze
from queue import Queue

COLORS = [74, 80]

def is_last_row_floor(maze_vector, width, position, value):
    """
    The last row of the maze contains either the start, end or maze floor.
    You can't walk in these so you must make sure that these floors are invalid
    """
    return position > len(maze_vector) - width - 1 and value == 255

def is_next_color(color, last_color):
    """
    Gates use a system of colors to determine if you can go through or not
    e.g. If you pass a red gate, you can't go through a red gate again but you can go through the next
    gate in the COLOR order, in this case blue. The order is determined by the COLORS array.
    n.b. When you get at the end of the COLORS array, the next gate you can go through is the first in
    the array, thus gates use a circular system.
    """
    if not last_color:
        return True

    color_index = COLORS.index(color)
    last_color_index = COLORS.index(last_color)
    if color_index > last_color_index:
        return True

    if last_color_index == len(COLORS) - 1 and color_index == 0:
        return True

    return False

def is_oob(maze_vector, position):
    """
    Check if the position is out of bounds of the maze
    """
    return position < 0 or position > len(maze_vector)

def get_last_value(maze_vector, solution, width, start):
    """
    Transform a string solution into the last value of that solution.
    Go through the maze and returning either the value or -1 to signify that it's an invalid path
    """
    manipulations = {"S": width, "W": -1, "N": -width, "E": 1}

    position = start
    last_color = None
    value = -1
    already_visited = []
    for direction in solution:
        position = position + manipulations[direction]

        if position in already_visited:
            return -1

        if is_oob(maze_vector, position):
            return -1

        value = maze_vector[position]
        if value == 0 or is_last_row_floor(maze_vector, width, position, value):
            return -1

        if value in COLORS and is_next_color(value, last_color):
            last_color = value
            position = position + manipulations[direction]
        elif value in COLORS and not is_next_color(value, last_color):
            return -1

        if value == 2:
            return value

        already_visited.append(position)

    return value

def solve(maze):
    _, width = maze.shape
    maze_vector = maze.flatten()
    start = np.where(maze_vector == 1)[0][0]
    solution = ""
    solutions = Queue()
    solutions.put("N")

    directions = ["S", "W", "N", "E"]
    while get_last_value(maze_vector, solution, width, start) != 2 and solutions.qsize() != 0:
        solution = solutions.get()
        for direction in directions:
            possible_solution = solution + direction
            if get_last_value(maze_vector, possible_solution, width, start) != -1:
                solutions.put(possible_solution)

    return solution

if __name__ == "__main__":
    filename = sys.argv[1]
    maze = np.load(filename)
    print(maze)


    solution = solve(maze)
    print(solution)
