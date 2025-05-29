import pygame


#Inicialização do Pygame
pygame.init()
tamanho_tela = (854, 480)
tela = pygame.display.set_mode(tamanho_tela)  # Cria a janela do jogo com o tamanho especificado (largura, altura)
pygame.display.set_caption("POO_game_card")    # Define o título da janela como "Quebra Pedra"

fim_jogo = False

cores = {
    "branco": (255, 255, 255),
    "preto": (0, 0, 0),
    "vermelho": (255, 0, 0),
    "verde": (0, 255, 0),
    "azul": (0, 0, 255) 
}




while not fim_jogo:
    tela.fill(cores["preto"])  # Desenhar a tela de fundo preta
    
    

    for evento in pygame.event.get(): #pegar os eventos do usuario
    
        if evento.type == pygame.QUIT:
            fim_jogo = True
    pygame.time.delay(1)
    pygame.display.flip() # autualiza a tela
    

pygame.quit()  # Fechar o pygame