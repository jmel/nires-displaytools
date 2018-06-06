#!/usr/bin/env python
# Take difference between two fits files

import logging
import warnings
import astropy.io.fits as pf
import click

import nires.displaytools.helpers as helpers
from nires.displaytools.dp import display_image
LOG = logging.getLogger(__name__)


def diff_image(imname1, imname2, temp_name="ds9_diff.fits", imdir="."):
    im1 = helpers.read_image("{}/{}".format(imdir, imname1))
    im2 = helpers.read_image("{}/{}".format(imdir, imname2))

    # subtract the images
    hdu = pf.PrimaryHDU(im1 - im2)
    hdulist = pf.HDUList([hdu])

    # temp save
    with warnings.catch_warnings():
        warnings.simplefilter('ignore')
        hdulist.writeto("{}/{}".format(imdir, temp_name), clobber=True)


def construct_temp_name(inst):
    return "ds9_diff_{}.fits".format(inst)


@click.command()
@click.argument("inst", type=click.Choice(["v", "s"]), nargs=1)
@click.argument("fnums", nargs=-1)
def run(inst, fnums):
    """
    script to display the difference of two images
    """
    try:
        imname1 = helpers.name_resolve(fnums[0], inst)
        imname2 = helpers.name_resolve(fnums[1], inst)

        temp_name = construct_temp_name(inst)
        diff_image(imname1, imname2, temp_name=temp_name)
        display_image(inst, temp_name)

    except (TypeError, ValueError, IndexError):
        LOG.warning("Bad Request:\n   Unable to display picture\n"
                    "Example valid requests:\n"
                    "   pdiff s 10 11\n"
                    "   pdiffs 10 11\n"
                    "   pdiffv 10 lp\n")

if __name__ == '__main__':
    run()
