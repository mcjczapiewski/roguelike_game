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
    board = [[' ' for x in range(0, width - 2)] for y in range(0, height - 2)]
    # put some rooms on the board, max h/w is half of board h/w
    for room_num in range(1, random.randint(3, 8)):
        room_gen(board)
    # make paths
    path_gen(board)
    # return board
    return board


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
    walkable = [' ', '#', '+', ',', '.']
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
            elif board[check_row][check_col] not in walkable:
                return
            # move player to the next locations
            player['column_position'] += column_next[key_choice.index(option)]
            player['row_position'] += row_next[key_choice.index(option)]
            return


def room_gen(board):
    ''' generates empty room on the board '''
    # set room parameters
    try:
        r_height = random.randint(5, len(board) / 2)
        r_width = random.randint(5, len(board[0]) / 2)
    except RecursionError:
        r_height = 5
        r_width = 5
    # step 1: select random place on the board to start
    row_pointer = random.randint(0, len(board) - r_height)
    col_pointer = random.randint(0, len(board[0]) - r_width)
    # step 2: scan if making room is possible
    can_build = True
    for room_row in range(row_pointer, row_pointer + r_height):
        for room_col in range(col_pointer, col_pointer + r_width):
            if board[room_row][room_col] == 'X' or board[room_row][room_col] == ',':
                can_build = False
    # step 3: draw a room
    if can_build:
        for room_row in range(row_pointer, row_pointer + r_height):
            for room_col in range(col_pointer, col_pointer + r_width):
                board[room_row][room_col] = 'X'
        corridor_connector_list = []
        for room_row in range(row_pointer + 1, row_pointer + r_height - 1):
            for room_col in range(col_pointer + 1, col_pointer + r_width - 1):
                board[room_row][room_col] = ','
                temp = (room_row, room_col)
                corridor_connector_list.append(temp)
        # set corridor connector
        corridor_connector = random.choice(corridor_connector_list)
        board[corridor_connector[0]][corridor_connector[1]] = 'C'
    else:
        room_gen(board)


def check_pos_around(board, row_num, col_num):
    ''' creates a list of values around current position '''
    surrounding = {
        'n': '',  # value of field to the north
        'e': '',  # value of field to the east
        's': '',  # value of field to the south
        'w': '',  # value of field to the west
    }
    # set north
    if row_num == 0:
        surrounding['n'] = ''
    else:
        surrounding['n'] = board[row_num - 1][col_num]
    # set east
    if col_num == len(board[0]) - 1:
        surrounding['e'] = ''
    else:
        surrounding['e'] = board[row_num][col_num + 1]
    # set south
    if row_num == len(board) - 1:
        surrounding['s'] = ''
    else:
        surrounding['s'] = board[row_num + 1][col_num]
    # set west
    if col_num == 0:
        surrounding['w'] = ''
    else:
        surrounding['w'] = board[row_num][col_num - 1]
    return surrounding


def path_gen(board):
    ''' mark walls where making door is possible '''
    # make list of positions of corridor connectors
    corridor_connector_list = []
    for row in range(0, len(board)):
        for column in range(0, len(board[0])):
            if board[row][column] == 'C':
                temp = (row, column)
                corridor_connector_list.append(temp)
    # link connecotrs randomly
    while len(corridor_connector_list) > 1:
        pointer = random.choice(corridor_connector_list)
        corridor_connector_list.remove(pointer)
        next_pointer = random.choice(corridor_connector_list)
        # make list of path positions
        path_list = []
        for path_row in range(min(pointer[0], next_pointer[0]), max(pointer[0], next_pointer[0]) + 1):
            for path_col in range(min(pointer[1], next_pointer[1]), max(pointer[1], next_pointer[1]) + 1):
                temp = (path_row, path_col)
                path_list.append(temp)
        for path_row in range(min(pointer[0], next_pointer[0]) + 1, max(pointer[0], next_pointer[0]) ):
            for path_col in range(min(pointer[1], next_pointer[1]) + 1, max(pointer[1], next_pointer[1]) ):
                temp = (path_row, path_col)
                path_list.remove(temp)
        # change empty positions to path
        for path_row, path_col in path_list:
            if board[path_row][path_col] == ' ':
                board[path_row][path_col] = '.'
        # move pointer
        pointer = next_pointer
