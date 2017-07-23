import unittest

from sr.comp import ranker


simple_data = { '0': 3, '1': 2, '2': 1, '3': 0 }
simple_pos = { 1: set(['0']), 2: set(['1']), 3: set(['2']), 4: set(['3']) }
simple_points = { '0': 8, '1': 6, '2': 4, '3': 2 }
simple_points_5_zones = { '0': 10, '1': 8, '2': 6, '3': 4 }

two_teams_data = { '0': 3, '1': 2 }
two_teams_pos = { 1: set(['0']), 2: set(['1']) }
two_teams_points_2_zones = { '0': 4, '1': 2 }
two_teams_points_4_zones = { '0': 8, '1': 6 }

dsq_data = { '0': 3, '1': 2, '2': 1, '3': 0 }
dsq_dsq = [ '0', '2' ]
dsq_pos = { 1: set(['1']), 2: set(['3']), 3: set(['0', '2']) }
dsq_points = { '0': 0, '1': 8, '2': 0, '3': 6 }

tie1_data = { '0': 3, '1': 3, '2': 0, '3': 0 }
tie1_pos = { 1: set(['1', '0']), 3: set(['3', '2']) }
tie1_points_4_zones = { '0': 7, '1': 7, '2': 3, '3': 3 }
tie1_points_5_zones = { '0': 9, '1': 9, '2': 5, '3': 5 }

tie2_data = { '0': 3, '1': 3, '2': 0, '3': 0 }
tie2_dsq = [ '0', '2' ]
tie2_pos = { 1: set(['1']), 2: set(['3']), 3: set(['0', '2']) }
tie2_points_4_zones = { '0': 0, '1': 8, '2': 0, '3': 6 }
tie2_points_5_zones = { '0': 0, '1': 10, '2': 0, '3': 8 }


class PositionsTests(unittest.TestCase):
    longMessage = True

    def test_reject_non_integer_points(self):
        data = {k: str(v) for k, v in simple_data.items()}
        with self.assertRaises(ValueError):
            ranker.calc_positions(data)

    def test_reject_negative_points(self):
        data = {k: -v for k, v in simple_data.items()}
        with self.assertRaises(ValueError):
            ranker.calc_positions(data)

    def test_simple(self):
        pos = ranker.calc_positions(simple_data, [])
        self.assertEqual(simple_pos, pos, "Wrong positions")

    def test_simple_no_dsq(self):
        pos = ranker.calc_positions(simple_data)
        self.assertEqual(simple_pos, pos, "Wrong positions")

    def test_two_teams(self):
        pos = ranker.calc_positions(two_teams_data, [])
        self.assertEqual(two_teams_pos, pos, "Wrong positions")

    def test_tie(self):
        pos = ranker.calc_positions(tie1_data, [])
        self.assertEqual(tie1_pos, pos, "Wrong positions")

    def test_tie_no_dsq(self):
        pos = ranker.calc_positions(tie1_data)
        self.assertEqual(tie1_pos, pos, "Wrong positions")

    def test_dsq(self):
        pos = ranker.calc_positions(dsq_data, dsq_dsq)
        self.assertEqual(dsq_pos, pos, "Wrong positions")

    def test_dsq_tie(self):
        pos = ranker.calc_positions(tie2_data, tie2_dsq)
        self.assertEqual(tie2_pos, pos, "Wrong positions")


class RankedPointsTests(unittest.TestCase):
    longMessage = True

    def test_reject_too_may_teams(self):
        # self-check
        self.assertGreater(len(simple_pos), 2, "Need more than two entrants")

        with self.assertRaises(ValueError):
            ranker.calc_ranked_points(simple_pos, num_zones=2)

    def test_simple(self):
        points = ranker.calc_ranked_points(simple_pos, [])
        self.assertEqual(simple_points, points, "Wrong points")

    def test_simple_spare_zone(self):
        points = ranker.calc_ranked_points(simple_pos, num_zones=5)
        self.assertEqual(simple_points_5_zones, points, "Wrong points")

    def test_simple_no_dsq(self):
        points = ranker.calc_ranked_points(simple_pos)
        self.assertEqual(simple_points, points, "Wrong points")

    def test_two_teams(self):
        points = ranker.calc_ranked_points(two_teams_pos, num_zones=2)
        self.assertEqual(two_teams_points_2_zones, points, "Wrong points")

    def test_two_teams_two_spare_zones(self):
        points = ranker.calc_ranked_points(two_teams_pos, num_zones=4)
        self.assertEqual(two_teams_points_4_zones, points, "Wrong points")

    def test_tie(self):
        points = ranker.calc_ranked_points(tie1_pos, [])
        self.assertEqual(tie1_points_4_zones, points, "Wrong points")

    def test_tie_no_dsq(self):
        points = ranker.calc_ranked_points(tie1_pos)
        self.assertEqual(tie1_points_4_zones, points, "Wrong points")

    def test_dsq_tie(self):
        points = ranker.calc_ranked_points(tie2_pos, tie2_dsq)
        self.assertEqual(tie2_points_4_zones, points, "Wrong points")

    def test_dsq_tie_one_spare_zone(self):
        points = ranker.calc_ranked_points(tie2_pos, tie2_dsq, num_zones=5)
        self.assertEqual(tie2_points_5_zones, points, "Wrong points")

    def test_detects_position_overlap_single_tie(self):
        with self.assertRaises(ValueError):
            ranker.calc_ranked_points({1: ['A', 'B'], 2: ['C', 'D']})

    def test_detects_higher_position_overlap_double_tie_higher(self):
        with self.assertRaises(ValueError):
            ranker.calc_ranked_points({1: ['A', 'B', 'C'], 2: ['D']})

    def test_detects_lower_position_overlap_double_tie(self):
        with self.assertRaises(ValueError):
            ranker.calc_ranked_points({1: ['A', 'B', 'C'], 3: ['D']})
