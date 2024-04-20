import numpy as np
import cv2
from pydantic import BaseModel


#
# define data model
#
class Wall(BaseModel):
    x: int
    y: int


class Coin(BaseModel):
    x: int
    y: int
    value: int = 10


class Player(BaseModel):
    x: int
    y: int
    health: int = 100
    coins: int = 0


#
# create a level
#
player = Player(x=4, y=4)
walls = [
    Wall(x=0, y=0),
    Wall(x=1, y=0),
    Wall(x=2, y=0),
    Wall(x=3, y=0),
    Wall(x=4, y=6),
]
coins = [
    Coin(x=0, y=1, value=100),
    Coin(x=2, y=5),
]

#
# constants measured in pixel
#
SCREEN_SIZE_X, SCREEN_SIZE_Y = 640, 640
TILE_SIZE = 64


def draw_dungeon(player, walls, coins, player_img, wall_img, coin_img):
    frame = np.zeros((SCREEN_SIZE_Y, SCREEN_SIZE_X, 3), np.uint8)

    # draw player
    xpos, ypos = player.x * TILE_SIZE, player.y * TILE_SIZE
    frame[ypos : ypos + TILE_SIZE, xpos : xpos + TILE_SIZE] = player_img

    # draw walls
    for wall in walls:
        xpos, ypos = wall.x * TILE_SIZE, wall.y * TILE_SIZE
        frame[ypos : ypos + TILE_SIZE, xpos : xpos + TILE_SIZE] = wall_img

    # draw coins
    for coin in coins:
        xpos, ypos = coin.x * TILE_SIZE, coin.y * TILE_SIZE
        frame[ypos : ypos + TILE_SIZE, xpos : xpos + TILE_SIZE] = coin_img

    cv2.imshow("Dungeon Explorer", frame)


# define a function that doubles image size
size2x = lambda a: np.kron(a, np.ones((2, 2, 1), dtype=a.dtype))

# load image and extract square tiles from it
cactus_img = cv2.imread("cactus.png")
coin_img = cv2.imread("money.png")
player_img = cv2.imread("player1.png")


# define boundaries of the 2D grid
min_x, max_x = 0, SCREEN_SIZE_X // TILE_SIZE
min_y, max_y = 0, SCREEN_SIZE_Y // TILE_SIZE


exit_pressed = False
while not exit_pressed:
    draw_dungeon(player, walls, coins, player_img, cactus_img, coin_img)

    # remember old position
    old_x, old_y = player.x, player.y

    # handle keyboard input
    key = chr(cv2.waitKey(1) & 0xFF)
    if key == "d" and player.x < 9:
        player.x += 1
    elif key == "a" and player.x > 0:
        player.x -= 1
    elif key == "w" and player.y > 0:
        player.y -= 1
    elif key == "s":
        if player.y < 9:
            player.y += 1
        else:
            player.y = 0  # wrap-around move

    elif key == "j":
        player.x += 2
    elif key == "q":
        exit_pressed = True

    # check for walls
    for wall in walls:
        if player.x == wall.x and player.y == wall.y:
            player.x, player.y = old_x, old_y

    # collect coin if there is any
    for coin in coins:
        if player.x == coin.x and player.y == coin.y:
            # we found a coin
            coins.remove(coin)  # remove the coin we found from the level
            player.coins += coin.value
            print("you now have", player.coins, "coins")
            break  # stop the loop because we modified coins

cv2.destroyAllWindows()
