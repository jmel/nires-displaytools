import unittest
from mock import patch
from io import StringIO
import nires.displaytools.cu as cu

GROUP5 = "box(800,600,15,15,0) # color=orange width=2 font=\"helvetica 14 normal\" text={5} tag={group5}"
GROUP4 = "box(400,400,15,15,0) # color=orange width=2 font=\"helvetica 14 normal\" text={5} tag={group4}"


class CuTest(unittest.TestCase):
    def test_parse_coordinates(self):
        self.assertEqual((800, 600), cu.parse_coordinates(GROUP5))

    def test_parse_coordinates_float(self):
        line = "box(800.56,600.73,15,15,0)"
        self.assertEqual((800.56, 600.73), cu.parse_coordinates(line))

    def test_parse_coordinates_empty_line(self):
        self.assertEqual((None, None), cu.parse_coordinates(""))

    def test_parse_coordinates_bad_line(self):
        self.assertEqual((None, None), cu.parse_coordinates("box(red,blue,15,15,0)"))
