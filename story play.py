import pygame


def story_play(money, headpic, bodypic, bscore):
    levels = [(160, 140, 'Level 1', (0, 0, 0), (0, 255, 0), 0),
              (160, 240, 'Level 2', (0, 0, 0), (250, 0, 0), 1),
              (160, 340, 'Level 3', (0, 0, 0), (0, 0, 250), 2)]

    pygame.key.set_repeat()
    pygame.mouse.set_visible(True)
    done = False
    item = 0
    while not done:
        gameDisplay.blit(storyplay, [0, 0])
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                main_menu(money, headpic, bodypic, bscore)
            if e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:
                if item == 0:
                    level_1()
                elif item == 1:
                    level_2()
                elif item == 2:
                    level_3()

        pointer = pygame.mouse.get_pos()
        for i in levels:
            if pointer[0] > i[0]:
                if pointer[0] < i[0] + 50:
                    if pointer[1] > i[1]:
                        if pointer[1] < i[1] + 50:
                            item = i[5]