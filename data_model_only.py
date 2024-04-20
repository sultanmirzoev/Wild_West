from pydantic import BaseModel


# define what a wall is
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


# everything for one level
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

print(player)
print(walls)
print(coins)
