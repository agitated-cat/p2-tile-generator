import png
import math
from perlin_noise import PerlinNoise


def setPixel(x, y, color, inArray):
    outArray = inArray
    outArray[y][x*3] = color[0]
    outArray[y][x*3+1] = color[1]
    outArray[y][x*3+2] = color[2]
    return outArray

# image generator variables

# these are made for white tiles


tile_size = 128  # how big one tile is

# background_color: background color to start with, everything is drawn on top of this
background_color = [230, 230, 230]
# background_noise: how much the background color deviates from actual value (uses perlin noise) (example, 245 with 10 background_noise could be anywhere from 235-255)
background_noise = 25
edge_color = [145, 145, 145]  # edge color to be generated
edge_width = 2  # width of the edge in pixels

# white specific variables

dot_color = [188, 188, 188]  # color of the dots
dot_size = 2  # size of the dots in pixels
# dot_distance: distance of the dots between each other (like the "grid" between the dots)
dot_distance = 1
dot_edge = True  # whether or not we should draw edges around the dots to make it smoother
dot_edge_color = [226, 226, 226]  # the edge color of the dots

# image is square so we only need one size value
size = 512

image = []

# generate the perlin noise
noise1 = PerlinNoise(octaves=3, seed=258)
noise2 = PerlinNoise(octaves=6, seed=2395)
noise3 = PerlinNoise(octaves=12, seed=7581)
noise4 = PerlinNoise(octaves=24, seed=42069)

# generate y-coordinates
for i in range(size):
    image.append([])
x1 = 0
# for every y-coordinate, generate all of the x-coordinates (also default color is the background color we defined)
for x in image:

    for i in range(size):
        noisevalue = noise1([x1/size, i/size])
        noisevalue += 0.5 * noise2([x1/size, i/size])
        noisevalue += 0.25 * noise3([x1/size, i/size])
        noisevalue += 0.125 * noise4([x1/size, i/size])
        noisevalue *= background_noise
        noisevalue = math.floor(noisevalue)
        # noisevalue = 0
        x.append(background_color[0] + noisevalue)
        x.append(background_color[1] + noisevalue)
        x.append(background_color[2] + noisevalue)
    x1 += 1

# now, generate the edge of the tiles

vertical_lines = []

for i in range(0, size, tile_size):
    for w in range(edge_width):
        vertical_lines.append(i + w)
        vertical_lines.append(i + tile_size - 1 - w)

for x in vertical_lines:
    for y in range(size):
        image = setPixel(x, y, edge_color, image)

horizontal_lines = []

for i in range(0, size, tile_size):
    for w in range(edge_width):
        horizontal_lines.append(i + w)
        horizontal_lines.append(i + tile_size - 1 - w)

for x in range(size):
    for y in horizontal_lines:
        image = setPixel(x, y, edge_color, image)

pngimage = png.from_array(image, "RGB")
pngimage.save("tile.png")

print("it worked!!!")
