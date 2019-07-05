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

    def __getitem__(self, item):
        if 0 <= item <= 2:
            return self._corner[item]
        raise IndexError  # For for-loop terminating

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

    def __repr__(self):
        return "<Corner {}, {}, {}>".format(self._corner[0], self._corner[1], self._corner[2])

    def __str__(self):
        return str(list(self._corner))


class Edge:
    def __init__(self, edge):
        self._edge = list(edge)

    def __getitem__(self, item):
        if 0 <= item <= 1:
            return self._edge[item]
        raise IndexError  # For for-loop terminating

    def rotate(self):
        self._edge = list(reversed(self._edge))

    def rotated(self):
        return Edge(list(reversed(self._edge)))

    def __repr__(self):
        return "<Edge {}, {}>".format(*self._edge)

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

    def __eq__(self, other):
        return self.facet_list == other.facet_list

    def swap(self, location1: int, location2: int, *args) -> None:
        # Swaps two facets. If more than 2 facets, shifts them right (e.g., swap(A, B, C), A to B, B to C, C to A)
        cycle = [location1, location2]
        cycle = cycle + list(args)
        # Error checking:
        for i in cycle:
            try:
                # TODO: Are these numbers too magic?
                if not 0 <= i <= 47 or type(i) != int:
                    raise TypeError
            except TypeError:
                raise TypeError("Error in term {}: Expected int, received {}".format(i, type(i)))
        if len(cycle) != len(set(cycle)):  # Duplicate checking
            raise ValueError("Swaps cannot have duplicate items")

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

    def move(self, movement, reverse=False):
        movement_ = 0
        if type(movement) == str:
            movement_ = CubeMovement(movement)
        elif type(movement) == CubeMovement:
            movement_ = movement
        else:
            raise TypeError("Invalid type {}, expected 'str' or 'CubeMovement'".format(type(movement)))

        m = movement_.move[0]
        inverted = movement_.inverted
        double = movement_.double

        swap_list = dict()
        swap_list["U"] = [[1, 4, 6, 3],  # U edges
                          [0, 2, 7, 5],  # U corners
                          [17, 9, 41, 25],   # U side edges
                          [16, 8, 40, 24],   # U side corners #1
                          [18, 10, 42, 26]]  # U side corners #2
        swap_list["D"] = [[33, 36, 38, 35],  # D edges
                          [32, 34, 39, 37],  # D corners
                          [22, 30, 46, 14],  # D side edges
                          [13, 21, 29, 45],  # D side corners #1
                          [47, 15, 23, 31]]  # D side corners #2
        swap_list["L"] = [[9, 12, 14, 11],  # etc
                          [8, 10, 15, 13],
                          [3, 19, 35, 44],
                          [0, 16, 32, 47],
                          [5, 21, 37, 42]]
        swap_list["R"] = [[25, 28, 30, 27],  # etc
                          [24, 26, 31, 29],
                          [4, 43, 36, 20],
                          [7, 40, 39, 23],
                          [2, 45, 34, 18]]
        swap_list["F"] = [[17, 20, 22, 19],  # etc
                          [16, 18, 23, 21],
                          [6, 27, 33, 12],
                          [5, 24, 34, 15],
                          [7, 29, 32, 10]]
        swap_list["B"] = [[41, 44, 46, 43],  # etc
                          [40, 42, 47, 45],
                          [1, 11, 38, 28],
                          [2, 8, 37, 31],
                          [0, 13, 39, 26]]

        swap_face = swap_list[m]
        inverted = inverted ^ reverse  # If reverse=True, do the opposite of what inverted is.
        if inverted:
            for list_ in swap_face:
                list_.reverse()

        for list_ in swap_face:
            self.swap(*list_)
            if double:
                self.swap(*list_)

    @staticmethod
    def edge_keys():
        return [1, 3, 4, 6, 19, 20, 33, 35, 36, 38, 43, 44]

    @staticmethod
    def corner_keys():
        return [0, 2, 5, 7, 32, 34, 37, 39]

    @staticmethod
    def default_corners():
        corner_list = [(0, 8, 42), (2, 40, 26), (5, 16, 10), (7, 24, 18),
                       (32, 15, 21), (34, 23, 29), (37, 47, 13), (39, 31, 45)]
        c_ = list()
        for corner in corner_list:
            c_.append(Corner(corner))

        return c_

    @staticmethod
    def default_edges():
        edge_list = [(1, 41), (3, 9), (4, 25), (6, 17),
                     (19, 12), (20, 27), (33, 22), (35, 14),
                     (36, 30), (38, 46), (43, 28), (44, 11)]

        c_ = list()
        for edge in edge_list:
            c_.append(Edge(edge))

        return c_

    def get_corners(self):
        c_ = list()
        for key in self.corner_keys():
            c_.append(self.get_corner_at_key(key))
        return c_

    def get_edges(self):
        c_ = list()
        for key in self.edge_keys():
            c_.append(self.get_edge_at_key(key))
        return c_

    def get_edge_at_key(self, position):
        # See enumerated cube diagram for edge keys and edges connected to them
        for key, other in self.default_edges():
            if key == position:
                return Edge([self.facet_list[key], self.facet_list[other]])
        raise ValueError("Invalid key '{}'. 'position' must be a valid key.".format(position))

    def get_corner_at_key(self, position):
        # See enumerated cube diagram for edge keys and edges connected to them
        # Order is the key piece followed by other pieces in clockwise direction
        for key, o1, o2 in self.default_corners():
            if key == position:
                return Corner([self.facet_list[key], self.facet_list[o1], self.facet_list[o2]])
        raise ValueError("Invalid key '{}'. 'position' must be a valid key.".format(position))


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

    def __repr__(self):
        return "<Move: {}>".format(self.move)

    def __str__(self):
        return self.move


class Algorithm:
    def __init__(self, algorithm_string, cube):
        self._string = algorithm_string  # Valid algorithms are space-delimited, e.g., "R' U R U'"
        self._cube = cube
        self._step = 0

        self.string = ""
        self.algorithm = []
        self.set_algorithm(self._string)

    def __str__(self):
        return self.string

    def set_algorithm(self, string):
        str_list = string.split(" ")
        for s in str_list:
            try:
                self.algorithm.append(CubeMovement(s))
            except ValueError as e:
                self.algorithm = []  # We want this to be empty if it fails at making the alg
                raise ValueError(e)

        self.string = self._string = " ".join(str_list)

    def execute(self):
        for move in self.algorithm:
            self.step()

    def get_step(self):
        return self._step

    def step(self):
        if self._step >= len(self.algorithm):
            return  # Can't go forward any more  TODO: Should this be an exception?
        current_step = self.algorithm[self._step]
        self._cube.move(current_step)
        self._step += 1

    def step_back(self):
        if self._step <= 0:
            return  # Can't go back any more  TODO: Should this be an exception?
        self._step -= 1
        current_step = self.algorithm[self._step]
        self._cube.move(current_step, reverse=True)

    def is_executing(self):
        if 0 < self._step < len(self.algorithm):
            return True
        return False

    def is_finished(self):
        # Only available when stepping through algorithm, execute() resets to 0
        return self._step >= len(self.algorithm)


class SolvabilityChecker:
    def __init__(self, cube):
        self._cube = cube
        pass

    def has_correct_unique_facets(self):
        if sorted(self._cube.facet_list) == list(range(48)):
            return True
        return False

    def has_correct_edges(self):
        edges = self._cube.get_edges()
        default_edges = self._cube.default_edges()
        edges_correct = True
        for edge in edges:
            if edge not in default_edges and edge.rotated() not in default_edges:
                edges_correct = False
        return edges_correct

    def has_correct_corners(self):
        corners = self._cube.get_corners()
        default_corners = self._cube.default_corners()
        corners_correct = True
        for corner in corners:
            if corner not in default_corners \
              and corner.rotated(1) not in default_corners \
              and corner.rotated(2) not in default_corners:
                corners_correct = False
        return corners_correct

    def has_orientable_edges(self):
        edges = self._cube.get_edges()
        edge_keys = self._cube.edge_keys()

        counter = 0
        for edge in edges:
            # If the edge orientation of a piece is correct
            if edge[0] in edge_keys:
                counter += 1
        # A cube's edges can only be legally oriented in pairs, so if there is one flipped edge on
        # the cube there must always be another.
        # Therefore, solvable cubes will always have their number of flipped pieces divisible by 2.
        return counter % 2 == 0

    def has_orientable_corners(self):
        corners = self._cube.get_corners()
        corner_keys = self._cube.corner_keys()

        counter = 0
        for corner in corners:
            if corner[0] in corner_keys:
                pass
            if corner.rotated(1)[0] in corner_keys:
                counter -= 1
            if corner.rotated(2)[0] in corner_keys:
                counter += 1
        # Corners have 3 rotations. A backwards rotation of one piece cancels a forward rotation of another.
        # If two pieces are rotated forward, a third piece rotated backward twice cancels them out. Since there
        # are only three rotations, two backwards rotations counts as one forward rotation. Therefore, three
        # forward rotations cancels itself out. And thus rotations must be divisible by 3 to be orientable.
        return counter % 3 == 0

    def has_permutable_edges(self):
        pass

    def has_permutable_corners(self):
        pass


class Util:
    @staticmethod
    def get_color(subfacet: int) -> Color:
        # Each face has 8 subfacets (excluding centers)
        # Floor dividing a subfacet by 8 and adding 1 gives the face it belongs to
        # For example, the color of subfacet 36 can be found like this:
        # 36 // 8 + 1 == 5, so the color of 36 is the color of the 5th face (default yellow)
        return Color(subfacet // 8 + 1)

    @staticmethod
    def print_face(cube: Cube):
        st = ["UP", "LEFT", "FRONT", "RIGHT", "DOWN", "BACK"]
        sides = 6
        for i in range(sides):
            face = cube.facet_list[i * 8:i * 8 + 8]
            print("{}:".format(st[i]))
            print("{} {} {}\n{} A {}\n{} {} {}".format(*face))


if __name__ == '__main__':
    # R2 = CubeMovement("R2")
    # cb = Cube()
    # cb.move(R2)
    # print_face(cb)
    c = Cube()
    a = Algorithm("R U R' U R U2 R'", c)
    a.execute()
    a.execute()
    #c.move("F")
    c.move("L")
    c.move("R")
    #c.swap(6, 17)
    #print(c.get_edges())
    #print(c.get_edge_at_key(6))
    #Util.print_face(c)
    sc = SolvabilityChecker(c)
    print(sc.has_orientable_edges())
    print(sc.has_orientable_corners())