#!/usr/bin/env python
# display wavelength info

import click
import logging
import re

from nires.settings import CALIBRATION_PATH, TMPDIR
from nires.displaytools.ds9 import Ds9

WAVELENGTH_REG = "wavelength.reg"
LOG = logging.getLogger(__name__)


def shift_region(redshift):
    with open("{}/{}".format(TMPDIR, "z_wavelength.reg"), "w") as outfile:
        with open("{}/{}".format(CALIBRATION_PATH, WAVELENGTH_REG), "r") as infile:
            for line in infile:
                if "# text" in line:
                    LOG.warning("found text %s", line)
                    nums = re.findall(r"[\d\.]+", line)
                    LOG.warning("extracted nums %s", nums)
                    out_string = "# text({},{}) text={{{:4.2f}}}\n".format(
                        nums[0], nums[1], float(nums[2]) / (1. + redshift))
                    LOG.warning("Out text %s", out_string)
                    outfile.write(out_string)
                else:
                    outfile.write(line)
        infile.close()
    outfile.close()


@click.command()
@click.option('--z', default="0")
def run(z):
    """
    Script to display a picture
    """
    ds9 = Ds9("Spectrograph")
    try:
        if z == "0":
            ds9.wavelength_disp()
        else:
            redshift = float(z)
            shift_region(redshift)
            ds9.redshift_disp()

    except (UnboundLocalError, ValueError, IndexError) as error:
        LOG.warning("Error: %s", error)
        LOG.warning("Bad Request:\n   Unable to display wavelengths\n"
                    "Example valid requests:\n"
                    "   dp s 11\n"
                    "   dps 11\n"
                    "   dps lp\n"
                    "   dpv 7")

if __name__ == '__main__':
    run()
