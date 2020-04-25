import logging

from PIL import Image, ImageDraw

# Cannot read DAT yet, need to hard-code colors
terrain_colors = {
    0: (127, 139, 55, 255),  # Grass
    1: (63, 95, 159, 255),  # Shallow water
    2: (255, 179, 43, 255),  # Coastline
    6: (207, 163, 67, 255),  # Desert
    20: (55, 95, 39, 255),  # Some kind of forest
    13: (163, 115, 79, 255),  # Dirt
    10: (55, 95, 39, 255),  # Some other kind of forest
    22: (39, 63, 143, 255)  # Deep water
}

# 8 player colors
minmap_player_colors = [(255, 255, 255, 255),
                        (7, 15, 103, 255),
                        (255, 0, 0, 255),
                        (254, 254, 0, 255),
                        (95, 51, 27, 255),
                        (239, 99, 7, 255),
                        (0, 211, 39, 255),
                        (143, 143, 143, 255),
                        (0, 171, 147, 255)]

# Colors for each terrain type in the minimap
minimap_terrain_colors = {
    0: {
        'name': 'Grass',
        'color': ((127, 139, 55, 255),(99, 123, 47, 255), (75, 107, 43, 255)),
        'cliff': ((35, 0, 0, 255), (219, 219, 243, 255))
    },
    1: {
        'name': 'Water',
        'color': ((87, 123, 179, 255),(63, 95, 159, 255), (39, 63, 143, 255)),
        'cliff': ((95, 67, 55, 255), (103, 75, 63, 255))
    },
    2: {
        'name': 'Beach',
        'color': ((255, 195, 111, 255),(255, 179, 43, 255), (251, 159, 31, 255)),
        'cliff': ((255, 239, 219, 255), (15, 15, 15, 255))
    },
    3: {
        'name': 'Thin River',
        'color': ( (87, 123, 179, 255),(63, 95, 159, 255), (39, 63, 143, 255)),
        'cliff': ((95, 67, 55, 255), (103, 75, 63, 255))
    },
    4: {
        'name': 'Shallows',
        'color': ((147, 187, 215, 255),(115, 155, 199, 255), (87, 123, 179, 255)),
        'cliff': ((95, 67, 55, 255), (103, 75, 63, 255))
    },
    5: {
        'name': 'Jungle Edge',
        'color': ( (75, 107, 43, 255),(55, 95, 39, 255), (27, 67, 27, 255)),
        'cliff': ((0, 131, 123, 255), (0, 131, 123, 255))
    },
    6: {
        'name': 'Desert',
        'color': ((231, 191, 95, 255),(207, 163, 67, 255), (183, 139, 43, 255)),
        'cliff': ((255, 239, 219, 255), (15, 15, 15, 255))
    },
    7: {
        'name': 'Crop',
        'color': ((203, 151, 111, 255),(151, 111, 79, 255), (127, 95, 67, 255)),
        'cliff': ((255, 0, 0, 255), (255, 0, 47, 255))
    },
    8: {
        'name': 'Rows',
        'color': ((203, 151, 111, 255),(151, 111, 79, 255), (127, 95, 67, 255)),
        'cliff': ((255, 0, 0, 255), (255, 0, 47, 255))
    },
    9: {
        'name': 'Wheat',
        'color': ( (167, 131, 35, 255),(135, 103, 39, 255), (107, 75, 39, 255)),
        'cliff': ((243, 227, 195, 255), (243, 235, 215, 255))
    },
    10: {
        'name': 'Forest',
        'color': ((55, 95, 39, 255),(39, 79, 31, 255), (27, 67, 27, 255)),
        'cliff': ((0, 79, 79, 255), (0, 131, 123, 255))
    },
    11: {
        'name': 'Dirt',
        'color': ((231, 191, 95, 255),(207, 163, 67, 255), (183, 139, 43, 255)),
        'cliff': ((255, 239, 219, 255), (15, 15, 15, 255))
    },
    12: {
        'name': 'Grass 2',
        'color': ((127, 139, 55, 255),(99, 123, 47, 255), (75, 107, 43, 255)),
        'cliff': ((35, 0, 0, 255), (219, 219, 243, 255))
    },
    13: {
        'name': 'Desert Palm',
        'color': ((207, 163, 67, 255),(183, 139, 43, 255), (163, 115, 79, 255)),
        'cliff': ((255, 239, 219, 255), (15, 15, 15, 255))
    },
    14: {
        'name': 'Desert Impass',
        'color': ((231, 191, 95, 255),(207, 163, 67, 255), (183, 139, 43, 255)),
        'cliff': ((255, 239, 219, 255), (15, 15, 15, 255))
    },
    15: {
        'name': 'Water Impass',
        'color': ((87, 123, 179, 255),(63, 95, 159, 255), (39, 63, 143, 255)),
        'cliff': ((95, 67, 55, 255), (103, 75, 63, 255))
    },
    16: {
        'name': 'Grass Impass',
        'color': ((127, 139, 55, 255),(99, 123, 47, 255), (75, 107, 43, 255)),
        'cliff': ((35, 0, 0, 255), (219, 219, 243, 255))
    },
    17: {
        'name': 'Fog',
        'color': ((0, 0, 0, 255),(0, 0, 0, 255), (0, 0, 0, 255)),
        'cliff': ((0, 0, 0, 255), (0, 0, 0, 255))
    },
    18: {
        'name': 'Forest Edge',
        'color': ((75, 107, 43, 255),(55, 95, 39, 255), (39, 79, 31, 255)),
        'cliff': ((0, 131, 123, 255), (0, 131, 123, 255))
    },
    19: {
        'name': 'Pine forest',
        'color': ((55, 95, 39, 255),(39, 79, 31, 255), (27, 67, 27, 255)),
        'cliff': ((0, 79, 79, 255), (0, 131, 123, 255))
    },
    20: {
        'name': 'Jungle',
        'color': ((127, 139, 55, 255),(39, 79, 31, 255), (75, 107, 43, 255)),
        'cliff': ((35, 0, 0, 255), (219, 219, 243, 255))
    },
    21: {
        'name': 'Pine edge',
        'color': ((75, 107, 43, 255),(55, 95, 39, 255), (39, 79, 31, 255)),
        'cliff': ((0, 131, 123, 255), (0, 131, 123, 255))
    },
    22: {
        'name': 'Deep water',
        'color': ((39, 63, 143, 255),(23, 39, 123, 255), (7, 15, 103, 255)),
        'cliff': ((95, 67, 55, 255), (103, 75, 63, 255))
    }
}

minimap_object_colors = {
    66: (223, 207, 15, 255),  # Gold mine
    102: (199, 199, 199, 255),  # Stone mine
    264: (135, 103, 39, 255),  # (231, 191, 95),  # Cliffs
    65: (155, 183, 111, 255)  # Gazelle
}


minimap_object_hide = [
    162, # Double flag
    330 # Flag
]


def lightfilter(xy, tiles, width):
    my_depth = depth_of(xy[0], xy[1], tiles, width, 0)
    top_depth = depth_of(xy[0], xy[1] - 1, tiles, width, my_depth)
    left_depth = depth_of(xy[0] - 1, xy[1], tiles, width, my_depth)
    right_depth = depth_of(xy[0] + 1, xy[1], tiles, width, my_depth)
    bottom_depth = depth_of(xy[0], xy[1] + 1, tiles, width, my_depth)

    if my_depth < top_depth or my_depth > bottom_depth:
        return 0
    if my_depth != top_depth or my_depth != left_depth or my_depth != right_depth:
        return 2
    return 1


def depth_of(x, y, tiles, width, default):
    if x < 0 or x >= width:
        return default
    if y < 0 or y >= (len(tiles) // width):
        return default
    return tiles[width * y + x].elevation


def draw(scenario):
    map = scenario['map_scen']
    outp = Image.new('RGBA', (map.width, map.height), (255, 255, 255, 0))
    draw = ImageDraw.Draw(outp)
    width = map.width
    unknown_colors = {}
    for i in range(0, len(map.tiles)):
        tile = map.tiles[i]
        x = i % width
        y = i // width
        if tile.terrain in minimap_terrain_colors:
            idx = lightfilter((x, y), map.tiles, width);
            color = minimap_terrain_colors[tile.terrain]['color'][idx]
        else:
            unknown_colors[tile.terrain] = True
            color = (0, 0, 0, 255)
        draw.point((x, y), color)

    # Gaia objects (only resources & cliffs are drawn)
    if len(scenario['objects']) > 0:
        for obj in scenario['objects'][0]:
            id = 264 if (264 <= obj.type_id <= 273) else obj.type_id
            x = int(obj.position[0])
            y = int(obj.position[1])
            if id in minimap_object_colors:
                color = minimap_object_colors[id]
                draw.ellipse([(x - 1, y - 1), (x + 1, y + 1)], color)

    # Regular player objects
    for i in range(1, len(scenario['objects'])):
        for obj in scenario['objects'][i]:
            if obj.type_id in minimap_object_hide:
                continue
            color = minmap_player_colors[i]
            x = int(obj.position[0])
            y = int(obj.position[1])
            draw.ellipse([(x - 1, y - 1), (x + 1, y + 1)], color)

    for y in sorted(unknown_colors.keys()):
        logging.info("Terrain ID %d not known", y)

    return outp.resize((1000, 1000)).rotate(45, expand=True)
