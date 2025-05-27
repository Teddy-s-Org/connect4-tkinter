# Connect 4 (Python)

![Game Screenshot](7x6_board.png)

I saw this video online and wanted to create the simple, pretty UI with my own contribution. Not sure whose application he is running, but I am to lazy to look. I also made a CLI version of the game before creating the pretty version to explore the main 'win checking' algorithm. Overall a fun project.

-Update: Didn't realize it was supposed to be a 7x6 board. It is now updated, but this is easily changable. Thank goodness for global variables.

link: https://youtu.be/iIF0Ha-1h6c?si=ugrcV8njugyENPUQ

## Running the game (easy):
In order to run the application, it is straight-forward. Just make sure you have Python, and also make sure you have the 'tkinter' library. 

### Run the GUI version:
```
python3 connect4_gui.py
```

### Run the CLI version:
```
python3 connect4_cli.py
```

## Algorithm Description:
The win-checking algorithm operates by evaluating the most recent move made by a player, rather than scanning the entire board. From that single position, it checks in four directions: horizontal, vertical, and both diagonals, counting consecutive matching pieces in both directions along each line. If the total count reaches four, it confirms a win.

By focusing only on the most recent move, the algorithm avoids unnecessary computation and reduces the number of positions it needs to evaluate. This makes it highly efficient for small, fixed-size grids like Connect 4. On a 6x7 board, each direction involves at most six checks (three in each direction), leading to a worst-case time complexity of O(1) - constant time relative to board size. Memory usage is minimal and remains O(1) since no additional data structures are created beyond local counters. This makes the approach both fast and memory-efficient for real-time gameplay.

## 7x7 board:

![Game Screenshot](C4_gameplay.png)