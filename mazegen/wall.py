from enum import IntFlag


class Wall(IntFlag):
    """Represent maze walls using bit flags."""
    NORTH = 1
    EAST = 2
    SOUTH = 4
    WEST = 8

    def opposite(self) -> "Wall":
    """Return the opposite wall direction."""
        opposites: dict[Wall, Wall] = {
                Wall.NORTH: Wall.SOUTH,
                Wall.EAST: Wall.WEST,
                Wall.SOUTH: Wall.NORTH,
                Wall.WEST: Wall.EAST,
                }
        return opposites[self]
