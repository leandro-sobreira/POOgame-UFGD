# UFGD Card Game Hub

![Gameplay GIF of the Main Menu](https://i.imgur.com/your-menu-gif-url.gif) A suite of classic card games developed in Pygame as a final project for an Object-Oriented Programming course. This project showcases key OOP principles through a Model-View-Controller (MVC) architecture and features a robust, object-oriented data persistence system.

---

## ✨ Features

-   **Two Complete Games:**
    -   **Blackjack:** Play against the house with a betting system in a faithful implementation of the classic game of 21.
    -   **UNO:** A full UNO match against three computer-controlled opponents, featuring all the special cards and rules.
-   **Object-Oriented Design:** The entire project is built on OOP principles, with classes for game logic, UI elements, and data models.
-   **MVC Architecture:** A clean separation between game logic (Model), the graphical interface (View), and application flow (Controller) makes the codebase modular and scalable.
-   **Robust Data Persistence:**
    -   Game wins are saved to `gamedata.dat` using a class-based repository pattern.
    -   The system includes automatic data migration to handle legacy data formats, ensuring stability.
-   **Dynamic Leaderboard:** A scores screen allows filtering victories by game and sorts them from highest to lowest score.
-   **Immersive UI:** Features navigable menus, background music, and sound effects for an engaging player experience.

---

## 🏗️ Architectural Pattern: MVC

The project strictly follows the Model-View-Controller pattern to promote a clean separation of concerns.

-   **Model:** (`src/games/`, `src/classes/`)
    -   Contains the "brains" of the application. It manages the rules, state, and logic of each game (`BlackjackGame`, `UnoGame`). It is completely independent of the user interface.

-   **View:** (`src/interface.py`)
    -   Responsible for all things visual. It renders the user interface, the game board, and cards based on data from the Model. It captures user input and informs the Controller of the user's intentions.

-   **Controller:** (`src/main_game.py`)
    -   Acts as the orchestrator. It initializes the game, decides which screen to display, instantiates the Models, and injects data into the Views. It also coordinates with the `ScoreRepository` for data persistence.

---

## 🚀 How to Run

1.  **Prerequisites:**
    -   Python 3.x
    -   Pygame library (`pip install pygame`)

2.  **Execution:**
    -   Navigate to the project's root directory (`POOgame-UFGD/project/`) and run:
        ```bash
        python main.py
        ```

---

## 🎮 Controls

-   **Arrow Keys:** Navigate through menus and in-game options.
-   **Z / Enter:** Confirm a selection.
-   **X / Escape:** Go back or exit a submenu/screen.

#### **Blackjack**
-   **Hit:** Press `Z` or `H`.
-   **Stand:** Press `X` or `S`.

#### **UNO**
-   **Navigate Cards:** Use the arrow keys.
-   **Play/Draw Card:** Press `Z` or `Enter` to confirm your selection.

---

## 📚 Documentation

For detailed information about the project's classes and methods, you can build and view the Sphinx documentation located in the `docs/` directory.

1.  Install Sphinx and the theme:
    ```bash
    pip install sphinx sphinx_rtd_theme
    ```
2.  Navigate to the `docs/` directory and build the HTML:
    ```bash
    make html
    ```
3.  Open `docs/_build/html/index.html` in your web browser.

---

## 🧑‍💻 Authors

This project was developed with dedication by:
-   **Abner Lucas Pereira Cardoso Vera**
-   **Eduardo Rodrigues Rizzi**
-   **Leandro Peres Sobreira**
-   **Marcos Henrique Almeida Lima**