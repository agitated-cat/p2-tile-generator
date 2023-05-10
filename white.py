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

# image generator variables

# these are made for white tiles


tile_size = 128  # how big one tile is

# background_color: background color to start with, everything is drawn on top of this
background_color = [230, 230, 230]
# background_noise: how much the background color deviates from actual value (uses perlin noise) (example, 245 with 10 background_noise could be anywhere from 235-255)
edge_color = [165, 165, 165]  # edge color to be generated
edge_width = 2  # width of the edge in pixels

# white specific variables

dot_color = [200, 200, 200]  # color of the dots
dot_size = 2  # size of the dots in pixels
# dot_distance: distance of the dots between each other (like the "grid" between the dots)
dot_distance = 1
dot_edge = True  # whether or not we should draw edges around the dots to make it smoother
dot_edge_color = [225, 225, 225]  # the edge color of the dots
# dot_background_color: color of the dots in the background around edges
dot_background_color = [220, 220, 220]
# dot_background_distance: how many dots from the edge are considered "background dots"
dot_background_distance = 1
# auto-calculated variable that tells how far the dots should spawn from the edges of the tile
dot_edge_distance = round(((tile_size - (edge_width * 2)) %
                          ((dot_size * 2) + (dot_distance * 2))) / 2) + dot_size + dot_distance

print(dot_edge_distance)

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

# generate the dots for each tile

odd_dot_lines = []

for i in range(dot_edge_distance + edge_width, tile_size - dot_edge_distance - edge_width, (dot_size * 2) + (dot_distance * 2)):
    for w in range(0, size, tile_size):
        odd_dot_lines.append(i + w)


ix = 1
iy = 1
for x in odd_dot_lines:
    iy = 1
    for y in range(dot_edge_distance + edge_width, tile_size - dot_edge_distance - edge_width, (dot_size * 2) + (dot_distance * 2)):
        for w in range(0, size, tile_size):
            # rand_dot_color = math.floor(dot_color_random * noisedots([x/size, y/size]))
            rand_dot_color = 0
            background_color_bool_x = dot_background_distance * num_tiles < ix and ix <= len(odd_dot_lines) - (dot_background_distance * num_tiles)
            background_color_bool_y = dot_background_distance * num_tiles < iy and iy <= len(odd_dot_lines) - (dot_background_distance * num_tiles)
            new_dot_color = []
            if (background_color_bool_y and background_color_bool_x):
                new_dot_color = [dot_color[0] + rand_dot_color, dot_color[1] + rand_dot_color, dot_color[2] + rand_dot_color]
            else:
                new_dot_color = [dot_background_color[0] + rand_dot_color, dot_background_color[1] + rand_dot_color, dot_background_color[2] + rand_dot_color]
            for x1 in range(0, dot_size):
                image = setPixel(x + x1, y + w - 1, dot_edge_color, image) # top part of dot edge
                image = setPixel(x + x1, y + w + dot_size, dot_edge_color, image) # bottom part of dot edge

                normal = setPixel(x + x1, y + w - 1, [128, 96, 224], normal) # top part of dot edge normal
                normal = setPixel(x + x1, y + w + dot_size, [128, 160, 224], normal) # bottom part of dot edge normal
                for y1 in range(0, dot_size):
                    image = setPixel(x + x1, y + y1 + w, new_dot_color, image)
                    image = setPixel(x - 1, y + y1 + w, dot_edge_color, image) # left part of dot edge
                    image = setPixel(x + dot_size, y + y1 + w, dot_edge_color, image) # right part of dot edge

                    normal = setPixel(x - 1, y + y1 + w, [160, 128, 224], normal) # left part of dot edge normal
                    normal = setPixel(x + dot_size, y + y1 + w, [96, 128, 224], normal) # right part of dot edge normal
            iy += 1
    ix += 1

even_dot_lines = []

for i in range(dot_edge_distance + edge_width + dot_size + dot_distance, tile_size - dot_edge_distance - edge_width, (dot_size * 2) + (dot_distance * 2)):
    for w in range(0, size, tile_size):
        even_dot_lines.append(i + w)

ix = 1
iy = 1
for x in even_dot_lines:
    iy = 1
    for y in range(dot_edge_distance + edge_width + dot_size + dot_distance, tile_size - dot_edge_distance - edge_width, (dot_size * 2) + (dot_distance * 2)):
        for w in range(0, size, tile_size):
            # rand_dot_color = math.floor(dot_color_random * noisedots([x/size, y/size]))
            rand_dot_color = 0
            new_dot_color = []
            background_color_bool_x = dot_background_distance * num_tiles < ix and ix <= len(even_dot_lines) - (dot_background_distance * num_tiles)
            background_color_bool_y = dot_background_distance * num_tiles < iy and iy <= len(even_dot_lines) - (dot_background_distance * num_tiles)
            if (background_color_bool_y and background_color_bool_x):
                new_dot_color = [dot_color[0] + rand_dot_color, dot_color[1] + rand_dot_color, dot_color[2] + rand_dot_color]
            else:
                new_dot_color = [dot_background_color[0] + rand_dot_color, dot_background_color[1] + rand_dot_color, dot_background_color[2] + rand_dot_color]
            for x1 in range(0, dot_size):
                image = setPixel(x + x1, y + w - 1, dot_edge_color, image)
                image = setPixel(x + x1, y + w + dot_size, dot_edge_color, image)

                normal = setPixel(x + x1, y + w - 1, [128, 96, 224], normal) # top part of dot edge normal
                normal = setPixel(x + x1, y + w + dot_size, [128, 160, 224], normal) # bottom part of dot edge normal
                for y1 in range(0, dot_size):
                    image = setPixel(x + x1, y + y1 + w, new_dot_color, image)
                    image = setPixel(x - 1, y + y1 + w, dot_edge_color, image)
                    image = setPixel(x + dot_size, y + y1 + w, dot_edge_color, image)

                    normal = setPixel(x - 1, y + y1 + w, [160, 128, 224], normal) # left part of dot edge normal
                    normal = setPixel(x + dot_size, y + y1 + w, [96, 128, 224], normal) # right part of dot edge normal
            iy += 1
    ix += 1

# save image
pngimage = png.from_array(image, "RGB")
pngimage.save("tile.png")

pngnormal = png.from_array(normal, "RGB")
pngnormal.save("normal.png")

pngssbump = png.from_array(ssbump, "RGB")
pngssbump.save("ssbump.png")

print("it worked!!!")

print(num_tiles)