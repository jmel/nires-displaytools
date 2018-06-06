import unittest
from mock import patch

import nires.displaytools.helpers as helpers


class HelpersTest(unittest.TestCase):

    def test_is_number(self):
        self.assertTrue(helpers.is_number("56"))
        self.assertFalse(helpers.is_number("hi"))
        self.assertFalse(helpers.is_number(None))

    @patch("os.listdir", return_value=["s1.fits", "s2.fits", "v3.fits", "temp.txt"])
    def test_get_most_recent_file(self, mock_os):
        self.assertEqual("s2.fits", helpers.get_most_recent_file(".", prefix="s"))
        self.assertEqual("v3.fits", helpers.get_most_recent_file(".", prefix="v"))
        self.assertIsNone(helpers.get_most_recent_file(".", prefix="p"))

    @patch("os.listdir", return_value=[])
    def test_get_most_recent_file(self, mock_os):
        self.assertIsNone(helpers.get_most_recent_file(".", prefix="s"))

    def test_construct_filename(self):
        self.assertEqual("s*0041.fits", helpers.construct_filename("41", "s"))

    def test_construct_cursor(self):
        self.assertEqual("regions command '{box 10 10 10 10 # "
                         "color=blue tag=group1 width=2 "
                         "font=\"helvetica 14 normal\" "
                         "text=\"1\"}'",
                         helpers.construct_cursor(10, 10, 10,
                                                  "group1", "1", "blue"))
