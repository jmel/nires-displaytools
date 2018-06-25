#!/usr/bin/env python
# run quicklook

from time import sleep
import os
import logging
import click

import nires.displaytools.helpers as helpers
import nires.displaytools.pdiff as pdiff
import nires.displaytools.dp as dp
from nires.displaytools.bp import get_buffer
from nires.displaytools.ds9 import Ds9
from nires.settings import TMPDIR

LOG = logging.getLogger(__name__)
NIRES_AUTODISPLAY_STOP = "NIRES_AUTODISPLAY_STOP"
NIRES_AUTODISPLAY_START = "NIRES_AUTODISPLAY_START"


class QuickLook:
    def __init__(self, data_dir="."):
        """
        Setup the QuickLook windows and display first frames
        """

        self.data_dir = data_dir

        self.lp = {
            "v": helpers.get_most_recent_file(self.data_dir, "v"),
            "s": helpers.get_most_recent_file(self.data_dir, "s")
        }

        Ds9("Spectrograph")
        Ds9("Viewer")

    def run(self):
        """
        run the system

        :return:
        """
        while os.path.isfile("{}/{}".format(TMPDIR, NIRES_AUTODISPLAY_START)):
            self.run_inst("v")
            self.run_inst("s")
            sleep(3)

    def run_inst(self, inst):
        """
        run commands for each display

        :param inst:
        :return:
        """
        lp = helpers.get_most_recent_file(self.data_dir, inst)
        if lp > self.lp[inst]:
            self.lp[inst] = lp

            # now that you have a new file wait briefly to write out
            sleep(2)
            self.update_display(inst, self.lp[inst])

    def update_display(self, inst, lp):
        """
        check for buffer image, if there is one do a pdiff, else do a display picture

        :param inst:
        :param lp:
        :return:
        """
        bp = get_buffer(inst)
        if bp and bp != "none":
            temp_name = pdiff.construct_temp_name(inst)
            pdiff.diff_image(lp, bp, temp_name=temp_name, data_dir=self.data_dir)
            dp.display_image(inst, fname=temp_name, data_dir=TMPDIR)
        else:
            dp.display_image(inst, fname=lp, data_dir=self.data_dir)


@click.command()
@click.argument("option", type=click.Choice(["auto", "manual"]), nargs=1)
@click.option('--d', default=".")
def run(option, d):

    ql = QuickLook(data_dir=d)
    if option == "manual":
        os.system("touch {}/{}".format(TMPDIR, NIRES_AUTODISPLAY_STOP))
        os.system("rm {}/{}".format(TMPDIR, NIRES_AUTODISPLAY_START))
    elif option == "auto":
        os.system("touch {}/{}".format(TMPDIR, NIRES_AUTODISPLAY_START))
        os.system("rm {}/{}".format(TMPDIR, NIRES_AUTODISPLAY_STOP))
        ql.update_display("v", ql.lp["v"])
        ql.update_display("s", ql.lp["s"])
        ql.run()

if __name__ == '__main__':
    run()

