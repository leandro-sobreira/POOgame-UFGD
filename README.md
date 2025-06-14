# UFGD Online Casino

![Gameplay GIF](Apresentation1.gif)

A suite of casino-style card games developed as a final project for an Object-Oriented Programming course at UFGD. The project showcases core OOP principles, a Model-View-Controller (MVC) architectural pattern, and game development with Pygame.

---

## Features

-   **Robust MVC Architecture:** A clean separation between game logic (Model), graphical interface (View), and flow control (Controller).
-   **Object-Oriented Screen Manager:** A standardized UI management system where each screen is an object, ensuring consistency and extensibility.
-   **Persistent Player Data:** Player names and scores are automatically saved and loaded, with exception handling for corrupted files.
-   **Blackjack:** A fully playable Blackjack game with betting, hitting, and standing mechanics.
-   **UNO Logic:** The complete game logic for UNO is implemented, ready for a graphical interface to be built.
-   **Sound Effects & Music:** Background music and UI sound effects for a more immersive experience.

---

## Architectural Pattern: Model-View-Controller (MVC)

This project was refactored to follow the MVC pattern, promoting a clean separation of concerns and making the codebase more modular and scalable.

-   **Model:** (`src/games/`, `src/classes/`)
    -   Contains the "brains" of the application. It manages the rules, state, and logic of the games (e.g., `BlackjackGame`). It is completely independent of the user interface.

-   **View:** (`src/interface.py`)
    -   Responsible for all things visual. It renders the user interface, the game board, and the cards based on the data provided by the Model. It contains no game logic. It captures user input and informs the Controller.

-   **Controller:** (`src/main_game.py`)
    -   Acts as the orchestrator. It initializes the game, listens for returns from the Views to decide which screen to display next, instantiates the Models, and injects them into the Views when a game starts.

---

## Project Structure

POOgame-UFGD-Rizzi/
│
├── main.py             # Main entry point for the game
└── src/
├── main_game.py    # The Controller: manages game flow and screens
├── interface.py    # The Views: contains all UI screen classes
├── setup.py        # Global constants (colors, screen size, fonts)
├── database_manager.py # Handles saving and loading player data
│
├── games/
│   ├── blackjack.py  # Blackjack game logic (Model)
│   └── uno.py        # UNO game logic (Model)
│
├── classes/
│   ├── deck.py       # Abstract classes for Deck, Hand, Player
│   ├── standard.py   # Classes for a standard 52-card deck
│   └── uno.py        # Classes specific to the game of UNO
│
├── img/              # Game assets (images, icons, cards)
├── sounds/           # Game audio (music, sound effects)
└── fonts/            # Font files

---

## How to Run

1.  **Prerequisites:**
    -   Python 3.x
    -   Pygame library (`pip install pygame`)

2.  **Execution:**
    -   Navigate to the root directory of the project (`POOgame-UFGD-Rizzi/`) and run:
        ```bash
        python main.py
        ```

---

## Gameplay Controls

-   **Arrow Keys (Up/Down):** Navigate through menu options.
-   **Z / Enter:** Confirm a selection in the menu.
-   **Blackjack - Hit:** Press `Z` or `H`.
-   **Blackjack - Stand:** Press `X` or `S`.

---

## Future Improvements

-   [ ] Implement the graphical user interface for the UNO game.
-   [ ] Create a "Config" screen to allow users to adjust audio volume.
-   [ ] Add more casino games (e.g., Poker).

---

## Authors

Developed with dedication by:
- **[Eduardo Rizzi]**
- **[Leandro Peres Sobreira]**
- **[Marcos Henrique Almeida Lima]**
- **[Abner Lucas Pereira Cardoso Vera]**