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


def get_centered_pos(screen_size, window_size):
    return (screen_size[0] - window_size[0]) // 2, (screen_size[1] - window_size[1]) // 2


def set_fullscreen(is_full, fullscreen_size, windowed_size):
    hwnd = pygame.display.get_wm_info()['window']
    x, y = (0, 0) if is_full else get_centered_pos(fullscreen_size, windowed_size)
    w, h = fullscreen_size if is_full else windowed_size
    pygame.display.set_mode((w, h), pygame.NOFRAME)
    windll.user32.MoveWindow(hwnd, x, y, w, h, False)
