from time import sleep
import logging

import nires.displaytools.helpers as helpers
import nires.displaytools.pdiff as pdiff
import nires.displaytools.dp as dp
from nires.displaytools.bp import get_buffer

LOG = logging.getLogger(__name__)


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

        self.update_display("v", self.lp["v"])
        self.update_display("s", self.lp["s"])

    def run(self):
        """
        run the system

        :return:
        """
        done = False
        while not done:
            self.run_inst("v")
            self.run_inst("s")
            sleep(2)

    def run_inst(self, inst):
        """
        run commands for each display

        :param inst:
        :return:
        """
        lp = helpers.get_most_recent_file(self.data_dir, inst)
        if lp > self.lp[inst]:
            self.lp[inst] = lp
            self.update_display(inst, self.lp[inst])

    def update_display(self, inst, lp):
        """
        check for buffer image, if there is one do a pdiff, else do a display picture

        :param inst:
        :param lp:
        :return:
        """
        bp = get_buffer(self.data_dir, inst)
        if bp and bp != "none":
            temp_name = pdiff.construct_temp_name(inst)
            pdiff.diff_image(lp, bp, temp_name=temp_name, imdir=self.data_dir)
            dp.display_image(inst, fname=temp_name, data_dir=self.data_dir)
        else:
            dp.display_image(inst, fname=lp, data_dir=self.data_dir)
