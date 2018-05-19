import astropy.io.fits as pf
import glob
import os
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
    except:
        LOG.warning("Could not open %s", fname)
    
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
    except ValueError:
        return False


def get_most_recent_file(path, prefix="s", suffix=".fits"):
    """
    get the most recent filename of the spectrograph 's' or viewer 'v'
    :param path:
    :param prefix:
    :param suffix:
    :return:
    """
    
    files = sorted([f for f in os.listdir(path) if f.startswith(prefix[0]) and f.endswith(suffix) and len(f) < 22])
    return files[-1]


def construct_filename(index_string: str, prefix: str):
    """
    construct the filename by padding the input file index_string with '0's
    :param index_string:
    :param prefix:
    :return:
    """
    return prefix + index_string.zfill(4) + ".fits"


def name_resolve(index_string, prefix):
    """
    get filename of image you want to display from the few chars provided
    :param index_string:
    :param prefix:
    :return:
    """

    # check if only want most recent file indicated by indexString='c'
    if index_string == "lp":
        try:
            return get_most_recent_file(".", prefix)
        except:
            LOG.warning("Bad Request:\n\tCould not resolve name of latest picture")
    # Check for length of input string to determine if you need to construct the name

    if is_number(index_string):
        name = construct_filename(index_string, prefix)
          
        try:
            return glob.glob(DATA_PATH + "/" + name)[0]  # made the path absolute
        except IndexError as error:
            LOG.warning("Bad Request:\n\tCould not find picture number: %s",
                        index_string)
    return ""


def return_instrument(instrument_string):
    if instrument_string == "v":
        title = "Viewer"
        prefix = "v*"
    elif instrument_string == "s":
        title = "Spectrograph"
        prefix = "s*"
    else:
        LOG.warning("Bad Request:\n\tPlease specify 'v' for Viewer or 's' for Spectrograph")
    return title, prefix


def construct_cursor(x, y, size=15, group="group1", label="1", color="white"):
    font = "helvetica 14 normal"
    regions = "regions command '{{box {} {} {} {} # " \
              "color={} tag={} width=2 font=\"{}\" text=\"{}\"}}'".format(
                x, y, size, size, color, group, font, label)
    return regions
