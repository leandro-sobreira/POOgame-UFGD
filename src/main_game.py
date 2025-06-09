# Importe as bibliotecas necessárias
import json
import math
import os
import pygame
import random
import sys

import setup as st
import interface as it

from games import blackjack, game_intro, uno
 

#Inicialização do Pygame
pygame.init()

# Crie o nome do jogo (exibido no superior da janela)
pygame.display.set_caption("Cassino Online UFGD")
pygame.display.set_icon(pygame.image.load(os.path.join(st.img_folder, "icon.png")))# Define o ícone da janela com uma imagem (com transparência)

# Relógio para controlar o tempo das ações no jogo
clock = pygame.time.Clock()

#Pré-configura o mixer de áudio
pygame.mixer.pre_init(44100, -16, 1, 512)# 44100 Hz de frequência, 16 bits (signed), mono, buffer de 512 bytes
pygame.mixer.init()# Inicializa o mixer de áudio com os parâmetros acima

#DISPLAY – define a resolução da janela, titulo e icone
screen_size = (st.SCREEN_WIDTH, st.SCREEN_HEIGHT)  # Largura x Altura da janela
screen = pygame.display.set_mode(screen_size)  # Cria a janela com esse tamanho

def Game():
    game_over = False


    #screen.fill(cores["preto"])  # Desenhar a tela de fundo preta  
    #intro_obj = src.game_sprites.intro(screen, "CARD GAME", "src/fonts/Ghost Shadow.ttf", 64, 1)
    #intro_time = 0
    #intro_duration = 10000  # milissegundos (10 segundos)
    #intro_running = True

    intro_screen = it.IntroScreen(screen, "CARD GAME", os.path.join(st.font_folder, "Ghost Shadow.ttf"), 64, 1)
    select_game = intro_screen.loop()

    print("Jogo selecionado:", intro_screen)
    #del intro_screen  # libera referência para coletor de lixo

    if intro_screen == 3:

        it.BlackjackScreen(screen).loop()


    


 


    '''
    opcao = src.game_intro.game_intro(screen)
    print(opcao)
    if opcao == 0:
        fim_jogo = True
    
    

    # Loop principal do menu inicial
    while not fim_jogo:
        # ⏱️ Temporizador para controlar a taxa de quadros
        clock.tick(FPS)
        

        
        # 🎮🎮✨------------------ Adicionar o loop do jogo aqui----------------✨🎮🎮
        # opcao == 3 significa BlackJack



        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                fim_jogo = True
            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE:
                    fim_jogo = True



        pygame.display.flip() # autualiza a tela
    '''
    
    

    
    game = blackjack.BlackjackGame('Lepanto')
    game.play()




    #game = UnoGame()
    #game.play()

    
    
    pygame.mouse.set_visible(True)# Ao final, mostra novamente o cursor do mouse (caso tenha sido escondido)
    pygame.mixer.music.fadeout(1000)# Encerra a música suavemente (1 segundo de fade)
    pygame.time.delay(1000)# Espera 1 segundo para garantir que o som finalize
    
    pygame.quit()# Fecha o pygame corretamente
