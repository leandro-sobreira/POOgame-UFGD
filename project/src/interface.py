import pygame
import os
from . import setup as st
import random
from abc import ABC, abstractmethod
from . import database_manager as db

# --- ABSTRACT SCREEN CLASS (BASE FOR ALL SCREENS) ---
class Screen(ABC): 
    """
    An abstract base class for all game screens.
    Ensures that every screen has a consistent structure and behavior.
    """ 
    def __init__(self, screen, player_name=None):
        self.screen = screen
        self.player_name = player_name
        self.next_screen = None
        self._background = None

        # Load common sounds
        
        #self.select_sound = pygame.mixer.Sound(os.path.join(st.sound_folder, "computer-processing-sound-effects-short-click-select-02-122133.ogg")) 
        #self.ok_sound = pygame.mixer.Sound(os.path.join(st.sound_folder, "computer-processing-sound-effects-short-click-select-01-122134.ogg"))
        #self.select_sound.set_volume(0.2)
        #self.ok_sound.set_volume(0.2)
        #self.reset_sound.set_volume(0.2)
        
        self.select_sound = pygame.mixer.Sound(os.path.join(st.sound_folder, "short-click-select_02.ogg")) 
        self.ok_sound = pygame.mixer.Sound(os.path.join(st.sound_folder, "short-click-select_01.ogg")) 
        self.reset_sound = pygame.mixer.Sound(os.path.join(st.sound_folder, "reset.ogg")) 
        self.flip_card = pygame.mixer.Sound(os.path.join(st.sound_folder, "flipcard.ogg"))

    def set_background(self, image_path): 
        """Sets and scales the background image.""" 
        background = pygame.image.load(image_path).convert() 
        self._background = pygame.transform.scale(background, self.screen.get_size()) 

    def set_music(self, music_path, volume=0.2): 
        """Loads and plays background music in a loop.""" 
        pygame.mixer.music.load(music_path) 
        pygame.mixer.music.set_volume(volume) 
        pygame.mixer.music.play(-1) 

    def draw_text_with_outline(self, surface, text, font, pos, text_color, outline_color, outline_width=2, rotation=0): 
        """Renders text with a simple outline.""" 
        x, y = pos 
        # Render outline 
        for dx in range(-outline_width, outline_width + 1): 
            for dy in range(-outline_width, outline_width + 1): 
                if dx != 0 or dy != 0: 
                    outline_surf = font.render(text, True, outline_color) 
                    if rotation != 0:
                        outline_surf = pygame.transform.rotate(outline_surf, rotation)
                    surface.blit(outline_surf, (x - outline_surf.get_width() // 2 + dx, y - outline_surf.get_height() // 2 + dy)) 
        # Render main text 
        text_surf = font.render(text, True, text_color) 
        if rotation != 0:
            text_surf = pygame.transform.rotate(text_surf, rotation)
        surface.blit(text_surf, (x - text_surf.get_width() // 2, y - text_surf.get_height() // 2)) 


    @abstractmethod
    def handle_event(self, event): 
        """Abstract method to handle screen-specific events.""" 
        pass 

    @abstractmethod
    def update(self): 
        """Abstract method for per-frame logic updates.""" 
        pass 

    @abstractmethod
    def draw(self): 
        """Abstract method to draw the screen's elements.""" 
        pass 

    def loop(self): 
        """
        The main loop for a screen. It handles events, updates, and drawing.
        Returns the key for the next screen to be displayed.
        """ 
        is_running = True 
        while is_running: 
            st.clock.tick(st.FPS) 

            for event in pygame.event.get(): 
                if event.type == pygame.QUIT: 
                    self.next_screen = "QUIT" 
                # Pass the event to the specific handler of the child screen 
                self.handle_event(event) 
            self.update() # Call update for continuous logic 
            self.draw() 
            pygame.display.flip() 
            
            if self.next_screen: 
                is_running = False 
        
        return self.next_screen 

class PlayerNameScreen(Screen): 
    def __init__(self, screen, prompt_text="Enter Your Name and Press Enter"): 
        super().__init__(screen) 
        self.set_background(os.path.join(st.img_folder, "title.png")) 
        self.__font = pygame.font.Font(st.text_font, 32) 
        self.input_font = pygame.font.Font(st.text_font, 28) 
        self.player_name = "" 
        self.prompt_text = prompt_text 

    def handle_event(self, event): 
        if event.type == pygame.KEYDOWN: 
            if event.key in [pygame.K_RETURN, pygame.K_KP_ENTER]: 
                self.ok_sound.play() 
                self.next_screen = "GET_PLAYER" 
            elif event.key == pygame.K_BACKSPACE: 
                self.player_name = self.player_name[:-1] 
            else:
                if event.unicode.isprintable() and len(self.player_name) < 15: # Limit name length 
                    self.player_name += event.unicode 

    def update(self): 
        pass 

    def draw(self): 
        self.screen.blit(self._background, (0, 0)) 
        self.draw_text_with_outline(self.screen, self.prompt_text, self.__font, (st.SCREEN_WIDTH / 2, st.SCREEN_HEIGHT / 2 - 50), st.WHITE, st.BLACK) 
        
        input_rect = pygame.Rect(st.SCREEN_WIDTH / 2 - 150, st.SCREEN_HEIGHT / 2, 300, 50) 
        pygame.draw.rect(self.screen, st.WHITE, input_rect, 2) 
        input_surface = self.input_font.render(self.player_name, True, st.WHITE) 
        self.screen.blit(input_surface, (input_rect.x + 10, input_rect.y + 10)) 

class MenuScreen(Screen): 
    def __init__(self, screen, player_name): 
        super().__init__(screen, player_name) 
        self.set_background(os.path.join(st.img_folder, "title.png")) 
        self.set_music(os.path.join(st.sound_folder, "1197551_Butterflies.ogg")) 
        self.title_font = pygame.font.Font(os.path.join(st.font_folder, st.title_font), st.title_size) 
        
        self.buttons = [ 
            Button((st.SCREEN_WIDTH/2, st.SCREEN_HEIGHT - 200), "Start", "GAME_SELECT"), 
            Button((st.SCREEN_WIDTH/2, st.SCREEN_HEIGHT - 150), "Erase Data", "ERASE_DATA"), 
            Button((st.SCREEN_WIDTH/2, st.SCREEN_HEIGHT - 100), "Scores", "SCORES"), 
            Button((st.SCREEN_WIDTH/2, st.SCREEN_HEIGHT - 50), "Quit", "QUIT") 
        ]
        self.selected_index = 0 
        self.all_sprites = pygame.sprite.Group(self.buttons) 

    def handle_event(self, event): 
        if event.type == pygame.KEYDOWN: 
            if event.key in (pygame.K_UP, pygame.K_w): 
                self.select_sound.play() 
                self.selected_index = (self.selected_index - 1) % len(self.buttons) 
            elif event.key in (pygame.K_DOWN, pygame.K_s): 
                self.select_sound.play() 
                self.selected_index = (self.selected_index + 1) % len(self.buttons) 
            elif event.key in (pygame.K_z, pygame.K_RETURN): 
                selected_button = self.buttons[self.selected_index] 
                self.ok_sound.play() 
                self.next_screen = selected_button.action 

    def update(self): 
        pass 

    def draw(self):
        self.screen.blit(self._background, (0, 0))
        self.draw_text_with_outline(self.screen, "CARD GAME", self.title_font, (st.SCREEN_WIDTH/2, st.SCREEN_HEIGHT/4), st.BLACK, st.WHITE)
        
        # CORREÇÃO AQUI:
        # A linha antiga que causava o erro foi substituída.
        # Agora usamos self.player_name e não exibimos mais os pontos.
        welcome_text = f"Welcome, {self.player_name}!"
        self.draw_text_with_outline(self.screen, welcome_text, pygame.font.Font(st.button_font, 22), (st.SCREEN_WIDTH/2, st.SCREEN_HEIGHT/2), st.WHITE, st.BLACK)

        for i, button in enumerate(self.buttons):
            button.set_selected(i == self.selected_index)
        self.all_sprites.update()
        self.all_sprites.draw(self.screen)

class GameSelectScreen(Screen): 
    def __init__(self, screen, player_name): 
        super().__init__(screen, player_name) 
        self.set_background(os.path.join(st.img_folder, "games/blackjack/mesa.png")) 
        self.title_font = pygame.font.Font(st.button_font, st.title_size) 

        self.buttons = [ 
            Button((st.SCREEN_WIDTH/2, 200), "Blackjack", "BLACKJACK"), 
            Button((st.SCREEN_WIDTH/2, 250), "UNO", "UNO"), 
            Button((st.SCREEN_WIDTH/2, 350), "Back to Menu", "MENU") 
        ]
        self.selected_index = 0 
        self.all_sprites = pygame.sprite.Group(self.buttons) 

    def handle_event(self, event): 
        if self.selected_index == 0:
            background = os.path.join(st.img_folder, "games/blackjack/mesa.png")
        elif self.selected_index == 1:
            background = os.path.join(st.img_folder, "games/uno/mesa.png")
        else:
            background = os.path.join(st.img_folder, "title.png")
        self.set_background(os.path.join(st.img_folder, background))
        if event.type == pygame.KEYDOWN: 
            if event.key in (pygame.K_UP, pygame.K_w): 
                self.select_sound.play() 
                self.selected_index = (self.selected_index - 1) % len(self.buttons) 
            elif event.key in (pygame.K_DOWN, pygame.K_s): 
                self.select_sound.play() 
                self.selected_index = (self.selected_index + 1) % len(self.buttons) 
            elif event.key in (pygame.K_z, pygame.K_RETURN): 
                self.ok_sound.play() 
                self.next_screen = self.buttons[self.selected_index].action 

    def update(self): 
        pass 
    
    def draw(self): 
        self.screen.blit(self._background, (0, 0)) 
        self.draw_text_with_outline(self.screen, "Select a Game", self.title_font, (st.SCREEN_WIDTH/2, 80), st.WHITE, st.BLACK) 
        for i, button in enumerate(self.buttons): 
            button.set_selected(i == self.selected_index) 
        self.all_sprites.update() 
        self.all_sprites.draw(self.screen) 

# In src/interface.py, replace the entire ScoresScreen class with this one.

class ScoresScreen(Screen):
    def __init__(self, screen):
        super().__init__(screen)
        self.set_background(os.path.join(st.img_folder, "title.png"))
        self.__title_font = pygame.font.Font(st.text_font, 42)
        self.__text_font = pygame.font.Font(st.text_font, 32)
        
        # --- Internal State ---
        self.__page = "GAME_SELECT"  # Start on the game selection page
        self.__selected_game_index = 0
        self.__scroll_offset = 0
        self.__visible_rows = 12
        
        # --- Data Loading and Processing ---
        all_wins = db.get_all_wins()
        # Create a dictionary to hold scores for each game
        self.__game_scores = {
            "Blackjack": [],
            "Uno": []
        }
        for win in all_wins:
            game_name = win.get("game") # Get the game name from the win record
            if game_name in self.__game_scores:
                self.__game_scores[game_name].append(win)

        # Sort scores for each game by score in descending order, for each game individually
        for game in self.__game_scores:
            self.__game_scores[game].sort(key=lambda x: x["score"], reverse=True)
        
        # Create a list of games that have at least one score recorded
        self.__available_games = [game for game, scores in self.__game_scores.items() if scores]

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            # --- Event Handling for GAME_SELECT page ---
            if self.__page == "GAME_SELECT":
                if event.key in (pygame.K_x, pygame.K_ESCAPE):
                    self.ok_sound.play()
                    self.next_screen = "MENU"
                
                # Only allow navigation if there are games with scores
                if self.__available_games:
                    if event.key in (pygame.K_UP, pygame.K_w):
                        self.select_sound.play()
                        self.__selected_game_index = (self.__selected_game_index - 1) % len(self.__available_games)
                    elif event.key in (pygame.K_DOWN, pygame.K_s):
                        self.select_sound.play()
                        self.__selected_game_index = (self.__selected_game_index + 1) % len(self.__available_games)
                    elif event.key in (pygame.K_z, pygame.K_RETURN):
                        self.ok_sound.play()
                        self.__page = "SCORES"  # Switch to the scores page
                        self.__scroll_offset = 0  # Reset scroll for the new list

            # --- Event Handling for SCORES page ---
            elif self.__page == "SCORES":
                if event.key in (pygame.K_x, pygame.K_ESCAPE):
                    self.ok_sound.play()
                    self.__page = "GAME_SELECT"  # Go back to the game selection page
                
                # Scrolling logic for the scores list
                selected_game = self.__available_games[self.__selected_game_index]
                if self.__game_scores[selected_game]:
                    if event.key in (pygame.K_UP, pygame.K_w):
                        self.select_sound.play()
                        self.__scroll_offset = max(0, self.__scroll_offset - 1)
                    elif event.key in (pygame.K_DOWN, pygame.K_s):
                        self.select_sound.play()
                        max_scroll = len(self.__game_scores[selected_game]) - self.__visible_rows
                        self.__scroll_offset = min(max(0, max_scroll), self.__scroll_offset + 1)

    def update(self):
        pass

    def draw(self):
        self.screen.blit(self._background, (0, 0))
        self.draw_text_with_outline(self.screen, "Press ESC to go back", self.__text_font, (st.SCREEN_WIDTH/2, st.SCREEN_HEIGHT - 40), st.WHITE, st.BLACK)

        # --- Drawing logic for GAME_SELECT page ---
        if self.__page == "GAME_SELECT":
            self.draw_text_with_outline(self.screen, "Select a Game to View Scores", self.__title_font, (st.SCREEN_WIDTH/2, 80), st.WHITE, st.BLACK)
            
            if not self.__available_games:
                self.draw_text_with_outline(self.screen, "No scores recorded yet.", self.__text_font, (st.SCREEN_WIDTH/2, 300), st.WHITE, st.BLACK)
            else:
                for i, game_name in enumerate(self.__available_games):
                    y_pos = 200 + i * 50
                    color = st.GREEN if i == self.__selected_game_index else st.WHITE
                    self.draw_text_with_outline(self.screen, game_name, self.__text_font, (st.SCREEN_WIDTH/2, y_pos), color, st.BLACK)

        # --- Drawing logic for SCORES page ---
        elif self.__page == "SCORES":
            selected_game_name = self.__available_games[self.__selected_game_index]
            scores_for_game = self.__game_scores[selected_game_name]
            
            self.draw_text_with_outline(self.screen, f"{selected_game_name} Rankings", self.__title_font, (st.SCREEN_WIDTH/2, 60), st.WHITE, st.BLACK)
            
            # Draw headers
            header_y = 120
            self.draw_text_with_outline(self.screen, "Player", self.__text_font, (st.SCREEN_WIDTH/4, header_y), st.YELLOW, st.BLACK)
            self.draw_text_with_outline(self.screen, "Score", self.__text_font, (st.SCREEN_WIDTH/2, header_y), st.YELLOW, st.BLACK)
            self.draw_text_with_outline(self.screen, "Date", self.__text_font, (st.SCREEN_WIDTH * 3/4, header_y), st.YELLOW, st.BLACK)

            # Draw scores
            visible_wins = scores_for_game[self.__scroll_offset : self.__scroll_offset + self.__visible_rows]
            for i, win in enumerate(visible_wins):
                y_pos = 180 + i * 40
                self.draw_text_with_outline(self.screen, win['player_name'], self.__text_font, (st.SCREEN_WIDTH/4, y_pos), st.WHITE, st.BLACK)
                self.draw_text_with_outline(self.screen, str(win['score']), self.__text_font, (st.SCREEN_WIDTH/2, y_pos), st.GREEN, st.BLACK)
                self.draw_text_with_outline(self.screen, win['date'], self.__text_font, (st.SCREEN_WIDTH * 3/4, y_pos), st.WHITE, st.BLACK)

class BlackjackScreen(Screen): 
    """The View for the Blackjack game. It only draws what the Model tells it to.""" 
    def __init__(self, screen, game_instance): 
        super().__init__(screen) 
        self.__game = game_instance  # This is the Model 
        self.__current_action_phase = None 
        self.__assets_folder = os.path.join(st.img_folder, "games/blackjack")
        self.set_background(os.path.join(self.__assets_folder, "mesa.png")) 
        self.__selected_opc = 0
        self.__font = pygame.font.Font(st.text_font, 32)
        self.__card_sprites = pygame.sprite.Group() 
        self.load_card_images() 
        self.__input_value = ''
        self.__amount = 0
        
    def load_card_images(self): 
        """Pre-loads all card images into a dictionary for quick access.""" 
        self.card_images = {} 
        cards_path = os.path.join(self.__assets_folder, "cards") # 
        for filename in os.listdir(cards_path): 
            if filename.endswith(".png"): 
                key = filename.replace(".png", "") # e.g., "king_of_spade" 
                image = pygame.image.load(os.path.join(cards_path, filename)).convert_alpha() 
                self.card_images[key] = pygame.transform.scale(image, (70 * st.SCALE, 98 * st.SCALE)) 

    def handle_event(self, event): 
        if self.__game.state == "BET":
            if event.type == pygame.KEYDOWN:
                #if event.key in [pygame.K_RETURN, pygame.K_KP_ENTER] and self.__input_value != '':

                if event.key == pygame.K_RETURN and self.__input_value != "":
                    self.__amount = int(self.__input_value)
                    
                    self.__game.betAmount = self.__amount
                    #print("recebi", self.__game.bet_amount)
                    self.__game.state = "PLAYER_TURN"
                elif event.key == pygame.K_BACKSPACE:
                    self.__input_value = self.__input_value[:-1]
                elif event.unicode.isdigit():
                    self.__input_value += event.unicode
                    
            self.__game.setBetAmount()

        elif self.__game.state == "PLAYER_TURN": 
            if event.type == pygame.KEYDOWN: 
                if event.key in (pygame.K_z, pygame.K_h): # 'Z' or 'H' to Hit 
                    self.flip_card.play() 
                    self.__game.player_hit() 

                elif event.key in (pygame.K_x, pygame.K_s): # 'X' or 'S' to Stand 
                    self.ok_sound.play() 
                    self.__game.player_stand() 
        
            """elif self.__game.state == "ROUND_OVER": 
                if event.type == pygame.KEYDOWN: 
                    if event.key in (pygame.K_z, pygame.K_RETURN): 
                        # Decide whether to start a new round or exit 
                        if self.__game.player.points >= 10: 
                            self.__game.state = "BET"
                            #self.__game.setBetAmount() # Play again 
                        else:
                            self.next_screen = "UPDATE_PLAYER_DATA" # Not enough points, exit to menu 
                    elif event.key in (pygame.K_x, pygame.K_ESCAPE):
                        self.next_screen = "MENU" """
        
        elif self.__game.state == "ROUND_OVER":
            buttons = ['yes', 'no']

            if event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_RIGHT, pygame.K_d):
                    self.select_sound.play()
                    self.__selected_opc = (self.__selected_opc + 1) % len(buttons)
                elif event.key in (pygame.K_LEFT, pygame.K_a):
                    self.select_sound.play()
                    self.__selected_opc = (self.__selected_opc - 1) % len(buttons)
                elif event.key in (pygame.K_z, pygame.K_RETURN):
                    # Player chose 'Quit' (index 1)
                    if self.__selected_opc == 1:
                        # If the player won, return data to be logged
                        if "Win" in self.__game.result:
                            final_score = self.__game.player.points
                            self.next_screen = ("LOG_WIN", final_score, "Blackjack")
                        else: # If they lost or tied, just return to menu
                            self.next_screen = "MENU"
                    else: # Player chose to play again
                        if self.__game.player.points >= 10:
                            self.__game.state = "BET"
                            self.__input_value = '' # Reset bet input
                        else: # Not enough points, offer a restart
                            self.__game.player.points = 1000
                            self.__game.state = "BET"
                            self.__input_value = '' # Reset bet input
    
    def sync_sprites_with_model(self): 
        #Updates the card sprites on screen to match the game model. 
        self.__card_sprites.empty() 
        # Sync dealer's hand 
        for i, card in enumerate(self.__game.table.cards): 
            pos = ((st.SCREEN_WIDTH/2 - (len(self.__game.table.cards)*20)/2 + i * 20)*st.SCALE, 120) 
            image_key = card.sprite
            self.__card_sprites.add(CardSprite(pos, self.card_images[image_key])) 
        # Sync player's hand 
            
        for i, card in enumerate(self.__game.player.cards): 
            pos = ((st.SCREEN_WIDTH/2 - (len(self.__game.player.cards)*20)/2 + i * 20)*st.SCALE, (st.SCREEN_HEIGHT*6/8 +i*15)*st.SCALE) 
            image_key = card.sprite
            self.__card_sprites.add(CardSprite(pos, self.card_images[image_key])) 

        
    def update(self): 
        current_game_state = self.__game.state

        if current_game_state == "START":
            if self.__current_action_phase is None:
                self.__current_action_phase = "giving_cards"
                self.__action_timer = pygame.time.get_ticks() + 350
            elif self.__current_action_phase == "giving_cards":
                if pygame.time.get_ticks() >= self.__action_timer:
                    self.__game.give_start_cards()
                    self.__current_action_phase = None

        elif current_game_state == "DEALER_TURN":
            if self.__current_action_phase is None:
                self.__current_action_phase = "dealer_buying"
                self.__action_timer = pygame.time.get_ticks() + 1000 # 1.5-second delay
            elif self.__current_action_phase == "dealer_buying":
                if pygame.time.get_ticks() >= self.__action_timer:
                    self.__game._dealer_play() # Bot performs its action
                    self.__current_action_phase = None # Reset phase; game state will change

    def draw(self): 
        self.screen.blit(self._background, (0, 0)) 
        self.sync_sprites_with_model() 
        self.__card_sprites.draw(self.screen) 

        self.draw_text_with_outline(self.screen, f'{self.__game.player.points}$', self.__font, (st.SCREEN_WIDTH*1/8, st.SCREEN_HEIGHT*1/12), st.GREEN, st.BLACK) 
        
        # Draw scores 
        dealer_score_text = f"Dealer's Hand: {self.__game.table.sumValues()}" 
        player_score_text = f"{self.__game.player.name}'s Hand: {self.__game.player.sumValues()}" 
        self.draw_text_with_outline(self.screen, dealer_score_text, self.__font, (st.SCREEN_WIDTH/2, 40), st.WHITE, st.BLACK) 
        self.draw_text_with_outline(self.screen, player_score_text, self.__font, (st.SCREEN_WIDTH/2, st.SCREEN_HEIGHT*4/5+100), st.WHITE, st.BLACK) 

        

        # Draw prompts or results 
        if self.__game.state == "BET":

            self.done = False
            box_width = 450
            box_height = 150
            pos = pygame.Rect((st.SCREEN_WIDTH - box_width) / 2,(st.SCREEN_HEIGHT - box_height) / 2,box_width, box_height )
            pygame.draw.rect(self.screen, st.BLACK, pos)  # fundo da caixa
            pygame.draw.rect(self.screen, st.WHITE, pos, 2)  # borda branca

            # Renderiza o texto do prompt
            prompt_surface = self.__font.render("Enter the bet amount", True, st.WHITE)
            prompt_rect = prompt_surface.get_rect(center=(st.SCREEN_WIDTH / 2, st.SCREEN_HEIGHT / 2 - 40))
            self.screen.blit(prompt_surface, prompt_rect)

            # Renderiza o valor digitado
            input_surface = self.__font.render(self.__input_value, True, st.GREEN)
            input_rect = input_surface.get_rect(center=(st.SCREEN_WIDTH / 2, st.SCREEN_HEIGHT / 2 + 10))
            self.screen.blit(input_surface, input_rect)
    
        elif self.__game.state == "PLAYER_TURN": 
            prompt = "Z Hit" 
            self.draw_text_with_outline(self.screen, prompt, self.__font, (st.SCREEN_WIDTH*7/8, st.SCREEN_HEIGHT*11/12), st.GREEN, st.BLACK) 
            prompt = "X Stand" 
            self.draw_text_with_outline(self.screen, prompt, self.__font, (st.SCREEN_WIDTH*7/8, st.SCREEN_HEIGHT*11/12-25), st.GREEN, st.BLACK) 

            """elif self.__game.state == "ROUND_OVER": 
            result_text = f"Result: {self.__game.result}" 
            self.draw_text_with_outline(self.screen, result_text, pygame.font.Font(st.text_font, 32), (st.SCREEN_WIDTH/2, 240), st.MAGENTA, st.BLACK) 
            prompt = "Press [Z] to play again." if self.__game.player.points >= 10 else "Not enough points. Press [Z] to exit." 
            self.draw_text_with_outline(self.screen, prompt, self.__font, (st.SCREEN_WIDTH/2, 280), st.WHITE, st.BLACK) 
            if self.__game.player.points >= 10:
                prompt = "Or [X] to quit and save your score"
                self.draw_text_with_outline(self.screen, prompt, self.__font, (st.SCREEN_WIDTH/2, 320), st.WHITE, st.BLACK) #  """
            
        elif self.__game.state == "ROUND_OVER":
            buttons = ['yes', 'no']
            opc_buttons = [
                Button((st.SCREEN_WIDTH/2 - 150, st.SCREEN_HEIGHT/2+100), "Yes", "yes", 30),
                Button((st.SCREEN_WIDTH/2 + 150, st.SCREEN_HEIGHT/2+100), "Quit", "no", 30)
            ]
            for i, button in enumerate(opc_buttons):
                button.set_selected(i == self.__selected_opc)
            color_sprite_group = pygame.sprite.Group(opc_buttons)
            color_sprite_group.update()
            color_sprite_group.draw(self.screen)
            self.draw_text_with_outline(self.screen, self.__game.result, pygame.font.Font(st.text_font, 32), (st.SCREEN_WIDTH/2, 240), st.MAGENTA, st.BLACK) 
            self.draw_text_with_outline(self.screen, f'+{self.__game.win_value}$', pygame.font.Font(st.text_font, 32), (st.SCREEN_WIDTH/2, 280), st.YELLOW, st.BLACK) 
            prompt = "Bet again? (Quit to save points)" if self.__game.player.points >= 10 else "Not enough points. Restart?"   
            self.draw_text_with_outline(self.screen, prompt, self.__font, (st.SCREEN_WIDTH/2, st.SCREEN_HEIGHT/2 +50), st.WHITE, st.BLACK) # 
            

    def get_player_data(self): 
        """Returns the updated player data when the game is over.""" 
        return self.__game.get_player_data() 
    
class UnoScreen(Screen):
    def __init__(self, screen, game_instance):
        super().__init__(screen)
        self.__game = game_instance
        self.__assets_folder = os.path.join(st.img_folder, "games/uno")
        self.set_background(os.path.join(self.__assets_folder, "mesa.png"))
        self.__selected_card = 0
        self.__selected_color = 0
        self.__selected_opc = 0
        self.__card_sprites = pygame.sprite.Group() 
        self.__action_timer = 0 # Timer for timed actions
        self.__current_action_phase = None # To manage multi-step timed actions
        self.load_card_images()


    def load_card_images(self): 
        """Pre-loads all card images into a dictionary for quick access.""" 
        self.card_images = {} 
        cards_path = os.path.join(self.__assets_folder, "cards") 
        for filename in os.listdir(cards_path): 
            if filename.endswith(".png"): 
                key = filename.replace(".png", "") # e.g., "blue_2" 
                image = pygame.image.load(os.path.join(cards_path, filename)).convert_alpha() 
                self.card_images[key] = pygame.transform.scale(image, (st.UNO_CARD_WIDTH, st.UNO_CARD_HEIGHT))
    def card_position(self, player_index, card_index):
        card_spacement = 50
        return (len(self.__game.players[player_index].cards)-1)*card_spacement/2-card_index*card_spacement
    
    def sync_sprites_with_model(self):
        self.__card_sprites.empty()
    # Sync Bots
        for i in range(1,4):
            for j, card in enumerate(self.__game.players[i].cards):
                image_key = card.sprite
                if i == 1:
                    pos = (st.SCREEN_WIDTH*1/10 , (st.SCREEN_HEIGHT-self.card_position(1,j))/2)
                    rotate = 90
                elif i == 2:
                    pos = ((st.SCREEN_WIDTH-self.card_position(2,j))/2, st.SCREEN_HEIGHT*1/8)
                    rotate = 0
                elif i == 3:
                    pos = (st.SCREEN_WIDTH*9/10 , (st.SCREEN_HEIGHT-self.card_position(3,j))/2)
                    rotate = -90
                self.__card_sprites.add(CardSprite(pos, pygame.transform.rotate(self.card_images[image_key],rotate)))

    # Sync Player hand 
        for i, card in enumerate(self.__game.players[0].cards): 
            posx=(st.SCREEN_WIDTH-self.card_position(0,i))/2
            posy=st.SCREEN_HEIGHT*7/8
            if self.__selected_card >= 0:
                if i <= self.__selected_card and i >= 0:
                    posx -= st.UNO_CARD_WIDTH/4
                else:
                    posx += st.UNO_CARD_WIDTH/4
            if i == self.__selected_card:
                posy -= 35
            elif self.__game.disc_deck.topCard() and self.__game.players[0].cards[i].match(self.__game.disc_deck.topCard()):
                posy -= 10
            pos = (posx, posy)
            image_key = card.sprite
            self.__card_sprites.add(CardSprite(pos, self.card_images[image_key])) 

    # Sync Discard Deck 
        pos = (st.SCREEN_WIDTH/2, st.SCREEN_HEIGHT/2)
        image_key = self.__game.disc_deck.topCard().sprite   
        self.__card_sprites.add(CardSprite(pos, self.card_images[image_key]))

    # Sync Buy Deck 
        if self.__game.buy_deck.isEmpty():
            self.__game.reshuffle_buy_deck()
        image_key = self.__game.buy_deck.topCard().sprite
        for i in range(-1,int(self.__game.buy_deck.size()/5)):
            pos = (st.SCREEN_WIDTH*7/10+i*2, st.SCREEN_HEIGHT*2/5+i)
            if i == int(self.__game.buy_deck.size()/5)-1 and self.__selected_card == -1 and not self.__game.players.already_buy:
                pos = (st.SCREEN_WIDTH*7/10+i*2, st.SCREEN_HEIGHT*2/5+i+30)
            self.__card_sprites.add(CardSprite(pos, self.card_images[image_key])) 
            
    def draw(self):
        self.screen.blit(self._background, (0, 0))
        self.sync_sprites_with_model()
        self.__card_sprites.draw(self.screen)

        #place the names
        for i in range(4):
            rotation = 0
            text_color = st.WHITE
            if i == 0:
                pos = (st.SCREEN_WIDTH/2, st.SCREEN_HEIGHT*7/8+50)
            elif i == 1:
                pos = (st.SCREEN_WIDTH*1/10-50, st.SCREEN_HEIGHT/2)
                rotation = -90
            elif i == 2:
                pos = (st.SCREEN_WIDTH/2, st.SCREEN_HEIGHT*1/8-50)
            elif i == 3:
                pos = (st.SCREEN_WIDTH*9/10+50, st.SCREEN_HEIGHT/2)
                rotation = 90
            if i == self.__game.players.turn:
                text_color = st.GREEN
            self.draw_text_with_outline(self.screen, self.__game.players[i].name, pygame.font.Font(st.button_font, 20), (pos), text_color, st.BLACK, 2, rotation)

        #place de rotacion image        
        if self.__game.players.rotation == 1:
            rotation_image = pygame.image.load(os.path.join(self.__assets_folder, "rotation.png")).convert_alpha()
            rect = rotation_image.get_rect(center=(st.SCREEN_WIDTH/2, st.SCREEN_HEIGHT/2))
            self.screen.blit(rotation_image, rect)
        else:
            rotation_image = pygame.image.load(os.path.join(self.__assets_folder, "rotation.png")).convert_alpha()
            rotation_image = pygame.transform.flip(rotation_image, True, False)
            rect = rotation_image.get_rect(center=(st.SCREEN_WIDTH/2, st.SCREEN_HEIGHT/2))
            self.screen.blit(rotation_image, rect)

        if self.__game.state == "PLAYER_TURN":
            text_color = st.WHITE
            if self.__game.players.already_buy:
                if self.__selected_card == -1:
                    text_color = st.GREEN
                self.draw_text_with_outline(self.screen, "Skip", pygame.font.Font(st.button_font, 20), (st.SCREEN_WIDTH/2, st.SCREEN_HEIGHT*5/8), text_color, st.BLACK)

        elif self.__game.state == "PLAYER_SELEC_COLOR":
            colors = ['red','yellow','green','blue']
            color_buttons = [
                Button((st.SCREEN_WIDTH/2 - 150, st.SCREEN_HEIGHT/2+100), "Red", "red", 30),
                Button((st.SCREEN_WIDTH/2 - 50, st.SCREEN_HEIGHT/2+100), "Yellow", "yellow", 30),
                Button((st.SCREEN_WIDTH/2 + 50, st.SCREEN_HEIGHT/2+100), "Green", "green", 30),
                Button((st.SCREEN_WIDTH/2 + 150, st.SCREEN_HEIGHT/2+100), "Blue", "blue", 30)
            ]
            for i, button in enumerate(color_buttons):
                button.set_selected(i == self.__selected_color)
            color_sprite_group = pygame.sprite.Group(color_buttons)
            self.__game.disc_deck.topCard().color = colors[self.__selected_color]
            color_sprite_group.update()
            color_sprite_group.draw(self.screen)
            self.draw_text_with_outline(self.screen, "Select a color", pygame.font.Font(st.button_font, 30), (st.SCREEN_WIDTH/2, st.SCREEN_HEIGHT/2-100), st.WHITE, st.BLACK)

        elif self.__game.state == "ROUND_OVER":
            buttons = ['yes', 'no']
            opc_buttons = [
                Button((st.SCREEN_WIDTH/2 - 150, st.SCREEN_HEIGHT/2+100), "Play Again", "yes", 30),
                Button((st.SCREEN_WIDTH/2 + 150, st.SCREEN_HEIGHT/2+100), "Quit", "no", 30)
            ]
            for i, button in enumerate(opc_buttons):
                button.set_selected(i == self.__selected_opc)
            color_sprite_group = pygame.sprite.Group(opc_buttons)
            color_sprite_group.update()
            color_sprite_group.draw(self.screen)
            if self.__game.players.getCurrentPlayer() == self.__game.players.getHumanPlayer():
                self.draw_text_with_outline(self.screen, f'{self.__game.players.getHumanPlayer().name} Win! with {self.__game.players.getHumanPlayer().points}', pygame.font.Font(st.button_font, 30), (st.SCREEN_WIDTH/2, st.SCREEN_HEIGHT/2-100), st.WHITE, st.BLACK)
            else:
                self.draw_text_with_outline(self.screen, f'You lose!', pygame.font.Font(st.button_font, 30), (st.SCREEN_WIDTH/2, st.SCREEN_HEIGHT/2-100), st.WHITE, st.BLACK)

            

    def update(self):
        current_game_state = self.__game.state

        if current_game_state == "BOT_TURN":
            if self.__current_action_phase is None:
                # Bot's turn begins, set a timer for "thinking"
                self.__current_action_phase = "bot_thinking"
                self.__action_timer = pygame.time.get_ticks() + 1500 # 1.5-second delay
            elif self.__current_action_phase == "bot_thinking":
                if pygame.time.get_ticks() >= self.__action_timer:
                    self.__game.bot_play() # Bot performs its action
                    self.__current_action_phase = None # Reset phase; game state will change
        
        # If game state changed from a timed phase, reset the phase
        elif self.__current_action_phase is not None:
             self.__current_action_phase = None

    def handle_event(self, event):
        # Possible states: START, PLAYER_TURN, PLAYER_SELEC_COLOR, BOT_TURN, ,ROUND_OVER
        current_game_state = self.__game.state



        if self.__game.state == "START":
            self.__game.start_round()


        
        elif current_game_state == "PLAYER_TURN":
            #print("PLAYER TURN")
            player_cards = self.__game.players.getHumanPlayer().cards

            if event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_LEFT, pygame.K_a):
                    self.select_sound.play()
                    self.__selected_card = ((self.__selected_card - 1) % (self.__game.players.getHumanPlayer().size()+1))
                elif event.key in (pygame.K_RIGHT, pygame.K_d):
                    self.select_sound.play()
                    self.__selected_card = ((self.__selected_card + 1) % (self.__game.players.getHumanPlayer().size()+1))
                elif event.key in (pygame.K_z, pygame.K_RETURN):
                    if self.__selected_card >= 0:
                        self.__game.player_play_card(self.__selected_card) 
                        self.flip_card.play()
                    elif self.__selected_card == -1:
                        if not self.__game.players.already_buy:
                            self.__selected_card = self.__game.player_draw_card(self.__game.players.getHumanPlayer())
                            self.__game.players.getHumanPlayer().sort
                        else:
                            self.__game.next_turn()

                if self.__selected_card >= self.__game.players.getHumanPlayer().size():
                    self.__selected_card = -1


        
        elif current_game_state == "PLAYER_SELEC_COLOR":
            #print("PLAYER SELEC COLOR")
            colors = ['red','yellow','green','blue']

            if event.type == pygame.KEYDOWN: 
                if event.key in (pygame.K_RIGHT, pygame.K_d): 
                    self.select_sound.play() 
                    self.__selected_color = (self.__selected_color + 1) % len(colors) 
                elif event.key in (pygame.K_LEFT, pygame.K_a): 
                    self.select_sound.play() 
                    self.__selected_color = (self.__selected_color - 1) % len(colors) 
                elif event.key in (pygame.K_z, pygame.K_RETURN): 
                    self.__game.human_select_color(colors[self.__selected_color])       




        elif current_game_state == "ROUND_OVER":
            buttons = ['yes', 'no']

            if event.type == pygame.KEYDOWN: 
                if event.key in (pygame.K_RIGHT, pygame.K_d): 
                    self.select_sound.play() 
                    self.__selected_opc = (self.__selected_opc + 1) % len(buttons) 
                elif event.key in (pygame.K_LEFT, pygame.K_a): 
                    self.select_sound.play() 
                    self.__selected_opc = (self.__selected_opc - 1) % len(buttons) 
                elif event.key in (pygame.K_z, pygame.K_RETURN): 
                    if self.__selected_opc == 0:
                        self.__game.start_round()
                    else:
                        self.next_screen = "MENU"

        # BOT_TURN and ROUND_OVER logic is now handled in update() for timed delays


class NotificationScreen(Screen): 
    """A simple screen to display a message for a short time before transitioning.""" 
    def __init__(self, screen, message, next_screen, player_data=None): 
        super().__init__(screen, player_data) 
        self.message = message 
        self.next_screen_key = next_screen 
        self.__font = pygame.font.Font(st.button_font, st.title_size) 
        self.set_background(os.path.join(st.img_folder, "title.png")) 
        self.entry_time = pygame.time.get_ticks() 
    
    def update(self):
        pass

    def handle_event(self, event): 
        # Transition on key press or after a delay 
        if event.type == pygame.KEYDOWN or pygame.time.get_ticks() - self.entry_time > 2000: 
            self.next_screen = self.next_screen_key 
            
    def draw(self): 
        self.screen.blit(self._background, (0,0)) 
        self.draw_text_with_outline(self.screen, self.message, self.__font, (st.SCREEN_WIDTH/2, st.SCREEN_HEIGHT/2), st.WHITE, st.BLACK) 

# --- SPRITE CLASSES ---

class Button(pygame.sprite.Sprite): 
    def __init__(self, xy_pos, message, action, font_size=st.button_size): 
        super().__init__() 
        self.__message = message 
        self.action = action 
        self.__font = pygame.font.Font(st.button_font, font_size) 
        self.__is_selected = False 
        self.__colors = [st.WHITE, st.GREEN] 
        self.image = self.__font.render(self.__message, True, self.__colors[0]) 
        self.rect = self.image.get_rect(center=xy_pos) 
    
    def set_selected(self, is_selected): 
        self.__is_selected = is_selected 

    def update(self): 
        color = self.__colors[1] if self.__is_selected else self.__colors[0] 
        self.image = self.__font.render(self.__message, True, color) 

class CardSprite(pygame.sprite.Sprite): 
    def __init__(self, pos, image): 
        super().__init__() 
        self.image = image 
        self.rect = self.image.get_rect(center=pos) #