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
import sys
import atexit
from PIL import Image, ImageDraw
__author__ = "Manmeet Gill"
__contact__ = "contact@manmeetgill.com"
__website__ = "https://manmeetgill.com"
__script__ = "PyHDDKeepAlive"
__version__ = "v0.1"
__git__ = "https://github.com/tf2manu994/PyTree"

# Set defaults
SPREAD = 12  # how much branches spread apart
AAFACTOR = 10  # How much bigger we render for anti-aliasing
FINALHEIGHT = 1000  # the height for the final image
FINALWIDTH = 1000   # the width for the final image
WIDTH = FINALWIDTH * AAFACTOR  # Rendered size
HEIGHT = FINALHEIGHT * AAFACTOR  # Rendered size
MAXDEPTH = 12  # maximum recursion depth
LENGTHFACTOR = 120  # branch length factor
VALIDARGS = False


@atexit.register
def cleanup():
    """
    :rtype: int
    """
    print("Stopping...")
    sys.exit

for argument in sys.argv[1:]:
    # Remove flag markers, we don't need to process those.
    argument = argument.replace("-", "")
    argument = argument.replace("/", "")
    if argument[:6].lower() == "spread":
        SPREAD = int(argument[7:])
        print("Spread set to %s" % SPREAD)
        VALIDARGS = True
    elif argument[:8].lower() == "aafactor":
        AAFACTOR = int(argument[9:])
        print("AA Factor set to %s" % AAFACTOR)
        VALIDARGS = True
    elif argument[:6].lower() == "height":
        FINALHEIGHT = int(argument[7:])
        print("Height set to %s" % HEIGHT)
        VALIDARGS = True
    elif argument[:5].lower() == "width":
        FINALWIDTH = int(argument[6:])
        print("Width set to %s" % WIDTH)
        VALIDARGS = True
    elif argument[:5].lower() == "depth":
        MAXDEPTH = int(argument[6:])
        print("Depth set to %s" % MAXDEPTH)
        VALIDARGS = True
    elif argument[:6].lower() == "length":
        LENGTHFACTOR = int(argument[7:])
        print("Length  set to %s" % LENGTHFACTOR)
        VALIDARGS = True
    elif argument.lower() == help:
        print("Valid Flags - Description - Default")
        print("spread - How far the branches spread apart - 12")
        print("aafactor - The factor at which to render the file - 10")
        print("height - The height of the final file - 1000")
        print("width - The width of the final file - 1000")
        print("depth - How many layers to make the tree - 12")
        print("length - The length of the branches - 120")
    elif argument.lower() == "contact" or "copyright" or "author" or "version":
        print(__author__)
        print(__contact__)
        print(__website__)
        print(__script__, __version__)
        print(__git__)
        print("For help, run with the argument \"help\"")
    else:
        print("No arguments were given, running with defaults")

# Create objects
TREEFILE = Image.new('RGB', (WIDTH, HEIGHT))
DRAW = ImageDraw.Draw(TREEFILE)


def tree(
        xstart: float,  # The x co-ordinate for the start of the line
        ystart: float,  # The y co-ordinate for the start of the line
        angle: int,  # the angle to branch out, in radians
        depth: int  # How far we have to go
):

    """
    :rtype: void
    """
    # If we haven't looped to the limit ...
    if depth > 0:
        # Get the end location of the lines
        xend = xstart + int(math.cos(math.radians(angle)) *
                            depth * LENGTHFACTOR)
        yend = ystart + int(math.sin(math.radians(angle)) *
                            depth * LENGTHFACTOR)
        # Get decimals for to draw based on how far in we are
        (reddec, greendec, bluedec) = colorsys.hsv_to_rgb(float(depth) /
                                                          MAXDEPTH, 1.0, 1.0)
        # Turn them into RGB to draw
        # Yes, I know that rgb is 256 for red.
        # Red makes people angry so I want less of that.
        redhex, greenhex, bluehex = \
            int(200 * reddec),\
            int(255 * greendec),\
            int(255 * bluedec)
        # Actually draw
        DRAW.line([xstart, ystart, xend, yend],
                  (redhex, greenhex, bluehex),
                  depth)
        # Draw the two that branch out from the end of that line.
        tree(
            xend,
            yend,
            angle - SPREAD,
            depth - 1
        )
        tree(
            xend,
            yend,
            angle + SPREAD,
            depth - 1
        )


# Start drawing!
tree(WIDTH / 2,
     HEIGHT,
     -90,
     MAXDEPTH)
TREEFILE = TREEFILE.resize((1000, 1000), Image.ANTIALIAS)
TREEFILE.save("PyTree.png", "PNG")
print("Completed! Saved file PyTree.png in current working directory")
