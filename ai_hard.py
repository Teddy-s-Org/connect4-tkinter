import copy
import math

def get_hard_move(board, rows, cols, player, depth=4):
    _, best_col = minimax(board, depth, -math.inf, math.inf, True, player, rows, cols)
    return best_col

def minimax(board, depth, alpha, beta, maximizing_player, player, rows, cols):
    opponent = 'R' if player == 'Y' else 'Y'
    valid_cols = [c for c in range(cols) if 'X' in board[c]]

    is_terminal = is_terminal_node(board, rows, cols)
    if depth == 0 or is_terminal:
        if is_terminal:
            if winning_player(board, player, rows, cols):
                return (1000000, None)
            elif winning_player(board, opponent, rows, cols):
                return (-1000000, None)
            else:
                return (0, None)  # Draw
        else:
            return (score_board(board, player, rows, cols), None)

    if maximizing_player:
        value = -math.inf
        best_col = None
        for col in valid_cols:
            temp_board = copy.deepcopy(board)
            row = get_drop_row(temp_board[col], rows)
            temp_board[col][row] = player
            new_score, _ = minimax(temp_board, depth - 1, alpha, beta, False, player, rows, cols)
            if new_score > value:
                value = new_score
                best_col = col
            alpha = max(alpha, value)
            if alpha >= beta:
                break
        return value, best_col
    else:
        value = math.inf
        best_col = None
        for col in valid_cols:
            temp_board = copy.deepcopy(board)
            row = get_drop_row(temp_board[col], rows)
            temp_board[col][row] = opponent
            new_score, _ = minimax(temp_board, depth - 1, alpha, beta, True, player, rows, cols)
            if new_score < value:
                value = new_score
                best_col = col
            beta = min(beta, value)
            if alpha >= beta:
                break
        return value, best_col

def get_drop_row(column, rows):
    for i in range(rows):
        if column[i] == 'X':
            return i
    return None

def is_terminal_node(board, rows, cols):
    return all('X' not in board[c] for c in range(cols)) or \
           winning_player(board, 'R', rows, cols) or \
           winning_player(board, 'Y', rows, cols)

def winning_player(board, piece, rows, cols):
    for col in range(cols):
        for row in range(rows):
            if board[col][row] == piece:
                if check_win(board, col, row, piece, rows, cols):
                    return True
    return False

def score_board(board, player, rows, cols):
    # Use the same scoring logic as medium AI
    for col in range(cols):
        for row in range(rows):
            if board[col][row] == player:
                return score_position(board, col, row, player, rows, cols)
    return 0

def score_position(board, col, row, player, rows, cols):
    center_col = cols // 2
    score = 0

    opponent = 'R' if player == 'Y' else 'Y'

    # --- Winning move
    if check_win(board, col, row, player, rows, cols):
        return 10000  # highest possible score

    # --- Blocking move
    board[col][row] = opponent
    if check_win(board, col, row, opponent, rows, cols):
        score += 300  # increased from 200
    board[col][row] = player

    # --- Center bias
    score += max(0, 1 - abs(center_col - col))  # max +1

    # --- Line-building: 2s and 3s
    directions = [(1, 0), (0, 1), (1, 1), (1, -1)]
    forks = 0  # count possible forks
    for dx, dy in directions:
        count = 1
        count += count_aligned_pieces(board, col, row, dx, dy, player, rows, cols)
        count += count_aligned_pieces(board, col, row, -dx, -dy, player, rows, cols)

        if count == 2:
            score += 30
        elif count == 3:
            score += 150
            forks += 1

    # --- Reward creating a fork (multiple 3-in-a-rows)
    if forks >= 2:
        score += 400

    # --- Trap detection: avoid letting opponent create a fork
    for test_col in range(cols):
        if 'X' not in board[test_col]:
            continue
        temp_board = copy.deepcopy(board)
        test_row = get_drop_row(temp_board[test_col], rows)
        if test_row is None:
            continue
        temp_board[test_col][test_row] = opponent

        # Count how many winning directions this creates for opponent
        threats = 0
        for dx, dy in directions:
            cnt = 1
            cnt += count_aligned_pieces(temp_board, test_col, test_row, dx, dy, opponent, rows, cols)
            cnt += count_aligned_pieces(temp_board, test_col, test_row, -dx, -dy, opponent, rows, cols)
            if cnt >= 3:
                threats += 1

        if threats >= 2:
            score -= 500  # avoid letting opponent fork

    return score

def count_aligned_pieces(board, col, row, dx, dy, piece, rows, cols):
    count = 0
    cx, cy = col + dx, row + dy
    while 0 <= cx < cols and 0 <= cy < rows:
        if board[cx][cy] == piece:
            count += 1
            cx += dx
            cy += dy
        else:
            break
    return count


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
