# Graphics engine code
import numpy as np
import cv2
from game_logic import wild_west, get_objects, move_command, update
from cutscene import cutscene
import pygame

def play_song(songfile: str) -> None:
    pygame.mixer.music.load(songfile)
    pygame.mixer.music.play()

# First cutscene
cutscene(
    text="Welcome to Wild West! Press any button to start",
    wait=5,
    songfile="start_end_game.mp3",
    imagefile="wild_desert.png",
)

# Second cutscene
cutscene(
    text="An infamous gang is roaming the region and     attacking lone travellers",
    wait=5,
    songfile="start_end_game.mp3",
    imagefile="gang.png",
)

# Third cutscene
cutscene(
    text="Try to get to your hometown safe",
    wait=5,
    songfile="start_end_game.mp3",
    imagefile="hometown.png",
)
# Fourth cutscene
cutscene(
    text="Press Space to shoot and WASD to move",
    wait=5,
    songfile="start_end_game.mp3",
    imagefile="desert2.png",
)
# Fifth cutscene
cutscene(
    text="Are you ready to embark on this treacherous    journey?",
    wait=5,
    songfile="start_end_game.mp3",
    imagefile="wild_desert.png",
)
play_song("RODEO RANGER.mp3")

# map keyboard keys to move commands
MOVES = {
    "a": "left",
    "d": "right",
    "w": "up",
    "s": "down",
    "j": "jump",
    " ": "shot",
}

#
# constants measured in pixels
#
SCREEN_SIZE_X, SCREEN_SIZE_Y = 640, 640
TILE_SIZE = 64


def read_image(filename: str) -> np.ndarray:
    """
    Reads an image from the given filename and doubles its size.
    If the image file does not exist, an error is created.
    """
    img = cv2.imread(filename)  # sometimes returns None
    return img


IMAGES = {
    "player": read_image("player1.png"),
    "cactus": read_image("cactus.png"),
    "coin": read_image("money.png"),
    "cave_entrance": read_image("cave.png"),
    "trap": read_image("trap.png"),
    "bullet": read_image("bullet.png"),
    "enemy_bullet": read_image("bullet.png"),
    "rider enemy": read_image("rider_enemy.png"),
    "enemy": read_image("enemy.png"),
}


def draw(obj, player_health, player_coins):
    frame = np.zeros((SCREEN_SIZE_Y, SCREEN_SIZE_X, 3), np.uint8)
    # Set background color
    background_color = (165, 213, 250)  #OpenCV uses the BGR color space by default
    frame[:, :] = background_color
    for x, y, name in obj:
        # calculate screen positions
        xpos, ypos = x * TILE_SIZE, y * TILE_SIZE
        image = IMAGES[name]
        frame[ypos : ypos + TILE_SIZE, xpos : xpos + TILE_SIZE] = image


    # Display player's health in the top right corner
    font = cv2.FONT_HERSHEY_SIMPLEX
    health_text = f"Health: {player_health}"
    text_size = cv2.getTextSize(health_text, font, 1, 2)[0]
    text_x = SCREEN_SIZE_X - text_size[0] - 10
    text_y = 30
    cv2.putText(frame, health_text, (text_x, text_y), font, 1, (0, 0, 0), 2, cv2.LINE_AA)

    # Display player's coins below health
    coins_text = f"Coins: {player_coins}"
    coins_text_size = cv2.getTextSize(coins_text, font, 1, 2)[0]
    coins_text_x = SCREEN_SIZE_X - coins_text_size[0] - 10
    coins_text_y = text_y + text_size[1] + 10  # Add a small margin below the health text
    cv2.putText(frame, coins_text, (coins_text_x, coins_text_y), font, 1, (0, 0, 0), 2, cv2.LINE_AA)

    cv2.imshow("Wild West", frame)


UPDATE_MAX = 25


update_cycle = UPDATE_MAX
exit_game = False

while not exit_game:
    # draw
    obj = get_objects(wild_west)
    player_health = wild_west.player.health  # Get player's health
    player_coins = wild_west.player.coins  # Get player's coins
    draw(obj, player_health, player_coins)  # Pass values to the draw function
    update_cycle -= 1
    if update_cycle <= 0:
        update(wild_west)
        update_cycle = UPDATE_MAX

    # handle keyboard input
    key = chr(cv2.waitKey(1) & 0xFF)
    if key == "q":
        exit_game = True
    if key in MOVES:
        move_command(wild_west, wild_west.player, MOVES[key])
    if wild_west.event == "new level":
        wild_west.event = ""  # delete the event
        cutscene(
            text="Congratulations Cowboy, you just completed the level. Now the real challenge starts.",
            songfile="start_end_game.mp3",
            imagefile="wild_desert.png",
        )
        cutscene(
            text="Welcome To The New Level",
            wait=5,
            songfile="start_end_game.mp3",
            imagefile="wild_desert.png",
        )
        play_song("RODEO RANGER.mp3") #playing the song at the start of the game
    elif wild_west.event == "game over": #game over cutscene
        cutscene(
            text="Congratulations! You arrived to your hometown  safe and sound!",
            wait=5,
            songfile="start_end_game.mp3",
            imagefile="safe_arrival.png",
        )
        exit_game = True
    elif wild_west.event == "you died": #death cutscene
        cutscene(
            text="Game over. Good luck next time, Cowboy.",
            wait=5,
            songfile="start_end_game.mp3",
            imagefile="wild_desert.png",
        )
        exit_game = True

cv2.destroyAllWindows()
