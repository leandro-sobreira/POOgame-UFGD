import pygame
from src.config import clock, FPS, buttom_size, title_size, cores, escala, buttom_font
from abc import ABC, abstractmethod
import os
import random





#💻💻Uma classe abstrata da tela
class Tela(ABC):
    def __init__(self, screen):
        self.screen = screen
        self._background_path = "Assets/title.png"
        self._background = pygame.image.load(self._background_path).convert()
        self._background = pygame.transform.scale(self._background, screen.get_size())

        self._musica_path = "Assets/sounds/1197551_Butterflies.ogg"
        pygame.mixer.music.load(self._musica_path)
        pygame.mixer.music.set_volume(0.2)
        pygame.mixer.music.play(-1)

        self.select_sound = pygame.mixer.Sound("Assets/sounds/select.ogg")
        self.ok = pygame.mixer.Sound("Assets/sounds/ok.ogg")
        self.reset = pygame.mixer.Sound("Assets/sounds/reset.ogg")

    @property # transforma um método em uma propriedade acessível como atributo, ex: obj.nome.
    def background(self):
        return self._background_path

    @background.setter #permite definir valor para a propriedade, ex: obj.nome = "novo".
    def background(self, caminho):
        self._background_path = caminho
        self._background = pygame.image.load(caminho).convert()
        self._background = pygame.transform.scale(self._background, self.screen.get_size())

    @property
    def musica(self):
        return self._musica_path

    @musica.setter
    def musica(self, caminho):
        self._musica_path = caminho
        pygame.mixer.music.load(caminho)
        pygame.mixer.music.play(-1)

    def desenhar_fundo(self):
        self.screen.blit(self._background, (0, 0))

    @abstractmethod
    def loop(self):
        pass




# ♥️♠️ Tela do blackJack
class Telacartas(Tela):
    def __init__(self, screen):
        super().__init__(screen)
        
        self.background = "Assets/mesa.png"
        self.comprar = "Assets/X.png"

    
        self.carta1 = Carta((400*escala, 100*escala), "Assets/Cards/cardSpades4.png", tamanho=(70*escala, 98*escala))
        self.carta2 = Carta((425*escala, 100*escala), "Assets/Cards_Fundo/cardBack_blue5.png", tamanho=(70*escala, 98*escala))

        self.__Xcomprar = pygame.image.load(self.comprar).convert_alpha()
        self.__Xcomprar = pygame.transform.scale(self.__Xcomprar, (30*escala, 30*escala))
        self.botões = pygame.sprite.Group(self.carta1, self.carta2)
        self.resultado = None  # Começa sem a tela de resultado

        

    def loop(self):
        rodando = True
        clock = pygame.time.Clock()
        while rodando:
            clock.tick(FPS)

            

            #⌨️⌨️ Z X Funções do teclado
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    rodando = False

                #Teclas
                elif evento.type == pygame.KEYDOWN: # evento de clique
                    if evento.key == pygame.K_x:
                        self.adicionar_carta()


                    elif evento.key == pygame.K_c:
                        self.resultado = Resultado(self.screen, "Você perdeu, como sempre.")







            self.desenhar_fundo()
            self.botões.draw(self.screen)
            self.screen.blit(self.__Xcomprar, (750*escala, 400*escala))

            
            if self.resultado:
                self.resultado.desenhar_fundo()
            pygame.display.flip()


    def adicionar_carta(self):
        # Pega uma carta aleatoria e coloca na tela 
        caminho = "Assets/Cards/"
        arquivos = os.listdir(caminho)
        imagens = [f for f in arquivos if f.endswith(".png")]

        if not imagens:
            return  # Nenhuma imagem disponível

        imagem_aleatoria = random.choice(imagens)
        
        # 🃏 Posição da nova carta: um pouco à direita da última
        #TODO Não centralizado
        cartas = self.botões.sprites()
        if cartas:
            ultima = cartas[-1].rect
            nova_x = ultima.right + 10    # 10px de espaço
        else:
            nova_x = 410 * escala

        nova_carta = Carta((nova_x, 300 * escala), os.path.join(caminho, imagem_aleatoria), tamanho=(70 * escala, 98 * escala))
        self.botões.add(nova_carta)


#🏆🏆 Resultados da partida, 
class Resultado(Tela):
    def __init__(self, screen, texto):
        

        self.__texto = texto
        self.screen = screen
        self.fonte = pygame.font.Font("Assets/fonts/Magofah.ttf", title_size)
        self.centro = (screen.get_width() // 2, screen.get_height() // 4)


    def desenhar_fundo(self):
        # Cria um overlay preto com 50% de transparência
        overlay = pygame.Surface(self.screen.get_size(), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 200))  # RGBA (128 = 50% de alfa)

        self.screen.blit(overlay, (0, 0))  # Aplica o escurecimento

        # Desenha o texto por cima
        texto_renderizado = self.fonte.render(self.__texto, True, (255, 255, 255))
        rect = texto_renderizado.get_rect(center=self.centro)
        self.screen.blit(texto_renderizado, rect)
    
    def loop(self):
        pass





#🙊
class intro(pygame.sprite.Sprite):
    def __init__(self, screen, title_game, title_font, title_size, title_scale):

        # Chama o método __init__ da superclasse
        pygame.sprite.Sprite.__init__(self)

        #⛰️⛰️ background
        self.__background = pygame.image.load("Assets/title.png").convert()
        self.__background = pygame.transform.scale(self.__background, screen.get_size())


         #✨✨ Titulo Com contorno Branco
        self.screen = screen
        self.texto = title_game
        self.fonte = pygame.font.Font(title_font, title_size)
        self.centro = (screen.get_width() // 2, screen.get_height() // 4)
        self.contorno_offset = 2 * title_scale
        

        # 🎥🎥 Cria a surface, folha transparente, com o título e contorno já renderizados
        self.surface = pygame.Surface(screen.get_size(), pygame.SRCALPHA)
        self.__render()


        #🖲️🖲️ Botões
        self.start_button = Button((screen.get_width()/2, screen.get_height() - (150 * escala)), "Start", cores["preto"], buttom_font, buttom_size)
        self.erase_button = Button((screen.get_width()/2, screen.get_height() - (110 * escala)), "Erase Data", cores["preto"], buttom_font, buttom_size)
        self.config_button = Button((screen.get_width()/2, screen.get_height() - (70 * escala)), "Config", cores["preto"], buttom_font, buttom_size)
        self.quit_button = Button((screen.get_width()/2, screen.get_height() - (30 * escala)), "Quit", cores["preto"], buttom_font, buttom_size)

        self.buttons = [self.start_button, self.erase_button, self.config_button, self.quit_button]
        self.all_sprites = pygame.sprite.Group(self.buttons)
        self.selected = [self.start_button]



        # 🎵🎻Configurações dos sons
        pygame.mixer.music.load("Assets/sounds/1197551_Butterflies.ogg") #musica de fundo da tela
        pygame.mixer.music.set_volume(0.2)
        pygame.mixer.music.play(-1)
        # Efeitos sonoros
        self.select_sound = pygame.mixer.Sound("Assets/sounds/computer-processing-sound-effects-short-click-select-02-122133.ogg") 
        self.ok = pygame.mixer.Sound("Assets/sounds/computer-processing-sound-effects-short-click-select-01-122134.ogg")
        self.reset = pygame.mixer.Sound("Assets/sounds/reset.ogg")

        self.select_sound.set_volume(0.5)
        self.ok.set_volume(0.5)
        self.reset.set_volume(0.5)


        

    def __render(self):

        #✨✨ Titulo Com contorno Branco
        for dx, dy in [(-self.contorno_offset, -self.contorno_offset), (-self.contorno_offset, 0), (-self.contorno_offset, self.contorno_offset),
                       (0, -self.contorno_offset), (0, self.contorno_offset),
                       (self.contorno_offset, -self.contorno_offset), (self.contorno_offset, 0), (self.contorno_offset, self.contorno_offset)]:
            contorno = self.fonte.render(self.texto, True, cores["branco"])
            rect = contorno.get_rect(center=(self.centro[0] + dx, self.centro[1] + dy))
            self.surface.blit(contorno, rect)

        texto_principal = self.fonte.render(self.texto, True, cores["preto"])
        rect = texto_principal.get_rect(center=self.centro)
        self.surface.blit(texto_principal, rect)


        #🖲️🖲️ Botões
        self.surface.blit(texto_principal, rect)

    def desenhar(self):
        self.screen.blit(self.__background, (0, 0))
        self.screen.blit(self.surface, (0, 0))
        self.all_sprites.draw(self.screen)



    def loop(self):
        clock = pygame.time.Clock()
        self.jogo = None  # Aqui ficará o resultado final
        keep_going = True
        selected = [self.buttons[0]]

        while keep_going:
            clock.tick(FPS)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    keep_going = False
                    self.jogo = 0  # sair do jogo
                    return

                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        if selected != [self.buttons[0]]:
                            self.select_sound.play()
                            selected = [self.buttons[self.buttons.index(selected[0]) - 1]]

                    elif event.key == pygame.K_DOWN:
                        if selected != [self.buttons[-1]]:
                            self.select_sound.play()
                            selected = [self.buttons[self.buttons.index(selected[0]) + 1]]


                    # Confirmar seleção ao pressionar Z
                    elif event.key == pygame.K_z:
                        self.ok.play()
                        botao = selected[0]
                        keep_going = False
                        if botao == self.start_button:
                            pygame.mixer.music.pause()

                            self.jogo = GameSelect(self.screen, self.ok, self.select_sound).loop()


                            if self.jogo == 0:
                                pygame.mixer.music.unpause()  # Volta a tocar a música
                                keep_going = True  # Volta pro menu se cancelado
                                
                        elif botao == self.quit_button:
                            self.jogo = 0
                        elif botao == self.config_button:
                            self.jogo = 2
                        elif botao == self.erase_button:
                            self.reset.play()
                            # lógica de reset

            for b in self.buttons:
                b.set_deselect()
            selected[0].set_select()

            self.desenhar()
            self.all_sprites.update()
            pygame.display.flip()

        return self.jogo
    
            

    
class GameSelect:
    def __init__(self, screen, ok, select_sound):
        self.screen = screen
        self.ok = ok
        self.select_sound = select_sound

        self.BlackJack_button = Button(
            (screen.get_width() / 2, screen.get_height() - (200 * escala)),
            "Blackjack", cores["branco"], buttom_font, buttom_size)
        self.Quit_button = Button(
            (screen.get_width() / 2, screen.get_height() - (150 * escala)),
            "Quit", cores["branco"], buttom_font, buttom_size)

        self.buttons = [self.BlackJack_button, self.Quit_button]
        self.all_sprites = pygame.sprite.Group(self.buttons)
        self.selected = [self.buttons[0]]

    def loop(self):
        keep_going = True
        while keep_going:
            clock.tick(FPS)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return 0
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP and self.selected != [self.BlackJack_button]:
                        self.select_sound.play()
                        self.selected = [self.BlackJack_button]
                    elif event.key == pygame.K_DOWN and self.selected != [self.Quit_button]:
                        self.select_sound.play()
                        self.selected = [self.Quit_button]
                    elif event.key == pygame.K_z:
                        self.ok.play()
                        if self.selected == [self.Quit_button]:
                            return 0
                        elif self.selected == [self.BlackJack_button]:
                            return 3

            self.screen.fill(cores["preto"])

            for btn in self.buttons:
                if btn in self.selected:
                    btn.set_select()
                else:
                    btn.set_deselect()

            self.all_sprites.update()
            self.all_sprites.draw(self.screen)
            pygame.display.update()

class Carta(pygame.sprite.Sprite):
    def __init__(self, xy_pos, image_path, image_selected_path=None, tamanho=None):
        pygame.sprite.Sprite.__init__(self)
        self.image_normal = pygame.image.load(image_path).convert_alpha()
        self.image_selected = pygame.image.load(image_selected_path).convert_alpha() if image_selected_path else self.image_normal

        # Redimensiona se o tamanho for fornecido
        if tamanho:
            self.image_normal = pygame.transform.scale(self.image_normal, tamanho)
            self.image_selected = pygame.transform.scale(self.image_selected, tamanho)

        self.image = self.image_normal
        self.rect = self.image.get_rect(center=xy_pos) #retângulo que representa a posição e tamanho da imagem
        self.original_pos = self.rect.center
        self__selected = False


class ImageButton(pygame.sprite.Sprite):
    def __init__(self, xy_pos, image_path, image_selected_path=None):
        pygame.sprite.Sprite.__init__(self)
        self.image_normal = pygame.image.load(image_path).convert_alpha()
        self.image_selected = pygame.image.load(image_selected_path).convert_alpha() if image_selected_path else self.image_normal

        self.image = self.image_normal
        self.rect = self.image.get_rect(center=xy_pos) #retângulo que representa a posição e tamanho da imagem
        self.original_pos = self.rect.center
        self.selected = False

    def set_select(self):
        self.selected = True
        self.image = self.image_selected
        # Move 10 pixels pra cima
        self.rect.center = (self.original_pos[0], self.original_pos[1] - 10)

    def set_deselect(self):
        self.selected = False
        self.image = self.image_normal
        # Volta pra posição original
        self.rect.center = self.original_pos

    def update(self):
        pass




class Button(pygame.sprite.Sprite): #Roubado em sua maior parte do  witchCraft
    '''Esta é a classe de botão onde os sprites de botões são criados.
    O sprite de botão é usado no menu principal para selecionar opções
    que executam funções específicas.
    '''
    
    def __init__(self, xy_pos, message, colour, font_path, font_size):
        '''Este método inicializa o sprite usando o parâmetro xy_pos para
        definir a posição do botão. O parâmetro message define o texto exibido,
        e o parâmetro colour define a cor inicial do texto do botão.
        '''
        
        # Chama o método __init__ da superclasse
        pygame.sprite.Sprite.__init__(self)
        
        #🔏 Atributos privados
        self.__message = message
        self.__font = pygame.font.Font(font_path, font_size)
        self.__select = 0  # 0 = não selecionado, 1 = selecionado
        self.__colours = [colour, (255, 99, 71)]  # cor normal e cor quando selecionado
        #🥖 Atributos Publicos
        self.image = self.__font.render(message, 1, self.__colours[self.__select])
        self.rect = self.image.get_rect()
        self.rect.center = xy_pos  # centraliza o botão na posição passada
    
    def set_select(self):
        '''Este método define o botão como selecionado.'''
        self.__select = 1
        

    def set_deselect(self):
        '''Define o botão como não selecionado.'''
        self.__select = 0
    
    def update(self):
        '''Este método é chamado automaticamente a cada frame
        para atualizar a cor do botão dependendo se está selecionado.'''
        
        # Atualiza a imagem com a cor conforme o estado de seleção
        self.image = self.__font.render(
            self.__message, 1, self.__colours[self.__select])
        
        # Reinicia o estado para 0 (não selecionado)
        self.__select = 0
        

'''
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    rodando = False

                elif evento.type == pygame.KEYDOWN:
                    if evento.key == pygame.K_ESCAPE:
                        rodando = False
                    elif evento.key == pygame.K_RIGHT:
                        # Deseleciona carta atual
                        self.botões.sprites()[self.index_selecionado].set_deselect()
                        # Avança índice (com wrap-around)
                        self.index_selecionado = (self.index_selecionado + 1) % len(self.botões)
                        # Seleciona nova carta
                        self.botões.sprites()[self.index_selecionado].set_select()

                    elif evento.key == pygame.K_LEFT:
                        self.botões.sprites()[self.index_selecionado].set_deselect()
                        self.index_selecionado = (self.index_selecionado - 1) % len(self.botões)
                        self.botões.sprites()[self.index_selecionado].set_select()'''