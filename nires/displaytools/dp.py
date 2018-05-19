#!/usr/bin/env python
# Take difference between two fits files

import logging
import sys

import nires.displaytools.helpers as helpers
from nires.displaytools.ds9 import Ds9

LOG = logging.getLogger(__name__)


try:
    title, prefix = helpers.return_instrument(sys.argv[1])
    fname = helpers.name_resolve(sys.argv[2], prefix)
    if fname:
        ds9 = Ds9(title).open(fname)
except (UnboundLocalError, ValueError, IndexError):
    LOG.warning("Bad Request:\n\tUnable to display picture\n"
                "Example valid requests:\n"
                "\t> dp s 11\n"
                "\t> dps 11\n"
                "\t> dps lp\n"
                "\t> dpv 7")



