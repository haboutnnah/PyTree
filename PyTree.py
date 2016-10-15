import colorsys
import math
from PIL import Image, ImageDraw

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
treefile = Image.new('RGB', (WIDTH, HEIGHT))
draw = ImageDraw.Draw(treefile)


def tree(x1: int,  # The x co-ordinate for the start of the line
         y1: int,  # The y co-ordinate for the start of the line
         angle: int,  # the angle to branch out, in radians
         depth: int  # How far we have to go
         ) -> int:
    # If we haven't looped to the limit ...
    if depth > 0:
        # Get the end location of the lines
        x2 = x1 + int(math.cos(math.radians(angle)) * depth * LENGTHFACTOR)
        y2 = y1 + int(math.sin(math.radians(angle)) * depth * LENGTHFACTOR)
        # Get decimals for to draw based on how far in we are
        (r, g, b) = colorsys.hsv_to_rgb(float(depth) / MAXDEPTH, 1.0, 1.0)
        # Turn them into RGB to draw
            # Yes, I know that rgb is 256 for red.
            # Red makes people angry so I want less of that.
        red, green, blue = int(200 * r), int(255 * g), int(255 * b)
        # Actually draw
        draw.line([x1, y1, x2, y2], (red, green, blue), depth)
        # Draw the two that branch out from the end of that line.
        tree(x2, y2, angle - SPREAD, depth - 1)
        tree(x2, y2, angle + SPREAD, depth - 1)


# Start drawing!
tree(WIDTH / 2, HEIGHT, -90, MAXDEPTH)
treefile = treefile.resize((1000, 1000), Image.ANTIALIAS)
treefile.save("PyTree.png", "PNG")
