import random


def create_board(width, height):
    '''
    Creates a new game board based on input parameters.

    Args:
    int: The width of the board
    int: The height of the board

    Returns:
    list: Game board
    '''
    # create list of lists where:
    # width == sublist length, height == number of sublists
    matrix = [["." for x in range(0, width - 2)] for y in range(0, height - 2)]
    # put some rooms on the board
    room_gen(matrix, 5, 3)
    room_gen(matrix, 6, 4)
    room_gen(matrix, 4, 7)
    # return board
    return matrix


def put_player_on_board(board, player):
    '''
    Modifies the game board by placing the player icon at its coordinates.

    Args:
    list: The game board
    dictionary: The player information containing the icon and coordinates

    Returns:
    Nothing
    '''
    # set temp to what is in the filed before player stands there
    player['temp_field'] = board[player['row_position']][player['column_position']]
    # put player in the position
    board[player['row_position']][player['column_position']] = player['icon']


def movement(key, player, board):
    ''' moves the player position, if movement is allowed '''
    # retrieve the original value of the field
    board[player['row_position']][player['column_position']] = player['temp_field']
    # movement
    key_choice = ['w', 's', 'a', 'd']
    column_next = [0, 0, -1, 1]
    row_next = [-1, 1, 0, 0]
    walkable = ['.', '#', '+']   
    for option in key_choice:
        if key == option:
            # next position
            check_col = player['column_position'] + column_next[key_choice.index(option)]
            check_row = player['row_position'] + row_next[key_choice.index(option)]
            # validate if after the move, player still on board
            if check_col not in range(0, len(board[0])):
                return
            elif check_row not in range(0, len(board)):
                return
            elif check_pos_value(check_col, check_row, board) not in walkable:
                return
            # move player to the next locations
            player['column_position'] += column_next[key_choice.index(option)]
            player['row_position'] += row_next[key_choice.index(option)]
            return


def check_pos_value(board_col, board_row, board):
    ''' return what is in the given position on the map '''
    pos_value = board[board_row][board_col]
    return pos_value


def room_gen(board, r_height, r_width):
    ''' generates empty room on the board '''
    # step 1: select random place on the board to start
    row_pointer = random.randint(0, len(board) - r_height)
    col_pointer = random.randint(0, len(board[0]) - r_width)
    # step 2: scan if making room is possible
    can_build = True
    for room_row in range(row_pointer, row_pointer + r_height):
        for room_col in range(col_pointer, col_pointer + r_width):
            if board[room_row][room_col] == 'X':
                can_build = False
    # step 3: draw a room
    if can_build == True:
        for room_row in range(row_pointer, row_pointer + r_height):
            for room_col in range(col_pointer, col_pointer + r_width):
                board[room_row][room_col] = 'X'
        for room_row in range(row_pointer + 1, row_pointer + r_height - 1):
            for room_col in range(col_pointer + 1, col_pointer + r_width - 1):
                board[room_row][room_col] = '.'
    else:
        room_gen(board, r_height, r_width)



# for row in create_board(50, 30):
#     print("".join(row))



def create_level(board):
    pass
