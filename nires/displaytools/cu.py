#!/usr/bin/env python
# Control the cursors on the NIRES viewer ds9 window

import sys
from nires.displaytools.ds9 import Ds9

argc = len(sys.argv)

if argc == 1:
    sys.exit()

color = ["white",
         "yellow",
         "cyan",
         "blue",
         "magenta",
         "green",
         "orange",
         "red",
         "brown",
         "black"]

cu_number = sys.argv[1]

ds9 = Ds9("Viewer")

if cu_number.lower() == 'all':
    ds9.cursor_delete(group="all")
    if argc == 2:
        for i in range(10):
            ds9.cursor_disp(540 + i * 50, 600, 15, group="group" + str(i), label=str(i), color=color[i])
    sys.exit()

if cu_number.lower() == 'save':
    if argc == 3:
        region_file = sys.argv[2]
    else:
        region_file = 'ds9.reg'
    ds9.region_save(region_file)

if argc == 3:
    command = sys.argv[2]
    if command.lower() == 'del':
        ds9.cursor_delete(group="group" + cu_number)
    elif command.lower() == 'cent':
        ds9.cursor_centroid(group="group" + cu_number)
    elif command.lower() == 'info':
        ds9.cursor_info(group="group" + cu_number)
    sys.exit()

if argc == 2:
    cu_x = 540 + int(cu_number) * 50
    cu_y = 600
if argc >= 4:
    cu_x = sys.argv[2]
    cu_y = float(sys.argv[3])
    if cu_x == 'slit':
        slitpos_x = [475, 485, 495, 505, 515, 525, 535, 545, 555, 565]
        cu_x = slitpos_x[int(cu_y) - 1]
        cu_y = 915
    else:
        cu_x = float(cu_x)

ds9.cursor_delete(group="group" + cu_number)
ds9.cursor_disp(cu_x, cu_y, 15, group="group" + cu_number, color=color[int(cu_number)], label=cu_number)
