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
    board = [["." for x in range(0, width - 2)] for y in range(0, height - 2)]
    # put some rooms on the board, max h/w is half of board h/w
    for room_num in range(1, random.randint(3, 8)):
        room_gen(board)
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
    walkable = ['.', '#', '+', ',', 'D']
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


def room_gen(board):
    ''' generates empty room on the board '''
    # set room parameters
    r_height = random.randint(5, len(board) / 2)
    r_width = random.randint(5, len(board[0]) / 2)
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
        for room_row in range(row_pointer + 1, row_pointer + r_height - 1):
            for room_col in range(col_pointer + 1, col_pointer + r_width - 1):
                board[room_row][room_col] = ','
    else:
        room_gen(board)
    # step 4: scan if making door is possible
    for row in range(row_pointer, row_pointer + r_height):
        for column in range(col_pointer, col_pointer + r_width):
            surr = check_pos_around(board, row, column)
            # check if not next to end of board
            if '' in surr.values():
                pass
            # check if can be door (vertical wall)
            elif surr['n'] == surr['s'] == 'X' and (surr['w'] == ',' or surr['e'] == ','):
                board[row][column] = 'D'
            # check if can be door (horizontal wall)
            elif surr['w'] == surr['e'] == 'X' and (surr['n'] == ',' or surr['s'] == ','):
                board[row][column] = 'D'
    # step 5: make door
    door_not_added = True
    while door_not_added:
        for row in range(row_pointer, row_pointer + r_height):
            for column in range(col_pointer, col_pointer + r_width):
                if board[row][column] == 'D':
                    if random.randint(1, 20) == 1:
                        board[row][column] = '+'
                        door_not_added = False
    # step 6: close the walls
    for row in range(row_pointer, row_pointer + r_height):
        for column in range(col_pointer, col_pointer + r_width):
            if board[row][column] == 'D':
                board[row][column] = 'X'


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
    for row in board:
        for column in row:
            surr = check_pos_around(board, row, column)
            if surr['n'] == surr['s'] == 'X' and (surr['w'] == ',' or surr['e'] == ','):
                board[row][column] = ''
