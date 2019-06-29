import unittest
import cube


class TestCubePieces(unittest.TestCase):
    def setUp(self) -> None:
        self.cube = cube.Cube()
        self.COLORS = cube.Color

    def test_solved_cube_correct_number_of_facets(self):
        facets = self.cube.facet_list.copy()
        facets.sort()

        self.assertEqual(facets, list(range(48)))

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
        self.assertEqual(cube.get_color(39), cube.Color.YELLOW)
        self.assertEqual(cube.get_color(3), cube.Color.WHITE)

class TestPieceSwap(unittest.TestCase):
    def setUp(self) -> None:
        self.cube = cube.Cube()
        # self.facet_check_list = list(range(48))
        # self.facet_check_list[1] = 2
        # self.facet_check_list[2] = 1

    def test_swap_two_facets(self):
        self.cube.swap(1, 2)
        self.assertEqual(self.cube.facet_list[2], 1)
        self.assertEqual(self.cube.facet_list[1], 2)

    def test_swap_three_facets(self):
        # self.facet_check_list = list(range(48))  # Reset list
        # self.facet_check_list[22] = 24
        # self.facet_check_list[23] = 22
        # self.facet_check_list[24] = 23
        self.cube.swap(22, 23, 24)
        self.assertEqual(self.cube.facet_list[22], 24)
        self.assertEqual(self.cube.facet_list[23], 22)
        self.assertEqual(self.cube.facet_list[24], 23)

    def test_swap_8_facets(self):
        self.cube.swap(38, 39, 40, 41, 42, 43, 44, 45)
        self.assertEqual(self.cube.facet_list[38], 45)
        self.assertEqual(self.cube.facet_list[39], 38)
        self.assertEqual(self.cube.facet_list[43], 42)

    def test_passing_wrong_type(self):
        self.assertRaises(TypeError, self.cube.swap, 1, 2, "g")

    def test_passing_duplicate_values(self):
        self.assertRaises(ValueError, self.cube.swap, 1, 16, 33, 16)


if __name__ == '__main__':
    unittest.main()