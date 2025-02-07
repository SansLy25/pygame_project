from pathlib import Path

import pygame
from engine.objects import Player, GameObject, Enemy, Boss
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

    rooms_path = Path("../rooms/")
    level_count = len([item for item in rooms_path.iterdir() if item.is_file()])
    current_level = 0

    screen_width = WIDTH
    screen_height = HEIGHT
    screen = pygame.display.set_mode((screen_width, screen_height))
    app = App(screen)
    pygame.mixer.music.load("../assets/menuLoop.mp3")
    pygame.mixer.music.play(-1)
    font = pygame.font.Font(None, 36)
    pygame.display.set_caption("GameObject Example")

    player_animation = Animation(
        [f"../assets/player/animations/run/{i}.png" for i in range(6)], 100, "run"
    )

    background = Background(
        [f"../assets/background/{i}.png" for i in range(1, 7)], WIDTH, HEIGHT
    )
    room = Room("../rooms/0.txt", 0, 0, 80)

    player = Player(
        room.spawn_point[0],
        room.spawn_point[1],
        45,
        76,
        sprite_path="../assets/player/player_stay.png",
        a0=Acceleration(1, Vector.unit_from_angle(90)),
        animation=player_animation,
    )

    running = True

    clock = pygame.time.Clock()
    game_other = False
    flag = True
    boss_level = False
    you_win = False
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
            if (
                not game_started
                and event.type == pygame.MOUSEBUTTONDOWN
                and event.button == 1
                and app.play_button.is_hovered
            ):  # меню
                game_started = True
                is_paused = False
                pygame.mixer.music.stop()
                app.is_menu_music = False
                pygame.mixer.music.load("../assets/stage1.mp3")
                pygame.mixer.music.play(-1)
            if not is_settings and is_paused:  # пауза
                if (
                    event.type == pygame.MOUSEBUTTONDOWN
                    and event.button == 1
                    and app.resume_button.is_hovered
                ):
                    is_paused = not is_paused
                if (
                    event.type == pygame.MOUSEBUTTONDOWN
                    and event.button == 1
                    and app.exit_button.is_hovered
                ):
                    game_started = False
                if (
                    event.type == pygame.MOUSEBUTTONDOWN
                    and event.button == 1
                    and app.settings_button.is_hovered
                ):
                    is_settings = True
            elif is_settings and is_paused:  # настройки
                if (
                    event.type == pygame.MOUSEBUTTONDOWN
                    and event.button == 1
                    and app.back1_button.is_hovered
                ):
                    is_settings = False
            elif app.is_lvlup:  # меню улучшений
                if (
                    event.type == pygame.MOUSEBUTTONDOWN
                    and event.button == 1
                    and app.upgrade_manager.crit_button.is_hovered
                ):
                    player.crit_damage = player.crit_damage * 1.2
                    app.is_lvlup = False
                    player.is_max_exp = False
                if (
                    event.type == pygame.MOUSEBUTTONDOWN
                    and event.button == 1
                    and app.upgrade_manager.damage_button.is_hovered
                ):
                    player.damage = player.damage * 1.2
                    app.is_lvlup = False
                    player.is_max_exp = False
                if (
                    event.type == pygame.MOUSEBUTTONDOWN
                    and event.button == 1
                    and app.upgrade_manager.crit_chance_button.is_hovered
                ):
                    player.crit_chance = int(player.crit_chance * 1.02)
                    app.is_lvlup = False
                    player.is_max_exp = False
                if (
                    event.type == pygame.MOUSEBUTTONDOWN
                    and event.button == 1
                    and app.upgrade_manager.hp_button.is_hovered
                ):
                    player.max_hp += 100
                    player.current_hp += 100
                    app.is_lvlup = False
                    player.is_max_exp = False
                if (
                    event.type == pygame.MOUSEBUTTONDOWN
                    and event.button == 1
                    and app.upgrade_manager.attack_speed_button.is_hovered
                ):
                    player.attack_speed += 0.5
                    app.is_lvlup = False
                    player.is_max_exp = False
                if (
                    event.type == pygame.MOUSEBUTTONDOWN
                    and event.button == 1
                    and app.upgrade_manager.cancel_button.is_hovered
                ):
                    app.is_lvlup = False
                    player.is_max_exp = False
            elif player.is_item_found:
                if (
                    event.type == pygame.MOUSEBUTTONDOWN
                    and event.button == 1
                    and app.cancel_button.is_hovered
                ):
                    player.is_item_found = False
                if (
                    event.type == pygame.MOUSEBUTTONDOWN
                    and event.button == 1
                    and app.pick_button.is_hovered
                ):
                    player.is_item_found = False
                    player.damage_mod = player.found_item.damage
                    player.attack_speed_mod = player.found_item.attack_speed
                    player.crit_chance_mod = player.found_item.crit_chance
                    player.crit_damage_mod = player.found_item.crit_damage
            hover_check(event)
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                is_paused = not is_paused
                is_settings = False

        if game_started:
            screen.fill((0, 0, 0))
            if not is_paused:
                if not app.is_lvlup:
                    if player.hp_check():
                        game_other = True
                        is_paused = True

                    enemies = list(filter(lambda x: type(x) is Enemy, room.objects))
                    player.current_time = tick_count

                    if boss_level:
                        if boss.hp_check():
                            you_win = True
                            is_paused = True
                        enemies.append(boss)
                        boss.set_target(player)

                    if player.is_max_exp:
                        app.is_lvlup = True
                    if mouse[0]:
                        player.attack(enemies, tick_count)
                    if keys[pygame.K_SPACE]:
                        player.jump()

                    if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
                        player.speed = player.speed + Speed(
                            0.6, Vector.unit_from_angle(0)
                        )
                        player.target_orientation = "right"

                    if keys[pygame.K_LEFT] or keys[pygame.K_a]:
                        player.speed = player.speed + Speed(
                            0.6, Vector.unit_from_angle(180)
                        )
                        player.target_orientation = "left"

                    all_objects = list(GameObject.all_game_objects)
                    if player.room > current_level:
                        GameObject.all_game_objects.clear()
                        GameObject.all_game_objects.add(player)
                        room = Room(f"../rooms/{player.room}.txt", 0, 0, 80)
                        player.x = room.spawn_point[0]
                        player.y = room.spawn_point[1]
                        current_level += 1
                        tick_count = 0
                        player.last_attack_time = 0
                        player.last_damage_time = 0
                        if current_level == level_count - 1:
                            boss = Boss(
                                WIDTH // 2 - 200,
                                600,
                                400,
                                600,
                                sprite_path="../assets/pixel-0077-668142567.png",
                            )
                            boss.last_attack_time = tick_count
                            boss.set_target(player)
                            boss_level = True
                            enemies.append(boss)
                    # фон обновляем отдельно, тк это кластер объектов, а также нужно передать координаты игрока
                    background.update(screen, player.x, player.y)
                    collide = False
                    for obj in room.objects:
                        if player.check_collide(obj):
                            collide = True
                        if type(obj) is Enemy:
                            obj.set_target(player)

                    for obj in enemies:
                        if type(obj) is not Boss:
                            if obj.is_can_attack:
                                obj.attack(tick_count)

                    for object in all_objects:
                        object.update(
                            screen, [obj for obj in all_objects if obj != object]
                        )

                    if boss_level:
                        if boss.columns:
                            for i in boss.columns:
                                if i.active:
                                    i.damage(14, tick_count)
                        if boss.bullets:
                            for i in boss.bullets:
                                if i.active:
                                    i.damage(14, tick_count)

                    app.expbar.update(player.current_exp, player.max_exp)
                    app.expbar.draw()
                    app.hpbar.update(player.current_hp, player.max_hp)
                    app.hpbar.draw()
                    if boss_level:
                        app.boss_bar.draw()
                        app.boss_bar.update(boss.current_hp)

                    if player.is_item_found:
                        app.item_found()

                elif app.is_lvlup:
                    app.upgrade_manager.draw()
            elif is_paused:
                if is_settings:
                    app.pause()
                elif game_other:
                    app.death(player.lvl + 1, player.room, level_count)
                elif you_win:
                    app.you_win(player.lvl + 1, player.room, current_level)
                else:
                    app.settings(events)

        else:
            app.start_screen()

        fps = int(clock.get_fps())
        fps_text = font.render(f"FPS: {fps}", True, (255, 255, 255))
        screen.blit(fps_text, (10, 10))
        pygame.display.flip()
        clock.tick(60)
        tick_count += 1

    pygame.quit()
