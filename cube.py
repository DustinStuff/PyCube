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
        X  X  X   X  X  X   0  1  2   X  X  X
        X  X  X   X  X  X   3  U  4   X  X  X
        X  X  X   X  X  X   5  6  7   X  X  X

       40 41 42   8 9  10  16 17 18  24 25 26
       43 B  44  11 L  12  19 F  20  27 R  28
       45 46 47  13 14 15  21 22 23  29 30 31

        X  X  X   X  X  X  32 33 34   X  X  X
        X  X  X   X  X  X  35 D  36   X  X  X
        X  X  X   X  X  X  37 38 39   X  X  X
        """
        # self.cube_dict = {
        #     "edges": {
        #         # Up
        #         "UB": Edge([2, 42]),
        #         "UL": Edge([4, 10]),
        #         "UR": Edge([5, 26]),
        #         "UF": Edge([7, 18]),
        #         # Front
        #         "FL": Edge([20, 13]),
        #         "FR": Edge([21, 28]),
        #         # Back
        #         "BL": Edge([45, 12]),
        #         "BR": Edge([44, 29]),
        #         # Down
        #         "DB": Edge([39, 47]),
        #         "DL": Edge([36, 15]),
        #         "DR": Edge([37, 31]),
        #         "DF": Edge([34, 23])
        #     },
        #     "corners": {
        #         # Up
        #         "UBL": Corner([1, 9, 43]),
        #         "UBR": Corner([3, 41, 27]),
        #         "UFL": Corner([6, 17, 11]),
        #         "UFR": Corner([8, 25, 19]),
        #         # Down
        #         "DBL": Corner([38, 48, 14]),
        #         "DBR": Corner([40, 32, 46]),
        #         "DFL": Corner([33, 16, 22]),
        #         "DFR": Corner([35, 24, 30])
        #     }
        # }

        self.facet_list = list(range(48))  # Each item represents a facet
        # Locations can be referred to by a normal range(48)

    def swap(self, location1: int, location2: int, *args) -> None:
        # Swaps two pieces. If more than 2 pieces, shifts the pieces right (e.g., swap(A, B, C), A to B, B to C, C to A)
        cycle = [location1, location2]
        cycle = cycle + list(args)
        # Error checking:
        for i in cycle:
            # TODO: Are these numbers too magic?
            try:
                if not 0 <= i <= 47 or type(i) != int:
                    raise TypeError("Error in term {}: Expected int, received {}".format(i, type(i)))
            except TypeError:
                raise TypeError("Error in term {}: Expected int, received {}".format(i, type(i)))
        if len(cycle) != len(set(cycle)):  # Duplicate checking
            raise ValueError("Swaps cannot have duplicate items")

        temp = -1
        pos1 = cycle[0]  # just swaps with first element
        for i in range(len(cycle) - 1):  # Only need n-1 loops since we'll be adding 1 to i
            pos2 = cycle[i+1]
            temp_value = self.facet_list[pos2]
            self.facet_list[pos2] = self.facet_list[pos1]
            self.facet_list[pos1] = temp_value


    # def swap(self, piece1, piece2):
    #     corners = self.cube_dict["corners"]
    #     edges = self.cube_dict["edges"]
    #     if piece1 in corners.keys() and piece2 in corners.keys():
    #         temp = corners[piece1]
    #         corners[piece1] = corners[piece2]
    #         corners[piece2] = temp
    #     elif piece1 in edges.keys() and piece2 in edges.keys():
    #         temp = edges[piece1]
    #         edges[piece1] = edges[piece2]
    #         edges[piece2] = temp
    #     else:
    #         raise ValueError("Pieces must be either edges or corners.")


class CubeMovement:
    def __init__(self, movement: str):
        self.inverted = False
        self.double = False
        self.move = ""

        if len(movement) > 2:
            raise ValueError("Invalid movement, only one move supported")

        move = list(movement)[0]
        if move not in list("UDFBLRXYZ"):
            raise ValueError("Error resolving movement")

        if len(movement) == 2:
            mod = list(movement)[-1]
            if mod == "'":
                self.inverted = True
            elif mod == "2":
                self.double = True
            else:
                raise ValueError("Invalid second character, "'" and "2" supported')

        self.move = movement


def get_color(subfacet: int) -> Color:
    # Each face has 8 subfacets (excluding centers)
    # Floor dividing a subfacet by 8 and adding 1 gives the face it belongs to
    # For example, the color of subfacet 36 can be found like this:
    # 36 // 8 + 1 == 5, so the color of 36 is the color of the 5th face (default yellow)
    return Color(subfacet // 8 + 1)
