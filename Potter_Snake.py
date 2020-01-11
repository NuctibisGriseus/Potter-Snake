import time
import random
import pygame
import sys

pygame.init()

# задаем размеры окна и блоков змейки
display_width = 600
display_height = 600
block_size = 25

# Слышите - музычка!
pygame.mixer.music.load('Я съем твой мозг.mp3')
pygame.mixer.music.play(-1)
pygame.mixer.music.set_volume(0.1)

blink_sound = pygame.mixer.Sound('blinc.wav')
select_sound = pygame.mixer.Sound('select.wav')
game_over = pygame.mixer.Sound('game_over.wav')
minus_life = pygame.mixer.Sound('crestrage_collide.wav')
buy = pygame.mixer.Sound('buy.wav')

# задаем цвета заранее
white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 225)

# Куплены ли персонажи?
n_bought = False
r_bought = False
h_bought = False
d_bought = False
m_bought = False

# заливаем картинки крестражей
slyth_medal = pygame.image.load("medal.png")
hufp_gls = pygame.image.load("chacha.png")
ravclo = pygame.image.load("diadema.png")
rise_stone = pygame.image.load("ring.png")
nagi = pygame.image.load("nagaina.png")
tmr_diary = pygame.image.load("diary.png")
scar = pygame.image.load("Scar.png")

# создаем окно
gameDisplay = pygame.display.set_mode((600, 600))
pygame.display.set_caption("Harry Potter - Snake")

yaoi_availability = False
font = pygame.font.Font('HARRYP__.TTF', 25)
f1 = pygame.font.Font('HARRYP__.TTF', 60)
gameExit = False


def message_to_screen(message, color, x, y):
    screen_text = font.render(message, True, color)
    gameDisplay.blit(screen_text, [x, y])


def snake(headim, bodyim, snakelist, snakehead, lead_x, lead_y):
    for XnY in snakelist:
        gameDisplay.blit(pygame.image.load(bodyim), XnY)
        gameDisplay.blit(pygame.image.load(headim), [lead_x, lead_y])


# фоны
menu = pygame.image.load("menu.jpg")
shop = pygame.image.load("shop.jpg")
blitz = pygame.image.load("blitz.png")
y = pygame.image.load("Картинки для пасхалки\y1.jpg")

# количество галеонов
galeon = 0

# костюмы персонажей
headharry = "Harry Potter Head.png"
bodyharry = 'Harry Potter Body.png'
headneet = 'Neet.png'
bodyneet = 'N_body.png'
headron = "Ron_head.png"
bodyron = 'Ron_body.png'
headhermi = 'Hermi.png'
bodyhermi = 'Hermi Body.png'
dumblehead = 'Dumldore.png'
dumblebody = 'D_body.png'
dracohead = "malfoy_head.png"
dracobody = 'malfoy_body.png'


best_score = 0


def main_menu(money, headpic, bodypic, bscore, yi, n, r, h, d, m):
    menu_items = [(200, 160, 'Blitz Play', (0, 0, 0), (0, 250, 0), 0),
                  (200, 240, 'Shop and Converter', (0, 0, 0), (0, 0, 250), 1)]

    yaoi_collection = (200, 320, 'Yaoi Collection', (0, 0, 0), (250, 0, 0), 2)

    if yi:
        menu_items.append(yaoi_collection)
    pygame.key.set_repeat()
    pygame.mouse.set_visible(True)

    done = False
    item = 0
    while not done:
        gameDisplay.blit(menu, [0, 0])
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:
                if item == 0:
                    select_sound.play()
                    blitz_play(money, headpic, bodypic, bscore, yi, n, r, h, d, m)
                elif item == 1:
                    select_sound.play()
                    shop_screen(money, headpic, bodypic, bscore, yi, n, r, h, d, m)
                elif item == 2:
                    select_sound.play()
                    yaoi(money, headpic, bodypic, bscore, yi, n, r, h, d, m)

        pointer = pygame.mouse.get_pos()
        for i in menu_items:
            if pointer[0] > i[0]:
                if pointer[0] < i[0] + 50:
                    if pointer[1] > i[1]:
                        if pointer[1] < i[1] + 50:
                            item = i[5]

        gameDisplay.blit(f1.render('Harry Potter - Snake', 1, (0, 0, 0)), [21, 12])
        gameDisplay.blit(f1.render('Harry Potter - Snake', 1, (235, 196, 0)), [20, 12])

        for i in menu_items:
            if item == i[5]:
                gameDisplay.blit(font.render(i[2], 1, i[4]), [i[0], i[1] - 40])
            else:
                gameDisplay.blit(font.render(i[2], 1, i[3]), [i[0], i[1] - 40])
        pygame.display.flip()


def your_game_is_over(money, headpic, bodypic, bscore, yi, n, r, h, d, m, score):
    pygame.mixer.music.pause()
    game_over.play()
    gameDisplay.blit(blitz, [0, 0])
    message_to_screen(''.join(["Game Over! Score: ", str(score)]), white, 100, 200)
    if score > bscore:
        bscore = score
    message_to_screen(''.join(["Best Score: ", str(bscore)]), white, 100, 250)
    message_to_screen('Press "Escape" To Come Back To Menu', white, 100, 300)
    pygame.display.update()
    time.sleep(5)
    pygame.mixer.music.play(-1)
    blitz_play(money, headpic, bodypic, bscore, yi, n, r, h, d, m)


def blitz_play(money, headpic, bodypic, bscore, yi, n, r, h, d, m):
    # координаты головы змейки
    lead_x = display_width / 2
    lead_y = display_height / 2

    # переменные, отвечающие за направление движения змейки
    lead_x_change = 0
    lead_y_change = 0

    gamexit = False

    snakelist = []
    snakelength = 1

    lives = 3
    score = 0

    crestrages = [ravclo, slyth_medal, tmr_diary, scar, nagi, hufp_gls, rise_stone]
    first_crest = random.choice(crestrages)
    crestrages.pop(crestrages.index(first_crest))
    second_crest = random.choice(crestrages)
    crestrages.pop(crestrages.index(second_crest))
    third_crest = random.choice(crestrages)
    crestrages.pop(crestrages.index(third_crest))

    magix = round(random.randrange(50, 90) / block_size) * block_size
    magiy = round(random.randrange(50, 90) / block_size) * block_size
    coinx = round(random.randrange(80, 200) / block_size) * block_size
    coiny = round(random.randrange(80, 200) / block_size) * block_size
    fx = round(random.randrange(80, 500) / block_size) * block_size
    fy = round(random.randrange(80, 500) / block_size) * block_size
    sx = round(random.randrange(80, 500) / block_size) * block_size
    sy = round(random.randrange(80, 500) / block_size) * block_size
    thx = round(random.randrange(80, 500) / block_size) * block_size
    thy = round(random.randrange(80, 500) / block_size) * block_size

    while not gamexit:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                main_menu(money, headpic, bodypic, bscore, yi, n, r, h, d, m)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    lead_x_change = -block_size
                    lead_y_change = 0
                elif event.key == pygame.K_RIGHT:
                    lead_x_change = block_size
                    lead_y_change = 0
                elif event.key == pygame.K_DOWN:
                    lead_x_change = 0
                    lead_y_change = block_size
                elif event.key == pygame.K_UP:
                    lead_x_change = 0
                    lead_y_change = -block_size
                elif event.key == pygame.K_ESCAPE:
                    main_menu(money, headpic, bodypic, bscore, yi, n, r, h, d, m)

        # столкновение со стеной
        if lead_x >= display_width - block_size or lead_x < 0 or lead_y >= display_height - block_size or lead_y < 0:
            your_game_is_over(money, headpic, bodypic, bscore, yi, n, r, h, d, m, score)

        # движение змейки
        lead_x += lead_x_change
        lead_y += lead_y_change
        snakehead = [lead_x, lead_y]
        snakelist.append(snakehead)
        if len(snakelist) > snakelength:
            del snakelist[0]

        # столкновение змейки с самой собой
        for eachSegment in snakelist[:-1]:
            if eachSegment == snakehead:
                your_game_is_over(money, headpic, bodypic, bscore, yi, n, r, h, d, m, score)

        # столкновение с магией
        if lead_x == magix and lead_y == magiy:
            blink_sound.play()
            magix = round(random.randrange(40, 560) / block_size) * block_size
            magiy = round(random.randrange(40, 560) / block_size) * block_size
            snakelength += 1
            score += 1
        # столкновение с галеоном
        if lead_x == coinx and lead_y == coiny:
            blink_sound.play()
            coinx = round(random.randrange(40, 560) / block_size) * block_size
            coiny = round(random.randrange(40, 560) / block_size) * block_size
            money += 1
        # столкновение с крестражами
        if lead_x == fx and lead_y == fy:
            fx = round(random.randrange(40, 560) / block_size) * block_size
            fy = round(random.randrange(40, 560) / block_size) * block_size
            if lives > 1:
                minus_life.play()
                lives -= 1
            else:
                your_game_is_over(money, headpic, bodypic, bscore, yi, n, r, h, d, m, score)
        if lead_x == sx and lead_y == sy:
            sx = round(random.randrange(40, 560) / block_size) * block_size
            sy = round(random.randrange(40, 560) / block_size) * block_size
            if lives > 1:
                minus_life.play()
                lives -= 1
            else:
                your_game_is_over(money, headpic, bodypic, bscore, yi, n, r, h, d, m, score)
        if lead_x == thx and lead_y == thy:
            thx = round(random.randrange(40, 560) / block_size) * block_size
            thy = round(random.randrange(40, 560) / block_size) * block_size
            if lives > 1:
                minus_life.play()
                lives -= 1
            else:
                your_game_is_over(money, headpic, bodypic, bscore, yi, n, r, h, d, m, score)
        gameDisplay.blit(blitz, [0, 0])
        # отображение количества очков
        message_to_screen(''.join(["Score: ", str(score)]), white, 10, 10)
        message_to_screen(''.join(["Galeons: ", str(money)]), white, 100, 10)
        message_to_screen(''.join(["Lives: ", str(lives)]), white, 210, 10)

        # отображение яблока
        gameDisplay.blit(pygame.image.load("Magic.png"), [magix, magiy])
        gameDisplay.blit(pygame.image.load("Galeon.png"), [coinx, coiny])
        # отображение крестража
        gameDisplay.blit(first_crest, [fx, fy])
        gameDisplay.blit(second_crest, [sx, sy])
        gameDisplay.blit(third_crest, [thx, thy])
        # отображение змейки
        snake(headpic, bodypic, snakelist, snakehead, lead_x, lead_y)

        pygame.display.update()
        pygame.time.delay(300)


def shop_screen(money, headpic, bodypic, bscore, yi, n, r, h, d, m):
    buttons = [[160, 80, " Harry Potter : Free", black, red, 2, True],
               [160, 140, " N.E.E.T. : 2 Galeons", black, red, 3, False],
               [160, 200, " Ron Weasly : 10 Galeons", black, red, 4, False],
               [160, 260, " Hermione Granger : 15 Galeons", black, red, 5, False],
               [160, 320, " Dumbldore : 30 Galeons", black, red, 6, False],
               [160, 380, " Draco : 30 Galeons", black, red, 7, False],
               [20, 50, 'Home', white, blue, 33]]
    pygame.key.set_repeat()
    pygame.mouse.set_visible(True)
    done = False
    item = 4
    j = [n, r, h, d, m]
    k = buttons[1:6]
    for i in k:
        if i[-1] != j[k.index(i)]:
            i[-1] = j[k.index(i)]

    while not done:
        gameDisplay.blit(shop, [0, 0])
        message_to_screen('Home', black, 21, 11)
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                main_menu(money, headpic, bodypic, bscore, yi, n, r, h, d, m)
            if e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:
                if item == 3:
                    if n:
                        select_sound.play()
                        headpic = headneet
                        bodypic = bodyneet
                    else:
                        if money >= 2:
                            buy.play()
                            money -= 2
                            headpic = headneet
                            bodypic = bodyneet
                            n = True
                            k = buttons[1]
                            k[-1] = True
                elif item == 4:
                    if r:
                        select_sound.play()
                        headpic = headron
                        bodypic = bodyron
                    else:
                        if money >= 10:
                            buy.play()
                            money -= 10
                            headpic = headron
                            bodypic = bodyron
                            r = True
                            k = buttons[2]
                            k[-1] = True
                elif item == 5:
                    if h:
                        select_sound.play()
                        headpic = headhermi
                        bodypic = bodyhermi
                    else:
                        if money >= 15:
                            buy.play()
                            money -= 15
                            headpic = headhermi
                            bodypic = bodyhermi
                            h = True
                            k = buttons[3]
                            k[-1] = True
                elif item == 6:
                    if d:
                        select_sound.play()
                        headpic = dumblehead
                        bodypic = dumblebody
                    else:
                        if money >= 30:
                            buy.play()
                            money -= 30
                            headpic = dumblehead
                            bodypic = dumblebody
                            d = True
                            k = buttons[4]
                            k[-1] = True
                elif item == 7:
                    if m:
                        select_sound.play()
                        headpic = dracohead
                        bodypic = dracobody
                    else:
                        if money >= 30:
                            buy.play()
                            money -= 30
                            headpic = dracohead
                            bodypic = dracobody
                            m = True
                            k = buttons[5]
                            k[-1] = True
                elif item == 2:
                    select_sound.play()
                    headpic = headharry
                    bodypic = bodyharry

                elif item == 33:
                    select_sound.play()
                    main_menu(money, headpic, bodypic, bscore, yi, n, r, h, d, m)
                if n and h and d and r and m is True:
                    yi = True
        gameDisplay.blit(pygame.image.load("Harry Potter head.png"), [100, 35])
        gameDisplay.blit(pygame.image.load("Neet.png"), [100, 100])
        gameDisplay.blit(pygame.image.load("Ron_head.png"), [85, 145])
        gameDisplay.blit(pygame.image.load("Hermi.png"), [90, 210])
        gameDisplay.blit(pygame.image.load("Dumldore.png"), [95, 275])
        gameDisplay.blit(pygame.image.load("malfoy_head.png"), [100, 330])
        message_to_screen(''.join(["Galeons: ", str(money)]), black, 485, 10)
        pointer = pygame.mouse.get_pos()
        for i in buttons:
            if pointer[0] > i[0]:
                if pointer[0] < i[0] + 50:
                    if pointer[1] > i[1]:
                        if pointer[1] < i[1] + 50:
                            item = i[5]

        for i in buttons:
            if not i[-1]:
                if item == i[5]:
                    gameDisplay.blit(font.render(i[2], 1, i[4]), [i[0], i[1] - 40])
                else:
                    gameDisplay.blit(font.render(i[2], 1, i[3]), [i[0], i[1] - 40])
            else:
                if item == i[5]:
                    gameDisplay.blit(font.render(i[2], 1, (235, 196, 0)), [i[0], i[1] - 40])
                else:
                    gameDisplay.blit(font.render(i[2], 1, (214, 118, 9)), [i[0], i[1] - 40])
        pygame.display.flip()


def yaoi(money, headpic, bodypic, bscore, yi, n, r, h, d, m):
    pictures = ['Картинки для пасхалки\drarry.jpg', 'Картинки для пасхалки\drarry1.jpg',
                'Картинки для пасхалки\js.jpg', 'Картинки для пасхалки\dg.jpg',
                'Картинки для пасхалки\ksts.jpg', 'Картинки для пасхалки\ewt1.jpg',
                'Картинки для пасхалки\snape.jpg', 'Картинки для пасхалки\томми.jpg',
                'Картинки для пасхалки\т1.jpg', 'Картинки для пасхалки\волди.jpg',
                'Картинки для пасхалки\drarry2.jpg', 'Картинки для пасхалки\drarry3.jpg',
                'Картинки для пасхалки\drarry4.jpg', 'Картинки для пасхалки\y2.jpg',
                'Картинки для пасхалки\ls.jpg', 'Картинки для пасхалки\ls2.jpg',
                'Картинки для пасхалки\drarre5.jpg', 'Картинки для пасхалки\snarre.jpg',
                'Картинки для пасхалки\luci.jpg', 'Картинки для пасхалки\ewt.jpg',
                'Картинки для пасхалки\drarry6.jpg', 'Картинки для пасхалки\drarry comic.jpg',
                'Картинки для пасхалки\oppachki.jpg', 'Картинки для пасхалки\y3.jpg',
                'Картинки для пасхалки\snarry.jpg', 'Картинки для пасхалки\y1.jpg',
                'Картинки для пасхалки\гаррерон.jpg', 'Картинки для пасхалки\снарре.jpg']

    pos = 0
    home = (20, 50, 'Press "Escape" To Return To The Menu', (235, 196, 0), black, 33)
    pygame.key.set_repeat()
    pygame.mouse.set_visible(True)
    done = False
    gameDisplay.blit(y, [0, 0])
    gameDisplay.blit(font.render(home[2], 1, home[4]), [home[0], home[1] - 40])
    gameDisplay.blit(font.render(home[2], 1, home[3]), [home[0], home[1] - 41])
    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                main_menu(money, headpic, bodypic, bscore, yi, n, r, h, d)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    select_sound.play()
                    if pos == 0:
                        pos = 27
                    else:
                        pos -= 1
                    gameDisplay.blit(pygame.image.load(pictures[pos]), [0, 0])
                elif event.key == pygame.K_RIGHT:
                    select_sound.play()
                    if pos == 27:
                        pos = 0
                    else:
                        pos += 1
                    gameDisplay.blit(pygame.image.load(pictures[pos]), [0, 0])
                elif event.key == pygame.K_ESCAPE:
                    main_menu(money, headpic, bodypic, bscore, yi, n, r, h, d, m)

                gameDisplay.blit(font.render(home[2], 1, home[4]), [home[0], home[1] - 40])
                gameDisplay.blit(font.render(home[2], 1, home[3]), [home[0], home[1] - 41])

            pygame.display.flip()


main_menu(galeon, headharry, bodyharry, best_score, yaoi_availability, n_bought, r_bought, h_bought, d_bought, m_bought)
