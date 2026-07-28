from enum import IntFlag


class Wall(IntFlag):
    NORTH = 1
    EAST = 2
    SOUTH = 4
    WEST = 8

    def opposite(self) -> "Wall":
        opposites: dict[Wall, Wall] = {
                Wall.NORTH: Wall.SOUTH,
                Wall.EAST: Wall.WEST,
                Wall.SOUTH: Wall.NORTH,
                Wall.WEST: Wall.EAST,
                }
        return opposites[self]
