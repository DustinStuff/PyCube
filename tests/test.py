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
        self.assertEqual(cube.Util.get_color(20), cube.Color.BLUE)
        self.assertEqual(cube.Util.get_color(41), cube.Color.GREEN)
        self.assertEqual(cube.Util.get_color(47), cube.Color.GREEN)
        self.assertEqual(cube.Util.get_color(39), cube.Color.YELLOW)
        self.assertEqual(cube.Util.get_color(3), cube.Color.WHITE)


class TestCubeFunctionality(unittest.TestCase):
    def setUp(self):
        self.cube = cube.Cube()

    def test_swap(self):
        test_cube = cube.Cube()
        test_cube.facet_list[0] = 1
        test_cube.facet_list[1] = 0
        self.cube.swap(0, 1)
        self.assertEqual(test_cube, self.cube)

    def test_get_edge_at_key(self):
        key = 4
        test_edge = cube.Edge((4, 25))
        edge = self.cube.get_edge_at_key(key)
        self.assertEqual(test_edge, edge)

        self.cube.swap(4, 25)
        edge = self.cube.get_edge_at_key(key)
        self.assertNotEqual(test_edge, edge)

    def test_get_corner_at_key(self):
        pass  # TODO: Write this one

    def test_get_swapped_edge_at_key(self):
        key = 4
        test_edge = cube.Edge((25, 4))
        self.cube.swap(4, 25)
        edge = self.cube.get_edge_at_key(key)
        self.assertEqual(test_edge, edge)

        self.cube.swap(4, 25)
        edge = self.cube.get_edge_at_key(key)
        self.assertNotEqual(test_edge, edge)




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


class TestCubeMovement(unittest.TestCase):
    # TODO: Add test cube movement cases to make sure movements are actually correct
    pass


class TestAlgorithmClass(unittest.TestCase):
    def setUp(self) -> None:
        self.cube = cube.Cube()
        self.alg = cube.Algorithm("R U R' U'", self.cube)

    def test_step_forward_then_backward(self):
        default_cube = cube.Cube()
        self.alg.step()
        self.alg.step_back()
        self.assertEqual(default_cube, self.cube)

    def test_is_executing(self):
        self.alg.step()
        self.assertTrue(self.alg.is_executing())
        self.alg.step()
        self.alg.step()
        self.alg.step()
        self.assertFalse(self.alg.is_executing())
        self.alg.step_back()
        self.assertTrue(self.alg.is_executing())

    def test_is_finished(self):
        #alg = cube.Algorithm("R U R' U'", self.cube)
        # Who even uses loops
        self.assertFalse(self.alg.is_finished())
        self.alg.step()
        self.assertFalse(self.alg.is_finished())
        self.alg.step()
        self.assertFalse(self.alg.is_finished())
        self.alg.step()
        self.assertFalse(self.alg.is_finished())
        self.alg.step()
        self.assertTrue(self.alg.is_finished())

    def test_steps_too_far(self):
        # alg = cube.Algorithm("R U R' U'", self.cube)
        self.alg.step()
        self.alg.step()
        self.alg.step()
        self.alg.step()
        self.alg.step()

    def test_step_executes_correctly(self):
        test_cube = cube.Cube()
        test_cube.move("R")
        self.alg.step()
        self.assertEqual(test_cube, self.cube)
        test_cube.move("U")
        self.alg.step()
        self.assertEqual(test_cube, self.cube)
        test_cube.move("R'")
        self.alg.step()
        self.assertEqual(test_cube, self.cube)
        test_cube.move("U'")
        self.alg.step()
        self.assertEqual(test_cube, self.cube)

    def test_algorithm_executes_correctly(self):
        test_cube = cube.Cube()
        test_cube.move("R")
        test_cube.move("U")
        test_cube.move("R'")
        test_cube.move("U'")
        self.alg.execute()
        self.assertTrue(self.cube == test_cube)
        self.assertTrue(self.alg.is_finished())


class TestSolvabilityClass(unittest.TestCase):
    def setUp(self) -> None:
        self.cube = cube.Cube()
        self.solve_check = cube.SolvabilityChecker(self.cube)

    def test_facet_list_correct_no_duplicates(self):
        self.cube.move("R2")
        self.assertTrue(self.solve_check.has_correct_unique_facets())
        self.cube.swap(1, 2)  # Impossible case, but should still pass this test
        self.assertTrue(self.solve_check.has_correct_unique_facets())
        self.cube.facet_list[1] = 5
        self.assertFalse(self.solve_check.has_correct_unique_facets())

    def test_has_correct_edges(self):
        self.cube.move("R2")
        self.assertTrue(self.solve_check.has_correct_edges())
        self.cube.swap(4, 25)  # Unsolvable case, but should still pass this test
        self.assertTrue(self.solve_check.has_correct_edges())
        self.cube.swap(4, 1)
        self.assertFalse(self.solve_check.has_correct_edges())
        self.cube.swap(4, 1)  # Swap edge back to true case
        self.cube.swap(0, 2)  # Swaps corners, should pass
        self.assertTrue(self.solve_check.has_correct_edges())

    def test_has_correct_corners(self):
        self.cube.move("R2")
        self.cube.move("L")
        self.assertTrue(self.solve_check.has_correct_corners())
        self.cube.swap(13, 37, 47)  # Unsolvable, but still should pass
        self.assertTrue(self.solve_check.has_correct_corners())
        self.cube.swap(13, 37)  # leet. should fail.
        self.assertFalse(self.solve_check.has_correct_corners())
        self.cube.swap(13, 37)
        self.cube.swap(12, 14)  # Swaps edges, should pass
        self.assertTrue(self.solve_check.has_correct_corners())

    def test_has_orientable_edges(self):
        self.assertTrue(self.solve_check.has_orientable_edges())
        self.cube.move("R")
        self.assertTrue(self.solve_check.has_orientable_edges())
        self.cube.move("F")
        self.assertTrue(self.solve_check.has_orientable_edges())

        self.cube.swap(4, 25)
        self.assertFalse(self.solve_check.has_orientable_edges())
        self.cube.swap(6, 17)
        self.assertTrue(self.solve_check.has_orientable_edges())

    def test_has_orientable_corners(self):
        #self.assertTrue(self.solve_check.has_orientable_corners())
        #self.assertTrue(self.solve_check.has_orientable_corners())
        self.cube.move("R")
        self.cube.move("F")
        self.cube.swap(5, 16, 10)
        self.assertFalse(self.solve_check.has_orientable_corners())
        self.cube.swap(0, 42, 8)
        self.assertTrue(self.solve_check.has_orientable_corners())

if __name__ == '__main__':
    unittest.main()
