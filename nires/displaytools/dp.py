#!/usr/bin/env python
# Take difference between two fits files

import logging
import sys
import click

import nires.displaytools.helpers as helpers
from nires.displaytools.ds9 import Ds9

LOG = logging.getLogger(__name__)


@click.command()
@click.argument("inst", type=click.Choice(["v", "s"]), nargs=1)
@click.argument("fnum", nargs=1)
def run(inst, fnum):
    """
    Script to display a picture
    """
    try:
        title, prefix = helpers.return_instrument(inst)
        fname = helpers.name_resolve(fnum, prefix)
        if fname:
            ds9 = Ds9(title)
            ds9.open(fname)
    except (UnboundLocalError, ValueError, IndexError):
        LOG.warning("Bad Request:\n   Unable to display picture\n"
                    "Example valid requests:\n"
                    "   dp s 11\n"
                    "   dps 11\n"
                    "   dps lp\n"
                    "   dpv 7")

if __name__ == '__main__':
    run()

