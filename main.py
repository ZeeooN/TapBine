# Nosaukums: TapBine
# Izstrādāja: Haralds Bikše
# Studenta apliecības numurs: 211RDB120

import sys
import time

import pygame as pg
import random as rn

# Ekrāna iestatijumi
DisplayH = 450
DisplayW = 450
DispHW = (DisplayH, DisplayW)

# Inacializē pygame
pg.init()
pg_disp = pg.display.set_mode(DispHW, 0)

# Spļes lauka un tā stāvokļa definēšana
field = []
field_even = False

# Spļes koka definēšana
game_tree = None
h_tree = None
i_tree = None

# Gajienu vēsture. Tiek glabāta katra gajiena indeks
move_history = []


# ------- Funkcijas -------
# Zīmēt kvadrātu uz ektrāna norādītajā poszīcijā
# pos_x - x kordināta | pos_y - y kordināta
def draw_rect(pos_x, pos_y):
    pg.draw.rect(pg_disp, (0, 0, 0), pg.Rect(pos_x, pos_y, 50, 50))
    pg.display.flip()


# Zīmēt apli uz ekrāna norādītajā pozīcijā
# pos_x - x kordināta | pos_y - y kordināta
def draw_circl(pos_x, pos_y):
    pg.draw.circle(pg_disp, (0, 0, 0), (pos_x + 25, pos_y + 25), 25)
    pg.display.flip()


# Zīmēt norādīto figūru norādītajā pozīcijā, ja laukā ir nepara skaits ar figūrām
# f_type - figuras tips (0 - kavdrāts, 1 - aplis), pos - pozīcija laukā [-2;2]
def draw_odd(f_type, pos):
    if f_type == 0:
        draw_rect(200 + (55 * pos), 200)
    elif f_type == 1:
        draw_circl(200 + (55 * pos), 200)


# Zīmēt norādīto figūru norādītajā pozīcijā, ja laukā ir pāra skaits ar figūrām
# f_type - figuras tips (0 - kavdrāts, 1 - aplis), pos - pozīcija laukā [-2;-1] U [1;2]
def draw_even(f_type, pos):
    if pos < -1:
        offset = -84
    elif pos > 1:
        offset = 84
    else:
        offset = 28 * pos

    if f_type == 0:
        draw_rect(200 + offset, 200)
    elif f_type == 1:
        draw_circl(200 + offset, 200)


# No nodotās kursora pozīcijas nosaka uz kuras figūras uz lauka tika nospiest un atgriež tā indeksu masīvā
# ja laukā ir nepāra skaits ar figūrām
# cur_pos - masīvs/saraksts, kas satur kursora koordinātas, f_len - lauka masīva lielums
def get_odd_field_pos(cur_pos, f_len):
    if (cur_pos[1] >= 200) and (cur_pos[1] <= 250):
        if ((cur_pos[0] >= 90) and (cur_pos[0] <= 140)) and (f_len > 3):
            return 0
        if (cur_pos[0] >= 145) and (cur_pos[0] <= 195):
            if f_len < 4:
                return 0
            return 1
        if (cur_pos[0] >= 200) and (cur_pos[0] <= 250):
            if f_len < 4:
                return 1
            return 2
        if (cur_pos[0] >= 255) and (cur_pos[0] <= 305):
            if f_len < 4:
                return 2
            return 3
        if ((cur_pos[0] >= 310) and (cur_pos[0] <= 360)) and (f_len > 3):
            return 4
    return -1


# No nodotās kursora pozīcijas nosaka uz kuras figūras uz lauka tika nospiest un atgriež tā indeksu masīvā
# ja laukā ir pāra sakits ar figūrām
# cur_pos - masīvs/saraksts, kas satur kursora koordinātas, f_len - lauka masīva lielums
def get_even_field_pos(cur_pos, f_len):
    if (cur_pos[1] >= 200) and (cur_pos[1] <= 250):
        if ((cur_pos[0] >= 116) and (cur_pos[0] <= 166)) and (f_len > 2):
            return 0
        if (cur_pos[0] >= 172) and (cur_pos[0] <= 222):
            if f_len < 3:
                return 0
            return 1
        if (cur_pos[0] >= 228) and (cur_pos[0] <= 278):
            if f_len < 3:
                return 1
            return 2
        if ((cur_pos[0] >= 284) and (cur_pos[0] <= 334)) and (f_len > 2):
            return 3
    return -1


# Uzzīmē laukumu uz ekrāna
# g_field - masīvs no kura datiem tiek uzīmēts lauks ar attiecīgajām figūrām
def draw_field(g_field):
    pg.draw.rect(pg_disp, (255, 255, 255), pg.Rect(90, 200, 270, 50))
    j = -2
    if len(g_field) % 2 != 0:
        if len(g_field) == 3:
            j = -1
        elif len(g_field) == 1:
            j = 0
        for i in g_field:
            draw_odd(i, j)
            j = j + 1
    else:
        if len(g_field) == 2:
            j = -1
        for i in field:
            draw_even(i, j)
            j = j + 1
            if j == 0:
                j = 1
    pg.display.flip()


# Apvieno divas figuras, ja 2 kavadrāti -> aplis, ja 2 apļi -> kvadrāts, ja aplis un kvadrāts -> aplis
# un ja kvadrāts un aplis -> kvadrāts
# x - pirmās figūras vērtība, y - otrās figuūras vērtība
# 0 = kvadrāts, 1 = aplis
def merge(x, y):
    if x == 0 and y == 0:
        return 1
    if x == 0 and y == 1:
        return 0
    if x == 1 and y == 0:
        return 1
    if x == 1 and y == 1:
        return 0


# Pēc dotā masīva noteiktajā pozicijā veic figūru apvienošanu un atgriež rezultāta masīvu
# g_field - masīvs ar vērtībāb 0 vai 1, index - pozīcijā kurā veikt apvienošanu
def field_merge(g_field, index):
    new_field = []
    if len(g_field) != 2:
        if index > 0:
            for i in range(0, index):
                new_field.append(g_field[i])
            new_field.append(merge(g_field[index], g_field[index + 1]))
            for i in range(index + 2, len(g_field)):
                new_field.append(g_field[i])
        else:
            new_field.append(merge(g_field[index], g_field[index + 1]))
            for i in range(index + 2, len(g_field)):
                new_field.append(g_field[i])
    else:
        return [merge(g_field[index], g_field[index + 1])]
    return new_field


# Uzģenerē spēles lauka masīvu un aizpilda to ar nejaušām vērtībām [0;1]
def generate_field():
    new_field = [0, 0, 0, 0, 0]
    for i in range(0, (len(new_field) - 1)):
        new_field[i] = round(rn.random())
    return new_field


# Izvada informāciju par to kuram spēlētājam jāveic gājies (Spēlētās vai Dators)
# player - Spēlētājs kurš pašlaik veic gājienu (0 - Dators, 1 - Spēlētējs)
def move_info(player):
    if player == 0:
        pg.draw.rect(pg_disp, (255, 255, 255), pg.Rect(0, 400, 450, 50))
        pg.draw.rect(pg_disp, (0, 0, 0), pg.Rect(0, 0, 450, 50))
        font = pg.font.SysFont('', 24)
        text = font.render('Datora gājiens', True, (255, 255, 255))
        pg_disp.blit(text, (170, 15))
    elif player == 1:
        pg.draw.rect(pg_disp, (255, 255, 255), pg.Rect(0, 0, 450, 50))
        pg.draw.rect(pg_disp, (0, 0, 0), pg.Rect(0, 400, 450, 50))
        font = pg.font.SysFont('', 24)
        text = font.render('Tavs gājiens', True, (255, 255, 255))
        pg_disp.blit(text, (180, 415))

    pg.display.flip()


# Spēles galvenā funkcija (priekš lietotāja gajiena)
# cur_pos - masīvs, kas satur kursora pozīciju
def game_main(cur_pos):
    global field_even, field
    if len(field) > 2:
        if not field_even:
            get_index = get_odd_field_pos(cur_pos, len(field))
            if get_index != (len(field) - 1):
                move_history.append(get_index)
                field = field_merge(field, get_index)
                field_even = True
        else:
            get_index = get_even_field_pos(cur_pos, len(field))
            if get_index != (len(field) - 1):
                move_history.append(get_index)
                field = field_merge(field, get_index)
                field_even = False
        draw_field(field)


# Algoritma gajiena veikšana
# algo_start_m - Dators veica pirmo gājiennu (True or False)
def game_algo_move(algo_start_m=False):
    global field_even, field, h_tree, i_tree, move_history
    if len(field) > 2:
        if not field_even:
            get_index = treeGen.algo_make_move(h_tree, i_tree, move_history, algo_start_m)
            move_history.append(get_index)
            field = field_merge(field, get_index)
            field_even = True
        else:
            get_index = treeGen.algo_make_move(h_tree, i_tree, move_history, algo_start_m)
            move_history.append(get_index)
            field = field_merge(field, get_index)
            field_even = False
        draw_field(field)


# Funkcija, kas tiek izsaukta pēc izvēles pogas nospiešana un sagatavo visu priekš spēles sākuma
def game_start():
    global field, game_tree, h_tree, i_tree

    # Atiestat kursoru uz parasto un notīra ekrānu priekš spēles
    pg.mouse.set_cursor(pg.cursors.arrow)
    pg_disp.fill((255, 255, 255))
    field = generate_field()
    draw_field(field)
    pg.display.flip()

    # Koka ģenerēšana
    temp = treeGen.generate_tree(field)
    game_tree = temp[0]
    i_tree = temp[1]
    h_tree = treeGen.h_generation(game_tree)


# Funkcija, lai pārbaudītu spēles baigu rezultātu un atgriež uzvarētāju
# (0 - Otrais spēlētājs uzvarēja, 1 - Pirmais spēlētājs uzvarēja)
def game_check():
    global field
    if len(field) == 2:
        if field[0] == 0:
            return 0
        else:
            return 1


# Spēles beigu rezultātu izvade uz ekrāna. Paziņo uzvarētāju.
# resault - Spēles uzvarētājs, algo_first - Vai dators veica primo gājienu
def game_end(result, algo_first):
    if algo_first:
        p_info = ['Dators', 'Spēlētājs']
    else:
        p_info = ['Spēlētājs', 'Dators']

    pg.draw.rect(pg_disp, (255, 255, 255), pg.Rect(0, 400, 450, 50))
    pg.draw.rect(pg_disp, (255, 255, 255), pg.Rect(0, 0, 450, 50))
    pg.draw.rect(pg_disp, (0, 0, 0), pg.Rect(0, 0, 450, 50))
    font = pg.font.SysFont('', 24)
    if result == 0:
        text = font.render('Uzvarēja ' + p_info[1], True, (255, 255, 255))
    else:
        text = font.render('Uzvarēja ' + p_info[0], True, (255, 255, 255))

    pg_disp.blit(text, (160, 15))

    text = font.render('Nospied peles kreiso pogu, lai atgrieztos sākumekrānā', True, (0, 0, 0))
    pg_disp.blit(text, (10, 415))

    pg.display.flip()


# Aizpilda ekrānu ar baltu krāsu un uzzīmē izvēles pogas
def game_menu():
    # Aizpilda ekrānu ar baltu krāsu
    pg_disp.fill((255, 255, 255))

    # Uzraksta spēles nosaukumu un papild informāciju
    font = pg.font.SysFont('', 48)
    text = font.render('TapBine', True, (0, 0, 0))
    pg_disp.blit(text, (150, 100))

    font = pg.font.SysFont('', 24)
    text = font.render('Izvēleies kurš sāks spēli:', True, (0, 0, 0))
    pg_disp.blit(text, (126, 150))

    # Uzīmē izvēles pogas
    btn_user()
    btn_bot()

    # Nomaina kursoru uz bultu(standarta kursors)
    pg.mouse.set_cursor(pg.cursors.arrow)
    pg.display.flip()


# Izvelnes poga priekš pirmā gājiena izvēles (lietotāja pirmais gājiens)
# Kā arī pārējās zīmēšanas funkcijas priekš pogas grafiskā izskata
# color - Teksta krāsa
def btn_user_text(color):
    font = pg.font.SysFont('', 28)
    text = font.render('Es', True, color)
    pg_disp.blit(text, (143, 217))


def btn_user():
    pg.draw.rect(pg_disp, (0, 0, 0), pg.Rect(100, 200, 110, 50), 0, 7)
    btn_user_text((255, 255, 255))
    pg.display.flip()


def btn_user_hover():
    pg.draw.rect(pg_disp, (110, 110, 110), pg.Rect(100, 200, 110, 50), 0, 7)
    btn_user_text((255, 255, 255))
    pg.display.flip()


def btn_user_pressed():
    pg.draw.rect(pg_disp, (46, 46, 46), pg.Rect(100, 200, 110, 50), 0, 7)
    btn_user_text((255, 255, 255))
    pg.display.flip()


# Izvelnes poga priekš pirmā gājiena izvēles (datora pirmais gājiens)
# color - Teksta krāsa
def btn_bot_text(color):
    font = pg.font.SysFont('', 28)
    text = font.render('Dators', True, color)
    pg_disp.blit(text, (255, 217))


def btn_bot():
    pg.draw.rect(pg_disp, (0, 0, 0), pg.Rect(230, 200, 110, 50), 0, 7)
    btn_bot_text((255, 255, 255))
    pg.display.flip()


def btn_bot_hover():
    pg.draw.rect(pg_disp, (110, 110, 110), pg.Rect(230, 200, 110, 50), 0, 7)
    btn_bot_text((255, 255, 255))
    pg.display.flip()


def btn_bot_pressed():
    pg.draw.rect(pg_disp, (46, 46, 46), pg.Rect(230, 200, 110, 50), 0, 7)
    btn_bot_text((255, 255, 255))
    pg.display.flip()


# ------- Funkcijas beigas -------


# Programmas izpildāmā daļa
if __name__ == '__main__':
    # Importē koka ģenerēšanas funkcijas
    import treeGen

    # Izsauc funkciju, lai uzzīmētu spēles izvelni
    game_menu()

    # Status vai spēle ir sākata vai nē
    game_playing = False
    algo_start = False

    # Status vai kursors ir bijis uz izvelnes pogām
    cursor_was_on_btn = False

    # Spēles galvenais cikls
    while True:
        for event in pg.event.get():
            # Programmas aizvēršana
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()

            # Peles pogas nospiešana
            elif event.type == pg.MOUSEBUTTONDOWN:
                m_press = pg.mouse.get_pressed()
                if m_press[0]:
                    c_pos = list(pg.mouse.get_pos())

                    # Ja spēle nav sākta gaida līdz tik izvēlēts kurš sāk spēli
                    if not game_playing:
                        if (c_pos[1] >= 200) and (c_pos[1] <= 250):
                            if (c_pos[0] >= 100) and (c_pos[0] <= 210):
                                btn_user_pressed()
                                game_playing = True
                                game_start()
                                move_info(1)
                            elif (c_pos[0] >= 230) and (c_pos[0] <= 340):
                                btn_bot_pressed()
                                game_playing = True
                                algo_start = True
                                game_start()
                                move_info(0)
                                time.sleep(0.5)
                                game_algo_move(algo_start)
                                move_info(1)

                    # Ja tiek sākta jauna spēle
                    elif game_playing:
                        if len(field) > 2:
                            game_main(c_pos)
                            move_info(0)
                            time.sleep(0.5)
                            game_algo_move(algo_start)
                            move_info(1)

                            # Pāruda vai spēle nav beigusies
                            if len(field) == 2:
                                get_win = game_check()
                                game_end(get_win, algo_start)

                        else:
                            # Kad spēle ir beigusies un spēlētājs ir nospiedis peles pogu, tiek atgriezts atpakļ sākumā
                            game_playing = False
                            algo_start = False
                            game_menu()

            # Kursora pārvietošanās
            elif event.type == pg.MOUSEMOTION:
                c_pos = list(pg.mouse.get_pos())
                if not game_playing:
                    if (c_pos[1] >= 200) and (c_pos[1] <= 250):
                        if (c_pos[0] >= 100) and (c_pos[0] <= 210):
                            btn_user_hover()
                            pg.mouse.set_cursor(pg.cursors.diamond)
                            if not cursor_was_on_btn:
                                cursor_was_on_btn = True
                        elif (c_pos[0] >= 230) and (c_pos[0] <= 340):
                            btn_bot_hover()
                            pg.mouse.set_cursor(pg.cursors.diamond)
                            if not cursor_was_on_btn:
                                cursor_was_on_btn = True
                        else:
                            if cursor_was_on_btn:
                                pg.mouse.set_cursor(pg.cursors.arrow)
                                btn_user()
                                btn_bot()
                                cursor_was_on_btn = False
                    else:
                        if cursor_was_on_btn:
                            pg.mouse.set_cursor(pg.cursors.arrow)
                            btn_user()
                            btn_bot()
                            cursor_was_on_btn = False
