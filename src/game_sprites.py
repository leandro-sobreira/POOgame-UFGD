import pygame


''' Texto IA para estudos
Classe:
class Button(...) define uma classe que encapsula dados e comportamentos.

Herança:
Button herda de pygame.sprite.Sprite, reutilizando e estendendo funcionalidades.

Encapsulamento:
Atributos com __ como __message e __select são privados, protegendo dados internos.

Métodos:
Funções como __init__, set_select e update são comportamentos da classe.

Polimorfismo (implícito):
update() pode ser chamado por um grupo de sprites (Group.update()), permitindo que o comportamento varie dependendo do objeto.
'''
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
    
    def update(self):
        '''Este método é chamado automaticamente a cada frame
        para atualizar a cor do botão dependendo se está selecionado.'''
        
        # Atualiza a imagem com a cor conforme o estado de seleção
        self.image = self.__font.render(
            self.__message, 1, self.__colours[self.__select])
        
        # Reinicia o estado para 0 (não selecionado)
        self.__select = 0
