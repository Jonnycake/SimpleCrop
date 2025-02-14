#!/usr/bin/env python3
import sys
from argparse import ArgumentParser
from PIL import Image, ImageOps

parser = ArgumentParser()
parser.add_argument("input", help="The input image filepath")
parser.add_argument("width", help="The required size in pixels for the output (e.g. 553)")
parser.add_argument("height", help="The required height in pixels for the output (e.g. 744)")
parser.add_argument("-o", "--output", help="The output image filepath (if none specified, image will be displayed)")
parser.add_argument("-x", "--centering-x", help="The centering X offset from top left (0.0 - 1.0) - default: 0.5 (center)")
parser.add_argument("-y", "--centering-y", help="The centering y offset from top left (0.0 - 1.0) - default: 0.5 (center)")
parser.add_argument('-c', "--contain", help="Constrain the image to the given width and height - ensuring it all fits", action="store_true")
args = parser.parse_args()

try:
    width = int(args.width)
except ValueError:
    print("ERROR: Invalid width specified")
    sys.exit(1)

try:
    height = int(args.height)
except ValueError:
    print("ERROR: Invalid height specified")
    sys.exit(1)

try:
    centering_x = float(args.centering_x)
except TypeError:
    centering_x = 0.5
except ValueError:
    print("WARNING: Invalid value provided for X offset, defaulting to 0.5")
    centering_x = 0.5

if centering_x < 0.0 or centering_x > 1.0:
    centering_x = max(0.0, min(centering_x, 1.0))
    print("WARNING: X offset is outside valid range, clamping to: ", centering_x)


try:
    centering_y = float(args.centering_y)
except TypeError:
    centering_y = 0.5
except ValueError:
    print("WARNING: Invalid value provided for Y offset, defaulting to 0.5")
    centering_y = 0.5

if centering_y < 0.0 or centering_y > 1.0:
    centering_y = max(0.0, min(centering_y, 1.0))
    print("WARNING: Y offset is outside valid range, clamping to: ", centering_y)

print(centering_x, centering_y, args.input, args.output)

with Image.open(args.input) as im:
    if not args.contain:
        temp_im = ImageOps.fit(im, (width, height), centering=(centering_x, centering_y))
    else:
        temp_im = ImageOps.contain(im, (width, height))


    if args.output:
        temp_im.save(args.output)
    else:
        temp_im.show()
