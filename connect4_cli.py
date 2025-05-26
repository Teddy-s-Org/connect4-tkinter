'''This is going to be a connect 4 game in 
python that has a simple UI.
'''
from collections import deque

def createBoard(numTurns):
    board = [deque(['X'] * 7) for _ in range(7)]
    gameState = True #Gamestate = true if game is still going, false if game is over
    turnBased(gameState, numTurns, board)

def printBoard(gameBoard):
    for row in reversed(range(7)):
        for col in range(7):
            print(gameBoard[col][row], end=' ')
        print()

def computeTurn(color, board, col):
    for i in range(7):
        if board[col][i] == 'X':
            board[col][i] = color
            break
    return board

def checkWin(board, turn):
    col = board[turn]
    for row_index in range(7):
        if col[row_index] != 'X':
            player_piece = col[row_index]
            break
    else:
        return False

    def count_matches(x, y, dx, dy):
        count = 0
        cx, cy = x + dx, y+dy
        while 0 <= cx < 7 and 0 <= cy < 7:
            if board[cx][cy] == player_piece:
                count += 1
                cx += dx
                cy += dy
            else:
                break
        return count

    directions = [(1,0), (0,1), (1,1), (1,-1)]
    for dx, dy in directions:
        total = 1
        total += count_matches(turn, row_index, dx, dy)
        total += count_matches(turn, row_index, -dx, -dy)

        if total >= 4:
            return True
    return False



def turnBased(gameState, numTurns, board):
    while gameState: #game is still playable
        if numTurns == 49:
            printBoard(board)
            print("Cats Game. No one wins.")
            gameState = False
        elif numTurns % 2 == 1: #yellows turn
            printBoard(board)
            print("Yellow. It is your turn. Where would you like to play?")
            print("Enter a valid column (1-7)")
            validInput = False
            while not validInput:
                turn = input()
                if turn.isnumeric() and int(turn) >= 1 and int(turn) <= 7 and 'X' in board[int(turn)-1]:
                    turn = int(turn)
                    validInput = True
                else:
                    print("Enter a valid column (1-7)")        
            board = computeTurn('Y', board, turn-1)
            if checkWin(board, turn-1):
                print("Yellow Wins!")
                gameState = False
        else: #reds turn, red also goes first
            printBoard(board)
            print("Red. It is your turn. Where would you like to play?")
            print("Enter a valid column (1-7)")
            validInput = False
            while not validInput:
                turn = input()
                if turn.isnumeric() and int(turn) >= 1 and int(turn) <= 7 and 'X' in board[int(turn)-1]:
                    turn = int(turn)
                    validInput = True
                else:
                    print("Enter a valid column (1-7)")
            board = computeTurn('R', board, turn-1)
            if checkWin(board, turn-1):
                print("Red Wins!")
                gameState = False
        numTurns += 1
        

createBoard(numTurns = 0)