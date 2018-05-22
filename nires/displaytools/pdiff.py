#!/usr/bin/env python
# Take difference between two fits files

import logging
import warnings
import astropy.io.fits as pf
import click

import nires.displaytools.helpers as helpers
from nires.displaytools.ds9 import Ds9

LOG = logging.getLogger(__name__)


@click.command()
@click.argument("inst", type=click.Choice(["v", "s"]), nargs=1)
@click.argument("fnums", nargs=-1)
def run(inst, fnums):
    """
    script to display the difference of two images
    """
    try:
        title, prefix = helpers.return_instrument(inst)

        a = helpers.read_image(helpers.name_resolve(fnums[0], prefix))
        b = helpers.read_image(helpers.name_resolve(fnums[1], prefix))

        # subtract the images
        hdu = pf.PrimaryHDU(a - b)
        hdulist = pf.HDUList([hdu])

        # temp save
        fname = "ds9_diff.fits"
        with warnings.catch_warnings():
            warnings.simplefilter('ignore')
            hdulist.writeto(fname, clobber=True)

        # display
        ds9 = Ds9(title)
        ds9.region_save()
        ds9.open(fname, 1)
        ds9.region_open()

    except (TypeError, ValueError, IndexError):
        LOG.warning("Bad Request:\n   Unable to display picture\n"
                    "Example valid requests:\n"
                    "   pdiff s 10 11\n"
                    "   pdiffs 10 11\n"
                    "   pdiffv 10 lp\n")

if __name__ == '__main__':
    run()
