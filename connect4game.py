import random, sys

players = {1: "+", -1: "x"}
funcs = {1: max, -1: min}


mm = [0,  0,  0,  0,  0,  0,  0,  0,  0,
      0,  0, 10, 20, 30, 20, 10,  0,  0,
      0, 10, 20, 30, 40, 30, 20, 10,  0,
      0, 20, 30, 40, 50, 40, 30, 20,  0,
      0, 20, 30, 40, 50, 40, 30, 20,  0,
      0, 10, 20, 30, 40, 30, 20, 10,  0,
      0,  0, 10, 20, 30, 20, 10,  0,  0,
      0,  0,  0,  0,  0,  0,  0,  0,  0]


def pretty_board(board):
    print(board[10:17]+"\n"+board[19:26]+"\n"+board[28:35]+"\n"+board[37:44]+"\n"+board[46:53]+"\n"+board[55:62]+"\n")


def start_board():
    return "?"*8 + "??......."*6 + "?"*10


def get_valid_moves(board):
    cols = []
    for c in range(10, 17):
        if board[c] == ".":
            cols.append(c)
    return cols


def make_move(board, player, col):
    index = col
    while board[index+9] == ".":
        index += 9
    return board[:index] + players[player] + board[index+1:], index


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


def minimax(board, player, depth):
    cols = get_valid_moves(board)
    if len(cols) == 0:
        return 0, -5, -5
    if depth == 0:
        score = 0
        for m in range(11, 61):
            if board[m] == "+":
                score += mm[m]
            elif board[m] == "x":
                score -= mm[m]
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


def game(opponent):
    board = start_board()
    print("1234567")
    pretty_board(board)
    print()
    while True:
        if len(get_valid_moves(board)) == 0:
            print("No winner!")
            break
        if opponent == "RANDOM":            # RANDOMGAME
            col = random.choice(get_valid_moves(board))
            board, index = make_move(board, 1, col)
            print("Random chose column", index % 9)
            print("1234567")
            pretty_board(board)
            print()
            if goal_test(board, 1, index):
                print("Random Wins!")
                break

        elif opponent == "PLAYER":          # PLAYERGAME
            col = int(input("Which column (1 - 7)? "))
            board, index = make_move(board, 1, col)
            print("You chose column", index % 9)
            print("1234567")
            pretty_board(board)
            print()
            if goal_test(board, 1, index):
                print("You Win!")
                break

        v, index, board = minimax(board, -1, 5)     # AI
        print("AI chose column", index % 9)
        print("1234567")
        pretty_board(board)
        print()
        if goal_test(board, -1, index):
            print("AI Wins!")
            break


if __name__ == "__main__":
    game(sys.argv[1])
