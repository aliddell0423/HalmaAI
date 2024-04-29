# Halma Game with wxPython GUI

Welcome to our implementation of Halma, a classic board game, with a wxPython graphical user interface (GUI). In this game, players can challenge themselves against an AI opponent.

## Game Description

Halma is a strategic board game for two players. The objective is to be the first to move all of your pieces from your corner of the board to the opposite corner, occupying the opponent's starting location. Players can move their pieces in any direction, including diagonally, and can also jump over their own and opponent's pieces to advance across the board.

## Features

- **Graphical User Interface**: The game features a user-friendly GUI built using wxPython, allowing players to interact with the game board easily.
- **Single Player Mode**: Players can enjoy the game against an AI opponent, which implements basic strategies to provide a challenging experience.
- **Customizable Settings**: Players can adjust game settings such as difficulty level, board size, and piece colors according to their preferences.
- **Undo and Redo**: The game supports undo and redo functionality, allowing players to retract and replay their moves.
- **Save and Load**: Players can save their game progress and load it later to resume playing from where they left off.

## Technologies Used

- **Python**: The game logic and AI algorithms are implemented in Python.
- **wxPython**: A cross-platform GUI toolkit for Python used to create the graphical interface.
- **Minimax Algorithm**: The AI opponent uses a basic Minimax algorithm with alpha-beta pruning to make strategic decisions.

## Installation and Usage

1. Clone the repository:

   ```bash
   git clone <repository-url>

   ```
   
2. Make sure wxPython is installed, then run:

   ``` bash
   $ python main.py
   ```

Gameplay Instructions

1. Use the mouse to select and move pieces on the game board.
2. You can jump over your own and opponent's pieces to move across the board.
3. The AI opponent will make its moves after you've made yours.
4. The game ends when one player successfully moves all their pieces to the opposite corner of the board.
