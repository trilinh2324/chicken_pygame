import random
from sys import exit
from var import *
from os import remove
import pygame

def create_game(name):
    pygame.init()
    screen = pygame.display.set_mode((1366, 768))
    pygame.display.set_caption(name)
    pygame.display.set_icon(pygame.image.load('../Data/image/chicken.png'))
    load_music(all_music()['bg'], 0.2).play(-1)
    return screen

def w_file(lv_game, lv_gun, score, hp):
    with open('../Data/save/save.txt', 'w') as file:
        file.writelines([f"{lv_game}\n", f"{lv_gun}\n", f"{score}\n", f"{hp}\n"])

def r_file():
    with open('../Data/save/save.txt') as file:
        return [int(line.strip()) for line in file]

def close():
    pygame.quit()
    exit()

def load_music(path, vol):
    sound = pygame.mixer.Sound(path)
    sound.set_volume(vol)
    return sound

def collision(inf_1, inf_2):
    for i in range(len(inf_1['pos'])):
        inf_1['rect'].topleft = inf_1['pos'][i]
        for j in range(len(inf_2['pos'])):
            inf_2['rect'].topleft = inf_2['pos'][j]
            if (inf_1['rect']).colliderect(inf_2['rect']):
                return [i, j]
    return None

def change_pos(tuple_1, tuple_2):
    return tuple(a + b for a, b in zip(tuple_1, tuple_2))

def add_event(id_event, timer):
    event_id = pygame.USEREVENT + id_event
    pygame.time.set_timer(event_id, timer)
    return event_id

def show_score_hp(screen, score, hp):
    screen.blit(text(f"Điểm: {score}", 40, 'Yellow'), (50, 0))
    screen.blit(text(f"Mạng: {hp}", 40, 'Brown'), (50, 60))

def screen_playing(screen, obj, pl_inf, ck_inf, boss_inf_data, egg_inf, ls_inf, score_inf, item_inf_data, score, hp, time):
    for i, j in obj: screen.blit(i, j)
    for pos in ls_inf['pos']: screen.blit(ls_inf['img'], pos)
    for pos in ck_inf['pos']: screen.blit(ck_inf['img'], pos)
    for pos in egg_inf['pos']: screen.blit(egg_inf['img'], pos)
    for pos in score_inf['pos']: screen.blit(score_inf['img'], pos)
    for pos in item_inf_data['pos']: screen.blit(item_inf_data['img'], pos)
    if boss_inf_data['pos']:
        screen.blit(boss_inf_data['img'], boss_inf_data['pos'][0])
    show_score_hp(screen, score, hp)
    screen.blit(text(f"Thời gian: {time}", 30, 'Red'), (1100, 700))
    screen.blit(pl_inf['img'], pl_inf['pos'][0])
    pygame.display.update()

def add_pos_menu(obj_menu):
    new_arr = [[obj_menu[0], (500, 100)]]
    pos_y = 350
    for i in range(1, len(obj_menu)):
        new_arr.append([obj_menu[i], (600, pos_y)])
        pos_y += 100
    return new_arr

def create_menu(screen, menu):
    obj = add_pos_menu(menu)
    bg = get_img('bg')
    signal = text('>>>', 50, 'White')
    pos_sgn = (obj[1][1][0] - 80, obj[1][1][1])
    fps = pygame.time.Clock()
    select = 1
    while True:
        fps.tick(15)
        screen.blit(bg, (0, 0))
        screen.blit(signal, pos_sgn)
        for i, j in obj: screen.blit(i, j)
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT: close()
        key = pygame.key.get_pressed()
        if key[pygame.K_DOWN] and select < len(menu) - 1:
            select += 1; pos_sgn = change_pos(pos_sgn, (0, 100))
        elif key[pygame.K_UP] and select > 1:
            select -= 1; pos_sgn = change_pos(pos_sgn, (0, -100))
        elif key[pygame.K_RETURN]:
            return select

def create_chicken(level, number_ck, ck_inf):
    distance = 80; x = 100; y = 0; direct = False
    for i in range(number_ck):
        ck_inf['pos'].append((x, y)); ck_inf['direct'].append(direct)
        if (i + 1) % 15 == 0: x, y, direct = 100, y+100, not direct
        else: x += distance

def create_laser(num_ray, ls_inf, pl_inf, sound):
    px, py = pl_inf['pos'][0]
    if num_ray == 1:
        ls_inf['pos'].append((px + 20, py - 20))
    elif num_ray == 2:
        ls_inf['pos'].append((px, py - 20))
        ls_inf['pos'].append((px + 40, py - 20))
    elif num_ray == 3:
        ls_inf['pos'].append((px - 20, py - 20))
        ls_inf['pos'].append((px + 20, py - 20))
        ls_inf['pos'].append((px + 60, py - 20))
    elif num_ray == 4:
        ls_inf['pos'].append((px - 30, py - 20))
        ls_inf['pos'].append((px - 10, py - 20))
        ls_inf['pos'].append((px + 50, py - 20))
        ls_inf['pos'].append((px + 70, py - 20))
    elif num_ray == 5:  
        ls_inf['pos'].append((px + 20, py - 20))  
        ls_inf['pos'].append((px, py - 20))       
        ls_inf['pos'].append((px + 40, py - 20))  
        ls_inf['pos'].append((px - 20, py - 20))  
        ls_inf['pos'].append((px + 60, py - 20))  
    sound.play()

def create_egg(level, egg_inf, ck_inf, boss_inf_data):
    if boss_inf_data['pos']:
        egg_inf['pos'].append(change_pos(boss_inf_data['pos'][0], (40, 100)))
        egg_inf['direct'].append(boss_inf_data['direct'])
    elif ck_inf['pos']:
        temp = random.randint(0, len(ck_inf['pos']) - 1)
        egg_inf['pos'].append(change_pos(ck_inf['pos'][temp], (10, 50)))
        egg_inf['direct'].append(ck_inf['direct'][temp])

def move(speed, inf):
    for i in range(len(inf['pos'])):
        inf['pos'][i] = change_pos(inf['pos'][i], (0, speed))

def move_ck(inf):
    for i in range(len(inf['pos'])):
        step = -1 if inf['direct'][i] else 1
        inf['pos'][i] = change_pos(inf['pos'][i], (step, 0))
        if inf['pos'][i][0] > 1300: inf['direct'][i] = True
        elif inf['pos'][i][0] < 0: inf['direct'][i] = False

def move_boss(boss_inf_data):
    if boss_inf_data['pos']:
        step = -2 if boss_inf_data['direct'] else 2
        x, y = boss_inf_data['pos'][0]
        x += step
        if x < 0: boss_inf_data['direct'] = False
        elif x > 1200: boss_inf_data['direct'] = True
        boss_inf_data['pos'][0] = (x, y)

def move_eggs(inf):
    for i in range(len(inf['pos'])):
        step = -2 if inf['direct'][i] else 2
        inf['pos'][i] = change_pos(inf['pos'][i], (step, 2))

def out_screen(inf, size_screen):
    inf['pos'] = [p for p in inf['pos'] if 0 <= p[0] <= size_screen[0] and 0 <= p[1] <= size_screen[1]]

def screen_show_mess(screen, string):
    screen.blit(get_img('bg'), (0, 0))
    screen.blit(text(string, 60, 'Red'), (300, 300))
    pygame.display.update()

def countdown_next_level(screen, lv):
    for i in range(3, 0, -1):
        screen_show_mess(screen, f"Bắt đầu Level {lv} sau {i}")
        pygame.time.delay(1000)
    screen_show_mess(screen, "Bắt đầu!")
    pygame.time.delay(800)

def loop_playing(screen, load=None):
    if load is None:
        load = [1, 1, 0, 5]
    lv_game, lv_gun, score, hp = load
    if lv_game > 1:
        w_file(lv_game, lv_gun, score, hp)

    game = game_level()
    gun = gun_level()
    pl_inf = player_inf()
    ck_inf = chicken_inf()
    boss_data = boss_inf(lv_game)
    boss_data['hp'] += (lv_game - 1) * 5

    ls_inf = laser_inf()
    egg_inf = eg_inf()
    item_data = item_inf()
    score_inf = sc_inf()

    create_chicken(lv_game, game[lv_game][1], ck_inf)
    laser_sound = load_music(all_music()['shoot'], 0.05)
    boom_sound = load_music(all_music()['explode_ck'], 0.05)
    collision_sound = load_music(all_music()['collision'], 0.05)

    ls_speed = add_event(0, gun[lv_gun][0])
    egg_speed = add_event(1, game[lv_game][0])
    countdown = add_event(2, 1000)

    count = game[lv_game][3]
    obj = obj_default_playing()
    fps = pygame.time.Clock()
    Max = pygame.display.get_window_size()

    while True:
        fps.tick(60)
        screen_playing(screen, obj, pl_inf, ck_inf, boss_data, egg_inf, ls_inf, score_inf, item_data, score, hp, count)

        for event in pygame.event.get():
            if event.type == pygame.QUIT: close()
            elif event.type == ls_speed: create_laser(min(lv_gun, 5), ls_inf, pl_inf, laser_sound)
            elif event.type == egg_speed: create_egg(lv_game, egg_inf, ck_inf, boss_data)
            elif event.type == countdown: count -= 1

        if not ck_inf['pos'] and not boss_data['pos']:
            boss_data['pos'] = [(600, 100)]

        if boss_data['pos'] and boss_data['hp'] <= 0:
            lv_game += 1
            w_file(lv_game, lv_gun, score, hp)
            if lv_game <= 10:
                countdown_next_level(screen, lv_game)
                loop_playing(screen, [lv_game, lv_gun, score, hp])
            else:
                screen_show_mess(screen, "Bạn đã thắng toàn bộ trò chơi!")
                pygame.time.delay(3000)
            return

        if hp <= 0 or count == 0:
            screen_show_mess(screen, "Bạn đã thua!")
            pygame.time.delay(3000)
            if lv_game != 1: remove('../Data/save/save.txt')
            return

        out_screen(ls_inf, Max)
        out_screen(score_inf, Max)
        out_screen(egg_inf, Max)
        out_screen(item_data, Max)
        move_ck(ck_inf)
        move_boss(boss_data)
        move_eggs(egg_inf)
        move(-gun[lv_gun][2], ls_inf)
        move(1, score_inf)
        move(1, item_data)

        check = collision(ls_inf, ck_inf)
        if check:
            boom_sound.play()
            score += 1
            if random.random() < 0.2:
                item_data['pos'].append(ck_inf['pos'][check[1]])
            score_inf['pos'].append(ck_inf['pos'][check[1]])
            ls_inf['pos'].pop(check[0])
            ck_inf['pos'].pop(check[1])
            ck_inf['direct'].pop(check[1])
        else:
            check = collision(ls_inf, boss_data)
            if check:
                boom_sound.play()
                ls_inf['pos'].pop(check[0])
                boss_data['hp'] -= 1


        check = collision(egg_inf, pl_inf)
        if check:
            collision_sound.play()
            hp -= 1
            egg_inf['pos'].pop(check[0])
            egg_inf['direct'].pop(check[0])
            lv_gun = 1
            pygame.time.set_timer(ls_speed, gun[lv_gun][0])
            ls_inf['pos'].clear()


        check = collision(item_data, pl_inf)
        if check:
            if lv_gun < 5:
                lv_gun += 1
            pygame.time.set_timer(ls_speed, gun[lv_gun][0])
            item_data['pos'].pop(check[0])


        check = collision(score_inf, pl_inf)
        if check:
            score_inf['pos'].pop(check[0])
            score += 1

        key = pygame.key.get_pressed()
        pos_x, pos_y = pl_inf['pos'][0]
        if (key[pygame.K_LEFT] or key[pygame.K_a]) and pos_x - pl_inf['move'] > 0:
            pl_inf['pos'][0] = change_pos(pl_inf['pos'][0], (-pl_inf['move'], 0))
        elif (key[pygame.K_RIGHT] or key[pygame.K_d]) and pos_x + pl_inf['move'] + pl_inf['rect'].width <= Max[0]:
            pl_inf['pos'][0] = change_pos(pl_inf['pos'][0], (pl_inf['move'], 0))
        elif (key[pygame.K_UP] or key[pygame.K_w]) and pos_y - pl_inf['move'] > Max[1] // 2:
            pl_inf['pos'][0] = change_pos(pl_inf['pos'][0], (0, -pl_inf['move']))
        elif (key[pygame.K_DOWN] or key[pygame.K_s]) and pos_y + pl_inf['move'] + pl_inf['rect'].height <= Max[1]:
            pl_inf['pos'][0] = change_pos(pl_inf['pos'][0], (0, pl_inf['move']))
        elif key[pygame.K_ESCAPE]:
            choose = create_menu(screen, [
                text("TẠM DỪNG", 80, "Red"),
                text("Tiếp tục", 50, "Yellow", True),
                text("Quay lại Trang chủ", 50, "Yellow", True)
            ])
            if choose == 2: return
