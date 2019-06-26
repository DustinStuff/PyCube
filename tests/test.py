import unittest
import cube


class TestCubePieces(unittest.TestCase):
    def setUp(self) -> None:
        self.cube = cube.Cube()
        self.COLORS = cube.Color

    def test_solved_cube_correct_number_of_facets(self):
        facets = []

        for k, v in self.cube.cube_dict.items():
            if k == "corners":
                for k, corner in v.items():
                    facets += corner._corner
            if k == "edges":
                for k, edge in v.items():
                    facets += edge._edge

        facets.sort()
        self.assertEqual(facets, list(range(1, 49)))

    def test_facets_have_correct_corresponding_color(self):
        # White = top
        # Yellow = bottom
        # Red = left
        # Orange = right
        # Blue = front
        # Green = back

        # Tests some random and error-prone facets.
        self.assertEqual(cube.get_color(20), cube.Color.BLUE)
        self.assertEqual(cube.get_color(41), cube.Color.GREEN)
        self.assertEqual(cube.get_color(47), cube.Color.GREEN)
        self.assertEqual(cube.get_color(40), cube.Color.YELLOW)
        self.assertEqual(cube.get_color(3), cube.Color.WHITE)


class TestCubeManipulation(unittest.TestCase):
    def setUp(self) -> None:
        self.manipulated_cube = cube.Cube()
        self.test_case_cube = cube.Cube()
        self.test_case_cube.cube_dict["corners"]["UBL"] = cube.Corner([33, 16, 22])
        self.test_case_cube.cube_dict["corners"]["DFL"] = cube.Corner([1, 9, 43])

    def test_swap_corners_UBL_DFL(self):
        self.manipulated_cube.swap("UBL", "DFL")


if __name__ == '__main__':
    unittest.main()
