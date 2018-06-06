import astropy.io.fits as pf
import glob
import os
import fnmatch
import logging

from nires.settings import DATA_PATH

LOG = logging.getLogger(__name__)

if not DATA_PATH:
    DATA_PATH = "."


def read_image(fname):
    """
    Try to return an image from a filename eles return none
    :param fname:
    :return:
    """
    try:
        a = pf.open(fname)[0].data
        return a
    except Exception as error:
        LOG.warning("Could not open %s, %s", fname, error)
    
    return None


def is_number(s):
    """
    if string is number return true else return false
    :param s:
    :return:
    """
    try:
        float(s)
        return True
    except (ValueError, TypeError):
        return False


def get_most_recent_file(data_dir, prefix="s", suffix=".fits"):
    """
    get the most recent filename of the spectrograph 's' or viewer 'v'
    :param data_dir:
    :param prefix:
    :param suffix:
    :return:
    """
    try:
        files = sorted([f for f in os.listdir(data_dir) if f.startswith(prefix[0]) and f.endswith(suffix) and len(f) < 22])
        return files[-1]
    except IndexError:
        LOG.warning("Data Directory is empty, cannot display image")
    return None


def get_specific_file(data_dir, prefix: str, index_string: str):
    """
    construct the filename by padding the input file index_string with '0's
    :param data_dir
    :param prefix:
    :param index_string:
    :return:
    """
    for file in os.listdir(data_dir):
        if fnmatch.fnmatch(file, "{}*{}.fits".format(prefix, index_string.zfill(4))):
            return file
    LOG.warning("Could not find file with number: %s", index_string)
    return None


def name_resolve(index_string, prefix, data_dir="."):
    """
    get filename of image you want to display from the few chars provided
    :param index_string:
    :param prefix:
    :param data_dir:
    :return:
    """

    # Check if only want most recent file indicated by indexString='c'
    if index_string == "lp":
        return get_most_recent_file(data_dir, prefix)

    # Check for length of input string to determine if you need to construct the name
    if is_number(index_string):
        return get_specific_file(data_dir, prefix, index_string)

    return None


def return_instrument(prefix):
    """
    Convert prefix to instrument name
    :param prefix:
    :return:
    """
    if prefix == "v":
        title = "Viewer"
    elif prefix == "s":
        title = "Spectrograph"
    else:
        LOG.warning("Bad Request:\n\tPlease specify 'v' for Viewer or 's' for Spectrograph")
    return title


def construct_cursor(x, y, size=15, group="group1", label="1", color="white", font="helvetica 14 normal"):
    """
    Method to construct the cursor string from inputs
    :param x:
    :param y:
    :param size:
    :param group:
    :param label:
    :param color:
    :param font:
    :return:
    """
    regions = "regions command '{{box {} {} {} {} # " \
              "color={} tag={} width=2 font=\"{}\" text=\"{}\"}}'".format(
                x, y, size, size, color, group, font, label)
    return regions
