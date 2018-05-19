#!/usr/bin/env python
# change the display

import sys
import logging

from nires.displaytools.ds9 import Ds9
from nires.displaytools.helpers import return_instrument

LOG = logging.getLogger(__name__)

try:
    title, prefix = return_instrument(sys.argv[1])
    ds9 = Ds9(title)
    ds9.lindisp(float(sys.argv[2]), float(sys.argv[3]))
except (UnboundLocalError, ValueError):
    LOG.warning("Bad Request:\n\tUnable to change display\n"
                "Example valid requests:\n"
                "\t> lindisp s 0 100\n"
                "\t> lindisps 0 100\n"
                "\t> lindispv 0 100")

