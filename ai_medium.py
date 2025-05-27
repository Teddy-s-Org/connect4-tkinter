import copy
import random


def is_known_fork_trap(board, rows, cols):
    try:
        # LEFT TRAP (columns 3, 4, 5, 6)
        if (
            board[3][0] == 'R' and  # Red in col 4
            board[3][1] == 'Y' and
            board[3][2] == 'Y' and
            board[4][0] == 'R' and  # Red in col 5
            board[5][0] == 'R' and  # Red in col 6
            board[2][0] == 'Y'      # Yellow just played col 3
        ):
            return 3  # col to avoid

        # RIGHT TRAP (columns 0,1,2,3) — mirror of above
        if (
            board[3][0] == 'R' and
            board[3][1] == 'Y' and
            board[3][2] == 'Y' and
            board[2][0] == 'R' and
            board[1][0] == 'R' and
            board[4][0] == 'Y'
        ):
            return 4  # col to avoid

    except IndexError:
        pass

    return None


def get_best_move(board, rows, cols, current_player):
    opponent = 'R' if current_player == 'Y' else 'Y'
    best_score = float('-inf')
    best_cols = []

    for col in range(cols):
        if 'X' not in board[col]:
            continue

        # Simulate AI move
        temp_board = copy.deepcopy(board)
        row = get_drop_row(temp_board[col], rows)
        temp_board[col][row] = current_player

        # Defensive 2-ply: check how many wins opponent gets next turn
        winning_responses = 0
        for opp_col in range(cols):
            if 'X' not in temp_board[opp_col]:
                continue
            opp_board = copy.deepcopy(temp_board)
            opp_row = get_drop_row(opp_board[opp_col], rows)
            if opp_row is None:
                continue
            opp_board[opp_col][opp_row] = opponent
            if check_win(opp_board, opp_col, opp_row, opponent, rows, cols):
                winning_responses += 1

        # If opponent gets 2 or more winning options, this move is unsafe
        if winning_responses >= 2:
            score = -9999
        else:
            score = score_position(temp_board, col, row, current_player, rows, cols)

        # Special trap avoidance: hardcoded pattern
        trap_col = is_known_fork_trap(temp_board, rows, cols)
        if trap_col is not None and col == trap_col:
            #print(f"[Medium AI] Avoiding known fork trap in column {trap_col}")
            score = -99999


        if score > best_score:
            best_score = score
            best_cols = [col]
        elif score == best_score:
            best_cols.append(col)

    # Prefer closer-to-center column if multiple best moves
    if best_cols:
        return sorted(best_cols, key=lambda c: abs(c - cols // 2))[0]
    else:
        return None

def get_drop_row(column, rows):
    for i in range(rows):
        if column[i] == 'X':
            return i
    return None

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

