import tkinter as tk
from collections import deque
import random
import argparse
import sys
from ai_medium import get_best_move
from ai_easy import get_easy_move

CELL_SIZE = 80
ROWS, COLS = 6, 7
PADDING_X = 50
PADDING_Y = 30

class Connect4GUI:
    def __init__(self, root, mode="2p"):
        self.root = root
        self.root.title("Connect 4")
        self.mode = mode

        self.canvas = tk.Canvas(
            root,
            width=COLS * CELL_SIZE + PADDING_X * 2,
            height=ROWS * CELL_SIZE + PADDING_Y * 2,
            bg="#3a3aa4"
        )

        self.canvas.pack()

        self.board = [deque(['X'] * ROWS) for _ in range(COLS)]
        self.turns = 0
        self.game_over = False
        self.hover_col = None

        self.win_message = None  # Store final result message

        self.canvas.bind("<Button-1>", self.handle_click)
        self.canvas.bind("<Motion>", self.track_mouse)
        self.draw_board()

    def ai_move(self):
        if self.mode == "easy":
            self.ai_easy()
        elif self.mode == "medium":
            col = get_best_move(self.board, ROWS, COLS, 'Y')
            if col is not None:
                self.drop_piece('Y', col)
        elif self.mode == "hard":
            from ai_hard import get_hard_move
            col = get_hard_move(self.board, ROWS, COLS, 'Y', depth=4)
            if col is not None:
                self.drop_piece('Y', col)


    def ai_easy(self):
        col = get_easy_move(self.board, ROWS, COLS, ai_color='Y', human_color='R')
        if col is not None:
            self.drop_piece('Y', col)


    def track_mouse(self, event):
        if self.game_over:
            self.hover_col = None
            self.draw_board()
            return

        col = (event.x - PADDING_X) // CELL_SIZE 
        if col < 0 or col >= COLS:
            self.hover_col = None
        else:
            self.hover_col = col
        self.draw_board()

    def draw_board(self):
        
        self.canvas.delete("all")

        # Simulated rounded background
        corner_radius = 30  
        left = PADDING_X - 10
        top = PADDING_Y - 10
        right = COLS * CELL_SIZE + PADDING_X + 10
        bottom = ROWS * CELL_SIZE + PADDING_Y + 10

        # Draw four corner circles
        self.canvas.create_oval(left, top, left + 2*corner_radius, top + 2*corner_radius,
                                fill="#001f3f", outline="")
        self.canvas.create_oval(right - 2*corner_radius, top, right, top + 2*corner_radius,
                                fill="#001f3f", outline="")
        self.canvas.create_oval(left, bottom - 2*corner_radius, left + 2*corner_radius, bottom,
                                fill="#001f3f", outline="")
        self.canvas.create_oval(right - 2*corner_radius, bottom - 2*corner_radius, right, bottom,
                                fill="#001f3f", outline="")

        # Draw side rectangles to connect the corners
        self.canvas.create_rectangle(left + corner_radius, top,
                                    right - corner_radius, bottom,
                                    fill="#001f3f", outline="")
        self.canvas.create_rectangle(left, top + corner_radius,
                                    right, bottom - corner_radius,
                                    fill="#001f3f", outline="")
        # Draw hover column effect (single pill-shaped overlay)
        if self.hover_col is not None and not self.game_over:
            self.draw_pill_overlay(self.hover_col, color="#252593")

        # Draw all cells
        for row in range(ROWS):
            for col in range(COLS):
                piece = self.board[col][ROWS - 1 - row]  # flip vertically
                if piece == 'X':
                    color = "#252593"  # darker blue for empty
                elif piece == 'R':
                    color = "#f23a3a"
                elif piece == 'Y':
                    color = "#dbda36"

                x = col * CELL_SIZE + PADDING_X
                y = row * CELL_SIZE + PADDING_Y
                self.canvas.create_oval(
                    x + 10, y + 10, x + CELL_SIZE - 10, y + CELL_SIZE - 10,
                    fill=color, outline=""
                )

        # If there's a win or draw message, display it
        if self.win_message:
            center_x = PADDING_X + (COLS * CELL_SIZE) // 2
            center_y = PADDING_Y + (ROWS * CELL_SIZE) // 2

            self.canvas.create_text(
                center_x, center_y,
                text=self.win_message, fill="white", font=('Arial', 32, 'bold')
            )
            self.canvas.create_text(
                center_x, center_y + 40,
                text="Click anywhere to restart", fill="white", font=('Arial', 16)
            )

    def handle_click(self, event):
        if self.game_over:
            self.reset_game()
            return

        col = (event.x - PADDING_X) // CELL_SIZE  
        if col < 0 or col >= COLS:
            return  # ignore invalid clicks

        if 'X' in self.board[col]:
            if self.mode == "2p":
                player = 'R' if self.turns % 2 == 0 else 'Y'
            else:
                player = 'R'  # Human is always Red vs. AI
            row = self.drop_piece(player, col)
            self.draw_board()

            if row is not None and self.check_win(col, row):
                self.win_message = "Red Wins!"
                self.game_over = True
                self.draw_board()
                return

            elif self.turns == ROWS * COLS - 1:
                self.win_message = "Cat's Game"
                self.game_over = True
                self.draw_board()
                return

            self.turns += 1

            # 🟡 Only trigger AI if not in 2-player mode
            if self.mode != "2p" and not self.game_over:
                self.ai_move()
                self.draw_board()

                # Check if AI won
                for c in range(COLS):
                    for r in range(ROWS):
                        if self.board[c][r] == 'Y':
                            if self.check_win(c, r):
                                self.win_message = "Yellow Wins!"
                                self.game_over = True
                                self.draw_board()
                                return

                self.turns += 1


    def drop_piece(self, player, col):
        for i in range(ROWS):
            if self.board[col][i] == 'X':
                self.board[col][i] = player
                return i  # Return the row where the piece was placed
        return None


    def check_win(self, col_index, row_index):
        player_piece = self.board[col_index][row_index]

        def count_matches(x, y, dx, dy):
            count = 0
            cx, cy = x + dx, y + dy
            while 0 <= cx < COLS and 0 <= cy < ROWS:
                if self.board[cx][cy] == player_piece:
                    count += 1
                    cx += dx
                    cy += dy
                else:
                    break
            return count

        directions = [(1, 0), (0, 1), (1, 1), (1, -1)]
        for dx, dy in directions:
            total = 1
            total += count_matches(col_index, row_index, dx, dy)
            total += count_matches(col_index, row_index, -dx, -dy)
            if total >= 4:
                return True
        return False


    def reset_game(self):
        self.board = [deque(['X'] * ROWS) for _ in range(COLS)]
        self.turns = 0
        self.game_over = False
        self.hover_col = None
        self.win_message = None
        self.draw_board()

    def draw_pill_overlay(self, col, color="#252593"):
        x = col * CELL_SIZE + PADDING_X
        y_top = PADDING_Y
        y_bottom = ROWS * CELL_SIZE + PADDING_Y


        # Smaller margin = slightly larger pill than slot
        margin = 6  # default is 10, reduce to expand the pill
        diameter = CELL_SIZE - 2 * margin
        radius = diameter // 2

        left = x + margin
        right = x + CELL_SIZE - margin

        # Top full circle
        self.canvas.create_oval(
            left, y_top,
            right, y_top + diameter,
            fill=color, outline="", width=0
        )

        # Bottom full circle
        self.canvas.create_oval(
            left, y_bottom - diameter,
            right, y_bottom,
            fill=color, outline="", width=0
        )

        # Middle rectangle (connect the two circles)
        self.canvas.create_rectangle(
            left, y_top + radius,
            right, y_bottom - radius,
            fill=color, outline="", width=0
        )


def parse_args():
    parser = argparse.ArgumentParser(description="Play Connect 4 with different difficulty levels.")
    parser.add_argument("mode", choices=["2p", "easy", "medium", "hard"],
                        help="Game mode: '2p' for two players, or 'easy', 'medium', 'hard' for AI difficulty.")
    return parser.parse_args()

if __name__ == "__main__":
    args = parse_args()
    root = tk.Tk()
    app = Connect4GUI(root, mode=args.mode)
    root.mainloop()
