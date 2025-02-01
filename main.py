import datetime
import math
import copy
import numpy as np

player_time = 0
opponent_time = 0

def input(txtfile):
    with open(txtfile, 'r') as file:
        player = file.readline().strip()
        t = file.readline().strip()
        time = t.split()
        global player_time
        global opponent_time
        player_time = float(time[0])
        opponent_time = float(time[1])
        game_board = [list(file.readline().strip()) for i in range(12)]  
        opponent = "X"
        if player == "X":
            opponent = "O"   

    depth = 1 if player_time < 20 else 2 if player_time < 60 else 3 if player_time < 120 else 4
    
    if len(legal_moves(player, opponent, game_board)) < 10:
        depth += 1

    if player_time > opponent_time:
        depth += 1
    # depth = 6
    # if player_time <= 50:
    #     depth = 2        
    # elif player_time <= 150:
    #     depth = 4
    
    
    
    current_time = datetime.datetime.now()
    possibility = minimax(player, opponent, game_board, depth)  
    output(possibility)
    end_time = datetime.datetime.now()
    print(end_time-current_time)
        
        
        
        
            

def legal_moves(player, opponent, game_board):
    possible_moves = []
    
    neighbor_coordinates = [(-1, -1), (0, -1), (1, -1), (-1, 0), (1, 0), (-1, 1), (0, 1), (1, 1)]

    
    for i in range(12):
        for j in range(12): 
            for tuple in neighbor_coordinates: 
                
                if game_board[i][j] == player: 
                    updated_i = i + tuple[0]
                    updated_j = j + tuple[1]
                    if ((updated_i) == -1 or (updated_i) == 12 or (updated_j) == -1 or (updated_j) == 12):
                        continue
                    else:
                        if game_board[updated_i][updated_j] == player or game_board[updated_i][updated_j] == ".":
                            continue
                        elif game_board[updated_i][updated_j] == opponent:
                            while((updated_i) != -1 and (updated_i) != 12 and (updated_j) != -1 and (updated_j) != 12):
                                if game_board[updated_i][updated_j] == opponent:
                                    updated_i = updated_i + tuple[0] 
                                    updated_j = updated_j + tuple[1]
                                elif game_board[updated_i][updated_j] == player:
                                    break
                                elif game_board[updated_i][updated_j] == ".":
                                    if ((updated_i, updated_j)) not in possible_moves:
                                        possible_moves.append((updated_i, updated_j))
                                    break

    return possible_moves

def update_game_board(player, opponent, old_game_board, possibility):
    game_board = copy.deepcopy(old_game_board)

    if possibility == (None, None):
        return game_board
    
    neighbors = [(-1, -1), (0, -1), (1, -1), (-1, 0), (1, 0), (-1, 1), (0, 1), (1, 1)]
    game_board[possibility[0]][possibility[1]] = player
    for tuples in neighbors:
        updated_row = possibility[0] + tuples[0]
        updated_column = possibility[1] + tuples[1]
        if ((updated_row) == -1 or (updated_row) == 12 or (updated_column) == -1 or (updated_column) == 12):
            continue            
        else:

            if game_board[updated_row][updated_column] == player or game_board[updated_row][updated_column] == ".":
                continue
            elif game_board[updated_row][updated_column] == opponent:
                while((updated_row) != -1 and (updated_row) != 12 and (updated_column) != -1 and (updated_column) != 12):
                    if game_board[updated_row][updated_column] == opponent: 
                        updated_row = updated_row + tuples[0] 
                        updated_column = updated_column + tuples[1]
                    elif game_board[updated_row][updated_column] == ".":
                        break
                    elif game_board[updated_row][updated_column] == player:
                        updated_row = updated_row - tuples[0] 
                        updated_column = updated_column - tuples[1]
                        while ((updated_row) != -1 and (updated_row) != 12 and (updated_column) != -1 and (updated_column) != 12 and game_board[updated_row][updated_column] != game_board[possibility[0]][possibility[1]]):
                            game_board[updated_row][updated_column] = player
                            updated_row = updated_row - tuples[0] 
                            updated_column = updated_column - tuples[1]

                            
                        break
    return game_board
   

# def terminal_test(player, opponent, game_board):
#     possible_moves_player = legal_moves(player, opponent, game_board)
#     possible_moves_opponent = legal_moves(opponent, player, game_board)

#     # print(possible_moves_player, possible_moves_opponent)
#     # print(possible_moves)  
#     isTerminalstate = False
    
#     if possible_moves_player == [] and possible_moves_opponent == []:
#         isTerminalstate = True
#     # print("player_possible moves:", possible_moves_player)
#     # print("opp possible moves:", possible_moves_opponent)

#     return isTerminalstate 
def utility(player,opponent,game_board):
    weights = {
    'corner': 10,
    'edge': 5,
    'mobility': 2,
    'piece': 1
}

  # Calculate the score for each feature
    corner = 0
    edge = 0
    piece = 0

    for i in range(12):
        for j in range(12):
            pc = 1 if  game_board[i][j]==player else 0 if game_board[i][j]=="." else -1

            # If the position is a corner, add the piece to the corner score
            if (i == j == 0 or i == j == 11):
                corner += pc

            # If the position is an edge, add the piece to the edge score
            if (i == 0 or j == 0 or i == 11 or j == 11):
                edge += pc

            # Add the piece to the piece score
            # if piece_at_position == state['player']:
            piece += pc

    # Calculate the score for each feature
    corner *= weights['corner']
    edge *= weights['edge']
    mobility = (len(legal_moves(player, opponent, game_board)) - len(legal_moves(opponent, player, game_board))) * weights['mobility']
    # mobility_score = calculate_mobility_score(state) * weights['mobility'] # Not using mobility score
    piece *= weights['piece']

    # Calculate the total evaluation score
    utility_value = corner + edge + piece + mobility
    return utility_value

def utility1(player, opponent, game_board):

    
    weights = np.array([[10,3, 5, 5, 5, 5, 5, 5, 5, 5, 3,10],
                [3,1,1,1,1,1,1,1,1,1,1,3],
                [5,1,1,1,1,1,1,1,1,1,1,5],
                [5,1,1,1,1,1,1,1,1,1,1,5],
                [5,1,1,1,1,1,1,1,1,1,1,5],
                [5,1,1,1,1,1,1,1,1,1,1,5],
                [5,1,1,1,1,1,1,1,1,1,1,5],
                [5,1,1,1,1,1,1,1,1,1,1,5],
                [5,1,1,1,1,1,1,1,1,1,1,5],
                [5,1,1,1,1,1,1,1,1,1,1,5],
                [3,1,1,1,1,1,1,1,1,1,1,3],
                [10,3, 5, 5, 5, 5, 5, 5, 5, 5, 3,10]])
    
    
    player_utility_value = 0
    opp_utility_value = 0

    for row in range(12):
        for column in range(12):
            if game_board[row][column] == player:
                player_utility_value += weights[row][column]
            elif game_board[row][column] == ".":
                continue
            elif game_board[row][column] == opponent:
                opp_utility_value += weights[row][column]
    
    final_utility_value = player_utility_value - opp_utility_value

    player_possible_moves = len(legal_moves(player, opponent, game_board))
    opp_possible_moves = len(legal_moves(opponent, player, game_board))
    final_possible_moves = 2*(player_possible_moves - opp_possible_moves)
    total_value = final_possible_moves + final_utility_value

    return total_value



# def eval(player, opponent, game_board):
#     updated_game_board = game_board
#     player_count = 0
#     opp_count = 0

#     for row in range(len(updated_game_board)):
#         for column in range(len(updated_game_board)):
#             if updated_game_board[row][column] == ".":
#                 continue
#             elif updated_game_board[row][column] == player:
#                 player_count += 1       
#             elif updated_game_board[row][column] == opponent:
#                 opp_count += 1     

#     if player == "X":
#         player_count += 1
#     elif opponent == "X":
#         opp_count += 1

#     if player_count > opp_count:
#         eval_value = math.inf
#     elif opp_count > player_count:
#         eval_value = - math.inf
#     elif opp_count == player_count:
#          if player_time > opponent_time:
#              eval_value = math.inf
#          elif player_time < opponent_time:
#              eval_value = - math.inf
#          elif player_time == opponent_time:
#              if player == "X":
#                  eval_value = math.inf
#              elif opponent == "X":
#                  eval_value = -math.inf
        

#     return eval_value


def min_value(player, opponent, game_board, alpha, beta, depth):
    if(player=="X"):
        opponent="O"
    else:
        opponent="X"
    v = math.inf
    action = (None, None)

    # if terminal_test(player, opponent, game_board) == True:
    #     print("reached min terminal")
    #     return eval(player, opponent, game_board), (None, None)
    
    possibilities = legal_moves(player, opponent, game_board)    
    if depth == 0 or possibilities == []:
        return utility(player, opponent, game_board), action


    depth = depth - 1
    for possibility in possibilities:
        new_game_board = update_game_board(player, opponent, game_board, possibility)
        maximum_value, max_action = max_value(opponent, player, new_game_board, alpha, beta, depth)

        if maximum_value < v:
            v = maximum_value
            action = possibility  
        # if v <= alpha:
        #     return v, action
        beta = min(beta, v) 
        if beta<=alpha:
            break            

    return v, action

def max_value(player, opponent, game_board, alpha, beta, depth):
    action = (None, None)
    v = -math.inf
    # if terminal_test(player, opponent, game_board) == True:
    #     print("reached max terminal")
    #     return eval(player, opponent, game_board), (None, None)
    possibilities = legal_moves(player, opponent, game_board)   
    if(player=="X"):
        opponent="O"
    else:
        opponent="X"
    if depth == 0 or possibilities == []:
        return utility(player, opponent, game_board), action
    
    depth = depth - 1
    for possibility in possibilities:
        new_game_board = update_game_board(player, opponent, game_board, possibility)
        minimum_value, _ = min_value(opponent, player, new_game_board, alpha, beta, depth)
        if minimum_value > v:       
            action = possibility
            v = minimum_value
        # if v >= beta:
        #     return v, action
        alpha = max(alpha, v)                
        if beta<=alpha:
            break
    
    return v, action
    
def minimax(player, opponent, game_board, depth):

    utility_value, action = max_value(player, opponent, game_board, - math.inf, math.inf, depth)
    return action  

def output(possibility):
    mapping = {0:"a", 1:"b", 2:"c", 3:"d", 4:"e", 5:"f", 6:"g", 7:"h", 8:"i", 9:"j", 10:"k", 11:"l"}
    if possibility[0] != None:
        row = possibility[0] + 1
    else:
        row = ""
    if possibility[1] != None: 
        if possibility[1] in mapping:
            column = mapping[possibility[1]]
        else:
            print("Not in Mapping")
    else:
        column = ""
    
    with open('output.txt', 'w') as file:
        file.write(column+str(row))
        
def main():
    txtfile = "input.txt"
    input(txtfile)
if __name__ == "__main__":
    main()