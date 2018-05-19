#!/usr/bin/env python
# Take difference between two fits files

import sys
import logging
import warnings
import astropy.io.fits as pf

import nires.displaytools.helpers as helpers
from nires.displaytools.ds9 import Ds9

LOG = logging.getLogger(__name__)


if len(sys.argv) == 4: 

    title, prefix = helpers.return_instrument(sys.argv[1])

    a = helpers.read_image(helpers.name_resolve(sys.argv[2], prefix))
    b = helpers.read_image(helpers.name_resolve(sys.argv[3], prefix))
else:
    LOG.warning("Bad Request:\n\tUnable to display picture\n"
                "Example valid requests:\n"
                "\t> pdiff s 10 11\n"
                "\t> pdiffs 10 11\n")
    exit();


try:
    hdu = pf.PrimaryHDU(a - b)
    hdulist = pf.HDUList([hdu])
except:
    LOG.warning("Could not create FITS HDU")

try:
    fname = "ds9_diff.fits"
    with warnings.catch_warnings():
        warnings.simplefilter('ignore')
        hdulist.writeto(fname, clobber=True)
    ds9 = Ds9(title)
    ds9.region_save()
    ds9.open(fname, 1)
    ds9.region_open()
except Exception as error:
    LOG.warning("Could not write %s", error)
