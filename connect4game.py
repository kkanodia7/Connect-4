# Created by Kushal Kanodia on Feb 2, 2019

import random
import sys

players = {1: "+", -1: "x"}     # One player is +, other is x
funcs = {1: max, -1: min}

# Board spaces' weights for AI
move_matrix = [0,  0,  0,  0,  0,  0,  0,  0,  0,
               0,  0, 10, 20, 30, 20, 10,  0,  0,
               0, 10, 20, 30, 40, 30, 20, 10,  0,
               0, 20, 30, 40, 50, 40, 30, 20,  0,
               0, 20, 30, 40, 50, 40, 30, 20,  0,
               0, 10, 20, 30, 40, 30, 20, 10,  0,
               0,  0, 10, 20, 30, 20, 10,  0,  0,
               0,  0,  0,  0,  0,  0,  0,  0,  0]


# Prints the board in nice square format
def pretty_board(board):
    print(board[10:17]+"\n"+board[19:26]+"\n"+board[28:35]+"\n"+board[37:44]+"\n"+board[46:53]+"\n"+board[55:62]+"\n")


# Returns the empty starting board
def start_board():
    return "?"*8 + "??......."*6 + "?"*10


# Returns all possible moves (all columns that are not filled)
def get_valid_moves(board):
    cols = []
    for c in range(10, 17):
        if board[c] == ".":
            cols.append(c)
    return cols


# Places given player's token in given column, returns new board
def make_move(board, player, col):
    index = col
    while board[index+9] == ".":
        index += 9
    return board[:index] + players[player] + board[index+1:], index


# Returns True if a given player's move in a given space resulted in a victory for that player
def goal_test(board, player, index):
    dirs = [1, 8, 9, 10]
    for nd in dirs:
        d = nd
        temp = index
        line = 1
        for i in range(5):
            temp += d
            line += 1
            if board[temp] != players[player]:
                line -= 1
                if d > 0:
                    d *= -1
                    temp = index
                else:
                    break
        if line >= 4:
            return True
    return False


# Uses MiniMax algorithm based on weight matrix, to pre-set depth, to determine best possible move for AI
def minimax(board, player, depth):
    cols = get_valid_moves(board)
    if len(cols) == 0:
        return 0, -5, -5
    if depth == 0:
        score = 0
        for m in range(11, 61):
            if board[m] == "+":
                score += move_matrix[m]
            elif board[m] == "x":
                score -= move_matrix[m]
        return score, -5, -5
    moves = []
    for c in cols:
        nm, index = make_move(board, player, c)
        if goal_test(nm, player, index):
            moves.append((100000 * player, index, nm))
        else:
            count = minimax(nm, -player, depth-1)[0]
            moves.append((count, index, nm))

    return funcs[player](moves)


# Takes in either RANDOM or PLAYER and plays it against AI
def game(opponent):
    board = start_board()
    print("1234567")
    pretty_board(board)
    print()
    while True:
        if len(get_valid_moves(board)) == 0:
            print("No winner!")
            break
        if opponent == "RANDOM":    # Random vs. AI
            col = random.choice(get_valid_moves(board))
            board, index = make_move(board, 1, col)
            print("Random chose column", index % 9)
            print("1234567")
            pretty_board(board)
            print()
            if goal_test(board, 1, index):
                print("Random Wins!")
                break

        elif opponent == "PLAYER":  # Player vs. AI
            col = int(input("Which column (1 - 7)? "))
            board, index = make_move(board, 1, col)
            print("You chose column", index % 9)
            print("1234567")
            pretty_board(board)
            print()
            if goal_test(board, 1, index):
                print("You Win!")
                break

        v, index, board = minimax(board, -1, 5)     # AI depth set at 5
        print("AI chose column", index % 9)
        print("1234567")
        pretty_board(board)
        print()
        if goal_test(board, -1, index):
            print("AI Wins!")
            break


if __name__ == "__main__":
    game(sys.argv[1])


# Potential Future Improvements:
#   - Select depth (difficulty) of AI before starting a game
#   - Take input of random / player while running, rather than from the command line
#   - Make pretty-board potentially look nicer by adding spaces between each column
#   - AB-pruning and other such optimizations to increase speed of AI
#   - Improve weight matrix to make AI smarter
#   - More heuristics for AI, besides just win-condition and weight matrix
#   - Ability to play AI against AI, setting separate difficulties for both
#   - Select board size before a game, rather than a fixed 7x6 board
