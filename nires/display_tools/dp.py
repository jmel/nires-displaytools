#!/usr/bin/env python
# Take difference between two fits files

import logging
import sys

import nires.display_tools.imDisplay as imD
from nires.display_tools.ds9 import Ds9

LOG = logging.getLogger(__name__)

fname = None
title = None

if len(sys.argv) == 3:
    title, prefix = imD.return_instrument(sys.argv[1])
    fname = imD.name_resolve(sys.argv[2], prefix)

if not fname:
    LOG.warning('Did not specify required arguments, Here are some examples: '
                '"dps 50" or "dp s 50", "dpv 50" or "dp v 50"  ')
    exit()
        
try:
    LOG.info("loading %s to ds9", fname)
    ds9 = Ds9(title)
    ds9.open(fname, 1)  # the number is used to set the frame number in the tile mode which is enable
except:
    LOG.error("Could not display %s", fname)
