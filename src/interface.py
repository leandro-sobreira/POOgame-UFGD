import pygame
import os
import random
import setup as st

from abc import ABC, abstractmethod

#Uma classe abstrata da tela
class Screen(ABC):
    #TODO Saber quem fez essa coisa linda aqui ^-^ (Codigo estranho..., mas interessante)
    def __init__(self, screen):
        self.screen = screen
        self._background_path = os.path.join(st.img_folder, "title.png")
        self._background = pygame.image.load(self._background_path).convert()
        self._background = pygame.transform.scale(self._background, screen.get_size())

        self._music_path = os.path.join(st.sound_folder, "1197551_Butterflies.ogg")

        pygame.mixer.music.load(self._music_path)
        pygame.mixer.music.set_volume(0.2)
        pygame.mixer.music.play(-1)
        
        self.select_sound = pygame.mixer.Sound(os.path.join(st.sound_folder, "select.ogg"))
        self.ok_sound = pygame.mixer.Sound(os.path.join(st.sound_folder, "ok.ogg"))
        self.reset_sound = pygame.mixer.Sound(os.path.join(st.sound_folder, "reset.ogg"))

    @property # transforma um método em uma propriedade acessível como atributo, ex: obj.nome.
    def background(self):
        return self._background_path

    @background.setter #permite definir valor para a propriedade, ex: obj.nome = "novo".
    def background(self, path):
        self._background_path = path
        self._background = pygame.image.load(path).convert()
        self._background = pygame.transform.scale(self._background, self.screen.get_size())

    @property
    def music(self):
        return self._music_path

    @music.setter
    def music(self, path):
        self._musica_path = path
        pygame.mixer.music.load(path)
        pygame.mixer.music.play(-1)

    def draw_background(self):
        self.screen.blit(self._background, (0, 0))

    @abstractmethod
    def loop(self):
        pass




#Tela do blackJack
class BlackjackScreen(Screen):
    def __init__(self, screen):
        super().__init__(screen)

        self.background = os.path.join(st.img_folder, "mesa.png")
        self.take = os.path.join(st.img_folder, "X.png")       
    
        self.card1 = Card((400*st.SCALE, 100*st.SCALE), os.path.join(st.img_folder, "cards/cardSpades4.png"), size=(70*st.SCALE, 98*st.SCALE))
        self.card2 = Card((425*st.SCALE, 100*st.SCALE), os.path.join(st.img_folder, "cards/cardSpades4.png"), size=(70*st.SCALE, 98*st.SCALE))

        self.__takeX = pygame.image.load(self.take).convert_alpha()
        self.__takeX = pygame.transform.scale(self.__takeX, (30*st.SCALE, 30*st.SCALE))
        self.buttons = pygame.sprite.Group(self.card1, self.card2)
        self.result = None  # Começa sem a tela de resultado        

    def loop(self):

        is_running = True
        clock = pygame.time.Clock()

        while is_running:

            clock.tick(st.FPS)

            #Z X Funções do teclado
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    is_running = False
                #Teclas
                elif event.type == pygame.KEYDOWN: # evento de clique
                    if event.key == pygame.K_x:
                        self.add_card()


                    elif event.key == pygame.K_c:
                        self.result = ResultScreen(self.screen, "Você perdeu, como sempre.")

            self.draw_background()
            self.buttons.draw(self.screen)
            self.screen.blit(self.__takeX, (750*st.SCALE, 400*st.SCALE))

            
            if self.result:
                self.result.draw_background()

            pygame.display.flip()


    def add_card(self):
        # Pega uma carta aleatoria e coloca na tela 
        path = os.path.join(st.img_folder, "cards")
        archives = os.listdir(path)
        images = [f for f in archives if f.endswith(".png")]

        if not images:
            return  # Nenhuma imagem disponível

        random_image = random.choice(images)
        
        #Posição da nova carta: um pouco à direita da última
        #TODO Não centralizado

        cards = self.buttons.sprites()

        if cards:
            last = cards[-1].rect
            new_x = last.right + 10    # 10px de espaço
        else:
            new_x = 410 * st.SCALE

        new_card = Card((new_x, 300 * st.SCALE), os.path.join(path, random_image), size=(70 * st.SCALE, 98 * st.SCALE))

        self.buttons.add(new_card)


#Resultados da partida, 
class ResultScreen(Screen):
    def __init__(self, screen, text):
        

        self.__text = text
        self.screen = screen
        self.font = pygame.font.Font(os.path.join(st.font_folder, "Magofah.ttf"), st.title_size)
        self.center = (screen.get_width() // 2, screen.get_height() // 4)


    def draw_background(self):
        # Cria um overlay preto com 50% de transparência
        overlay = pygame.Surface(self.screen.get_size(), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 200))  # RGBA (128 = 50% de alfa)

        self.screen.blit(overlay, (0, 0))  # Aplica o escurecimento

        # Desenha o texto por cima
        rendered_text = self.font.render(self.__text, True, (255, 255, 255))
        rect = rendered_text.get_rect(center=self.center)
        self.screen.blit(rendered_text, rect)
    
    def loop(self):
        pass


class IntroScreen(pygame.sprite.Sprite):
    #TODO rever tipagens e encapsulamento
    def __init__(self, screen, title_game, title_font, title_size, title_scale):

        # Chama o método __init__ da superclasse
        pygame.sprite.Sprite.__init__(self)

        #background
        self.__background = pygame.image.load(os.path.join(st.img_folder, "title.png")).convert()
        self.__background = pygame.transform.scale(self.__background, screen.get_size())

        # Titulo Com contorno Branco
        self.screen = screen
        self.text = title_game
        self.font = pygame.font.Font(title_font, title_size)
        self.center = (screen.get_width() // 2, screen.get_height() // 4)
        self.outline_offset = 2 * title_scale
        

        # Cria a surface, folha transparente, com o título e contorno já renderizados
        self.surface = pygame.Surface(screen.get_size(), pygame.SRCALPHA)
        self.__render()


        # Botões
        self.start_button = Button((screen.get_width()/2, screen.get_height() - (150 * st.SCALE)), "Start", st.BLACK, st.button_font, st.button_size)
        self.erase_button = Button((screen.get_width()/2, screen.get_height() - (110 * st.SCALE)), "Erase Data", st.BLACK, st.button_font, st.button_size)
        self.config_button = Button((screen.get_width()/2, screen.get_height() - (70 * st.SCALE)), "Config", st.BLACK, st.button_font, st.button_size)
        self.quit_button = Button((screen.get_width()/2, screen.get_height() - (30 * st.SCALE)), "Quit", st.BLACK, st.button_font, st.button_size)

        #gambiarra de listas
        self.buttons = [self.start_button, self.erase_button, self.config_button, self.quit_button]
        self.all_sprites = pygame.sprite.Group(self.buttons)
        self.selected = [self.start_button]


        # Configurações dos sons
        
        pygame.mixer.music.load(os.path.join(st.sound_folder, "1197551_Butterflies.ogg")) #musica de fundo da tela
        pygame.mixer.music.set_volume(0.2)
        pygame.mixer.music.play(-1)

        # Efeitos sonoros
        self.select_sound = pygame.mixer.Sound(os.path.join(st.sound_folder, "computer-processing-sound-effects-short-click-select-02-122133.ogg")) 
        self.ok_sound = pygame.mixer.Sound(os.path.join(st.sound_folder, "computer-processing-sound-effects-short-click-select-01-122134.ogg"))
        self.reset_sound = pygame.mixer.Sound(os.path.join(st.sound_folder, "reset.ogg"))

        self.select_sound.set_volume(0.5)
        self.ok_sound.set_volume(0.5)
        self.reset_sound.set_volume(0.5)


    def __render(self):

        #Titulo Com contorno Branco
        for dx, dy in [(-self.outline_offset, -self.outline_offset), (-self.outline_offset, 0), (-self.outline_offset, self.outline_offset),
                       (0, -self.outline_offset), (0, self.outline_offset),
                       (self.outline_offset, -self.outline_offset), (self.outline_offset, 0), (self.outline_offset, self.outline_offset)]:
            
            outline = self.font.render(self.text, True, st.WHITE)
            rect = outline.get_rect(center=(self.center[0] + dx, self.center[1] + dy))
            self.surface.blit(outline, rect)

        main_text = self.font.render(self.text, True, st.BLACK)
        rect = main_text.get_rect(center=self.center)
        self.surface.blit(main_text, rect)


        #Botões
        self.surface.blit(main_text, rect)

    def draw(self):
        self.screen.blit(self.__background, (0, 0))
        self.screen.blit(self.surface, (0, 0))
        self.all_sprites.draw(self.screen)


    def loop(self):
        clock = pygame.time.Clock()
        self.game = None  # Aqui ficará o resultado final
        keep_going = True
        selected = [self.buttons[0]]

        while keep_going:
            clock.tick(st.FPS)

            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    keep_going = False
                    self.game = 0  # sair do jogo

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
                        self.ok_sound.play()
                        button = selected[0]
                        keep_going = False

                        if button == self.start_button:
                            pygame.mixer.music.pause()

                            self.game = GameSelect(self.screen, self.ok_sound, self.select_sound).loop()
                           
                            


                            if self.game == 0:
                                pygame.mixer.music.unpause()  # Volta a tocar a música
                                keep_going = True  # Volta pro menu se cancelado
                                
                        elif button == self.quit_button:
                            self.game = 0
                        elif button == self.config_button:
                            self.game = 2
                        elif button == self.erase_button:
                            self.reset_sound.play()
                            
                            #TODO lógica de reset

            for b in self.buttons:
                b.set_deselect()

            selected[0].set_select()
            self.draw()
            self.all_sprites.update()

            pygame.display.flip()
        print(self.game)
        return self.game
    
            

    
class GameSelect:
    def __init__(self, screen, ok_sound, select_sound):
        self.screen = screen
        self.ok_sound = ok_sound
        self.select_sound = select_sound

        self.blackjack_button = Button(
            (screen.get_width() / 2, screen.get_height() - (200 * st.SCALE)),
            "Blackjack", st.WHITE, st.button_font, st.button_size)
        self.quit_button = Button(
            (screen.get_width() / 2, screen.get_height() - (150 * st.SCALE)),
            "Quit", st.WHITE, st.button_font, st.button_size)

        self.buttons = [self.blackjack_button, self.quit_button]
        self.all_sprites = pygame.sprite.Group(self.buttons)
        self.selected = [self.buttons[0]]

    def loop(self):

        keep_going = True

        while keep_going:
            st.clock.tick(st.FPS)

            for event in pygame.event.get():

                if event.type == pygame.QUIT:

                    return 0
                elif event.type == pygame.KEYDOWN:

                    if event.key == pygame.K_UP and self.selected != [self.blackjack_button]:
                        self.select_sound.play()
                        self.selected = [self.blackjack_button]
                    elif event.key == pygame.K_DOWN and self.selected != [self.quit_button]:
                        self.select_sound.play()
                        self.selected = [self.quit_button]
                    elif event.key == pygame.K_z:
                        self.ok_sound.play()
                        if self.selected == [self.quit_button]:
                            return 0
                        elif self.selected == [self.blackjack_button]:
                            return 3

            self.screen.fill(st.BLACK)

            for b in self.buttons:
                if b in self.selected:
                    b.set_select()
                else:
                    b.set_deselect()

            self.all_sprites.update()
            self.all_sprites.draw(self.screen)
            pygame.display.update()

class Card(pygame.sprite.Sprite):
    def __init__(self, xy_pos, image_path, image_selected_path=None, size=None):
        pygame.sprite.Sprite.__init__(self)
        self.image_normal = pygame.image.load(image_path).convert_alpha()
        self.image_selected = pygame.image.load(image_selected_path).convert_alpha() if image_selected_path else self.image_normal

        # Redimensiona se o tamanho for fornecido
        if size:
            self.image_normal = pygame.transform.scale(self.image_normal, size)
            self.image_selected = pygame.transform.scale(self.image_selected, size)

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
        
        #Atributos privados
        self.__message = message
        self.__font = pygame.font.Font(font_path, font_size)
        self.__select = 0  # 0 = não selecionado, 1 = selecionado
        self.__colours = [colour, (255, 99, 71)]  # cor normal e cor quando selecionado
        
        #Atributos Publicos
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