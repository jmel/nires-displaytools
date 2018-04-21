import pyfits as pf
import glob
import os
import logging

from nires.settings import DATAPATH

LOG = logging.getLogger(__name__)


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
    
    # handle old version of filename
    if len(files) == 0 and prefix[0] == "v":
        files = sorted([f for f in os.listdir(path) if f.startswith("i") and f.endswith(suffix) and len(f) < 22])

    return files[-1]


def construct_filename(index_string: str, prefix: str):
    """
    construct the filename by padding the input file index_string with '0's
    :param index_string:
    :param prefix:
    :return:
    """
    index_string_len = len(index_string)
    if index_string_len < 4:
        name = ("0" + index_string for i in range(4 - index_string_len)) + ".fits"
    else:
        name = prefix + index_string + ".fits"

    return name


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
            LOG.warning("Couldn't resolve name of latest picture")
    # Check for length of input string to determine if you need to construct the name

    if is_number(index_string):
        name = construct_filename(prefix, index_string)
          
        try:
            return glob.glob(DATAPATH + name)[0] #made the path absolute
        except:
            LOG.warning("Couldn't find picture number: %s", index_string)
    return ""


def return_instrument(instrument_string):
    if instrument_string == "v":
        title = "Viewer"
        prefix = "v*"
    elif instrument_string == "s":
        title = "Spectrograph"
        prefix = "s*"
    else:
        LOG.warning("Please specify v for Viewer or s for Spectrograph")
    return title, prefix
