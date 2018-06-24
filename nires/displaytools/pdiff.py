#!/usr/bin/env python
# Take difference between two fits files

import logging
import warnings
import astropy.io.fits as pf
import click

import nires.displaytools.helpers as helpers
from nires.displaytools.dp import display_image
from nires.settings import TMPDIR

LOG = logging.getLogger(__name__)


def diff_image(imname1, imname2, temp_name="ds9_diff.fits", data_dir="."):
    im1 = helpers.read_image("{}/{}".format(data_dir, imname1))
    im2 = helpers.read_image("{}/{}".format(data_dir, imname2))

    # subtract the images
    hdu = pf.PrimaryHDU(im1 - im2)
    hdulist = pf.HDUList([hdu])

    # temp save
    with warnings.catch_warnings():
        warnings.simplefilter('ignore')
        hdulist.writeto("{}/{}".format(TMPDIR, temp_name), clobber=True)


def construct_temp_name(inst):
    return "ds9_diff_{}.fits".format(inst)


@click.command()
@click.argument("inst", type=click.Choice(["v", "s"]), nargs=1)
@click.argument("fnums", nargs=-1)
@click.option('--d', default=".")
def run(inst, fnums, d):
    """
    script to display the difference of two images
    """
    try:
        imname1 = helpers.name_resolve(fnums[0], inst, data_dir=d)
        imname2 = helpers.name_resolve(fnums[1], inst, data_dir=d)

        temp_name = construct_temp_name(inst)
        diff_image(imname1, imname2, temp_name=temp_name, data_dir=d)
        display_image(inst, temp_name, data_dir=TMPDIR)

    except (TypeError, ValueError, IndexError):
        LOG.warning("Bad Request:\n   Unable to display picture\n"
                    "Example valid requests:\n"
                    "   pdiff s 10 11\n"
                    "   pdiffs 10 11\n"
                    "   pdiffv 10 lp\n")

if __name__ == '__main__':
    run()
