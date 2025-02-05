import pygame
from engine.objects import Player, GameObject, Enemy, SolidObject
from engine.app import App
from engine.animation import Animation
from engine.vectors import Vector, Acceleration, Speed
from engine.commons import WIDTH, HEIGHT
from game.background import Background

def hover_check(event):
    if event.type == pygame.MOUSEMOTION:
        app.play_button.check_hover(event.pos)
        app.resume_button.check_hover(event.pos)
        app.exit_button.check_hover(event.pos)
        app.settings_button.check_hover(event.pos)
        app.back1_button.check_hover(event.pos)
        app.upgrade_manager.crit_button.check_hover(event.pos)
        app.upgrade_manager.hp_button.check_hover(event.pos)
        app.upgrade_manager.crit_chance_button.check_hover(event.pos)
        app.upgrade_manager.damage_button.check_hover(event.pos)
        app.upgrade_manager.attack_speed_button.check_hover(event.pos)
        app.upgrade_manager.cancel_button.check_hover(event.pos)


if __name__ == "__main__":
    pygame.init()

    screen_width = WIDTH
    screen_height = HEIGHT
    screen = pygame.display.set_mode((screen_width, screen_height))
    app = App(screen)
    pygame.mixer.music.load('../assets/menuLoop.mp3')
    pygame.mixer.music.play(-1)

    pygame.display.set_caption("GameObject Example")

    game_object_animation = Animation(
        [f'../assets/player/animations/run/{i}.png' for i in
         range(6)], 100)

    background = Background([f'../assets/background/{i}.png' for i in range(1, 7)], WIDTH, HEIGHT)

    game_object = Player(100, 0, 45, 76,
                         sprite_path="../assets/player/player_stay.png",
                         a0=Acceleration(1,
                                         Vector.unit_from_angle(
                                             90)),
                         animation=game_object_animation)

    enemy = Enemy(500, 100, 100, 100, sprite_path="../assets/adventurer-00.png",
                  a0=Acceleration(1, Vector.unit_from_angle(90)))
    enemy.set_target(game_object)

    surface = SolidObject(0, 500, 1000, 1000)
    running = True
    clock = pygame.time.Clock()
    flag = True
    game_started = False
    is_paused = False
    is_settings = False
    tick_count = 0

    while running:
        keys = pygame.key.get_pressed()
        events = pygame.event.get()
        mouse = pygame.mouse.get_pressed()
        for event in events:
            if event.type == pygame.QUIT:
                running = False
            if not game_started and event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and app.play_button.is_hovered: # меню
                game_started = True
                is_paused = False
                pygame.mixer.music.stop()
                app.is_menu_music = False
                pygame.mixer.music.load('../assets/stage1.mp3')
                pygame.mixer.music.play(-1)
            if not is_settings and is_paused: # пауза
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and app.resume_button.is_hovered:
                    is_paused = not is_paused
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and app.exit_button.is_hovered:
                    game_started = False
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and app.settings_button.is_hovered:
                    is_settings = True
            else: # настройки
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and app.back1_button.is_hovered:
                    is_settings = False
            if app.is_lvlup: # меню улучшений
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and app.upgrade_manager.crit_button.is_hovered:
                    game_object.crit_damage = game_object.crit_damage * 1.2
                    app.is_lvlup = False
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and app.upgrade_manager.damage_button.is_hovered:
                    game_object.damage = game_object.damage * 1.2
                    app.is_lvlup = False
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and app.upgrade_manager.crit_chance_button.is_hovered:
                    game_object.crit_chance = int(game_object.crit_chance * 1.02)
                    app.is_lvlup = False
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and app.upgrade_manager.hp_button.is_hovered:
                    game_object.max_hp += 100
                    game_object.current_hp += 100
                    app.is_lvlup = False
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and app.upgrade_manager.attack_speed_button.is_hovered:
                    game_object.attack_speed += 0.5
                    app.is_lvlup = False
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and app.upgrade_manager.cancel_button.is_hovered:
                    app.is_lvlup = False
            hover_check(event)
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                is_paused = not is_paused
                is_settings = False

        if game_started:
            enemy.can_be_attacked()
            screen.fill((0, 0, 0))
            if not is_paused:
                if not app.is_lvlup:
                    if game_object.is_max_exp():
                        app.is_lvlup = True
                    if keys[pygame.K_j]:
                        enemy.respawn()
                    if mouse[0]:
                        game_object.attack([enemy], tick_count)
                    if keys[pygame.K_SPACE]:
                        game_object.jump()

                    if keys[pygame.K_RIGHT]:
                        game_object.speed = game_object.speed + Speed(0.6,
                                                                      Vector.unit_from_angle(
                                                                          0))
                        game_object.target_orientation = 'right'

                    if keys[pygame.K_LEFT]:
                        game_object.speed = game_object.speed + Speed(0.6,
                                                                      Vector.unit_from_angle(
                                                                          180))
                        game_object.target_orientation = 'left'

                    all_game_objects = GameObject.all_game_objects
                    # фон обновляем отдельно, тк это кластер объектов, а также нужно передать координаты игрока
                    background.update(screen, game_object.x, game_object.y)

                    for object in all_game_objects:
                        object.update(screen, [obj for obj in all_game_objects if obj != object])

                    app.expbar.update(game_object.current_exp, game_object.max_exp)
                    app.expbar.draw()
                    app.hpbar.update(game_object.current_hp, game_object.max_hp)
                    app.hpbar.draw()

                elif app.is_lvlup:
                    app.upgrade_manager.draw()
            elif is_paused:
                if not is_settings:
                    app.pause()
                else:
                    app.settings(events)

        else:
            app.start_screen()

        pygame.display.flip()
        clock.tick(120)
        tick_count += 1

    pygame.quit()