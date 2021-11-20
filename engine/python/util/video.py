from ctypes import windll
import os
import pygame


def load_image(name) -> pygame.Surface:
    try:
        image = pygame.image.load(os.path.join('resources/img', name + ".png"))
    except FileNotFoundError:
        try:
            image = pygame.image.load(os.path.join('engine/resources/img', name + '.png'))
        except FileNotFoundError:
            image = pygame.Surface((1, 1))
    return image.convert_alpha()


def scale_image(image, width, height):
    return pygame.transform.scale(image, (width, height))


def flip_image(image, flip_x, flip_y):
    return pygame.transform.flip(image, flip_x, flip_y)


def add_color_filter(image, color):
    image = image.copy()
    size = image.get_size()
    for y in range(size[1]):
        for x in range(size[0]):
            color_at = image.get_at((x, y))
            middle_color = [(color_at[x] + color[x]) // 2 for x in range(len(color))] + [color_at[3]]
            for i in range(len(middle_color)):
                if middle_color[i] > 255:
                    middle_color[i] = 255
            image.set_at((x, y), middle_color)
    return image


def draw_world(surface, world):
    surface.fill(world.background_color)
    player = world.get_player()
    for obj in world:
        rect = obj.get_texture_rect()
        image = scale_image(obj.get_texture(), rect.width, rect.height)
        if player:
            if obj != player:
                player_rect = player.get_texture_rect()
                if rect.collide_rect(player_rect):
                    image.set_alpha(220)
        world.obj_dict[obj] = surface.blit(image, (rect.x + world.cam_x, rect.y + world.cam_y))


def get_screen_size():
    return windll.user32.GetSystemMetrics(0), windll.user32.GetSystemMetrics(1)


def get_centered_pos(size_bigger, size_smaller):
    return (size_bigger[0] - size_smaller[0]) // 2, (size_bigger[1] - size_smaller[1]) // 2
