from enum import Enum
from collections import deque


class Color(Enum):
    WHITE = 1
    RED = 2
    BLUE = 3
    ORANGE = 4
    YELLOW = 5
    GREEN = 6


class Corner:
    def __init__(self, corner):
        self._corner = deque(corner)

    def is_mirrored(self, corner):
        return corner == self.mirrored()

    def is_rotated(self, corner):
        # Returns True if corner is a rotation of self
        # Note: Equality does count as a rotation.
        _c = corner.copy()
        for i in range(len(self._corner)):
            _c._rotate(1)
            if _c == self:
                return True
        return False

    def is_mirrored_rotation(self, corner):
        temp = self.copy()
        temp._mirror()
        return temp.is_rotated(corner)

    def _mirror(self):
        self._corner.reverse()

    def _rotate(self, rotations=1):
        self._corner.rotate(rotations)

    def mirrored(self):
        c = self.copy()
        c._mirror()
        return c

    def rotated(self, rotations=1):
        r = self.copy()
        r._rotate(rotations)
        return r

    def get_rotation_step(self, other):
        """
        Gets the amount of steps a corner is from another corner.
        Other is the point of reference which self compares itself to.
        """

        # TODO: Should the point of reference be self instead?

        if not self.is_rotated(other):
            raise ValueError("Corners must be valid rotations of each other.")
        else:
            r = 0
            if self == other:
                pass
            elif self == other.rotated(1):
                r = 1
            elif self == other.rotated(2):
                r = -1
            else:
                raise ValueError("Something went really wrong here!")
            return r

    def copy(self):
        return Corner(list(self._corner))

    def __eq__(self, other):
        return self._corner == other._corner

    def __str__(self):
        return str(list(self._corner))


class Edge:
    def __init__(self, edge):
        self._edge = list(edge)

    def rotate(self):
        self._edge = list(reversed(self._edge))

    def rotated(self):
        return Edge(list(reversed(self._edge)))

    def __str__(self):
        return str(self._edge)

    def __eq__(self, other):
        return self._edge == other._edge


class Cube:
    def __init__(self):
        """
        ...
        """
        """
        Facet definitions on unwrapped cube:
        X  X  X   X  X  X   1  2  3   X  X  X
        X  X  X   X  X  X   4  U  5   X  X  X
        X  X  X   X  X  X   6  7  8   X  X  X

       41 42 43   9 10 11  17 18 19  25 26 27
       44 B  45  12 L  13  20 F  21  28 R  29
       46 47 48  14 15 16  22 23 24  30 31 32

        X  X  X   X  X  X  33 34 35   X  X  X
        X  X  X   X  X  X  36 D  37   X  X  X
        X  X  X   X  X  X  38 39 40   X  X  X
        """
        self.cube_dict = {
            "edges": {
                # Up
                "UB": Edge([2, 42]),
                "UL": Edge([4, 10]),
                "UR": Edge([5, 26]),
                "UF": Edge([7, 18]),
                # Front
                "FL": Edge([20, 13]),
                "FR": Edge([21, 28]),
                # Back
                "BL": Edge([45, 12]),
                "BR": Edge([44, 29]),
                # Down
                "DB": Edge([39, 47]),
                "DL": Edge([36, 15]),
                "DR": Edge([37, 31]),
                "DF": Edge([34, 23])
            },
            "corners": {
                # Up
                "UBL": Corner([1, 9, 43]),
                "UBR": Corner([3, 41, 27]),
                "UFL": Corner([6, 17, 11]),
                "UFR": Corner([8, 25, 19]),
                # Down
                "DBL": Corner([38, 48, 14]),
                "DBR": Corner([40, 32, 46]),
                "DFL": Corner([33, 16, 22]),
                "DFR": Corner([35, 24, 30])
            }
        }

    def move(self, movement: str):
        c = CubeMovement(self, movement)
        c.move()

    def swap(self, piece1, piece2):
        corners = self.cube_dict["corners"]
        edges = self.cube_dict["edges"]
        if piece1 in corners.keys() and piece2 in corners.keys():
            temp = corners[piece1]
            corners[piece1] = corners[piece2]
            corners[piece2] = temp
        elif piece1 in edges.keys() and piece2 in edges.keys():
            temp = edges[piece1]
            edges[piece1] = edges[piece2]
            edges[piece2] = temp
        else:
            raise ValueError("Pieces must be either edges or corners.")

class CubeMovement:

    class Move(Enum):
        UP, LEFT, FRONT, RIGHT, DOWN, BACK = range(6)

    def __init__(self, cube: Cube, movement: str):
        self.cube = cube
        self.inverted = False
        if movement[-1] == "'":  # Move inverted
           self.movement = movement[:-1]  # Removes ' symbol
           self.inverted = True
        if movement.lower() in ["u", "up"]:
            self.movement = CubeMovement.Move.UP
        elif movement.lower() in ["d", "down"]:
            self.movement = CubeMovement.Move.DOWN
        elif movement.lower() in ["l", "left"]:
            self.movement = CubeMovement.Move.LEFT
        elif movement.lower() in ["r", "right"]:
            self.movement = CubeMovement.Move.RIGHT
        elif movement.lower() in ["f", "front"]:
            self.movement = CubeMovement.Move.FRONT
        elif movement.lower() in ["b", "back"]:
            self.movement = CubeMovement.Move.BACK

    def move(self):
        if self.movement == CubeMovement.Move.UP:
            self.move_up()
        elif self.movement == CubeMovement.Move.DOWN:
            self.move_down()
        elif self.movement == CubeMovement.Move.LEFT:
            self.move_left()
        elif self.movement == CubeMovement.Move.RIGHT:
            self.move_right()
        elif self.movement == CubeMovement.Move.FRONT:
            self.move_front()
        elif self.movement == CubeMovement.Move.BACK:
            self.move_back()

    def move_up(self):
        if self.inverted:
            pass
        else:

            pass

def get_color(subfacet: int) -> Color:
    # Each face has 8 subfacets (excluding centers)
    # Floor dividing a subfacet (subtracted by 1) by 8 and adding 1 gives the face it belongs to
    # For example, the color of subfacet 36 can be found like this:
    # (36 - 1) // 8 + 1 == 5, so the color of 36 is the color of the 5th face (default yellow)
    subfacet -= 1  # Corrects off-by-one error (facets not zero indexed)
    return Color(subfacet // 8 + 1)
