import pygame
import numpy
import math


SHOW_TILES = __name__ == "__main__"


if SHOW_TILES:
    pygame.init()
    window = pygame.display.set_mode((500, 500))


NUM_ITERS = 2
IDENTITY = [1, 0, 0, 0, 1, 0]
TILE_NAMES = ["Gamma", "Delta", "Theta", "Lambda", "Xi", "Pi", "Sigma", "Phi", "Psi"]

SPECTRE_POINTS = [
    (0, 0),
    (1.0, 0.0),
    (1.5, -math.sqrt(3) / 2),
    (1.5 + math.sqrt(3) / 2, 0.5 - math.sqrt(3) / 2),
    (1.5 + math.sqrt(3) / 2, 1.5 - math.sqrt(3) / 2),
    (2.5 + math.sqrt(3) / 2, 1.5 - math.sqrt(3) / 2),
    (3 + math.sqrt(3) / 2, 1.5),
    (3.0, 2.0),
    (3 - math.sqrt(3) / 2, 1.5),
    (2.5 - math.sqrt(3) / 2, 1.5 + math.sqrt(3) / 2),
    (1.5 - math.sqrt(3) / 2, 1.5 + math.sqrt(3) / 2),
    (0.5 - math.sqrt(3) / 2, 1.5 + math.sqrt(3) / 2),
    (-math.sqrt(3) / 2, 1.5),
    (0.0, 1.0)
]


COLOURS = {
    "Gamma" : (255, 255, 255),
    "Gamma1" : (255, 255, 255),
    "Gamma2" : (255, 255, 255),
    "Delta" : (220, 220, 220),
    "Theta" : (255, 191, 191),
    "Lambda" : (255, 160, 122),
    "Xi" : (255, 242, 0),
    "Pi" : (135, 206, 250),
    "Sigma" : (245, 245, 220),
    "Phi" : (0, 255, 0),
    "Psi" : (0, 255, 255)
}


drawn_tiles = []


class Tile:
    def __init__(self, points, label):
        self.points = points
        self.quad = [points[3], points[5], points[7], points[11]]

        self.label = label
        self.colour = COLOURS[label]

    def transform_points(self, transformation_matrix):  
        new_points = [transform_point(transformation_matrix, i) for i in SPECTRE_POINTS]
        self.points = [i for i in new_points]

    def draw(self, trans_matrix):
        global drawn_tiles

        self.transform_points(trans_matrix)
    
        if SHOW_TILES:
            draw_tile(self)

        obj_copy = Tile(self.points, self.label)
        drawn_tiles.append(obj_copy)


class MetaTile:
    def __init__(self, geometries, quad):
        self.geometries = geometries
        self.quad = quad

    def draw(self, metatile_trans_matrix):
        for tile, trans in self.geometries:
            tile.draw(mat_mul(metatile_trans_matrix, trans))


def mat_mul(a, b):
    return [
        a[0]*b[0] + a[1]*b[3],
        a[0]*b[1] + a[1]*b[4],
        a[0]*b[2] + a[1]*b[5] + a[2],

        a[3]*b[0] + a[4]*b[3],
        a[3]*b[1] + a[4]*b[4],
        a[3]*b[2] + a[4]*b[5] + a[5]
    ]


def rotate(angle):
    cos = numpy.cos(angle)
    sin = numpy.sin(angle)

    return [cos, -sin, 0, sin, cos, 0]


translate = lambda x, y: [1, 0, x, 0, 1, y]
translate_to = lambda start, end: translate(end[0] - start[0], end[1] - start[1])
transform_point = lambda matrix, point: (matrix[0] * point[0] + matrix[1] * point[1] + matrix[2], matrix[3] * point[0] + matrix[4] * point[1] + matrix[5])


def draw_tile(tile):
    points = [[x * 8 + 250 for x in i] for i in tile.points]
    pygame.draw.polygon(window, tile.colour, points)


def build_spectre_base():
    base_cluster = { label: Tile(SPECTRE_POINTS, label) for label in TILE_NAMES if label != "Gamma" }

    mystic = MetaTile(
        [
            [Tile(SPECTRE_POINTS, "Gamma1"), IDENTITY],
            [Tile(SPECTRE_POINTS, "Gamma2"), mat_mul(translate(SPECTRE_POINTS[8][0], SPECTRE_POINTS[8][1]), rotate(math.pi / 6))]
        ],
        [SPECTRE_POINTS[3], SPECTRE_POINTS[5], SPECTRE_POINTS[7], SPECTRE_POINTS[11]]
    )

    base_cluster["Gamma"] = mystic

    return base_cluster


def build_supertiles(tiles):
    quad = tiles["Delta"].quad
    R = [-1, 0, 0, 0, 1, 0]

    transformation_rules = [
        [60, 3, 1], [0, 2, 0], [60, 3, 1], [60, 3, 1],
        [0, 2, 0], [60, 3, 1], [-120, 3, 3]
    ]

    transformations = [IDENTITY]
    total_angle = 0
    rotation = IDENTITY
    transformed_quad = list(quad)

    for ang, start_point, end_point in transformation_rules:
        if ang != 0:
            total_angle += ang
            rotation = rotate(numpy.deg2rad(total_angle))
            transformed_quad = [transform_point(rotation, quad_pt) for quad_pt in quad]

        ttt = translate_to(
            transformed_quad[end_point],
            transform_point(transformations[-1], quad[start_point])
        )
        transformations.append(mat_mul(ttt, rotation))

    transformations = [mat_mul(R, transformation) for transformation in transformations]

    super_rules = {
        "Gamma":  ["Pi",  "Delta", None,  "Theta", "Sigma", "Xi",  "Phi",    "Gamma"],
        "Delta":  ["Xi",  "Delta", "Xi",  "Phi",   "Sigma", "Pi",  "Phi",    "Gamma"],
        "Theta":  ["Psi", "Delta", "Pi",  "Phi",   "Sigma", "Pi",  "Phi",    "Gamma"],
        "Lambda": ["Psi", "Delta", "Xi",  "Phi",   "Sigma", "Pi",  "Phi",    "Gamma"],
        "Xi":     ["Psi", "Delta", "Pi",  "Phi",   "Sigma", "Psi", "Phi",    "Gamma"],
        "Pi":     ["Psi", "Delta", "Xi",  "Phi",   "Sigma", "Psi", "Phi",    "Gamma"],
        "Sigma":  ["Xi",  "Delta", "Xi",  "Phi",   "Sigma", "Pi",  "Lambda", "Gamma"],
        "Phi":    ["Psi", "Delta", "Psi", "Phi",   "Sigma", "Pi",  "Phi",    "Gamma"],
        "Psi":    ["Psi", "Delta", "Psi", "Phi",   "Sigma", "Psi", "Phi",    "Gamma"]
    }
    super_quad = [
        transform_point(transformations[6], quad[2]),
        transform_point(transformations[5], quad[1]),
        transform_point(transformations[3], quad[2]),
        transform_point(transformations[0], quad[1])
    ]

    return {
        label: MetaTile(
            [ [tiles[substitution], transformation] for substitution, transformation in zip(substitutions, transformations) if substitution ],
            super_quad
        ) for label, substitutions in super_rules.items() }


def main(num_iters):
    tiles = build_spectre_base()

    for _ in range(num_iters):
        tiles = build_supertiles(tiles)

    tiles["Delta"].draw(IDENTITY)

    if SHOW_TILES:
        pygame.display.update()

        while True:
            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    quit()

    return tiles


if __name__ == "__main__":
    main(NUM_ITERS)