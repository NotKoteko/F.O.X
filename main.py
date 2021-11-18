import pygame

from engine.python.util.video import get_screen_size, set_fullscreen, get_centered_pos, draw_world
from python.worlds import Menu


# Свернуть и развернуть окно
def toggle_fullscreen():
    global fullscreen
    fullscreen = not fullscreen                                 # Меняем значение на противоположное
    set_fullscreen(fullscreen, get_screen_size(), WINDOW_SIZE)  # Сворачиваем/разворачиваем окно
    movement = 1 if fullscreen else -1
    world.cam_x += get_centered_pos(get_screen_size(), WINDOW_SIZE)[0] * movement
    world.cam_y += get_centered_pos(get_screen_size(), WINDOW_SIZE)[1] * movement


WINDOW_SIZE = 800, 600
MAX_FPS = 0
if __name__ == '__main__':
    pygame.init()                                   # Запуск PyGame
    pygame.font.init()                              # Запуск шрифтов
    screen = pygame.display.set_mode(WINDOW_SIZE)   # Создаём окно

    pygame.display.set_caption("FOX")               # Устанавливаем заголовок окна
    font = pygame.font.SysFont('calibri', 36)       # Записываем какой-то шрифт в переменную
    clock = pygame.time.Clock()                     # Эта штука считает время между кадрами
    frames, time, fps = 0, 0, 0

    world = Menu()
    fox = world.get_player()

    fullscreen = False                              # Переменная шоб следить за состоянием окна
    running = True                                  # Переменная шоб следить запущена ли игра

    while running:                                  # Игровой цикл (1 шаг = 1 кадр)
        time_passed = clock.tick(MAX_FPS)                                   # Счётчик мс между кадрами
        pressed_keys = pygame.key.get_pressed()                             # Зажатые клавиши
        events = pygame.event.get()                                         # Все события
        fox = world.get_player()

        for event in events:
            if event.type == pygame.QUIT:                                   # Выход из игры
                running = False
            elif event.type == pygame.KEYDOWN:                              # Нажатие клавиши:
                if event.key == pygame.K_ESCAPE:                                # ESC, выход из игры
                    running = False
                elif event.key == pygame.K_F11:                                 # F11, смена размера окна
                    toggle_fullscreen()

        draw_world(screen, world)                                  # Отрисовываем игровой мир
        upd_res = world.update(time_passed, events, pressed_keys)  # Обновляем мир

        if world.name == "Menu":
            world = upd_res
            fox = world.get_player()
        elif fox is not None:
            for obj in world:

                pygame.draw.rect(screen, (255, 0, 0),
                                 obj.get_texture_rect().move(world.cam_x, world.cam_y).to_pygame_rect(), 1)
                pygame.draw.rect(screen, (0, 0, 255), obj.rect.move(world.cam_x, world.cam_y).to_pygame_rect(), 1)
            screen.blit(font.render(f"{fps}", False, (255, 0, 0)), (10, 10))

        frames, time = frames + 1, time + time_passed
        if time > 1000:
            frames, time, fps = 0, 0, frames

        pygame.display.flip()  # Вываливаем всё на экран
    pygame.quit()  # Выходим из пайгейма, если закрыли окно
