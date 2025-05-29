import pygame
import src.game_sprites
from src.config import clock, FPS, buttom_size, title_size, cores, escala, buttom_font


def game_intro(screen):
    

    #⛰️⛰️ background
    background = pygame.image.load("src/images/title.png").convert()
    background = pygame.transform.scale(background, screen.get_size())
    screen.blit(background, (0, 0))


    #✨✨ Titulo Com contorno Branco
    titulo_font = pygame.font.Font("src/fonts/Ghost Shadow.ttf", title_size)
    # Renderiza o texto do contorno em várias posições ao redor
    contorno_offset = 2 * escala
    for dx, dy in [(-contorno_offset, -contorno_offset), (-contorno_offset, 0), (-contorno_offset, contorno_offset),
               (0, -contorno_offset), (0, contorno_offset),
               (contorno_offset, -contorno_offset), (contorno_offset, 0), (contorno_offset, contorno_offset)]:
        contorno_surface = titulo_font.render("CARD GAME", True, cores["branco"])
        contorno_rect = contorno_surface.get_rect()
        contorno_rect.centerx = (screen.get_width() // 2) + dx
        contorno_rect.centery = (screen.get_height() // 4) + dy
        screen.blit(contorno_surface, contorno_rect)

    titulo_surface = titulo_font.render("CARD GAME", True, cores["preto"])
    rect = titulo_surface.get_rect()
    rect.centerx = screen.get_width() // 2
    rect.centery = screen.get_height() // 4
    screen.blit(titulo_surface, rect)




    #🖲️🖲️ Botões
    start_button = src.game_sprites.Button((screen.get_width()/2, screen.get_height() - (150 * escala)),"Start", cores["preto"], buttom_font, buttom_size)
    erase_button = src.game_sprites.Button((screen.get_width()/2, screen.get_height() - (110 * escala)),"Erase Data", cores["preto"], buttom_font, buttom_size)
    config_button = src.game_sprites.Button((screen.get_width()/2, screen.get_height() - (70 * escala)),"Config", cores["preto"], buttom_font, buttom_size)
    quit_button = src.game_sprites.Button((screen.get_width()/2, screen.get_height() - (30 * escala)),"Quit", cores["preto"], buttom_font, buttom_size)


    buttons = [start_button, erase_button, config_button, quit_button]# Botões em ordem
    all_sprites = pygame.sprite.Group(buttons)# Agrupar todos os sprites
    selected = [buttons[0]]   



    # 🎵🎻Configurações dos sons
    pygame.mixer.music.load("src/sounds/1197551_Butterflies.ogg") #musica de fundo da tela
    pygame.mixer.music.set_volume(0.2)
    pygame.mixer.music.play(-1)
    # Efeitos sonoros
    select_sound = pygame.mixer.Sound("src/sounds/computer-processing-sound-effects-short-click-select-02-122133.ogg") 
    ok = pygame.mixer.Sound("src/sounds/computer-processing-sound-effects-short-click-select-01-122134.ogg")
    reset = pygame.mixer.Sound("src/sounds/reset.ogg")
    select_sound.set_volume(0.5)
    ok.set_volume(0.5)
    reset.set_volume(0.5)




    #📦📦 Atribuir valores a variáveis principais
    keep_going = True
    selected = [buttons[0]]# Seleção inicial    
     

    # 🪢🪢 Laço principal
    while keep_going:
        # ⏱️ Temporizador para controlar a taxa de quadros
        clock.tick(FPS)
     
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
                        ok.play()
                        if selected == [start_button]:
                            pygame.mixer.music.fadeout(1000)  # 1000 milissegundos = 1 segundo

                            # Retornar valor para iniciar o jogo
                            game_option = game_select(screen, ok, select_sound)
                            if game_option != 0 :
                                return game_option
                            
                            
                            
                        elif selected == [quit_button]:
                            # Retornar valor para sair do jogo
                            return 0
                        elif selected == [config_button]:
                            return 2
                    else:
                        # TODO:  Definir aqui a limpeza da pontuação

                        reset.play()
                        # Redefinir pontuação
                        #save_data = open("data/highscore.txt", 'w')
                        #save_data.write(str(0))
                        #save_data.close() 



                                    
        # Destacar botão selecionado
        for select in selected:
            select.set_select()



        #🆙 Atualizar tela
        all_sprites.clear(screen, background) #tira os sprites e coloca background
        all_sprites.update()
        all_sprites.draw(screen)       
        pygame.display.flip()
        











def game_select(screen, ok, select_sound):
    screen.fill(cores["preto"])


    #🖲️🖲️ Botões
    BlackJack_button = src.game_sprites.Button((screen.get_width()/2, screen.get_height() - (200 * escala)),"Blackjack", cores["branco"], buttom_font, buttom_size)
    Quit_button = src.game_sprites.Button((screen.get_width()/2, screen.get_height() - (150 * escala)),"Quit", cores["branco"], buttom_font, buttom_size)

    buttons = [BlackJack_button, Quit_button]# Botões em ordem
    all_sprites = pygame.sprite.Group(buttons)# Agrupar todos os sprites
    selected = [buttons[0]]   


     #📦📦 Atribuir valores a variáveis principais
    keep_going = True
      






    # 🪢🪢 Laço principal
    while keep_going:
        # ⏱️ Temporizador para controlar a taxa de quadros
        clock.tick(FPS)
     
        #  Tratamento de eventos
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                keep_going = False
                # Retornar valor de saída do jogo
                return 0
            
            # Navegar pelos botões
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    if selected != [BlackJack_button]:
                        select_sound.play()
                        selected = [buttons[(buttons.index(selected[0])-1)]]
                if event.key == pygame.K_DOWN:
                    if selected != [Quit_button]:
                        select_sound.play()
                        selected = [buttons[(buttons.index(selected[0])+1)]]


                # Confirmar seleção ao pressionar Z
                if event.key == pygame.K_z:
                    if selected == [Quit_button]:
                        keep_going = False
                        ok.play()
                        
                        #HACK se ficar dando start e quit adeus memoria
                        game_intro(screen)
                    if selected == [BlackJack_button]:
                        keep_going = False
                        ok.play()
                        return 3
                    

        # Destacar botão selecionado
        for select in selected:
            select.set_select()


        # Redesenhar tela
        screen.fill(cores["preto"])
        all_sprites.update()
        all_sprites.draw(screen)
        pygame.display.update()


                    
            
