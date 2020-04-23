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
    row_num = player['row_position']
    col_num = player['column_position']
    board[row_num][col_num] = player['icon']


def read_board_from_file(file_name):
    '''
    Reads board from txt file

    Args:
    file_name: comma delimited file

    Returns:
    list of lists
    '''
    pass


def movement(key, player, board):
    ''' moves the player position, if movement is allowed '''
    key_choice = ['w', 's', 'a', 'd']
    column_next = [0, 0, -1, 1]
    row_next = [-1, 1, 0, 0]
    walkable = ['.','#','+']
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
            player['column_position'] += column_next[key_choice.index(option)]
            player['row_position'] += row_next[key_choice.index(option)]
            return


def check_pos_value(board_col, board_row, board):
    ''' return what is in the given position on the map '''
    pos_value = board[board_row][board_col]
    return pos_value
