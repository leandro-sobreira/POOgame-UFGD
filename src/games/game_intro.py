import pygame
import os
import interface as it
import setup as st

def game_intro2(screen):
    pass

def game_intro(screen):

    #background

    background = pygame.image.load(os.path.join(st.img_folder, "title.png")).convert()
    background = pygame.transform.scale(background, screen.get_size())
    screen.blit(background, (0, 0))

    #Titulo Com contorno Branco
    title_font = pygame.font.Font(os.path.join(st.font_folder, "Ghost Shadow.ttf"), st.title_size)
    # Renderiza o texto do contorno em várias posições ao redor
    outline_offset = 2 * st.SCALE

    for dx, dy in [(-outline_offset, -outline_offset), (-outline_offset, 0), (-outline_offset, outline_offset),
               (0, -outline_offset), (0, outline_offset),
               (outline_offset, -outline_offset), (outline_offset, 0), (outline_offset, outline_offset)]:
        
        outline_surface = title_font.render("CARD GAME", True, st.WHITE)
        outline_rect = outline_surface.get_rect()
        outline_rect.centerx = (screen.get_width() // 2) + dx
        outline_rect.centery = (screen.get_height() // 4) + dy
        screen.blit(outline_surface, outline_rect)

    title_surface = title_font.render("CARD GAME", True, st.BLACK)
    rect = title_surface.get_rect()
    rect.centerx = screen.get_width() // 2
    rect.centery = screen.get_height() // 4
    screen.blit(title_surface, rect)

    #Botões
    
    start_button = it.Button((screen.get_width()/2, screen.get_height() - (150 * st.SCALE)),"Start", st.BLACK, st.button_font, st.button_size)
    erase_button = it.Button((screen.get_width()/2, screen.get_height() - (110 * st.SCALE)),"Erase Data", st.BLACK, st.button_font, st.button_size)
    config_button = it.Button((screen.get_width()/2, screen.get_height() - (70 * st.SCALE)),"Config", st.BLACK, st.button_font, st.button_size)
    quit_button = it.Button((screen.get_width()/2, screen.get_height() - (30 * st.SCALE)),"Quit", st.BLACK, st.button_font, st.button_size)

    buttons = [start_button, erase_button, config_button, quit_button]# Botões em ordem
    all_sprites = pygame.sprite.Group(buttons)# Agrupar todos os sprites
    selected = [buttons[0]]   

    #Configurações dos sons
    pygame.mixer.music.load(os.path.join(st.sound_folder, "1197551_Butterflies.ogg")) #musica de fundo da tela
    pygame.mixer.music.set_volume(0.2)
    pygame.mixer.music.play(-1)

    # Efeitos sonoros
    select_sound = pygame.mixer.Sound(os.path.join(st.sound_folder, "computer-processing-sound-effects-short-click-select-02-122133.ogg")) 
    ok_sound = pygame.mixer.Sound(os.path.join(st.sound_folder, "computer-processing-sound-effects-short-click-select-01-122134.ogg"))
    reset_sound = pygame.mixer.Sound(os.path.join(st.sound_folder, "reset.ogg"))

    select_sound.set_volume(0.5)
    ok_sound.set_volume(0.5)
    reset_sound.set_volume(0.5)

    #Atribuir valores a variáveis principais
    keep_going = True
    selected = [buttons[0]]# Seleção inicial    
     

    #Laço principal
    while keep_going:
        #Temporizador para controlar a taxa de quadros
        st.clock.tick(st.FPS)
     
        #  Tratamento de eventos
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                keep_going = False
                # Retornar valor de saída do jogo
                return 0
            

            # Navegar pelos botões
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    if selected != [start_button]:
                        select_sound.play()
                        selected = [buttons[(buttons.index(selected[0])-1)]]
                if event.key == pygame.K_DOWN:
                    if selected != [quit_button]:
                        select_sound.play()
                        selected = [buttons[(buttons.index(selected[0])+1)]]




                # Confirmar seleção ao pressionar Z
                if event.key == pygame.K_z:
                    if selected != [erase_button]:
                        keep_going = False
                        ok_sound.play()
                        if selected == [start_button]:
                            pygame.mixer.music.fadeout(1000)  # 1000 milissegundos = 1 segundo

                            # Retornar valor para iniciar o jogo
                            game_option = game_select(screen, ok_sound, select_sound)
                            if game_option != 0 :
                                return game_option
                            
                            
                            
                        elif selected == [quit_button]:
                            # Retornar valor para sair do jogo
                            return 0
                        elif selected == [config_button]:
                            return 2
                    else:
                        # TODO:  Definir aqui a limpeza da pontuação

                        reset_sound.play()
                        # Redefinir pontuação
                        #save_data = open("data/highscore.txt", 'w')
                        #save_data.write(str(0))
                        #save_data.close() 



                                    
        # Destacar botão selecionado
        for select in selected:
            select.set_select()



        #Atualizar tela
        all_sprites.clear(screen, background) #tira os sprites e coloca background
        all_sprites.update()
        all_sprites.draw(screen)       
        pygame.display.flip()
        

def game_select(screen, ok_sound, select_sound):
    screen.fill(st.BLACK)

    #Botões
    blackjack_button = it.Button((screen.get_width()/2, screen.get_height() - (200 * st.SCALE)),"Blackjack", st.WHITE, st.button_font, st.button_size)
    quit_button = it.Button((screen.get_width()/2, screen.get_height() - (150 * st.SCALE)),"Quit", st.WHITE, st.button_font, st.button_size)

    buttons = [blackjack_button, quit_button]# Botões em ordem
    all_sprites = pygame.sprite.Group(buttons)# Agrupar todos os sprites
    selected = [buttons[0]]   

    # Atribuir valores a variáveis principais
    keep_going = True
     
    # Laço principal
    while keep_going:
        # Temporizador para controlar a taxa de quadros
        st.clock.tick(st.FPS)
     
        #  Tratamento de eventos
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                keep_going = False
                # Retornar valor de saída do jogo
                return 0
            
            # Navegar pelos botões
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    if selected != [blackjack_button]:
                        select_sound.play()
                        selected = [buttons[(buttons.index(selected[0])-1)]]
                if event.key == pygame.K_DOWN:
                    if selected != [quit_button]:
                        select_sound.play()
                        selected = [buttons[(buttons.index(selected[0])+1)]]


                # Confirmar seleção ao pressionar Z
                if event.key == pygame.K_z:
                    if selected == [quit_button]:
                        keep_going = False
                        ok_sound.play()
                        
                        #HACK se ficar dando start e quit adeus memoria
                        game_intro(screen)
                    if selected == [blackjack_button]:
                        keep_going = False
                        ok_sound.play()
                        return 3
                    

        # Destacar botão selecionado
        for select in selected:
            select.set_select()


        # Redesenhar tela
        screen.fill(st.BLACK)
        all_sprites.update()
        all_sprites.draw(screen)
        pygame.display.update()


                    
            
