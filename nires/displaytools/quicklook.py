import os
from time import sleep
import logging

import nires.displaytools.helpers as helpers
from nires.displaytools.ds9 import Ds9
import nires.displaytools.pdiff as pdiff
import nires.displaytools.dp as dp

LOG = logging.getLogger(__name__)


class Quicklook():

    def __init__(self):
        """
        setup the quicklook windows and display first frames
        """

        self.data_dir = os.environment.get("DATA_DIR", ".")

        # setup viewer
        self.viewer = Ds9("Viewer")

        # setup spectrograph
        self.spectrograph = Ds9("Spectrograph")

        self.lp = {
            "v": helpers.get_most_recent_file_num(self.data_dir, "v"),
            "s": helpers.get_most_recent_file_num(self.data_dir, "s")
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
        lp = helpers.get_most_recent_file_num(self.data_dir, inst)
        if lp > self.lp[inst]:
            self.lp["inst"] = lp

    def update_display(self, inst, lp):
        """
        check for buffer image, if there is one do a pdiff, else do a display picture

        :param inst:
        :param lp:
        :return:
        """
        bp = self.get_buffer(inst)
        if bp:
            pdiff.run(inst, [lp, bp])
        else:
            dp.run(inst, lp)

    def get_buffer(self, inst):
        data = self.read_metadata()
        return data.get("buffer" + inst)

    def read_metadata(self):
        data = {}
        try:
            with open(self.data_dir + ".metadata", "r") as file:
                for line in file:
                    key, value = line.split(":")
                    data[key] = value
        except Exception as error:
            LOG.warning("could not find metadata file %s", error)

        return data





