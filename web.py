from flask import Flask, request, render_template_string, redirect, url_for
from collections import deque

app = Flask(__name__)

# Session state (simplified — no multi-user support)
board = [deque(['X'] * 7) for _ in range(7)]
num_turns = 0
output = []
game_over = False

# Dev test: update CI pipeline, adding to GHA

TEMPLATE = """
<!DOCTYPE html>
<html>
<head><title>Connect 4 Main</title></head>
<body>
<pre>{{output}}</pre>
{% if not game_over %}
<form method="POST">
    <label for="move">Enter a column (1-7):</label><br>
    <input type="text" id="move" name="move">
    <input type="submit" value="Play">
</form>
{% else %}
<p><strong>Game Over!</strong></p>
{% endif %}
</body>
</html>
"""

def render_board(b):
    lines = []
    for row in reversed(range(7)):
        line = ''
        for col in range(7):
            line += b[col][row] + ' '
        lines.append(line)
    return "\n".join(lines)

def compute_turn(color, b, col):
    for i in range(7):
        if b[col][i] == 'X':
            b[col][i] = color
            break
    return b

def check_win(b, turn):
    col = b[turn]
    for row_index in range(7):
        if col[row_index] != 'X':
            player_piece = col[row_index]
            break
    else:
        return False

    def count_matches(x, y, dx, dy):
        count = 0
        cx, cy = x + dx, y + dy
        while 0 <= cx < 7 and 0 <= cy < 7:
            if b[cx][cy] == player_piece:
                count += 1
                cx += dx
                cy += dy
            else:
                break
        return count

    directions = [(1, 0), (0, 1), (1, 1), (1, -1)]
    for dx, dy in directions:
        total = 1
        total += count_matches(turn, row_index, dx, dy)
        total += count_matches(turn, row_index, -dx, -dy)
        if total >= 4:
            return True
    return False

@app.route("/", methods=["GET", "POST"])
def game():
    global num_turns, output, board, game_over

    if request.method == "POST":
        if not game_over:
            move = request.form["move"]
            if move.isnumeric() and 1 <= int(move) <= 7 and 'X' in board[int(move)-1]:
                col = int(move) - 1
                color = 'Y' if num_turns % 2 else 'R'
                board = compute_turn(color, board, col)
                output.append(render_board(board))
                output.append(f"{'Yellow' if color == 'Y' else 'Red'} played column {col+1}")
                if check_win(board, col):
                    output.append(f"{'Yellow' if color == 'Y' else 'Red'} Wins!")
                    game_over = True
                num_turns += 1
            else:
                output.append("Invalid input. Please enter a valid column (1-7).")

    return render_template_string(
        TEMPLATE,
        output="\n".join(output),
        game_over=game_over
    )

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
