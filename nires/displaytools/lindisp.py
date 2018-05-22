#!/usr/bin/env python
# change the display

import sys
import logging
import click

from nires.displaytools.ds9 import Ds9
from nires.displaytools.helpers import return_instrument

LOG = logging.getLogger(__name__)


@click.command()
@click.argument("inst", type=click.Choice(["v", "s"]), nargs=1)
@click.argument("low", nargs=1)
@click.argument("high", nargs=1)
def run(inst, low, high):
    """
    script to change the display scale parameters
    """
    try:
        title, prefix = return_instrument(inst)
        ds9 = Ds9(title)
        ds9.lindisp(float(low), float(high))
    except (UnboundLocalError, ValueError):
        LOG.warning("Bad Request:\n   Unable to change display\n"
                    "Example valid requests:\n"
                    "   lindisp s 0 100\n"
                    "   lindisps 0 100\n"
                    "   lindispv 0 100")

if __name__ == '__main__':
    run()
