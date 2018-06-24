import shlex
import subprocess
import time
import logging

from nires.settings import CALIBRATION_PATH, DS9
from nires.displaytools.helpers import construct_cursor

LOG = logging.getLogger(__name__)


class Ds9:
    """
    The ds9 class provides wrappers around the unix commands xpaget
    and xpaset. The class is smart enough to automatically detect
    a running ds9 and attach automatically displayed images to it
    """
    title = None

    def __init__(self, title):
        """
        ds9 construction init checks to see if a ds9 called title
        is currently running. If not, a new ds9 instance is created with
        that title
        """

        self.title = title
        cmd = shlex.split("xpaset -p {} scale zscale".format(title))  # set the path from the globals.py

        retcode = subprocess.call(cmd)

        if retcode == 1:
            subprocess.Popen([DS9, "-title", self.title])
            time.sleep(5)
            if self.title == "Spectrograph":
                self.xpaset("width 1250")
                self.xpaset("height 700")
                self.xpaset("scale zscale")
                self.xpaset("colorbar NO")
                self.xpaset("zoom 0.58 0.58")
            if self.title == "Viewer":
                self.xpaset("scale zscale")
                self.xpaset("colorbar NO")
                self.xpaset("zoom 0.5 0.5")

    def xpaget(self, cmd):
        """
        xpaget is a convenience function around unix xpaget

        :param cmd:
        :return:
        """
        cmd = shlex.split("xpaget {} {}".format(self.title, cmd))
        retcode = subprocess.call(cmd)

    def xpapipe(self, cmd, pipein):
        """
        xpapipe is a convenience wrapper around echo pipein | xpaset

        :param cmd:
        :param pipein:
        :return:
        """
        cmd = shlex.split("xpaset {} {}".format(self.title, cmd))
        p = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        p.stdin.write(pipein)
        p.stdin.flush()

    def xpaset(self, cmd):
        """
        xpaget is a convenience function around unix xpaset

        :param cmd:
        :return:
        """
        cmd = shlex.split("xpaset -p {} {}".format(self.title, cmd))
        retcode = subprocess.call(cmd)

    def frame_num(self, frame):
        """
        sets the ds9 frame number to [frame]

        :param frame:
        :return:
        """
        self.xpaset("frame {}".format(frame))

    def open(self, fname, frame=1):
        """
        opens a fits file [fname] into frame [frame]

        :param fname:
        :param frame:
        :return:
        """
        self.region_save()
        self.frame_num(frame)
        self.xpaset("file {}".format(fname))
        self.region_open()

    def wavelength_disp(self):
        """
        display wavelength regions

        :return:
        """
        self.xpaset("regions delete all")
        self.xpaset("regions {}/wavelength.reg".format(CALIBRATION_PATH))

    def emission_disp(self):
        """
        display emission lines regions

        :return:
        """
        self.xpaset("regions delete all")
        self.xpaset("regions {}/z_emission.reg".format(CALIBRATION_PATH))

    def redshift_disp(self):
        """
        display redshifted regions

        :return:
        """
        self.xpaset("regions delete all")
        self.xpaset("regions {}/zregion.reg".format(CALIBRATION_PATH))

    def cursor_disp(self, x, y, size=15, group="group1", label="1", color="white"):
        """
        display cursors

        :param x:
        :param y:
        :param size:
        :param group:
        :param label:
        :param color:
        :return:
        """
        regions = construct_cursor(x, y, size, group, label, color)
        self.xpaset(regions)

    def cursor_label(self, x, y, group="group1", label="1", color="white"):
        """
        display cursor labels

        :param x:
        :param y:
        :param group:
        :param label:
        :param color:
        :return:
        """
        font = "helvetica 16 normal"
        s = "regions command '{text {} {} # " \
            "color={} tag={} width=2 font=\"{}\" text=\"{}\" }'".format(x,
                                                                        y,
                                                                        color,
                                                                        group,
                                                                        font,
                                                                        label)
        self.xpaset(s)

    def cursor_delete(self, group):
        """
        delete cursors in group

        :param group:
        :return:
        """
        if group == "groupall":
            s = "regions delete all"
        else:
            s = "regions group {} delete".format(group)
        self.xpaset(s)

    def wavelength_delete(self):
        """
        delete all of the wavelength regions
        :return:
        """
        self.xpaset("regions delete all")

    def cursor_centroid(self, group):
        """
        centroid the regions in a group

        :param group:
        :return:
        """
        self.xpaset("regions group {} select".format(group))
        self.xpaset("regions centroid radius 5 iterations 5")
        self.xpaset("regions selectnone")

    def cursor_info(self, group):
        """
        get infor for a cursor group

        :param group:
        :return:
        """
        self.xpaset("regions group {} select".format(group))
        self.xpaset("regions getinfo")

    def region_save(self, data_dir="."):
        """
        save current regions
        :param data_dir:
        :return:
        """
        self.xpaset("regions save {}/{}.reg".format(data_dir, self.title))

    def region_open(self, data_dir="."):
        self.xpaset("regions {}/{}.reg".format(data_dir, self.title))

    def lindisp(self, dmin, dmax):
        self.xpaset("scale linear")
        self.xpaset("scale limits {} {}".format(dmin, dmax))
