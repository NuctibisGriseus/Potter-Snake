import time
import random
import pygame
import sys

pygame.init()

# задаем размеры окна и блоков змейки
display_width = 600
display_height = 600
block_size = 25

# задаем цвета заранее
white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 225)

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

yaoi_availability = True
font = pygame.font.Font('HARRYP__.TTF', 25)
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


best_score = 0


def main_menu(money, headpic, bodypic, bscore):
    menu_items = [(200, 140, 'Blitz Play', (0, 0, 0), (0, 250, 0), 0),
                  (200, 220, 'Shop and Converter', (0, 0, 0), (0, 0, 250), 1)]

    yaoi_collection = (200, 300, 'Yaoi Collection', (0, 0, 0), (250, 0, 0), 2)

    if yaoi_availability:
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
                    blitz_play(money, headpic, bodypic, bscore)
                elif item == 1:
                    shop_screen(money, headpic, bodypic, bscore)
                elif item == 2:
                    yaoi(money, headpic, bodypic, bscore)

        pointer = pygame.mouse.get_pos()
        for i in menu_items:
            if pointer[0] > i[0]:
                if pointer[0] < i[0] + 50:
                    if pointer[1] > i[1]:
                        if pointer[1] < i[1] + 50:
                            item = i[5]

        for i in menu_items:
            if item == i[5]:
                gameDisplay.blit(font.render(i[2], 1, i[4]), [i[0], i[1] - 40])
            else:
                gameDisplay.blit(font.render(i[2], 1, i[3]), [i[0], i[1] - 40])
        pygame.display.flip()


def blitz_play(money, headpic, bodypic, bscore):
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

    magix = round(random.randrange(50, 90) / block_size) * block_size
    magiy = round(random.randrange(50, 90) / block_size) * block_size
    coinx = round(random.randrange(80, 200) / block_size) * block_size
    coiny = round(random.randrange(80, 200) / block_size) * block_size
    fx = round(random.randrange(80, 500) / block_size) * block_size
    fy = round(random.randrange(80, 500) / block_size) * block_size
    sx = round(random.randrange(80, 500) / block_size) * block_size
    sy = round(random.randrange(80, 500) / block_size) * block_size

    while not gamexit:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                gamexit = True
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
                    main_menu(money, headpic, bodypic, bscore)

        # столкновение со стеной
        if lead_x >= display_width - block_size or lead_x < 0 or lead_y >= display_height - block_size or lead_y < 0:
            gameDisplay.blit(blitz, [0, 0])
            message_to_screen(''.join(["Game Over! Score: ", str(score)]), white, 100, 200)
            if score > bscore:
                bscore = score
            message_to_screen(''.join(["Best Score: ", str(bscore)]), white, 100, 250)
            pygame.display.update()
            score = 0
            lead_y = 300
            lead_x = 300
            lead_x_change = 0
            lives = 3
            lead_y_change = 0
            snakelength = 1
            snakelist.clear()

            time.sleep(2)

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
                gameDisplay.blit(blitz, [0, 0])
                message_to_screen(''.join(["Game over! Score: ", str(score)]), white, 100, 200)
                if score > bscore:
                    bscore = score
                message_to_screen(''.join(["Best Score: ", str(bscore)]), white, 100, 250)
                pygame.display.update()
                score = 0
                lead_y = 300
                lead_x = 300
                lead_x_change = 0
                lead_y_change = 0
                snakelength = 1
                lives = 3
                snakelist.clear()
                time.sleep(2)

        # столкновение с яблоком
        if lead_x == magix and lead_y == magiy:
            magix = round(random.randrange(40, 560) / block_size) * block_size
            magiy = round(random.randrange(40, 560) / block_size) * block_size
            snakelength += 1
            score += 1
        # столкновение с монеткой
        if lead_x == coinx and lead_y == coiny:
            coinx = round(random.randrange(40, 560) / block_size) * block_size
            coiny = round(random.randrange(40, 560) / block_size) * block_size
            money += 1
        # столкновение с крестражами
        if lead_x == fx and lead_y == fy:
            fx = round(random.randrange(40, 560) / block_size) * block_size
            fy = round(random.randrange(40, 560) / block_size) * block_size
            if lives > 0:
                lives -= 1
            else:
                gameDisplay.blit(blitz, [0, 0])
                message_to_screen(''.join(["Game over! Score: ", str(score)]), white, 100, 200)
                if score > bscore:
                    bscore = score
                message_to_screen(''.join(["Best Score: ", str(bscore)]), white, 100, 250)
                pygame.display.update()
                score = 0
                lead_y = 300
                lead_x = 300
                lead_x_change = 0
                lead_y_change = 0
                snakelength = 1
                lives = 3
                snakelist.clear()
                time.sleep(2)
        if lead_x == sx and lead_y == sy:
            sx = round(random.randrange(40, 560) / block_size) * block_size
            sy = round(random.randrange(40, 560) / block_size) * block_size
            if lives > 0:
                lives -= 1
            else:
                gameDisplay.blit(blitz, [0, 0])
                message_to_screen(''.join(["Game over! Score: ", str(score)]), white, 100, 200)
                if score > bscore:
                    bscore = score
                message_to_screen(''.join(["Best Score: ", str(bscore)]), white, 100, 250)
                pygame.display.update()
                score = 0
                lead_y = 300
                lead_x = 300
                lead_x_change = 0
                lead_y_change = 0
                snakelength = 1
                lives = 3
                snakelist.clear()
                time.sleep(2)
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
        # отображение змейки
        snake(headpic, bodypic, snakelist, snakehead, lead_x, lead_y)

        pygame.display.update()
        pygame.time.delay(300)


def shop_screen(money, headpic, bodypic, bscore):
    buttons = [(160, 80, f" Harry Potter : Free", black, red, 2),
               (160, 140, f" N.E.E.T. : 2 Galeons", black, red, 3),
               (160, 200, f" Ron Weasly : 10 Galeons", black, red, 4),
               (160, 260, f" Hermione Granger : 15 Galeons", black, red, 5),
               (160, 320, f" Dumbldore : 30 Galeons", black, red, 6),
               (20, 50, 'Home', white, blue, 33)]
    pygame.key.set_repeat()
    pygame.mouse.set_visible(True)
    done = False
    n_bought = False
    r_bought = False
    h_bought = False
    d_bought = False
    item = 4
    while not done:
        gameDisplay.blit(shop, [0, 0])
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                main_menu(money, headpic, bodypic, bscore)
            if e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:
                if item == 3:
                    if n_bought:
                        headpic = headneet
                        bodypic = bodyneet
                    else:
                        if money >= 2:
                            money -= 2
                            headpic = headneet
                            bodypic = bodyneet
                            n_bought = True
                elif item == 4:
                    if r_bought:
                        headpic = headron
                        bodypic = bodyron
                    else:
                        if money >= 10:
                            money -= 10
                            headpic = headron
                            bodypic = bodyron
                            r_bought = True
                elif item == 5:
                    if h_bought:
                        headpic = headhermi
                        bodypic = bodyhermi
                    else:
                        if money >= 15:
                            money -= 15
                            headpic = headhermi
                            bodypic = bodyhermi
                            h_bought = True
                elif item == 6:
                    if d_bought:
                        headpic = dumblehead
                        bodypic = dumblebody
                    else:
                        if money >= 30:
                            money -= 30
                            headpic = dumblehead
                            bodypic = dumblebody
                            d_bought = True
                elif item == 2:
                    headpic = headharry
                    bodypic = bodyharry

                elif item == 33:
                    main_menu(money, headpic, bodypic, bscore)
        gameDisplay.blit(pygame.image.load("Harry Potter head.png"), [100, 35])
        gameDisplay.blit(pygame.image.load("Neet.png"), [100, 100])
        gameDisplay.blit(pygame.image.load("Ron_head.png"), [85, 145])
        gameDisplay.blit(pygame.image.load("Hermi.png"), [90, 210])
        gameDisplay.blit(pygame.image.load("Dumldore.png"), [95, 275])
        message_to_screen(''.join(["Galeons: ", str(money)]), black, 500, 10)
        pointer = pygame.mouse.get_pos()
        for i in buttons:
            if pointer[0] > i[0]:
                if pointer[0] < i[0] + 50:
                    if pointer[1] > i[1]:
                        if pointer[1] < i[1] + 50:
                            item = i[5]

        for i in buttons:
            if item == i[5]:
                gameDisplay.blit(font.render(i[2], 1, i[4]), [i[0], i[1] - 40])
            else:
                gameDisplay.blit(font.render(i[2], 1, i[3]), [i[0], i[1] - 40])
        pygame.display.flip()


def yaoi(money, headpic, bodypic, bscore):
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
    item = ''
    home = (20, 50, 'Home', white, white, 33)
    pygame.key.set_repeat()
    pygame.mouse.set_visible(True)
    done = False
    gameDisplay.blit(y, [0, 0])
    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                main_menu(money, headpic, bodypic, bscore)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    if pos == 0:
                        pos = 27
                    else:
                        pos -= 1
                    gameDisplay.blit(pygame.image.load(pictures[pos]), [0, 0])
                elif event.key == pygame.K_RIGHT:
                    if pos == 27:
                        pos = 0
                    else:
                        pos += 1
                    gameDisplay.blit(pygame.image.load(pictures[pos]), [0, 0])
                elif event.key == pygame.K_ESCAPE:
                    main_menu(money, headpic, bodypic, bscore)
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if item == 33:
                        main_menu(money, headpic, bodypic, bscore)
                pointer = pygame.mouse.get_pos()
                if pointer[0] > home[0]:
                    if pointer[0] < home[0] + 50:
                        if pointer[1] > home[1]:
                            if pointer[1] < home[1] + 50:
                                item = home[5]

                if item == home[5]:
                    gameDisplay.blit(font.render(home[2], 1, home[4]), [home[0], home[1] - 40])
                else:
                    gameDisplay.blit(font.render(home[2], 1, home[3]), [home[0], home[1] - 40])
            pygame.display.flip()


main_menu(0, headharry, bodyharry, best_score)
