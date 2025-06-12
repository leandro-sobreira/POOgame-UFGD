# UFGD Online Casino

![Gameplay GIF](Apresentation1.gif)

A suite of casino-style card games developed as a final project for an Object-Oriented Programming course at UFGD. The project showcases core OOP principles, architectural patterns like Model-View-Controller, and game development with Pygame.

---

## Features

- **Standardized UI:** A robust screen management system ensures a consistent user experience.
- **Persistent Player Data:** Player names and scores are automatically saved and loaded.
- **Blackjack:** A fully playable Blackjack game with betting, hitting, and standing mechanics.
- **UNO:** The complete game logic for UNO is implemented (UI pending).
- **Sound Effects & Music:** Background music and UI sound effects for an immersive experience.

---

## Architectural Pattern: Model-View-Controller (MVC)

This project was refactored to follow a design pattern similar to MVC, promoting a clean separation of concerns and making the codebase more modular and scalable.

-   **Model:** (`src/games/`, `src/classes/`)
    -   Contains the "brains" of the application. It manages the rules, state, and logic of the games (e.g., `BlackjackGame`). It is completely independent of the user interface.

-   **View:** (`src/interface.py`)
    -   Responsible for all things visual. It renders the user interface, the game board, and the cards based on the data provided by the Model. It does not contain any game logic.

-   **Controller:** (`src/main_game.py`)
    -   Acts as the orchestrator. It listens for user input (keyboard presses), tells the Model to update its state accordingly, and instructs the View on which screen to display.

---

## Project Structure

```
POOgame-UFGD/
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
```

---

## How to Run

1.  **Prerequisites:**
    -   Python 3.x
    -   Pygame library (`pip install pygame`)

2.  **Execution:**
    -   Navigate to the root directory of the project and run:
        ```bash
        python main.py
        ```

---

## Gameplay Controls

-   **Arrow Keys (Up/Down):** Navigate through menu options.
-   **Z / Enter:** Confirm a selection or action (e.g., Hit in Blackjack).
-   **X:** Secondary action (e.g., Stand in Blackjack).

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