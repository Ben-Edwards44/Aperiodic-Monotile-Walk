import pygame
import num_generate
import math


#Set to True to see the lines as they are drawn
SHOW_LINE_DRAWS = False
SHOW_TEXT = False

NUM_ITERS = 5
LENGTH = 3.4
COLOURS = ((38, 70, 83), (42, 157, 143), (233, 196, 106), (244, 162, 97), (231, 111, 81))

START_X = 400
START_Y = 100


pygame.init()
window = pygame.display.set_mode((1000, 800))
font = pygame.font.Font(None, 32)
pygame.display.set_caption("Random Walk")


current_colour = 0


def walk(start_x, start_y, angle):
    rad = math.radians(angle)

    new_x = start_x + LENGTH * math.cos(rad)
    new_y = start_y + LENGTH * math.sin(rad)

    return new_x, new_y


def draw_line(x1, y1, x2, y2, colour_inx):
    colour_inx = int(colour_inx / 360 * len(COLOURS))

    pygame.draw.line(window, COLOURS[colour_inx], (x1, y1), (x2, y2))

    if SHOW_LINE_DRAWS:
        pygame.display.update()


def nums_text(num):
    text_surf = font.render(f"Number of lines: {num}", False, (255, 255, 255), (0, 0, 0))
    text_rect = text_surf.get_rect()
    text_rect.topleft = (50, 50)

    window.blit(text_surf, text_rect)


def complete_walk(nums):
    prev_x = START_X
    prev_y = START_Y

    for x, i in enumerate(nums):
        angle = int(i) % 360
        new_x, new_y = walk(prev_x, prev_y, angle)

        draw_line(prev_x, prev_y, new_x, new_y, angle)

        prev_x = new_x
        prev_y = new_y

        if SHOW_LINE_DRAWS and SHOW_TEXT:
            nums_text(x + 1)

    if SHOW_TEXT:
        nums_text(len(nums))

    pygame.display.update()


def main():
    nums = num_generate.main(NUM_ITERS)
    complete_walk(nums)

    while True:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                quit()


main()