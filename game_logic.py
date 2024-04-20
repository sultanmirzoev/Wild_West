"""
Wild West game logic
"""

from pydantic import BaseModel
from levels import LEVELS
import random

#
# define data model
#
class Position(BaseModel):
    x: int
    y: int


class Player(BaseModel):
    position: Position
    health: int = 10
    coins: int = 0
    last_direction: str = "up"

class Bullet(BaseModel):
    position: Position
    direction: str

class EnemyBullet(BaseModel): #separate class for enemy bullets
    position: Position
    direction: str

class Enemy (BaseModel):
    health: int = 5
    position: Position
    direction: str = "up"
    shoot_counter: int = 0
    last_direction: str = "up"  # Track the last direction moved

class WildWest(BaseModel):
    player: Player
    walls: list[Position] = []
    coins: list[Position] = []
    cave_entrances: list[Position] = []
    traps: list[Position] = []
    bullets: list[Bullet] = []
    enemy_bullets: list[EnemyBullet] = []
    rider_enemies: list[Position] = []
    enemies: list[Enemy] = []

    event: str = ""
    level_number: int = 0




def get_next_position(position: Position, direction: str, occupied: list[Position]) -> Position:
    new = Position(x=position.x, y=position.y)
    if direction == "right" and new.x < 9:
        new.x += 1
    elif direction == "left" and new.x > 0:
        new.x -= 1
    elif direction == "up" and new.y > 0:
        new.y -= 1
    elif direction == "down":
        if new.y < 9:
            new.y += 1
    if new in occupied:
        return position
    else:
        return new


def move_command(wildwest, player, action: str) -> None:
    """handles player actions like 'left', 'right', 'jump', 'bullet'"""
    # remember old position
    old_position = player.position.model_copy()
    pos = player.position

    if action in ["up", "down", "left", "right"]:
        new = get_next_position(player.position, action, wildwest.walls)
        player.last_direction = action
        player.position = new

    elif action == "jump":
        pos.x += 2
    elif action == "shot":
        bullet = Bullet(position=pos.copy(), direction=player.last_direction)
        wildwest.bullets.append(bullet)
    # check for walls
    for wall in wildwest.walls:
        if player.position == wall:
            player.position = old_position

    # collect coin if there is any
    for coin in wildwest.coins:
        if player.position == coin:
            # we found a coin
            wildwest.coins.remove(coin)  # remove the coin we found from the level
            player.coins += 10
            print("you now have", player.coins, "coins")
            break  # stop the loop because we modified coins

    # check for cave entrances
    for cave_entrance in wildwest.cave_entrances:
        if player.position == cave_entrance:
            wildwest.level_number += 1
            if wildwest.level_number == len(LEVELS):
                wildwest.event = "game over"
            else:
                wildwest.event = "new level"
                start_level(wildwest=wildwest,
                            level=LEVELS[wildwest.level_number],
                            start_position=Position(x=4, y=8)
                            )
    # check for traps
    for trap in wildwest.traps:
        if player.position == trap:
            wildwest.event = "you died"
    # check for rider enemies
    for rider_enemy in wildwest.rider_enemies:
        if player.position == rider_enemy:
            wildwest.event = "you died"


def get_objects(wildwest) -> list[list[int, int, str]]:
    """
    returns everything inside the dungeon
    as a list of (x, y, object_type) items.
    """
    result = []
    result.append([wildwest.player.position.x, wildwest.player.position.y, "player"])
    for w in wildwest.walls:
        result.append([w.x, w.y, "cactus"])
    for c in wildwest.coins:
        result.append([c.x, c.y, "coin"])
    for r in wildwest.cave_entrances:
        result.append([r.x, r.y, "cave_entrance"])
    for t in wildwest.traps:
        result.append([t.x, t.y, "trap"])
    for r in wildwest.rider_enemies:
        result.append([r.x, r.y, "rider enemy"])
    for f in wildwest.bullets:
        result.append([f.position.x, f.position.y, "bullet"])
    for eb in wildwest.enemy_bullets:
        result.append([eb.position.x, eb.position.y, "enemy_bullet"])
    for e in wildwest.enemies:
        result.append([e.position.x, e.position.y, "enemy"])
    return result


def update(wildwest):
    for r in wildwest.rider_enemies:
        direction = random.choice(["up", "down", "left", "right", "wait", "wait", "wait", "wait"])
        if direction != "wait":
            new = get_next_position(r, direction, occupied = wildwest.walls + wildwest.rider_enemies +
            wildwest.enemies + wildwest.cave_entrances + wildwest.coins)
            r.x = new.x
            r.y = new.y

    for e in wildwest.enemies:
        direction = random.choice(["up", "down", "left", "right"])
        new = get_next_position(e.position, direction, occupied = wildwest.walls + wildwest.rider_enemies +
        wildwest.enemies + wildwest.cave_entrances + wildwest.coins)
        if new != e.position:
            e.last_direction = direction  # Update last_direction on actual movement
            e.position = new

    # Move and check collisions for player's bullets
    new_bullets = []
    for bullet in wildwest.bullets:
        new = get_next_position(bullet.position, bullet.direction,
        occupied=wildwest.walls + wildwest.cave_entrances)
        if new != bullet.position:
            bullet.position = new
            new_bullets.append(bullet)
        for enemy in wildwest.enemies:
            if bullet.position == enemy.position:
                enemy.health -= 1
                if enemy.health <= 0:
                    wildwest.enemies.remove(enemy)
    wildwest.bullets = new_bullets

    # Move and check collisions for enemy bullets
    new_enemy_bullets = []
    for bullet in wildwest.enemy_bullets:
        new = get_next_position(bullet.position, bullet.direction,
        occupied=wildwest.walls + wildwest.cave_entrances)
        if new != bullet.position:
            bullet.position = new
            new_enemy_bullets.append(bullet)
        if bullet.position == wildwest.player.position:
            wildwest.player.health -= 1  # Player hit by enemy bullet
    wildwest.enemy_bullets = new_enemy_bullets

    # Enemy shooting behavior
    for enemy in wildwest.enemies:
        enemy.shoot_counter += 1
        if enemy.shoot_counter >= 3:
            bullet = EnemyBullet(position=enemy.position.copy(),
                                 direction=enemy.last_direction)  # Use last_direction for shooting
            wildwest.enemy_bullets.append(bullet)
            enemy.shoot_counter = 0

# define the level we will play
wild_west = WildWest(
    player=Player(position=Position(x=8, y=4)),
)

def start_level(
        wildwest: WildWest, level: list[str], start_position: Position, **kwargs
) -> None:
    wildwest.player.position = start_position
    wildwest.traps = []
    wildwest.walls = []
    wildwest.coins = []
    wildwest.cave_entrances = []
    wildwest.bullets = []
    wildwest.enemy_bullets = []
    wildwest.rider_enemies = []
    wildwest.enemies = []
    for y, row in enumerate(level):  # y is a row number 0, 1, 2, ...
        for x, tile in enumerate(row):  # x is a column number 0, 1, 2, ...
            if tile == "T":
                traps = Position(x=x, y=y)
                wildwest.traps.append(traps)
            if tile == "#":
                wall = Position(x=x, y=y)
                wildwest.walls.append(wall)
            if tile == "X":
                cave_entrance = Position(x=x, y=y)
                wildwest.cave_entrances.append(cave_entrance)
            if tile == "$":
                coin = Position(x=x, y=y)
                wildwest.coins.append(coin)
            if tile == "R":
                rider_enemy = Position(x=x, y=y)
                wildwest.rider_enemies.append(rider_enemy)
            if tile == "E":
                enemy = Enemy(position = Position(x=x, y=y))
                wildwest.enemies.append(enemy)

start_level(wild_west, LEVELS[0], Position(x = 4, y = 8))
