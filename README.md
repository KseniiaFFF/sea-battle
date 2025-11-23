🛳️ Sea Battle — Python Console Game

This is a fully implemented console version of the classic Battleship game written in Python.
The player places ships manually, the bot places ships automatically, and then the battle begins.

The game supports:
 • Manual ship placement
 • Automatic ship placement for the bot
 • Validation of ship placement rules
 • Saving and loading the game
 • Hit, miss, damage, and destruction mechanics
 • Console-based board rendering
 • Recording game results in stats.txt

======

📌 Features

✔ Complete Battleship logic:
 • Ships of sizes 1, 2, 3, and 4
 • Ships cannot touch each other
 • Placement validation
 • Shooting logic with hit/miss checking
 • Determining when a ship is fully destroyed
 • Automatically marking destroyed ships

✔ Save system

The game saves:
 • Player field
 • Bot field
 • Ship lists
 • Damaged cells

Load the game anytime during ship placement by entering 777.

✔ Statistics

Each finished game is recorded in:
stats.txt

Format:
User won: <number of moves>
Bot won: <number of moves>

======

🎮 How to Play
 1. Install Python 3.10+
 2. Run the game:
    second_sea.py
 3. Place your ships manually:

 • Enter ship size (1–4)
 • Choose orientation (1 — horizontal, 2 — vertical)
 • Enter coordinates I and J (1–10)

 4. Enter 777 to load a saved game
 5. Enter 0 to save and exit

After ship placement, the battle begins automatically.   
