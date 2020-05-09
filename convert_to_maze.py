import base64
import io
from PIL import Image
import numpy as np
import sys
import os

def arrow_symbol(block):
    """
    Check the direction of the arrow in the block and return the appropriate symbol
    """
    diff_num_black_pixels = np.apply_along_axis(lambda x: np.bincount(x)[0], 1, block)
    for i in range(len(diff_num_black_pixels) - 1):
        if diff_num_black_pixels[i] < diff_num_black_pixels[i + 1]:
            return 1
        elif diff_num_black_pixels[i] > diff_num_black_pixels[i + 1]:
            return 2

    return np.argmax(np.bincount(block.flatten()))

def to_symbol(block, last_line=False):
    """
    Convert the matrix of pixels into a single symbol
    """
    counts = np.bincount(block.flatten())
    if last_line:
        return arrow_symbol(block)

    main_color = np.argmax(counts[0:-1])
    if main_color:
        return main_color
    else:
        return np.argmax(counts)

def convert_to_maze(data):
    """
    Convert a numpy array representing an image of a maze into a matrix of symbols
    """
    starting_coordinates = (65, 195)
    start_y = 50
    start_x = 195

    win_width = 65
    win_height = 65

    bottom_padding = 45
    right_padding = 55

    # Cropping the image to only contain the maze
    maze = data[start_x:data.shape[0]-bottom_padding, start_y:data.shape[1]-right_padding]

    # Divide the maze's image matrix into smaller matrices and find the symbol for each sub-matrix
    maze_width = maze.shape[1]
    maze_height = maze.shape[0]
    num_blocks_x = int(maze_height / win_height)
    num_blocks_y = int(maze_width / win_width)
    start_x = 0
    start_y = 0
    converted_maze = np.empty((num_blocks_x, num_blocks_y))
    for x in range(num_blocks_x):
        end_x = min(start_x + win_height, maze_height)
        for y in range(num_blocks_y):
            end_y = min(start_y + win_width, maze_width)
            block = maze[start_x:end_x, start_y:end_y]
            if x == num_blocks_x-1:
                symbol = to_symbol(block, last_line=True)
            else:
                symbol = to_symbol(block)
            converted_maze[x, y] = symbol
            if end_y != maze_width:
                start_y = end_y
        if end_x != maze_height:
            start_x = end_x
        start_y = 0

    return converted_maze


if __name__ == "__main__":
    filename = sys.argv[1]
    with open(filename) as encoded_maze_file:
        encoded_maze = encoded_maze_file.read().replace('\n', '')
        decoded_maze = base64.b64decode(encoded_maze)
        image = Image.open(io.BytesIO(decoded_maze)).convert('L')
        data = np.asarray(image)
        maze = convert_to_maze(data)
        print(maze)
        np.save(os.path.splitext(filename)[0] + '_decoded', maze)
