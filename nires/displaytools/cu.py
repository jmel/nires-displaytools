#!/usr/bin/env python
# Control the cursors on the NIRES viewer ds9 window

import click
import logging
import random

from nires.displaytools.ds9 import Ds9

COLORS = ["white",
          "yellow",
          "cyan",
          "blue",
          "black",
          "orange",
          "magenta",
          "green",
          "red",
          "brown",
]
LOG = logging.getLogger(__name__)


def display_cursor(ds9, cursor):
    """
    method to display cursors on viewer
    :param ds9:
    :param cursor:
    :return:
    """
    if cursor == 'all':
        ds9.cursor_delete(group="group" + cursor)
        for i in range(6):
            ds9.cursor_disp(800, 100 + i * 100, 15,
                            group="group" + str(i),
                            label=str(i),
                            color=COLORS[i])
    else:
        cu_x = 800
        cu_y = 100 + int(cursor[0]) * 100
        ds9.cursor_delete(group="group" + cursor)
        ds9.cursor_disp(cu_x, cu_y, 15,
                        group="group" + cursor,
                        label=cursor,
                        color=COLORS[int(cursor)])


def move_cursor(ds9, cursor, args):
    """
    method to move cursors on image. can either move to pixel position or slit position
    :param ds9:
    :param cursor:
    :param args:
    :return:
    """
    if args[0] != "slit":
        cu_x = float(args[0])
        cu_y = float(args[1])
    else:
        Y_SLIT_POS = [float(x) * 1.0 + random.random() * 5. - 2.5 for x in list(range(415, 516, 10))]
        X_SLIT_POS = [(126.5 - 121.5) / (402.5 - 533.5) * (y - 533.5) + 121.5 for y in Y_SLIT_POS]
        cu_x = X_SLIT_POS[int(args[1])]
        cu_y = Y_SLIT_POS[int(args[1])]

    ds9.cursor_delete(group="group" + cursor)
    ds9.cursor_disp(cu_x, cu_y, 15,
                    group="group" + cursor,
                    label=cursor,
                    color=COLORS[int(cursor)])


def parse_coordinates(line: str):
    x_pos = None
    y_pos = None
    words = line.replace("(", ",").split(",")
    try:
        x_pos = float(words[1])
        y_pos = float(words[2])
    except (ValueError, IndexError):
        LOG.error("could not parse line %s to coords", line)
    return x_pos, y_pos


def move_telescope(cursor, args):
    cursor2 = args[0]
    LOG.error("moving telescope from cursor %s to %s", cursor, cursor2)
    with open("Viewer.reg", "r") as file:
        for line in file:
            if "box" in line:
                if "group" + cursor in line:
                    x_pos_1, y_pos_1 = parse_coordinates(line)
                if "group" + cursor2 in line:
                    x_pos_2, y_pos_2 = parse_coordinates(line)
    try:
        x_shift = x_pos_1 - x_pos_2
        y_shift = y_pos_1 - y_pos_2
        LOG.error("x shift: %s, y shift: %s", x_shift, y_shift)
    except (ValueError, UnboundLocalError):
        LOG.error("could not move telescope from cursor %s to cursor %s", cursor, cursor2)


@click.command()
@click.argument("command", default="disp",
                type=click.Choice(['disp', 'save', 'mv', 'mt', 'slit', 'cent', 'info', 'del']),
                nargs=1)
@click.argument("cursor", default="0",  nargs=1)
@click.argument("args", nargs=-1)
def run(command, cursor, args):
    """
    This script controls the viewer cursors
    """
    ds9 = Ds9("Viewer")

    try:
        if command == "disp":
            display_cursor(ds9, cursor)
        elif command == "save":
            ds9.region_save()
        elif command == "mv":
            move_cursor(ds9, cursor, args)
        elif command == "mt":
            move_telescope(cursor, args)
        elif command == "cent":
            ds9.cursor_centroid(group="group" + cursor)
        elif command == "info":
            ds9.cursor_info(group="group" + cursor)
        elif command == "del":
            ds9.cursor_delete(group="group" + cursor)
        ds9.region_save()
    except (ValueError, IndexError, TypeError):
        LOG.warning("Bad Request:\n   Unable to run cursor command\n"
                    "Example valid requests:\n"
                    "   cu [COMMAND] [CURSOR] [ARGS]\n"
                    "   cu disp all\n"
                    "   cu mv 1 500 500\n"
                    "   cu del 5\n"
                    "   cu info 3")

if __name__ == '__main__':
    run()
