#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
PyTree v0.1 by Manmeet Gill
© Manmeet Gill 2016
https://manmeetgill.com
contact@manmeetgill.com
https://github.com/tf2manu994/PyTree
"""
import colorsys
import math
from PIL import Image, ImageDraw
from typing import Iterator

__author__ = "Manmeet Gill"
__contact__ = "contact@manmeetgill.com"
__website__ = "https://manmeetgill.com"
__script__ = "PyHDDKeepAlive"
__version__ = "v0.1"
__git__ = "https://github.com/tf2manu994/PyTree"

# Set variables
# TODO: make these set by command line arguments
SPREAD = 12  # how much branches spread apart
AAFACTOR = 10  # How much bigger we render for anti-aliasing
FINALHEIGHT = 1000  # the height for the final image
FINALWIDTH = 1000   # the width for the final image
WIDTH = FINALWIDTH * AAFACTOR  # Rendered size
HEIGHT = FINALHEIGHT * AAFACTOR  # Rendered size
FINALHEIGHT = 1000  # the height for the final image
FINALWIDTH = 1000   # the width for the final image
MAXDEPTH = 12  # maximum recursion depth
LENGTHFACTOR = 120  # branch length factor

# Create objects
TREEFILE = Image.new('RGB', (WIDTH, HEIGHT))
DRAW = ImageDraw.Draw(TREEFILE)


def tree(xstart: int,  # The x co-ordinate for the start of the line
         ystart: int,  # The y co-ordinate for the start of the line
         angle: int,  # the angle to branch out, in radians
         depth: int  # How far we have to go
        ) -> Iterator[int]:
    # If we haven't looped to the limit ...
    if depth > 0:
        # Get the end location of the lines
        xend = xstart + int(math.cos(math.radians(angle)) * depth * LENGTHFACTOR)
        yend = ystart + int(math.sin(math.radians(angle)) * depth * LENGTHFACTOR)
        # Get decimals for to draw based on how far in we are
        (reddec, greendec, bluedec) = colorsys.hsv_to_rgb(float(depth) / MAXDEPTH, 1.0, 1.0)
        # Turn them into RGB to draw
        # Yes, I know that rgb is 256 for red.
        # Red makes people angry so I want less of that.
        redhex, greenhex, bluehex = int(200 * reddec), int(255 * greendec), int(255 * bluedec)
        # Actually draw
        DRAW.line([xstart, ystart, xend, yend], (redhex, greenhex, bluehex), depth)
        # Draw the two that branch out from the end of that line.
        tree(xend, yend, angle - SPREAD, depth - 1)
        tree(xend, yend, angle + SPREAD, depth - 1)


# Start drawing!
tree(WIDTH / 2, HEIGHT, -90, MAXDEPTH)
TREEFILE = TREEFILE.resize((1000, 1000), Image.ANTIALIAS)
TREEFILE.save("PyTree.png", "PNG")
