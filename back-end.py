import random
import math
from typing import List, Tuple
import pygame
from pygame.locals import (
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    KEYDOWN,
    QUIT,
)

pygame.init()

Anneau = Tuple[float, float, str]
fru = Tuple[float, float, bool]  # Les coordonnees et si oui ou non le fruit est mangé
blocks_init = 3
taille_case = 20
nb_case = 50
screen = pygame.display.set_mode([nb_case * taille_case, nb_case * taille_case])
pygame.mixer.init()
pygame.mixer.music.load('song.wav')
pygame.mixer.music.set_volume(0.2)


class snake:
    def __init__(self):
        self.nb_blocks = blocks_init
        self.pos_blocks: List[Anneau] = [(2, 1, 'e'), (1, 1, 'e'), (0, 1, 'e')]


class fruits:
    def __init__(self):
        self.couleur: Tuple[int, int, int] = (255, 50, 100)
        self.pos: fru


def deplace_une_case(case: Anneau, direct: str) -> Anneau:
    x, y, _ = case
    if direct == 'n':
        return x, y - 1, direct
    if direct == 'e':
        return x + 1, y, direct
    if direct == 's':
        return x, y + 1, direct
    if direct == 'o':
        return x - 1, y, direct


def deplace_snake(sn: snake, direc: str):
    x: float
    y: float
    dir1: str
    dir2: str
    if direc == 'n':
        for i1 in range(sn.nb_blocks):
            if i1 == 0:
                _, _, dir1 = sn.pos_blocks[i1]
                sn.pos_blocks[i1] = deplace_une_case(sn.pos_blocks[i1], 'n')
            else:
                _, _, dir2 = sn.pos_blocks[i1]
                sn.pos_blocks[i1] = deplace_une_case(sn.pos_blocks[i1], dir1)
                dir1 = dir2
    elif direc == 's':
        for i2 in range(sn.nb_blocks):
            if i2 == 0:
                _, _, dir1 = sn.pos_blocks[i2]
                sn.pos_blocks[i2] = deplace_une_case(sn.pos_blocks[i2], 's')
            else:
                _, _, dir2 = sn.pos_blocks[i2]
                sn.pos_blocks[i2] = deplace_une_case(sn.pos_blocks[i2], dir1)
                dir1 = dir2
    elif direc == 'e':
        for i3 in range(sn.nb_blocks):
            if i3 == 0:
                _, _, dir1 = sn.pos_blocks[i3]
                sn.pos_blocks[i3] = deplace_une_case(sn.pos_blocks[i3], 'e')
            else:
                _, _, dir2 = sn.pos_blocks[i3]
                sn.pos_blocks[i3] = deplace_une_case(sn.pos_blocks[i3], dir1)
                dir1 = dir2
    elif direc == 'o':
        for i4 in range(sn.nb_blocks):
            if i4 == 0:
                _, _, dir1 = sn.pos_blocks[i4]
                sn.pos_blocks[i4] = deplace_une_case(sn.pos_blocks[i4], 'o')
            else:
                _, _, dir2 = sn.pos_blocks[i4]
                sn.pos_blocks[i4] = deplace_une_case(sn.pos_blocks[i4], dir1)
                dir1 = dir2


sn = snake()
fr = fruits()


def rand_fruit(fr1: fruits) -> fruits:
    global nb_case
    global taille_case
    d: float = taille_case / 2
    x: float = int((random.random() * 10 * nb_case) % nb_case)
    y: float = int((random.random() * 10 * nb_case) % nb_case)
    fr1.pos = (x * taille_case + d, y * taille_case + d, False)
    fr1.couleur = (255, 50, 100)
    return fr1


fr = rand_fruit(fr)


def add_anneau(sn: snake) -> snake:
    global taille_case
    x1, y1, dir1 = sn.pos_blocks[sn.nb_blocks - 1]
    sn.nb_blocks = sn.nb_blocks + 1
    if dir1 == 'n':
        sn.pos_blocks.append((x1, y1 + 1, dir1))
        return sn
    elif dir1 == "e":
        sn.pos_blocks.append((x1 - 1, y1, dir1))
        return sn
    elif dir1 == "s":
        sn.pos_blocks.append((x1, y1 - 1, dir1))
        return sn
    elif dir1 == "o":
        sn.pos_blocks.append((x1 + 1, y1, dir1))
        return sn


def affichage_and_back_end():
    global sn
    global screen
    global taille_case
    global fr
    global nb_case
    run: bool = True
    x: float
    y: float
    x1: float
    y1: float
    x0: float
    y0: float
    eaten: bool
    direct: str
    d: float = taille_case / 2
    cmpt: int = 0
    game_over: bool = False  # New variable to track game over state

    while run:
        if (cmpt % 50) == 0 and not game_over:
            _, _, direct = sn.pos_blocks[0]
            deplace_snake(sn, direct)
        if cmpt % 50000 == 0:
            pygame.mixer.music.play()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == KEYDOWN:
                if not game_over:  # Only allow movement if game is not over
                    if event.key == K_UP:
                        deplace_snake(sn, 'n')
                    elif event.key == K_DOWN:
                        deplace_snake(sn, 's')
                    elif event.key == K_LEFT:
                        deplace_snake(sn, 'o')
                    elif event.key == K_RIGHT:
                        deplace_snake(sn, 'e')
                if event.key == K_ESCAPE:  # Allow player to exit game with Esc key
                    run = False

        screen.fill((100, 255, 100))
        for i in range(sn.nb_blocks):
            x, y, _ = sn.pos_blocks[i]
            if i == 0:
                if x <= 0 or y <= 0 or x >= nb_case or y >= nb_case:
                    game_over = True
                    break
                x0 = x * taille_case + d
                y0 = y * taille_case + d
                pygame.draw.rect(screen, (100, 100, 255), (x * taille_case, y * taille_case, taille_case, taille_case))
            else:
                pygame.draw.rect(screen, (255, 100, 55), (x * taille_case, y * taille_case, taille_case, taille_case))

        if game_over:  # Display game over message
            font = pygame.font.Font(None, 36)
            text = font.render("Game Over! Press 'ESC' to exit", True, (255, 0, 0))
            text_rect = text.get_rect(center=(nb_case * taille_case // 2, nb_case * taille_case // 2))
            screen.blit(text, text_rect)
        else:
            cmpt += 1
            x1, y1, eaten = fr.pos
            if cmpt % 100 == 0 and eaten == True:
                fr = rand_fruit(fr)

            if (((math.sqrt((x0 - x1) ** 2 + (y0 - y1) ** 2)) <= d) and eaten == False):
                sn = add_anneau(sn)
                fr.pos = (x1, y1, True)

            if eaten == False:
                pygame.draw.circle(screen, fr.couleur, (x1, y1), taille_case / 2)  # On multiplie pour l'echelle

        pygame.display.flip()

        pygame.time.delay(4) # Increase this value to slow down the snake
    pygame.quit()


def main():
    global screen
    global sn
    affichage_and_back_end()


main()
