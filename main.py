import pygame
import src.game_intro, src.game_sprites
from src.config import cores, tela_altura, tela_largura, clock, FPS
from src.game_sprites import intro, Telacartas




# 🎻🎵 Pré-configura o mixer de áudio:
pygame.mixer.pre_init(44100, -16, 1, 512)# 44100 Hz de frequência, 16 bits (signed), mono, buffer de 512 bytes
pygame.mixer.init()# Inicializa o mixer de áudio com os parâmetros acima

#🎮🕹️ Inicialização do Pygame
pygame.init()# Inicializa todos os módulos do pygame (gráfico, som, etc)










def main():
    fim_jogo = False

    # 🖥️🖥️ DISPLAY – define a resolução da janela, titulo e icone
    screen_size = (tela_largura, tela_altura)  # Largura x Altura da janela
    screen = pygame.display.set_mode(screen_size)  # Cria a janela com esse tamanho
    pygame.display.set_icon(pygame.image.load("./src/images/icon.png").convert_alpha())# Define o ícone da janela com uma imagem (com transparência)
    pygame.display.set_caption("Card Game")# Define o nome da janela (barra de título)
    #screen.fill(cores["preto"])  # Desenhar a tela de fundo preta
    
 


    
    #intro_obj = src.game_sprites.intro(screen, "CARD GAME", "src/fonts/Ghost Shadow.ttf", 64, 1)
    #intro_time = 0
    #intro_duration = 10000  # milissegundos (10 segundos)
    #intro_running = True

    tela_intro = intro(screen, "CARD GAME", "src/fonts/Ghost Shadow.ttf", 64, 1)
    jogo_selecionado = tela_intro.loop()
    print("Jogo selecionado:", jogo_selecionado)
    del tela_intro  # libera referência para coletor de lixo

    if jogo_selecionado == 3:

        Telacartas(screen).loop();


    


 


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

    
    
    pygame.mouse.set_visible(True)# Ao final, mostra novamente o cursor do mouse (caso tenha sido escondido)
    pygame.mixer.music.fadeout(1000)# Encerra a música suavemente (1 segundo de fade)
    pygame.time.delay(1000)# Espera 1 segundo para garantir que o som finalize
    
    pygame.quit()# Fecha o pygame corretamente








main()