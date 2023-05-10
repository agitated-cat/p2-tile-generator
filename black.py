import png
import math
import random
import noise

def setPixel(x, y, color, inArray):
    outArray = inArray
    outArray[y][x*3] = color[0]
    outArray[y][x*3+1] = color[1]
    outArray[y][x*3+2] = color[2]
    return outArray

def lerpColor(color1, color2, lerpamount):
    outcolor = [0, 0, 0]
    colordistance = [0.0, 0.0, 0.0]
    colordistance[0] = color1[0] - color2[0]
    colordistance[1] = color1[1] - color2[1]
    colordistance[2] = color1[2] - color2[2]
    outcolor[0] = round(color1[0] - (colordistance[0] * lerpamount))
    outcolor[1] = round(color1[1] - (colordistance[1] * lerpamount))
    outcolor[2] = round(color1[2] - (colordistance[2] * lerpamount))
    return outcolor

# image generator variables

# these are made for white tiles


tile_size = 128  # how big one tile is

# background_color: background color to start with, everything is drawn on top of this
background_color = [55, 55, 55]
# background_noise: how much the background color deviates from actual value (uses perlin noise) (example, 245 with 10 background_noise could be anywhere from 235-255)
edge_color = [115, 115, 115]  # edge color to be generated
# 115 115 115, 25 25 25
edge_width = 2  # width of the edge in pixels

# total amount of stripes in the image
stripes = 16
# width of stripes in pixels, should be less than size / stripes
stripe_width = 24
stripe_color = [61, 61, 61]

# image is square so we only need one size value
size = 512
num_tiles = round(size / tile_size)

image = []
normal = []
ssbump = []

# generate y-coordinates
for i in range(size):
    image.append([])
for i in range(size):
    normal.append([])
for i in range(size):
    ssbump.append([])

# for every y-coordinate, generate all of the x-coordinates (also default color is the background color we defined)
for x in image:
    for i in range(size):
        x.append(background_color[0])
        x.append(background_color[1])
        x.append(background_color[2])

for x in normal:
    for i in range(size):
        x.append(128)
        x.append(128)
        x.append(255)

for x in ssbump:
    for i in range(size):
        x.append(89)
        x.append(89)
        x.append(89)

# generate da stripes

stripe_lines = []

if (stripes != 0):
    offset = size / (stripes)
    print(offset)

    count = 0

    while (count < size):
        stripe_lines.append(round((offset + count) - (offset / 2) - (stripe_width / 2)))
        count += offset

    print(stripe_lines)

    for x in stripe_lines:
        for y in range(size):
            for w in range(stripe_width):
                image = setPixel(x + w, y, stripe_color, image)

    for x in stripe_lines:
        for y in range(size):
            if (edge_width < (y % tile_size) < tile_size - edge_width - 1):
                for w in range(stripe_width):
                    normal = setPixel(x + w, y, lerpColor([96, 128, 224], [160, 128, 224], (w / stripe_width)), normal)

# now, generate the edge of the tiles

vertical_lines = []
vertical_lines_normal_right = []
vertical_lines_normal_left = []

for i in range(0, size, tile_size):
    for w in range(edge_width):
        vertical_lines_normal_right.append(i + tile_size + w - edge_width - 1)
        vertical_lines_normal_left.append(i + edge_width - w)
        vertical_lines.append(i + w)
        vertical_lines.append(i + tile_size - 1 - w)

for x in vertical_lines:
    for y in range(size):
        image = setPixel(x, y, edge_color, image)
for x in vertical_lines_normal_right:
    for y in range(size):
        if (edge_width < (y % tile_size) < tile_size - edge_width - 1):
            normal = setPixel(x, y, [192, 128, 192], normal)
            ssbump = setPixel(x, y, [179, 0, 0], ssbump)
for x in vertical_lines_normal_left:
    for y in range(size):
        if (edge_width < (y % tile_size) < tile_size - edge_width - 1):
            normal = setPixel(x, y, [64, 128, 192], normal)
            ssbump = setPixel(x, y, [0, 179, 179], ssbump)

horizontal_lines = []
horizontal_lines_normal_up = []
horizontal_lines_normal_down = []

for i in range(0, size, tile_size):
    for w in range(edge_width):
        horizontal_lines_normal_down.append(i + tile_size + w - edge_width - 1)
        horizontal_lines_normal_up.append(i + edge_width - w)
        horizontal_lines.append(i + w)
        horizontal_lines.append(i + tile_size - 1 - w)

for x in range(size):
    for y in horizontal_lines:
        image = setPixel(x, y, edge_color, image)

for x in range(size):
    for y in horizontal_lines_normal_down:
        if (edge_width < (x % tile_size) < tile_size - edge_width - 1):
            normal = setPixel(x, y, [128, 64, 192], normal)
            ssbump = setPixel(x, y, [89, 179, 0], ssbump)

for x in range(size):
    for y in horizontal_lines_normal_up:
        if (edge_width < (x % tile_size) < tile_size - edge_width - 1):
            normal = setPixel(x, y, [128, 192, 192], normal)
            ssbump = setPixel(x, y, [89, 0, 179], ssbump)

# save image
pngimage = png.from_array(image, "RGB")
pngimage.save("tile.png")

pngnormal = png.from_array(normal, "RGB")
pngnormal.save("normal.png")

pngssbump = png.from_array(ssbump, "RGB")
pngssbump.save("ssbump.png")

print("it worked!!!")

print(num_tiles)