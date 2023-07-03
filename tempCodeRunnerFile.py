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
            text = font.render("Game Over!", True, (255, 0, 0))
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