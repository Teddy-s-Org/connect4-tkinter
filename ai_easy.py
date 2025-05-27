import random
import copy

def get_easy_move(board, rows, cols, ai_color='Y', human_color='R'):
    for col in range(cols):
        if 'X' in board[col]:
            row = simulate(board, col, ai_color, rows)
            if row is not None and check_win(board, col, row, ai_color, rows, cols):
                return col

    for col in range(cols):
        if 'X' in board[col]:
            row = simulate(board, col, human_color, rows)
            if row is not None and check_win(board, col, row, human_color, rows, cols):
                return col

    valid = [c for c in range(cols) if 'X' in board[c]]
    return random.choice(valid) if valid else None

def simulate(board, col, color, rows):
    for i in range(rows):
        if board[col][i] == 'X':
            board[col][i] = color
            row = i
            break
    else:
        return None

    win = check_win(board, col, row, color, rows, len(board))
    board[col][row] = 'X'
    return row if win else None

def check_win(board, col_index, row_index, piece, rows, cols):
    directions = [(1, 0), (0, 1), (1, 1), (1, -1)]

    def count_matches(dx, dy):
        count = 0
        cx, cy = col_index + dx, row_index + dy
        while 0 <= cx < cols and 0 <= cy < rows and board[cx][cy] == piece:
            count += 1
            cx += dx
            cy += dy
        return count

    for dx, dy in directions:
        total = 1
        total += count_matches(dx, dy)
        total += count_matches(-dx, -dy)
        if total >= 4:
            return True
    return False
