import pygame
from engine.objects import Player, GameObject, Enemy, SolidObject
from src.engine.app import App
from src.engine.animation import Animation
from src.engine.vectors import Vector, Acceleration, Speed
from src.engine.commons import WIDTH, HEIGHT
from game.background import Background
from src.engine.levels import Room

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
        app.cancel_button.check_hover(event.pos)
        app.pick_button.check_hover(event.pos)



if __name__ == "__main__":
    pygame.init()

    screen_width = WIDTH
    screen_height = HEIGHT
    screen = pygame.display.set_mode((screen_width, screen_height))
    app = App(screen)
    pygame.mixer.music.load('../assets/menuLoop.mp3')
    pygame.mixer.music.play(-1)
    font = pygame.font.Font(None, 36)
    pygame.display.set_caption("GameObject Example")

    game_object_animation = Animation(
        [f'../assets/player/animations/run/{i}.png' for i in
         range(6)], 100)

    background = Background([f'../assets/background/{i}.png' for i in range(1, 7)], WIDTH, HEIGHT)
    room = Room('../rooms/room1.txt', 0, 0, 80)

    game_object = Player(100, 560, 45, 76,
                         sprite_path="../assets/player/player_stay.png",
                         a0=Acceleration(1,
                                         Vector.unit_from_angle(
                                             90)),
                         animation=game_object_animation)

    """enemy = Enemy(500, 100, 100, 100, sprite_path="../assets/adventurer-00.png",
                  a0=Acceleration(1, Vector.unit_from_angle(90)))
    enemy.set_target(game_object)"""

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
            if not game_started and event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and app.play_button.is_hovered:  # меню
                game_started = True
                is_paused = False
                pygame.mixer.music.stop()
                app.is_menu_music = False
                pygame.mixer.music.load('../assets/stage1.mp3')
                pygame.mixer.music.play(-1)
            if not is_settings and is_paused:  # пауза
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and app.resume_button.is_hovered:
                    is_paused = not is_paused
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and app.exit_button.is_hovered:
                    game_started = False
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and app.settings_button.is_hovered:
                    is_settings = True
            elif is_settings and is_paused:  # настройки
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and app.back1_button.is_hovered:
                    is_settings = False
            elif app.is_lvlup:  # меню улучшений
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and app.upgrade_manager.crit_button.is_hovered:
                    game_object.crit_damage = game_object.crit_damage * 1.2
                    app.is_lvlup = False
                    game_object.is_max_exp = False
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and app.upgrade_manager.damage_button.is_hovered:
                    game_object.damage = game_object.damage * 1.2
                    app.is_lvlup = False
                    game_object.is_max_exp = False
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and app.upgrade_manager.crit_chance_button.is_hovered:
                    game_object.crit_chance = int(game_object.crit_chance * 1.02)
                    app.is_lvlup = False
                    game_object.is_max_exp = False
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and app.upgrade_manager.hp_button.is_hovered:
                    game_object.max_hp += 100
                    game_object.current_hp += 100
                    app.is_lvlup = False
                    game_object.is_max_exp = False
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and app.upgrade_manager.attack_speed_button.is_hovered:
                    game_object.attack_speed += 0.5
                    app.is_lvlup = False
                    game_object.is_max_exp = False
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and app.upgrade_manager.cancel_button.is_hovered:
                    app.is_lvlup = False
                    game_object.is_max_exp = False
            elif game_object.is_item_found:
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and app.cancel_button.is_hovered:
                    game_object.is_item_found = False
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and app.pick_button.is_hovered:
                    game_object.is_item_found = False
                    game_object.damage_mod = game_object.found_item.damage
                    game_object.attack_speed_mod = game_object.found_item.attack_speed
                    game_object.crit_chance_mod = game_object.found_item.crit_chance
                    game_object.crit_damage_mod = game_object.found_item.crit_damage
            hover_check(event)
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                is_paused = not is_paused
                is_settings = False

        if game_started:
            """enemy.can_be_attacked()"""
            screen.fill((0, 0, 0))
            if not is_paused:
                if not app.is_lvlup:
                    enemies = list(filter(lambda x: type(x) is Enemy, room.objects))
                    if game_object.is_max_exp:
                        app.is_lvlup = True
                    if keys[pygame.K_j]:
                        game_object.debug()
                    if mouse[0]:
                        game_object.attack(enemies, tick_count)
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

                    all_game_objects = list(GameObject.all_game_objects) + room.objects
                    # фон обновляем отдельно, тк это кластер объектов, а также нужно передать координаты игрока
                    background.update(screen, game_object.x, game_object.y)
                    collide = False
                    for obj in room.objects:
                        if game_object.check_collide(obj):
                            collide = True
                        if type(obj) is Enemy:
                            obj.set_target(game_object)

                    for obj in enemies:
                        if obj.is_can_attack:
                            obj.attack(tick_count)

                    for object in all_game_objects:
                        object.update(screen, [obj for obj in all_game_objects if obj != object])

                    """if enemy.is_can_attack:
                        enemy.attack(tick_count)"""

                    app.expbar.update(game_object.current_exp, game_object.max_exp)
                    app.expbar.draw()
                    app.hpbar.update(game_object.current_hp, game_object.max_hp)
                    app.hpbar.draw()
                    if game_object.is_item_found:
                        app.item_found()

                elif app.is_lvlup:
                    app.upgrade_manager.draw()
            elif is_paused:
                if not is_settings:
                    app.pause()
                else:
                    app.settings(events)

        else:
            app.start_screen()

        fps = int(clock.get_fps())
        fps_text = font.render(f"FPS: {fps}", True,(255, 255, 255))
        screen.blit(fps_text, (10, 10))
        pygame.display.flip()
        clock.tick(60)
        tick_count += 1

    pygame.quit()