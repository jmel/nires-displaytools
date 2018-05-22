import unittest

import nires.displaytools.helpers as helpers


class HelpersTest(unittest.TestCase):

    def test_construct_filename(self):
        self.assertEqual("s0041.fits", helpers.construct_filename("41", "s"))

    def test_construct_cursor(self):
        self.assertEqual("regions command '{box 10 10 10 10 # "
                         "color=blue tag=group1 width=2 "
                         "font=\"helvetica 14 normal\" "
                         "text=\"1\"}'",
                         helpers.construct_cursor(10, 10, 10,
                                                  "group1", "1", "blue"))
