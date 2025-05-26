import pygame
print("python")


# Inicializar
pygame.init()
tamanho_tela = (500, 500)
tela = pygame.display.set_mode(tamanho_tela)  # Cria a janela do jogo com o tamanho especificado (largura, altura)
pygame.display.set_caption("Quebra Pedra")    # Define o título da janela como "Quebra Pedra"


tamanho_bola = 15
bola = pygame.Rect(100, 300, tamanho_bola, tamanho_bola) #Criando um retangulo do py game para depois colocar na tela
tamanho_jogador = 100
jogador = pygame.Rect(0, 450, tamanho_jogador, 15) #Criando um retangulo do py game para depois colocar na tela


qtde_blocos_linha = 8
qtde_linhas_blocos = 5
qtde_total_blocos = qtde_blocos_linha * qtde_linhas_blocos


def criar_blocos(qtde_blocos_linha, qtde_linhas_blocos):
    altura_tela = tamanho_tela[1]
    largura_tela = tamanho_tela[0]
    distancia_entre_blocos = 5
    altura_bloco = 20  # Mova esta linha pra cima
    distancia_entre_linhas = altura_bloco + 10
    largura_bloco = largura_tela / 8 - distancia_entre_blocos
    blocos = []
    
    for j in range(qtde_linhas_blocos):
        for i in range(qtde_blocos_linha):
            bloco = pygame.Rect(i * (largura_bloco + distancia_entre_blocos), j * distancia_entre_linhas, largura_bloco, altura_bloco)
            blocos.append(bloco)
    
    return blocos



cores = {
    "branco": (255, 255, 255),
    "preto": (0, 0, 0),
    "vermelho": (255, 0, 0),
    "verde": (0, 255, 0),
    "azul": (0, 0, 255) 
}


fim_jogo = False
pontuacao = 0
movimento_bola = [1, -1]  



# criar as funções do jogo
def movimentar_jogador(evento):
    if evento.type == pygame.KEYDOWN:
        if evento.key == pygame.K_RIGHT:
            if (jogador.x + tamanho_jogador) < tamanho_tela[0]:
                jogador.x = jogador.x + 1
        if evento.key == pygame.K_LEFT:
            if jogador.x > 0:
                jogador.x = jogador.x - 1

    

def movimentar_bola(bola):
    movimento = movimento_bola
    bola.x += movimento[0]
    bola.y += movimento[1]

    if bola.x <= 0:
        movimento[0] = - movimento[0]
    if bola.y <= 0:
        movimento[1] = - movimento[1]
    if bola.x + tamanho_bola >= tamanho_tela[0]:
        movimento[0] = - movimento[0]
    if bola.y + tamanho_bola >= tamanho_tela[1]:
        movimento = None


    if jogador.collidepoint(bola.x, bola.y):
        movimento[1] = - movimento[1]
    for bloco in blocos:
        if bloco.collidepoint(bola.x, bola.y):
            blocos.remove(bloco)
            movimento[1] = - movimento[1]


    return movimento
    

def atualizar_pontuacao(pontuacao):
    font = pygame.font.Font(None, 30) # Texto,
    texto = font.render(f"Fontuacao: {pontuacao}", 1, cores["verde"])
    tela.blit(texto, (0, 780))
    if pontuacao >= qtde_total_blocos:
        return True
    else :
        return False

    

# desenhar as coisas na tela

def desenhar_inicio_jogo():

    tela.fill(cores["preto"])  # Desenhar a tela de fundo preta
    pygame.draw.rect(tela, cores["azul"], jogador)
    pygame.draw.rect(tela, cores["branco"], bola)


def desenhar_blocos(blocos):
    for bloco in blocos:
        pygame.draw.rect(tela, cores["vermelho"], bloco)



blocos = criar_blocos(qtde_blocos_linha, qtde_linhas_blocos)

# criar o loop do jogo

while not fim_jogo: 
    desenhar_inicio_jogo()
    desenhar_blocos(blocos)
    fim_jogo = atualizar_pontuacao(qtde_total_blocos - len(blocos))
    for evento in pygame.event.get(): #pegar os eventos do usuario
        
        if evento.type == pygame.QUIT:
            fim_jogo = True
    movimentar_jogador(evento)
    
    movimento_bola = movimentar_bola(bola)
    if not movimentar_bola:
        fim_jogo = True
    pygame.time.delay(1)  # Atrasar o loop do jogo por 1 milissegundos
    pygame.display.flip()   # Atualizar a tela

pygame.quit()  # Fechar o pygame