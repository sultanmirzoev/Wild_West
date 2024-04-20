"""
Proof-of-concept: move around on a 2D grid

Install dependencies:

    pip install numpy opencv-python
"""
import numpy as np
import cv2


# constants measured in pixel
SCREEN_SIZE_X, SCREEN_SIZE_Y = 640, 640
TILE_SIZE = 64


def draw_dungeon(background, player, x, y):
    frame = background.copy()
    xpos, ypos = x * TILE_SIZE, y * TILE_SIZE
    frame[ypos : ypos + TILE_SIZE, xpos : xpos + TILE_SIZE] = player
    cv2.imshow("Dungeon Explorer", frame)


# define a function that doubles image size
size2x = lambda a: np.kron(a, np.ones((2, 2, 1), dtype=a.dtype))

# load image and extract square tiles from it
wall = size2x(cv2.imread("tiles/wall.png"))
player = size2x(cv2.imread("tiles/deep_elf_high_priest.png"))

# define boundaries of the 2D grid
min_x, max_x = 0, SCREEN_SIZE_X // TILE_SIZE
min_y, max_y = 0, SCREEN_SIZE_Y // TILE_SIZE

# NumPy array used as background (BGR color channels)
background = np.zeros((SCREEN_SIZE_Y, SCREEN_SIZE_X, 3), np.uint8)

# starting position of the player
x, y = 4, 4
exit_pressed = False

while not exit_pressed:
    draw_dungeon(background, player, x, y)

    # handle keyboard input
    key = chr(cv2.waitKey(1) & 0xFF)
    if key == "d" and x < 9:
        x += 1
    elif key == "a" and x > 0:
        x -= 1
    elif key == "w" and y > 0:
        y -= 1
    elif key == "s":
        if y < 9:
            y += 1
        else:
            y = 0  # wrap-around move

    elif key == "j":
        x += 2
    elif key == "q":
        exit_pressed = True

cv2.destroyAllWindows()
