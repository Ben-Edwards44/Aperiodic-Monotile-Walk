import tile
import pygame
from math import sqrt


VISULISE = __name__ == "__main__"


if VISULISE:
    pygame.init()
    window = pygame.display.set_mode((500, 500))
    pygame.display.set_caption("Numbers Generated from Spectre Tile")


NUM_ITERS = 6


def get_tiles(num_iters):
    tile.main(num_iters)

    return tile.drawn_tiles


def sort_tiles(tiles):
    pos = [get_avg_pos(i) for i in tiles]

    min_x = min([i[0] for i in pos])
    max_x = max([i[0] for i in pos])

    min_y = min([i[1] for i in pos])
    max_y = max([i[1] for i in pos])

    length = len(tiles)

    range_x = length / (max_x - min_x)
    range_y = length / (max_y - min_y)

    tile_inxs = {}
    for i, x in enumerate(tiles):
        pos_x = (pos[i][0] + abs(min_x)) * range_x
        pos_y = (pos[i][1] + abs(min_y)) * range_y

        if pos_x < 0:
            print(pos_x, pos[i][0])

        tile_inxs[x] = (int(pos_x), int(pos_y))

    grid = [[None for _ in range(length + 1)] for _ in range(length + 1)]

    for k, v in tile_inxs.items():
        grid[v[0]][v[1]] = k

    return grid


def get_avg_pos(tile):
    x = 0
    y = 0

    for i in tile.points:
        x += i[0]
        y += i[1]

    n = len(tile.points)

    return x / n, y / n


def pos_nums(tiles):
    nums = []

    for i in tiles:
        pos = get_avg_pos(i)
        num = pos[0] * pos[1]

        nums.append(num)

    return nums


def draw(num_grid):
    for i in range(window.get_width()):
        for x in range(window.get_height()):
            colour = [int(abs(num_grid[i][x])) % 255 for _ in range(3)]

            pygame.draw.circle(window, colour, (i, x), 1)

    pygame.display.update()


def convert_to_grid(nums):
    length = int(sqrt(len(nums)))

    grid = [[None for _ in range(length)] for _ in range(length)]

    for i in range(length):
        for x in range(length):
            inx = i * length + x
            grid[i][x] = nums[inx]

    return grid


def main(num_iters):
    tiles = get_tiles(num_iters)
    nums = pos_nums(tiles)

    if VISULISE:
        grid = convert_to_grid(nums)
        draw(grid)

        while True:
            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    quit()

    return nums


if __name__ == "__main__":
    main(NUM_ITERS)