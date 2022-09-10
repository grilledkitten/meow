import pygame as pg
import random as rand

pg.init()

#   field sizes : 50 * 25

w = 50
h = 25

width = 1000
height = 500

font = pg.font.Font(None, 16)
bigfont = pg.font.Font(None, 240)
sc = pg.display.set_mode((width, height))
pg.display.update()
bg = (115, 107, 93)
lines = (209, 205, 181)
not_opened = (189, 145, 56)
sc.fill(not_opened)
pg.display.set_caption('minesweeper')

bombs = [[0 for i in range(w)] for j in range(h)]
field = [[0 for i in range(w)] for j in range(h)]
flags = [[0 for i in range(w)] for j in range(h)]
bombs_amount = 200
bombs_array = []
i = 0
while i < bombs_amount:  # bomb generation
    x = rand.randint(0, w - 1)
    y = rand.randint(0, h - 1)
    bomb = [x, y]
    if (len(bombs_array) != 0) and (bomb not in bombs_array) or (len(bombs_array) == 0):
        bombs_array.append(bomb)
        bombs[y][x] = 1
        i += 1
for f in range(h):   # counting amount of bombs in neighbourhood
    for s in range(w):
        k = 0
        if bombs[f][s] != 1:
            k = 0
            x_arr = [s]
            y_arr = [f]
            if s > 0:
                x_arr.append(s - 1)
            if s < w - 1:
                x_arr.append(s + 1)
            if f > 0:
                y_arr.append(f - 1)
            if f < h - 1:
                y_arr.append(f + 1)
            for a in x_arr:
                for b in y_arr:
                    if not ((a == s) and (b == f)):
                        k += bombs[b][a]
            field[f][s] = k
pg.display.update()
click = [[0 for i in range(w)] for j in range(h)]
flags_am = 0
opened_cells = 0

def check_2nd_cl(c1, c2):
    return click[c2][c1] == 1


def check_0(c1, c2):
    return field[c2][c1] == 0


def check_fl_am(c1, c2):
    return flags_count(c1, c2) == field[c2][c1]


def draw(c1, c2):   # c1 - x    c2 - y !!!!! (c2 строка c1 столбец)
    n = str(field[c2][c1])
    if n == "0":
        n = " "
    t = font.render(n, True, (0, 0, 100))
    pl = t.get_rect(center=(10 + c1 * 20, 10 + c2 * 20))
    pg.draw.rect(sc, bg, pg.Rect(c1 * 20, c2 * 20, 20, 20))
    sc.blit(t, pl)
    pg.display.update()


def game_over(c1_, c2_):
    pg.draw.rect(sc, bg, pg.Rect(c1_ * 20, c2_ * 20, 20, 20))
    bmb = font.render("@", True, (100, 0, 0))
    plc = bmb.get_rect(center=(10 + c1_ * 20, 10 + c2_ * 20))
    sc.blit(bmb, plc)
    pg.display.update()
    for item in bombs_array:
        c1 = item[0]
        c2 = item[1]
        if c1 != c1_ and c2 != c2_:
            bmb = font.render("@", True, (0, 0, 0))
            plc = bmb.get_rect(center=(10 + c1 * 20, 10 + c2 * 20))
            sc.blit(bmb, plc)
            pg.display.update()
    t = bigfont.render("GAME OVER", True, (100, 0, 0))
    pl = t.get_rect(center=(500, 250))
    sc.blit(t, pl)
    pg.display.update()
    run = True
    while run:
        for i in pg.event.get():
            if i.type == pg.QUIT:
                run = False
    pg.quit()
    quit()
    return 0


def win():
    t = bigfont.render("VICTORY", True, (0, 100, 0))
    pl = t.get_rect(center=(500, 250))
    sc.blit(t, pl)
    pg.display.update()
    run = True
    while run:
        for i in pg.event.get():
            if i.type == pg.QUIT:
                run = False
    pg.quit()
    quit()
    return 0


def open_around(c1, c2):
    global opened_cells
    x_arr = [c1]
    y_arr = [c2]
    if c1 > 0:
        x_arr.append(c1 - 1)
    if c1 < w - 1:
        x_arr.append(c1 + 1)
    if c2 > 0:
        y_arr.append(c2 - 1)
    if c2 < h - 1:
        y_arr.append(c2 + 1)
    for x in x_arr:
        for y in y_arr:
            if not ((x == c1) and (y == c2)):
                if (bombs[y][x] == 0) and (flags[y][x] == 0):
                    draw(x, y)
                    opened_cells += 1
                if (bombs[y][x] == 1) and (flags[y][x] == 0):
                    game_over(c1, c2)
    return 0


def flags_count(c1, c2):   # c1 - x    c2 - y !!!!! (c2 строка c1 столбец)
    k = 0
    x_arr = [c1]
    y_arr = [c2]
    if c1 > 0:
        x_arr.append(c1 - 1)
    if c1 < w - 1:
        x_arr.append(c1 + 1)
    if c2 > 0:
        y_arr.append(c2 - 1)
    if c2 < h - 1:
        y_arr.append(c2 + 1)
    for x in x_arr:
        for y in y_arr:
            if not ((x == c1) and (y == c2)):
                k += flags[y][x]
    return k


def opening(event):   # c1 - x    c2 - y !!!!! (c2 строка c1 столбец)
    global opened_cells, flags_am
    p = event.pos
    if (p[0] % 20 == 0) or (p[1] % 20 == 0):
        return None
    c1 = p[0] // 20
    c2 = p[1] // 20
    print("opening", c1, c2, bombs[c2][c1] == 1)
    opened_cells += 1
    if check_2nd_cl(c1, c2) and flags[c2][c1] == 1:
        pg.draw.rect(sc, not_opened, pg.Rect(c1 * 20, c2 * 20, 20, 20))
        pg.display.update()
        click[c2][c1] = 0
        flags[c2][c1] = 0
        flags_am -= 1
        return 0
    if check_2nd_cl(c1, c2) and (check_0(c1, c2) or check_fl_am(c1, c2)) or check_0(c1, c2) or check_fl_am(c1, c2):
        if check_0(c1, c2):
            draw(c1, c2)
        click[c2][c1] = 1
        open_around(c1, c2)
        return 0
    if bombs[c2][c1] == 1:
        game_over(c1, c2)
    draw(c1, c2)
    click[c2][c1] = 1
    return 0


def flag(event):
    global flags_am
    p = event.pos
    c1 = p[0] // 20
    c2 = p[1] // 20
    print("flag", c1, c2)
    t = font.render("F", True, (255, 255, 255))
    pl = t.get_rect(center=(10 + c1 * 20, 10 + c2 * 20))
    pg.draw.rect(sc, bg, pg.Rect(c1 * 20, c2 * 20, 20, 20))
    sc.blit(t, pl)
    pg.display.update()
    flags[c2][c1] = 1
    click[c2][c1] = 1
    flags_am += 1
    pass


running = True
while running:
    for i in pg.event.get():
        if flags_am == bombs_amount and opened_cells == 1250 - bombs_amount:
            win()
        if i.type == pg.QUIT:
            running = False
        if i.type == pg.MOUSEBUTTONDOWN:
            if i.button == 1:
                opening(i)
            if i.button == 3:
                flag(i)

pg.quit()
quit()
