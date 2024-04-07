import sys
import random

boardsize = None
board = None
komi = 0
handicap = 0

def debug(str):
    sys.stderr.write(str)
    sys.stderr.write("\n")

def board_char(a):
    if a == 2:
        return "o"
    if a == 1:
        return "x"
    return "."

def debug_board(board):
    # rows are backwards
    for row in range(len(board)-1,-1,-1):
        board_row = board[row]
        sys.stderr.write(f"{' '.join(board_char(a) for a in board_row)}\n")

def parsemove(move):
    row = int(move[1])-1
    if move[0] > "i": # skip i
        col = ord(move[0]) - ord("a") - 1
    else:
        col = ord(move[0]) - ord("a")
    return [row, col]

def format_move(col, row):
    if col == None:
        return "PASS"

    r = str(row + 1)
    if col >= ord("i") - ord("a"):
        c = chr(ord("a") + col + 1)
    else:
        c = chr(ord("a") + col)
    return c + r

def random_move(board, color):
    col = None
    row = None
    for i in range(1000):
        col = random.randrange(boardsize[0])
        row = random.randrange(boardsize[1])
        if 0 == board[row][col]:
            break
    return [col, row]

def play_moves(board, color, moves):
    move_string = " ".join(format_move(m[0], m[1]) for m in moves)
    print(f"= {move_string}\n")
    for m in moves:
        board[m[1]][m[0]] = color

while True:
    line = input().strip().split(" ")
    cmd = line[0]
    args = line[1:]

    sys.stderr.write(f"BOT RECEIVED: {cmd} {args}\n")

    match cmd:
        case "list_commands":
            print("""= aa_confirm_safety
accurate_approxlib
accuratelib
advance_random_seed
all_legal
all_move_values
analyze_eyegraph
analyze_semeai
analyze_semeai_after_move
attack
attack_either
black
block_off
boardsize
break_in
captures
clear_board
clear_cache
color
combination_attack
combination_defend
connect
countlib
cputime
decrease_depths
defend
defend_both
disconnect
does_attack
does_defend
does_surround
dragon_data
dragon_status
dragon_stones
draw_search_area
dump_stack
echo
echo_err
estimate_score
eval_eye
experimental_score
eye_data
final_score
final_status
final_status_list
findlib
finish_sgftrace
fixed_handicap
followup_influence
genmove
genmove_black
genmove_white
get_connection_node_counter
get_handicap
get_komi
get_life_node_counter
get_owl_node_counter
get_random_seed
get_reading_node_counter
get_trymove_counter
gg-undo
gg_genmove
half_eye_data
help
increase_depths
initial_influence
invariant_hash_for_moves
invariant_hash
is_legal
is_surrounded
kgs-genmove_cleanup
known_command
komi
ladder_attack
last_move
level
limit_search
list_commands
list_stones
loadsgf
move_influence
move_probabilities
move_reasons
move_uncertainty
move_history
name
new_score
orientation
owl_attack
owl_connection_defends
owl_defend
owl_does_attack
owl_does_defend
owl_substantial
owl_threaten_attack
owl_threaten_defense
place_free_handicap
play
popgo
printsgf
protocol_version
query_boardsize
query_orientation
quit
reg_genmove
report_uncertainty
reset_connection_node_counter
reset_life_node_counter
reset_owl_node_counter
reset_reading_node_counter
reset_search_mask
reset_trymove_counter
restricted_genmove
same_dragon
set_free_handicap
set_random_seed
set_search_diamond
set_search_limit
showboard
start_sgftrace
surround_map
tactical_analyze_semeai
test_eyeshape
time_left
time_settings
top_moves
top_moves_black
top_moves_white
tryko
trymove
tune_move_ordering
unconditional_status
undo
version
white
worm_cutstone
worm_data
worm_stones
""")
        case "boardsize":
            boardsize = [int(args[0]), int(args[0])]
            board = [[0 for i in range(boardsize[0])] for j in range(boardsize[1])]

            print("= \n\n")

        case "clear_board":
            # TODO: clear board
            print("= \n")
        case "komi":
            komi = float(args[0])
            print("= \n")
        case "set_free_handicap":
            for move in args:
                (row, col) = parsemove(move)
                board[row][col] = 1
                handicap += 1
            print("= \n")
        case "place_free_handicap":
            handicap = int(args[0])
            moves = []
            for i in range(handicap):
                for j in range(1000):
                    move = random_move(board, 1)
                    if 0 == moves.count(move):
                        break
                moves.append(move)
            play_moves(board, 1, moves)
        case "play":
            if args[0] == "white":
                color = 2
            else:
                color = 1
            (row, col) = parsemove(args[1])
            board[row][col] = color
            print("= \n")
        case "genmove":
            if args[0] == "white":
                color = 2
            else:
                color = 1
            move = random_move(board, color)
            play_moves(board, color, [move])
        case "quit":
            quit()
        case _:
            debug("UNKNOWN COMMAND")

    if board:
        nl = "\n"
        debug_board(board)
