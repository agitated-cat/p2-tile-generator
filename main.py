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
edge_color = [165, 165, 165]  # edge color to be generated
edge_width = 2  # width of the edge in pixels

# white specific variables

dot_color = [200, 200, 200]  # color of the dots
dot_size = 2  # size of the dots in pixels
# dot_distance: distance of the dots between each other (like the "grid" between the dots)
dot_distance = 1
dot_edge = True  # whether or not we should draw edges around the dots to make it smoother
dot_edge_color = [220, 220, 220]  # the edge color of the dots
# dot_background_color: color of the dots in the background around edges
dot_background_color = [210, 210, 210]
# dot_background_distance: how many dots from the edge are considered "background dots"
dot_background_distance = 3
# auto-calculated variable that tells how far the dots should spawn from the edges of the tile
dot_edge_distance = round(((tile_size - (edge_width * 2)) %
                          ((dot_size * 2) + (dot_distance * 2))) / 2) + dot_size + dot_distance

print(dot_edge_distance)

# image is square so we only need one size value
size = 512

image = []
normal = []

# generate the perlin noise
noise1 = PerlinNoise(octaves=3, seed=2)
noise2 = PerlinNoise(octaves=6, seed=3)
noise3 = PerlinNoise(octaves=12, seed=4)
noise4 = PerlinNoise(octaves=24, seed=1)

# generate y-coordinates
for i in range(size):
    image.append([])
for i in range(size):
    normal.append([])
x1 = 0
# for every y-coordinate, generate all of the x-coordinates (also default color is the background color we defined)
for x in image:
    for i in range(size):
        # noisevalue = noise1([x1/size, i/size])
        # noisevalue += 0.5 * noise2([x1/size, i/size])
        # noisevalue += 0.25 * noise3([x1/size, i/size])
        # noisevalue += 0.125 * noise4([x1/size, i/size])
        # noisevalue *= background_noise
        # noisevalue = math.floor(noisevalue)
        noisevalue = 0
        x.append(background_color[0] + noisevalue)
        x.append(background_color[1] + noisevalue)
        x.append(background_color[2] + noisevalue)
    x1 += 1

for x in normal:
    for i in range(size):
        x.append(128)
        x.append(128)
        x.append(255)
    x1 += 1

# now, generate the edge of the tiles

vertical_lines = []
vertical_lines_normal_right = []
vertical_lines_normal_left = []

for i in range(0, size, tile_size):
    for w in range(edge_width):
        vertical_lines.append(i + w)
        vertical_lines.append(i + tile_size - 1 - w)

for x in vertical_lines:
    for y in range(size):
        image = setPixel(x, y, edge_color, image)
for x in vertical_lines_normal_right:
    for y in range(size):
        normal = setPixel(x, y, [192, 128, 192], normal)
for x in vertical_lines_normal_left:
    for y in range(size):
        normal = setPixel(x, y, [64, 128, 192], normal)

horizontal_lines = []
horizontal_lines_normal_up = []
horizontal_lines_normal_down = []

for i in range(0, size, tile_size):
    for w in range(edge_width):
        horizontal_lines.append(i + w)
        horizontal_lines.append(i + tile_size - 1 - w)

for x in range(size):
    for y in horizontal_lines:
        image = setPixel(x, y, edge_color, image)

# generate the dots for each tile

odd_dot_lines = []

for i in range(dot_edge_distance + edge_width, tile_size - dot_edge_distance - edge_width, (dot_size * 2) + (dot_distance * 2)):
    for w in range(0, size, tile_size):
        odd_dot_lines.append(i + w)

for x in odd_dot_lines:
    for y in range(dot_edge_distance + edge_width, tile_size - dot_edge_distance - edge_width, (dot_size * 2) + (dot_distance * 2)):
        for w in range(0, size, tile_size):
            for x1 in range(0, dot_size):
                image = setPixel(x + x1, y + w - 1, dot_edge_color, image)
                image = setPixel(x + x1, y + w + dot_size, dot_edge_color, image)
                for y1 in range(0, dot_size):
                    image = setPixel(x + x1, y + y1 + w, dot_color, image)
                    image = setPixel(x - 1, y + y1 + w, dot_edge_color, image)
                    image = setPixel(x + dot_size, y + y1 + w, dot_edge_color, image)

even_dot_lines = []

for i in range(dot_edge_distance + edge_width + dot_size + dot_distance, tile_size - dot_edge_distance - edge_width, (dot_size * 2) + (dot_distance * 2)):
    for w in range(0, size, tile_size):
        even_dot_lines.append(i + w)

for x in even_dot_lines:
    for y in range(dot_edge_distance + edge_width + dot_size + dot_distance, tile_size - dot_edge_distance - edge_width, (dot_size * 2) + (dot_distance * 2)):
        for w in range(0, size, tile_size):
            for x1 in range(0, dot_size):
                image = setPixel(x + x1, y + w - 1, dot_edge_color, image)
                image = setPixel(x + x1, y + w + dot_size, dot_edge_color, image)
                for y1 in range(0, dot_size):
                    image = setPixel(x + x1, y + y1 + w, dot_color, image)
                    image = setPixel(x - 1, y + y1 + w, dot_edge_color, image)
                    image = setPixel(x + dot_size, y + y1 + w, dot_edge_color, image)

        # save image
pngimage = png.from_array(image, "RGB")
pngimage.save("tile.png")

pngnormal = png.from_array(normal, "RGB")
pngnormal.save("normal.png")

print("it worked!!!")
