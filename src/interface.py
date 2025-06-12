import pygame
import os
from . import setup as st

from abc import ABC, abstractmethod

# --- HELPER FUNCTIONS ---

def draw_text_with_outline(surface, text, font, pos, text_color, outline_color, outline_width=2): #
    """Renders text with a simple outline.""" #
    x, y = pos #
    # Render outline #
    for dx in range(-outline_width, outline_width + 1): #
        for dy in range(-outline_width, outline_width + 1): #
            if dx != 0 or dy != 0: #
                outline_surf = font.render(text, True, outline_color) #
                surface.blit(outline_surf, (x - outline_surf.get_width() // 2 + dx, y - outline_surf.get_height() // 2 + dy)) #
    # Render main text #
    text_surf = font.render(text, True, text_color) #
    surface.blit(text_surf, (x - text_surf.get_width() // 2, y - text_surf.get_height() // 2)) #

# --- ABSTRACT SCREEN CLASS (BASE FOR ALL SCREENS) ---

class Screen(ABC): #
    """
    An abstract base class for all game screens.
    Ensures that every screen has a consistent structure and behavior.
    """ #
    def __init__(self, screen, player_data=None): #
        self.screen = screen #
        self.player_data = player_data #
        self.next_screen = None #
        self._background = None #

        # Load common sounds #
        self.select_sound = pygame.mixer.Sound(os.path.join(st.sound_folder, "select.ogg")) #
        self.ok_sound = pygame.mixer.Sound(os.path.join(st.sound_folder, "ok.ogg")) #
        self.reset_sound = pygame.mixer.Sound(os.path.join(st.sound_folder, "reset.ogg")) #

    def set_background(self, image_path): #
        """Sets and scales the background image.""" #
        background = pygame.image.load(image_path).convert() #
        self._background = pygame.transform.scale(background, self.screen.get_size()) #

    def set_music(self, music_path, volume=0.2): #
        """Loads and plays background music in a loop.""" #
        pygame.mixer.music.load(music_path) #
        pygame.mixer.music.set_volume(volume) #
        pygame.mixer.music.play(-1) #

    @abstractmethod
    def handle_event(self, event): #
        """Abstract method to handle screen-specific events.""" #
        pass #

    @abstractmethod
    def draw(self): #
        """Abstract method to draw the screen's elements.""" #
        pass #

    def loop(self): #
        """
        The main loop for a screen. It handles events, updates, and drawing.
        Returns the key for the next screen to be displayed.
        """ #
        is_running = True #
        while is_running: #
            st.clock.tick(st.FPS) #

            for event in pygame.event.get(): #
                if event.type == pygame.QUIT: #
                    self.next_screen = "QUIT" #
                # Pass the event to the specific handler of the child screen #
                self.handle_event(event) #

            self.draw() #
            pygame.display.flip() #
            
            if self.next_screen: #
                is_running = False #
        
        return self.next_screen #

# --- SCREEN IMPLEMENTATIONS ---

class PlayerNameScreen(Screen): #
    def __init__(self, screen): #
        super().__init__(screen) #
        self.set_background(os.path.join(st.img_folder, "title.png")) #
        self.font = pygame.font.Font(st.button_font, 32) #
        self.input_font = pygame.font.Font(st.button_font, 28) #
        self.player_name = "" #
        self.prompt_text = "Enter Your Name and Press Enter" #

    def handle_event(self, event): #
        if event.type == pygame.KEYDOWN: #
            if event.key == pygame.K_RETURN: #
                self.ok_sound.play() #
                self.next_screen = "GET_PLAYER" #
            elif event.key == pygame.K_BACKSPACE: #
                self.player_name = self.player_name[:-1] #
            else:
                if len(self.player_name) < 15: # Limit name length #
                    self.player_name += event.unicode #
    
    def draw(self): #
        self.screen.blit(self._background, (0, 0)) #
        draw_text_with_outline(self.screen, self.prompt_text, self.font, (st.SCREEN_WIDTH / 2, st.SCREEN_HEIGHT / 2 - 50), st.WHITE, st.BLACK) #
        
        input_rect = pygame.Rect(st.SCREEN_WIDTH / 2 - 150, st.SCREEN_HEIGHT / 2, 300, 50) #
        pygame.draw.rect(self.screen, st.WHITE, input_rect, 2) #
        input_surface = self.input_font.render(self.player_name, True, st.WHITE) #
        self.screen.blit(input_surface, (input_rect.x + 10, input_rect.y + 10)) #

class MenuScreen(Screen): #
    def __init__(self, screen, player_data): #
        super().__init__(screen, player_data) #
        self.set_background(os.path.join(st.img_folder, "title.png")) #
        self.set_music(os.path.join(st.sound_folder, "1197551_Butterflies.ogg")) #
        self.title_font = pygame.font.Font(os.path.join(st.font_folder, "Ghost Shadow.ttf"), st.title_size) #
        
        self.buttons = [ #
            Button((st.SCREEN_WIDTH/2, st.SCREEN_HEIGHT - 200), "Start", "GAME_SELECT"), #
            Button((st.SCREEN_WIDTH/2, st.SCREEN_HEIGHT - 150), "Erase Data", "ERASE_DATA"), #
            Button((st.SCREEN_WIDTH/2, st.SCREEN_HEIGHT - 100), "Config", "CONFIG"), #
            Button((st.SCREEN_WIDTH/2, st.SCREEN_HEIGHT - 50), "Quit", "QUIT") #
        ]
        self.selected_index = 0 #
        self.all_sprites = pygame.sprite.Group(self.buttons) #

    def handle_event(self, event): #
        if event.type == pygame.KEYDOWN: #
            if event.key in (pygame.K_UP, pygame.K_w): #
                self.select_sound.play() #
                self.selected_index = (self.selected_index - 1) % len(self.buttons) #
            elif event.key in (pygame.K_DOWN, pygame.K_s): #
                self.select_sound.play() #
                self.selected_index = (self.selected_index + 1) % len(self.buttons) #
            elif event.key in (pygame.K_z, pygame.K_RETURN): #
                selected_button = self.buttons[self.selected_index] #
                if selected_button.action == "ERASE_DATA": #
                    self.reset_sound.play() #
                else:
                    self.ok_sound.play() #
                self.next_screen = selected_button.action #

    def draw(self): #
        self.screen.blit(self._background, (0, 0)) #
        draw_text_with_outline(self.screen, "CARD GAME", self.title_font, (st.SCREEN_WIDTH/2, st.SCREEN_HEIGHT/4), st.BLACK, st.WHITE) #
        
        welcome_text = f"Welcome, {self.player_data['name']}! Points: {self.player_data['blackjack_points']}" #
        draw_text_with_outline(self.screen, welcome_text, pygame.font.Font(st.button_font, 22), (st.SCREEN_WIDTH/2, st.SCREEN_HEIGHT/2), st.WHITE, st.BLACK) #

        for i, button in enumerate(self.buttons): #
            button.set_selected(i == self.selected_index) #
        self.all_sprites.update() #
        self.all_sprites.draw(self.screen) #

class GameSelectScreen(Screen): #
    def __init__(self, screen, player_data): #
        super().__init__(screen, player_data) #
        self.set_background(os.path.join(st.img_folder, "mesa.png")) #
        self.title_font = pygame.font.Font(st.button_font, st.title_size) #

        self.buttons = [ #
            Button((st.SCREEN_WIDTH/2, 200), "Blackjack", "BLACKJACK"), #
            Button((st.SCREEN_WIDTH/2, 250), "UNO", "UNO"), #
            Button((st.SCREEN_WIDTH/2, 350), "Back to Menu", "MENU") #
        ]
        self.selected_index = 0 #
        self.all_sprites = pygame.sprite.Group(self.buttons) #

    def handle_event(self, event): #
        if event.type == pygame.KEYDOWN: #
            if event.key in (pygame.K_UP, pygame.K_w): #
                self.select_sound.play() #
                self.selected_index = (self.selected_index - 1) % len(self.buttons) #
            elif event.key in (pygame.K_DOWN, pygame.K_s): #
                self.select_sound.play() #
                self.selected_index = (self.selected_index + 1) % len(self.buttons) #
            elif event.key in (pygame.K_z, pygame.K_RETURN): #
                self.ok_sound.play() #
                self.next_screen = self.buttons[self.selected_index].action #
    
    def draw(self): #
        self.screen.blit(self._background, (0, 0)) #
        draw_text_with_outline(self.screen, "Select a Game", self.title_font, (st.SCREEN_WIDTH/2, 80), st.WHITE, st.BLACK) #
        for i, button in enumerate(self.buttons): #
            button.set_selected(i == self.selected_index) #
        self.all_sprites.update() #
        self.all_sprites.draw(self.screen) #

class BlackjackScreen(Screen): #
    """The View for the Blackjack game. It only draws what the Model tells it to.""" #
    def __init__(self, screen, game_instance): #
        super().__init__(screen) #
        self.game = game_instance  # This is the Model #
        self.set_background(os.path.join(st.img_folder, "mesa.png")) #
        self.font = pygame.font.Font(st.button_font, 24) #
        self.card_sprites = pygame.sprite.Group() #
        self.load_card_images() #

    def load_card_images(self): #
        """Pre-loads all card images into a dictionary for quick access.""" #
        self.card_images = {} #
        cards_path = os.path.join(st.img_folder, "cards") #
        for filename in os.listdir(cards_path): #
            if filename.endswith(".png"): #
                key = filename.replace(".png", "") # e.g., "cardSpadesK" #
                image = pygame.image.load(os.path.join(cards_path, filename)).convert_alpha() #
                self.card_images[key] = pygame.transform.scale(image, (70 * st.SCALE, 98 * st.SCALE)) #
        # Add back of card image #
        back_image = pygame.image.load(os.path.join(st.img_folder, "X.png")).convert_alpha() #
        self.card_images["back"] = pygame.transform.scale(back_image, (70 * st.SCALE, 98 * st.SCALE)) #


    def handle_event(self, event): #
        if self.game.state == "PLAYER_TURN": #
            if event.type == pygame.KEYDOWN: #
                if event.key in (pygame.K_z, pygame.K_h): # 'Z' or 'H' to Hit #
                    self.ok_sound.play() #
                    self.game.player_hit() #
                elif event.key in (pygame.K_x, pygame.K_s): # 'X' or 'S' to Stand #
                    self.ok_sound.play() #
                    self.game.player_stand() #
        
        elif self.game.state == "ROUND_OVER": #
            if event.type == pygame.KEYDOWN: #
                if event.key in (pygame.K_z, pygame.K_RETURN): #
                    # Decide whether to start a new round or exit #
                    if self.game.player.getPoints() >= 10: #
                        self.game.start_round() # Play again #
                    else:
                        self.next_screen = "UPDATE_PLAYER_DATA" # Not enough points, exit to menu #
    
    def sync_sprites_with_model(self): #
        """Updates the card sprites on screen to match the game model.""" #
        self.card_sprites.empty() #
        # Sync dealer's hand #
        for i, card in enumerate(self.game.table.getCards()): #
            pos = (400 + i * 80, 120) #
            image_key = card.get_image_path() if card.getFace() else "back" #
            self.card_sprites.add(CardSprite(pos, self.card_images[image_key])) #
        # Sync player's hand #
        for i, card in enumerate(self.game.player.getCards()): #
            pos = (400 + i * 80, 350) #
            image_key = card.get_image_path() #
            self.card_sprites.add(CardSprite(pos, self.card_images[image_key])) #

    def draw(self): #
        self.screen.blit(self._background, (0, 0)) #
        self.sync_sprites_with_model() #
        self.card_sprites.draw(self.screen) #
        
        # Draw scores #
        dealer_score_text = f"Dealer's Hand: {self.game.table.sumValues() if self.game.state != 'PLAYER_TURN' else '?'}" #
        player_score_text = f"{self.game.player.getName()}'s Hand: {self.game.player.sumValues()}" #
        draw_text_with_outline(self.screen, dealer_score_text, self.font, (st.SCREEN_WIDTH/2, 40), st.WHITE, st.BLACK) #
        draw_text_with_outline(self.screen, player_score_text, self.font, (st.SCREEN_WIDTH/2, 450), st.WHITE, st.BLACK) #

        # Draw prompts or results #
        if self.game.state == "PLAYER_TURN": #
            prompt = "Press [Z] to Hit, [X] to Stand" #
            draw_text_with_outline(self.screen, prompt, self.font, (st.SCREEN_WIDTH/2, 250), st.GREEN, st.BLACK) #
        elif self.game.state == "ROUND_OVER": #
            result_text = f"Result: {self.game.result}" #
            prompt = "Press [Z] to play again." if self.game.player.getPoints() >= 10 else "Not enough points. Press [Z] to exit." #
            draw_text_with_outline(self.screen, result_text, pygame.font.Font(st.button_font, 32), (st.SCREEN_WIDTH/2, 240), st.MAGENTA, st.BLACK) #
            draw_text_with_outline(self.screen, prompt, self.font, (st.SCREEN_WIDTH/2, 280), st.WHITE, st.BLACK) #

    def get_player_data(self): #
        """Returns the updated player data when the game is over.""" #
        return self.game.get_player_data() #

class NotificationScreen(Screen): #
    """A simple screen to display a message for a short time before transitioning.""" #
    def __init__(self, screen, message, next_screen, player_data=None): #
        super().__init__(screen, player_data) #
        self.message = message #
        self.next_screen_key = next_screen #
        self.font = pygame.font.Font(st.button_font, st.title_size) #
        self.set_background(os.path.join(st.img_folder, "title.png")) #
        self.entry_time = pygame.time.get_ticks() #

    def handle_event(self, event): #
        # Transition on key press or after a delay #
        if event.type == pygame.KEYDOWN or pygame.time.get_ticks() - self.entry_time > 2000: #
            self.next_screen = self.next_screen_key #
            
    def draw(self): #
        self.screen.blit(self._background, (0,0)) #
        draw_text_with_outline(self.screen, self.message, self.font, (st.SCREEN_WIDTH/2, st.SCREEN_HEIGHT/2), st.WHITE, st.BLACK) #

# --- SPRITE CLASSES ---

class Button(pygame.sprite.Sprite): #
    def __init__(self, xy_pos, message, action, font_size=st.button_size): #
        super().__init__() #
        self.__message = message #
        self.action = action #
        self.__font = pygame.font.Font(st.button_font, font_size) #
        self.__is_selected = False #
        self.__colors = [st.WHITE, st.GREEN] #
        self.image = self.__font.render(self.__message, True, self.__colors[0]) #
        self.rect = self.image.get_rect(center=xy_pos) #
    
    def set_selected(self, is_selected): #
        self.__is_selected = is_selected #

    def update(self): #
        color = self.__colors[1] if self.__is_selected else self.__colors[0] #
        self.image = self.__font.render(self.__message, True, color) #

class CardSprite(pygame.sprite.Sprite): #
    def __init__(self, pos, image): #
        super().__init__() #
        self.image = image #
        self.rect = self.image.get_rect(center=pos) #