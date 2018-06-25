#!/usr/bin/env python
# display picture

import logging
import click

import nires.displaytools.helpers as helpers
from nires.displaytools.ds9 import Ds9
from nires.settings import TMPDIR

LOG = logging.getLogger(__name__)


def display_image(inst, fname, data_dir="."):
    """
    method to display images to ds9
    :param inst:
    :param fname:
    :param data_dir:
    :return:
    """
    title = helpers.return_instrument(inst)
    ds9 = Ds9(title)
    ds9.region_save(data_dir=TMPDIR)
    ds9.region_delete()
    ds9.open("{}/{}".format(data_dir, fname), 1)
    ds9.region_open(data_dir=TMPDIR)


@click.command()
@click.argument("inst", type=click.Choice(["v", "s"]), nargs=1)
@click.argument("fnum", nargs=1)
@click.option('--d', default=".")
def run(inst, fnum, d):
    """
    Script to display a picture
    """
    try:
        fname = helpers.name_resolve(fnum, inst, data_dir=d)
        if fname:
            display_image(inst, fname, data_dir=d)
    except (UnboundLocalError, ValueError, IndexError):
        LOG.warning("Bad Request:\n   Unable to display picture\n"
                    "Example valid requests:\n"
                    "   dp s 11\n"
                    "   dps 11\n"
                    "   dps lp\n"
                    "   dpv 7")

if __name__ == '__main__':
    run()

