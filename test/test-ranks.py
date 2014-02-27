
import os.path
import sys

# Hack the path..

p = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
sys.path.insert(0, p)
del p

# External
import unittest

# Local
import ranker
import utils as test_util

simple_data = { '0': 3, '1': 2, '2': 1, '3': 0 }
simple_pos = { 1: set(['0']), 2: set(['1']), 3: set(['2']), 4: set(['3']) }
simple_points = { '0': 4.0, '1': 3.0, '2': 2.0, '3': 1.0 }

dsq_data = { '0': 3, '1': 2, '2': 1, '3': 0 }
dsq_dsq = [ '0', '2' ]
dsq_pos = { 1: set(['1']), 2: set(['3']), 3: set(['0', '2']) }
dsq_points = { '0': 0.0, '1': 4.0, '2': 0.0, '3': 3.0 }

tie1_data = { '0': 3, '1': 3, '2': 0, '3': 0 }
tie1_pos = { 1: set(['1', '0']), 3: set(['3', '2']) }
tie1_points = { '0': 3.5, '1': 3.5, '2': 1.5, '3': 1.5 }

tie2_data = { '0': 3, '1': 3, '2': 0, '3': 0 }
tie2_dsq = [ '0', '2' ]
tie2_pos = { 1: set(['1']), 2: set(['3']), 3: set(['0', '2']) }
tie2_points = { '0': 0.0, '1': 4.0, '2': 0.0, '3': 3.0 }

class PositionsTests(unittest.TestCase):

	def test_simple(self):
		pos = ranker.calc_positions(simple_data, [])
		test_util.assertEqual(simple_pos, pos, "Wrong positions")

	def test_tie(self):
		pos = ranker.calc_positions(tie1_data, [])
		test_util.assertEqual(tie1_pos, pos, "Wrong positions")

	def test_dsq(self):
		pos = ranker.calc_positions(dsq_data, dsq_dsq)
		test_util.assertEqual(dsq_pos, pos, "Wrong positions")

	def test_dsq_tie(self):
		pos = ranker.calc_positions(tie2_data, tie2_dsq)
		test_util.assertEqual(tie2_pos, pos, "Wrong positions")

class RankedPointsTests(unittest.TestCase):

	def test_simple(self):
		points = ranker.calc_ranked_points(simple_pos, [])
		test_util.assertEqual(simple_points, points, "Wrong points")

	def test_tie(self):
		points = ranker.calc_ranked_points(tie1_pos, [])
		test_util.assertEqual(tie1_points, points, "Wrong points")

	def test_dsq_tie(self):
		points = ranker.calc_ranked_points(tie2_pos, tie2_dsq)
		test_util.assertEqual(tie2_points, points, "Wrong points")

if __name__ == '__main__':
	unittest.main(buffer=True)
